"use client";

import { useRef, useEffect } from "react";
import {
  AlertCircle,
  CheckCircle2,
  Loader2,
  Play,
  RotateCcw,
  XCircle,
} from "lucide-react";
import { SessionState } from "../types";
import { useTranslation } from "react-i18next";

interface KnowledgeTabBarProps {
  sessionState: SessionState;
  isLoading: boolean;
  canStart: boolean;
  readyCount: number;
  allPagesReady: boolean;
  isCompleted: boolean;
  onStartLearning: () => void;
  onNavigate: (knowledgeIndex: number) => void;
  onRetryPage: (knowledgeIndex: number) => void;
  onCompleteLearning: () => void;
  onResetSession: () => void;
  onShowSummary: () => void;
}

export default function KnowledgeTabBar({
  sessionState,
  isLoading,
  canStart,
  readyCount,
  allPagesReady,
  isCompleted,
  onStartLearning,
  onNavigate,
  onRetryPage,
  onCompleteLearning,
  onResetSession,
  onShowSummary,
}: KnowledgeTabBarProps) {
  const { t } = useTranslation();
  const scrollRef = useRef<HTMLDivElement>(null);
  const activeRef = useRef<HTMLButtonElement>(null);
  const totalCount = sessionState.knowledge_points.length;

  useEffect(() => {
    if (activeRef.current) {
      activeRef.current.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "center",
      });
    }
  }, [sessionState.current_index]);

  const renderStatusIcon = (index: number) => {
    const status = sessionState.page_statuses[index];
    if (status === "ready")
      return <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />;
    if (status === "generating")
      return <Loader2 className="h-3.5 w-3.5 animate-spin text-[var(--primary)]" />;
    if (status === "failed")
      return <XCircle className="h-3.5 w-3.5 text-rose-500" />;
    return <AlertCircle className="h-3.5 w-3.5 text-[var(--muted-foreground)]" />;
  };

  return (
    <div className="flex shrink-0 flex-col rounded-t-2xl border border-b-0 border-[var(--border)] bg-[var(--card)]">
      <div className="flex items-center gap-2 px-3 pb-1 pt-2">
        <div
          ref={scrollRef}
          className="scrollbar-hide flex flex-1 items-center gap-1 overflow-x-auto"
        >
          {sessionState.knowledge_points.map((knowledge, index) => {
            const isCurrent = sessionState.current_index === index;
            const status = sessionState.page_statuses[index] || "pending";
            const isReady = status === "ready";
            const isFailed = status === "failed";

            return (
              <button
                key={`tab-${index}`}
                ref={isCurrent && !isCompleted ? activeRef : null}
                onClick={() => {
                  if (isFailed) {
                    onRetryPage(index);
                  } else {
                    onNavigate(index);
                  }
                }}
                disabled={!isReady && !isFailed}
                title={knowledge.knowledge_title}
                className={`inline-flex shrink-0 items-center gap-1.5 whitespace-nowrap rounded-lg px-2.5 py-1.5 text-xs font-medium transition-colors ${
                  isCurrent && !isCompleted
                    ? "bg-[var(--primary)]/12 text-[var(--primary)]"
                    : isReady
                      ? "bg-[var(--muted)] text-[var(--foreground)] hover:bg-[var(--muted)]/80"
                      : "cursor-default bg-[var(--muted)]/40 text-[var(--muted-foreground)]"
                }`}
              >
                {renderStatusIcon(index)}
                <span>{index + 1}</span>
              </button>
            );
          })}
          {sessionState.status === "completed" && (
            <button
              ref={isCompleted ? activeRef : null}
              onClick={onShowSummary}
              className={`inline-flex shrink-0 items-center gap-1.5 whitespace-nowrap rounded-lg px-2.5 py-1.5 text-xs font-medium transition-colors ${
                isCompleted
                  ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300"
                  : "bg-[var(--muted)] text-[var(--foreground)] hover:bg-[var(--muted)]/80"
              }`}
            >
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
              <span>{t("Summary")}</span>
            </button>
          )}
        </div>

        <div className="flex shrink-0 items-center gap-1.5 border-l border-[var(--border)] pl-2">
          {canStart && (
            <button
              onClick={onStartLearning}
              disabled={isLoading}
              className="btn-primary inline-flex items-center gap-1 rounded-lg bg-[var(--primary)] px-3 py-1.5 text-xs font-medium text-[var(--primary-foreground)] transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {isLoading ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <Play className="h-3.5 w-3.5" />
              )}
              {t("Start")}
            </button>
          )}

          {!canStart && sessionState.status !== "completed" && (
            <button
              onClick={onCompleteLearning}
              disabled={isLoading || !allPagesReady}
              className="inline-flex items-center gap-1 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-emerald-700 disabled:opacity-50 dark:bg-emerald-500 dark:hover:bg-emerald-400"
            >
              {isLoading ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <CheckCircle2 className="h-3.5 w-3.5" />
              )}
              {t("Complete")}
            </button>
          )}

          <button
            onClick={onResetSession}
            className="inline-flex items-center gap-1 rounded-lg bg-[var(--muted)] px-2.5 py-1.5 text-xs font-medium text-[var(--foreground)] transition-colors hover:bg-[var(--muted)]/70"
            title={t("Reset session")}
          >
            <RotateCcw className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      <div className="mx-3 mb-1 h-1 overflow-hidden rounded-full bg-[var(--muted)]">
        <div
          className="h-full rounded-full bg-[var(--primary)] transition-all duration-500"
          style={{
            width: `${totalCount > 0 ? (readyCount / totalCount) * 100 : 0}%`,
          }}
        />
      </div>
    </div>
  );
}
