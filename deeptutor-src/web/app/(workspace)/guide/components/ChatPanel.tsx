"use client";

import { useRef, useEffect, useState } from "react";
import { MessageSquare, Send, Loader2 } from "lucide-react";
import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import "katex/dist/katex.min.css";
import { useTranslation } from "react-i18next";
import { ChatMessage } from "../types";

interface ChatPanelProps {
  messages: ChatMessage[];
  isLearning: boolean;
  currentKnowledgeTitle?: string;
  currentKnowledgeIndex?: number;
  onSendMessage: (message: string) => void;
}

export default function ChatPanel({
  messages,
  isLearning,
  currentKnowledgeTitle,
  currentKnowledgeIndex,
  onSendMessage,
}: ChatPanelProps) {
  const { t } = useTranslation();
  const [inputMessage, setInputMessage] = useState("");
  const [sendingMessage, setSendingMessage] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || sendingMessage) return;

    setSendingMessage(true);
    const message = inputMessage;
    setInputMessage("");

    try {
      await onSendMessage(message);
    } finally {
      setSendingMessage(false);
    }
  };

  return (
    <div className="surface-card flex flex-1 flex-col overflow-hidden border border-[var(--border)] bg-[var(--card)] text-[var(--card-foreground)]">
      <div className="flex items-center gap-2 border-b border-[var(--border)] bg-[var(--muted)]/35 p-3 text-xs font-bold uppercase tracking-wider text-[var(--muted-foreground)]">
        <MessageSquare className="h-4 w-4" />
        {t("Learning Assistant")}
      </div>

      {isLearning && currentKnowledgeTitle && (
        <div className="border-b border-[var(--border)] bg-[var(--primary)]/8 px-4 py-2 text-xs text-[var(--primary)]">
          {t("Current page")}: {currentKnowledgeIndex !== undefined ? currentKnowledgeIndex + 1 : ""}
          {currentKnowledgeIndex !== undefined ? ". " : ""}
          {currentKnowledgeTitle}
        </div>
      )}

      <div
        ref={chatContainerRef}
        className="flex-1 space-y-4 overflow-y-auto bg-[var(--background)]/30 p-4"
      >
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
          >
            <div
              className={`max-w-[90%] rounded-2xl px-4 py-3 text-sm ${
                msg.role === "user"
                  ? "rounded-tr-none bg-[var(--primary)] text-[var(--primary-foreground)] shadow-sm"
                  : msg.role === "system" && msg.content.includes("⏳")
                    ? "rounded-tl-none border border-amber-300/50 bg-amber-500/10 text-amber-900 dark:text-amber-200"
                    : msg.role === "system"
                      ? "rounded-tl-none border border-sky-300/50 bg-sky-500/10 text-sky-900 dark:text-sky-200"
                      : "rounded-tl-none border border-[var(--border)] bg-[var(--card)] text-[var(--foreground)] shadow-sm"
              }`}
            >
              {typeof msg.knowledge_index === "number" && (
                <div className="mb-2 text-[11px] font-semibold opacity-70">
                  {t("Knowledge Point")} {msg.knowledge_index + 1}
                </div>
              )}
              {msg.role === "system" || msg.role === "assistant" ? (
                <MarkdownRenderer
                  content={msg.content}
                  variant="compact"
                  className="text-sm"
                />
              ) : (
                <p>{msg.content}</p>
              )}
            </div>
          </div>
        ))}
      </div>

      {isLearning && (
        <div className="border-t border-[var(--border)] bg-[var(--card)] p-3">
          <div className="relative flex items-center gap-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) =>
                e.key === "Enter" && !e.shiftKey && handleSendMessage()
              }
              placeholder={t("Have any questions? Feel free to ask...")}
              disabled={sendingMessage}
              className="flex-1 rounded-xl border border-transparent bg-[var(--muted)]/60 py-2.5 pl-4 pr-10 text-sm text-[var(--foreground)] outline-none transition placeholder:text-[var(--muted-foreground)] focus:border-[var(--primary)]/50 focus:bg-[var(--card)] focus:ring-2 focus:ring-[var(--primary)]/15 disabled:cursor-not-allowed disabled:opacity-50"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || sendingMessage}
              className="btn-primary rounded-xl bg-[var(--primary)] p-2.5 text-[var(--primary-foreground)] transition-opacity hover:opacity-90 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {sendingMessage ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
