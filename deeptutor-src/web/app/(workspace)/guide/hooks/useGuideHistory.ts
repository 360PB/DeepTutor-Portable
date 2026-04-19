import { useState, useCallback, useEffect } from "react";
import { apiUrl } from "@/lib/api";
import { SessionSummary } from "../types";

export function useGuideHistory() {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(apiUrl("/api/v1/guide/sessions"));
      if (!res.ok) {
        setSessions([]);
        return;
      }
      const data = await res.json();
      setSessions(
        Array.isArray(data.sessions) ? (data.sessions as SessionSummary[]) : [],
      );
    } catch {
      setSessions([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchHistory();
  }, [fetchHistory]);

  return { sessions, loading, refresh: fetchHistory };
}
