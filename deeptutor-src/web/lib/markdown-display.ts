"use client";

const ZERO_WIDTH_REGEX = /[\u200B-\u200D\uFEFF]/g;
const EMPTY_DETAILS_REGEX =
  /<details(?:\s[^>]*)?>\s*(<summary(?:\s[^>]*)?>\s*(?:&nbsp;|\s|<br\s*\/?>)*\s*<\/summary>\s*)?<\/details>/gi;
const EMPTY_SUMMARY_REGEX =
  /<summary(?:\s[^>]*)?>\s*(?:&nbsp;|\s|<br\s*\/?>)*\s*<\/summary>/gi;
const EMPTY_PROGRESS_REGEX =
  /<progress(?:\s[^>]*)?>\s*(?:&nbsp;|\s|<br\s*\/?>)*\s*<\/progress>/gi;
const RAW_INPUT_REGEX = /<input(?:\s[^>]*)?>/gi;
const EMPTY_FORM_CONTROL_REGEX =
  /<(textarea|select|button|meter)(?:\s[^>]*)?>\s*(?:&nbsp;|\s|<br\s*\/?>)*\s*<\/\1>/gi;
const EMPTY_FENCED_CODE_BLOCK_REGEX = /```[^\n`]*\n?\s*```/g;
const EMPTY_HTML_BLOCK_REGEX =
  /<(p|div|section|article|aside|blockquote)(?:\s[^>]*)?>\s*(?:&nbsp;|\s|<br\s*\/?>)*\s*<\/\1>/gi;
const HTML_TABLE_REGEX = /<table(?:\s[^>]*)?>[\s\S]*?<\/table>/gi;

function stripInvisibleCharacters(value: string): string {
  return value.replace(ZERO_WIDTH_REGEX, "");
}

function stripDisplaySyntax(value: string): string {
  return stripInvisibleCharacters(String(value))
    .replace(/&nbsp;/gi, " ")
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/<[^>]+>/g, "")
    .replace(/!\[(.*?)\]\([^)]+\)/g, "$1")
    .replace(/\[(.*?)\]\([^)]+\)/g, "$1")
    .replace(/[`*_~]/g, "")
    .trim();
}

function splitMarkdownTableCells(line: string): string[] {
  const trimmed = line.trim().replace(/^\|/, "").replace(/\|$/, "");
  if (!trimmed) return [""];
  return trimmed.split("|");
}

function isMarkdownTableSeparator(line: string): boolean {
  const trimmed = line.trim();
  if (!trimmed.includes("|")) return false;
  const cells = splitMarkdownTableCells(trimmed);
  return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell.trim()));
}

function isMarkdownTableStart(lines: string[], index: number): boolean {
  if (index + 1 >= lines.length) return false;

  const header = lines[index]?.trim() || "";
  const separator = lines[index + 1]?.trim() || "";
  if (!header || !separator || !header.includes("|") || !isMarkdownTableSeparator(separator)) {
    return false;
  }

  return splitMarkdownTableCells(header).length === splitMarkdownTableCells(separator).length;
}

function isMarkdownTableBodyRow(line: string, columnCount: number): boolean {
  const trimmed = line.trim();
  if (!trimmed || !trimmed.includes("|")) return false;
  return splitMarkdownTableCells(trimmed).length === columnCount;
}

function isEmptyMarkdownTable(lines: string[]): boolean {
  return lines
    .filter((_, index) => index !== 1)
    .every((line) => splitMarkdownTableCells(line).every((cell) => stripDisplaySyntax(cell).length === 0));
}

function removeEmptyMarkdownTables(content: string): string {
  const lines = content.split("\n");
  const cleaned: string[] = [];

  for (let index = 0; index < lines.length;) {
    if (!isMarkdownTableStart(lines, index)) {
      cleaned.push(lines[index]);
      index += 1;
      continue;
    }

    const columnCount = splitMarkdownTableCells(lines[index]).length;
    let end = index + 2;
    while (end < lines.length && isMarkdownTableBodyRow(lines[end], columnCount)) {
      end += 1;
    }

    const tableLines = lines.slice(index, end);
    if (!isEmptyMarkdownTable(tableLines)) {
      cleaned.push(...tableLines);
    }
    index = end;
  }

  return cleaned.join("\n");
}

