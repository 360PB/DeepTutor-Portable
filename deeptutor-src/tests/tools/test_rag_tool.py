"""Factory + tool-wrapper layer tests (llamaindex-only)."""

from __future__ import annotations

import pytest

from deeptutor.services.rag.factory import (
    DEFAULT_PROVIDER,
    get_pipeline,
    list_pipelines,
    normalize_provider_name,
)
from deeptutor.tools.rag_tool import (
    RAGService,
    get_available_providers,
    get_current_provider,
)


class TestNormalizeProviderName:
    """`normalize_provider_name` is now a stub: every input collapses to llamaindex."""

    @pytest.mark.parametrize(
        "value",
        [None, "", "  ", "llamaindex", "LlamaIndex", "lightrag", "raganything",
         "raganything_docling", "totally_unknown_xyz"],
    )
    def test_collapses_to_default(self, value) -> None:
        assert normalize_provider_name(value) == DEFAULT_PROVIDER


class TestPipelineFactory:
    def test_list_pipelines_only_default(self) -> None:
        pipelines = list_pipelines()
        assert isinstance(pipelines, list)
        assert {p["id"] for p in pipelines} == {DEFAULT_PROVIDER}

    def test_get_pipeline_returns_singleton(self) -> None:
        try:
            first = get_pipeline()
            second = get_pipeline()
        except (ValueError, ImportError) as exc:
            pytest.skip(f"LlamaIndex optional dependency missing: {exc}")
        assert first is second

    def test_get_pipeline_ignores_provider_name(self) -> None:
        """The legacy ``name`` argument is silently ignored."""
        try:
            a = get_pipeline("llamaindex")
            b = get_pipeline("lightrag")
            c = get_pipeline("nonexistent_xyz")
        except (ValueError, ImportError) as exc:
            pytest.skip(f"LlamaIndex optional dependency missing: {exc}")
        assert a is b is c


class TestRAGServiceClassHelpers:
    def test_list_providers_only_default(self) -> None:
        providers = RAGService.list_providers()
        assert {p["id"] for p in providers} == {DEFAULT_PROVIDER}

    def test_has_provider_default_true(self) -> None:
        assert RAGService.has_provider(DEFAULT_PROVIDER) is True

    def test_has_provider_unknown_false(self) -> None:
        assert RAGService.has_provider("nonexistent") is False
        assert RAGService.has_provider("") is False

    def test_get_current_provider_ignores_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("RAG_PROVIDER", "lightrag")
        assert get_current_provider() == DEFAULT_PROVIDER
        monkeypatch.delenv("RAG_PROVIDER", raising=False)
        assert get_current_provider() == DEFAULT_PROVIDER


class TestToolLayerExports:
    def test_get_available_providers_matches_class_method(self) -> None:
        assert get_available_providers() == RAGService.list_providers()
