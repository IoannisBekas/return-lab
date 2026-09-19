import katex from "katex";
import curriculum from "../src/data/curriculum.json";
import sourceManifest from "../src/data/sourceManifest.json";
import { quantitativeDeepLessons } from "../src/data/deep/quantitative";
import { economicsDeepLessons } from "../src/data/deep/economics";
import { corporateDeepLessons } from "../src/data/deep/corporate";
import { financialStatementDeepLessons } from "../src/data/deep/financialStatements";
import { equityDeepLessons } from "../src/data/deep/equity";
import { fixedIncomeDeepLessons } from "../src/data/deep/fixedIncome";
import { derivativesDeepLessons } from "../src/data/deep/derivatives";
import { alternativeDeepLessons } from "../src/data/deep/alternatives";
import { portfolioEthicsDeepLessons } from "../src/data/deep/portfolioEthics";
import type { DeepLesson } from "../src/data/deepLessonTypes";

const goldReadingIds = new Set([1, 28, 57, 83, 91]);
const expectedDeepIds = curriculum
  .map((reading) => reading.number)
  .filter((readingId) => !goldReadingIds.has(readingId));
const lessons: DeepLesson[] = [
  ...quantitativeDeepLessons,
  ...economicsDeepLessons,
  ...corporateDeepLessons,
  ...financialStatementDeepLessons,
  ...equityDeepLessons,
  ...fixedIncomeDeepLessons,
  ...derivativesDeepLessons,
  ...alternativeDeepLessons,
  ...portfolioEthicsDeepLessons,
];

const failures: string[] = [];
const fail = (message: string) => failures.push(message);
const deepIds = lessons.map((lesson) => lesson.readingId);
const uniqueDeepIds = new Set(deepIds);

if (lessons.length !== expectedDeepIds.length || uniqueDeepIds.size !== expectedDeepIds.length) {
  fail(`Expected ${expectedDeepIds.length} unique universal lessons; found ${lessons.length} records and ${uniqueDeepIds.size} IDs.`);
}

for (const expectedId of expectedDeepIds) {
  if (!uniqueDeepIds.has(expectedId)) fail(`Reading ${expectedId} has no universal deep lesson.`);
}
for (const readingId of uniqueDeepIds) {
  if (!expectedDeepIds.includes(readingId)) fail(`Reading ${readingId} should use an existing gold lesson, not universal data.`);
}

type SourceEntry = (typeof sourceManifest)[number];
const sourceByReading = new Map<number, SourceEntry[]>();
for (const entry of sourceManifest) {
  const entries = sourceByReading.get(entry.readingId) || [];
  entries.push(entry);
  sourceByReading.set(entry.readingId, entries);
}

let formulaCount = 0;
let exampleCount = 0;
let assessmentCount = 0;
const longTeachingStrings = new Map<string, string[]>();
const exampleIds = new Set<string>();
const assessmentIds = new Set<string>();
const lostLatexEscape = /(?<!\\)\b(?:Delta|Gamma|Theta|Lambda|Sigma|Omega|alpha|beta|gamma|delta|theta|lambda|mu|rho|sigma|omega|mathrm|mathbf|text|frac|sqrt|sum|prod|times|cdot)\b/;
const latexControlCharacter = /[\u0000-\u001F\u007F]/;

