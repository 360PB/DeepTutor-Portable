import test from "node:test";
import assert from "node:assert/strict";
import {
  hasVisibleMarkdownContent,
  normalizeMarkdownForDisplay,
} from "../lib/markdown-display";

test("normalizeMarkdownForDisplay removes empty details blocks", () => {
  const input = "Before\n\n<details><summary></summary></details>\n\nAfter";
  assert.equal(normalizeMarkdownForDisplay(input), "Before\n\nAfter");
});

test("normalizeMarkdownForDisplay removes raw html control placeholders", () => {
  const input = "Before\n\n<progress></progress>\n<input type=\"text\" />\n<textarea> </textarea>\n\nAfter";
  assert.equal(normalizeMarkdownForDisplay(input), "Before\n\nAfter");
});

test("normalizeMarkdownForDisplay removes empty markdown tables", () => {
  const input = "Before\n\n| |\n|---|\n\nAfter";
  assert.equal(normalizeMarkdownForDisplay(input), "Before\n\nAfter");
});

test("normalizeMarkdownForDisplay removes empty html tables", () => {
  const input = "Before\n\n<table><tr><td>&nbsp;</td></tr></table>\n\nAfter";
  assert.equal(normalizeMarkdownForDisplay(input), "Before\n\nAfter");
});

test("normalizeMarkdownForDisplay keeps meaningful tables", () => {
  const input = "Before\n\n| Topic |\n|---|\n| Math |\n\nAfter";
  assert.equal(normalizeMarkdownForDisplay(input), input);
});

test("hasVisibleMarkdownContent rejects empty raw-html placeholders", () => {
  assert.equal(
    hasVisibleMarkdownContent("<details><summary></summary></details>"),
    false,
  );
});

test("hasVisibleMarkdownContent rejects raw html control placeholders", () => {
  assert.equal(
    hasVisibleMarkdownContent("<progress></progress>\n<input type=\"text\" />"),
    false,
  );
});

test("hasVisibleMarkdownContent rejects empty markdown tables", () => {
  assert.equal(hasVisibleMarkdownContent("| |\n|---|"), false);
});

test("hasVisibleMarkdownContent keeps meaningful markdown", () => {
  assert.equal(
    hasVisibleMarkdownContent("这是一个正常回复。\n\n- 第一条"),
    true,
  );
});
