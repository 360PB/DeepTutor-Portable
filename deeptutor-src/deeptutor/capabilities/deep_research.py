"""
Deep Research Capability
========================

Multi-agent deep research with report generation.
Wraps ``ResearchPipeline`` as a first-class built-in capability.
"""

from __future__ import annotations

import asyncio
from typing import Any
from deeptutor.capabilities.request_contracts import get_capability_request_schema
from deeptutor.core.capability_protocol import BaseCapability, CapabilityManifest
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream_bus import StreamBus
from deeptutor.core.trace import derive_trace_metadata, merge_trace_metadata, new_call_id


class DeepResearchCapability(BaseCapability):
    manifest = CapabilityManifest(
        name="deep_research",
        description="Multi-agent deep research with report generation.",
        stages=["rephrasing", "decomposing", "researching", "reporting"],
        tools_used=["rag", "web_search", "paper_search", "code_execution"],
        cli_aliases=["research"],
        request_schema=get_capability_request_schema("deep_research"),
    )

    async def run(self, context: UnifiedContext, stream: StreamBus) -> None:
        from deeptutor.agents.research.research_pipeline import ResearchPipeline
        from deeptutor.agents.research.request_config import (
            build_research_runtime_config,
            validate_research_request_config,
        )
        from deeptutor.capabilities._answer_now import extract_answer_now_context
        from deeptutor.services.config import load_config_with_main
        from deeptutor.services.llm.config import get_llm_config

        answer_now_payload = extract_answer_now_context(context)
        if answer_now_payload is not None:
            await self._run_answer_now(context, stream, answer_now_payload)
            return

        llm_config = get_llm_config()
        kb_name = context.knowledge_bases[0] if context.knowledge_bases else None
        topic = context.user_message
        enabled_tools = set(
            self.manifest.tools_used
            if context.enabled_tools is None
            else context.enabled_tools
        )
        request_config = validate_research_request_config(context.config_overrides)

        # Consistency normalization: if "kb" is selected as a research source
        # but no knowledge base is actually attached, drop "kb" from the
        # effective sources. This avoids any code path falling through to a
        # placeholder KB at the pipeline layer. If after the downgrade no
        # source is left at all, surface a clear error to the user.
        if "kb" in request_config.sources and not kb_name:
            request_config = request_config.model_copy(
                update={
                    "sources": [src for src in request_config.sources if src != "kb"],
                }
            )
            await stream.progress(
                message=(
                    "Knowledge base source was selected, but no knowledge "
                    "base is attached; KB retrieval is disabled for this "
                    "research run."
                ),
                source=self.name,
                stage="rephrasing",
                metadata={"trace_kind": "warning", "reason": "kb_without_kb_name"},
            )
            if not request_config.sources:
                await stream.error(
                    "Deep research requires at least one source. Please "
                    "either attach a knowledge base or enable web/papers "
                    "sources.",
                    source=self.name,
                )
                return

        config = build_research_runtime_config(
            base_config=load_config_with_main("main.yaml"),
            request_config=request_config,
            enabled_tools=enabled_tools,
            kb_name=kb_name,
        )

        def _normalize_stage(stage: str) -> str:
            mapping = {
                "rephrase": "rephrasing",
                "check_satisfaction": "rephrasing",
                "decompose": "decomposing",
                "decompose_no_rag": "decomposing",
                "check_sufficiency": "researching",
                "generate_query_plan": "researching",
                "plan_next_step": "researching",
                "generate_summary": "researching",
                "deduplicate": "reporting",
                "generate_outline": "reporting",
                "write_introduction": "reporting",
                "write_section_body": "reporting",
                "write_conclusion": "reporting",
                "write_full_report": "reporting",
            }
            return mapping.get(stage, stage or "researching")

        def _stage_card(stage: str, status: str = "") -> str:
            if stage in {"rephrasing"} or status.startswith(("planning_started", "rephrase")):
                return "understand"
            if stage in {"decomposing"} or status.startswith(("decompose", "queue_")):
                return "decompose"
            if stage == "reporting":
                return "result"
            return "evidence"

        def _progress_message(data: dict[str, Any]) -> str:
            status = str(data.get("status") or data.get("type") or "").strip()
            pretty_map = {
                "planning_started": "Clarifying the research question",
                "rephrase_completed": "Refined the research focus",
                "rephrase_skipped": "Using the original topic directly",
                "decompose_started": "Breaking the topic into subtopics",
                "decompose_completed": "Prepared subtopics for investigation",
                "queue_seeded": "Queued a research subtopic",
                "researching_started": "Searching for evidence",
                "block_started": "Investigating a subtopic",
                "block_completed": "Completed one evidence block",
                "researching_completed": "Evidence gathering finished",
                "reporting_started": "Drafting the final result",
                "reporting_completed": "Final result is ready",
            }
            return pretty_map.get(
                status,
                str(data.get("message") or status or data.get("type") or "").strip(),
            )

        async def _emit_progress(data: dict[str, Any]) -> None:
            raw_stage = str(data.get("stage") or "researching")
            stage = _normalize_stage(raw_stage)
            status = str(data.get("status") or data.get("type") or "")
            message = _progress_message(data)
            if not message:
                return
            await stream.progress(
                message=message,
                source=self.name,
                stage=stage,
                metadata={
                    key: value
                    for key, value in data.items()
                    if key not in {"message", "status", "type", "stage"}
                }
                | {
                    "research_stage_card": _stage_card(stage, status),
                    "research_status": status,
                },
            )

        def _progress_cb(data: dict[str, Any]) -> None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                return
            loop.create_task(_emit_progress(data))

        def _label_from_update(update: dict[str, Any], stage: str) -> str:
            agent_name = str(update.get("agent_name") or "")
            raw_stage = str(update.get("stage") or "")
            block_id = str(update.get("block_id") or "")
            iteration = update.get("iteration")

            if agent_name == "rephrase_agent":
                return "Rephrase topic"
            if agent_name == "decompose_agent":
                return "Decompose topic"
            if agent_name == "note_agent":
                return "Summarize evidence"
            if stage == "reporting":
                if raw_stage == "generate_outline":
                    return "Generate outline"
                if raw_stage.startswith("write_"):
                    return "Write report"
                return "Reporting"
            if block_id and isinstance(iteration, int):
                return f"{block_id.replace('_', ' ').title()} · Round {iteration}"
            if block_id:
                return block_id.replace("_", " ").title()
            return "Research step"

        async def _trace_cb(update: dict[str, Any]) -> None:
            event = str(update.get("event", "") or "")
            stage = _normalize_stage(str(update.get("phase") or update.get("stage") or "researching"))
            raw_stage = str(update.get("stage") or "")
            base_metadata = {
                key: value
                for key, value in update.items()
                if key
                not in {"event", "state", "response", "chunk", "result", "tool_name", "tool_args"}
            }
            call_id = str(base_metadata.get("call_id") or new_call_id("research"))
            base_metadata.setdefault("call_id", call_id)
            base_metadata.setdefault("phase", stage)
            base_metadata.setdefault("label", _label_from_update(update, stage))
            base_metadata.setdefault("research_stage_card", _stage_card(stage, raw_stage))

            if event == "llm_call":
                state = str(update.get("state", "running"))
                label = str(base_metadata.get("label", "") or "")
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
                    return

            if event == "tool_call":
                await stream.tool_call(
                    tool_name=str(update.get("tool_name", "") or "tool"),
                    args=update.get("tool_args", {}) or {},
                    source=self.name,
                    stage=stage,
                    metadata=derive_trace_metadata(
                        base_metadata,
                        trace_role="tool",
                        trace_kind="tool_call",
                    ),
                )
                return

            if event == "tool_result":
                state = str(update.get("state", "complete") or "complete")
                result = str(update.get("result", "") or "")
                if state == "error":
                    await stream.error(
                        result,
                        source=self.name,
                        stage=stage,
                        metadata=derive_trace_metadata(
                            base_metadata,
                            trace_role="tool",
                            trace_kind="tool_result",
                        ),
                    )
                    return
                await stream.tool_result(
                    tool_name=str(update.get("tool_name", "") or "tool"),
                    result=result,
                    source=self.name,
                    stage=stage,
                    metadata=derive_trace_metadata(
                        base_metadata,
                        trace_role="tool",
                        trace_kind="tool_result",
                    ),
                )
                return

        confirmed_outline = request_config.confirmed_outline
        conversation_history = context.conversation_history or []

        if confirmed_outline is None:
            outline_items = await self._generate_outline_preview(
                config=config,
                llm_config=llm_config,
                kb_name=kb_name,
                topic=topic,
                stream=stream,
                progress_callback=_progress_cb,
                trace_callback=_trace_cb,
                conversation_history=conversation_history,
            )
            sub_topics_data = (
                [item.model_dump() for item in outline_items]
                if hasattr(outline_items[0], "model_dump")
                else outline_items
            )

            outline_md = self._outline_to_markdown(topic, sub_topics_data)
            await stream.content(outline_md, source=self.name, stage="decomposing")

            await stream.result(
                {
                    "outline_preview": True,
                    "sub_topics": sub_topics_data,
                    "topic": topic,
                    "research_config": {
                        "mode": request_config.mode,
                        "depth": request_config.depth,
                        "sources": list(request_config.sources),
                        **({"manual_subtopics": request_config.manual_subtopics} if request_config.manual_subtopics is not None else {}),
                        **({"manual_max_iterations": request_config.manual_max_iterations} if request_config.manual_max_iterations is not None else {}),
                    },
                },
                source=self.name,
            )
            return

        pre_outline = [
            {"title": item.title, "overview": item.overview}
            for item in confirmed_outline
        ]

        pipeline = ResearchPipeline(
            config=config,
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
            api_version=llm_config.api_version,
            kb_name=kb_name,
            progress_callback=_progress_cb,
            trace_callback=_trace_cb,
            pre_confirmed_outline=pre_outline,
        )

        async with stream.stage("researching", source=self.name):
            await stream.thinking(f"Researching topic: {topic}", source=self.name, stage="researching")
            result = await pipeline.run(topic=topic)

        report = result.get("report", "")
        if report:
            async with stream.stage("reporting", source=self.name):
                await stream.content(report, source=self.name, stage="reporting")

        await stream.result(
            {"response": report, "metadata": result.get("metadata", {})},
            source=self.name,
        )

    async def _run_answer_now(
        self,
        context: UnifiedContext,
        stream: StreamBus,
        payload: dict[str, Any],
    ) -> None:
        """
        Fast-path for ``deep_research``: skip the rephrase/decompose/research
        loop and synthesize the report directly from whatever evidence the
        partial trace already contains.
        """
        from deeptutor.capabilities._answer_now import (
            build_answer_now_trace_metadata,
            format_trace_summary,
            join_chunks,
            labeled_block,
            load_answer_now_prompts,
            make_skip_notice,
            stream_synthesis,
        )

        original = str(payload.get("original_user_message") or context.user_message).strip()
        partial = str(payload.get("partial_response") or "").strip()
        trace_summary = format_trace_summary(payload.get("events"), language=context.language)

        prompts = load_answer_now_prompts("research", context.language)
        system_prompt = str(prompts.get("system", "")).strip()
        user_prompt = str(prompts.get("user_template", "")).format(
            original=original,
            current_draft=labeled_block("Current Draft", partial),
            research_trace=labeled_block("Research Trace", trace_summary),
        )

        trace_meta = build_answer_now_trace_metadata(
            capability=self.name, phase="reporting", label="Answer now"
        )
        notice = make_skip_notice(
            capability=self.name,
            language=context.language,
            stages_skipped=["rephrasing", "decomposing", "researching"],
        )

        async with stream.stage("reporting", source=self.name, metadata=trace_meta):
            if notice:
                await stream.content(notice + "\n\n", source=self.name, stage="reporting")
            chunks: list[str] = []
            async for chunk in stream_synthesis(
                stream=stream,
                source=self.name,
                stage="reporting",
                trace_meta=trace_meta,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=3200,
            ):
                chunks.append(chunk)

        report = join_chunks(chunks)
        full = (notice + "\n\n" + report).strip() if notice else report
        await stream.result(
            {
                "response": full,
                "metadata": {"answer_now": True},
            },
            source=self.name,
        )

    @staticmethod
    def _outline_to_markdown(
        topic: str, sub_topics: list[dict[str, str]]
    ) -> str:
        """Serialize an outline to Markdown so it is persisted in session history."""
        lines = [f"**Research Outline — {topic}**\n"]
        for i, item in enumerate(sub_topics, 1):
            lines.append(f"{i}. **{item.get('title', '')}**")
            overview = item.get("overview", "")
            if overview:
                lines.append(f"   {overview}")
        return "\n".join(lines)

    async def _generate_outline_preview(
        self,
        *,
        config: dict[str, Any],
        llm_config: Any,
        kb_name: str | None,
        topic: str,
        stream: StreamBus,
        progress_callback: Any,
        trace_callback: Any,
        conversation_history: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, str]]:
        """Run only the planning phase (rephrase + decompose) and return sub-topics."""
        from deeptutor.agents.research.research_pipeline import ResearchPipeline

        if conversation_history:
            config = {**config, "conversation_history": conversation_history}

        pipeline = ResearchPipeline(
            config=config,
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
            api_version=llm_config.api_version,
            kb_name=kb_name,
            progress_callback=progress_callback,
            trace_callback=trace_callback,
        )

        async with stream.stage("decomposing", source=self.name):
            await stream.thinking(
                f"Generating research outline for: {topic}",
                source=self.name,
                stage="decomposing",
            )
            optimized_topic = await pipeline._phase1_planning(topic)

        sub_topics = []
        for block in pipeline.queue.blocks:
            sub_topics.append({"title": block.sub_topic, "overview": block.overview})

        return sub_topics
