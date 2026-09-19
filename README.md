# Return Lab

Return Lab is a standalone finance course built with React, TypeScript, and Vite. It teaches the supplied Level I curriculum through 93 chapters, 152 complete modules, and 456 original practice questions with explained answers.

Each reading includes:

- explicit learning objectives and complete teaching notes;
- concept-specific formulas or analytical decision rules;
- key-term definitions and a repeatable reasoning process;
- worked applications and common mistakes;
- three original graded questions with explained answers per module;
- chapter review and knowledge checks; and
- progress tracking stored in the learner's browser.

Reading 1 also includes an interactive time-weighted return calculator. The home page supports topic filtering and full-text search across reading and module titles.

## Run locally

```bash
npm install
npm run dev
```

Create a production build with:

```bash
npm run build
```

Validate curriculum completeness with:

```bash
npm run validate:curriculum
```

The validation command confirms that chapters 1–93 are present and that every module has objectives, full lesson notes, key terms, a formula or decision rule, a worked application, common mistakes, a summary, and three valid practice questions with answer explanations.

## Project structure

```text
src/App.tsx                  Interface, navigation, progress, and exercises
src/data/curriculum.json     Original lesson copy for 93 readings
src/styles.css               Responsive visual system
public/assets/               Fonts and generated brand/learning media
scripts/validate-curriculum.mjs
```

## Course authorship

The supplied reference material defines the curriculum coverage. Return Lab provides a self-contained course through original teaching notes, examples, questions, solutions, and explanations written for this application.

## Hosting

The app is a static Vite build. The `dist/` output can be hosted on GitHub Pages, Cloudflare Pages, Netlify, Vercel, or any static web server. Hash-based lesson routes keep direct navigation compatible with static hosting.
