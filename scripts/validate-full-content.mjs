import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import katex from "katex";

const root = fileURLToPath(new URL("../", import.meta.url));
const readJson = (path) => JSON.parse(readFileSync(resolve(root, path), "utf8"));
const curriculum = readJson("src/data/manifest.json");
const objectiveSource = readJson("src/data/sourceManifest.json");
const objectiveQuestions = readJson("src/data/objectiveQuestions.json");
const classification = readJson("docs/math-visual-classification.json");
const forbidden = /\b(?:LOS|Schweser(?:Notes)?|Kaplan|QBank|Book\s+[1-4]|PDF\s+page|source map|verification scope|this book|Copyright|Reproduced|Republished|Ibid|Standards of Practice Handbook|CFA curriculum learning module|All rights reserved|with permission|published by)\b/i;
const contentDir = resolve(root, "public/content");
const assets = new Set();
let blockCount = 0;
let imageOccurrences = 0;
let mathOccurrences = 0;
let objectiveCount = 0;
let quizCount = 0;

function visibleText(value) {
  const stepText = value.steps?.flatMap((step) => [step.title, ...(step.body || []), ...(step.rows || []).flat(), ...(step.equations || [])]) || [];
  return [value.text, value.prose, value.alt, value.prompt, value.explanation, value.latex, ...stepText]
    .filter((item) => typeof item === "string").join("\n");
}

function validateKatex(latex, location, displayMode = true) {
  try {
    katex.renderToString(latex, { displayMode, strict: "ignore", throwOnError: true });
  } catch (error) {
    throw new Error(`${location}: invalid KaTeX (${error.message})`, { cause: error });
  }
}

function validateBlocks(blocks, location) {
  assert(Array.isArray(blocks), `${location}: missing content array`);
  for (const block of blocks) {
    blockCount += 1;
    assert(["heading", "paragraph", "question", "image", "math", "worked-example"].includes(block.type), `${location}: invalid block type ${block.type}`);
    const text = visibleText(block);
    assert(!text.includes("\uFFFD"), `${location}: unreadable character`);
    assert(!forbidden.test(text), `${location}: source-only reference in learner content`);
    if (block.type === "math") {
      mathOccurrences += 1;
      assert(typeof block.latex === "string" && block.latex.trim(), `${location}: empty LaTeX`);
      assert(typeof block.sourceAsset === "string" && /^[a-zA-Z0-9-]+\.png$/.test(block.sourceAsset), `${location}: missing math source asset`);
      validateKatex(block.latex, `${location} asset ${block.sourceAsset}`, block.display !== false);
      continue;
    }
    if (block.type === "worked-example") {
      mathOccurrences += 1;
      assert(typeof block.sourceAsset === "string" && /^[a-zA-Z0-9-]+\.png$/.test(block.sourceAsset), `${location}: missing worked-example source asset`);
      assert(typeof block.title === "string" && block.title.trim(), `${location}: missing worked-example title`);
      assert(Array.isArray(block.steps) && block.steps.length > 0, `${location}: missing worked-example steps`);
      for (const step of block.steps) {
        assert(typeof step.title === "string" && step.title.trim(), `${location}: missing worked-example step title`);
        for (const equation of step.equations || []) validateKatex(equation, `${location} asset ${block.sourceAsset}`);
      }
      continue;
    }
    if (block.type === "image") {
      imageOccurrences += 1;
      assert(block.visualKind === "diagram-chart-or-table", `${location}: unclassified retained image`);
      assert(typeof block.alt === "string" && block.alt.trim(), `${location}: missing visual description`);
      assert(typeof block.src === "string" && /^content\/figures\/[a-zA-Z0-9-]+\.png$/.test(block.src), `${location}: invalid asset URL`);
      const path = resolve(root, "public", block.src);
      assert(path.startsWith(contentDir + sep), `${location}: asset outside content directory`);
      assert(block.width > 0 && block.height > 0, `${location}: missing image dimensions`);
      if (!assets.has(path)) {
        assets.add(path);
        const bytes = readFileSync(path);
        assert(bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10])), `${location}: invalid PNG`);
        assert(bytes.readUInt32BE(16) > 0 && bytes.readUInt32BE(20) > 0, `${location}: empty image`);
      }
      continue;
    }
    assert(typeof block.text === "string" && block.text.trim(), `${location}: empty content`);
    if (block.type === "question") assert(/^.+\?$/.test(block.text), `${location}: learning outcome is not a question`);
  }
}

