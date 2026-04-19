from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from deeptutor.api.routers import settings as settings_router
from deeptutor.services.config.provider_runtime import (
    ResolvedEmbeddingConfig,
    ResolvedLLMConfig,
)
from deeptutor.services.embedding import client as embedding_client_module
from deeptutor.services.embedding import config as embedding_config_module
from deeptutor.services.llm import client as llm_client_module
from deeptutor.services.llm import config as llm_config_module


class _DummyLogger:
    def debug(self, *_args, **_kwargs) -> None:
        pass

    def error(self, *_args, **_kwargs) -> None:
        pass

    def info(self, *_args, **_kwargs) -> None:
        pass


class _FakeEmbeddingAdapter:
    def __init__(self, config: dict[str, Any]):
        self.config = config

    async def embed(self, request):
        return type("EmbeddingResponse", (), {"embeddings": [[] for _ in request.texts]})()


class _FakeCatalogService:
    def __init__(self, catalog: dict[str, Any]):
        self._catalog = deepcopy(catalog)

    def save(self, catalog: dict[str, Any]) -> dict[str, Any]:
        self._catalog = deepcopy(catalog)
        return deepcopy(self._catalog)

    def load(self) -> dict[str, Any]:
        return deepcopy(self._catalog)

    def apply(self, catalog: dict[str, Any]) -> dict[str, str]:
        current = self.save(catalog)
        llm_profile = current["services"]["llm"]["profiles"][0]
        llm_model = llm_profile["models"][0]
        embedding_profile = current["services"]["embedding"]["profiles"][0]
        embedding_model = embedding_profile["models"][0]
        return {
            "LLM_BINDING": llm_profile["binding"],
            "LLM_API_KEY": llm_profile["api_key"],
            "LLM_HOST": llm_profile["base_url"],
            "LLM_MODEL": llm_model["model"],
            "EMBEDDING_BINDING": embedding_profile["binding"],
            "EMBEDDING_API_KEY": embedding_profile["api_key"],
            "EMBEDDING_HOST": embedding_profile["base_url"],
            "EMBEDDING_MODEL": embedding_model["model"],
        }


def _build_catalog(
    *,
    llm_model: str,
    llm_base_url: str,
    llm_api_key: str,
    embedding_model: str,
    embedding_base_url: str,
    embedding_api_key: str,
) -> dict[str, Any]:
    return {
        "version": 1,
        "services": {
            "llm": {
                "active_profile_id": "llm-profile-default",
                "active_model_id": "llm-model-default",
                "profiles": [
                    {
                        "id": "llm-profile-default",
                        "name": "Default LLM Endpoint",
                        "binding": "openai",
                        "base_url": llm_base_url,
                        "api_key": llm_api_key,
                        "api_version": "",
                        "extra_headers": {},
                        "models": [
                            {
                                "id": "llm-model-default",
                                "name": llm_model,
                                "model": llm_model,
                            }
                        ],
                    }
                ],
            },
            "embedding": {
                "active_profile_id": "embedding-profile-default",
                "active_model_id": "embedding-model-default",
                "profiles": [
                    {
                        "id": "embedding-profile-default",
                        "name": "Default Embedding Endpoint",
                        "binding": "openai",
                        "base_url": embedding_base_url,
                        "api_key": embedding_api_key,
                        "api_version": "",
                        "extra_headers": {},
                        "models": [
                            {
                                "id": "embedding-model-default",
                                "name": embedding_model,
                                "model": embedding_model,
                                "dimension": "1536",
                            }
                        ],
                    }
                ],
            },
            "search": {
                "active_profile_id": None,
                "profiles": [],
            },
        },
    }


