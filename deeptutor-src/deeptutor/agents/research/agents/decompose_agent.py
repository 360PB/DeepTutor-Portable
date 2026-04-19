#!/usr/bin/env python
"""
DecomposeAgent - Topic decomposition Agent
Responsible for decomposing topics into multiple subtopics and generating overviews for each subtopic
"""

from typing import Any

import json

from deeptutor.agents.base_agent import BaseAgent
from deeptutor.agents.research.data_structures import ToolTrace
from deeptutor.core.trace import build_trace_metadata, new_call_id
from deeptutor.tools.rag_tool import rag_search

from ..utils.json_utils import extract_json_from_text


class DecomposeAgent(BaseAgent):
    """Topic decomposition Agent"""

    _MODE_TO_STYLE = {
        "notes": "study_notes",
        "report": "report",
        "comparison": "comparison",
        "learning_path": "learning_path",
    }

    @staticmethod
    def _build_trace_meta(mode: str) -> dict[str, Any]:
        return build_trace_metadata(
            call_id=new_call_id("research-decompose"),
            phase="decomposing",
            label="Decompose topic",
            call_kind="llm_generation",
            trace_role="plan",
            trace_kind="llm_generation",
            mode=mode,
        )

    def __init__(
        self,
        config: dict[str, Any],
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        kb_name: str | None = None,
    ):
        language = config.get("system", {}).get("language", "zh")
        super().__init__(
            module_name="research",
            agent_name="decompose_agent",
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            language=language,
            config=config,
        )
        rag_cfg = config.get("rag", {}) or {}
        self.kb_name = rag_cfg.get("kb_name") or kb_name or None

        researching_cfg = config.get("researching", {})
        self.enable_rag = researching_cfg.get("enable_rag", True)
        # Defensive: never attempt RAG without a real KB name. The
        # capability/runtime config layer is responsible for stripping
        # ``kb`` from sources when no KB is attached, but this guard keeps
        # the agent safe even when called directly.
        if not self.kb_name:
            self.enable_rag = False

        self.conversation_history: list[dict[str, Any]] = config.get("conversation_history", [])

        self.citation_manager = None
        intent_mode = str(config.get("intent", {}).get("mode", "") or "")
        reporting_style = str(config.get("reporting", {}).get("style", "") or "")
        self._research_style = reporting_style or self._MODE_TO_STYLE.get(intent_mode, "report")

    def set_citation_manager(self, citation_manager):
        """Set citation manager"""
        self.citation_manager = citation_manager

    def _format_conversation_context(self) -> str:
        """Format conversation history into a context block for the LLM."""
        if not self.conversation_history:
            return ""
        parts: list[str] = []
        for msg in self.conversation_history:
            role = msg.get("role", "user")
            content = str(msg.get("content", "")).strip()
            if not content:
                continue
            parts.append(f"[{role}]: {content}")
        if not parts:
            return ""
        return (
            "\n<conversation_history>\n"
            "The following is the conversation history of this session. "
            "If the user's current request references or modifies a previous outline, "
            "use this history as context.\n\n"
            + "\n\n".join(parts)
            + "\n</conversation_history>\n"
        )

    def _get_mode_contract(self, stage: str) -> str:
        return (
            self.get_prompt("mode_contracts", f"{self._research_style}_{stage}", "")
            or ""
        ).strip()

    async def process(
        self, topic: str, num_subtopics: int = 5, mode: str = "manual"
    ) -> dict[str, Any]:
        """
        Decompose topic into subtopics and generate overview for each subtopic

        Args:
            topic: Main topic
            num_subtopics: Expected number of subtopics in manual mode, or maximum limit in auto mode
            mode: Mode, "manual" (manually specify count) or "auto" (auto-generate)

        Returns:
            Dictionary containing decomposition results
            {
                "main_topic": str,
                "sub_topics": [
                    {
                        "title": str,
                        "overview": str
                    },
                    ...
                ],
                "total_subtopics": int,
                "mode": str
            }
        """
        print(f"\n{'=' * 70}")
        print("🔀 DecomposeAgent - Topic Decomposition")
        print(f"{'=' * 70}")
        print(f"Main Topic: {topic}")
        print(f"Mode: {mode}")
        print(f"RAG Enabled: {self.enable_rag}")
        if mode == "auto":
            print(f"Max Subtopic Limit: {num_subtopics}\n")
        else:
            print(f"Expected Subtopic Count: {num_subtopics}\n")

        # If RAG is disabled, use direct LLM generation without RAG context
        if not self.enable_rag:
            print("⚠️ RAG is disabled, generating subtopics directly from LLM...")
            return await self._process_without_rag(topic, num_subtopics, mode)

        print("\n🔍 Step 1: Executing RAG retrieval to get background knowledge...")
        rag_context, source_query = await self._retrieve_background_knowledge(topic)

        print("\n🎯 Step 2: Generating subtopics...")
        if mode == "auto":
            sub_topics = await self._generate_sub_topics_auto(
                topic=topic, rag_context=rag_context, max_subtopics=num_subtopics
            )
        else:
            sub_topics = await self._generate_sub_topics(
                topic=topic, rag_context=rag_context, num_subtopics=num_subtopics
            )

        print(f"✓ Generated {len(sub_topics)} subtopics")

        return {
            "main_topic": topic,
            "sub_queries": [source_query] if source_query else [],
            "rag_context": rag_context,
            "sub_topics": sub_topics,
            "total_subtopics": len(sub_topics),
            "mode": mode,
            "rag_context_summary": "RAG background based on topic",
        }

    async def _retrieve_background_knowledge(self, topic: str) -> tuple[str, str]:
        """Retrieve one background context for lightweight decomposition."""
        source_query = (topic or "").strip()
        if not source_query:
            return "", ""
        if not self.kb_name:
            print("  ⚠️ No knowledge base configured; skipping RAG retrieval.")
            return "", source_query

        try:
            result = await rag_search(query=source_query, kb_name=self.kb_name)
            rag_context = result.get("answer", "")
            print(f"  ✓ Retrieved background knowledge ({len(rag_context)} characters)")

            if self.citation_manager:
                citation_id = self.citation_manager.get_next_citation_id(stage="planning")
                tool_type = "rag"

                import time

                tool_id = f"plan_tool_{int(time.time() * 1000)}"
                raw_answer_json = json.dumps(result, ensure_ascii=False)
                trace = ToolTrace(
                    tool_id=tool_id,
                    citation_id=citation_id,
                    tool_type=tool_type,
                    query=source_query,
                    raw_answer=raw_answer_json,
                    summary=rag_context[:500] if rag_context else "",
                )
                self.citation_manager.add_citation(
                    citation_id=citation_id,
                    tool_type=tool_type,
                    tool_trace=trace,
                    raw_answer=raw_answer_json,
                )

            return rag_context, source_query
        except Exception as e:
            print(f"  ✗ RAG retrieval failed: {e!s}")
            return "", source_query

    async def _process_without_rag(
        self, topic: str, num_subtopics: int, mode: str = "manual"
    ) -> dict[str, Any]:
        """
        Process without RAG: directly generate subtopics from LLM based on topic.
        Used when RAG is disabled by user.

        Args:
            topic: Main topic
            num_subtopics: Number of subtopics to generate (exact for manual, max for auto)
            mode: "manual" or "auto"

        Returns:
            Dictionary containing decomposition results
        """
        print("\n🎯 Generating subtopics directly (no RAG)...")

        system_prompt = self.get_prompt(
            "system",
            "role",
            "You are a research planning expert. Your task is to decompose complex topics into clear subtopics.",
        )
        system_prompt += self._format_conversation_context()

        user_prompt_template = self.get_prompt("process", "decompose_without_rag")
        if not user_prompt_template:
            raise ValueError(
                "DecomposeAgent missing decompose_without_rag prompt, please configure process.decompose_without_rag in prompts/{lang}/decompose_agent.yaml"
            )

        # Build requirement based on mode
        if mode == "auto":
            decompose_requirement = f"""
Quantity Requirements:
Generate between 3 and {num_subtopics} subtopics based on the complexity of the topic.
- For simple topics, generate fewer subtopics (3-4)
- For complex topics, generate more subtopics (up to {num_subtopics})
- Prioritize the most important and distinctive aspects of the topic
"""
        else:
            decompose_requirement = f"""
Quantity Requirements:
Generate exactly {num_subtopics} subtopics. Please ensure exactly {num_subtopics} subtopics are generated, no more, no less.
"""

        user_prompt = user_prompt_template.format(
            topic=topic,
            decompose_requirement=decompose_requirement,
            mode_instruction=self._get_mode_contract("decompose"),
        )

        _chunks: list[str] = []
        async for _c in self.stream_llm(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            stage="decompose_no_rag",
            trace_meta=self._build_trace_meta(mode),
        ):
            _chunks.append(_c)
        response = "".join(_chunks)

        # Parse JSON output
        from ..utils.json_utils import ensure_json_dict, ensure_keys, extract_json_from_text

        data = extract_json_from_text(response)
        try:
            obj = ensure_json_dict(data)
            ensure_keys(obj, ["sub_topics"])
            subs = obj.get("sub_topics", [])
            if not isinstance(subs, list):
                raise ValueError("sub_topics must be an array")
            # Clean and limit subtopics
            cleaned = []
            for it in subs[:num_subtopics]:
                if isinstance(it, dict):
                    cleaned.append(
                        {"title": it.get("title", ""), "overview": it.get("overview", "")}
                    )
            sub_topics = cleaned
        except Exception:
            sub_topics = []

        print(f"✓ Generated {len(sub_topics)} subtopics (without RAG)")

        return {
            "main_topic": topic,
            "sub_queries": [],  # No sub-queries when RAG is disabled
            "rag_context": "",  # No RAG context
            "sub_topics": sub_topics,
            "total_subtopics": len(sub_topics),
            "mode": f"{mode}_no_rag",
            "rag_context_summary": "RAG disabled - subtopics generated directly from LLM",
        }

    async def _generate_sub_topics_auto(
        self, topic: str, rag_context: str, max_subtopics: int
    ) -> list[dict[str, str]]:
        """
        Auto mode: Autonomously generate subtopics based on RAG background

        Args:
            topic: Main topic
            rag_context: RAG background knowledge
            max_subtopics: Maximum subtopic count limit

        Returns:
            Subtopics list
        """
        system_prompt = self.get_prompt("system", "role")
        if not system_prompt:
            raise ValueError(
                "DecomposeAgent missing system prompt, please configure system.role in prompts/{lang}/decompose_agent.yaml"
            )
        system_prompt += self._format_conversation_context()

        user_prompt_template = self.get_prompt("process", "decompose")
        if not user_prompt_template:
            raise ValueError(
                "DecomposeAgent missing decompose prompt, please configure process.decompose in prompts/{lang}/decompose_agent.yaml"
            )

        # Auto mode: Dynamically generate subtopics not exceeding the limit
        decompose_requirement = f"""
Quantity Requirements:
Dynamically generate no more than {max_subtopics} subtopics. Please carefully analyze the background knowledge, identify core content areas related to the topic, and independently generate subtopics around the topic-related book content.
- The number of subtopics should be reasonable, not exceeding {max_subtopics}
- Prioritize subtopics most relevant and important to the topic
- Ensure subtopics do not duplicate and cover different dimensions of the topic
"""

        user_prompt = user_prompt_template.format(
            topic=topic,
            rag_context=rag_context,
            decompose_requirement=decompose_requirement,
            mode_instruction=self._get_mode_contract("decompose"),
        )

        _chunks: list[str] = []
        async for _c in self.stream_llm(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            stage="decompose",
            trace_meta=self._build_trace_meta("auto"),
        ):
            _chunks.append(_c)
        response = "".join(_chunks)

        # Parse JSON output (strict validation)
        from ..utils.json_utils import ensure_json_dict, ensure_keys, extract_json_from_text

        data = extract_json_from_text(response)
        try:
            obj = ensure_json_dict(data)
            ensure_keys(obj, ["sub_topics"])
            subs = obj.get("sub_topics", [])
            if not isinstance(subs, list):
                raise ValueError("sub_topics must be an array")
            # Limit count not exceeding max_subtopics
            cleaned = []
            for it in subs[:max_subtopics]:
                if isinstance(it, dict):
                    cleaned.append(
                        {"title": it.get("title", ""), "overview": it.get("overview", "")}
                    )
            return cleaned
        except Exception:
            # Fallback: return empty list
            return []

    async def _generate_sub_topics(
        self, topic: str, rag_context: str, num_subtopics: int
    ) -> list[dict[str, str]]:
        """
        Generate subtopics based on RAG background

        Args:
            topic: Main topic
            rag_context: RAG background knowledge
            num_subtopics: Expected number of subtopics

        Returns:
            Subtopics list
        """
        system_prompt = self.get_prompt("system", "role")
        if not system_prompt:
            raise ValueError(
                "DecomposeAgent missing system prompt, please configure system.role in prompts/{lang}/decompose_agent.yaml"
            )
        system_prompt += self._format_conversation_context()

        user_prompt_template = self.get_prompt("process", "decompose")
        if not user_prompt_template:
            raise ValueError(
                "DecomposeAgent missing decompose prompt, please configure process.decompose in prompts/{lang}/decompose_agent.yaml"
            )

        # Manual mode: Explicitly generate specified number of subtopics
        decompose_requirement = f"""
Quantity Requirements:
Explicitly generate {num_subtopics} subtopics. Please ensure exactly {num_subtopics} subtopics are generated, no more, no less.
"""

        user_prompt = user_prompt_template.format(
            topic=topic,
            rag_context=rag_context,
            decompose_requirement=decompose_requirement,
            mode_instruction=self._get_mode_contract("decompose"),
        )

        _chunks: list[str] = []
        async for _c in self.stream_llm(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            stage="decompose",
            trace_meta=self._build_trace_meta("manual"),
        ):
            _chunks.append(_c)
        response = "".join(_chunks)

        # Parse JSON output (strict validation)
        from ..utils.json_utils import ensure_json_dict, ensure_keys, extract_json_from_text

        data = extract_json_from_text(response)
        try:
            obj = ensure_json_dict(data)
            ensure_keys(obj, ["sub_topics"])
            subs = obj.get("sub_topics", [])
            if not isinstance(subs, list):
                raise ValueError("sub_topics must be an array")
            # Only select required fields
            cleaned = []
            for it in subs[:num_subtopics]:
                if isinstance(it, dict):
                    cleaned.append(
                        {"title": it.get("title", ""), "overview": it.get("overview", "")}
                    )
            return cleaned
        except Exception:
            # Fallback: return empty list
            return []


__all__ = ["DecomposeAgent"]
