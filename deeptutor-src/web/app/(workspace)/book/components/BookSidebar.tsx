"use client";

import { Plus, Library, Loader2, Trash2, Compass } from "lucide-react";
import type { Book, Page } from "@/lib/book-types";

const STATUS_LABEL: Record<string, string> = {
  pending: "Queued",
  planning: "Planning",
  generating: "Compiling",
  ready: "Ready",
  partial: "Partial",
  error: "Failed",
};

export interface BookSidebarProps {
  books: Book[];
  loadingBooks: boolean;
  selectedBookId: string | null;
  onSelectBook: (id: string | null) => void;
  onNewBook: () => void;
  onDeleteBook: (id: string) => void;
  pages?: Page[];
  selectedPageId?: string | null;
  onSelectPage?: (id: string) => void;
}

export default function BookSidebar({
  books,
  loadingBooks,
  selectedBookId,
  onSelectBook,
  onNewBook,
  onDeleteBook,
  pages = [],
  selectedPageId = null,
  onSelectPage,
}: BookSidebarProps) {
  return (
    <aside className="flex h-full w-[232px] flex-col gap-3 border-r border-[var(--border)] bg-[var(--card)]/40 px-3 py-4">
      <button
        onClick={onNewBook}
        className="inline-flex items-center justify-center gap-2 rounded-xl bg-[var(--primary)] px-3 py-2 text-sm font-medium text-[var(--primary-foreground)] hover:opacity-90"
      >
        <Plus className="h-4 w-4" /> New book
      </button>

      <section className="flex-1 overflow-y-auto">
        <div className="mb-2 flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
          <Library className="h-3.5 w-3.5" /> My Books
        </div>
        {loadingBooks ? (
          <div className="flex items-center gap-2 px-2 py-3 text-xs text-[var(--muted-foreground)]">
            <Loader2 className="h-3.5 w-3.5 animate-spin" /> Loading…
          </div>
        ) : books.length === 0 ? (
          <div className="rounded-md border border-dashed border-[var(--border)] px-2 py-3 text-xs text-[var(--muted-foreground)]">
            No books yet. Create one to get started.
          </div>
        ) : (
          <ul className="space-y-1">
            {books.map((book) => {
              const active = book.id === selectedBookId;
              return (
                <li key={book.id}>
                  <div
                    className={`group flex items-start gap-2 rounded-lg px-2 py-2 text-sm ${
                      active
                        ? "bg-[var(--primary)]/10 text-[var(--foreground)]"
                        : "hover:bg-[var(--muted)]/40 text-[var(--foreground)]"
                    }`}
                  >
                    <button
                      onClick={() => onSelectBook(book.id)}
                      className="flex flex-1 flex-col gap-0.5 text-left"
                    >
                      <span className="truncate font-medium">{book.title || "Untitled book"}</span>
                      <span className="text-[10px] uppercase tracking-wider text-[var(--muted-foreground)]">
                        {book.status} · {book.chapter_count || 0} chapters
                      </span>
                    </button>
                    <button
                      onClick={() => onDeleteBook(book.id)}
                      className="invisible rounded-md p-1 text-rose-500 hover:bg-rose-50 group-hover:visible dark:hover:bg-rose-500/10"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </section>

      {selectedBookId && pages.length > 0 && (
        <section>
          <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
            Chapters
          </div>
          <ul className="space-y-1">
            {pages.map((page) => {
              const active = page.id === selectedPageId;
              const isOverview = page.content_type === "overview";
              return (
                <li key={page.id}>
                  <button
                    onClick={() => onSelectPage?.(page.id)}
                    className={`flex w-full items-start justify-between gap-2 rounded-md px-2 py-1.5 text-left text-xs ${
                      active
                        ? "bg-[var(--primary)]/15 text-[var(--foreground)]"
                        : "text-[var(--muted-foreground)] hover:bg-[var(--muted)]/40 hover:text-[var(--foreground)]"
                    } ${
                      isOverview
                        ? "border border-dashed border-[var(--border)]"
                        : ""
                    }`}
                  >
                    <span className="flex min-w-0 items-start gap-1.5">
                      {isOverview && (
                        <Compass className="mt-[1px] h-3 w-3 shrink-0 text-[var(--primary)]" />
                      )}
                      <span className="line-clamp-2">
                        {page.title || "Untitled"}
                      </span>
                    </span>
                    <span className="shrink-0 rounded-full bg-[var(--muted)] px-1.5 py-0.5 text-[9px] uppercase tracking-wider text-[var(--muted-foreground)]">
                      {STATUS_LABEL[page.status] || page.status}
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
        </section>
      )}
    </aside>
  );
}
