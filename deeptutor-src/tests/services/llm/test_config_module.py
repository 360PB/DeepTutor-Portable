"""Tests for LLM configuration helpers."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from deeptutor.services.config.env_store import EnvStore
from deeptutor.services.config.provider_runtime import ResolvedLLMConfig
from deeptutor.services.llm import config as config_module
from deeptutor.services.llm.config import LLMConfig
from deeptutor.services.llm.exceptions import LLMConfigError


def _reset_config_cache() -> None:
    config_module._LLM_CONFIG_CACHE = None


def _set_temp_env_store(monkeypatch, tmp_path: Path, content: str) -> EnvStore:
    env_path = tmp_path / ".env"
    env_path.write_text(content, encoding="utf-8")
    store = EnvStore(path=env_path)
    monkeypatch.setattr(config_module, "get_env_store", lambda: store)
    return store


def test_get_llm_config_from_resolver(monkeypatch) -> None:
    """Resolver-backed loading should populate provider metadata."""
    _reset_config_cache()

    def _fake_resolver() -> ResolvedLLMConfig:
        return ResolvedLLMConfig(
            model="openai/gpt-4o-mini",
            provider_name="openrouter",
            provider_mode="gateway",
            binding_hint="openrouter",
            binding="openrouter",
            api_key="sk-or-test",
            base_url="https://openrouter.ai/api/v1",
            effective_url="https://openrouter.ai/api/v1",
            api_version=None,
            extra_headers={"X-Test": "1"},
            reasoning_effort="medium",
        )

    monkeypatch.setattr(config_module, "resolve_llm_runtime_config", _fake_resolver)
    config = config_module.get_llm_config()

    assert isinstance(config, LLMConfig)
    assert config.model == "openai/gpt-4o-mini"
    assert config.provider_name == "openrouter"
    assert config.provider_mode == "gateway"
    assert config.base_url == "https://openrouter.ai/api/v1"
    assert config.extra_headers == {"X-Test": "1"}
    assert config.reasoning_effort == "medium"


def test_get_llm_config_falls_back_to_env(monkeypatch, tmp_path: Path) -> None:
    """Resolver failure should fall back to legacy env compatibility."""
    _reset_config_cache()
    monkeypatch.setattr(
        config_module,
        "resolve_llm_runtime_config",
        lambda: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    _set_temp_env_store(
        monkeypatch,
        tmp_path,
        "\n".join(
            [
                "LLM_MODEL=gpt-test",
                "LLM_HOST=https://api.openai.com/v1",
                "LLM_API_KEY=test-key",
                "LLM_BINDING=openai",
            ]
        )
        + "\n",
    )

    config = config_module.get_llm_config()
    assert config.model == "gpt-test"
    assert config.base_url == "https://api.openai.com/v1"
    assert config.binding == "openai"


def test_initialize_environment_sets_openai_env(monkeypatch) -> None:
    """initialize_environment should set OPENAI env vars from resolver output."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)

    monkeypatch.setattr(
        config_module,
        "resolve_llm_runtime_config",
        lambda: ResolvedLLMConfig(
            model="gpt-4o-mini",
            provider_name="openai",
            provider_mode="standard",
            binding_hint="openai",
            binding="openai",
            api_key="test-key",
            base_url="https://example.com/v1",
            effective_url="https://example.com/v1",
            api_version=None,
            extra_headers={},
            reasoning_effort=None,
        ),
    )
    config_module.initialize_environment()
    assert os.environ["OPENAI_API_KEY"] == "test-key"
    assert os.environ["OPENAI_BASE_URL"] == "https://example.com/v1"


def test_strip_value_handles_quotes() -> None:
    assert config_module._strip_value(" 'value' ") == "value"


def test_resolver_missing_model_raises(monkeypatch, tmp_path: Path) -> None:
    _reset_config_cache()

    monkeypatch.setattr(
        config_module,
        "resolve_llm_runtime_config",
        lambda: ResolvedLLMConfig(
            model="",
            provider_name="openai",
            provider_mode="standard",
            binding_hint="openai",
            binding="openai",
            api_key="test-key",
            base_url="https://example.com/v1",
            effective_url="https://example.com/v1",
            api_version=None,
            extra_headers={},
            reasoning_effort=None,
        ),
    )
    _set_temp_env_store(
        monkeypatch,
        tmp_path,
        "\n".join(
            [
                "LLM_MODEL=",
                "LLM_HOST=",
                "LLM_API_KEY=",
                "LLM_BINDING=openai",
            ]
        )
        + "\n",
    )

    with pytest.raises(LLMConfigError):
        config_module.get_llm_config()
