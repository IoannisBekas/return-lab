# Return Lab

Return Lab is a standalone finance-learning app built with React, TypeScript, and Vite. It provides a navigable path through 93 Level I readings and 152 modules. An internal coverage manifest maps those modules to 365 learning outcomes in the supplied source books.

Five representative readings currently use the source-verified deep-lesson format:

- Reading 1: Rates and Returns
- Reading 28: Analyzing Income Statements
- Reading 57: Yield-Based Bond Duration Measures and Properties
- Reading 83: Portfolio Risk and Return
- Reading 91: Guidance for Standards I–VII

These lessons include objective-level explanations, KaTeX mathematics, variables and units, assumptions and valid domains, original worked examples, deterministic interactive diagrams, misconception checks, and balanced application questions with feedback for every option. The remaining readings retain their foundation lessons while they move through the same verification process.

The app stores reading progress, retrieval responses, and deep-lesson assessment attempts in the learner's browser. Reading files and the deep-lesson bundle load on demand.

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
```

`content:split` generates one lazy-loadable JSON file per reading. `validate:content` checks the 93 generated readings, the 152-module/365-outcome source map, known formula-routing regressions, and every structured KaTeX expression.

## Project structure

```text
src/App.tsx                                  Routing, curriculum, progress, and exercises
src/components/learning/GoldLesson.tsx       Deep-lesson renderer and assessment state
src/components/learning/FinanceVisuals.tsx   Accessible interactive finance diagrams
src/components/learning/MathText.tsx         Shared KaTeX renderer
src/data/curriculum.json                     Foundation course records
src/data/goldQuantLessons.ts                  Readings 1, 57, and 83 enrichment
src/data/goldDecisionLessons.ts               Readings 28 and 91 enrichment
src/data/sourceManifest.json                  Module-to-source/outcome coverage map
src/data/manifest.json                        Lightweight curriculum index
src/data/readings/                            Generated lazy reading files
scripts/build_source_manifest.py              Source-map generator
scripts/split-curriculum.mjs                  Reading-split generator
scripts/validate-content.mjs                  Content, formula, and synchronization checks
```

## Course authorship

The supplied reference material defines the required concepts and scope. Return Lab uses original teaching prose, examples, visuals, questions, and solutions. Source pages verify notation and coverage; source chapters and question banks are not reproduced in the application.

## Hosting

The app builds to static files in `dist/`. Hash-based routes support direct lesson and section navigation on GitHub Pages and other static hosts.

Set `VITE_BASE_PATH` when the deployment repository uses a different path from the source repository, for example:

```bash
VITE_BASE_PATH=/return-lab-live/ npm run build
```
