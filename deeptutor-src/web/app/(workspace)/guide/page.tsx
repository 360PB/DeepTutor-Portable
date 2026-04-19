"use client";

import { useEffect, useMemo, useState } from "react";
import {
  BookOpen,
  ChevronRight,
  ChevronLeft,
  ArrowRight,
  Loader2,
  Sparkles,
} from "lucide-react";
import "katex/dist/katex.min.css";

import type { SelectedRecord } from "./types";
import NotebookRecordPicker from "@/components/notebook/NotebookRecordPicker";
import SaveToNotebookModal from "@/components/notebook/SaveToNotebookModal";
import {
  ChatPanel,
  HTMLViewer,
  DebugModal,
  CompletionSummary,
  KnowledgeTabBar,
  SessionSwitcher,
  SessionHistoryList,
} from "./components";
import { useGuideSession, useGuideHistory } from "./hooks";
import { useTranslation } from "react-i18next";

export default function GuidePage() {
  const { t } = useTranslation();

  const {
    sessionState,
    chatMessages,
    isLoading,
    loadingMessage,
    canStart,
    isCompleted,
    readyCount,
    allPagesReady,
    currentPageReady,
    createSession,
    startLearning,
    navigateTo,
    retryPage,
    completeLearning,
    sendMessage,
    fixHtml,
    resetSession,
    loadSession,
  } = useGuideSession();

  const { sessions, loading: historyLoading, refresh: refreshHistory } = useGuideHistory();

  const [showDebugModal, setShowDebugModal] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [sidebarWide, setSidebarWide] = useState(false);
  const [topicInput, setTopicInput] = useState("");
  const [showNotebookPicker, setShowNotebookPicker] = useState(false);
  const [selectedNotebookRecords, setSelectedNotebookRecords] = useState<
    SelectedRecord[]
  >([]);
  const [showSaveModal, setShowSaveModal] = useState(false);

  const [hiddenSummaryBySession, setHiddenSummaryBySession] = useState<
    Record<string, boolean>
  >({});

  const leftWidthPercent = sidebarCollapsed ? 0 : sidebarWide ? 75 : 25;
  const rightWidthPercent = sidebarCollapsed ? 100 : sidebarWide ? 25 : 75;
  const isIdle = sessionState.status === "idle";
  const currentSessionKey = sessionState.session_id || "__guide__";
  const showingSummary =
    sessionState.status === "completed" &&
    Boolean(sessionState.summary) &&
    !hiddenSummaryBySession[currentSessionKey];
  const notebookReferenceGroups = useMemo(() => {
    const groups = new Map<string, { notebookName: string; count: number }>();
    selectedNotebookRecords.forEach((record) => {
      const existing = groups.get(record.notebookId);
      if (existing) {
        existing.count += 1;
      } else {
        groups.set(record.notebookId, {
          notebookName: record.notebookName,
          count: 1,
        });
      }
    });
    return Array.from(groups.entries()).map(([notebookId, value]) => ({
      notebookId,
      ...value,
    }));
  }, [selectedNotebookRecords]);
  const notebookReferencesPayload = useMemo(() => {
    const grouped = new Map<string, string[]>();
    selectedNotebookRecords.forEach((record) => {
      const current = grouped.get(record.notebookId) || [];
      current.push(record.id);
      grouped.set(record.notebookId, current);
    });
    return Array.from(grouped.entries()).map(([notebook_id, record_ids]) => ({
      notebook_id,
      record_ids,
    }));
  }, [selectedNotebookRecords]);
  const guideSavePayload = useMemo(() => {
    if (sessionState.status === "idle" || !sessionState.session_id) return null;
    return {
      recordType: "guided_learning" as const,
      title: sessionState.topic || "Guided Learning Session",
      userQuery: sessionState.topic || "",
      output: JSON.stringify(
        {
          topic: sessionState.topic,
          status: sessionState.status,
          knowledge_points: sessionState.knowledge_points,
          current_index: sessionState.current_index,
          html_pages: sessionState.html_pages,
          page_statuses: sessionState.page_statuses,
          summary: sessionState.summary,
        },
        null,
        2,
      ),
      metadata: {
        source: "guided_learning",
        progress: sessionState.progress,
        session_id: sessionState.session_id,
      },
    };
  }, [sessionState]);

  const handleCreateSession = () => {
    createSession(topicInput, notebookReferencesPayload);
  };

  const handleResetSession = async () => {
    await resetSession();
    refreshHistory();
  };

  const handleLoadSession = async (sessionId: string) => {
    await loadSession(sessionId);
  };

  const handleFixHtml = async (description: string) => {
    return await fixHtml(description);
  };

  useEffect(() => {
    if (typeof window === "undefined") return;
    const params = new URLSearchParams(window.location.search);
    const session = params.get("session");
    if (session) {
      void loadSession(session);
    }
  }, [loadSession]);

  return (
    <div className="h-screen flex gap-0 p-4 animate-fade-in relative">
      {/* LEFT PANEL */}
      <div
        className={`flex flex-col gap-3 h-full transition-all duration-300 flex-shrink-0 mr-4 ${sidebarCollapsed ? "overflow-hidden" : ""}`}
        style={{
          width: sidebarCollapsed ? 0 : `${leftWidthPercent}%`,
          minWidth: sidebarCollapsed
            ? 0
            : `${Math.max(leftWidthPercent * 0.01 * 1200, 300)}px`,
          maxWidth: sidebarCollapsed ? 0 : `${leftWidthPercent}%`,
        }}
      >
        {isIdle ? (
          <div className="surface-card flex flex-col overflow-hidden border border-[var(--border)] bg-[var(--card)] text-[var(--card-foreground)]">
            <div className="border-b border-[var(--border)] bg-[var(--muted)]/35 p-3">
              <h2 className="flex items-center gap-2 font-semibold text-[var(--foreground)]">
                <Sparkles className="h-5 w-5 text-[var(--primary)]" />
                {t("Describe what you want to learn")}
              </h2>
              <p className="mt-2 text-sm text-[var(--muted-foreground)]">
                {t(
                  "Write a short learning request, and the system will design a progressive guided learning plan for you.",
                )}
              </p>
            </div>

            <div className="space-y-4 p-4">
              <textarea
                value={topicInput}
                onChange={(e) => setTopicInput(e.target.value)}
                placeholder={t(
                  "For example: Teach me linear algebra from the basics, with intuition, key formulas, and common mistakes.",
                )}
                rows={8}
                className="w-full resize-none rounded-xl border border-[var(--border)] bg-[var(--card)] px-4 py-3 text-sm text-[var(--foreground)] outline-none transition placeholder:text-[var(--muted-foreground)] focus:border-[var(--primary)]/50 focus:ring-2 focus:ring-[var(--primary)]/15"
              />

              <div className="rounded-xl border border-[var(--border)] bg-[var(--muted)]/30 p-3.5">
                <div className="flex items-center justify-between gap-2">
                  <div className="inline-flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--primary)]">
                    <BookOpen className="h-3 w-3" />
                    {t("Notebook Context")}
                  </div>
                  <span className="rounded-full bg-[var(--muted)] px-2 py-0.5 text-[9px] font-medium uppercase tracking-wider text-[var(--muted-foreground)]">
                    {t("Optional")}
                  </span>
                </div>
                <p className="mt-1.5 text-xs leading-relaxed text-[var(--muted-foreground)]">
                  {t("Ground the plan with saved notebook records.")}
                </p>
                <button
                  onClick={() => setShowNotebookPicker(true)}
                  className="mt-3 inline-flex w-full items-center justify-center gap-2 whitespace-nowrap rounded-lg border border-dashed border-[var(--border)] bg-[var(--card)] px-3 py-2 text-xs font-medium text-[var(--muted-foreground)] transition-colors hover:border-[var(--primary)]/50 hover:bg-[var(--primary)]/8 hover:text-[var(--primary)]"
                >
                  <BookOpen className="h-3.5 w-3.5" />
                  {selectedNotebookRecords.length > 0
                    ? t("Update selection ({n})", {
                        n: selectedNotebookRecords.length,
                      })
                    : t("Select records")}
                </button>
                {notebookReferenceGroups.length > 0 && (
                  <div className="mt-2.5 flex flex-wrap gap-1.5">
                    {notebookReferenceGroups.map((group) => (
                      <span
                        key={group.notebookId}
                        className="inline-flex max-w-full items-center gap-1.5 truncate rounded-full border border-[var(--border)] bg-[var(--card)] px-2.5 py-0.5 text-[11px] text-[var(--foreground)]"
                        title={`${group.notebookName} (${group.count})`}
                      >
                        <span className="truncate">{group.notebookName}</span>
                        <span className="shrink-0 text-[var(--muted-foreground)]">
                          {group.count}
                        </span>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <button
                onClick={handleCreateSession}
                disabled={isLoading || !topicInput.trim()}
                className="btn-primary inline-flex items-center gap-2 rounded-xl bg-[var(--primary)] px-4 py-2.5 text-sm font-medium text-[var(--primary-foreground)] transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Sparkles className="h-4 w-4" />
                )}
                {t("Generate learning plan")}
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-end">
              <button
                onClick={() => setShowSaveModal(true)}
                className="inline-flex items-center gap-2 rounded-xl border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-sm font-medium text-[var(--foreground)] transition-colors hover:border-[var(--primary)]/40 hover:bg-[var(--primary)]/8 hover:text-[var(--primary)]"
              >
                <BookOpen className="h-4 w-4" />
                {t("Add to Notebook")}
              </button>
            </div>
            <SessionSwitcher
              currentSessionId={sessionState.session_id}
              currentTopic={sessionState.topic}
              currentStatus={sessionState.status}
              sessions={sessions}
              onLoadSession={handleLoadSession}
              onNewSession={handleResetSession}
            />
            <ChatPanel
              messages={chatMessages}
              isLearning={sessionState.status === "learning" && currentPageReady}
              currentKnowledgeTitle={
                sessionState.current_index >= 0
                  ? sessionState.knowledge_points[sessionState.current_index]
                      ?.knowledge_title
                  : undefined
              }
              currentKnowledgeIndex={
                sessionState.current_index >= 0
                  ? sessionState.current_index
                  : undefined
              }
              onSendMessage={sendMessage}
            />
          </>
        )}
      </div>

      {/* RIGHT PANEL */}
      <div
        className="flex flex-col h-full overflow-hidden transition-all duration-300 flex-1 relative"
        style={{ width: `${rightWidthPercent}%` }}
      >
        {/* Collapse/Expand buttons */}
        {isIdle && (
          <div className="absolute top-4 left-4 z-20 flex gap-2">
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-2 text-[var(--muted-foreground)] shadow-sm transition-colors hover:bg-[var(--muted)] hover:text-[var(--foreground)]"
              title={
                sidebarCollapsed ? t("Expand sidebar") : t("Collapse sidebar")
              }
            >
              {sidebarCollapsed ? (
                <ChevronRight className="h-4 w-4" />
              ) : (
                <ChevronLeft className="h-4 w-4" />
              )}
            </button>
            {!sidebarCollapsed && (
              <button
                onClick={() => setSidebarWide(!sidebarWide)}
                className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-2 text-[var(--muted-foreground)] shadow-sm transition-colors hover:bg-[var(--muted)] hover:text-[var(--foreground)]"
                title={
                  sidebarWide
                    ? t("Switch to narrow sidebar (1:3)")
                    : t("Switch to wide sidebar (3:1)")
                }
              >
                <ArrowRight
                  className={`h-4 w-4 transition-transform ${sidebarWide ? "rotate-180" : ""}`}
                />
              </button>
            )}
          </div>
        )}

        {isIdle ? (
          <div className="surface-card flex flex-1 flex-col overflow-hidden border border-[var(--border)] bg-[var(--card)] text-[var(--card-foreground)]">
            <SessionHistoryList
              sessions={sessions}
              loading={historyLoading}
              onLoadSession={handleLoadSession}
            />
          </div>
        ) : (
          <>
            {/* Knowledge tab bar */}
            <KnowledgeTabBar
              sessionState={sessionState}
              isLoading={isLoading}
              canStart={canStart}
              readyCount={readyCount}
              allPagesReady={allPagesReady}
              isCompleted={showingSummary}
              onStartLearning={startLearning}
              onNavigate={(index) => {
                setHiddenSummaryBySession((prev) => ({
                  ...prev,
                  [currentSessionKey]: true,
                }));
                navigateTo(index);
              }}
              onRetryPage={retryPage}
              onCompleteLearning={() => {
                completeLearning();
                setHiddenSummaryBySession((prev) => ({
                  ...prev,
                  [currentSessionKey]: false,
                }));
              }}
              onResetSession={handleResetSession}
              onShowSummary={() =>
                setHiddenSummaryBySession((prev) => ({
                  ...prev,
                  [currentSessionKey]: false,
                }))
              }
            />

            {/* Main content */}
            <div className="flex-1 min-h-0 flex flex-col">
              {showingSummary && sessionState.summary ? (
                <CompletionSummary summary={sessionState.summary} />
              ) : sessionState.status === "learning" || (isCompleted && !showingSummary) ? (
                <HTMLViewer
                  html={
                    sessionState.current_index >= 0
                      ? sessionState.html_pages[sessionState.current_index] ||
                        ""
                      : ""
                  }
                  currentIndex={sessionState.current_index}
                  loadingMessage={
                    sessionState.current_index >= 0 &&
                    sessionState.page_statuses[sessionState.current_index] ===
                      "failed"
                      ? t(
                          "This page failed to generate. You can retry it from the tab bar.",
                        )
                      : loadingMessage ||
                        t("Waiting for the selected interactive page...")
                  }
                  onOpenDebugModal={() => setShowDebugModal(true)}
                />
              ) : (
                <div className="flex h-full flex-col items-center justify-center rounded-b-2xl border border-t-0 border-[var(--border)] bg-[var(--card)] p-8 text-[var(--muted-foreground)]">
                  <Loader2 className="mb-4 h-12 w-12 animate-spin text-[var(--primary)]" />
                  <p>{loadingMessage || t("Loading learning content...")}</p>
                </div>
              )}
            </div>
          </>
        )}
      </div>

      <DebugModal
        isOpen={showDebugModal}
        onClose={() => setShowDebugModal(false)}
        onFix={handleFixHtml}
      />
      <NotebookRecordPicker
        open={showNotebookPicker}
        onClose={() => setShowNotebookPicker(false)}
        onApply={(records) => setSelectedNotebookRecords(records)}
      />
      <SaveToNotebookModal
        open={showSaveModal}
        payload={guideSavePayload}
        onClose={() => setShowSaveModal(false)}
      />
    </div>
  );
}
