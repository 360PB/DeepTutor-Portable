#!/usr/bin/env python
"""
RephraseAgent - Topic rephrasing Agent
Responsible for rephrasing and optimizing user input
"""

from typing import Any

from deeptutor.agents.base_agent import BaseAgent
from deeptutor.core.trace import build_trace_metadata, new_call_id

from ..utils.json_utils import extract_json_from_text


class RephraseAgent(BaseAgent):
    """Topic rephrasing Agent"""

    _MODE_TO_STYLE = {
        "notes": "study_notes",
        "report": "report",
        "comparison": "comparison",
        "learning_path": "learning_path",
    }

    @staticmethod
    def _build_trace_meta(iteration: int) -> dict[str, Any]:
        return build_trace_metadata(
            call_id=new_call_id("research-rephrase"),
            phase="rephrasing",
            label="Rephrase topic",
            call_kind="llm_generation",
            trace_role="thought",
            trace_kind="llm_generation",
            iteration=iteration,
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
            agent_name="rephrase_agent",
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            language=language,
            config=config,
        )
        self.conversation_history: list[dict[str, Any]] = []
        self.session_history: list[dict[str, Any]] = config.get("conversation_history", [])
        intent_mode = str(config.get("intent", {}).get("mode", "") or "")
        reporting_style = str(config.get("reporting", {}).get("style", "") or "")
        self._research_style = reporting_style or self._MODE_TO_STYLE.get(intent_mode, "report")

    def reset_history(self):
        """Reset conversation history for a new research session"""
        self.conversation_history = []

    def _get_mode_contract(self, stage: str) -> str:
        return (
            self.get_prompt("mode_contracts", f"{self._research_style}_{stage}", "")
            or ""
        ).strip()

    def _format_conversation_history(self) -> str:
        """Format conversation history for prompt"""
        if not self.conversation_history:
            return ""

        history_parts = []
        for entry in self.conversation_history:
            role = entry.get("role", "unknown")
            iteration = entry.get("iteration", 0)
            content = entry.get("content", "")

            if role == "user":
                if iteration == 0:
                    history_parts.append(f"[User - Initial Input]\n{content}")
                else:
                    history_parts.append(f"[User - Feedback (Round {iteration})]\n{content}")
            elif role == "assistant":
                topic = content.get("topic", "") if isinstance(content, dict) else str(content)
                history_parts.append(f"[Assistant - Rephrased Topic (Round {iteration})]\n{topic}")

        return "\n\n".join(history_parts)

    async def process(
        self, user_input: str, iteration: int = 0, previous_result: dict[str, Any] = None
    ) -> dict[str, Any]:
        """
        Rephrase and optimize user input using the accumulated planning context.

        Args:
            user_input: Research topic or the latest rephrased topic
            iteration: Iteration count (for tracking rephrasing rounds)
            previous_result: Previous rephrasing result

        Returns:
            Dictionary containing rephrasing results
            {
                "topic": str,                  # Optimized research topic (a clear, explicit statement)
                "iteration": int,              # Iteration count
            }
        """
        print(f"\n{'=' * 70}")
        print(f"🔄 RephraseAgent - Topic Rephrasing (Iteration {iteration})")
        print(f"{'=' * 70}")

        # Reset history for new session (iteration 0)
        if iteration == 0:
            self.reset_history()
            print(f"Original Input: {user_input}\n")
        else:
            print(f"User Feedback: {user_input}\n")
            print(f"Conversation History: {len(self.conversation_history)} entries\n")

        # Add current user input to history
        self.conversation_history.append(
            {
                "role": "user",
                "content": user_input,
                "iteration": iteration,
            }
        )

        system_prompt = self.get_prompt("system", "role")
        if not system_prompt:
            raise ValueError(
                "RephraseAgent missing system prompt, please configure system.role in prompts/{lang}/rephrase_agent.yaml"
            )
        if self.session_history:
            ctx_parts = []
            for msg in self.session_history:
                role = msg.get("role", "user")
                content = str(msg.get("content", "")).strip()
                if content:
                    ctx_parts.append(f"[{role}]: {content}")
            if ctx_parts:
                system_prompt += (
                    "\n\n<session_history>\n"
                    "The following is the earlier conversation in this session. "
                    "Use it to understand what the user previously discussed or planned.\n\n"
                    + "\n\n".join(ctx_parts)
                    + "\n</session_history>"
                )

        # Get user prompt template
        user_prompt_template = self.get_prompt("process", "rephrase")
        if not user_prompt_template:
            raise ValueError(
                "RephraseAgent missing rephrase prompt, please configure process.rephrase in prompts/{lang}/rephrase_agent.yaml"
            )

        # Format conversation history for prompt
        history_text = self._format_conversation_history()

        # Format user prompt with full history
        user_prompt = user_prompt_template.format(
            user_input=user_input,
            iteration=iteration,
            conversation_history=history_text,
            previous_result=history_text,
            mode_instruction=self._get_mode_contract("rephrase"),
        )

        _chunks: list[str] = []
        async for _c in self.stream_llm(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            stage="rephrase",
            trace_meta=self._build_trace_meta(iteration),
        ):
            _chunks.append(_c)
        response = "".join(_chunks)

        # Parse JSON output
        data = extract_json_from_text(response)
        from ..utils.json_utils import ensure_json_dict, ensure_keys

        try:
            result = ensure_json_dict(data)
            ensure_keys(result, ["topic"])
        except Exception:
            # Fallback: use user input or last assistant topic
            fallback_topic = user_input
            for entry in reversed(self.conversation_history):
                if entry.get("role") == "assistant":
                    content = entry.get("content", {})
                    if isinstance(content, dict) and content.get("topic"):
                        fallback_topic = content["topic"]
                        break
            result = {"topic": fallback_topic}

        result["iteration"] = iteration

        # Add assistant response to history
        self.conversation_history.append(
            {
                "role": "assistant",
                "content": result,
                "iteration": iteration,
            }
        )

        print("\n✓ Rephrasing Completed:")
        print(f"  Optimized Research Topic: {result.get('topic', '')}")

        return result


__all__ = ["RephraseAgent"]