def _patch_runtime(
    monkeypatch: pytest.MonkeyPatch,
    service: _FakeCatalogService,
) -> None:
    monkeypatch.setattr(settings_router, "get_model_catalog_service", lambda: service)
    monkeypatch.setattr(llm_client_module, "get_logger", lambda *_args, **_kwargs: _DummyLogger())
    monkeypatch.setattr(
        embedding_client_module,
        "get_logger",
        lambda *_args, **_kwargs: _DummyLogger(),
    )
    monkeypatch.setattr(
        embedding_client_module,
        "_resolve_adapter_class",
        lambda _binding: _FakeEmbeddingAdapter,
    )

    def _resolve_llm_runtime_config() -> ResolvedLLMConfig:
        catalog = service.load()
        profile = catalog["services"]["llm"]["profiles"][0]
        model = profile["models"][0]
        return ResolvedLLMConfig(
            model=model["model"],
            provider_name=profile["binding"],
            provider_mode="standard",
            binding_hint=profile["binding"],
            binding=profile["binding"],
            api_key=profile["api_key"],
            base_url=profile["base_url"],
            effective_url=profile["base_url"],
            api_version=None,
            extra_headers={},
            reasoning_effort=None,
        )

    def _resolve_embedding_runtime_config() -> ResolvedEmbeddingConfig:
        catalog = service.load()
        profile = catalog["services"]["embedding"]["profiles"][0]
        model = profile["models"][0]
        return ResolvedEmbeddingConfig(
            model=model["model"],
            provider_name=profile["binding"],
            provider_mode="standard",
            binding_hint=profile["binding"],
            binding=profile["binding"],
            api_key=profile["api_key"],
            base_url=profile["base_url"],
            effective_url=profile["base_url"],
            api_version=None,
            extra_headers={},
            dimension=int(model["dimension"]),
            request_timeout=60,
            batch_size=10,
        )

    monkeypatch.setattr(
        llm_config_module,
        "resolve_llm_runtime_config",
        _resolve_llm_runtime_config,
    )
    monkeypatch.setattr(
        embedding_config_module,
        "resolve_embedding_runtime_config",
        _resolve_embedding_runtime_config,
    )


@pytest.fixture(autouse=True)
def _reset_runtime_state() -> None:
    llm_config_module.clear_llm_config_cache()
    llm_client_module.reset_llm_client()
    embedding_client_module.reset_embedding_client()
    yield
    llm_config_module.clear_llm_config_cache()
    llm_client_module.reset_llm_client()
    embedding_client_module.reset_embedding_client()


@pytest.mark.asyncio
async def test_update_catalog_invalidates_runtime_caches(monkeypatch: pytest.MonkeyPatch) -> None:
    initial_catalog = _build_catalog(
        llm_model="gpt-old",
        llm_base_url="https://old-llm.example/v1",
        llm_api_key="old-llm-key",
        embedding_model="text-embedding-old",
        embedding_base_url="https://old-embedding.example/v1",
        embedding_api_key="old-embedding-key",
    )
    updated_catalog = _build_catalog(
        llm_model="gpt-new",
        llm_base_url="https://new-llm.example/v1",
        llm_api_key="new-llm-key",
        embedding_model="text-embedding-new",
        embedding_base_url="https://new-embedding.example/v1",
        embedding_api_key="new-embedding-key",
    )
    service = _FakeCatalogService(initial_catalog)
    _patch_runtime(monkeypatch, service)

    old_llm_config = llm_config_module.get_llm_config()
    old_llm_client = llm_client_module.get_llm_client()
    old_embedding_client = embedding_client_module.get_embedding_client()

    response = await settings_router.update_catalog(
        settings_router.CatalogPayload(catalog=updated_catalog)
    )

    new_llm_config = llm_config_module.get_llm_config()
    new_llm_client = llm_client_module.get_llm_client()
    new_embedding_client = embedding_client_module.get_embedding_client()

    assert response == {"catalog": updated_catalog}
    assert old_llm_config.model == "gpt-old"
    assert new_llm_config.model == "gpt-new"
    assert new_llm_config.base_url == "https://new-llm.example/v1"
    assert new_llm_config is not old_llm_config
    assert new_llm_client is not old_llm_client
    assert new_llm_client.config.model == "gpt-new"
    assert new_embedding_client is not old_embedding_client
    assert new_embedding_client.config.model == "text-embedding-new"
    assert new_embedding_client.config.base_url == "https://new-embedding.example/v1"


