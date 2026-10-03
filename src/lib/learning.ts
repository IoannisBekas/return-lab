import { useSyncExternalStore } from "react";

export type StudyPosition = { readingId: number; sectionId?: string; questionId?: string; updatedAt: number };
export type QuestionAttempt = { correct: boolean; revealed: boolean; at: number };
export type QuestionRecord = {
  questionId: string;
  readingId: number;
  prompt: string;
  sectionId: string;
  objectiveIds: string[];
  attempts: QuestionAttempt[];
  firstCorrect?: boolean;
  latestCorrect: boolean;
  dueAt: number;
  intervalDays: number;
};
export type StudyState = {
  version: 1;
  resume?: StudyPosition;
  visited: number[];
  completedModules: Record<string, string[]>;
  quizPositions: Record<string, string>;
  questionIds: Record<string, string[]>;
  questions: Record<string, QuestionRecord>;
};

const STORAGE_KEY = "return-lab-study-v1";
const DAY = 86_400_000;
const emptyState = (): StudyState => ({ version: 1, visited: [], completedModules: {}, quizPositions: {}, questionIds: {}, questions: {} });
const stringArrays = (value: unknown): Record<string, string[]> => value && typeof value === "object" && !Array.isArray(value)
  ? Object.fromEntries(Object.entries(value).filter(([, items]) => Array.isArray(items)).map(([key, items]) => [key, items.filter((item: unknown) => typeof item === "string")])) : {};

function loadState(): StudyState {
  try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null") as StudyState | null;
    if (!stored || stored.version !== 1 || !Array.isArray(stored.visited)) return emptyState();
    const validReadings = stored.visited.filter((id) => Number.isInteger(id) && id >= 1 && id <= 93);
    const questions = Object.fromEntries(Object.entries(stored.questions || {}).filter(([, question]) =>
      question && Number.isInteger(question.readingId) && typeof question.prompt === "string" && typeof question.sectionId === "string" && typeof question.questionId === "string" && Array.isArray(question.attempts) && Array.isArray(question.objectiveIds),
    ).map(([id, question]) => {
      const attempts = question.attempts.filter((attempt) => attempt && typeof attempt.correct === "boolean" && typeof attempt.revealed === "boolean" && Number.isFinite(attempt.at));
      return [id, { ...question, attempts, firstCorrect: attempts.find((attempt) => !attempt.revealed)?.correct, latestCorrect: attempts.at(-1)?.correct === true && attempts.at(-1)?.revealed === false, objectiveIds: question.objectiveIds.filter((objective) => typeof objective === "string"), dueAt: Number.isFinite(question.dueAt) ? question.dueAt : 0, intervalDays: Number.isFinite(question.intervalDays) ? question.intervalDays : 0 }];
    }));
    const resume = stored.resume && Number.isInteger(stored.resume.readingId) && stored.resume.readingId >= 1 && stored.resume.readingId <= 93
      ? { ...stored.resume, sectionId: typeof stored.resume.sectionId === "string" ? stored.resume.sectionId : undefined, questionId: typeof stored.resume.questionId === "string" ? stored.resume.questionId : undefined } : undefined;
    return { version: 1, resume, visited: validReadings, questions, completedModules: stringArrays(stored.completedModules), questionIds: stringArrays(stored.questionIds), quizPositions: Object.fromEntries(Object.entries(stored.quizPositions || {}).filter(([, id]) => typeof id === "string")) };
  } catch { return emptyState(); }
}

let state = loadState();
const listeners = new Set<() => void>();
function publish(next: StudyState) {
  state = next;
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch { /* Study stays available for this session. */ }
  listeners.forEach((listener) => listener());
}
function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => { listeners.delete(listener); };
}
if (typeof window !== "undefined") window.addEventListener("storage", (event) => {
  if (event.key === STORAGE_KEY || event.key === null) {
    state = loadState();
    listeners.forEach((listener) => listener());
  }
});

export const readStudyState = () => state;
export function useStudyState() { return useSyncExternalStore(subscribe, readStudyState, readStudyState); }

export function rememberStudyPosition(readingId: number, sectionId?: string, questionId?: string) {
  if (!Number.isInteger(readingId) || readingId < 1 || readingId > 93) return;
  if (state.resume?.readingId === readingId && state.resume.sectionId === sectionId && state.resume.questionId === questionId) return;
  publish({ ...state, visited: [...new Set([...state.visited, readingId])], resume: { readingId, sectionId, questionId, updatedAt: Date.now() } });
}

