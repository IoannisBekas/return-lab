# Return Lab

Return Lab is a standalone finance learning app built with React, TypeScript, and Vite. Its Level I curriculum spans 93 readings, 152 modules, and 365 learning outcomes.

Every reading includes:

- a complete lesson with module text, equations, tables, figures, and review material;
- explanations organized around the learning outcomes;
- formal notation where it applies, rendered with KaTeX and paired with variables, units, assumptions, valid domains, and interpretation;
- worked examples with a stated plan, auditable steps, an interpretation, and a sanity check;
- common misconception checks;
- application questions with feedback for every answer choice and stepwise solutions;
- module quizzes with answers and explanations hidden until the learner chooses to reveal them.

Selected topics also include interactive diagrams for cash flow timing, supply and demand, statement links, bond price sensitivity, option payoffs, portfolio risk and return, and ethical decision making. Progress and assessment attempts are stored in the learner's browser.

The formula and statistical reference is available from the main navigation, lesson outline, and footer. Equations, tables, and diagrams can be enlarged for detailed study.

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
npm run validate:full
```

`validate:content` checks the 93 curriculum records, the 152 module and 365 outcome source map, known formula routing regressions, and the structured KaTeX in the five custom lesson layouts. `validate:deep` checks the other 88 lessons for exact module and objective coverage, developed explanations, worked examples for every module, complete answer feedback, unique identifiers, and valid KaTeX. `validate:full` checks all complete readings and reference sections, module and objective coverage, review and solution content, valid figure assets, and unwanted book or publisher references. The production build runs all three content validators before TypeScript and Vite.

## Project structure

```text
src/App.tsx                                  Routing, curriculum index, and progress
src/components/learning/FullReading.tsx      Complete reading, review, figures, and solutions
src/components/learning/ReferenceLibrary.tsx Formula and statistical reference
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
public/content/readings/                      Complete lesson content by reading
public/content/figures/                       Equations, tables, and diagrams
public/content/reference.json                Formula and statistical reference content
scripts/build_full_readings.py                Complete instructional content importer
scripts/validate-content.mjs                  Curriculum, source, and custom lesson checks
scripts/validate-deep-content.ts              Site wide deep lesson checks
scripts/validate-full-content.mjs             Complete reading and reference validation
```

## Content maintenance

Learning objectives and module metadata support internal content validation. Students see the lessons, explanations, examples, and practice directly in the app; internal source locators and verification notes are not part of the learning interface.

The complete content layer ingests the supplied instructional readings, examples, quizzes, solutions, review material, and reference tables. Paragraphs reflow to the screen, mathematical crops are converted to KaTeX, and genuine diagrams, charts, and statistical tables remain zoomable. Every imported multiple-choice question is presented as an interactive card with hidden answers, option feedback, reasoning, progress, retry, and a final score.

To regenerate complete content, install Python with PyMuPDF, place the four supplied PDFs in one directory with their original filenames, then run:

```bash
python -m pip install pymupdf pix2text
npm run content:full
npm run validate:full
```

`content:full` imports the configured local source directory, creates learner-friendly outcome questions, builds structured quizzes, classifies every visual, and converts mathematical visuals. Recognition results are cached in `work/math-latex-cache.json`. Source documents, local paths, and validation metadata are not shipped in the student interface.

## Hosting

The app builds to static files in `dist/`. Hash based routes support direct lesson and section navigation on GitHub Pages and other static hosts.

Set `VITE_BASE_PATH` when the deployment repository uses a different path from the source repository. For example:

```bash
VITE_BASE_PATH=/return-lab-live/ npm run build
```
