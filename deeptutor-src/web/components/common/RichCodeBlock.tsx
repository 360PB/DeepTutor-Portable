"use client";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

const MONOSPACE =
  'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace';

const PLAIN_LANGS = new Set(["", "text", "txt", "plain", "plaintext", "none"]);

export default function RichCodeBlock({
  raw,
  lang,
  className,
}: {
  raw: string;
  lang: string;
  className?: string;
}) {
  const normalizedLang = (lang || "").toLowerCase();
  const isPlain = PLAIN_LANGS.has(normalizedLang);

  return (
    <div
      className={`md-code-block overflow-hidden rounded-xl border border-[var(--border)] bg-[#1f2937] ${
        className || ""
      }`}
    >
      {!isPlain ? (
        <div className="border-b border-white/10 px-3 py-2 text-[11px] font-medium uppercase tracking-wider text-[#9ca3af]">
          {normalizedLang}
        </div>
      ) : null}
      {isPlain ? (
        // Skip the highlighter entirely for unlabeled / plain blocks so we
        // don't trigger Prism "unknown language" warnings and keep a tidy
        // monospace presentation that matches the highlighted variant.
        <pre
          className="overflow-x-auto p-4 text-sm leading-[1.7] text-[#e5e7eb]"
          style={{ margin: 0, fontFamily: MONOSPACE }}
        >
          <code className="md-code-block__code" style={{ fontFamily: MONOSPACE }}>
            {raw}
          </code>
        </pre>
      ) : (
        <SyntaxHighlighter
          language={normalizedLang}
          style={oneDark}
          PreTag="pre"
          customStyle={{
            margin: 0,
            borderRadius: 0,
            background: "#1f2937",
            padding: "1rem",
            fontSize: "0.875rem",
            lineHeight: "1.7",
          }}
          codeTagProps={{
            className: "md-code-block__code",
            style: { fontFamily: MONOSPACE },
          }}
          wrapLongLines={false}
        >
          {raw}
        </SyntaxHighlighter>
      )}
    </div>
  );
}
