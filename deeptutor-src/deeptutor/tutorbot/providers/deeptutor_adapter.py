"""LLM provider adapter that reuses DeepTutor's LLM configuration.

When TutorBot runs in-process inside the DeepTutor server, this provider
reads api_key / model / base_url from DeepTutor's unified config and
delegates to the appropriate provider (OpenAICompat or Anthropic).
"""

from __future__ import annotations

from deeptutor.tutorbot.providers.base import LLMProvider


def create_deeptutor_provider() -> LLMProvider:
    """Build a provider pre-configured from DeepTutor's LLMConfig."""
    from deeptutor.services.llm.config import get_llm_config
    from deeptutor.services.provider_registry import find_by_model, find_by_name

    cfg = get_llm_config()

    api_key = cfg.api_key or None
    api_base = cfg.effective_url or cfg.base_url or None
    model = cfg.model
    extra_headers = cfg.extra_headers or {}
    provider_name = cfg.provider_name or None

    spec = None
    if provider_name:
        spec = find_by_name(provider_name)
    if spec is None and model:
        spec = find_by_model(model)

    backend = spec.backend if spec else "openai_compat"

    if backend == "anthropic":
        from deeptutor.tutorbot.providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider(
            api_key=api_key,
            api_base=api_base,
            default_model=model,
            extra_headers=extra_headers,
        )

    from deeptutor.tutorbot.providers.openai_compat_provider import OpenAICompatProvider
    return OpenAICompatProvider(
        api_key=api_key,
        api_base=api_base,
        default_model=model,
        extra_headers=extra_headers,
        spec=spec,
        provider_name=provider_name,
    )
