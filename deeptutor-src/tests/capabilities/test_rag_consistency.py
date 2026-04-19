"""
Tests for RAG/KB consistency normalization at the capability layer.

These tests pin the contract that:

* ``deep_solve`` strips ``rag`` from the effective tool set when no
  knowledge base is attached, and emits a warning so the UI can surface
  the mismatch.
* ``deep_research`` strips ``kb`` from the effective sources list when
  no knowledge base is attached, and surfaces a clear error if all
  sources end up empty.

Both behaviours guarantee that no downstream agent or pipeline ever
attempts a RAG call against a missing/placeholder knowledge base.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream import StreamEvent, StreamEventType
from deeptutor.core.stream_bus import StreamBus


async def _drain(bus: StreamBus, task) -> list[StreamEvent]:
    await task
    await bus.close()
    return [event async for event in bus.subscribe()]


def _fake_llm_config() -> MagicMock:
    cfg = MagicMock()
    cfg.api_key = "sk-test"
    cfg.base_url = None
    cfg.api_version = None
    return cfg


# ---------------------------------------------------------------------------
# deep_solve: rag without KB → tool stripped, warning emitted
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_deep_solve_strips_rag_when_no_knowledge_base() -> None:
    from deeptutor.capabilities.deep_solve import DeepSolveCapability

    captured_kwargs: dict[str, Any] = {}

    class _FakeSolver:
        def __init__(self, **kwargs: Any) -> None:
            captured_kwargs.update(kwargs)

        async def ainit(self) -> None:
            return None

        def set_trace_callback(self, _cb: Any) -> None:
            return None

        async def solve(self, **_kwargs: Any) -> dict[str, Any]:
            return {"final_answer": "ok", "metadata": {}}

    capability = DeepSolveCapability()
    bus = StreamBus()
    context = UnifiedContext(
        user_message="solve x^2 = 4",
        active_capability="deep_solve",
        enabled_tools=["rag", "web_search"],
        knowledge_bases=[],  # explicitly empty
        language="en",
    )

    with patch(
        "deeptutor.agents.solve.main_solver.MainSolver",
        new=_FakeSolver,
    ), patch(
        "deeptutor.services.llm.config.get_llm_config",
        return_value=_fake_llm_config(),
    ):
        events = await _drain(bus, capability.run(context, bus))

    # rag must NOT be in the enabled_tools we forwarded to MainSolver
    assert "rag" not in captured_kwargs["enabled_tools"]
    assert "web_search" in captured_kwargs["enabled_tools"]
    assert captured_kwargs["kb_name"] is None
    assert captured_kwargs["disable_planner_retrieve"] is True

    # And a warning progress event should have been emitted
    warnings = [
        e for e in events
        if e.type == StreamEventType.PROGRESS
        and (e.metadata or {}).get("reason") == "rag_without_kb"
    ]
    assert warnings, "expected a rag_without_kb warning event"


@pytest.mark.asyncio
async def test_deep_solve_keeps_rag_when_knowledge_base_attached() -> None:
    from deeptutor.capabilities.deep_solve import DeepSolveCapability

    captured_kwargs: dict[str, Any] = {}

    class _FakeSolver:
        def __init__(self, **kwargs: Any) -> None:
            captured_kwargs.update(kwargs)

        async def ainit(self) -> None:
            return None

        def set_trace_callback(self, _cb: Any) -> None:
            return None

        async def solve(self, **_kwargs: Any) -> dict[str, Any]:
            return {"final_answer": "ok", "metadata": {}}

    capability = DeepSolveCapability()
    bus = StreamBus()
    context = UnifiedContext(
        user_message="solve x^2 = 4",
        active_capability="deep_solve",
        enabled_tools=["rag", "web_search"],
        knowledge_bases=["my-kb"],
        language="en",
    )

    with patch(
        "deeptutor.agents.solve.main_solver.MainSolver",
        new=_FakeSolver,
    ), patch(
        "deeptutor.services.llm.config.get_llm_config",
        return_value=_fake_llm_config(),
    ):
        await _drain(bus, capability.run(context, bus))

    assert "rag" in captured_kwargs["enabled_tools"]
    assert captured_kwargs["kb_name"] == "my-kb"
    assert captured_kwargs["disable_planner_retrieve"] is False


# ---------------------------------------------------------------------------
# deep_research: kb in sources without KB → kb dropped or hard error
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_deep_research_drops_kb_source_when_no_knowledge_base() -> None:
    from deeptutor.capabilities.deep_research import DeepResearchCapability

    captured_config: dict[str, Any] = {}

    async def _fake_outline(self, **kwargs: Any):  # noqa: ARG001
        captured_config.update(kwargs.get("config") or {})
        return [{"title": "Subtopic 1", "overview": "Overview 1"}]

    capability = DeepResearchCapability()
    bus = StreamBus()
    context = UnifiedContext(
        user_message="A topic to research",
        active_capability="deep_research",
        enabled_tools=["rag", "web_search"],
        knowledge_bases=[],
        config_overrides={
            "mode": "report",
            "depth": "standard",
            "sources": ["kb", "web"],  # kb requested but no KB attached
        },
        language="en",
    )

    with patch.object(
        DeepResearchCapability,
        "_generate_outline_preview",
        new=_fake_outline,
    ), patch(
        "deeptutor.services.llm.config.get_llm_config",
        return_value=_fake_llm_config(),
    ), patch(
        "deeptutor.services.config.load_config_with_main",
        return_value={},
    ):
        events = await _drain(bus, capability.run(context, bus))

    # The runtime config must NOT enable RAG, but must still allow web.
    researching = captured_config.get("researching", {})
    assert researching.get("enable_rag") is False
    assert researching.get("enable_web_search") is True
    # rag intent stripped from request_config sources
    assert captured_config["intent"]["sources"] == ["web"]

    # A warning progress event must be present
    warnings = [
        e for e in events
        if e.type == StreamEventType.PROGRESS
        and (e.metadata or {}).get("reason") == "kb_without_kb_name"
    ]
    assert warnings, "expected a kb_without_kb_name warning event"


@pytest.mark.asyncio
async def test_deep_research_errors_when_only_kb_source_and_no_knowledge_base() -> None:
    from deeptutor.capabilities.deep_research import DeepResearchCapability

    capability = DeepResearchCapability()
    bus = StreamBus()
    context = UnifiedContext(
        user_message="topic",
        active_capability="deep_research",
        enabled_tools=["rag"],
        knowledge_bases=[],
        config_overrides={
            "mode": "report",
            "depth": "standard",
            "sources": ["kb"],  # ONLY kb, and no KB attached
        },
        language="en",
    )

    with patch(
        "deeptutor.services.llm.config.get_llm_config",
        return_value=_fake_llm_config(),
    ), patch(
        "deeptutor.services.config.load_config_with_main",
        return_value={},
    ):
        events = await _drain(bus, capability.run(context, bus))

    errors = [e for e in events if e.type == StreamEventType.ERROR]
    assert errors, "expected an error event when no usable source remains"
    assert "source" in errors[0].content.lower()
