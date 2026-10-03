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

Readings open as module study sessions with estimated time, recall prompts, recaps, and scoped checkpoints. Learners can also browse the full reading. The home page resumes the saved module or question; the lesson outline and main navigation remain available on mobile.

Worked examples invite learners to attempt each step before revealing it. Selected examples include calculation checks with explicit units and rounding tolerances. Interactive diagrams cover cash flow timing, supply and demand, statement links, bond price sensitivity, option payoffs, portfolio risk and return, and ethical decision making. Readings 70, 74, 75, and 92 have focused forward-pricing, put–call parity, binomial-replication, and composite-construction labs.

Progress, reflection notes, and practice attempts are stored in the learner's browser. Quiz retries preserve first-attempt history. Readings distinguish study completion from mastery: mastery requires attempting both the module quiz and application questions, with at least 80% correct on the latest independent attempts. Revealing an answer does not earn mastery. The review page links missed questions to their concepts and schedules later recall; self-rated review changes the schedule without changing assessment scores. Existing reading and answer storage keys remain compatible. Study history is local to this browser and device.

The formula and statistical reference is available from the main navigation, lesson outline, and footer. Search and topic filters preserve complete formula entries with their equations, definitions, and conditions. Formula flashcards have due/all queues, lesson links, and Again/Hard/Good review ratings after recall. Equations, tables, and diagrams can be enlarged for detailed study.

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
npm run test:learning
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
src/components/learning/ReviewPage.tsx       Personal question and flashcard review plan
src/components/learning/ActivityLab.tsx      Active examples and focused finance labs
src/components/learning/activityModels.ts   Finance calculation models and identities
src/lib/learning.ts                         Study position, question history, and mastery
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

On PowerShell, use `$env:VITE_BASE_PATH='/return-lab-live/'` before `npm run build`. The `return-lab` source repository workflow publishes at `/return-lab/`; the published course link above uses the `return-lab-live` repository and a build made with `/return-lab-live/`. Copy the complete `dist/` output, including `content/`, to that static repository and retain its `.nojekyll` file. Run `npm run test:learning`, the production build, and browser checks before publishing.