@pytest.mark.asyncio
async def test_apply_catalog_invalidates_runtime_caches(monkeypatch: pytest.MonkeyPatch) -> None:
    initial_catalog = _build_catalog(
        llm_model="gpt-before-apply",
        llm_base_url="https://before-apply-llm.example/v1",
        llm_api_key="before-apply-llm-key",
        embedding_model="text-embedding-before-apply",
        embedding_base_url="https://before-apply-embedding.example/v1",
        embedding_api_key="before-apply-embedding-key",
    )
    applied_catalog = _build_catalog(
        llm_model="gpt-after-apply",
        llm_base_url="https://after-apply-llm.example/v1",
        llm_api_key="after-apply-llm-key",
        embedding_model="text-embedding-after-apply",
        embedding_base_url="https://after-apply-embedding.example/v1",
        embedding_api_key="after-apply-embedding-key",
    )
    service = _FakeCatalogService(initial_catalog)
    _patch_runtime(monkeypatch, service)

    llm_config_module.get_llm_config()
    old_llm_client = llm_client_module.get_llm_client()
    old_embedding_client = embedding_client_module.get_embedding_client()

    response = await settings_router.apply_catalog(
        settings_router.CatalogPayload(catalog=applied_catalog)
    )

    new_llm_config = llm_config_module.get_llm_config()
    new_llm_client = llm_client_module.get_llm_client()
    new_embedding_client = embedding_client_module.get_embedding_client()

    assert response["catalog"] == applied_catalog
    assert response["env"]["LLM_MODEL"] == "gpt-after-apply"
    assert response["env"]["EMBEDDING_MODEL"] == "text-embedding-after-apply"
    assert new_llm_config.model == "gpt-after-apply"
    assert new_llm_client is not old_llm_client
    assert new_llm_client.config.base_url == "https://after-apply-llm.example/v1"
    assert new_embedding_client is not old_embedding_client
    assert new_embedding_client.config.model == "text-embedding-after-apply"


@pytest.mark.asyncio
async def test_complete_tour_invalidates_runtime_caches(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    initial_catalog = _build_catalog(
        llm_model="gpt-before-tour",
        llm_base_url="https://before-tour-llm.example/v1",
        llm_api_key="before-tour-llm-key",
        embedding_model="text-embedding-before-tour",
        embedding_base_url="https://before-tour-embedding.example/v1",
        embedding_api_key="before-tour-embedding-key",
    )
    completed_catalog = _build_catalog(
        llm_model="gpt-after-tour",
        llm_base_url="https://after-tour-llm.example/v1",
        llm_api_key="after-tour-llm-key",
        embedding_model="text-embedding-after-tour",
        embedding_base_url="https://after-tour-embedding.example/v1",
        embedding_api_key="after-tour-embedding-key",
    )
    service = _FakeCatalogService(initial_catalog)
    _patch_runtime(monkeypatch, service)

    tour_cache = tmp_path / ".tour_cache.json"
    tour_cache.write_text('{"status": "running"}', encoding="utf-8")
    monkeypatch.setattr(settings_router, "TOUR_CACHE", tour_cache)

    llm_config_module.get_llm_config()
    old_llm_client = llm_client_module.get_llm_client()
    old_embedding_client = embedding_client_module.get_embedding_client()

    response = await settings_router.complete_tour(
        settings_router.TourCompletePayload(catalog=completed_catalog)
    )

    new_llm_config = llm_config_module.get_llm_config()
    new_llm_client = llm_client_module.get_llm_client()
    new_embedding_client = embedding_client_module.get_embedding_client()
    cache = tour_cache.read_text(encoding="utf-8")

    assert response["env"]["LLM_MODEL"] == "gpt-after-tour"
    assert response["env"]["EMBEDDING_MODEL"] == "text-embedding-after-tour"
    assert response["status"] == "completed"
    assert new_llm_config.model == "gpt-after-tour"
    assert new_llm_client is not old_llm_client
    assert new_embedding_client is not old_embedding_client
    assert '"status": "completed"' in cache