for (const lesson of lessons) {
  const reading = curriculum.find((candidate) => candidate.number === lesson.readingId);
  if (!reading) {
    fail(`Deep lesson ${lesson.readingId} has no curriculum record.`);
    continue;
  }
  if (!lesson.title.trim()) fail(`Reading ${lesson.readingId} has no learner-facing lesson title.`);
  if (/\b(?:TODO|TBD|placeholder)\b/i.test(JSON.stringify(lesson))) fail(`Reading ${lesson.readingId} contains unfinished placeholder text.`);

  const expectedModules = reading.modules.map((module) => module.id).sort();
  const sectionModules = lesson.sections.map((section) => section.moduleId).sort();
  if (JSON.stringify(sectionModules) !== JSON.stringify(expectedModules)) {
    fail(`Reading ${lesson.readingId} sections do not match curriculum modules (${sectionModules.join(", ")} vs ${expectedModules.join(", ")}).`);
  }

  const sourceEntries = sourceByReading.get(lesson.readingId) || [];
  const sourceObjectives = new Set(sourceEntries.flatMap((entry) => entry.objectives.map((objective) => objective.id)));
  const sourceModules = sourceEntries.map((entry) => entry.moduleId).sort();
  if (JSON.stringify(sourceModules) !== JSON.stringify(expectedModules)) {
    fail(`Reading ${lesson.readingId} source-map modules do not match its curriculum modules.`);
  }

  for (const section of lesson.sections) {
    const expectedTitle = reading.modules.find((module) => module.id === section.moduleId)?.title;
    if (section.title !== expectedTitle) fail(`Reading ${lesson.readingId} module ${section.moduleId} title does not match the curriculum.`);
    if (!section.lead.trim()) fail(`Reading ${lesson.readingId} module ${section.moduleId} has no lead.`);
    if (section.paragraphs.length < 2) fail(`Reading ${lesson.readingId} module ${section.moduleId} needs at least two explanatory paragraphs.`);
    if (section.keyPoints.length < 3) fail(`Reading ${lesson.readingId} module ${section.moduleId} needs at least three key points.`);
    for (const paragraph of section.paragraphs) {
      if (paragraph.trim().length < 90) fail(`Reading ${lesson.readingId} module ${section.moduleId} has an underdeveloped paragraph.`);
      if (paragraph.length >= 120) {
        const locations = longTeachingStrings.get(paragraph) || [];
        locations.push(`${lesson.readingId}:${section.moduleId}`);
        longTeachingStrings.set(paragraph, locations);
      }
    }
  }

  if (!lesson.sections.some((section) => section.miniExample)) {
    fail(`Reading ${lesson.readingId} needs at least one mini-example.`);
  }

  const exampleModules = new Set(lesson.workedExamples.flatMap((example) => example.moduleIds));
  for (const moduleId of expectedModules) {
    if (!exampleModules.has(moduleId)) fail(`Reading ${lesson.readingId} module ${moduleId} has no worked example.`);
  }
  for (const example of lesson.workedExamples) {
    exampleCount += 1;
    if (exampleIds.has(example.id)) fail(`Worked example ID ${example.id} is duplicated.`);
    exampleIds.add(example.id);
    if (!example.given.length || !example.find.trim() || !example.plan.trim()) fail(`Worked example ${example.id} is missing its brief.`);
    if (example.steps.length < 2) fail(`Worked example ${example.id} needs at least two auditable steps.`);
    if (!example.interpret.trim() || !example.sanityCheck.trim()) fail(`Worked example ${example.id} needs interpretation and a sanity check.`);
    for (const moduleId of example.moduleIds) {
      if (!expectedModules.includes(moduleId)) fail(`Worked example ${example.id} references unknown module ${moduleId}.`);
    }
    for (const step of example.steps) {
      if (!step.latex) continue;
      try {
        katex.renderToString(step.latex, { strict: "error", throwOnError: true });
      } catch (error) {
        fail(`Worked example ${example.id} contains invalid LaTeX “${step.latex}”: ${error instanceof Error ? error.message : error}`);
      }
      if (latexControlCharacter.test(step.latex)) fail(`Worked example ${example.id} contains a control character that may indicate a lost LaTeX escape.`);
      if (lostLatexEscape.test(step.latex)) fail(`Worked example ${example.id} appears to have lost a LaTeX command escape: “${step.latex}”.`);
    }
  }

  if (lesson.misconceptions.length < 3) fail(`Reading ${lesson.readingId} needs at least three specific misconceptions.`);
  if (lesson.assessments.length < 2) fail(`Reading ${lesson.readingId} needs at least two assessments.`);
  for (const assessment of lesson.assessments) {
    assessmentCount += 1;
    if (assessmentIds.has(assessment.id)) fail(`Assessment ID ${assessment.id} is duplicated.`);
    assessmentIds.add(assessment.id);
    if (!assessment.objectiveIds.length) fail(`Assessment ${assessment.id} has no objective mapping.`);
    for (const objectiveId of assessment.objectiveIds) {
      if (!sourceObjectives.has(objectiveId)) fail(`Assessment ${assessment.id} references unknown objective ${objectiveId}.`);
    }
    const optionIds = assessment.options.map((option) => option.id);
    const requiredOptionIds = ["A", "B", "C", "D"] as const;
    if (assessment.options.length !== 4 || new Set(optionIds).size !== 4 || requiredOptionIds.some((id) => !optionIds.includes(id))) {
      fail(`Assessment ${assessment.id} must have exactly one option A–D.`);
    }
    if (!assessment.options.some((option) => option.id === assessment.correctOptionId)) fail(`Assessment ${assessment.id} has no matching correct option.`);
    if (assessment.options.some((option) => !option.feedback.trim())) fail(`Assessment ${assessment.id} has an option without feedback.`);
    if (assessment.solution.length < 2) fail(`Assessment ${assessment.id} needs a stepwise solution.`);
  }
  const assessedObjectives = new Set(lesson.assessments.flatMap((assessment) => assessment.objectiveIds));
  for (const entry of sourceEntries) {
    if (entry.objectives.length && !entry.objectives.some((objective) => assessedObjectives.has(objective.id))) {
      fail(`Reading ${lesson.readingId} module ${entry.moduleId} has no objective-linked assessment.`);
    }
  }

  const formulaIds = new Set<string>();
  for (const formula of lesson.formulas) {
    formulaCount += 1;
    if (formulaIds.has(formula.id)) fail(`Reading ${lesson.readingId} repeats formula ID ${formula.id}.`);
    formulaIds.add(formula.id);
    if (!formula.variables.length || !formula.assumptions.length || !formula.domain.trim() || !formula.interpretation.trim()) {
      fail(`Formula ${formula.id} is missing variables, assumptions, domain, or interpretation.`);
    }
    try {
      katex.renderToString(formula.latex, { strict: "error", throwOnError: true });
    } catch (error) {
      fail(`Formula ${formula.id} contains invalid LaTeX “${formula.latex}”: ${error instanceof Error ? error.message : error}`);
    }
    if (latexControlCharacter.test(formula.latex)) fail(`Formula ${formula.id} contains a control character that may indicate a lost LaTeX escape.`);
    if (lostLatexEscape.test(formula.latex)) fail(`Formula ${formula.id} appears to have lost a LaTeX command escape: “${formula.latex}”.`);
    for (const variable of formula.variables) {
      try {
        katex.renderToString(variable.symbol, { strict: "error", throwOnError: true });
      } catch (error) {
        fail(`Formula ${formula.id} contains an invalid variable symbol “${variable.symbol}”: ${error instanceof Error ? error.message : error}`);
      }
      if (latexControlCharacter.test(variable.symbol)) fail(`Formula ${formula.id} variable contains a control character that may indicate a lost LaTeX escape.`);
      if (lostLatexEscape.test(variable.symbol)) fail(`Formula ${formula.id} variable “${variable.symbol}” appears to have lost a LaTeX command escape.`);
    }
  }
}

for (const [paragraph, locations] of longTeachingStrings) {
  if (locations.length > 1) fail(`Repeated teaching paragraph appears in ${locations.join(", ")}: ${paragraph.slice(0, 90)}…`);
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(
  `Validated ${lessons.length} universal deep lessons, ${lessons.reduce((sum, lesson) => sum + lesson.sections.length, 0)} module sections, ${formulaCount} formulas, ${exampleCount} worked examples, and ${assessmentCount} assessments.`,
);
