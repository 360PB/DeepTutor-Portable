export type VisualizeRenderType = "svg" | "chartjs" | "mermaid" | "html";
export type VisualizeRenderMode =
  | "auto"
  | "svg"
  | "chartjs"
  | "mermaid"
  | "html";

export interface VisualizeFormConfig {
  render_mode: VisualizeRenderMode;
}

export const DEFAULT_VISUALIZE_CONFIG: VisualizeFormConfig = {
  render_mode: "auto",
};

export function buildVisualizeWSConfig(
  cfg: VisualizeFormConfig,
): Record<string, unknown> {
  return { render_mode: cfg.render_mode };
}

const VISUALIZE_RENDER_LABELS: Record<VisualizeRenderMode, string> = {
  auto: "Auto",
  chartjs: "Chart.js",
  svg: "SVG",
  mermaid: "Mermaid",
  html: "HTML",
};

/**
 * One-line summary of the visualize form, shown next to the collapsed
 * `Settings` chevron in the composer. Pass `translate` (typically the
 * `t` function from `react-i18next`) so the summary follows the active
 * UI language.
 */
export function summarizeVisualizeConfig(
  cfg: VisualizeFormConfig,
  translate?: (key: string) => string,
): string {
  const label = VISUALIZE_RENDER_LABELS[cfg.render_mode] ?? cfg.render_mode;
  return translate ? translate(label) : label;
}

export interface VisualizeResult {
  response: string;
  render_type: VisualizeRenderType;
  code: {
    language: string;
    content: string;
  };
  analysis: {
    render_type: string;
    description: string;
    data_description: string;
    chart_type: string;
    visual_elements: string[];
    rationale: string;
  };
  review: {
    optimized_code: string;
    changed: boolean;
    review_notes: string;
  };
}

export function extractVisualizeResult(
  resultMetadata: Record<string, unknown> | undefined,
): VisualizeResult | null {
  if (!resultMetadata) return null;

  const renderType = resultMetadata.render_type;
  if (
    renderType !== "svg" &&
    renderType !== "chartjs" &&
    renderType !== "mermaid" &&
    renderType !== "html"
  )
    return null;

  const codeRaw =
    resultMetadata.code && typeof resultMetadata.code === "object"
      ? (resultMetadata.code as Record<string, unknown>)
      : {};

  if (!codeRaw.content) return null;

  return {
    response: String(resultMetadata.response ?? ""),
    render_type: renderType,
    code: {
      language: String(codeRaw.language ?? ""),
      content: String(codeRaw.content ?? ""),
    },
    analysis:
      resultMetadata.analysis && typeof resultMetadata.analysis === "object"
        ? (resultMetadata.analysis as VisualizeResult["analysis"])
        : {
            render_type: renderType,
            description: "",
            data_description: "",
            chart_type: "",
            visual_elements: [],
            rationale: "",
          },
    review:
      resultMetadata.review && typeof resultMetadata.review === "object"
        ? (resultMetadata.review as VisualizeResult["review"])
        : { optimized_code: "", changed: false, review_notes: "" },
  };
}
