import assert from "node:assert/strict";

const values = new Map<string, string>();
const events = new Map<string, (event: { key: string | null }) => void>();
Object.defineProperty(globalThis, "localStorage", { configurable: true, value: {
  getItem: (key: string) => values.get(key) ?? null,
  setItem: (key: string, value: string) => { values.set(key, value); },
} });
Object.defineProperty(globalThis, "window", { configurable: true, value: {
  addEventListener: (name: string, listener: (event: { key: string | null }) => void) => { events.set(name, listener); },
} });
const learning = await import("../src/lib/learning");
function reset() { values.clear(); events.get("storage")!({ key: null }); }
const attempt = (id: string, correct: boolean, revealed = false) => learning.recordQuestionAttempt({ questionId: id, readingId: 57, prompt: "Estimate the price change.", sectionId: "full-quiz", objectiveIds: ["57.a"], correct, revealed });

reset();
learning.rememberStudyPosition(57, "full-module-57.2");
assert.equal(learning.readStudyState().resume?.readingId, 57);
assert.equal(learning.studyPositionRoute(learning.readStudyState().resume!), "#/reading/57/section/full-module-57.2");
learning.rememberQuizPosition(57, "q-3");
assert.equal(learning.getSavedQuizQuestion(57), "q-3");
assert.equal(learning.studyPositionRoute(learning.readStudyState().resume!), "#/reading/57/section/full-quiz?question=q-3");
events.get("storage")!({ key: "return-lab-study-v1" });
assert.equal(learning.getSavedQuizQuestion(57), "q-3", "quiz position survives storage reload");
learning.completeModule(57, "57.2");
learning.completeModule(57, "57.2");
assert.deepEqual(learning.readStudyState().completedModules[57], ["57.2"]);

learning.registerQuestions(57, ["quiz:57:q-1", "quiz:57:q-2"]);
learning.registerQuestions(57, ["quiz:57:q-1"]);
learning.registerQuestions(57, ["application:57:a-1"]);
assert.equal(learning.readStudyState().questionIds[57].length, 3, "checkpoint scope never shrinks reading catalog");
attempt("quiz:57:q-1", false);
attempt("quiz:57:q-1", true);
const history = learning.readStudyState().questions["quiz:57:q-1"];
assert.equal(history.firstCorrect, false);
assert.equal(history.latestCorrect, true);
assert.equal(history.attempts.length, 2);
attempt("quiz:57:q-2", true, true);
assert.equal(learning.readStudyState().questions["quiz:57:q-2"].firstCorrect, undefined);
assert.equal(learning.readStudyState().questions["quiz:57:q-2"].latestCorrect, false, "revealed answers never earn mastery");
assert.ok(learning.readStudyState().questions["quiz:57:q-2"].dueAt <= Date.now());
assert.equal(learning.getReadingProgress(learning.readStudyState(), 57, true).status, "Read");
attempt("quiz:57:q-2", true);
attempt("application:57:a-1", true);
const progress = learning.getReadingProgress(learning.readStudyState(), 57);
assert.equal(progress.status, "Mastered");
assert.equal(progress.firstAttemptCorrect, 2);
assert.equal(progress.correct, 3);
assert.equal(learning.reviewQuestionRoute(history), "#/reading/57/section/full-quiz?question=q-1&retry=1");
learning.rateQuestionReview("quiz:57:q-1", "again");
assert.ok(learning.readStudyState().questions["quiz:57:q-1"].dueAt > Date.now());
assert.equal(learning.readStudyState().questions["quiz:57:q-1"].firstCorrect, false, "self-rated review cannot change assessment history");

reset();
learning.registerQuestions(1, ["quiz:1:q"]);
learning.recordQuestionAttempt({ questionId: "quiz:1:q", readingId: 1, prompt: "Return", sectionId: "full-quiz", correct: true });
assert.notEqual(learning.getReadingProgress(learning.readStudyState(), 1).status, "Mastered", "both module and application assessments are required");
reset();
const boundaryIds = Array.from({ length: 44 }, (_, index) => `${index ? "quiz" : "application"}:57:boundary-${index}`);
learning.registerQuestions(57, boundaryIds);
boundaryIds.forEach((id, index) => attempt(id, index < 35));
assert.equal(learning.getReadingProgress(learning.readStudyState(), 57).score, 80);
assert.notEqual(learning.getReadingProgress(learning.readStudyState(), 57).status, "Mastered", "rounded display scores cannot cross the mastery threshold");
attempt(boundaryIds[35], true);
assert.equal(learning.getReadingProgress(learning.readStudyState(), 57).status, "Mastered");
values.set("return-lab-study-v1", "{invalid json");
events.get("storage")!({ key: "return-lab-study-v1" });
assert.deepEqual(learning.readStudyState().questions, {});
values.set("return-lab-study-v1", JSON.stringify({ version: 1, visited: [1, "wrong"], completedModules: null, questionIds: { 1: "wrong" }, quizPositions: { 1: {} }, resume: { readingId: 999 }, questions: {} }));
events.get("storage")!({ key: "return-lab-study-v1" });
assert.equal(learning.getReadingProgress(learning.readStudyState(), 1).status, "In progress");
assert.deepEqual(learning.readStudyState().completedModules, {});
assert.equal(learning.readStudyState().resume, undefined);
Object.defineProperty(globalThis, "localStorage", { configurable: true, value: { getItem: () => { throw new Error("Storage blocked"); }, setItem: () => { throw new Error("Storage blocked"); } } });
events.get("storage")!({ key: null });
learning.rememberStudyPosition(2, "full-module-2.1");
assert.equal(learning.readStudyState().resume?.readingId, 2, "learning continues with blocked storage");
console.log("Learning state checks passed: resume, checkpoint catalog, history, revealed-answer handling, mastery, review scheduling, malformed and blocked storage.");
