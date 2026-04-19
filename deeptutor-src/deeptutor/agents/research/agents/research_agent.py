#!/usr/bin/env python
"""
ResearchAgent - Research Agent
Responsible for executing research logic and tool call decisions
"""

from collections.abc import Awaitable, Callable
import json
import re
from string import Template
from typing import Any

from deeptutor.agents.base_agent import BaseAgent
from deeptutor.core.trace import build_trace_metadata, new_call_id
from deeptutor.runtime.registry.tool_registry import get_tool_registry
from deeptutor.agents.research.data_structures import DynamicTopicQueue, TopicBlock

from ..utils.json_utils import extract_json_from_text


class ResearchAgent(BaseAgent):
    """Research Agent"""

    _MODE_TO_STYLE = {
        "notes": "study_notes",
        "report": "report",
        "comparison": "comparison",
        "learning_path": "learning_path",
    }

    @staticmethod
    def _build_trace_meta(
        *,
        label: str,
        iteration: int,
        block_id: str = "",
        trace_role: str = "thought",
    ) -> dict[str, Any]:
        return build_trace_metadata(
            call_id=new_call_id("research-step"),
            phase="researching",
            label=label,
            call_kind="llm_reasoning",
            trace_role=trace_role,
            trace_kind="llm_reasoning",
            iteration=iteration,
            block_id=block_id or None,
            trace_group="research_round" if block_id else None,
        )

    def __init__(
        self,
        config: dict[str, Any],
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
    ):
        language = config.get("system", {}).get("language", "zh")
        super().__init__(
            module_name="research",
            agent_name="research_agent",
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            language=language,
            config=config,
        )
        self.researching_config = config.get("researching", {})
        self.max_iterations = self.researching_config.get("max_iterations", 5)
        # Iteration mode: "fixed" (must explore all iterations) or "flexible" (can stop early)
        # In "fixed" mode, agent should be more conservative about declaring knowledge sufficient
        # In "flexible" mode (auto), agent can stop early when knowledge is truly sufficient
        self.iteration_mode = self.researching_config.get("iteration_mode", "fixed")
        self.enable_rag = self.researching_config.get("enable_rag", True)
        # Web search: global switch (tools.web_search.enabled) has higher priority
        # Only enabled when both global switch and module switch are True
        tools_web_search_enabled = (
            config.get("tools", {}).get("web_search", {}).get("enabled", True)
        )
        research_web_search_enabled = self.researching_config.get("enable_web_search", False)
        self.enable_web_search = tools_web_search_enabled and research_web_search_enabled
        self.enable_paper_search = self.researching_config.get("enable_paper_search", False)
        self.enable_run_code = self.researching_config.get("enable_run_code", True)
        # Store enabled tools list for prompt generation
        self.enabled_tools = self.researching_config.get("enabled_tools", ["RAG"])
        self._tool_registry = get_tool_registry()
        intent_mode = str(config.get("intent", {}).get("mode", "") or "")
        reporting_style = str(config.get("reporting", {}).get("style", "") or "")
        self._research_style = reporting_style or self._MODE_TO_STYLE.get(intent_mode, "report")

    @staticmethod
    def _convert_to_template_format(template_str: str) -> str:
        """
        Convert {var} style placeholders to $var style for string.Template.
        This avoids conflicts with LaTeX braces like {\rho}.
        """
        # Only convert simple {var_name} patterns, not nested or complex ones
        return re.sub(r"\{(\w+)\}", r"$\1", template_str)

    def _safe_format(self, template_str: str, **kwargs) -> str:
        """
        Safe string formatting using string.Template to avoid LaTeX brace conflicts.
        """
        converted = self._convert_to_template_format(template_str)
        return Template(converted).safe_substitute(**kwargs)

    def _get_mode_contract(self, stage: str) -> str:
        return (
            self.get_prompt("mode_contracts", f"{self._research_style}_{stage}", "")
            or ""
        ).strip()

    def _generate_available_tools_text(self) -> str:
        """Generate available tools list based on enabled tool configuration."""
        tool_names = self._get_enabled_prompt_tools()
        if not tool_names:
            return "(no tools available)"
        return self._tool_registry.build_prompt_text(
            tool_names,
            format="aliases",
            language=self.language,
        )

    def _generate_tool_phase_guidance(self) -> str:
        """Generate phased tool guidance based on enabled tools."""
        tool_names = self._get_enabled_prompt_tools()
        guidance = self._tool_registry.build_prompt_text(
            tool_names,
            format="phased",
            language=self.language,
        )
        if guidance:
            return guidance
        if self.language == "zh":
            return "当前没有额外工具可用，请围绕现有知识继续分析。"
        return "No extra tools are currently enabled; continue reasoning with the knowledge already gathered."

    def _get_enabled_prompt_tools(self) -> list[str]:
        tool_names: list[str] = []
        if self.enable_rag:
            tool_names.append("rag")
        if self.enable_paper_search:
            tool_names.append("paper_search")
        if self.enable_web_search:
            tool_names.append("web_search")
        if self.enable_run_code:
            tool_names.append("code_execution")
        deduped: list[str] = []
        for name in tool_names:
            if name not in deduped:
                deduped.append(name)
        return deduped

    def _is_llm_only_mode(self) -> bool:
        return not self._get_enabled_prompt_tools()

    async def _run_llm_self_research(
        self,
        *,
        topic: str,
        overview: str,
        query: str,
        current_knowledge: str,
        iteration: int,
        block_id: str,
    ) -> str:
        """Research internally with the model when no external tool is enabled."""
        if self.language == "zh":
            system_prompt = (
                "你是一个深度研究助理。在没有任何外部工具可用时，你需要只基于模型已有知识，"
                "围绕给定查询做谨慎、结构化的内部研究。不要假装访问了网页、论文或知识库。"
                "如果某些内容是常识性推断或可能存在不确定性，请明确说明。"
            )
            user_prompt = self._safe_format(
                """
请对下面的研究查询进行一次“纯 LLM 内部研究”。

主话题：{topic}
话题概览：{overview}
当前研究轮次：{iteration}
本轮查询：{query}
已有知识：
{current_knowledge}

模式聚焦：
{mode_instruction}

要求：
1. 只能基于模型已有知识进行分析，不要声称使用了外部来源。
2. 直接产出可被后续笔记/报告阶段吸收的研究内容。
3. 优先回答本轮查询对应的知识缺口，并保持结构化、信息密度高。
4. 如果存在不确定点，单独列出“Known Uncertainties”。

仅输出 JSON：
{{
  "content": "结构化研究内容",
  "confidence": "high/medium/low",
  "limitations": ["不确定点1", "不确定点2"]
}}
""",
                topic=topic,
                overview=overview or "(无)",
                iteration=iteration,
                query=query,
                current_knowledge=current_knowledge[:3000] if current_knowledge else "(无)",
                mode_instruction=self._get_mode_contract("research") or "(无额外模式指令)",
            )
        else:
            system_prompt = (
                "You are a deep-research assistant. When no external tools are enabled, "
                "you must research using only the model's internal knowledge. Do not claim "
                "to have searched the web, papers, or a knowledge base. Explicitly note uncertainty "
                "when needed."
            )
            user_prompt = self._safe_format(
                """
Perform one round of LLM-only internal research for the following query.

Main Topic: {topic}
Topic Overview: {overview}
Current Iteration: {iteration}
This Round's Query: {query}
Current Knowledge:
{current_knowledge}

Mode-Specific Focus:
{mode_instruction}

Requirements:
1. Use only the model's internal knowledge; do not pretend to access outside sources.
2. Produce content that can be directly absorbed by the later note/report stages.
3. Focus on the specific knowledge gap behind this query and keep the result structured and information-dense.
4. If anything is uncertain, list it under "Known Uncertainties".

Only output JSON:
{{
  "content": "Structured research content",
  "confidence": "high/medium/low",
  "limitations": ["uncertainty 1", "uncertainty 2"]
}}
""",
                topic=topic,
                overview=overview or "(none)",
                iteration=iteration,
                query=query,
                current_knowledge=current_knowledge[:3000] if current_knowledge else "(none)",
                mode_instruction=self._get_mode_contract("research") or "(no extra mode instruction)",
            )

        _chunks: list[str] = []
        async for _c in self.stream_llm(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            stage="llm_self_research",
            trace_meta=self._build_trace_meta(
                label="LLM self research",
                iteration=iteration,
                block_id=block_id,
            ),
        ):
            _chunks.append(_c)
        response = "".join(_chunks)

        try:
            data = extract_json_from_text(response)
        except Exception:
            data = None
        if isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False)
        return json.dumps({"content": response}, ensure_ascii=False)

    def _generate_research_depth_guidance(self, iteration: int, used_tools: list[str]) -> str:
        """
        Generate research depth guidance based on iteration, used tools, and iteration_mode

        Args:
            iteration: Current iteration number
            used_tools: List of tools already used

        Returns:
            Research depth guidance text
        """
        # Determine research phase based on max_iterations
        early_threshold = max(2, self.max_iterations // 3)
        middle_threshold = max(4, self.max_iterations * 2 // 3)

        if iteration <= early_threshold:
            phase = "early"
            phase_desc = f"Early Stage (Iteration 1-{early_threshold})"
            guidance = "Focus on building foundational knowledge using RAG/knowledge base tools."
        elif iteration <= middle_threshold:
            phase = "middle"
            phase_desc = f"Middle Stage (Iteration {early_threshold + 1}-{middle_threshold})"
            if self.enable_paper_search or self.enable_web_search:
                guidance = "Consider using Paper/Web search to add academic depth and real-time information."
            else:
                guidance = "Deepen knowledge coverage, explore different angles of the topic."
        else:
            phase = "late"
            phase_desc = f"Late Stage (Iteration {middle_threshold + 1}+)"
            guidance = "Fill knowledge gaps, ensure completeness before concluding."

        # Tool diversity analysis
        unique_tools = set(used_tools)
        available_tools = []
        if self.enable_rag and "rag" not in unique_tools:
            available_tools.append("rag")
        if self.enable_paper_search and "paper_search" not in unique_tools:
            available_tools.append("paper_search")
        if self.enable_web_search and "web_search" not in unique_tools:
            available_tools.append("web_search")

        diversity_hint = ""
        if available_tools and phase != "early":
            diversity_hint = f"\n**Tool Diversity Suggestion**: Consider using unexplored tools: {', '.join(available_tools)}"

        # Iteration mode specific guidance
        if self.iteration_mode == "flexible":
            # Auto/flexible mode: agent can decide when to stop
            mode_guidance = """
**Iteration Mode: FLEXIBLE (Auto)**
You have autonomy to decide when knowledge is sufficient. You may stop early if:
- Core concepts are well covered from multiple angles
- Key questions about the topic have been addressed
- Further iterations would only add marginal value
However, ensure you have made meaningful exploration before concluding."""
        else:
            # Fixed mode: more conservative about stopping
            mode_guidance = """
**Iteration Mode: FIXED**
This mode requires thorough exploration. Be CONSERVATIVE about declaring knowledge sufficient:
- In early iterations (first third), rarely conclude sufficiency
- In middle iterations, require strong evidence of comprehensive coverage
- Only in late iterations, conclude if truly comprehensive"""

        return f"""
**Research Phase Guidance** ({phase_desc}):
{guidance}

Current iteration: {iteration}/{self.max_iterations}
Tools already used: {", ".join(used_tools) if used_tools else "None"}
{diversity_hint}
{mode_guidance}
"""

    def _generate_online_search_instruction(self) -> str:
        """
        Generate online search guidance instructions from YAML config

        Returns:
            Online search guidance text, returns empty string if not enabled
        """
        if not self.enable_web_search and not self.enable_paper_search:
            return ""

        if self.enable_web_search and self.enable_paper_search:
            instruction = self.get_prompt("guidance", "online_search_both")
            if instruction:
                return instruction
        elif self.enable_web_search:
            instruction = self.get_prompt("guidance", "online_search_web_only")
            if instruction:
                return instruction
        elif self.enable_paper_search:
            instruction = self.get_prompt("guidance", "online_search_paper_only")
            if instruction:
                return instruction

        return ""

    def _generate_iteration_mode_criteria(self, iteration: int) -> str:
        """
        Generate iteration mode specific criteria for sufficiency check from YAML config

        Args:
            iteration: Current iteration number

        Returns:
            Iteration mode criteria text
        """
        # Calculate early threshold
        early_threshold = max(2, self.max_iterations // 3)

        if self.iteration_mode == "flexible":
            criteria = self.get_prompt("guidance", "iteration_mode_flexible")
            if criteria:
                return criteria
            # Fallback if YAML not configured
            return "- **FLEXIBLE mode (Auto)**: You have autonomy to decide sufficiency."
        else:
            criteria = self.get_prompt("guidance", "iteration_mode_fixed")
            if criteria:
                return criteria.format(early_threshold=early_threshold)
            # Fallback if YAML not configured
            return f"- **FIXED mode**: Be CONSERVATIVE about declaring sufficiency. Early threshold: {early_threshold}"

    async def plan_next_step(
        self,
        topic: str,
        overview: str,
        current_knowledge: str,
        iteration: int,
        existing_topics: list[str] | None = None,
        used_tools: list[str] | None = None,
    ) -> dict[str, Any]:
        """Evaluate sufficiency and plan the next tool call in one LLM round."""
        system_prompt = self.get_prompt("system", "role")
        if not system_prompt:
            raise ValueError(
                "ResearchAgent missing system prompt, please configure system.role in prompts/{lang}/research_agent.yaml"
            )
        user_prompt_template = self.get_prompt("process", "plan_next_step")
        if not user_prompt_template:
            raise ValueError(
                "ResearchAgent missing plan_next_step prompt, please configure process.plan_next_step in prompts/{lang}/research_agent.yaml"
            )

        topics_text = "(No other topics)"
        if existing_topics:
            topics_text = "\n".join([f"- {t}" for t in existing_topics])

        online_search_instruction = self._generate_online_search_instruction()
        research_depth_guidance = self._generate_research_depth_guidance(iteration, used_tools or [])
        iteration_mode_criteria = self._generate_iteration_mode_criteria(iteration)
        available_tools_text = self._generate_available_tools_text()
        tool_phase_guidance = self._generate_tool_phase_guidance()

        user_prompt = self._safe_format(
            user_prompt_template,
            topic=topic,
            overview=overview,
            current_knowledge=current_knowledge[:3000] if current_knowledge else "(None)",
            iteration=iteration,
            max_iterations=self.max_iterations,
            existing_topics=topics_text,
            available_tools=available_tools_text,
            tool_phase_guidance=tool_phase_guidance,
            research_depth_guidance=research_depth_guidance,
            online_search_instruction=online_search_instruction,
            iteration_mode_criteria=iteration_mode_criteria,
            mode_instruction=self._get_mode_contract("research"),
        )
        _chunks: list[str] = []
        async for _c in self.stream_llm(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            stage="plan_next_step",
            trace_meta=self._build_trace_meta(
                label="Plan next step",
                iteration=iteration,
                trace_role="plan",
            ),
        ):
            _chunks.append(_c)
        response = "".join(_chunks)

        from ..utils.json_utils import ensure_json_dict, ensure_keys

        data = extract_json_from_text(response)
        obj = ensure_json_dict(data)
        ensure_keys(obj, ["is_sufficient", "sufficiency_reason"])
        return obj

    async def process(
        self,
        topic_block: TopicBlock,
        call_tool_callback: Callable[[str, str], Awaitable[str]],
        note_agent,
        citation_manager,
        queue: DynamicTopicQueue,
        manager_agent,
        config: dict[str, Any],
        progress_callback: Callable[[str, Any], None] | None = None,
    ) -> dict[str, Any]:
        """
        Execute research for a single topic block (complete multi-round retrieval loop)

        Args:
            topic_block: Topic block to research
            call_tool_callback: Tool call callback function (tool_type, query) -> raw_answer
            note_agent: NoteAgent instance for generating summaries
            citation_manager: CitationManager instance for managing citations
            queue: DynamicTopicQueue instance for getting existing topic list
            manager_agent: ManagerAgent instance for adding new topics
            config: Configuration dictionary for getting parameters
            progress_callback: Optional callback for iteration progress (event_type, **data)

        Returns:
            Research result
            {
                "block_id": str,
                "iterations": int,
                "final_knowledge": str,
                "tools_used": List[str],
                "queries_used": List[dict],
                "status": str
            }
        """
        block_id_prefix = f"[{topic_block.block_id}]"
        print(f"\n{block_id_prefix} {'=' * 70}")
        print(f"{block_id_prefix} 🔬 ResearchAgent - Executing Research")
        print(f"{block_id_prefix} {'=' * 70}")
        print(f"{block_id_prefix} Topic: {topic_block.sub_topic}")
        print(f"{block_id_prefix} Overview: {topic_block.overview}")
        print(
            f"{block_id_prefix} Max iterations: {self.max_iterations}, Mode: {self.iteration_mode}\n"
        )

        iteration = 0
        current_knowledge = ""
        tools_used = []
        queries_used = []  # Track all queries for progress display
        llm_only_mode = self._is_llm_only_mode()

        # Helper to send progress updates
        def send_progress(event_type: str, **data):
            if progress_callback:
                try:
                    progress_callback(event_type, **data)
                except Exception:
                    pass  # Ignore callback errors

        while iteration < self.max_iterations:
            iteration += 1
            print(f"{block_id_prefix} \n【Iteration {iteration}/{self.max_iterations}】")

            # Send iteration started progress
            send_progress(
                "iteration_started",
                iteration=iteration,
                max_iterations=self.max_iterations,
                tools_used=tools_used.copy(),
            )

            # Step 1: Check if knowledge is sufficient
            send_progress(
                "checking_sufficiency", iteration=iteration, max_iterations=self.max_iterations
            )
            plan = await self.plan_next_step(
                topic=topic_block.sub_topic,
                overview=topic_block.overview,
                current_knowledge=current_knowledge,
                iteration=iteration,
                existing_topics=queue.list_topics(),
                used_tools=tools_used,
            )

            if plan.get("is_sufficient", False):
                print(
                    f"{block_id_prefix}   ✓ Current topic is sufficient, ending research for this topic"
                )
                send_progress(
                    "knowledge_sufficient",
                    iteration=iteration,
                    max_iterations=self.max_iterations,
                    reason=plan.get("sufficiency_reason", plan.get("reason", "")),
                )
                break

            send_progress(
                "generating_query",
                iteration=iteration,
                max_iterations=self.max_iterations,
                merged_planning=True,
            )

            # Dynamic splitting: if new topic is discovered, add to queue tail
            new_topic = plan.get("new_sub_topic")
            new_overview = plan.get("new_overview")
            new_topic_score = float(plan.get("new_topic_score") or 0)
            should_add_new_topic = plan.get("should_add_new_topic")
            min_score = config.get("researching", {}).get("new_topic_min_score", 0.75)
            new_topic_reason = plan.get("new_topic_reason")

            if isinstance(new_topic, str) and new_topic.strip():
                trimmed_topic = new_topic.strip()
                if should_add_new_topic is False:
                    print(
                        f"{block_id_prefix}   ↩️ LLM determined not to add new topic《{trimmed_topic}》, skipping"
                    )
                elif new_topic_score < min_score:
                    print(
                        f"{block_id_prefix}   ↩️ New topic《{trimmed_topic}》score {new_topic_score:.2f} below threshold {min_score:.2f}, skipping"
                    )
                else:
                    # Support both sync and async manager_agent
                    import inspect

                    add_topic_method = getattr(manager_agent, "add_new_topic")
                    if inspect.iscoroutinefunction(add_topic_method):
                        added = await add_topic_method(trimmed_topic, new_overview or "")
                    else:
                        added = manager_agent.add_new_topic(trimmed_topic, new_overview or "")
                    if added:
                        print(f"{block_id_prefix}   ✓ Added new topic《{trimmed_topic}》to queue")
                        send_progress(
                            "new_topic_added",
                            iteration=iteration,
                            max_iterations=self.max_iterations,
                            new_topic=trimmed_topic,
                            new_overview=new_overview or "",
                        )
                if new_topic_reason:
                    print(f"{block_id_prefix}     Reason: {new_topic_reason}")

            query = plan.get("query", "").strip()
            tool_type = "llm_self_research" if llm_only_mode else plan.get("tool_type", "rag")
            rationale = plan.get("rationale", "")

            if not query:
                print(f"{block_id_prefix}   ⚠️ Generated query is empty, skipping this iteration")
                send_progress(
                    "query_empty", iteration=iteration, max_iterations=self.max_iterations
                )
                continue

            # Track this query
            query_info = {
                "query": query,
                "tool_type": tool_type,
                "rationale": rationale,
                "iteration": iteration,
            }
            queries_used.append(query_info)

            # Send progress before tool call
            send_progress(
                "tool_calling",
                iteration=iteration,
                max_iterations=self.max_iterations,
                tool_type=tool_type,
                query=query,
                rationale=rationale,
            )

            # Step 3: Call tool
            if llm_only_mode:
                raw_answer = await self._run_llm_self_research(
                    topic=topic_block.sub_topic,
                    overview=topic_block.overview,
                    query=query,
                    current_knowledge=current_knowledge,
                    iteration=iteration,
                    block_id=topic_block.block_id,
                )
            else:
                raw_answer = await call_tool_callback(tool_type, query)

            # Send progress after tool call
            send_progress(
                "tool_completed",
                iteration=iteration,
                max_iterations=self.max_iterations,
                tool_type=tool_type,
                query=query,
            )

            # Step 4: Get citation ID from CitationManager (unified ID generation)
            send_progress(
                "processing_notes", iteration=iteration, max_iterations=self.max_iterations
            )

            # Get citation_id from CitationManager - support both sync and async
            import inspect

            if hasattr(
                citation_manager, "get_next_citation_id_async"
            ) and inspect.iscoroutinefunction(
                getattr(citation_manager, "get_next_citation_id_async", None)
            ):
                citation_id = await citation_manager.get_next_citation_id_async(
                    stage="research", block_id=topic_block.block_id
                )
            else:
                citation_id = citation_manager.get_next_citation_id(
                    stage="research", block_id=topic_block.block_id
                )

            # Step 5: NoteAgent records summary with the citation ID
            trace = await note_agent.process(
                tool_type=tool_type,
                query=query,
                raw_answer=raw_answer,
                citation_id=citation_id,
                topic=topic_block.sub_topic,
                context=current_knowledge,
            )
            topic_block.add_tool_trace(trace)

            # Step 6: Add citation information to citation manager
            # Support both sync and async citation_manager
            if hasattr(citation_manager, "add_citation") and callable(
                getattr(citation_manager, "add_citation", None)
            ):
                add_citation_method = getattr(citation_manager, "add_citation")
                if inspect.iscoroutinefunction(add_citation_method):
                    await add_citation_method(
                        citation_id=citation_id,
                        tool_type=tool_type,
                        tool_trace=trace,
                        raw_answer=raw_answer,
                    )
                else:
                    citation_manager.add_citation(
                        citation_id=citation_id,
                        tool_type=tool_type,
                        tool_trace=trace,
                        raw_answer=raw_answer,
                    )
            else:
                # Fallback to sync version
                citation_manager.add_citation(
                    citation_id=citation_id,
                    tool_type=tool_type,
                    tool_trace=trace,
                    raw_answer=raw_answer,
                )

            # Step 7: Update knowledge (accumulate summaries)
            current_knowledge = (current_knowledge + "\n" + trace.summary).strip()
            topic_block.iteration_count = iteration
            tools_used.append(tool_type)

            # Send iteration completed progress
            send_progress(
                "iteration_completed",
                iteration=iteration,
                max_iterations=self.max_iterations,
                tool_type=tool_type,
                query=query,
                tools_used=tools_used.copy(),
            )

        return {
            "block_id": topic_block.block_id,
            "iterations": iteration,
            "final_knowledge": current_knowledge,
            "tools_used": tools_used,
            "queries_used": queries_used,
            "status": "completed" if iteration < self.max_iterations else "max_iterations_reached",
        }


__all__ = ["ResearchAgent"]
