"""
Answer-Now Helpers
==================

Per-capability fast-path utilities for the universal "Answer now" interrupt.

Each capability owns *what* its fast path produces (text answer, quiz JSON,
manim code, ...). This module provides the shared plumbing:

* :func:`extract_answer_now_context` — parse and validate the payload that
  the frontend bundled with the cancelled turn.
* :func:`format_trace_summary` — render captured stream events into a
  compact, prompt-friendly summary the LLM can read in one shot.
* :func:`stream_synthesis` — thin async generator wrapper around the LLM
  service that yields text chunks while pushing them into the StreamBus.
* :func:`make_skip_notice` — i18n-aware notice prepended/appended to the
  fast-path output so the user knows which stages were skipped.

The orchestrator no longer re-routes ``answer_now`` to ``chat``; instead
each capability checks for the payload at the top of ``run()`` and
dispatches to its own answer-now path. ``chat`` keeps its original
synthesis behavior; structured-output capabilities (deep_question,
math_animator, visualize) collapse the remaining stages into a single
LLM call (or a code-gen + render pair, in math_animator's case).
"""

from __future__ import annotations

from typing import Any, AsyncIterator

from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream_bus import StreamBus
from deeptutor.core.trace import build_trace_metadata, merge_trace_metadata, new_call_id
from deeptutor.services.llm import (
    clean_thinking_tags,
    get_llm_config,
    get_token_limit_kwargs,
    stream as llm_stream,
)


# Per-event content cap. The trace can grow unbounded (especially for
# deep_research / deep_solve with many tool calls) so we truncate each
# entry rather than the whole transcript — this preserves event
# coverage at the cost of detail per step.
_MAX_EVENT_SNIPPET = 800
# Total trace summary cap. Far above this and we start eating into the
# answer budget on small-context models.
_MAX_TRACE_TOTAL = 6000


def extract_answer_now_context(context: UnifiedContext) -> dict[str, Any] | None:
    """
    Return the validated ``answer_now_context`` payload or ``None``.

    The frontend always packages ``original_user_message`` + an optional
    ``partial_response`` + an ``events`` array. We require at minimum a
    non-empty ``original_user_message`` because that's what every
    fast-path prompt is anchored on; if it is missing the capability
    falls through to its normal pipeline.
    """
    raw = context.config_overrides.get("answer_now_context")
    if not isinstance(raw, dict):
        return None
    if not str(raw.get("original_user_message") or "").strip():
        return None
    return raw


def format_trace_summary(events: Any, *, language: str = "en") -> str:
    """Render captured stream events into a compact text summary.

    Truncates each event to ``_MAX_EVENT_SNIPPET`` chars and the whole
    transcript to ``_MAX_TRACE_TOTAL`` chars so the prompt stays bounded.
    """
    fallback = (
        "没有可用的中间执行记录。"
        if language.startswith("zh")
        else "No intermediate execution trace was provided."
    )
    if not isinstance(events, list) or not events:
        return fallback

    lines: list[str] = []
    for index, event in enumerate(events, start=1):
        if not isinstance(event, dict):
            continue
        event_type = str(event.get("type") or "event").strip()
        stage = str(event.get("stage") or "").strip()
        content = str(event.get("content") or "").strip()
        metadata = event.get("metadata") if isinstance(event.get("metadata"), dict) else {}

        label_parts = [event_type]
        if stage:
            label_parts.append(stage)
        line = f"{index}. {' / '.join(label_parts)}"
        if content:
            snippet = (
                content
                if len(content) <= _MAX_EVENT_SNIPPET
                else content[: _MAX_EVENT_SNIPPET - 3].rstrip() + "..."
            )
            line += f": {snippet}"
        if isinstance(metadata, dict):
            tool_name = str(metadata.get("tool_name") or metadata.get("tool") or "").strip()
            if tool_name:
                line += f" [tool={tool_name}]"
        lines.append(line)

    if not lines:
        return fallback

    text = "\n".join(lines)
    if len(text) > _MAX_TRACE_TOTAL:
        text = text[: _MAX_TRACE_TOTAL - 3].rstrip() + "..."
    return text