export function rememberQuizPosition(readingId: number, questionId: string) {
  publish({ ...state, quizPositions: { ...state.quizPositions, [readingId]: questionId } });
  rememberStudyPosition(readingId, "full-quiz", questionId);
}
export const getSavedQuizQuestion = (readingId: number) => state.quizPositions[readingId];

export function completeModule(readingId: number, moduleId: string) {
  const modules = state.completedModules[readingId] || [];
  if (modules.includes(moduleId)) return;
  publish({ ...state, completedModules: { ...state.completedModules, [readingId]: [...modules, moduleId] } });
}

export function registerQuestions(readingId: number, questionIds: string[]) {
  const previous = state.questionIds[readingId] || [];
  const next = [...new Set([...previous, ...questionIds])];
  if (next.length === previous.length) return;
  publish({ ...state, questionIds: { ...state.questionIds, [readingId]: next } });
}

export function recordQuestionAttempt(input: {
  questionId: string; readingId: number; prompt: string; sectionId: string;
  objectiveIds?: string[]; correct: boolean; revealed?: boolean;
}) {
  const previous = state.questions[input.questionId];
  const at = Date.now();
  const revealed = input.revealed === true;
  const correct = input.correct && !revealed;
  const intervalDays = correct ? Math.min(30, previous?.latestCorrect ? Math.max(3, (previous.intervalDays || 1) * 2) : 1) : 0;
  const record: QuestionRecord = {
    questionId: input.questionId, readingId: input.readingId, prompt: input.prompt,
    sectionId: input.sectionId, objectiveIds: input.objectiveIds || [],
    attempts: [...(previous?.attempts || []), { at, correct, revealed }],
    firstCorrect: previous?.firstCorrect ?? (revealed ? undefined : correct),
    latestCorrect: correct, dueAt: at + intervalDays * DAY, intervalDays,
  };
  publish({ ...state, questions: { ...state.questions, [input.questionId]: record } });
}

export function rateQuestionReview(questionId: string, rating: "again" | "hard" | "good") {
  const previous = state.questions[questionId];
  if (!previous) return;
  const intervalDays = rating === "again" ? 1 : rating === "hard" ? 2 : Math.min(30, Math.max(3, previous.intervalDays * 2));
  publish({ ...state, questions: { ...state.questions, [questionId]: { ...previous, intervalDays, dueAt: Date.now() + intervalDays * DAY } } });
}

export function getReadingProgress(study: StudyState, readingId: number, isRead = false) {
  const ids = study.questionIds[readingId] || [];
  const records = ids.map((id) => study.questions[id]).filter((record): record is QuestionRecord => Boolean(record));
  const correct = records.filter((record) => record.latestCorrect).length;
  const firstAttemptCorrect = records.filter((record) => record.firstCorrect === true).length;
  const firstAttempts = records.filter((record) => typeof record.firstCorrect === "boolean").length;
  const score = ids.length ? Math.round(correct / ids.length * 100) : 0;
  const assessedBothWays = ids.some((id) => id.startsWith("quiz:")) && ids.some((id) => id.startsWith("application:"));
  const mastered = assessedBothWays && records.length === ids.length && correct / ids.length >= 0.8;
  const status = mastered ? "Mastered" : isRead ? "Read" : study.visited.includes(readingId) || records.length ? "In progress" : "Ready";
  return { status, correct, total: ids.length, answered: records.length, firstAttemptCorrect, firstAttempts, score };
}

export function studyPositionRoute(position: Pick<StudyPosition, "readingId" | "sectionId" | "questionId">) {
  return `#/reading/${position.readingId}${position.sectionId ? `/section/${encodeURIComponent(position.sectionId)}` : ""}${position.questionId ? `?question=${encodeURIComponent(position.questionId)}` : ""}`;
}

export function reviewQuestionRoute(question: QuestionRecord) {
  const rawQuestionId = question.questionId.startsWith("quiz:") ? question.questionId.split(":").slice(2).join(":") : undefined;
  return `${studyPositionRoute({ readingId: question.readingId, sectionId: question.sectionId, questionId: rawQuestionId })}${rawQuestionId ? "&" : "?"}retry=1`;
}
