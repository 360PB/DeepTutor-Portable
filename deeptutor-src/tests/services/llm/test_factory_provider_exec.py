"""Tests for provider-backed execution in llm.factory."""

from __future__ import annotations

import pytest

from deeptutor.services.llm.config import LLMConfig
from deeptutor.services.llm.factory import complete, stream  # noqa: F401


# ---------------------------------------------------------------------------
# extra_headers dedup / merge (regression for #324)
# ---------------------------------------------------------------------------


def _make_cfg(**overrides):
    defaults = dict(
        model="gpt-4o-mini",
        api_key="test-key",
        base_url="https://api.example.com/v1",
        binding="openai",
        provider_name="openai",
        provider_mode="standard",
    )
    defaults.update(overrides)
    return LLMConfig(**defaults)


@pytest.mark.asyncio
async def test_complete_extra_headers_from_kwargs_no_duplicate(monkeypatch) -> None:
    """Passing extra_headers via kwargs must not cause 'multiple values' TypeError."""
    cfg = _make_cfg(extra_headers={})
    captured: dict[str, object] = {}

    async def _fake_sdk_complete(**kwargs):
        captured.update(kwargs)
        return "ok"

    monkeypatch.setattr("deeptutor.services.llm.factory.get_llm_config", lambda: cfg)
    monkeypatch.setattr("deeptutor.services.llm.executors.sdk_complete", _fake_sdk_complete)
    monkeypatch.setattr("deeptutor.services.llm.factory.sdk_complete", _fake_sdk_complete)

    result = await complete("hello", extra_headers={"X-Custom": "val"})
    assert result == "ok"
    assert captured["extra_headers"] == {"X-Custom": "val"}


@pytest.mark.asyncio
async def test_complete_merges_config_and_caller_extra_headers(monkeypatch) -> None:
    """Caller extra_headers should be merged with config-level headers."""
    cfg = _make_cfg(extra_headers={"X-Config": "from-config"})
    captured: dict[str, object] = {}

    async def _fake_sdk_complete(**kwargs):
        captured.update(kwargs)
        return "ok"

    monkeypatch.setattr("deeptutor.services.llm.factory.get_llm_config", lambda: cfg)
    monkeypatch.setattr("deeptutor.services.llm.executors.sdk_complete", _fake_sdk_complete)
    monkeypatch.setattr("deeptutor.services.llm.factory.sdk_complete", _fake_sdk_complete)

    result = await complete("hello", extra_headers={"X-Caller": "from-caller"})
    assert result == "ok"
    headers = captured["extra_headers"]
    assert headers["X-Config"] == "from-config"
    assert headers["X-Caller"] == "from-caller"


@pytest.mark.asyncio
async def test_stream_extra_headers_from_kwargs_no_duplicate(monkeypatch) -> None:
    """Passing extra_headers via kwargs to stream must not cause 'multiple values' TypeError."""
    cfg = _make_cfg(extra_headers={})
    captured: dict[str, object] = {}

    async def _fake_sdk_stream(**kwargs):
        captured.update(kwargs)
        yield "chunk"

    monkeypatch.setattr("deeptutor.services.llm.factory.get_llm_config", lambda: cfg)
    monkeypatch.setattr("deeptutor.services.llm.executors.sdk_stream", _fake_sdk_stream)
    monkeypatch.setattr("deeptutor.services.llm.factory.sdk_stream", _fake_sdk_stream)

    chunks = []
    async for c in stream("hello", extra_headers={"X-Custom": "val"}):
        chunks.append(c)
    assert chunks == ["chunk"]
    assert captured["extra_headers"] == {"X-Custom": "val"}


@pytest.mark.asyncio
async def test_stream_merges_config_and_caller_extra_headers(monkeypatch) -> None:
    """Caller extra_headers should be merged with config-level headers in stream."""
    cfg = _make_cfg(extra_headers={"X-Config": "cfg"})
    captured: dict[str, object] = {}

    async def _fake_sdk_stream(**kwargs):
        captured.update(kwargs)
        yield "chunk"

    monkeypatch.setattr("deeptutor.services.llm.factory.get_llm_config", lambda: cfg)
    monkeypatch.setattr("deeptutor.services.llm.executors.sdk_stream", _fake_sdk_stream)
    monkeypatch.setattr("deeptutor.services.llm.factory.sdk_stream", _fake_sdk_stream)

    chunks = []
    async for c in stream("hello", extra_headers={"X-Caller": "clr"}):
        chunks.append(c)
    assert chunks == ["chunk"]
    headers = captured["extra_headers"]
    assert headers["X-Config"] == "cfg"
    assert headers["X-Caller"] == "clr"


# NOTE: The legacy litellm-routing tests (test_factory_complete_uses_litellm,
# test_factory_complete_uses_direct_azure,
# test_factory_complete_openai_codex_requires_oauth,
# test_factory_stream_uses_litellm) were removed. The factory no longer
# delegates to litellm — see deeptutor/services/llm/executors.py — so the
# `litellm_available`/`litellm_complete`/`litellm_stream` symbols and their
# routing branches no longer exist. The factory now always goes through
# `sdk_complete` / `sdk_stream`, which is exercised by the four
# extra_headers tests above and by tests/services/llm/test_factory_*.py
# elsewhere.
