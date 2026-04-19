from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from deeptutor.agents.chat.agentic_pipeline import AgenticChatPipeline
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream import StreamEvent, StreamEventType
from deeptutor.core.trace import build_trace_metadata
from deeptutor.core.stream_bus import StreamBus
from deeptutor.core.tool_protocol import ToolResult


async def _collect_bus_events(bus: StreamBus) -> tuple[list[StreamEvent], asyncio.Task[Any]]:
    events: list[StreamEvent] = []

    async def _consume() -> None:
        async for event in bus.subscribe():
            events.append(event)

    consumer = asyncio.create_task(_consume())
    await asyncio.sleep(0)
    return events, consumer  # type: ignore[return-value]


@pytest.mark.asyncio
async def test_native_tool_loop_executes_parallel_tool_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "deeptutor.agents.chat.agentic_pipeline.get_llm_config",
        lambda: SimpleNamespace(binding="openai", model="gpt-test", api_key="k", base_url="u", api_version=None),
    )

    class FakeRegistry:
        def __init__(self) -> None:
            self.inflight = 0
            self.max_inflight = 0

        def build_openai_schemas(self, _enabled_tools):
            return [{"type": "function", "function": {"name": "web_search"}}]

        def build_prompt_text(self, enabled_tools, **_kwargs):
            return "\n".join(enabled_tools)

        def get_enabled(self, selected):
            return [SimpleNamespace(name=name) for name in selected]

        async def execute(self, name: str, **kwargs):
            self.inflight += 1
            self.max_inflight = max(self.max_inflight, self.inflight)
            await asyncio.sleep(0.05)
            self.inflight -= 1
            return ToolResult(
                content=f"{name} => {kwargs.get('query', '') or kwargs.get('context', '')}".strip(),
                sources=[{"tool": name}],
                metadata={"tool": name},
                success=True,
            )

    registry = FakeRegistry()
    monkeypatch.setattr("deeptutor.agents.chat.agentic_pipeline.get_tool_registry", lambda: registry)

    pipeline = AgenticChatPipeline(language="en")
    pipeline.registry = registry

    class FakeCreate:
        def __init__(self) -> None:
            self.calls = 0

        async def __call__(self, **_kwargs):
            self.calls += 1
            if self.calls == 1:
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(
                                content="",
                                tool_calls=[
                                    SimpleNamespace(
                                        id="tool-call-1",
                                        function=SimpleNamespace(
                                            name="web_search",
                                            arguments='{"query":"first"}',
                                        ),
                                    ),
                                    SimpleNamespace(
                                        id="tool-call-2",
                                        function=SimpleNamespace(
                                            name="reason",
                                            arguments='{"context":"second"}',
                                        ),
                                    ),
                                ],
                            )
                        )
                    ]
                )
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content="No more tools needed.",
                            tool_calls=[],
                        )
                    )
                ]
            )

    fake_create = FakeCreate()
    monkeypatch.setattr(
        pipeline,
        "_build_openai_client",
        lambda: SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(create=fake_create),
            )
        ),
    )

    bus = StreamBus()
    events, consumer = await _collect_bus_events(bus)
    context = UnifiedContext(
        session_id="session-1",
        user_message="compare two sources",
        enabled_tools=["web_search", "reason"],
        language="en",
        metadata={"turn_id": "turn-1"},
    )

    traces = await pipeline._run_native_tool_loop(
        context=context,
        enabled_tools=["web_search", "reason"],
        thinking_text="Need outside evidence and a reasoning cross-check.",
        stream=bus,
    )
    await asyncio.sleep(0)
    await bus.close()
    await consumer

    assert fake_create.calls == 1
    assert registry.max_inflight >= 2
    assert [trace.name for trace in traces] == ["web_search", "reason"]

    tool_result_events = [event for event in events if event.type.value == "tool_result"]
    assert len(tool_result_events) == 2
    assert tool_result_events[0].metadata["tool_call_id"] == "tool-call-1"
    assert tool_result_events[1].metadata["tool_call_id"] == "tool-call-2"
    assert tool_result_events[0].metadata["tool_index"] == 0
    assert tool_result_events[1].metadata["tool_index"] == 1
    acting_thinking_events = [
        event for event in events
        if event.type == StreamEventType.THINKING and event.stage == "acting"
    ]
    assert acting_thinking_events == []


