"use client";

import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import { hasVisibleMarkdownContent } from "@/lib/markdown-display";

interface AssistantResponseProps {
  content: string;
  className?: string;
}

export default function AssistantResponse({
  content,
  className = "text-[14px] leading-[1.75]",
}: AssistantResponseProps) {
  if (!hasVisibleMarkdownContent(content)) return null;

  return (
    <div className={className}>
      <MarkdownRenderer
        content={content}
        variant="prose"
        className="text-[var(--foreground)]"
      />
    </div>
  );
}
