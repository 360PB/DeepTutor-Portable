"""Quiz block – delegates to the existing question generation coordinator."""

from __future__ import annotations

from typing import Any

from deeptutor.logging import get_logger

from ..models import BlockType, SourceAnchor
from .base import BlockContext, BlockGenerator, GenerationFailure

logger = get_logger("book.blocks.quiz")


class QuizGenerator(BlockGenerator):
    block_type = BlockType.QUIZ

    async def _generate(
        self, ctx: BlockContext
    ) -> tuple[dict[str, Any], list[SourceAnchor], dict[str, Any]]:
        params = ctx.block.params
        chapter_title = params.get("chapter_title", ctx.chapter.title)
        chapter_summary = params.get("chapter_summary", ctx.chapter.summary)
        objectives = params.get("objectives") or ctx.chapter.learning_objectives
        num_questions = max(1, min(8, int(params.get("num_questions") or 3)))
        difficulty = str(params.get("difficulty") or "medium")
        question_type = str(params.get("question_type") or "")

        topic = chapter_title.strip() or ctx.book_id
        preference = "; ".join(filter(None, [chapter_summary, *objectives]))

        try:
            from deeptutor.agents.question.coordinator import AgentCoordinator

            coordinator = AgentCoordinator(
                kb_name=ctx.primary_kb,
                language=ctx.language,
                enable_idea_rag=ctx.rag_enabled and bool(ctx.primary_kb),
            )
            summary = await coordinator.generate_from_topic(
                user_topic=topic,
                preference=preference,
                num_questions=num_questions,
                difficulty=difficulty,
                question_type=question_type,
            )
        except Exception as exc:
            logger.warning(f"QuizGenerator failed: {exc}", exc_info=True)
            raise GenerationFailure(f"quiz generation failed: {exc}") from exc

        questions = self._extract_questions(summary)
        if not questions:
            raise GenerationFailure("no questions generated")

        return (
            {"questions": questions, "topic": topic},
            [],
            {
                "completed": summary.get("completed", 0),
                "failed": summary.get("failed", 0),
                "kb": ctx.primary_kb,
            },
        )

    @staticmethod
    def _extract_questions(summary: dict[str, Any]) -> list[dict[str, Any]]:
        results = summary.get("results") or []
        if not isinstance(results, list):
            return []
        out: list[dict[str, Any]] = []
        for item in results:
            if not isinstance(item, dict) or not item.get("success"):
                continue
            qa = item.get("qa_pair") or {}
            if not isinstance(qa, dict):
                continue
            out.append(
                {
                    "question_id": qa.get("question_id", ""),
                    "question": qa.get("question", ""),
                    "question_type": qa.get("question_type", "written"),
                    "options": qa.get("options") or {},
                    "correct_answer": qa.get("correct_answer", ""),
                    "explanation": qa.get("explanation", ""),
                    "difficulty": qa.get("difficulty", ""),
                    "concentration": qa.get("concentration", ""),
                }
            )
        return out


__all__ = ["QuizGenerator"]
