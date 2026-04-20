export type MathAnimatorOutputMode = "video" | "image";
export type MathAnimatorQuality = "low" | "medium" | "high";

export interface MathAnimatorFormConfig {
  output_mode: MathAnimatorOutputMode;
  quality: MathAnimatorQuality;
  style_hint: string;
}

export const DEFAULT_MATH_ANIMATOR_CONFIG: MathAnimatorFormConfig = {
  output_mode: "video",
  quality: "medium",
  style_hint: "",
};

export interface MathAnimatorArtifact {
  type: "video" | "image";
  url: string;
  filename: string;
  content_type?: string;
  label?: string;
}

export interface MathAnimatorResult {
  response: string;
  output_mode: MathAnimatorOutputMode;
  code: {
    language: string;
    content: string;
  };
  artifacts: MathAnimatorArtifact[];
  timings: Record<string, number>;
  render: {
    quality?: string;
    retry_attempts?: number;
    retry_history?: Array<{ attempt: number; error: string }>;
    source_code_path?: string;
    visual_review?: {
      passed?: boolean;
      summary?: string;
      issues?: string[];
      suggested_fix?: string;
      reviewed_frames?: number;
    } | null;
  };
  summary?: {
    summary_text?: string;
    user_request?: string;
    generated_output?: string;
    key_points?: string[];
  };
}

export function buildMathAnimatorWSConfig(
  cfg: MathAnimatorFormConfig,
): Record<string, unknown> {
  return {
    output_mode: cfg.output_mode,
    quality: cfg.quality,
    style_hint: cfg.style_hint.trim(),
  };
}

function titleCase(value: string): string {
  if (!value) return "";
  return value.charAt(0).toUpperCase() + value.slice(1);
}

/**
 * One-line summary of the math-animator form, shown next to the collapsed
 * `Settings` chevron in the composer. Pass `translate` (typically `t` from
 * `react-i18next`) so the summary follows the active UI language.
 */
export function summarizeMathAnimatorConfig(
  cfg: MathAnimatorFormConfig,
  translate?: (key: string) => string,
): string {
  const output = titleCase(cfg.output_mode);
  const quality = titleCase(cfg.quality);
  return [translate ? translate(output) : output, translate ? translate(quality) : quality].join(" · ");
}

export function extractMathAnimatorResult(
  resultMetadata: Record<string, unknown> | undefined,
): MathAnimatorResult | null {
  if (!resultMetadata) return null;
  const artifacts = Array.isArray(resultMetadata.artifacts)
    ? resultMetadata.artifacts.filter((item): item is MathAnimatorArtifact => {
        return Boolean(
          item &&
            typeof item === "object" &&
            "type" in item &&
            "url" in item &&
            "filename" in item,
        );
      })
    : [];
  const codeRaw =
    resultMetadata.code && typeof resultMetadata.code === "object"
      ? (resultMetadata.code as Record<string, unknown>)
      : {};
  const hasOutputMode =
    resultMetadata.output_mode === "image" || resultMetadata.output_mode === "video";
  const timings =
    resultMetadata.timings && typeof resultMetadata.timings === "object"
      ? (resultMetadata.timings as Record<string, number>)
      : {};
  const render =
    resultMetadata.render && typeof resultMetadata.render === "object"
      ? (resultMetadata.render as MathAnimatorResult["render"])
      : {};
  const outputMode = resultMetadata.output_mode === "image" ? "image" : "video";

  // A plain `response` field is common across capabilities. Only treat the
  // payload as a math-animator result when it carries math-animator-specific
  // artifacts or render metadata.
  if (
    !artifacts.length &&
    !codeRaw.content &&
    !hasOutputMode &&
    Object.keys(timings).length === 0 &&
    Object.keys(render).length === 0
  ) {
    return null;
  }

  return {
    response: String(resultMetadata.response ?? ""),
    output_mode: outputMode,
    code: {
      language: String(codeRaw.language ?? "python"),
      content: String(codeRaw.content ?? ""),
    },
    artifacts,
    timings,
    render,
    summary:
      resultMetadata.summary && typeof resultMetadata.summary === "object"
        ? (resultMetadata.summary as MathAnimatorResult["summary"])
        : undefined,
  };
}
