"use client";

import { useState } from "react";
import { Bug, X, Loader2 } from "lucide-react";
import { useTranslation } from "react-i18next";

interface DebugModalProps {
  isOpen: boolean;
  onClose: () => void;
  onFix: (description: string) => Promise<boolean>;
}

export default function DebugModal({
  isOpen,
  onClose,
  onFix,
}: DebugModalProps) {
  const { t } = useTranslation();
  const [description, setDescription] = useState("");
  const [fixing, setFixing] = useState(false);

  if (!isOpen) return null;

  const handleFix = async () => {
    if (!description.trim() || fixing) return;

    setFixing(true);
    const success = await onFix(description);
    setFixing(false);

    if (success) {
      setDescription("");
      onClose();
    }
  };

  const handleClose = () => {
    setDescription("");
    onClose();
  };

  return (
    <div className="fixed inset-0 z-[80] flex items-center justify-center bg-[var(--background)]/65 p-4 backdrop-blur-md">
      <div className="surface-card w-[500px] max-w-full overflow-hidden rounded-2xl border border-[var(--border)] bg-[var(--card)] text-[var(--card-foreground)] shadow-[0_22px_70px_rgba(0,0,0,0.18)]">
        <div className="flex items-center justify-between border-b border-[var(--border)] p-4">
          <h3 className="flex items-center gap-2 font-semibold text-[var(--foreground)]">
            <Bug className="h-5 w-5 text-amber-600 dark:text-amber-400" />
            {t("Fix HTML Issue")}
          </h3>
          <button
            onClick={handleClose}
            className="rounded-lg p-1.5 text-[var(--muted-foreground)] transition-colors hover:bg-[var(--muted)] hover:text-[var(--foreground)]"
            aria-label={t("Close")}
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="space-y-4 p-6">
          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-wider text-[var(--muted-foreground)]">
              {t("Issue Description")}
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={t(
                "Describe the HTML issue, e.g.: button not clickable, style display error, interaction not working...",
              )}
              rows={6}
              className="w-full resize-none rounded-xl border border-[var(--border)] bg-[var(--card)] px-4 py-2 text-[var(--foreground)] outline-none transition placeholder:text-[var(--muted-foreground)] focus:border-amber-500/60 focus:ring-2 focus:ring-amber-500/15"
            />
          </div>
        </div>
        <div className="flex justify-end gap-2 border-t border-[var(--border)] p-4">
          <button
            onClick={handleClose}
            className="rounded-lg px-4 py-2 text-[var(--muted-foreground)] transition-colors hover:bg-[var(--muted)] hover:text-[var(--foreground)]"
          >
            {t("Cancel")}
          </button>
          <button
            onClick={handleFix}
            disabled={!description.trim() || fixing}
            className="flex items-center gap-2 rounded-lg bg-amber-600 px-4 py-2 text-white transition-colors hover:bg-amber-700 disabled:opacity-50 dark:bg-amber-500 dark:hover:bg-amber-400"
          >
            {fixing ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                {t("Fixing...")}
              </>
            ) : (
              <>
                <Bug className="h-4 w-4" />
                {t("Fix")}
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
