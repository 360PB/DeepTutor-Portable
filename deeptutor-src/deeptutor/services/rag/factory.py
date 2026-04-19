"""RAG pipeline factory.

The project ships with a single LlamaIndex-backed pipeline. The helpers
below remain because several call-sites import them; they have all been
collapsed to operate on the single supported pipeline.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

DEFAULT_PROVIDER = "llamaindex"

# Cached pipeline instances keyed by kb_base_dir.
_PIPELINE_CACHE: Dict[Optional[str], Any] = {}


def normalize_provider_name(_name: Optional[str] = None) -> str:
    """Always return the canonical provider name.

    Older configs/migrations may carry legacy provider strings (e.g.
    ``lightrag``); they are all treated as the only supported pipeline.
    """
    return DEFAULT_PROVIDER


def get_pipeline(
    name: str = DEFAULT_PROVIDER,
    kb_base_dir: Optional[str] = None,
    **kwargs: Any,
):
    """Return the (cached) LlamaIndex pipeline instance.

    The ``name`` argument is accepted for backward compatibility but is
    ignored — only the LlamaIndex pipeline is supported.
    """
    from .pipelines.llamaindex import LlamaIndexPipeline

    if kwargs:
        # When custom kwargs are provided, build a fresh instance and skip
        # the cache to honour overrides.
        if kb_base_dir is not None:
            kwargs.setdefault("kb_base_dir", kb_base_dir)
        return LlamaIndexPipeline(**kwargs)

    if kb_base_dir not in _PIPELINE_CACHE:
        _PIPELINE_CACHE[kb_base_dir] = LlamaIndexPipeline(kb_base_dir=kb_base_dir)
    return _PIPELINE_CACHE[kb_base_dir]


def list_pipelines() -> List[Dict[str, str]]:
    """Return the single available pipeline (kept for callers that still ask)."""
    return [
        {
            "id": DEFAULT_PROVIDER,
            "name": "LlamaIndex",
            "description": "Pure vector retrieval, fastest processing speed.",
        }
    ]


__all__ = [
    "DEFAULT_PROVIDER",
    "get_pipeline",
    "list_pipelines",
    "normalize_provider_name",
]
