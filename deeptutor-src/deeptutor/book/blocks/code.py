"""Code block – generates a runnable code snippet plus brief explanation.

Phase 2 implementation. Uses the unified LLM service with a strict JSON
response. The frontend ``CodeBlock`` component renders the code and the
explanation side-by-side; the playground "code_execution" tool can be
hooked in later for live runs.

Prompts live in ``deeptutor/book/prompts/{en,zh}/code.yaml``.
"""

from __future__ import annotations

import json
from typing import Any

from ..models import BlockType, SourceAnchor
from ._llm_writer import llm_text
from ._prompts import get_book_prompt, load_book_prompts
from .base import BlockContext, BlockGenerator, GenerationFailure


class CodeGenerator(BlockGenerator):
    block_type = BlockType.CODE

    async def _generate(
        self, ctx: BlockContext
    ) -> tuple[dict[str, Any], list[SourceAnchor], dict[str, Any]]:
        params = ctx.block.params
        chapter_title = params.get("chapter_title", ctx.chapter.title)
        chapter_summary = params.get("chapter_summary", ctx.chapter.summary)
        objectives = params.get("objectives") or ctx.chapter.learning_objectives
        language = str(params.get("language") or "python")
        intent = str(params.get("intent") or "demonstrate")

        prompts = load_book_prompts("code", ctx.language)
        none_label = "(无)" if ctx.language == "zh" else "(none)"
        user_prompt = get_book_prompt(prompts, "user_template").format(
            chapter_title=chapter_title,
            chapter_summary=chapter_summary or none_label,
            objectives_inline="; ".join(objectives) or none_label,
            intent=intent,
            language=language,
        )
        raw = await llm_text(
            user_prompt=user_prompt,
            system_prompt=get_book_prompt(prompts, "system"),
            max_tokens=900,
            temperature=0.3,
            response_format={"type": "json_object"},
            language=ctx.language,
        )

        data = _safe_json(raw)
        code = str(data.get("code") or "").strip()
        if not code:
            raise GenerationFailure("LLM did not return any code.")
        return (
            {
                "language": str(data.get("language") or language).strip() or language,
                "code": code,
                "explanation": str(data.get("explanation") or "").strip(),
                "intent": intent,
            },
            [],
            {},
        )


def _safe_json(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        idx = raw.find("\n")
        if idx > 0 and not raw[:idx].strip().startswith("{"):
            raw = raw[idx + 1 :]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


__all__ = ["CodeGenerator"]