function removeEmptyHtmlTables(content: string): string {
  return content.replace(HTML_TABLE_REGEX, (block) => (stripDisplaySyntax(block) ? block : ""));
}

const PREFIXED_CIT = String.raw`(?:web|rag|code|src)-\d+`;
const NUMERIC_CIT = String.raw`\d+`;
const SINGLE_CIT = `(?:${PREFIXED_CIT}|${NUMERIC_CIT})`;
const MULTI_CIT = `${SINGLE_CIT}(?:\\s*,\\s*${SINGLE_CIT})*`;

const INLINE_CITATION_REGEX = new RegExp(
  String.raw`(?<!\*\*|\[)\[(${MULTI_CIT})\](?!\(|:)`,
  "g",
);

const ESCAPED_CITATION_LINK_REGEX = new RegExp(
  String.raw`\\?\[(${SINGLE_CIT})\\?\]\s*\(#references\s+["` + "\u201c" + String.raw`]citation["` + "\u201d" + String.raw`]\)`,
  "g",
);

function unwrapBacktickedCitations(content: string): string {
  return content.replace(
    new RegExp(
      "`(\\[" + MULTI_CIT + "\\](?:\\s*\\(#references\\s+[\"\\u201c]citation[\"\\u201d]\\))?)`",
      "g",
    ),
    "$1",
  );
}

function linkifyCitations(content: string): string {
  const refSectionIdx = content.search(/^##\s+(References|参考文献)/m);
  const body = refSectionIdx >= 0 ? content.slice(0, refSectionIdx) : content;
  const tail = refSectionIdx >= 0 ? content.slice(refSectionIdx) : "";

  // Normalize existing citation links that may have escaped brackets or smart quotes
  let linked = body.replace(
    ESCAPED_CITATION_LINK_REGEX,
    (_match, id: string) => `[${id.trim()}](#references "citation")`,
  );

  // Convert bare [web-1] / [rag-1] / [1] / [1, 3] references to a single citation link
  linked = linked.replace(INLINE_CITATION_REGEX, (_match, refs: string) => {
    return `[${refs.trim()}](#references "citation")`;
  });

  // Handle escaped bare citations like \[web-1\] or \[1\] that linkifyCitations missed
  linked = linked.replace(
    new RegExp(String.raw`\\\[(${MULTI_CIT})\\\](?!\s*\()`, "g"),
    (_match, refs: string) => {
      return `[${refs.trim()}](#references "citation")`;
    },
  );

  // Remove stray space before trailing punctuation after citations
  linked = linked.replace(
    /(\(#references\s+"citation"\))\s+([.。,，;:!?])/g,
    "$1$2",
  );

  return linked + tail;
}

export function normalizeMarkdownForDisplay(content: string): string {
  if (!content) return "";

  const normalized = stripInvisibleCharacters(String(content))
    .replace(/\r\n/g, "\n")
    .replace(EMPTY_DETAILS_REGEX, "")
    .replace(EMPTY_SUMMARY_REGEX, "")
    .replace(EMPTY_PROGRESS_REGEX, "")
    .replace(RAW_INPUT_REGEX, "")
    .replace(EMPTY_FORM_CONTROL_REGEX, "")
    .replace(EMPTY_HTML_BLOCK_REGEX, "")
    .replace(/\n{3,}/g, "\n\n")
    .replace(/^\n+|\n+$/g, "");

  const cleaned = removeEmptyMarkdownTables(removeEmptyHtmlTables(normalized)).replace(/\n{3,}/g, "\n\n");
  return linkifyCitations(unwrapBacktickedCitations(cleaned));
}

export function hasVisibleMarkdownContent(content: string): boolean {
  const normalized = normalizeMarkdownForDisplay(content);
  if (!normalized.trim()) return false;

  const withoutEmptyBlocks = normalized
    .replace(EMPTY_FENCED_CODE_BLOCK_REGEX, "")
    .replace(/<[^>]+>/g, "")
    .replace(/\[(.*?)\]\([^)]+\)/g, "$1")
    .replace(/!\[(.*?)\]\([^)]+\)/g, "$1")
    .replace(/^[\s>*\-+|#`]+$/gm, "");

  return stripInvisibleCharacters(withoutEmptyBlocks).trim().length > 0;
}
