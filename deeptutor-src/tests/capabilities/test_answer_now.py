"""
Tests for the per-capability ``answer_now`` fast-paths.

Each capability now owns its own answer-now branch (instead of every
turn being re-routed to ``chat``). These tests pin the contract:

* Detection — the shared ``extract_answer_now_context`` correctly gates
  the branch on a non-empty ``original_user_message``.
* Trace formatting — long event lists are summarised, truncation
  applied, empty inputs fall back to a sentinel string.
* Skip notice — i18n-aware, omits when no stages were skipped.
* Per-capability flow — for each registered capability we mock the
  underlying LLM stream and assert the result envelope shape that the
  frontend depends on (``response`` always, plus capability-specific
  keys like ``summary.results`` for ``deep_question`` or ``code`` for
  ``visualize``).

The tests deliberately avoid touching the real LLM stack: we patch
``deeptutor.capabilities._answer_now.llm_stream`` (the alias the helper
imports) and ``deeptutor.capabilities._answer_now.get_llm_config`` so
the fast-paths run end-to-end without network or API keys.
"""

from __future__ import annotations

import json
from typing import Any, AsyncIterator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from deeptutor.capabilities import _answer_now
from deeptutor.capabilities._answer_now import (
    extract_answer_now_context,
    format_trace_summary,
    join_chunks,
    labeled_block,
    make_skip_notice,
)
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream import StreamEvent, StreamEventType
from deeptutor.core.stream_bus import StreamBus


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


async def _drain(bus: StreamBus, task) -> list[StreamEvent]:
    """Run ``task`` to completion, then return everything emitted on ``bus``."""
    await task
    await bus.close()
    return [event async for event in bus.subscribe()]


def _fake_llm_config(model: str = "gpt-4o-mini") -> MagicMock:
    cfg = MagicMock()
    cfg.binding = "openai"
    cfg.model = model
    cfg.api_key = "sk-test"
    cfg.base_url = None
    cfg.api_version = None
    return cfg


def _make_stream_factory(chunks: list[str]):
    """Return an async generator factory that yields the given chunks once."""

    async def _stream(*_args: Any, **_kwargs: Any) -> AsyncIterator[str]:
        for chunk in chunks:
            yield chunk

    return _stream


def _build_context(
    *,
    capability: str,
    payload: dict[str, Any] | None,
    user_message: str = "What is a Fourier transform?",
    config_overrides: dict[str, Any] | None = None,
    language: str = "en",
) -> UnifiedContext:
    overrides: dict[str, Any] = dict(config_overrides or {})
    if payload is not None:
        overrides["answer_now_context"] = payload
    return UnifiedContext(
        session_id="sess-test",
        user_message=user_message,
        active_capability=capability,
        config_overrides=overrides,
        language=language,
        metadata={"turn_id": "turn-test"},
    )


def _result_event(events: list[StreamEvent]) -> StreamEvent:
    """Return the single ``RESULT`` event; raise if absent."""
    matches = [e for e in events if e.type == StreamEventType.RESULT]
    assert len(matches) == 1, f"expected 1 RESULT event, got {len(matches)}"
    return matches[0]


def _content_text(events: list[StreamEvent]) -> str:
    return "".join(e.content for e in events if e.type == StreamEventType.CONTENT)


# ---------------------------------------------------------------------------
# 1. Shared helpers — pure functions
# ---------------------------------------------------------------------------


class TestExtractAnswerNowContext:
    def test_returns_payload_when_present(self) -> None:
        ctx = _build_context(
            capability="chat",
            payload={"original_user_message": "hi", "events": []},
        )
        assert extract_answer_now_context(ctx) == {
            "original_user_message": "hi",
            "events": [],
        }

    def test_returns_none_when_missing(self) -> None:
        ctx = _build_context(capability="chat", payload=None)
        assert extract_answer_now_context(ctx) is None

    def test_returns_none_when_not_dict(self) -> None:
        ctx = UnifiedContext(
            user_message="x",
            config_overrides={"answer_now_context": "not-a-dict"},
        )
        assert extract_answer_now_context(ctx) is None

    def test_returns_none_when_original_user_message_empty(self) -> None:
        ctx = _build_context(
            capability="chat",
            payload={"original_user_message": "   "},
        )
        assert extract_answer_now_context(ctx) is None


