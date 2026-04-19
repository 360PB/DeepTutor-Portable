"use client";

import { useTranslation } from "react-i18next";

interface AtMentionPopupProps {
  open: boolean;
  onSelectNotebook: () => void;
  onSelectHistory: () => void;
}

export default function AtMentionPopup({
  open,
  onSelectNotebook,
  onSelectHistory,
}: AtMentionPopupProps) {
  const { t } = useTranslation();

  if (!open) return null;

  return (
    <div className="absolute bottom-full left-0 z-[70] mb-2 w-56 rounded-2xl border border-[var(--border)] bg-[var(--card)] p-2 shadow-xl">
      <button
        onClick={onSelectNotebook}
        className="w-full rounded-xl px-3 py-2.5 text-left text-[14px] font-medium text-[var(--foreground)] transition hover:bg-[var(--muted)]/70"
      >
        {t("Notebook")}
      </button>
      <button
        onClick={onSelectHistory}
        className="w-full rounded-xl px-3 py-2.5 text-left text-[14px] font-medium text-[var(--foreground)] transition hover:bg-[var(--muted)]/70"
      >
        {t("Chat History")}
      </button>
    </div>
  );
}
