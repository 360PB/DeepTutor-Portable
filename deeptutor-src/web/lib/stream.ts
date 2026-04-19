import type { StreamEvent } from "@/lib/unified-ws";

export function shouldAppendEventContent(event: StreamEvent): boolean {
  if (event.type !== "content") return false;
  const metadata = (event.metadata ?? {}) as {
    call_id?: string;
    call_kind?: string;
  };
  if (!metadata.call_id) return true;
  return metadata.call_kind === "llm_final_response";
}