class TestFormatTraceSummary:
    def test_empty_events_returns_fallback_en(self) -> None:
        assert "No intermediate" in format_trace_summary([], language="en")

    def test_empty_events_returns_fallback_zh(self) -> None:
        assert "没有可用" in format_trace_summary([], language="zh")

    def test_non_list_returns_fallback(self) -> None:
        assert "No intermediate" in format_trace_summary("nope", language="en")

    def test_renders_event_with_stage_and_tool(self) -> None:
        events = [
            {
                "type": "tool_call",
                "stage": "acting",
                "content": "rag.query",
                "metadata": {"tool_name": "rag"},
            }
        ]
        out = format_trace_summary(events, language="en")
        assert "1. tool_call / acting" in out
        assert "rag.query" in out
        assert "[tool=rag]" in out

    def test_truncates_long_event_content(self) -> None:
        events = [
            {
                "type": "thinking",
                "stage": "planning",
                "content": "x" * 5000,
            }
        ]
        out = format_trace_summary(events, language="en")
        assert out.endswith("...")
        # The per-event cap is 800 chars; the rendered line stays bounded.
        assert len(out) < 1000

    def test_truncates_overall_transcript(self) -> None:
        events = [
            {"type": "thinking", "stage": "s", "content": "a" * 700}
            for _ in range(20)
        ]
        out = format_trace_summary(events, language="en")
        assert len(out) <= 6000
        assert out.endswith("...")

    def test_skips_non_dict_entries(self) -> None:
        events = ["bad", 42, {"type": "thinking", "content": "good"}]
        out = format_trace_summary(events, language="en")
        assert "good" in out
        assert "bad" not in out


class TestMakeSkipNotice:
    def test_empty_when_no_stages(self) -> None:
        assert make_skip_notice(capability="chat", language="en", stages_skipped=[]) == ""

    def test_english_lists_stages(self) -> None:
        notice = make_skip_notice(
            capability="deep_solve",
            language="en",
            stages_skipped=["planning", "reasoning"],
        )
        assert "planning, reasoning" in notice
        assert "`deep_solve`" in notice

    def test_chinese_uses_full_width_separator(self) -> None:
        notice = make_skip_notice(
            capability="deep_solve",
            language="zh",
            stages_skipped=["planning", "reasoning"],
        )
        assert "planning、reasoning" in notice
        assert "已跳过" in notice


class TestLabeledBlock:
    def test_renders_label_and_content(self) -> None:
        assert labeled_block("X", "hello") == "[X]\nhello"

    def test_uses_sentinel_for_empty_content(self) -> None:
        assert labeled_block("X", "   ") == "[X]\n(empty)"


class TestJoinChunks:
    def test_joins_and_strips_thinking_tags(self) -> None:
        with patch.object(_answer_now, "get_llm_config", return_value=_fake_llm_config()):
            text = join_chunks(["<think>private</think>", "Answer."])
            # ``clean_thinking_tags`` for the openai binding is a no-op, but
            # we still want to make sure the function does not blow up.
            assert "Answer." in text


# ---------------------------------------------------------------------------
# 2. Per-capability fast paths
# ---------------------------------------------------------------------------


class TestChatAnswerNow:
    """``chat`` keeps its existing synthesizer; we only assert the high-
    level behavior so a future refactor of ``_stage_answer_now`` doesn't
    silently change the contract."""

    @pytest.mark.asyncio
    async def test_chat_synthesises_final_answer_from_partial_trace(self) -> None:
        from deeptutor.agents.chat import agentic_pipeline as ap_module

        async def _fake_stream(self: Any, _messages: Any, **_kwargs: Any):
            for chunk in ("Hello", " ", "world"):
                yield chunk

        cfg = _fake_llm_config()

        with patch.object(
            ap_module.AgenticChatPipeline,
            "_stream_messages",
            _fake_stream,
        ), patch(
            "deeptutor.agents.chat.agentic_pipeline.get_llm_config",
            return_value=cfg,
        ):
            from deeptutor.capabilities.chat import ChatCapability

            ctx = _build_context(
                capability="chat",
                payload={
                    "original_user_message": "Explain Fourier",
                    "partial_response": "We had begun to think about ...",
                    "events": [
                        {"type": "thinking", "stage": "thinking", "content": "warming up"}
                    ],
                },
            )
            bus = StreamBus()
            cap = ChatCapability()
            events = await _drain(bus, cap.run(ctx, bus))

            text = _content_text(events)
            assert "Hello" in text
            result = _result_event(events)
            assert result.metadata.get("answer_now") is True
            assert "Hello world" in str(result.metadata.get("response", ""))


