"""
Deep Question Capability
========================

Multi-agent question generation pipeline: Idea -> Evaluate -> Generate -> Validate.
Wraps the existing ``AgentCoordinator``.
"""

from __future__ import annotations

import base64
import re
import tempfile
from typing import Any

from deeptutor.capabilities.request_contracts import get_capability_request_schema
from deeptutor.core.capability_protocol import BaseCapability, CapabilityManifest
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream_bus import StreamBus
from deeptutor.core.trace import merge_trace_metadata


class DeepQuestionCapability(BaseCapability):
    manifest = CapabilityManifest(
        name="deep_question",
        description="Fast question generation (Template batches -> Generate).",
        stages=["ideation", "generation"],
        tools_used=["rag", "web_search", "code_execution"],
        cli_aliases=["quiz"],
        request_schema=get_capability_request_schema("deep_question"),
    )

    async def run(self, context: UnifiedContext, stream: StreamBus) -> None:
        from deeptutor.agents.question.coordinator import AgentCoordinator
        from deeptutor.capabilities._answer_now import extract_answer_now_context
        from deeptutor.services.llm.config import get_llm_config
        from deeptutor.services.path_service import get_path_service

        answer_now_payload = extract_answer_now_context(context)
        if answer_now_payload is not None:
            await self._run_answer_now(context, stream, answer_now_payload)
            return

        llm_config = get_llm_config()
        kb_name = context.knowledge_bases[0] if context.knowledge_bases else None
        turn_id = str(context.metadata.get("turn_id", "") or context.session_id or "deep-question")
        output_dir = get_path_service().get_task_workspace("deep_question", turn_id)

        overrides = context.config_overrides
        followup_question_context = (
            context.metadata.get("question_followup_context", {}) or {}
        )
        if isinstance(followup_question_context, dict) and followup_question_context.get(
            "question"
        ):
            from deeptutor.agents.question.agents.followup_agent import FollowupAgent

            agent = FollowupAgent(
                language=context.language,
                api_key=llm_config.api_key,
                base_url=llm_config.base_url,
                api_version=llm_config.api_version,
            )
            agent.set_trace_callback(self._build_trace_bridge(stream))
            async with stream.stage("generation", source=self.name):
                answer = await agent.process(
                    user_message=context.user_message,
                    question_context=followup_question_context,
                    history_context=str(
                        context.metadata.get("conversation_context_text", "") or ""
                    ).strip(),
                )
                if answer:
                    await stream.content(answer, source=self.name, stage="generation")
                followup_payload: dict[str, Any] = {
                    "response": answer or "",
                    "mode": "followup",
                    "question_id": followup_question_context.get("question_id", ""),
                }
                cost_meta = self._collect_cost_summary("question")
                if cost_meta:
                    followup_payload["metadata"] = {"cost_summary": cost_meta}
                await stream.result(followup_payload, source=self.name)
            return

        mode = str(overrides.get("mode", "custom") or "custom").strip().lower()
        topic = str(overrides.get("topic") or context.user_message or "").strip()
        num_questions = int(overrides.get("num_questions", 1) or 1)
        difficulty = str(overrides.get("difficulty", "") or "")
        question_type = str(overrides.get("question_type", "") or "")
        preference = str(overrides.get("preference", "") or "")
        history_context = str(
            context.metadata.get("conversation_context_text", "") or ""
        ).strip()
        enabled_tools = set(
            self.manifest.tools_used
            if context.enabled_tools is None
            else context.enabled_tools
        )
        tool_flags_override = {
            "rag": "rag" in enabled_tools,
            "web_search": "web_search" in enabled_tools,
            "code_execution": "code_execution" in enabled_tools,
        }

        coordinator = AgentCoordinator(
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
            api_version=llm_config.api_version,
            kb_name=kb_name,
            language=context.language,
            output_dir=str(output_dir),
            tool_flags_override=tool_flags_override,
            enable_idea_rag="rag" in enabled_tools,
        )

        _trace_bridge = self._build_trace_bridge(stream)

        # Bridge ws_callback to StreamBus
        async def _ws_bridge(update: dict[str, Any]) -> None:
            update_type = update.get("type", "")
            inner = str(update.get("stage", "") or "")
            if update_type == "result" or inner in {"generation", "complete"}:
                stage = "generation"
            elif inner in {"parsing", "extracting", "ideation"}:
                stage = "ideation"
            else:
                stage = "generation" if update_type == "question_update" else "ideation"
            message = self._format_bridge_message(update_type, update)
            metadata = {
                key: value
                for key, value in update.items()
                if key not in {"type", "message"}
            }
            if "question_id" in update:
                metadata.setdefault("trace_id", str(update.get("question_id")))
                metadata.setdefault(
                    "label",
                    f"Generate {self._humanize_question_id(update.get('question_id'))}",
                )
            elif "batch" in update:
                metadata.setdefault("trace_id", f"batch-{update.get('batch')}")
                metadata.setdefault("label", f"Batch {update.get('batch')}")
            metadata["update_type"] = update_type
            metadata.setdefault("phase", stage)
            await stream.progress(
                message=message,
                source=self.name,
                stage=stage,
                metadata=merge_trace_metadata(metadata, {"trace_kind": "progress"}),
            )

        coordinator.set_ws_callback(_ws_bridge)
        if hasattr(coordinator, "set_trace_callback"):
            coordinator.set_trace_callback(_trace_bridge)

        if mode == "mimic":
            result = await self._run_mimic_mode(
                coordinator=coordinator,
                context=context,
                stream=stream,
                overrides=overrides,
            )
            if not result:
                return
        else:
            if not topic:
                await stream.error("Topic is required for custom question generation.", source=self.name)
                return

            async with stream.stage("ideation", source=self.name):
                await stream.thinking("Generating question templates...", source=self.name, stage="ideation")

            result = await coordinator.generate_from_topic(
                user_topic=topic,
                preference=preference,
                num_questions=num_questions,
                difficulty=difficulty,
                question_type=question_type,
                history_context=history_context,
            )

        content = self._render_summary_markdown(result)
        if content:
            await stream.content(content, source=self.name, stage="generation")

        result_payload: dict[str, Any] = {
            "response": content or "No questions generated.",
            "summary": result,
            "mode": mode,
        }
        cost_meta = self._collect_cost_summary("question")
        if cost_meta:
            result_payload["metadata"] = {"cost_summary": cost_meta}
        await stream.result(result_payload, source=self.name)

    async def _run_answer_now(
        self,
        context: UnifiedContext,
        stream: StreamBus,
        payload: dict[str, Any],
    ) -> None:
        """
        Fast-path for ``deep_question``: skip ideation/template generation
        and synthesise a complete quiz in one structured LLM call.

        The result envelope mirrors the standard pipeline (``summary.results``
        with ``qa_pair`` items) so the existing ``QuizViewer`` renders it
        without changes.
        """
        import json

        from deeptutor.capabilities._answer_now import (
            build_answer_now_trace_metadata,
            format_trace_summary,
            join_chunks,
            labeled_block,
            make_skip_notice,
            stream_synthesis,
        )

        is_zh = context.language.lower().startswith("zh")
        original = str(payload.get("original_user_message") or context.user_message).strip()
        partial = str(payload.get("partial_response") or "").strip()
        trace_summary = format_trace_summary(payload.get("events"), language=context.language)

        overrides = context.config_overrides
        topic = str(overrides.get("topic") or original).strip() or original
        num_questions = max(1, int(overrides.get("num_questions", 1) or 1))
        difficulty = str(overrides.get("difficulty", "") or "auto")
        question_type = str(overrides.get("question_type", "") or "auto")

        if is_zh:
            system_prompt = (
                "你是 DeepTutor 的题目生成器。用户已经在等待，请基于现有信息直接输出一组题目。"
                "严格输出 JSON：{\"questions\": [{\"question_id\": \"q_1\", "
                "\"question\": \"...\", \"question_type\": \"choice|written|coding\", "
                "\"options\": {\"A\": \"...\"}, \"correct_answer\": \"...\", "
                "\"explanation\": \"...\", \"difficulty\": \"...\", "
                "\"concentration\": \"...\"}, ...]}。"
                "若不是 choice 题，options 字段可省略。所有字符串使用 UTF-8。"
            )
            user_prompt = (
                f"用户原始问题/主题：{topic}\n\n"
                f"题量要求：{num_questions}\n"
                f"题型偏好：{question_type}（auto 表示自由选择）\n"
                f"难度偏好：{difficulty}\n\n"
                f"{labeled_block('Current Draft', partial)}\n\n"
                f"{labeled_block('Execution Trace', trace_summary)}\n\n"
                "立即输出符合上述 JSON schema 的题目集合，不要包含其他文字。"
            )
        else:
            system_prompt = (
                "You are DeepTutor's question generator. The user is waiting, "
                "so produce a complete question set in one shot using the "
                "context already gathered. Output strictly the JSON schema "
                "{\"questions\": [{\"question_id\": \"q_1\", \"question\": "
                "\"...\", \"question_type\": \"choice|written|coding\", "
                "\"options\": {\"A\": \"...\"}, \"correct_answer\": \"...\", "
                "\"explanation\": \"...\", \"difficulty\": \"...\", "
                "\"concentration\": \"...\"}, ...]}. Omit ``options`` when the "
                "type is not ``choice``."
            )
            user_prompt = (
                f"Topic: {topic}\n\n"
                f"Number of questions requested: {num_questions}\n"
                f"Preferred type: {question_type} (auto = free choice)\n"
                f"Preferred difficulty: {difficulty}\n\n"
                f"{labeled_block('Current Draft', partial)}\n\n"
                f"{labeled_block('Execution Trace', trace_summary)}\n\n"
                "Emit the JSON object now, no surrounding prose."
            )

        trace_meta = build_answer_now_trace_metadata(
            capability=self.name, phase="generation", label="Answer now"
        )

        notice = make_skip_notice(
            capability=self.name,
            language=context.language,
            stages_skipped=["ideation"],
        )

        chunks: list[str] = []
        async with stream.stage("generation", source=self.name, metadata=trace_meta):
            async for chunk in stream_synthesis(
                stream=stream,
                source=self.name,
                stage="generation",
                trace_meta=trace_meta,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=2400,
                push_content=False,
                response_format={"type": "json_object"},
            ):
                chunks.append(chunk)

        raw = join_chunks(chunks).strip()
        questions = self._parse_answer_now_json(raw, num_questions=num_questions)

        results = [
            {
                "qa_pair": {
                    "question_id": q.get("question_id") or f"q_{idx+1}",
                    "question": q.get("question", ""),
                    "question_type": q.get("question_type", "written"),
                    "options": q.get("options") or {},
                    "correct_answer": q.get("correct_answer", ""),
                    "explanation": q.get("explanation", ""),
                    "difficulty": q.get("difficulty", ""),
                    "concentration": q.get("concentration", ""),
                },
                "metadata": {"answer_now": True},
            }
            for idx, q in enumerate(questions)
        ]
        summary = {"results": results, "mode": "answer_now"}

        markdown = self._render_summary_markdown(summary)
        body = (notice + "\n\n" + markdown).strip() if notice else markdown
        if body:
            await stream.content(body, source=self.name, stage="generation")

        result_payload: dict[str, Any] = {
            "response": body or "No questions generated.",
            "summary": summary,
            "mode": "answer_now",
            "metadata": {"answer_now": True},
        }
        cost_meta = self._collect_cost_summary("question")
        if cost_meta:
            result_payload["metadata"]["cost_summary"] = cost_meta
        await stream.result(result_payload, source=self.name)

    @staticmethod
    def _parse_answer_now_json(raw: str, *, num_questions: int) -> list[dict[str, Any]]:
        """Tolerantly parse the model's JSON answer-now payload.

        We accept either ``{"questions": [...]}`` or a bare list. Anything
        unparseable yields a single placeholder so the UI doesn't crash.
        """
        import json

        if not raw:
            return []
        text = raw.strip()
        # Some models wrap JSON in fences even when response_format=json_object
        # is requested; strip a single fenced block defensively.
        if text.startswith("```"):
            text = text.strip("`")
            if "\n" in text:
                text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[: -3]
            text = text.strip()
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return [
                {
                    "question_id": "q_1",
                    "question": raw[:500],
                    "question_type": "written",
                    "correct_answer": "",
                    "explanation": "Model returned unparseable JSON during answer-now.",
                }
            ]

        if isinstance(parsed, dict):
            items = parsed.get("questions")
        else:
            items = parsed
        if not isinstance(items, list):
            return []
        cleaned = [item for item in items if isinstance(item, dict)]
        return cleaned[: max(num_questions, 1)] if cleaned else []

    @staticmethod
    def _collect_cost_summary(module_name: str) -> dict[str, Any] | None:
        from deeptutor.agents.base_agent import BaseAgent
        stats = BaseAgent._shared_stats.get(module_name)
        if not stats or not stats.calls:
            return None
        s = stats.get_summary()
        stats.reset()
        return {
            "total_cost_usd": s.get("cost_usd", 0),
            "total_tokens": s.get("total_tokens", 0),
            "total_calls": s.get("calls", 0),
        }

    async def _run_mimic_mode(
        self,
        coordinator,
        context: UnifiedContext,
        stream: StreamBus,
        overrides: dict[str, Any],
    ) -> dict[str, Any]:
        paper_path = str(overrides.get("paper_path", "") or "").strip()
        max_questions = int(overrides.get("max_questions", 10) or 10)
        pdf_attachment = next(
            (
                attachment
                for attachment in context.attachments
                if attachment.filename.lower().endswith(".pdf")
                or attachment.type == "pdf"
                or attachment.mime_type == "application/pdf"
            ),
            None,
        )

        if pdf_attachment and pdf_attachment.base64:
            async with stream.stage("ideation", source=self.name):
                await stream.thinking(
                    "Parsing uploaded exam paper and extracting templates...",
                    source=self.name,
                    stage="ideation",
                )

            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as temp_pdf:
                temp_pdf.write(base64.b64decode(pdf_attachment.base64))
                temp_pdf.flush()
                return await coordinator.generate_from_exam(
                    exam_paper_path=temp_pdf.name,
                    max_questions=max_questions,
                    paper_mode="upload",
                    history_context=str(
                        context.metadata.get("conversation_context_text", "") or ""
                    ).strip(),
                )

        if paper_path:
            async with stream.stage("ideation", source=self.name):
                await stream.thinking(
                    "Loading parsed exam paper and extracting templates...",
                    source=self.name,
                    stage="ideation",
                )
            return await coordinator.generate_from_exam(
                exam_paper_path=paper_path,
                max_questions=max_questions,
                paper_mode="parsed",
                history_context=str(
                    context.metadata.get("conversation_context_text", "") or ""
                ).strip(),
            )

        await stream.error(
            "Mimic mode requires either an uploaded PDF or a parsed exam directory.",
            source=self.name,
        )
        return {}

    @staticmethod
    def _format_bridge_message(update_type: str, update: dict[str, Any]) -> str:
        """Build a human-readable progress line from a coordinator ws_callback."""
        if update_type == "progress":
            stage = update.get("stage", "")
            status = update.get("status", "")
            cur = update.get("current", "")
            tot = update.get("total", "")
            qid = update.get("question_id", "")
            batch = update.get("batch", "")
            parts = [f"[{stage}]" if stage else ""]
            if status:
                parts.append(status)
            if cur != "" and tot:
                parts.append(f"({cur}/{tot})")
            if batch:
                parts.append(f"batch={batch}")
            if qid:
                parts.append(f"question={qid}")
            return " ".join(p for p in parts if p) or update_type

        if update_type == "templates_ready":
            count = update.get("count", 0)
            batch = update.get("batch", "")
            templates = update.get("templates", [])
            prefix = f"Templates ready (batch {batch}): {count}" if batch else f"Templates ready: {count}"
            lines = [prefix]
            for t in templates:
                if isinstance(t, dict):
                    lines.append(
                        f"  [{t.get('question_id','')}] {t.get('concentration','')[:80]} "
                        f"({t.get('question_type','')}/{t.get('difficulty','')})"
                    )
            return "\n".join(lines)

        if update_type == "question_update":
            qid = DeepQuestionCapability._humanize_question_id(update.get("question_id", ""))
            current = update.get("current", "")
            total = update.get("total", "")
            return f"Generating {qid} ({current}/{total})"

        if update_type == "result":
            qid = DeepQuestionCapability._humanize_question_id(update.get("question_id", ""))
            idx = update.get("index", "")
            q = update.get("question", {})
            qt = q.get("question_type", "") if isinstance(q, dict) else ""
            diff = q.get("difficulty", "") if isinstance(q, dict) else ""
            success = update.get("success", True)
            ordinal = ""
            if isinstance(idx, int):
                ordinal = f"#{idx + 1}, "
            return f"{qid} done ({ordinal}{qt}/{diff}, success={success})"

        return update.get("message", update_type)

    @staticmethod
    def _humanize_question_id(question_id: Any) -> str:
        raw = str(question_id or "").strip()
        match = re.fullmatch(r"q_(\d+)", raw.lower())
        if match:
            return f"Question {match.group(1)}"
        return raw or "Question"

    def _render_summary_markdown(self, summary: dict[str, Any]) -> str:
        results = summary.get("results", []) if isinstance(summary, dict) else []
        if not results:
            return ""

        lines: list[str] = []
        for idx, item in enumerate(results, 1):
            qa_pair = item.get("qa_pair", {}) if isinstance(item, dict) else {}
            question = qa_pair.get("question", "")
            if not question:
                continue

            lines.append(f"### Question {idx}\n")
            lines.append(question)

            options = qa_pair.get("options", {})
            if isinstance(options, dict) and options:
                for key, value in options.items():
                    lines.append(f"- {key}. {value}")

            answer = qa_pair.get("correct_answer", "")
            if answer:
                lines.append(f"\n**Answer:** {answer}")

            explanation = qa_pair.get("explanation", "")
            if explanation:
                lines.append(f"\n**Explanation:** {explanation}")

            lines.append("")

        return "\n".join(lines).strip()

    def _build_trace_bridge(self, stream: StreamBus):
        async def _trace_bridge(update: dict[str, Any]) -> None:
            event = str(update.get("event", "") or "")
            stage = str(update.get("phase") or update.get("stage") or "generation")
            base_metadata = {
                key: value
                for key, value in update.items()
                if key
                not in {"event", "state", "response", "chunk", "result", "tool_name", "tool_args"}
            }

            if event == "llm_call":
                state = str(update.get("state", "running"))
                label = str(update.get("label", "") or "")
                if state == "running":
                    await stream.progress(
                        message=label,
                        source=self.name,
                        stage=stage,
                        metadata=merge_trace_metadata(
                            base_metadata,
                            {"trace_kind": "call_status", "call_state": "running"},
                        ),
                    )
                    return
                if state == "streaming":
                    chunk = str(update.get("chunk", "") or "")
                    if chunk:
                        await stream.thinking(
                            chunk,
                            source=self.name,
                            stage=stage,
                            metadata=merge_trace_metadata(
                                base_metadata,
                                {"trace_kind": "llm_chunk"},
                            ),
                        )
                    return
                if state == "complete":
                    was_streaming = update.get("streaming", False)
                    if not was_streaming:
                        response = str(update.get("response", "") or "")
                        if response:
                            await stream.thinking(
                                response,
                                source=self.name,
                                stage=stage,
                                metadata=merge_trace_metadata(
                                    base_metadata,
                                    {"trace_kind": "llm_output"},
                                ),
                            )
                    await stream.progress(
                        message="",
                        source=self.name,
                        stage=stage,
                        metadata=merge_trace_metadata(
                            base_metadata,
                            {"trace_kind": "call_status", "call_state": "complete"},
                        ),
                    )
                    return
                if state == "error":
                    await stream.error(
                        str(update.get("response", "") or "LLM call failed."),
                        source=self.name,
                        stage=stage,
                        metadata=merge_trace_metadata(
                            base_metadata,
                            {"trace_kind": "call_status", "call_state": "error"},
                        ),
                    )
                    return

            if event == "tool_call":
                await stream.tool_call(
                    tool_name=str(update.get("tool_name", "") or "tool"),
                    args=update.get("tool_args", {}) or {},
                    source=self.name,
                    stage=stage,
                    metadata=merge_trace_metadata(
                        base_metadata,
                        {"trace_kind": "tool_call"},
                    ),
                )
                return

            if event == "tool_result":
                state = str(update.get("state", "complete"))
                result = str(update.get("result", "") or "")
                if state == "error":
                    await stream.error(
                        result,
                        source=self.name,
                        stage=stage,
                        metadata=merge_trace_metadata(
                            base_metadata,
                            {"trace_kind": "tool_result"},
                        ),
                    )
                    return
                await stream.tool_result(
                    tool_name=str(update.get("tool_name", "") or "tool"),
                    result=result,
                    source=self.name,
                    stage=stage,
                    metadata=merge_trace_metadata(
                        base_metadata,
                        {"trace_kind": "tool_result"},
                    ),
                )

        return _trace_bridge
