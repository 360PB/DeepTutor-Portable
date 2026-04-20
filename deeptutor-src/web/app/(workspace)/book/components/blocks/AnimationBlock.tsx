"use client";

import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import type { Block } from "@/lib/book-types";

export interface AnimationBlockProps {
  block: Block;
}

interface Artifact {
  type?: string;
  url?: string;
  filename?: string;
  content_type?: string;
  label?: string;
}

export default function AnimationBlock({ block }: AnimationBlockProps) {
  const payload = (block.payload || {}) as Record<string, unknown>;
  const videoUrl = String(payload.video_url || "");
  const summary = String(payload.summary || "");
  const description = String(payload.description || "");
  const artifacts = (payload.artifacts as Artifact[] | undefined) || [];

  if (!videoUrl && artifacts.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-[var(--border)] bg-[var(--card)]/40 p-4 text-xs italic text-[var(--muted-foreground)]">
        (Animation payload is empty)
      </div>
    );
  }

  const primary = videoUrl || artifacts[0]?.url || "";
  const isVideo =
    primary.endsWith(".mp4") ||
    primary.endsWith(".webm") ||
    artifacts.some((a) => (a.content_type || "").startsWith("video/"));

  return (
    <figure className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-3 shadow-sm">
      <div className="overflow-hidden rounded-xl bg-black">
        {isVideo ? (
          <video
            src={primary}
            controls
            className="h-auto w-full"
            preload="metadata"
          />
        ) : (
          <img src={primary} alt={description || "Animation frame"} className="h-auto w-full" />
        )}
      </div>
      {(summary || description) && (
        <figcaption className="mt-3 text-xs leading-snug text-[var(--muted-foreground)]">
          <MarkdownRenderer content={summary || description} variant="default" />
        </figcaption>
      )}
    </figure>
  );
}
