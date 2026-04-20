/**
 * Shared types for Quiz Generation (deep_question capability).
 */

export type DeepQuestionMode = "custom" | "mimic";

export interface DeepQuestionFormConfig {
  mode: DeepQuestionMode;
  topic: string;
  num_questions: number;
  difficulty: string;
  question_type: string;
  preference: string;
  paper_path: string;
  max_questions: number;
}

export const DEFAULT_QUIZ_CONFIG: DeepQuestionFormConfig = {
  mode: "custom",
  topic: "",
  num_questions: 3,
  difficulty: "auto",
  question_type: "auto",
  preference: "",
  paper_path: "",
  max_questions: 10,
};

export interface QuizQuestion {
  question_id: string;
  question: string;
  question_type: "choice" | "written" | "coding";
  options?: Record<string, string>;
  correct_answer: string;
  explanation: string;
  difficulty?: string;
  concentration?: string;
  knowledge_context?: string;
}

export interface QuizFollowupContext {
  parent_quiz_session_id?: string;
  question_id: string;
  question: string;
  question_type: QuizQuestion["question_type"];
  options?: Record<string, string>;
  correct_answer: string;
  explanation: string;
  difficulty?: string;
  concentration?: string;
  knowledge_context?: string;
  user_answer?: string;
  is_correct?: boolean;
}

/**
 * Extract QuizQuestion[] from the raw `result` event metadata returned by
 * the deep_question capability.
 */
export function extractQuizQuestions(
  resultMetadata: Record<string, unknown> | undefined,
): QuizQuestion[] | null {
  if (!resultMetadata) return null;
  const summary = resultMetadata.summary as Record<string, unknown> | undefined;
  if (!summary) return null;
  const results = summary.results as Array<Record<string, unknown>> | undefined;
  if (!Array.isArray(results) || results.length === 0) return null;

  const parsed: Array<QuizQuestion | null> = results.map((item) => {
    const qa = (item.qa_pair ?? item) as Record<string, unknown>;
    if (!qa.question) return null;
    const question: QuizQuestion = {
      question_id: String(qa.question_id ?? ""),
      question: String(qa.question ?? ""),
      question_type: (qa.question_type as QuizQuestion["question_type"]) ?? "written",
      options: qa.options as Record<string, string> | undefined,
      correct_answer: String(qa.correct_answer ?? ""),
      explanation: String(qa.explanation ?? ""),
      difficulty: qa.difficulty ? String(qa.difficulty) : undefined,
      concentration: qa.concentration ? String(qa.concentration) : undefined,
      knowledge_context:
        qa.metadata &&
        typeof qa.metadata === "object" &&
        "knowledge_context" in qa.metadata &&
        qa.metadata.knowledge_context
          ? String(qa.metadata.knowledge_context)
          : undefined,
    };
    return question;
  });

  return parsed.filter((question): question is QuizQuestion => question !== null);
}

export function buildQuizFollowupConfig(
  question: QuizQuestion,
  userAnswer: string,
  isCorrect: boolean | null,
  parentQuizSessionId?: string | null,
): Record<string, unknown> {
  const context: QuizFollowupContext = {
    question_id: question.question_id,
    question: question.question,
    question_type: question.question_type,
    options: question.options,
    correct_answer: question.correct_answer,
    explanation: question.explanation,
    difficulty: question.difficulty,
    concentration: question.concentration,
    knowledge_context: question.knowledge_context,
    user_answer: userAnswer || undefined,
    is_correct: typeof isCorrect === "boolean" ? isCorrect : undefined,
    parent_quiz_session_id: parentQuizSessionId || undefined,
  };

  return {
    followup_question_context: context,
  };
}

function titleCase(value: string): string {
  if (!value) return "";
  return value.charAt(0).toUpperCase() + value.slice(1);
}

/**
 * One-line summary of the quiz form, shown next to the collapsed `Settings`
 * chevron in the composer. Pass `translate` (`t` from `react-i18next`) so the
 * summary follows the active UI language.
 */
export function summarizeQuizConfig(
  cfg: DeepQuestionFormConfig,
  translate?: (key: string) => string,
): string {
  const tr = translate ?? ((s: string) => s);
  if (cfg.mode === "mimic") {
    const target = cfg.paper_path.trim() || tr("no paper");
    return [tr("Mimic Paper"), target, `${tr("Max")} ${cfg.max_questions}`].join(" · ");
  }
  return [
    tr("Custom"),
    `${cfg.num_questions} ${tr("questions")}`,
    tr(titleCase(cfg.difficulty || "auto")),
    tr(titleCase(cfg.question_type || "auto")),
  ].join(" · ");
}

/**
 * Build the `config` payload to send over WebSocket for a quiz generation
 * request.
 */
export function buildQuizWSConfig(
  cfg: DeepQuestionFormConfig,
): Record<string, unknown> {
  if (cfg.mode === "mimic") {
    return {
      mode: "mimic",
      paper_path: cfg.paper_path.trim(),
      max_questions: cfg.max_questions,
    };
  }
  return {
    mode: "custom",
    num_questions: cfg.num_questions,
    difficulty: cfg.difficulty === "auto" ? "" : cfg.difficulty,
    question_type: cfg.question_type === "auto" ? "" : cfg.question_type,
    preference: cfg.preference.trim(),
  };
}
