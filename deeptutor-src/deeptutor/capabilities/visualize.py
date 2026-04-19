"""
Visualize Capability
====================

Three-stage visualization pipeline: Analyze -> Generate -> Review.
Produces SVG or Chart.js code from user requests and conversation context.
"""

from __future__ import annotations

from typing import Any

from deeptutor.capabilities.request_contracts import get_capability_request_schema
from deeptutor.core.capability_protocol import BaseCapability, CapabilityManifest
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream_bus import StreamBus
from deeptutor.core.trace import merge_trace_metadata


class VisualizeCapability(BaseCapability):
    manifest = CapabilityManifest(
        name="visualize",
        description="Generate SVG, Chart.js, or Mermaid visualizations.",
        stages=["analyzing", "generating", "reviewing"],
        tools_used=[],
        cli_aliases=["visualize", "viz"],
        request_schema=get_capability_request_schema("visualize"),
    )

    async def run(self, context: UnifiedContext, stream: StreamBus) -> None:
        from deeptutor.agents.visualize.pipeline import VisualizePipeline
        from deeptutor.capabilities._answer_now import extract_answer_now_context
        from deeptutor.services.llm.config import get_llm_config

        answer_now_payload = extract_answer_now_context(context)
        if answer_now_payload is not None:
            await self._run_answer_now(context, stream, answer_now_payload)
            return

        llm_config = get_llm_config()
        history_context = str(
            context.metadata.get("conversation_context_text", "") or ""
        ).strip()
        render_mode = str(
            context.config_overrides.get("render_mode", "auto") or "auto"
        ).strip().lower()

        pipeline = VisualizePipeline(
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
            api_version=llm_config.api_version,
            language=context.language,
            trace_callback=self._build_trace_bridge(stream),
        )

        # Stage 1: Analyze
        async with stream.stage("analyzing", source=self.name):
            await stream.thinking(
                "Analyzing visualization requirements...",
                source=self.name,
                stage="analyzing",
            )
            analysis = await pipeline.run_analysis(
                user_input=context.user_message,
                history_context=history_context,
                render_mode=render_mode,
            )
            await stream.progress(
                message=f"Render type: {analysis.render_type} — {analysis.description}",
                source=self.name,
                stage="analyzing",
            )

        # Stage 2: Generate code
        async with stream.stage("generating", source=self.name):
            await stream.thinking(
                "Generating visualization code...",
                source=self.name,
                stage="generating",
            )
            code = await pipeline.run_code_generation(
                user_input=context.user_message,
                history_context=history_context,
                analysis=analysis,
            )
            await stream.progress(
                message="Code generated.",
                source=self.name,
                stage="generating",
            )

        # Stage 3: Review & optimise
        async with stream.stage("reviewing", source=self.name):
            await stream.thinking(
                "Reviewing and optimizing code...",
                source=self.name,
                stage="reviewing",
            )
            review = await pipeline.run_review(
                user_input=context.user_message,
                analysis=analysis,
                code=code,
            )
            final_code = review.optimized_code
            if review.changed:
                await stream.progress(
                    message=f"Code optimized: {review.review_notes}",
                    source=self.name,
                    stage="reviewing",
                )
            else:
                await stream.progress(
                    message="Code looks good — no changes needed.",
                    source=self.name,
                    stage="reviewing",
                )

        # Emit final content as a fenced code block for the chat area
        if analysis.render_type == "svg":
            lang_tag = "svg"
        elif analysis.render_type == "mermaid":
            lang_tag = "mermaid"
        else:
            lang_tag = "javascript"
        content_md = f"```{lang_tag}\n{final_code}\n```"
        await stream.content(content_md, source=self.name, stage="reviewing")

        # Structured result for the frontend viewer
        await stream.result(
            {
                "response": content_md,
                "render_type": analysis.render_type,
                "code": {
                    "language": lang_tag,
                    "content": final_code,
                },
                "analysis": analysis.model_dump(),
                "review": review.model_dump(),
            },
            source=self.name,
        )

    async def _run_answer_now(
        self,
        context: UnifiedContext,
        stream: StreamBus,
        payload: dict[str, Any],
    ) -> None:
        """
        Fast-path for ``visualize``: skip analysis + review and emit final
        code in a single structured LLM call. The result envelope mirrors
        the standard pipeline so ``VisualizationViewer`` renders it
        directly.
        """
        import json
        import re

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

        render_mode = str(
            context.config_overrides.get("render_mode", "auto") or "auto"
        ).strip().lower()

        if is_zh:
            system_prompt = (
                "你是 DeepTutor 的可视化代码生成器。用户已经在等待，"
                "请直接输出最终可渲染的代码。"
                "严格输出 JSON：{\"render_type\": \"svg|chartjs|mermaid\", "
                "\"code\": \"...\"}。"
                "code 字段是可直接渲染的源代码（SVG 标签 / Chart.js JS 代码 / Mermaid 文本）。"
            )
            user_prompt = (
                f"用户请求：{original}\n\n"
                f"render_mode：{render_mode}\n\n"
                f"{labeled_block('Current Draft', partial)}\n\n"
                f"{labeled_block('Execution Trace', trace_summary)}\n\n"
                "立即输出符合 schema 的 JSON。"
            )
        else:
            system_prompt = (
                "You are DeepTutor's visualization code generator. The user "
                "is waiting, so emit the final renderable code in one shot. "
                "Output strictly the JSON {\"render_type\": "
                "\"svg|chartjs|mermaid\", \"code\": \"...\"}, where ``code`` "
                "is the renderable source (SVG markup, Chart.js JS, or "
                "Mermaid DSL)."
            )
            user_prompt = (
                f"User request: {original}\n\n"
                f"render_mode hint: {render_mode}\n\n"
                f"{labeled_block('Current Draft', partial)}\n\n"
                f"{labeled_block('Execution Trace', trace_summary)}\n\n"
                "Emit the JSON now."
            )

        trace_meta = build_answer_now_trace_metadata(
            capability=self.name, phase="generating", label="Answer now"
        )
        notice = make_skip_notice(
            capability=self.name,
            language=context.language,
            stages_skipped=["analyzing", "reviewing"],
        )

        chunks: list[str] = []
        async with stream.stage("generating", source=self.name, metadata=trace_meta):
            async for chunk in stream_synthesis(
                stream=stream,
                source=self.name,
                stage="generating",
                trace_meta=trace_meta,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=2400,
                push_content=False,
                response_format={"type": "json_object"},
            ):
                chunks.append(chunk)

        raw = join_chunks(chunks).strip()
        # Strip optional code fences for resilience.
        if raw.startswith("```"):
            raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
            if raw.endswith("```"):
                raw = raw[: -3].rstrip()
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"render_type": "svg", "code": raw}
        if not isinstance(parsed, dict):
            parsed = {"render_type": "svg", "code": str(parsed)}

        render_type = str(parsed.get("render_type") or "svg").strip().lower()
        if render_type not in {"svg", "chartjs", "mermaid"}:
            render_type = "svg"
        final_code = str(parsed.get("code") or "").strip()

        lang_tag = "svg" if render_type == "svg" else (
            "mermaid" if render_type == "mermaid" else "javascript"
        )
        content_md = f"```{lang_tag}\n{final_code}\n```"
        body = (notice + "\n\n" + content_md).strip() if notice else content_md
        await stream.content(body, source=self.name, stage="generating")

        await stream.result(
            {
                "response": body,
                "render_type": render_type,
                "code": {
                    "language": lang_tag,
                    "content": final_code,
                },
                "analysis": {
                    "render_type": render_type,
                    "description": "Answer-now: skipped analysis stage.",
                    "data_description": "",
                    "chart_type": "",
                    "visual_elements": [],
                    "rationale": "",
                },
                "review": {
                    "optimized_code": final_code,
                    "changed": False,
                    "review_notes": "Answer-now: skipped review stage.",
                },
                "metadata": {"answer_now": True},
            },
            source=self.name,
        )

    def _build_trace_bridge(self, stream: StreamBus):
        async def _trace_bridge(update: dict[str, Any]) -> None:
            event = str(update.get("event", "") or "")
            stage = str(update.get("phase") or update.get("stage") or "analyzing")
            base_metadata = {
                key: value
                for key, value in update.items()
                if key
                not in {"event", "state", "response", "chunk", "result", "tool_name", "tool_args"}
            }

            if event != "llm_call":
                return

            state = str(update.get("state", "running"))
            label = str(
                base_metadata.get("label", "") or stage.replace("_", " ").title()
            )
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
                    message=label,
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

        return _trace_bridge