@pytest.mark.asyncio
async def test_execute_tool_call_streams_retrieve_progress_for_rag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "deeptutor.agents.chat.agentic_pipeline.get_llm_config",
        lambda: SimpleNamespace(binding="openai", model="gpt-test", api_key="k", base_url="u", api_version=None),
    )

    class FakeRegistry:
        def get_enabled(self, selected):
            return [SimpleNamespace(name=name) for name in selected]

        async def execute(self, name: str, **kwargs):
            event_sink = kwargs.get("event_sink")
            if event_sink is not None:
                await event_sink("status", "Selecting provider: llamaindex", {"provider": "llamaindex"})
                await event_sink("status", "Retrieving chunks...", {"mode": "hybrid"})
            return ToolResult(
                content=f"{name} => grounded answer",
                sources=[{"tool": name}],
                metadata={"tool": name},
                success=True,
            )

    registry = FakeRegistry()
    monkeypatch.setattr("deeptutor.agents.chat.agentic_pipeline.get_tool_registry", lambda: registry)

    pipeline = AgenticChatPipeline(language="en")
    pipeline.registry = registry

    bus = StreamBus()
    events, consumer = await _collect_bus_events(bus)
    context = UnifiedContext(
        session_id="session-1",
        user_message="what is a transformer",
        enabled_tools=["rag"],
        knowledge_bases=["demo-kb"],
        language="en",
        metadata={"turn_id": "turn-1"},
    )
    trace_meta = build_trace_metadata(
        call_id="chat-react-1",
        phase="acting",
        label="Round 1",
        call_kind="react_round",
        trace_id="chat-react-1",
        trace_role="thought",
        trace_group="react_round",
        round=1,
    )
    retrieve_meta = pipeline._retrieve_trace_metadata(
        trace_meta,
        context=context,
        tool_call_id="tool-call-rag",
        tool_name="rag",
        tool_index=0,
        tool_args={"query": "transformer model", "kb_name": "demo-kb"},
    )

    result = await pipeline._execute_tool_call(
        "rag",
        {"query": "transformer model", "kb_name": "demo-kb"},
        stream=bus,
        retrieve_meta=retrieve_meta,
    )
    await asyncio.sleep(0)
    await bus.close()
    await consumer

    assert result["success"] is True
    retrieve_events = [
        event
        for event in events
        if event.type == StreamEventType.PROGRESS and event.metadata.get("trace_role") == "retrieve"
    ]
    assert [event.content for event in retrieve_events] == [
        "Query: transformer model",
        "Selecting provider: llamaindex",
        "Retrieving chunks...",
        "Retrieve complete (22 chars)",
    ]


@pytest.mark.asyncio
async def test_native_tool_loop_caps_parallel_tool_calls_at_eight(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "deeptutor.agents.chat.agentic_pipeline.get_llm_config",
        lambda: SimpleNamespace(binding="openai", model="gpt-test", api_key="k", base_url="u", api_version=None),
    )

    class FakeRegistry:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def build_openai_schemas(self, _enabled_tools):
            return [{"type": "function", "function": {"name": "web_search"}}]

        def build_prompt_text(self, enabled_tools, **_kwargs):
            return "\n".join(enabled_tools)

        def get_enabled(self, selected):
            return [SimpleNamespace(name=name) for name in selected]

        async def execute(self, name: str, **kwargs):
            self.calls.append(f"{name}:{kwargs.get('query', '')}")
            return ToolResult(
                content=f"{name} => {kwargs.get('query', '')}",
                sources=[{"tool": name}],
                metadata={"tool": name},
                success=True,
            )

    registry = FakeRegistry()
    monkeypatch.setattr("deeptutor.agents.chat.agentic_pipeline.get_tool_registry", lambda: registry)

    pipeline = AgenticChatPipeline(language="en")
    pipeline.registry = registry

    tool_calls = [
        SimpleNamespace(
            id=f"tool-call-{index}",
            function=SimpleNamespace(
                name="web_search",
                arguments=f'{{"query":"q{index}"}}',
            ),
        )
        for index in range(10)
    ]

    async def fake_create(**_kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="Use multiple tools in parallel.",
                        tool_calls=tool_calls,
                    )
                )
            ]
        )

    monkeypatch.setattr(
        pipeline,
        "_build_openai_client",
        lambda: SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(create=fake_create),
            )
        ),
    )

    bus = StreamBus()
    events, consumer = await _collect_bus_events(bus)
    context = UnifiedContext(
        session_id="session-1",
        user_message="collect broad evidence",
        enabled_tools=["web_search"],
        language="en",
        metadata={"turn_id": "turn-1"},
    )

    traces = await pipeline._run_native_tool_loop(
        context=context,
        enabled_tools=["web_search"],
        thinking_text="Need multiple web sources.",
        stream=bus,
    )
    await asyncio.sleep(0)
    await bus.close()
    await consumer

    assert len(traces) == 8
    assert len(registry.calls) == 8
    assert registry.calls[-1] == "web_search:q7"
    progress_events = [event.content for event in events if event.type == StreamEventType.PROGRESS]
    assert any("8 can run in parallel" in content for content in progress_events)
