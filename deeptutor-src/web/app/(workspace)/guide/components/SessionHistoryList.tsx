"use client";

import {
  BookOpen,
  CheckCircle2,
  Clock,
  FileText,
  GraduationCap,
  Loader2,
} from "lucide-react";
import { SessionSummary } from "../types";
import { useTranslation } from "react-i18next";

interface SessionHistoryListProps {
  sessions: SessionSummary[];
  loading: boolean;
  onLoadSession: (sessionId: string) => void;
}

function StatusBadge({ status }: { status: string }) {
  const { t } = useTranslation();
  if (status === "completed") {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/15 px-2 py-0.5 text-[11px] font-semibold text-emerald-700 dark:text-emerald-300">
        <CheckCircle2 className="h-3 w-3" />
        {t("Completed")}
      </span>
    );
  }
  if (status === "learning") {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-[var(--primary)]/12 px-2 py-0.5 text-[11px] font-semibold text-[var(--primary)]">
        <BookOpen className="h-3 w-3" />
        {t("In Progress")}
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-[var(--muted)] px-2 py-0.5 text-[11px] font-semibold text-[var(--muted-foreground)]">
      <FileText className="h-3 w-3" />
      {t("Planned")}
    </span>
  );
}

export default function SessionHistoryList({
  sessions,
  loading,
  onLoadSession,
}: SessionHistoryListProps) {
  const { t } = useTranslation();

  if (loading) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center p-8 text-[var(--muted-foreground)]">
        <Loader2 className="mb-3 h-8 w-8 animate-spin" />
        <p className="text-sm">{t("Loading history...")}</p>
      </div>
    );
  }

  if (sessions.length === 0) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center p-8 text-[var(--muted-foreground)]">
        <GraduationCap className="mb-4 h-20 w-20 text-[var(--muted-foreground)]/40" />
        <h3 className="mb-1 text-base font-medium text-[var(--foreground)]">
          {t("No learning history yet")}
        </h3>
        <p className="max-w-sm text-center text-sm">
          {t(
            "Describe what you want to learn on the left, and your guided learning sessions will appear here.",
          )}
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4">
      <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted-foreground)]">
        {t("Learning History")}
      </h3>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {sessions.map((session) => (
          <button
            key={session.session_id}
            onClick={() => onLoadSession(session.session_id)}
            className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-4 text-left shadow-sm transition-all hover:-translate-y-0.5 hover:border-[var(--primary)]/40 hover:shadow-md"
          >
            <p className="mb-2 line-clamp-2 text-sm font-medium text-[var(--foreground)]">
              {session.topic || t("Untitled")}
            </p>
            <div className="mb-2 flex items-center gap-2">
              <StatusBadge status={session.status} />
              <span className="flex items-center gap-0.5 text-[10px] text-[var(--muted-foreground)]">
                <Clock className="h-3 w-3" />
                {new Date(session.created_at * 1000).toLocaleDateString()}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-[var(--muted)]">
                <div
                  className="h-full rounded-full bg-[var(--primary)] transition-all"
                  style={{ width: `${session.progress}%` }}
                />
              </div>
              <span className="shrink-0 text-[10px] text-[var(--muted-foreground)]">
                {session.ready_count}/{session.total_points}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
