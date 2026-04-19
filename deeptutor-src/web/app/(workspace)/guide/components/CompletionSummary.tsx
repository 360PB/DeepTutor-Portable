"use client";

import { CheckCircle2 } from "lucide-react";
import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import "katex/dist/katex.min.css";
import { useTranslation } from "react-i18next";

interface CompletionSummaryProps {
  summary: string;
}

export default function CompletionSummary({ summary }: CompletionSummaryProps) {
  const { t } = useTranslation();

  return (
    <div className="surface-card relative flex flex-1 flex-col overflow-hidden border border-[var(--border)] bg-[var(--card)] text-[var(--card-foreground)]">
      <div className="flex shrink-0 items-center justify-between border-b border-[var(--border)] bg-gradient-to-r from-emerald-500/10 to-[var(--primary)]/10 p-4">
        <h2 className="flex items-center gap-2 font-semibold text-[var(--foreground)]">
          <CheckCircle2 className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
          {t("Learning Summary")}
        </h2>
      </div>
      <div className="flex-1 overflow-y-auto bg-[var(--card)] p-8">
        <MarkdownRenderer content={summary || ""} variant="prose" />
      </div>
    </div>
  );
}
