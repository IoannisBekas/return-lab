# Return Lab

Return Lab is a standalone finance learning application built with React, TypeScript, and Vite. It turns the supplied Level I curriculum outline into an original, navigable learning path with 93 readings and 152 taught modules.

Each reading includes:

- a concise explanation of the core idea;
- concept-specific instruction for every module in the outline;
- a repeatable reasoning process;
- an applied practice prompt and self-check;
- a reading-level knowledge check; and
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

The validation command confirms that readings 1–93 are present and that every module has a title, explanation, three-step reasoning method, and self-check.

## Project structure

```text
src/App.tsx                  Interface, navigation, progress, and exercises
src/data/curriculum.json     Original lesson copy for 93 readings
src/styles.css               Responsive visual system
public/assets/               Fonts and generated brand/learning media
scripts/validate-curriculum.mjs
```

## Content policy

The source PDFs and Markdown exports are reference material supplied by the project owner. They are not committed to this repository. Return Lab contains an original educational treatment of the curriculum structure; it does not include copied source chapters, end-of-chapter question banks, or answer keys.

## Hosting

The app is a static Vite build. The `dist/` output can be hosted on GitHub Pages, Cloudflare Pages, Netlify, Vercel, or any static web server. Hash-based lesson routes keep direct navigation compatible with static hosting.
