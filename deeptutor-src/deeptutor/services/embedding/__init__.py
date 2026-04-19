"""
Embedding Service
=================

Unified embedding client for all DeepTutor modules.
Supports normalized providers: custom/openai/azure_openai/cohere/jina/ollama/vllm.

Usage:
    from deeptutor.services.embedding import get_embedding_client, EmbeddingClient, EmbeddingConfig

    # Get singleton client
    client = get_embedding_client()
    vectors = await client.embed(["text1", "text2"])

    # Get an async embedding callable
    embed_func = client.get_embedding_func()
"""

from .adapters import (
    BaseEmbeddingAdapter,
    CohereEmbeddingAdapter,
    EmbeddingRequest,
    EmbeddingResponse,
    JinaEmbeddingAdapter,
    OllamaEmbeddingAdapter,
    OpenAICompatibleEmbeddingAdapter,
)
from .client import EmbeddingClient, get_embedding_client, reset_embedding_client
from .config import EmbeddingConfig, get_embedding_config

__all__ = [
    "EmbeddingClient",
    "EmbeddingConfig",
    "get_embedding_client",
    "get_embedding_config",
    "reset_embedding_client",
    "BaseEmbeddingAdapter",
    "EmbeddingRequest",
    "EmbeddingResponse",
    "OpenAICompatibleEmbeddingAdapter",
    "CohereEmbeddingAdapter",
    "JinaEmbeddingAdapter",
    "OllamaEmbeddingAdapter",
]