def labeled_block(label: str, content: str) -> str:
    """Format a labeled section in a way the LLM reliably picks up."""
    body = content.strip() if isinstance(content, str) and content.strip() else "(empty)"
    return f"[{label}]\n{body}"


def make_skip_notice(*, capability: str, language: str, stages_skipped: list[str]) -> str:
    """A short user-visible note prepended to the fast-path output.

    Helps the user understand that the result is a "best-effort early
    exit" rather than the full pipeline output.
    """
    if not stages_skipped:
        return ""
    if language.startswith("zh"):
        joined = "、".join(stages_skipped)
        return (
            f"> ⚡ 已跳过 `{capability}` 的 {joined} 阶段，以下为基于已有信息的快速结果。"
        )
    joined = ", ".join(stages_skipped)
    return (
        f"> ⚡ Skipped {joined} stage(s) of `{capability}`; the result below is "
        f"a best-effort synthesis from the partial trace."
    )


def build_answer_now_trace_metadata(
    *,
    capability: str,
    phase: str,
    label: str,
) -> dict[str, Any]:
    """Standard trace card metadata for an answer-now stage."""
    return build_trace_metadata(
        call_id=new_call_id(f"{capability}-answer-now"),
        phase=phase,
        label=label,
        call_kind="llm_final_response",
        trace_id=f"{capability}-answer-now",
        trace_role="response",
        trace_group="stage",
    )


async def stream_synthesis(
    *,
    stream: StreamBus,
    source: str,
    stage: str,
    trace_meta: dict[str, Any],
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 1800,
    push_content: bool = True,
    response_format: dict[str, Any] | None = None,
) -> AsyncIterator[str]:
    """
    Stream a single LLM synthesis call into the StreamBus.

    Yields raw chunks (still useful for capabilities that need to
    parse them, e.g. structured JSON outputs). When ``push_content``
    is true (default), every chunk is also pushed as a ``CONTENT``
    event so the frontend renders the answer live.
    """
    llm_config = get_llm_config()
    model = getattr(llm_config, "model", None)

    await stream.progress(
        trace_meta.get("label", "Answer now"),
        source=source,
        stage=stage,
        metadata=merge_trace_metadata(
            trace_meta,
            {"trace_kind": "call_status", "call_state": "running"},
        ),
    )

    extra_kwargs: dict[str, Any] = {"temperature": 0.2}
    if model:
        extra_kwargs.update(get_token_limit_kwargs(model, max_tokens))
    if response_format is not None:
        extra_kwargs["response_format"] = response_format

    chunks: list[str] = []
    try:
        async for chunk in llm_stream(
            prompt=user_prompt,
            system_prompt=system_prompt,
            **extra_kwargs,
        ):
            if not chunk:
                continue
            chunks.append(chunk)
            if push_content:
                await stream.content(
                    chunk,
                    source=source,
                    stage=stage,
                    metadata=merge_trace_metadata(trace_meta, {"trace_kind": "llm_chunk"}),
                )
            yield chunk
    finally:
        await stream.progress(
            "",
            source=source,
            stage=stage,
            metadata=merge_trace_metadata(
                trace_meta,
                {"trace_kind": "call_status", "call_state": "complete"},
            ),
        )


def join_chunks(chunks: list[str]) -> str:
    """Concatenate chunks and strip OpenAI-style ``<think>`` wrappers."""
    text = "".join(chunks)
    llm_config = get_llm_config()
    binding = getattr(llm_config, "binding", None) or "openai"
    model = getattr(llm_config, "model", None)
    return clean_thinking_tags(text, binding, model)


__all__ = [
    "build_answer_now_trace_metadata",
    "extract_answer_now_context",
    "format_trace_summary",
    "join_chunks",
    "labeled_block",
    "make_skip_notice",
    "stream_synthesis",
]
