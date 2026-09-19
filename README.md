# Return Lab

Return Lab is a standalone finance learning app built with React, TypeScript, and Vite. It teaches the full supplied Level I curriculum across 93 readings, 152 modules, and 365 mapped learning outcomes.

Every reading includes:

- original explanations organized around the source learning outcomes;
- formal notation where it applies, rendered with KaTeX and paired with variables, units, assumptions, valid domains, and interpretation;
- worked examples with a stated plan, auditable steps, an interpretation, and a sanity check;
- common misconception checks;
- application questions with feedback for every answer choice and stepwise solutions;
- a module and page level source map for coverage verification.

Selected topics also include interactive diagrams for cash flow timing, supply and demand, statement links, bond price sensitivity, option payoffs, portfolio risk and return, and ethical decision making. Progress and assessment attempts are stored in the learner's browser.

Use the published course at [ioannisbekas.github.io/return-lab-live](https://ioannisbekas.github.io/return-lab-live/).

## Run locally

```bash
npm install
npm run dev
```

Create and validate a production build with:

```bash
npm run build
```

Useful content commands:

```bash
npm run content:split
npm run validate:curriculum
npm run validate:content
npm run validate:deep
```

`validate:content` checks the 93 curriculum records, the 152 module and 365 outcome source map, known formula routing regressions, and the structured KaTeX in the five custom lesson layouts. `validate:deep` checks the other 88 lessons for exact module and objective coverage, developed explanations, worked examples for every module, complete answer feedback, unique identifiers, and valid KaTeX.

## Project structure

```text
src/App.tsx                                  Routing, curriculum index, and progress
src/components/learning/GoldLesson.tsx       Deep lesson loader and shared renderer
src/components/learning/FinanceVisuals.tsx   Accessible interactive finance diagrams
src/components/learning/MathText.tsx         Shared KaTeX renderer
src/data/deep/*.ts                           Topic grouped lessons for 88 readings
src/data/deepLessonTypes.ts                  Deep lesson content contract
src/data/goldQuantLessons.ts                 Custom layouts for readings 1, 57, and 83
src/data/goldDecisionLessons.ts               Custom layouts for readings 28 and 91
src/data/sourceManifest.json                  Module to source and outcome coverage map
src/data/manifest.json                        Lightweight curriculum index
src/data/readings/                            Generated source synchronized records
scripts/validate-content.mjs                  Curriculum, source, and custom lesson checks
scripts/validate-deep-content.ts              Site wide deep lesson checks
```

## Course authorship

The supplied reference books define the required scope, terminology, and notation. Return Lab turns that scope into original teaching prose, examples, diagrams, questions, and solutions. The application does not reproduce source chapters, publisher question banks, or answer keys.

## Hosting

The app builds to static files in `dist/`. Hash based routes support direct lesson and section navigation on GitHub Pages and other static hosts.

Set `VITE_BASE_PATH` when the deployment repository uses a different path from the source repository. For example:

```bash
VITE_BASE_PATH=/return-lab-live/ npm run build
```