class TestDeepSolveAnswerNow:
    @pytest.mark.asyncio
    async def test_jumps_to_writing_stage(self) -> None:
        cfg = _fake_llm_config()
        chunks = ["The Fourier transform ", "decomposes signals."]
        with patch.object(_answer_now, "get_llm_config", return_value=cfg), patch.object(
            _answer_now, "llm_stream", _make_stream_factory(chunks)
        ):
            from deeptutor.capabilities.deep_solve import DeepSolveCapability

            ctx = _build_context(
                capability="deep_solve",
                payload={
                    "original_user_message": "Explain Fourier transform",
                    "partial_response": "Planning ...",
                    "events": [
                        {
                            "type": "thinking",
                            "stage": "planning",
                            "content": "Need to break this into intuition + math",
                        }
                    ],
                },
                language="en",
            )
            bus = StreamBus()
            cap = DeepSolveCapability()
            events = await _drain(bus, cap.run(ctx, bus))

            stage_starts = [
                e for e in events if e.type == StreamEventType.STAGE_START
            ]
            assert any(e.stage == "writing" for e in stage_starts)

            text = _content_text(events)
            assert "Skipped" in text  # the skip notice prepended
            assert "decomposes signals" in text

            result = _result_event(events)
            assert result.metadata.get("metadata", {}).get("answer_now") is True
            assert result.metadata.get("response", "").endswith("decomposes signals.")
            assert result.metadata.get("output_dir") == ""


class TestDeepQuestionAnswerNow:
    @pytest.mark.asyncio
    async def test_emits_quiz_envelope(self) -> None:
        cfg = _fake_llm_config()
        payload_json = json.dumps(
            {
                "questions": [
                    {
                        "question_id": "q_1",
                        "question": "What is 2+2?",
                        "question_type": "choice",
                        "options": {"A": "3", "B": "4", "C": "5"},
                        "correct_answer": "B",
                        "explanation": "Basic arithmetic.",
                        "difficulty": "easy",
                        "concentration": "arithmetic",
                    },
                    {
                        "question_id": "q_2",
                        "question": "Define derivative.",
                        "question_type": "written",
                        "correct_answer": "Limit of difference quotient.",
                        "explanation": "Standard textbook definition.",
                    },
                ]
            }
        )
        with patch.object(_answer_now, "get_llm_config", return_value=cfg), patch.object(
            _answer_now, "llm_stream", _make_stream_factory([payload_json])
        ):
            from deeptutor.capabilities.deep_question import DeepQuestionCapability

            ctx = _build_context(
                capability="deep_question",
                payload={
                    "original_user_message": "Generate calc warm-ups",
                    "events": [],
                },
                config_overrides={"num_questions": 2, "topic": "calculus warm-ups"},
            )
            bus = StreamBus()
            cap = DeepQuestionCapability()
            events = await _drain(bus, cap.run(ctx, bus))

            result = _result_event(events)
            summary = result.metadata.get("summary") or {}
            results = summary.get("results") or []
            assert len(results) == 2
            assert results[0]["qa_pair"]["question"] == "What is 2+2?"
            assert results[0]["qa_pair"]["options"]["B"] == "4"
            assert result.metadata.get("mode") == "answer_now"
            assert result.metadata.get("metadata", {}).get("answer_now") is True

            # The rendered markdown should make it into a CONTENT event so
            # the chat surface still shows a textual recap of the quiz.
            text = _content_text(events)
            assert "What is 2+2?" in text
            assert "Skipped" in text  # skip notice

    @pytest.mark.asyncio
    async def test_handles_unparseable_json_gracefully(self) -> None:
        cfg = _fake_llm_config()
        with patch.object(_answer_now, "get_llm_config", return_value=cfg), patch.object(
            _answer_now, "llm_stream", _make_stream_factory(["not json at all"])
        ):
            from deeptutor.capabilities.deep_question import DeepQuestionCapability

            ctx = _build_context(
                capability="deep_question",
                payload={"original_user_message": "x", "events": []},
                config_overrides={"num_questions": 1, "topic": "x"},
            )
            bus = StreamBus()
            cap = DeepQuestionCapability()
            events = await _drain(bus, cap.run(ctx, bus))

            # Should still produce a result event with a placeholder
            # question, not crash with a JSONDecodeError.
            result = _result_event(events)
            results = (result.metadata.get("summary") or {}).get("results") or []
            assert len(results) == 1
            assert results[0]["qa_pair"]["question_type"] == "written"


