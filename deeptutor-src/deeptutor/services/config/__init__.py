"""Configuration helpers backed by runtime YAML and the project `.env` file."""

from .env_store import ConfigSummary, EnvStore, get_env_store
from .knowledge_base_config import (
    KnowledgeBaseConfigService,
    get_kb_config_service,
)
from .model_catalog import ModelCatalogService, get_model_catalog_service
from .loader import (
    PROJECT_ROOT,
    get_agent_params,
    get_runtime_settings_dir,
    get_path_from_config,
    load_config_with_main,
    parse_language,
    resolve_config_path,
)

__all__ = [
    "ConfigSummary",
    "EnvStore",
    "get_env_store",
    # From loader.py
    "PROJECT_ROOT",
    "get_runtime_settings_dir",
    "load_config_with_main",
    "resolve_config_path",
    "get_path_from_config",
    "parse_language",
    "get_agent_params",
    "ResolvedLLMConfig",
    "ResolvedEmbeddingConfig",
    "ResolvedSearchConfig",
    "resolve_llm_runtime_config",
    "resolve_embedding_runtime_config",
    "resolve_search_runtime_config",
    "search_provider_state",
    "NANOBOT_LLM_PROVIDERS",
    "SUPPORTED_SEARCH_PROVIDERS",
    "DEPRECATED_SEARCH_PROVIDERS",
    # From knowledge_base_config.py
    "KnowledgeBaseConfigService",
    "get_kb_config_service",
    "ModelCatalogService",
    "get_model_catalog_service",
    "ConfigTestRunner",
    "TestRun",
    "get_config_test_runner",
]


def __getattr__(name: str):
    """Lazy-load provider_runtime exports to avoid circular imports."""
    if name in {
        "DEPRECATED_SEARCH_PROVIDERS",
        "NANOBOT_LLM_PROVIDERS",
        "SUPPORTED_SEARCH_PROVIDERS",
        "ResolvedLLMConfig",
        "ResolvedEmbeddingConfig",
        "ResolvedSearchConfig",
        "resolve_embedding_runtime_config",
        "resolve_llm_runtime_config",
        "resolve_search_runtime_config",
        "search_provider_state",
    }:
        import importlib

        provider_runtime = importlib.import_module(f"{__name__}.provider_runtime")

        return getattr(provider_runtime, name)
    if name in {"ConfigTestRunner", "TestRun", "get_config_test_runner"}:
        import importlib

        test_runner = importlib.import_module(f"{__name__}.test_runner")
        return getattr(test_runner, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
