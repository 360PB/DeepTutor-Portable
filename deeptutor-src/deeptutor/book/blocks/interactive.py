"""Interactive block – self-contained interactive HTML widget.

Wraps :class:`deeptutor.agents.visualize.pipeline.VisualizePipeline` with
``render_mode="html"``. The payload carries an HTML document the frontend
renders in an isolated iframe.
"""

from __future__ import annotations

from typing import Any

from deeptutor.logging import get_logger

from ..models import BlockType, SourceAnchor
from .base import BlockContext, BlockGenerator, GenerationFailure

logger = get_logger("book.blocks.interactive")


class InteractiveGenerator(BlockGenerator):
    block_type = BlockType.INTERACTIVE

    async def _generate(
        self, ctx: BlockContext
    ) -> tuple[dict[str, Any], list[SourceAnchor], dict[str, Any]]:
        params = ctx.block.params
        chapter_title = params.get("chapter_title", ctx.chapter.title)
        chapter_summary = params.get("chapter_summary", ctx.chapter.summary)
        objectives = params.get("objectives") or ctx.chapter.learning_objectives
        focus = str(params.get("focus") or "")
        interaction = str(params.get("interaction") or "interactive")

        history_lines: list[str] = []
        if chapter_summary:
            history_lines.append(f"Chapter summary: {chapter_summary}")
        if objectives:
            history_lines.append("Learning objectives:")
            for obj in objectives:
                history_lines.append(f"- {obj}")
        history_context = "\n".join(history_lines)

        focus_clause = f" focusing on {focus}" if focus else ""
        user_input = (
            f"Build an {interaction} HTML page for the chapter "
            f"\"{chapter_title}\"{focus_clause}. The page should let the learner "
            "manipulate state, drag/click controls, or step through a guided "
            "demo to internalise the concept."
        )

        try:
            from deeptutor.agents.visualize.pipeline import VisualizePipeline
            from deeptutor.services.llm.config import get_llm_config

            llm_config = get_llm_config()
            pipeline = VisualizePipeline(
                api_key=llm_config.api_key,
                base_url=llm_config.base_url,
                api_version=llm_config.api_version,
                language=ctx.language,
            )
            analysis = await pipeline.run_analysis(
                user_input=user_input,
                history_context=history_context,
                render_mode="html",
            )
            code = await pipeline.run_code_generation(
                user_input=user_input,
                history_context=history_context,
                analysis=analysis,
            )
            review = await pipeline.run_review(
                user_input=user_input,
                analysis=analysis,
                code=code,
            )
        except Exception as exc:
            logger.warning(f"InteractiveGenerator failed: {exc}", exc_info=True)
            raise GenerationFailure(f"interactive generation failed: {exc}") from exc

        final_code = review.optimized_code or code

        return (
            {
                "render_type": "html",
                "code": {"language": "html", "content": final_code},
                "description": analysis.description,
                "chart_type": analysis.chart_type,
            },
            [],
            {
                "review_changed": review.changed,
                "review_notes": review.review_notes,
            },
        )


__all__ = ["InteractiveGenerator"]
