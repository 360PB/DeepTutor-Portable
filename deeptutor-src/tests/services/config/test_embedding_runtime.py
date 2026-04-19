"""Tests for normalized embedding runtime resolution."""

from __future__ import annotations

from pathlib import Path

from deeptutor.services.config.env_store import EnvStore
from deeptutor.services.config.provider_runtime import resolve_embedding_runtime_config


def _build_catalog(
    *,
    embedding_profile: dict | None = None,
    embedding_model: dict | None = None,
) -> dict:
    embedding_profile = embedding_profile or {
        "id": "embedding-p",
        "name": "Embedding",
        "binding": "openai",
        "base_url": "",
        "api_key": "",
        "api_version": "",
        "extra_headers": {},
        "models": [{"id": "embedding-m", "name": "m", "model": "text-embedding-3-large"}],
    }
    embedding_model = embedding_model or embedding_profile["models"][0]
    return {
        "version": 1,
        "services": {
            "llm": {"active_profile_id": None, "active_model_id": None, "profiles": []},
            "embedding": {
                "active_profile_id": embedding_profile["id"],
                "active_model_id": embedding_model["id"],
                "profiles": [embedding_profile],
            },
            "search": {"active_profile_id": None, "profiles": []},
        },
    }


def _env(tmp_path: Path, lines: list[str]) -> EnvStore:
    defaults = [
        "EMBEDDING_BINDING=",
        "EMBEDDING_MODEL=",
        "EMBEDDING_API_KEY=",
        "EMBEDDING_HOST=",
        "EMBEDDING_DIMENSION=",
        "EMBEDDING_API_VERSION=",
        "OPENAI_API_KEY=",
        "AZURE_OPENAI_API_KEY=",
        "AZURE_API_KEY=",
        "COHERE_API_KEY=",
        "JINA_API_KEY=",
        "HOSTED_VLLM_API_KEY=",
    ]
    env_path = tmp_path / ".env"
    env_path.write_text("\n".join(defaults + lines) + "\n", encoding="utf-8")
    return EnvStore(path=env_path)


def test_embedding_explicit_binding_and_headers(tmp_path: Path) -> None:
    catalog = _build_catalog(
        embedding_profile={
            "id": "embedding-p",
            "name": "Embedding",
            "binding": "jina",
            "base_url": "",
            "api_key": "jina-key",
            "api_version": "",
            "extra_headers": {"X-App": "demo"},
            "models": [
                {
                    "id": "embedding-m",
                    "name": "jina",
                    "model": "jina-embeddings-v3",
                    "dimension": "1024",
                }
            ],
        }
    )
    env = _env(
        tmp_path,
        [
            "EMBEDDING_BINDING=",
            "EMBEDDING_MODEL=",
            "EMBEDDING_API_KEY=",
            "EMBEDDING_HOST=",
            "EMBEDDING_DIMENSION=",
            "EMBEDDING_API_VERSION=",
        ],
    )
    resolved = resolve_embedding_runtime_config(catalog=catalog, env_store=env)
    assert resolved.provider_name == "jina"
    assert resolved.provider_mode == "standard"
    assert resolved.effective_url == "https://api.jina.ai/v1"
    assert resolved.extra_headers == {"X-App": "demo"}
    assert resolved.dimension == 1024


def test_embedding_alias_canonicalization_google_to_openai(tmp_path: Path) -> None:
    catalog = _build_catalog(
        embedding_profile={
            "id": "embedding-p",
            "name": "Embedding",
            "binding": "google",
            "base_url": "",
            "api_key": "k",
            "api_version": "",
            "extra_headers": {},
            "models": [{"id": "embedding-m", "name": "m", "model": "text-embedding-3-small"}],
        }
    )
    resolved = resolve_embedding_runtime_config(catalog=catalog, env_store=_env(tmp_path, []))
    assert resolved.provider_name == "openai"
    assert resolved.binding == "openai"


def test_embedding_local_fallback_from_base_url(tmp_path: Path) -> None:
    catalog = _build_catalog(
        embedding_profile={
            "id": "embedding-p",
            "name": "Embedding",
            "binding": "",
            "base_url": "http://localhost:11434",
            "api_key": "",
            "api_version": "",
            "extra_headers": {},
            "models": [{"id": "embedding-m", "name": "m", "model": "nomic-embed-text"}],
        }
    )
    resolved = resolve_embedding_runtime_config(catalog=catalog, env_store=_env(tmp_path, []))
    assert resolved.provider_name == "ollama"
    assert resolved.provider_mode == "local"
    assert resolved.api_key == "sk-no-key-required"


def test_embedding_openai_default_base_injected(tmp_path: Path) -> None:
    catalog = _build_catalog(
        embedding_profile={
            "id": "embedding-p",
            "name": "Embedding",
            "binding": "openai",
            "base_url": "",
            "api_key": "sk-test",
            "api_version": "",
            "extra_headers": {},
            "models": [{"id": "embedding-m", "name": "m", "model": "text-embedding-3-large"}],
        }
    )
    resolved = resolve_embedding_runtime_config(catalog=catalog, env_store=_env(tmp_path, []))
    assert resolved.provider_name == "openai"
    assert resolved.effective_url == "https://api.openai.com/v1"


def test_embedding_provider_env_key_fallback(tmp_path: Path) -> None:
    catalog = _build_catalog(
        embedding_profile={
            "id": "embedding-p",
            "name": "Embedding",
            "binding": "cohere",
            "base_url": "",
            "api_key": "",
            "api_version": "",
            "extra_headers": {},
            "models": [{"id": "embedding-m", "name": "m", "model": "embed-v4.0"}],
        }
    )
    env = _env(
        tmp_path,
        [
            "COHERE_API_KEY=cohere-test-key",
            "EMBEDDING_BINDING=",
            "EMBEDDING_MODEL=",
            "EMBEDDING_API_KEY=",
            "EMBEDDING_HOST=",
            "EMBEDDING_DIMENSION=",
            "EMBEDDING_API_VERSION=",
        ],
    )
    resolved = resolve_embedding_runtime_config(catalog=catalog, env_store=env)
    assert resolved.provider_name == "cohere"
    assert resolved.api_key == "cohere-test-key"
