"""RAGService end-to-end behavior tests (with a fake pipeline)."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from deeptutor.services.rag.service import RAGService


class _FakePipeline:
    """Minimal pipeline stub that records calls and returns canned results."""

    def __init__(self, search_result: Dict[str, Any] | None = None) -> None:
        self.calls: list[dict] = []
        self.search_result = search_result or {
            "answer": "fake answer",
            "sources": [{"id": 1}],
            "provider": "lightrag",  # deliberately wrong; service must overwrite
        }

    async def initialize(self, kb_name: str, file_paths, **kwargs) -> bool:
        self.calls.append({"op": "initialize", "kb_name": kb_name, "files": list(file_paths)})
        return True

    async def search(self, query: str, kb_name: str, **kwargs) -> Dict[str, Any]:
        self.calls.append({"op": "search", "query": query, "kb_name": kb_name, "kwargs": kwargs})
        return dict(self.search_result)

    async def delete(self, kb_name: str) -> bool:
        self.calls.append({"op": "delete", "kb_name": kb_name})
        return True


@pytest.fixture
def fake_service(tmp_path) -> tuple[RAGService, _FakePipeline]:
    pipeline = _FakePipeline()
    service = RAGService(kb_base_dir=str(tmp_path))
    service._pipeline = pipeline  # type: ignore[attr-defined]
    return service, pipeline


def test_provider_argument_is_silently_ignored(tmp_path) -> None:
    """Constructor accepts ``provider`` for back-compat but always uses llamaindex."""
    service = RAGService(kb_base_dir=str(tmp_path), provider="lightrag")
    assert service.provider == "llamaindex"


@pytest.mark.asyncio
async def test_search_force_overwrites_provider_in_result(fake_service) -> None:
    """Even if the underlying pipeline lies about its provider, RAGService normalizes."""
    service, pipeline = fake_service
    pipeline.search_result = {"answer": "x", "provider": "raganything"}

    result = await service.search(query="hello", kb_name="kb")
    assert result["provider"] == "llamaindex"


@pytest.mark.asyncio
async def test_search_drops_mode_kwarg_before_calling_pipeline(fake_service) -> None:
    """The ``mode`` kwarg is intentionally consumed by the service layer."""
    service, pipeline = fake_service
    await service.search(query="hi", kb_name="kb", mode="hybrid", top_k=5)

    last = pipeline.calls[-1]
    assert last["op"] == "search"
    assert "mode" not in last["kwargs"]
    assert last["kwargs"].get("top_k") == 5


@pytest.mark.asyncio
async def test_search_aliases_answer_and_content(fake_service) -> None:
    """Pipelines that only return ``content`` should still expose ``answer`` and vice versa."""
    service, pipeline = fake_service

    pipeline.search_result = {"content": "only-content", "provider": "x"}
    result = await service.search(query="q", kb_name="kb")
    assert result["answer"] == "only-content"
    assert result["content"] == "only-content"
    assert result["query"] == "q"

    pipeline.search_result = {"answer": "only-answer", "provider": "x"}
    result = await service.search(query="q2", kb_name="kb")
    assert result["content"] == "only-answer"
    assert result["answer"] == "only-answer"


@pytest.mark.asyncio
async def test_smart_retrieve_aggregates_passages_with_query_hints(
    fake_service, monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, pipeline = fake_service
    pipeline.search_result = {"answer": "PASSAGE", "content": "PASSAGE", "provider": "x"}

    async def _fake_aggregate(_self, _ctx, passages):
        return "AGG:" + "|".join(passages)

    monkeypatch.setattr(RAGService, "_aggregate", _fake_aggregate, raising=True)

    out = await service.smart_retrieve(
        context="anything",
        kb_name="kb",
        query_hints=["q1", "q2"],
    )
    assert out["answer"].startswith("AGG:")
    assert out["answer"].count("PASSAGE") == 2
    assert len(out["sources"]) == 2
    queries = [c["query"] for c in pipeline.calls if c["op"] == "search"]
    assert queries == ["q1", "q2"]


@pytest.mark.asyncio
async def test_smart_retrieve_returns_empty_when_no_passages(
    fake_service, monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, pipeline = fake_service
    pipeline.search_result = {"answer": "", "content": "", "provider": "x"}

    out = await service.smart_retrieve(
        context="anything",
        kb_name="kb",
        query_hints=["q"],
    )
    assert out == {"answer": "", "sources": []}


@pytest.mark.asyncio
async def test_delete_removes_kb_directory_when_pipeline_lacks_delete(tmp_path) -> None:
    """Fallback path: delete the KB dir directly if the pipeline does not implement delete."""
    kb_dir = tmp_path / "demo"
    (kb_dir / "raw").mkdir(parents=True)
    (kb_dir / "raw" / "f.txt").write_text("hi")

    class _NoDeletePipeline:
        async def initialize(self, *a, **k):
            return True

        async def search(self, *a, **k):
            return {}

    service = RAGService(kb_base_dir=str(tmp_path))
    service._pipeline = _NoDeletePipeline()  # type: ignore[attr-defined]

    assert await service.delete(kb_name="demo") is True
    assert not kb_dir.exists()