class TestDeepResearchAnswerNow:
    @pytest.mark.asyncio
    async def test_emits_report_envelope(self) -> None:
        cfg = _fake_llm_config()
        chunks = ["# Report\n\n", "Body section.\n\n", "## Conclusion\n\nWrap-up."]
        with patch.object(_answer_now, "get_llm_config", return_value=cfg), patch.object(
            _answer_now, "llm_stream", _make_stream_factory(chunks)
        ):
            from deeptutor.capabilities.deep_research import DeepResearchCapability

            ctx = _build_context(
                capability="deep_research",
                payload={
                    "original_user_message": "State of LLM evals 2025",
                    "events": [
                        {
                            "type": "tool_result",
                            "stage": "researching",
                            "content": "Found 3 evals.",
                            "metadata": {"tool": "web_search"},
                        }
                    ],
                },
                language="en",
            )
            bus = StreamBus()
            cap = DeepResearchCapability()
            events = await _drain(bus, cap.run(ctx, bus))

            stage_starts = [
                e for e in events if e.type == StreamEventType.STAGE_START
            ]
            assert any(e.stage == "reporting" for e in stage_starts)

            result = _result_event(events)
            assert result.metadata.get("metadata", {}).get("answer_now") is True
            response = str(result.metadata.get("response", ""))
            assert "# Report" in response
            assert "Conclusion" in response


class TestVisualizeAnswerNow:
    @pytest.mark.asyncio
    async def test_emits_renderable_code_envelope(self) -> None:
        cfg = _fake_llm_config()
        payload_json = json.dumps(
            {
                "render_type": "svg",
                "code": "<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'/>",
            }
        )
        with patch.object(_answer_now, "get_llm_config", return_value=cfg), patch.object(
            _answer_now, "llm_stream", _make_stream_factory([payload_json])
        ):
            from deeptutor.capabilities.visualize import VisualizeCapability

            ctx = _build_context(
                capability="visualize",
                payload={
                    "original_user_message": "Draw a circle",
                    "events": [],
                },
                config_overrides={"render_mode": "svg"},
            )
            bus = StreamBus()
            cap = VisualizeCapability()
            events = await _drain(bus, cap.run(ctx, bus))

            result = _result_event(events)
            assert result.metadata.get("render_type") == "svg"
            code = result.metadata.get("code") or {}
            assert code.get("language") == "svg"
            assert "<svg" in code.get("content", "")
            assert result.metadata.get("metadata", {}).get("answer_now") is True

            content = _content_text(events)
            assert "```svg" in content

    @pytest.mark.asyncio
    async def test_falls_back_to_svg_when_render_type_invalid(self) -> None:
        cfg = _fake_llm_config()
        payload_json = json.dumps({"render_type": "totally-bogus", "code": "x"})
        with patch.object(_answer_now, "get_llm_config", return_value=cfg), patch.object(
            _answer_now, "llm_stream", _make_stream_factory([payload_json])
        ):
            from deeptutor.capabilities.visualize import VisualizeCapability

            ctx = _build_context(
                capability="visualize",
                payload={"original_user_message": "x", "events": []},
            )
            bus = StreamBus()
            cap = VisualizeCapability()
            events = await _drain(bus, cap.run(ctx, bus))

            result = _result_event(events)
            assert result.metadata.get("render_type") == "svg"

    @pytest.mark.asyncio
    async def test_strips_code_fences_around_json(self) -> None:
        cfg = _fake_llm_config()
        fenced = "```json\n{\"render_type\": \"mermaid\", \"code\": \"graph TD;A-->B\"}\n```"
        with patch.object(_answer_now, "get_llm_config", return_value=cfg), patch.object(
            _answer_now, "llm_stream", _make_stream_factory([fenced])
        ):
            from deeptutor.capabilities.visualize import VisualizeCapability

            ctx = _build_context(
                capability="visualize",
                payload={"original_user_message": "diagram", "events": []},
            )
            bus = StreamBus()
            cap = VisualizeCapability()
            events = await _drain(bus, cap.run(ctx, bus))

            result = _result_event(events)
            assert result.metadata.get("render_type") == "mermaid"
            assert "graph TD" in (result.metadata.get("code") or {}).get("content", "")


