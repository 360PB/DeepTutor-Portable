"""
Multimodal Message Utilities
=============================

Converts plain-text messages + image attachments into the multimodal
message format expected by vision-capable LLMs.

Supports:
- OpenAI-compatible API (content array with image_url blocks)
- Anthropic API (content array with image source blocks)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from .capabilities import supports_vision

logger = logging.getLogger(__name__)

MIME_FALLBACK = "image/png"


@dataclass
class MultimodalResult:
    """Result of multimodal message preparation."""

    messages: list[dict[str, Any]]
    vision_supported: bool
    images_stripped: bool


def _guess_mime_type(filename: str, fallback: str = MIME_FALLBACK) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "webp": "image/webp",
        "svg": "image/svg+xml",
    }.get(ext, fallback)


def _build_openai_image_part(
    *,
    base64_data: str,
    mime_type: str,
    url: str = "",
) -> dict[str, Any]:
    if url:
        image_url = url
    else:
        image_url = f"data:{mime_type};base64,{base64_data}"
    return {"type": "image_url", "image_url": {"url": image_url}}


def _build_anthropic_image_part(
    *,
    base64_data: str,
    mime_type: str,
) -> dict[str, Any]:
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": base64_data,
        },
    }


def prepare_multimodal_messages(
    messages: list[dict[str, Any]],
    attachments: list[Any] | None,
    binding: str = "openai",
    model: str | None = None,
) -> MultimodalResult:
    """
    Inject image attachments into the last user message.

    If the model supports vision the last user message ``content`` field is
    converted from a plain string into a content-parts array that includes
    both the original text and the image(s).

    If the model does **not** support vision, the messages are returned
    unchanged and ``images_stripped`` is set to ``True`` so the caller
    can emit a warning to the user.

    Args:
        messages: The OpenAI-style messages list (may be mutated).
        attachments: ``Attachment`` objects from ``UnifiedContext``.
        binding: Provider binding (``"openai"``, ``"anthropic"``, …).
        model: Model name used for capability lookup.

    Returns:
        A ``MultimodalResult`` with the (potentially modified) messages.
    """
    if not attachments:
        return MultimodalResult(
            messages=messages,
            vision_supported=True,
            images_stripped=False,
        )

    image_attachments = [a for a in attachments if getattr(a, "type", "") == "image"]
    if not image_attachments:
        return MultimodalResult(
            messages=messages,
            vision_supported=True,
            images_stripped=False,
        )

    vision_ok = supports_vision(binding, model)

    if not vision_ok:
        logger.info(
            "Model %s/%s does not support vision – stripping %d image(s)",
            binding,
            model,
            len(image_attachments),
        )
        return MultimodalResult(
            messages=messages,
            vision_supported=False,
            images_stripped=True,
        )

    last_user_idx = _find_last_user_message(messages)
    if last_user_idx is None:
        return MultimodalResult(
            messages=messages,
            vision_supported=True,
            images_stripped=False,
        )

    is_anthropic = (binding or "").lower() in ("anthropic", "claude")
    _inject_images(
        messages,
        last_user_idx,
        image_attachments,
        anthropic=is_anthropic,
    )

    return MultimodalResult(
        messages=messages,
        vision_supported=True,
        images_stripped=False,
    )


def _find_last_user_message(messages: list[dict[str, Any]]) -> int | None:
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].get("role") == "user":
            return i
    return None


def _inject_images(
    messages: list[dict[str, Any]],
    user_idx: int,
    image_attachments: list[Any],
    *,
    anthropic: bool = False,
) -> None:
    msg = messages[user_idx]
    original_content = msg.get("content", "")

    if isinstance(original_content, str):
        content_parts: list[dict[str, Any]] = [{"type": "text", "text": original_content}]
    elif isinstance(original_content, list):
        content_parts = list(original_content)
    else:
        content_parts = [{"type": "text", "text": str(original_content)}]

    for att in image_attachments:
        mime = getattr(att, "mime_type", "") or _guess_mime_type(
            getattr(att, "filename", "image.png")
        )
        b64 = getattr(att, "base64", "") or ""
        url = getattr(att, "url", "") or ""

        if not b64 and not url:
            continue

        if anthropic:
            content_parts.append(_build_anthropic_image_part(base64_data=b64, mime_type=mime))
        else:
            content_parts.append(
                _build_openai_image_part(base64_data=b64, mime_type=mime, url=url)
            )

    messages[user_idx] = {**msg, "content": content_parts}


__all__ = [
    "MultimodalResult",
    "prepare_multimodal_messages",
]
