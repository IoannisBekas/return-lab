# Return Lab design brief

Return Lab should feel like an editorial finance workbook made interactive: calm, precise, and structured around learning rather than a marketing funnel.

## Visual system

- Paper background with a restrained grid gives lessons the character of working notes.
- Ink, steel blue, and signal red create a compact functional palette.
- Outfit carries headings and long-form teaching copy; IBM Plex Mono carries labels, numbers, and measurements.
- Borders organize the interface in place of decorative shadows.
- Generated mechanical imagery represents finance as a connected system of inputs, assumptions, and outputs.

## Learning structure

The curriculum page makes all 93 readings visible and searchable. A reading page follows the same sequence every time: core idea, module explanation, reasoning method, application, self-check, and knowledge check. This consistency lets the learner focus on the finance concept instead of relearning the interface.

Progress is local to the browser and requires no account. All lesson routes use URL hashes so the production build works on static GitHub-compatible hosting without server-side rewrite rules.

## Content boundary

The application stores original explanatory copy and a factual hierarchy of topics, readings, and module titles. It does not store the reference PDFs, exported Markdown chapters, copied examples, or source question banks.