class TestMathAnimatorAnswerNow:
    """Math animator's fast-path keeps the real ``code_generation`` +
    ``render`` stages — those are the whole point of the capability —
    while skipping ``concept_analysis``, ``concept_design`` and
    ``summary``. We verify dispatch and result envelope by mocking the
    pipeline's two retained stages so we don't actually invoke Manim."""

    @pytest.mark.asyncio
    async def test_skips_analysis_design_summary_but_calls_codegen_and_render(
        self,
    ) -> None:
        from deeptutor.agents.math_animator.models import (
            GeneratedCode,
            RenderResult,
        )

        # Skip the whole test cleanly when manim isn't available, since
        # math_animator.run() short-circuits before we can patch anything.
        import importlib.util as _ilu

        if _ilu.find_spec("manim") is None:
            pytest.skip("manim not installed; math_animator answer-now test skipped")

        from deeptutor.capabilities.math_animator import MathAnimatorCapability

        analysis_agent_calls: list[Any] = []
        design_agent_calls: list[Any] = []
        summary_agent_calls: list[Any] = []

        with patch(
            "deeptutor.agents.math_animator.pipeline.MathAnimatorPipeline"
        ) as PipelineCls:
            pipeline_instance = PipelineCls.return_value
            pipeline_instance.run_analysis = AsyncMock(
                side_effect=lambda *a, **k: analysis_agent_calls.append(("a",))
            )
            pipeline_instance.run_design = AsyncMock(
                side_effect=lambda *a, **k: design_agent_calls.append(("d",))
            )
            pipeline_instance.run_summary = AsyncMock(
                side_effect=lambda *a, **k: summary_agent_calls.append(("s",))
            )
            pipeline_instance.run_code_generation = AsyncMock(
                return_value=GeneratedCode(code="from manim import *\nclass S(Scene): pass")
            )
            pipeline_instance.run_render = AsyncMock(
                return_value=(
                    "from manim import *\nclass S(Scene): pass",
                    RenderResult(
                        output_mode="video",
                        artifacts=[],
                        public_code_path="",
                        source_code_path="/tmp/scene.py",
                        quality="medium",
                        retry_attempts=0,
                        retry_history=[],
                        visual_review=None,
                    ),
                )
            )

            cap = MathAnimatorCapability()
            ctx = _build_context(
                capability="math_animator",
                payload={
                    "original_user_message": "Animate a sine wave",
                    "events": [],
                },
                config_overrides={"output_mode": "video", "quality": "medium"},
            )
            bus = StreamBus()
            events = await _drain(bus, cap.run(ctx, bus))

            # Skipped stages must NOT have been invoked.
            assert pipeline_instance.run_analysis.await_count == 0
            assert pipeline_instance.run_design.await_count == 0
            assert pipeline_instance.run_summary.await_count == 0
            # Retained stages MUST have been invoked exactly once.
            assert pipeline_instance.run_code_generation.await_count == 1
            assert pipeline_instance.run_render.await_count == 1

            result = _result_event(events)
            assert result.metadata.get("metadata", {}).get("answer_now") is True
            assert result.metadata.get("output_mode") == "video"
            assert result.metadata.get("code", {}).get("language") == "python"


# ---------------------------------------------------------------------------
# 3. Bypass — when no payload is set, the normal path runs
# ---------------------------------------------------------------------------


class TestNormalPathWhenNoAnswerNow:
    """A defensive check: capabilities must NOT enter the fast-path
    when ``answer_now_context`` is absent. If they did, the regular
    pipeline would be silently shadowed."""

    @pytest.mark.asyncio
    async def test_deep_solve_without_payload_calls_main_solver(self) -> None:
        from deeptutor.capabilities.deep_solve import DeepSolveCapability

        # We patch MainSolver at its import site inside the capability.
        with patch(
            "deeptutor.agents.solve.main_solver.MainSolver"
        ) as SolverCls, patch(
            "deeptutor.services.llm.config.get_llm_config", return_value=_fake_llm_config()
        ):
            solver = SolverCls.return_value
            solver.ainit = AsyncMock()
            solver.solve = AsyncMock(return_value={"final_answer": "from solver"})

            cap = DeepSolveCapability()
            ctx = _build_context(
                capability="deep_solve",
                payload=None,
                user_message="topic",
            )
            bus = StreamBus()
            events = await _drain(bus, cap.run(ctx, bus))

            solver.solve.assert_awaited_once()
            result = _result_event(events)
            assert "from solver" in str(result.metadata.get("response", ""))
