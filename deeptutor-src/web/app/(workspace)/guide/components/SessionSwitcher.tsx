"use client";

import { useState, useRef, useEffect } from "react";
import {
  ChevronDown,
  Plus,
  Clock,
  CheckCircle2,
  BookOpen,
  FileText,
} from "lucide-react";
import { SessionSummary } from "../types";
import { useTranslation } from "react-i18next";

interface SessionSwitcherProps {
  currentSessionId: string | null;
  currentTopic: string;
  currentStatus: string;
  sessions: SessionSummary[];
  onLoadSession: (sessionId: string) => void;
  onNewSession: () => void;
}

function StatusBadge({ status }: { status: string }) {
  const { t } = useTranslation();
  if (status === "completed") {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] font-semibold text-emerald-700 dark:text-emerald-300">
        <CheckCircle2 className="h-3 w-3" />
        {t("Completed")}
      </span>
    );
  }
  if (status === "learning") {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-[var(--primary)]/12 px-2 py-0.5 text-[10px] font-semibold text-[var(--primary)]">
        <BookOpen className="h-3 w-3" />
        {t("In Progress")}
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-[var(--muted)] px-2 py-0.5 text-[10px] font-semibold text-[var(--muted-foreground)]">
      <FileText className="h-3 w-3" />
      {t("Planned")}
    </span>
  );
}

export default function SessionSwitcher({
  currentSessionId,
  currentTopic,
  currentStatus,
  sessions,
  onLoadSession,
  onNewSession,
}: SessionSwitcherProps) {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const otherSessions = sessions.filter(
    (s) => s.session_id !== currentSessionId,
  );

  return (
    <div ref={containerRef} className="relative shrink-0">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-2 rounded-xl border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-left transition-colors hover:bg-[var(--muted)]/40"
      >
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-[var(--foreground)]">
            {currentTopic || t("Untitled Session")}
          </p>
          <StatusBadge status={currentStatus} />
        </div>
        <ChevronDown
          className={`h-4 w-4 shrink-0 text-[var(--muted-foreground)] transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      {open && (
        <div className="absolute left-0 right-0 top-full z-30 mt-1 max-h-64 overflow-y-auto rounded-xl border border-[var(--border)] bg-[var(--popover)] text-[var(--popover-foreground)] shadow-lg">
          {otherSessions.length > 0 && (
            <div className="py-1">
              {otherSessions.map((session) => (
                <button
                  key={session.session_id}
                  onClick={() => {
                    onLoadSession(session.session_id);
                    setOpen(false);
                  }}
                  className="flex w-full items-center gap-2 px-3 py-2 text-left transition-colors hover:bg-[var(--muted)]/60"
                >
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-xs font-medium text-[var(--foreground)]">
                      {session.topic || t("Untitled")}
                    </p>
                    <div className="mt-0.5 flex items-center gap-2">
                      <StatusBadge status={session.status} />
                      <span className="flex items-center gap-0.5 text-[10px] text-[var(--muted-foreground)]">
                        <Clock className="h-3 w-3" />
                        {new Date(session.created_at * 1000).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}
          <div className="border-t border-[var(--border)] p-2">
            <button
              onClick={() => {
                onNewSession();
                setOpen(false);
              }}
              className="flex w-full items-center justify-center gap-1.5 rounded-lg bg-[var(--primary)]/10 px-3 py-2 text-xs font-medium text-[var(--primary)] transition-colors hover:bg-[var(--primary)]/18"
            >
              <Plus className="h-3.5 w-3.5" />
              {t("New Session")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
