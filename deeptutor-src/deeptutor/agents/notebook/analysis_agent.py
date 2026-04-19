"""Notebook analysis agent for cross-record grounding."""

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

from deeptutor.core.stream import StreamEvent, StreamEventType
from deeptutor.core.trace import build_trace_metadata, derive_trace_metadata, new_call_id
from deeptutor.services.llm import clean_thinking_tags, get_llm_config, get_token_limit_kwargs
from deeptutor.services.llm import complete as llm_complete, stream as llm_stream
from deeptutor.services.llm import stream as llm_stream
from deeptutor.utils.json_parser import parse_json_response

logger = logging.getLogger(__name__)

EventSink = Callable[[StreamEvent], Awaitable[None]]


def _clip_text(value: str, limit: int) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n...[truncated]"


class NotebookAnalysisAgent:
    """Analyze selected notebook records before the main capability runs."""

    def __init__(self, language: str = "en") -> None:
        self.language = "zh" if str(language or "en").lower().startswith("zh") else "en"
        self.llm_config = get_llm_config()
        self.model = getattr(self.llm_config, "model", None)
        self.api_key = getattr(self.llm_config, "api_key", None)
        self.base_url = getattr(self.llm_config, "base_url", None)
        self.api_version = getattr(self.llm_config, "api_version", None)
        self.binding = getattr(self.llm_config, "binding", None) or "openai"

    async def analyze(
        self,
        *,
        user_question: str,
        records: list[dict[str, Any]],
        emit: EventSink | None = None,
    ) -> str:
        thinking_text = await self._stage_thinking(user_question=user_question, records=records, emit=emit)
        selected_records = await self._stage_acting(
            user_question=user_question,
            thinking_text=thinking_text,
            records=records,
            emit=emit,
        )
        observation = await self._stage_observing(
            user_question=user_question,
            thinking_text=thinking_text,
            selected_records=selected_records,
            emit=emit,
        )

        if emit is not None:
            await emit(
                StreamEvent(
                    type=StreamEventType.RESULT,
                    source="notebook_analysis",
                    metadata={
                        "observation": observation,
                        "selected_record_ids": [record.get("id", "") for record in selected_records],
                    },
                )
            )
        return observation

    async def _stage_thinking(
        self,
        *,
        user_question: str,
        records: list[dict[str, Any]],
        emit: EventSink | None,
    ) -> str:
        trace_meta = build_trace_metadata(
            call_id=new_call_id("notebook-thinking"),
            phase="thinking",
            label="Notebook reasoning",
            call_kind="llm_reasoning",
            trace_id="notebook-thinking",
            trace_role="thought",
            trace_group="stage",
        )
        await self._emit_stage_start("notebook_thinking", trace_meta, emit)
        chunks: list[str] = []
        async for chunk in llm_stream(
            prompt=self._thinking_prompt(user_question, records),
            system_prompt=self._thinking_system_prompt(),
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            api_version=self.api_version,
            binding=self.binding,
            temperature=0.2,
            **self._token_kwargs(900),
        ):
            if not chunk:
                continue
            chunks.append(chunk)
            if emit is not None:
                await emit(
                    StreamEvent(
                        type=StreamEventType.THINKING,
                        source="notebook_analysis",
                        stage="notebook_thinking",
                        content=chunk,
                        metadata=derive_trace_metadata(trace_meta, trace_kind="llm_chunk"),
                    )
                )
        await self._emit_stage_end("notebook_thinking", trace_meta, emit)
        return clean_thinking_tags("".join(chunks), self.binding, self.model).strip()

    async def _stage_acting(
        self,
        *,
        user_question: str,
        thinking_text: str,
        records: list[dict[str, Any]],
        emit: EventSink | None,
    ) -> list[dict[str, Any]]:
        trace_meta = build_trace_metadata(
            call_id=new_call_id("notebook-acting"),
            phase="acting",
            label="Notebook selection",
            call_kind="tool_planning",
            trace_id="notebook-acting",
            trace_role="tool",
            trace_group="tool_call",
        )
        await self._emit_stage_start("notebook_acting", trace_meta, emit)
        _chunks: list[str] = []
        async for _c in llm_stream(
            prompt=self._acting_prompt(user_question, thinking_text, records),
            system_prompt=self._acting_system_prompt(),
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            api_version=self.api_version,
            binding=self.binding,
            temperature=0.1,
            **self._token_kwargs(500),
        ):
            _chunks.append(_c)
        raw = "".join(_chunks)
        payload = parse_json_response(raw, logger_instance=logger, fallback={})
        selected_ids = payload.get("selected_record_ids") if isinstance(payload, dict) else []
        if not isinstance(selected_ids, list):
            selected_ids = []

        wanted = []
        seen: set[str] = set()
        record_map = {str(record.get("id", "")): record for record in records}
        for record_id in selected_ids:
            key = str(record_id or "").strip()
            if not key or key in seen or key not in record_map:
                continue
            wanted.append(record_map[key])
            seen.add(key)
            if len(wanted) >= 5:
                break

        if not wanted:
            wanted = records[: min(5, len(records))]

        if emit is not None:
            await emit(
                StreamEvent(
                    type=StreamEventType.TOOL_CALL,
                    source="notebook_analysis",
                    stage="notebook_acting",
                    content="notebook_lookup",
                    metadata=derive_trace_metadata(
                        trace_meta,
                        trace_kind="tool_call",
                        args={"selected_record_ids": [record.get("id", "") for record in wanted]},
                    ),
                )
            )
            await emit(
                StreamEvent(
                    type=StreamEventType.TOOL_RESULT,
                    source="notebook_analysis",
                    stage="notebook_acting",
                    content=self._tool_result_text(wanted),
                    metadata=derive_trace_metadata(
                        trace_meta,
                        trace_kind="tool_result",
                        tool="notebook_lookup",
                    ),
                )
            )
        await self._emit_stage_end("notebook_acting", trace_meta, emit)
        return wanted

    async def _stage_observing(
        self,
        *,
        user_question: str,
        thinking_text: str,
        selected_records: list[dict[str, Any]],
        emit: EventSink | None,
    ) -> str:
        trace_meta = build_trace_metadata(
            call_id=new_call_id("notebook-observing"),
            phase="observing",
            label="Notebook observation",
            call_kind="llm_observation",
            trace_id="notebook-observing",
            trace_role="observe",
            trace_group="stage",
        )
        await self._emit_stage_start("notebook_observing", trace_meta, emit)
        chunks: list[str] = []
        async for chunk in llm_stream(
            prompt=self._observing_prompt(user_question, thinking_text, selected_records),
            system_prompt=self._observing_system_prompt(),
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            api_version=self.api_version,
            binding=self.binding,
            temperature=0.2,
            **self._token_kwargs(1200),
        ):
            if not chunk:
                continue
            chunks.append(chunk)
            if emit is not None:
                await emit(
                    StreamEvent(
                        type=StreamEventType.OBSERVATION,
                        source="notebook_analysis",
                        stage="notebook_observing",
                        content=chunk,
                        metadata=derive_trace_metadata(trace_meta, trace_kind="observation"),
                    )
                )
        await self._emit_stage_end("notebook_observing", trace_meta, emit)
        return clean_thinking_tags("".join(chunks), self.binding, self.model).strip()

    async def _emit_stage_start(
        self,
        stage: str,
        metadata: dict[str, Any],
        emit: EventSink | None,
    ) -> None:
        if emit is None:
            return
        await emit(
            StreamEvent(
                type=StreamEventType.STAGE_START,
                source="notebook_analysis",
                stage=stage,
                metadata=metadata,
            )
        )

    async def _emit_stage_end(
        self,
        stage: str,
        metadata: dict[str, Any],
        emit: EventSink | None,
    ) -> None:
        if emit is None:
            return
        await emit(
            StreamEvent(
                type=StreamEventType.STAGE_END,
                source="notebook_analysis",
                stage=stage,
                metadata=metadata,
            )
        )

    def _thinking_system_prompt(self) -> str:
        if self.language == "zh":
            return (
                "你是 DeepTutor 的 notebook thinking 阶段。"
                "你会先阅读用户问题与 notebook 摘要列表，判断要从哪些历史记录中提取细节。"
                "输出内部思考，不要直接回答用户。"
            )
        return (
            "You are DeepTutor's notebook thinking stage. "
            "Review the user question and notebook summaries, then reason about which saved records matter most. "
            "Output internal reasoning only, not the final answer."
        )

    def _acting_system_prompt(self) -> str:
        if self.language == "zh":
            return (
                "你是 DeepTutor 的 notebook acting 阶段。"
                "你必须只输出 JSON：{\"selected_record_ids\": [最多5个id]}。"
                "优先选择最能支撑当前问题的记录，避免冗余。"
            )
        return (
            "You are DeepTutor's notebook acting stage. "
            'Output JSON only: {"selected_record_ids": [up to 5 ids]}. '
            "Choose the records most useful for the current question."
        )

    def _observing_system_prompt(self) -> str:
        if self.language == "zh":
            return (
                "你是 DeepTutor 的 notebook observing 阶段。"
                "请基于用户问题、thinking、以及选中历史记录的细节，产出一份供后续主能力使用的上下文总结。"
                "总结必须结构化、紧凑，并区分已知事实、可复用内容、仍需谨慎的点。"
                "不要用第一人称描述内部流程。"
            )
        return (
            "You are DeepTutor's notebook observing stage. "
            "Synthesize the user question, the prior reasoning, and the selected record details into a compact context note "
            "for the main capability. Distinguish confirmed facts, reusable material, and uncertainties."
        )

    def _thinking_prompt(self, user_question: str, records: list[dict[str, Any]]) -> str:
        catalog = self._summary_catalog(records)
        if self.language == "zh":
            return (
                f"用户问题：\n{user_question.strip() or '(empty)'}\n\n"
                f"可用 notebook 摘要：\n{catalog}\n\n"
                "请思考：当前问题最需要哪些历史信息？哪些记录可能只需要摘要，哪些必须查看原文细节？"
            )
        return (
            f"User question:\n{user_question.strip() or '(empty)'}\n\n"
            f"Available notebook summaries:\n{catalog}\n\n"
            "Reason about which saved records matter most and which ones likely require full detail."
        )

    def _acting_prompt(
        self,
        user_question: str,
        thinking_text: str,
        records: list[dict[str, Any]],
    ) -> str:
        catalog = self._summary_catalog(records)
        if self.language == "zh":
            return (
                f"用户问题：\n{user_question.strip() or '(empty)'}\n\n"
                f"[Thinking]\n{thinking_text or '(empty)'}\n\n"
                f"可选记录：\n{catalog}\n\n"
                "请只返回最值得查看细节的记录 id，最多 5 个。"
            )
        return (
            f"User question:\n{user_question.strip() or '(empty)'}\n\n"
            f"[Thinking]\n{thinking_text or '(empty)'}\n\n"
            f"Available records:\n{catalog}\n\n"
            "Return only the ids of the records whose full details should be inspected, up to 5."
        )

    def _observing_prompt(
        self,
        user_question: str,
        thinking_text: str,
        selected_records: list[dict[str, Any]],
    ) -> str:
        detailed_blocks = "\n\n".join(
            [
                "\n".join(
                    [
                        f"Record ID: {record.get('id', '')}",
                        f"Notebook: {record.get('notebook_name', '')}",
                        f"Title: {record.get('title', '')}",
                        f"Summary: {record.get('summary', '')}",
                        f"Content:\n{_clip_text(record.get('output', ''), 2500)}",
                    ]
                )
                for record in selected_records
            ]
        ) or "(none)"
        if self.language == "zh":
            return (
                f"用户问题：\n{user_question.strip() or '(empty)'}\n\n"
                f"[Thinking]\n{thinking_text or '(empty)'}\n\n"
                f"[Detailed Records]\n{detailed_blocks}\n\n"
                "请输出 notebook 分析结论，用于注入后续主能力。"
                "建议包含：1. 与当前问题直接相关的历史信息；2. 可复用的结论/草稿/上下文；3. 需要谨慎处理的地方。"
            )
        return (
            f"User question:\n{user_question.strip() or '(empty)'}\n\n"
            f"[Thinking]\n{thinking_text or '(empty)'}\n\n"
            f"[Detailed Records]\n{detailed_blocks}\n\n"
            "Produce the notebook analysis output that will be injected into the main capability. "
            "Include directly relevant history, reusable conclusions or drafts, and any caveats."
        )

    def _summary_catalog(self, records: list[dict[str, Any]]) -> str:
        lines: list[str] = []
        for record in records:
            lines.append(
                " | ".join(
                    [
                        f"id={record.get('id', '')}",
                        f"notebook={record.get('notebook_name', '')}",
                        f"type={record.get('type', '')}",
                        f"title={_clip_text(record.get('title', ''), 80)}",
                        f"summary={_clip_text(record.get('summary', '') or record.get('title', ''), 240)}",
                    ]
                )
            )
        return "\n".join(lines) if lines else "(none)"

    def _tool_result_text(self, records: list[dict[str, Any]]) -> str:
        blocks = []
        for record in records:
            blocks.append(
                "\n".join(
                    [
                        f"- {record.get('id', '')} | {record.get('notebook_name', '')} | {record.get('title', '')}",
                        _clip_text(record.get("output", ""), 400),
                    ]
                )
            )
        return "\n\n".join(blocks) if blocks else "(none)"

    def _token_kwargs(self, max_tokens: int) -> dict[str, Any]:
        if not self.model:
            return {}
        return get_token_limit_kwargs(self.model, max_tokens)
