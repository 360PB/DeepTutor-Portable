"use client";

import {
  AlertCircle,
  CheckCircle2,
  Loader2,
  Play,
  RotateCcw,
  Sparkles,
  XCircle,
} from "lucide-react";
import { SessionState } from "../types";
import { useTranslation } from "react-i18next";

interface ProgressPanelProps {
  sessionState: SessionState;
  isLoading: boolean;
  canStart: boolean;
  readyCount: number;
  allPagesReady: boolean;
  onStartLearning: () => void;
  onNavigate: (knowledgeIndex: number) => void;
  onRetryPage: (knowledgeIndex: number) => void;
  onCompleteLearning: () => void;
  onResetSession: () => void;
}

export default function ProgressPanel({
  sessionState,
  isLoading,
  canStart,
  readyCount,
  allPagesReady,
  onStartLearning,
  onNavigate,
  onRetryPage,
  onCompleteLearning,
  onResetSession,
}: ProgressPanelProps) {
  const { t } = useTranslation();

  const totalCount = sessionState.knowledge_points.length;

  const renderStatusIcon = (knowledgeIndex: number) => {
    const status = sessionState.page_statuses[knowledgeIndex];

    if (status === "ready") {
      return <CheckCircle2 className="h-4 w-4 text-emerald-500" />;
    }
    if (status === "generating") {
      return <Loader2 className="h-4 w-4 animate-spin text-[var(--primary)]" />;
    }
    if (status === "failed") {
      return <XCircle className="h-4 w-4 text-rose-500" />;
    }
    return <AlertCircle className="h-4 w-4 text-[var(--muted-foreground)]" />;
  };

  return (
    <div className="surface-card border border-[var(--border)] bg-[var(--card)] p-4 text-[var(--card-foreground)]">
      <div className="mb-2 flex items-center justify-between gap-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-[var(--muted-foreground)]">
          {t("Learning Progress")}
        </span>
        <span className="text-xs text-[var(--muted-foreground)]">
          {readyCount}/{totalCount} {t("pages ready")}
        </span>
      </div>
      <div className="mb-4 h-2 overflow-hidden rounded-full bg-[var(--muted)]">
        <div
          className="h-full rounded-full bg-[var(--primary)] transition-all duration-500"
          style={{ width: `${sessionState.progress}%` }}
        />
      </div>
      {totalCount > 0 && (
        <p className="mb-4 text-xs text-[var(--muted-foreground)]">
          {t("Open any page once it is ready. Early stages are prioritized.")}
        </p>
      )}

      <div className="mb-4 space-y-2">
        {sessionState.knowledge_points.map((knowledge, index) => {
          const status = sessionState.page_statuses[index] || "pending";
          const isCurrent = sessionState.current_index === index;
          const isReady = status === "ready";
          const isFailed = status === "failed";

          return (
            <div
              key={`${knowledge.knowledge_title}-${index}`}
              className={`rounded-xl border px-3 py-3 transition-colors ${
                isCurrent
                  ? "border-[var(--primary)]/40 bg-[var(--primary)]/8"
                  : "border-[var(--border)] bg-[var(--muted)]/30"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <button
                  onClick={() => onNavigate(index)}
                  className="flex-1 text-left"
                >
                  <div className="flex items-center gap-2 text-sm font-medium text-[var(--foreground)]">
                    {renderStatusIcon(index)}
                    <span>{index + 1}.</span>
                    <span className="line-clamp-2">{knowledge.knowledge_title}</span>
                  </div>
                  <p className="mt-1 text-xs text-[var(--muted-foreground)]">
                    {status === "ready"
                      ? t("Ready to open")
                      : status === "generating"
                        ? t("Generating interactive page...")
                        : status === "failed"
                          ? t("Generation failed")
                          : t("Waiting in queue")}
                  </p>
                </button>

                {isFailed && (
                  <button
                    onClick={() => onRetryPage(index)}
                    className="inline-flex items-center gap-1 rounded-lg border border-rose-300/50 bg-rose-500/8 px-2 py-1 text-xs text-rose-600 hover:bg-rose-500/15 dark:text-rose-300"
                  >
                    <RotateCcw className="h-3 w-3" />
                    {t("Retry")}
                  </button>
                )}
                {isReady && (
                  <button
                    onClick={() => onNavigate(index)}
                    className="inline-flex items-center gap-1 rounded-lg border border-emerald-300/50 bg-emerald-500/8 px-2 py-1 text-xs text-emerald-600 hover:bg-emerald-500/15 dark:text-emerald-300"
                  >
                    <Sparkles className="h-3 w-3" />
                    {t("Open")}
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="flex flex-wrap gap-2">
        {canStart && (
          <button
            onClick={onStartLearning}
            disabled={isLoading}
            className="btn-primary flex flex-1 items-center justify-center gap-2 rounded-lg bg-[var(--primary)] px-4 py-2 text-sm font-medium text-[var(--primary-foreground)] transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                {t("Starting...")}
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                {t("Start Learning")}
              </>
            )}
          </button>
        )}

        {!canStart && (
          <button
            onClick={onResetSession}
            className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-[var(--muted)] px-4 py-2 text-sm font-medium text-[var(--foreground)] transition-colors hover:bg-[var(--muted)]/70"
          >
            <RotateCcw className="h-4 w-4" />
            {t("New Session")}
          </button>
        )}

        {!canStart && sessionState.status !== "completed" && (
          <button
            onClick={onCompleteLearning}
            disabled={isLoading || !allPagesReady}
            className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-emerald-500 dark:hover:bg-emerald-400"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                {t("Generating Summary...")}
              </>
            ) : (
              <>
                <CheckCircle2 className="h-4 w-4" />
                {t("Complete Learning")}
              </>
            )}
          </button>
        )}
      </div>
    </div>
  );
}
