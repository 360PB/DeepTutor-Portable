"""RAG service exports."""

from .factory import (
    DEFAULT_PROVIDER,
    get_pipeline,
    list_pipelines,
    normalize_provider_name,
)
from .file_routing import DocumentType, FileClassification, FileTypeRouter
from .service import RAGService


def __getattr__(name: str):
    """Lazy import pipeline implementation classes."""
    if name == "LlamaIndexPipeline":
        from .pipelines.llamaindex import LlamaIndexPipeline

        return LlamaIndexPipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "RAGService",
    "FileTypeRouter",
    "FileClassification",
    "DocumentType",
    "get_pipeline",
    "list_pipelines",
    "normalize_provider_name",
    "DEFAULT_PROVIDER",
    "LlamaIndexPipeline",
]
