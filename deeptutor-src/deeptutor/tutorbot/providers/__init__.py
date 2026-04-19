"""LLM provider abstraction module."""

from deeptutor.tutorbot.providers.base import LLMProvider, LLMResponse

__all__ = ["LLMProvider", "LLMResponse", "OpenAICompatProvider", "AnthropicProvider"]


def __getattr__(name: str):
    if name == "OpenAICompatProvider":
        from deeptutor.tutorbot.providers.openai_compat_provider import OpenAICompatProvider
        return OpenAICompatProvider
    if name == "AnthropicProvider":
        from deeptutor.tutorbot.providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider
    # Legacy alias
    if name == "LiteLLMProvider":
        from deeptutor.tutorbot.providers.openai_compat_provider import OpenAICompatProvider
        return OpenAICompatProvider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
