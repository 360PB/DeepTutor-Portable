"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, XCircle, Eye, EyeOff } from "lucide-react";
import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import type { Block } from "@/lib/book-types";

export interface QuizAttemptArgs {
  questionId?: string;
  userAnswer?: string;
  isCorrect: boolean;
}

interface QuizQuestion {
  question_id?: string;
  question?: string;
  question_type?: string;
  options?: Record<string, string> | null;
  correct_answer?: string;
  explanation?: string;
  difficulty?: string;
}

export interface QuizBlockProps {
  block: Block;
  onAttempt?: (block: Block, args: QuizAttemptArgs) => void;
}

export default function QuizBlock({ block, onAttempt }: QuizBlockProps) {
  const questions = (block.payload?.questions as QuizQuestion[] | undefined) || [];
  if (questions.length === 0) {
    return (
      <div className="text-sm text-[var(--muted-foreground)]">
        No quiz questions generated.
      </div>
    );
  }
  return (
    <section>
      <div className="mb-3 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--primary)]">
        <span className="h-px flex-1 bg-[var(--primary)]/20" />
        Quick Check
        <span className="h-px flex-1 bg-[var(--primary)]/20" />
      </div>
      <div className="space-y-3">
        {questions.map((q, idx) => (
          <QuizQuestionCard
            key={q.question_id || idx}
            index={idx}
            question={q}
            onAttempt={(args) => onAttempt?.(block, args)}
          />
        ))}
      </div>
    </section>
  );
}

function QuizQuestionCard({
  index,
  question,
  onAttempt,
}: {
  index: number;
  question: QuizQuestion;
  onAttempt?: (args: QuizAttemptArgs) => void;
}) {
  const [selected, setSelected] = useState<string | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [reported, setReported] = useState(false);
  const isMultiple =
    (question.question_type || "").toLowerCase() === "multiple_choice";
  const correct = String(question.correct_answer || "").trim();
  const options = question.options || {};

  useEffect(() => {
    if (revealed && selected && !reported && onAttempt) {
      onAttempt({
        questionId: question.question_id,
        userAnswer: selected,
        isCorrect: selected === correct,
      });
      setReported(true);
    }
  }, [revealed, selected, reported, onAttempt, question.question_id, correct]);

  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--background)] p-3">
      <div className="flex items-baseline justify-between gap-2">
        <div className="text-sm font-medium text-[var(--foreground)]">
          {index + 1}. {question.question || "(missing)"}
        </div>
        {question.difficulty && (
          <span className="rounded-full bg-[var(--muted)] px-2 py-0.5 text-[10px] uppercase tracking-wider text-[var(--muted-foreground)]">
            {question.difficulty}
          </span>
        )}
      </div>

      {isMultiple && Object.keys(options).length > 0 ? (
        <div className="mt-3 space-y-1.5">
          {Object.entries(options).map(([key, label]) => {
            const isSelected = selected === key;
            const isCorrect = revealed && key === correct;
            const isWrongPick = revealed && isSelected && key !== correct;
            return (
              <button
                key={key}
                onClick={() => setSelected(key)}
                className={`flex w-full items-start gap-2 rounded-lg border px-3 py-2 text-left text-sm transition-colors ${
                  isCorrect
                    ? "border-emerald-300 bg-emerald-50 text-emerald-900 dark:border-emerald-500/40 dark:bg-emerald-500/10 dark:text-emerald-100"
                    : isWrongPick
                      ? "border-rose-300 bg-rose-50 text-rose-900 dark:border-rose-500/40 dark:bg-rose-500/10 dark:text-rose-100"
                      : isSelected
                        ? "border-[var(--primary)] bg-[var(--primary)]/8 text-[var(--foreground)]"
                        : "border-[var(--border)] bg-[var(--card)] text-[var(--foreground)] hover:border-[var(--primary)]/40"
                }`}
              >
                <span className="font-mono text-xs uppercase text-[var(--muted-foreground)]">
                  {key}.
                </span>
                <span className="flex-1">{label}</span>
                {isCorrect && <CheckCircle2 className="mt-0.5 h-4 w-4" />}
                {isWrongPick && <XCircle className="mt-0.5 h-4 w-4" />}
              </button>
            );
          })}
        </div>
      ) : (
        <div className="mt-2 text-xs text-[var(--muted-foreground)]">
          {question.question_type === "fill_in_blank"
            ? "Think about your answer, then reveal the solution."
            : "Open response — click reveal to see the model answer."}
        </div>
      )}

      <div className="mt-3 flex items-center justify-between gap-2">
        <button
          onClick={() => setRevealed((v) => !v)}
          className="inline-flex items-center gap-1.5 rounded-md border border-[var(--border)] bg-[var(--card)] px-2.5 py-1 text-xs font-medium text-[var(--muted-foreground)] hover:border-[var(--primary)]/40 hover:text-[var(--primary)]"
        >
          {revealed ? (
            <EyeOff className="h-3.5 w-3.5" />
          ) : (
            <Eye className="h-3.5 w-3.5" />
          )}
          {revealed ? "Hide answer" : "Reveal answer"}
        </button>
        {revealed && correct && (
          <span className="text-xs text-[var(--muted-foreground)]">
            Answer: <span className="font-mono text-[var(--foreground)]">{correct}</span>
          </span>
        )}
      </div>

      {revealed && question.explanation && (
        <div className="mt-2 rounded-lg border border-[var(--border)] bg-[var(--muted)]/40 p-2">
          <MarkdownRenderer
            content={String(question.explanation)}
            variant="compact"
          />
        </div>
      )}
    </div>
  );
}
