import { existsSync, readFileSync, readdirSync } from "node:fs";
import katex from "katex";

const root = new URL("../", import.meta.url);
const readJson = (path) => JSON.parse(readFileSync(new URL(path, root), "utf8"));
const curriculum = readJson("src/data/curriculum.json");
const manifest = readJson("src/data/manifest.json");
const sourceManifest = readJson("src/data/sourceManifest.json");
const readingDirectory = new URL("src/data/readings/", root);

const failures = [];
const fail = (message) => failures.push(message);

if (manifest.length !== curriculum.length || curriculum.length !== 93) {
  fail(`Expected 93 synchronized curriculum records; found curriculum=${curriculum.length}, manifest=${manifest.length}.`);
}

const readingFiles = readdirSync(readingDirectory).filter((file) => file.endsWith(".json"));
if (readingFiles.length !== 93) fail(`Expected 93 split reading files; found ${readingFiles.length}.`);

for (const reading of curriculum) {
  const filename = `src/data/readings/${String(reading.number).padStart(3, "0")}.json`;
  if (!existsSync(new URL(filename, root))) {
    fail(`Missing split reading ${filename}.`);
    continue;
  }
  const split = readJson(filename);
  if (JSON.stringify(split) !== JSON.stringify(reading)) fail(`Split reading ${reading.number} is stale.`);
}

const sourceModuleIds = new Set(sourceManifest.map((record) => record.moduleId));
const sourceObjectiveIds = sourceManifest.flatMap((record) => record.objectives.map((objective) => objective.id));
if (sourceManifest.length !== 152 || sourceModuleIds.size !== 152) {
  fail(`Expected 152 unique source-mapped modules; found ${sourceManifest.length} records and ${sourceModuleIds.size} IDs.`);
}
if (sourceObjectiveIds.length !== 365 || new Set(sourceObjectiveIds).size !== 365) {
  fail(`Expected 365 unique source learning outcomes; found ${sourceObjectiveIds.length} records and ${new Set(sourceObjectiveIds).size} IDs.`);
}

const formulasByModule = new Map(
  curriculum.flatMap((reading) => reading.modules.map((module) => [module.id, module.formula])),
);
const expectedFormulaLabels = new Map([
  ["2.2", "Cash flow additivity"],
  ["5.1", "Portfolio variance"],
  ["25.1", "Weighted-average cost of capital"],
  ["48.1", "Periodic coupon cash flow"],
]);
for (const [moduleId, label] of expectedFormulaLabels) {
  if (formulasByModule.get(moduleId)?.label !== label) fail(`Module ${moduleId} has the wrong formula mapping.`);
}
if (formulasByModule.get("25.1")?.expression.includes("w-dr-d")) fail("WACC still contains ambiguous debt notation.");

const goldFiles = ["src/data/goldQuantLessons.ts", "src/data/goldDecisionLessons.ts"];
let latexCount = 0;
for (const filename of goldFiles) {
  const source = readFileSync(new URL(filename, root), "utf8");
  const expressions = [...source.matchAll(/latex:\s*String\.raw`([^`]*)`/g)].map((match) => match[1]);
  latexCount += expressions.length;
  for (const expression of expressions) {
    try {
      katex.renderToString(expression, { strict: "error", throwOnError: true });
    } catch (error) {
      fail(`${filename} contains invalid LaTeX “${expression}”: ${error instanceof Error ? error.message : error}`);
    }
  }
}
if (latexCount < 25) fail(`Expected at least 25 checked LaTeX expressions; found ${latexCount}.`);

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(`Validated 93 lazy readings, 152 source-mapped modules, 365 learning outcomes, and ${latexCount} KaTeX expressions.`);
