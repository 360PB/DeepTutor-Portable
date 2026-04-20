"""
Shared LLM helper for text-flavoured block generators.

Avoids subclassing BaseAgent for these tiny calls; instead uses
``deeptutor.services.llm.complete`` directly with a sane default config.
"""

from __future__ import annotations

from typing import Any

from deeptutor.services.llm import (
    clean_thinking_tags,
    complete as llm_complete,
    get_llm_config,
    get_token_limit_kwargs,
)

from ._language import language_directive


async def llm_text(
    *,
    user_prompt: str,
    system_prompt: str,
    max_tokens: int = 1200,
    temperature: float = 0.4,
    response_format: dict[str, Any] | None = None,
    language: str | None = None,
) -> str:
    """Run an LLM completion for a Book block / agent.

    Pass ``language`` (the book's chosen language code, e.g. ``"zh"`` or
    ``"en"``) and the helper appends a strict language directive to the
    system prompt. This is the single chokepoint that prevents the LLM from
    drifting between languages when prompts contain English token names,
    JSON keys, or non-matching source material.
    """
    if language:
        system_prompt = system_prompt.rstrip() + language_directive(language)

    config = get_llm_config()
    model = config.model
    binding = getattr(config, "binding", None) or "openai"
    kwargs: dict[str, Any] = {"temperature": temperature}
    kwargs.update(get_token_limit_kwargs(model, max_tokens))
    if response_format:
        kwargs["response_format"] = response_format
    response = await llm_complete(
        prompt=user_prompt,
        system_prompt=system_prompt,
        model=model,
        api_key=config.api_key,
        base_url=config.base_url,
        api_version=getattr(config, "api_version", None),
        binding=binding,
        **kwargs,
    )
    return clean_thinking_tags(response, binding, model).strip()


__all__ = ["llm_text"]