function validateQuiz(question, location) {
  quizCount += 1;
  assert(typeof question.id === "string" && question.id, `${location}: missing ID`);
  assert(typeof question.prompt === "string" && question.prompt.trim(), `${location}: empty prompt`);
  assert(!forbidden.test(visibleText(question)), `${location}: source-only reference in question`);
  assert(Array.isArray(question.options) && question.options.length === 3, `${location}: expected three selectable choices`);
  assert.deepEqual(question.options.map((option) => option.id), ["A", "B", "C"], `${location}: invalid option IDs`);
  for (const option of question.options) {
    assert(typeof option.text === "string" && option.text.trim(), `${location}: empty option ${option.id}`);
    assert(!forbidden.test(option.text), `${location}: source-only reference in option ${option.id}`);
  }
  assert(question.options.some((option) => option.id === question.correctOptionId), `${location}: answer key is not a choice`);
  assert(typeof question.explanation === "string", `${location}: missing explanation`);
  assert(question.explanation.trim() || question.solutionBlocks.length, `${location}: no answer reasoning`);
  assert(Array.isArray(question.objectiveIds), `${location}: missing internal objective links`);
  validateBlocks(question.supportingBlocks, `${location} supporting material`);
  validateBlocks(question.solutionBlocks, `${location} solution`);
}

const expectedObjectives = objectiveSource.flatMap((module) => module.objectives);
assert.equal(expectedObjectives.length, 365, "Source objective count changed");
assert.equal(objectiveQuestions.length, 365, "Every source objective needs one learner question");
assert.equal(new Set(objectiveQuestions.map((item) => item.id)).size, 365, "Duplicate learner objective IDs");
for (const item of objectiveQuestions) {
  assert(item.question.endsWith("?"), `Objective ${item.id}: learner version is not a question`);
  assert(!forbidden.test(item.question), `Objective ${item.id}: source label is visible`);
}

const files = readdirSync(resolve(contentDir, "readings")).filter((name) => name.endsWith(".json"));
assert.equal(files.length, curriculum.length, "Every reading must have complete content");
for (const reading of curriculum) {
  const lesson = readJson(`public/content/readings/${String(reading.number).padStart(3, "0")}.json`);
  const location = `Reading ${reading.number}`;
  assert.equal(lesson.readingId, reading.number, `${location}: wrong ID`);
  assert.equal(lesson.title, reading.title, `${location}: wrong title`);
  assert.deepEqual(lesson.modules.map((module) => module.id), reading.modules.map((module) => module.id), `${location}: module coverage changed`);
  const expectedIds = objectiveSource.filter((item) => item.readingId === reading.number).flatMap((item) => item.objectives.map((objective) => objective.id));
  assert.deepEqual(lesson.objectives.map((objective) => objective.id), expectedIds, `${location}: objective mapping changed`);
  objectiveCount += lesson.objectives.length;
  validateBlocks(lesson.introduction, `${location} introduction`);
  for (const module of lesson.modules) {
    assert(module.blocks.length, `${location}: empty module ${module.id}`);
    validateBlocks(module.blocks, `${location} module ${module.id}`);
  }
  if (![90, 91, 93].includes(reading.number)) assert(lesson.review.length, `${location}: missing review`);
  validateBlocks(lesson.review, `${location} review`);
  assert(Array.isArray(lesson.quizSets) && lesson.quizSets.length, `${location}: missing interactive quizzes`);
  lesson.quizSets.forEach((set, setIndex) => {
    assert(set.questions.length, `${location}: empty quiz set ${setIndex + 1}`);
    set.questions.forEach((question, index) => validateQuiz(question, `${location} quiz ${setIndex + 1} question ${index + 1}`));
  });
}

const reference = readJson("public/content/reference.json");
assert.equal(reference.sections.length, 4, "Missing reference section");
for (const section of reference.sections) {
  assert(section.blocks.length, `Reference ${section.id}: empty`);
  validateBlocks(section.blocks, `Reference ${section.id}`);
}

assert.equal(objectiveCount, 365, "All 365 learning outcomes must be represented");
assert.equal(quizCount, 565, "All 565 imported multiple-choice questions must be interactive");
assert.equal(classification.summary.sourceAssetsClassified, 976, "Every original visual asset must be classified");
assert.equal(classification.summary.nativeMath + classification.summary.meaningfulVisuals + classification.summary.rebuiltTables, 976, "Visual classification totals do not reconcile");
assert.equal(classification.assets.length, 976, "Visual classification audit is incomplete");
for (const visual of classification.assets) {
  assert(Array.isArray(visual.sourceIds) && visual.sourceIds.length, `${visual.asset}: missing original source trace`);
  if (visual.classification === "native-math") {
    assert(typeof visual.latex === "string" && visual.latex.trim(), `${visual.asset}: missing converted notation`);
    if ("recognitionConfidence" in visual && visual.recognitionConfidence !== null) assert(typeof visual.recognitionConfidence === "number" && visual.recognitionConfidence >= 0.8, `${visual.asset}: equation recognition requires review`);
    assert(visual.verification.includes("source-traced") && visual.verification.includes("katex-parse-checked"), `${visual.asset}: equation verification is incomplete`);
    validateKatex(visual.latex, `Classification ${visual.asset}`);
  }
}
console.log(`Validated ${files.length} readings, ${objectiveCount} learner questions, ${quizCount} interactive quiz questions, ${mathOccurrences} native-math occurrences, ${imageOccurrences} meaningful visual occurrences, and ${classification.assets.length} classified source assets.`);
