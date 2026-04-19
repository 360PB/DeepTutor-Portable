"use client";

import { useTranslation } from "react-i18next";
import {
  summarizeMathAnimatorConfig,
  type MathAnimatorFormConfig,
} from "@/lib/math-animator-types";
import {
  CollapsibleConfigSection,
  Field,
  INPUT_CLS,
} from "@/components/chat/home/composer-field";

interface MathAnimatorConfigPanelProps {
  value: MathAnimatorFormConfig;
  onChange: (next: MathAnimatorFormConfig) => void;
  collapsed: boolean;
  onToggleCollapsed: () => void;
}

export default function MathAnimatorConfigPanel({
  value,
  onChange,
  collapsed,
  onToggleCollapsed,
}: MathAnimatorConfigPanelProps) {
  const { t } = useTranslation();
  const update = <K extends keyof MathAnimatorFormConfig>(
    key: K,
    val: MathAnimatorFormConfig[K],
  ) => onChange({ ...value, [key]: val });

  return (
    <CollapsibleConfigSection
      collapsed={collapsed}
      summary={summarizeMathAnimatorConfig(value)}
      onToggleCollapsed={onToggleCollapsed}
      bodyClassName="flex flex-wrap items-end gap-x-3 gap-y-2 px-3.5 pb-2.5"
    >
      <Field label="Output" width="w-[100px]">
        <select
          value={value.output_mode}
          onChange={(e) => update("output_mode", e.target.value as MathAnimatorFormConfig["output_mode"])}
          className={`${INPUT_CLS} w-full`}
        >
          <option value="video">{t("Video")}</option>
          <option value="image">{t("Image")}</option>
        </select>
      </Field>

      <Field label="Quality" width="w-[100px]">
        <select
          value={value.quality}
          onChange={(e) => update("quality", e.target.value as MathAnimatorFormConfig["quality"])}
          className={`${INPUT_CLS} w-full`}
        >
          <option value="low">{t("Low")}</option>
          <option value="medium">{t("Medium")}</option>
          <option value="high">{t("High")}</option>
        </select>
      </Field>

      <Field label="Style Hint" width="min-w-[160px] flex-1">
        <input
          type="text"
          value={value.style_hint}
          onChange={(e) => update("style_hint", e.target.value)}
          placeholder={t("Style, pacing, color...")}
          className={`${INPUT_CLS} w-full`}
        />
      </Field>
    </CollapsibleConfigSection>
  );
}

