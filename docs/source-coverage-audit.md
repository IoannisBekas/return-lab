# Instructional content coverage audit

Internal engineering evidence, 19 September 2026. This file is not learner-facing.

## Finding and resolution

The former lesson layer was a compressed study aid, not a replacement for the supplied instructional material. All 93 readings now have a separate full-content import derived from the original PDFs, including their introductions, teaching paragraphs, worked examples, module questions, answer explanations, and review material. A separate reference library preserves the instructional formula sheets and statistical appendices. Existing original explanations and interactive exercises remain supplementary.

The import is verified against an independently extracted original-PDF inventory. This establishes source coverage and file integrity; it does not establish that every original exercise has been independently recalculated or that every page has undergone visual comparison.

## Original scope and current preservation

| Independently inventoried item | Original scope | Validation |
| --- | ---: | --- |
| Readings | 93 | All reading files present |
| Instructional chapter pages | 1,025 | Every page and original block has an audit disposition |
| Formula/appendix pages | 26 | All blocks accounted for in reference library |
| Modules | 152 | Exact module IDs preserved |
| Learning outcomes | 365 | Exact objective IDs preserved |
| Explicit worked-example headings | 189 | All example markers preserved |
| Figure captions | 129 | All figure IDs preserved |
| Numbered module-quiz question starts | 565 | Quiz headings and question-number sequences match exactly |
| Instructional chapter image occurrences | 957 | All mapped to emitted visual assets |
| Decorative note/quiz image occurrences | 276 | Exact known icons excluded |

Chapter content contains 11,889 output blocks, including 940 visual blocks, and approximately 347,697 searchable text words. The reference library adds 148 blocks including 36 visual blocks. Output image counts differ from source occurrences because several inline fragments are preserved together in one composite region.

All 1,233 original chapter image occurrences reconcile exactly: 957 instructional occurrences imported and 276 decorative occurrences omitted. Every imported image audit record resolves to an image actually emitted in the corresponding reading. The validator also checks asset decoding, duplicate dispositions, missing original block IDs, and publisher/source-reference leakage.

## Why the earlier coverage checks were insufficient

The 88 generic deep lessons had 130 module sections and only 263 explanatory paragraphs: 127 sections contained exactly two paragraphs. They provided 23,352 explanatory words compared with 236,978 source teaching words for those same readings. Seventy-two source learning outcomes were not mapped to a deep-lesson assessment. These measurements identify compression and assessment gaps; word count alone is not a completeness test. Five specialist lessons were excluded from that comparison.

Representative substantive gaps before the full-content import:

| Reading | Previously compressed or missing knowledge |
| --- | --- |
| 2, Time Value of Money | Financial-calculator setup and sign conventions; continuous discounting; negative yields; loan-payment calculation; preferred-stock valuation; multistage dividend calculations and terminal-value timing; numerical coupon-yield solving; cash-flow decomposition; forward-FX arbitrage mechanics. The source has 12 named examples; the former lesson had three worked examples and no assessment of outcome 2.c. |
| 12, Market Structures | Twelve source figures explain shutdown/breakeven, costs, scale, and market behavior. Short prose summaries did not preserve those graphical arguments. |
| 32, Inventories | Detailed lower-of-cost/market treatment, framework exceptions, write-down/recovery calculations, cost-flow diagrams, and inventory-ratio cases exceeded the six existing explanatory paragraphs. |
| 52, Bond Prices and Yields | Accrued-interest day-count conventions, between-coupon valuation, pull-to-par figures, and matrix/spread-interpolation calculations were reduced to two paragraphs and one worked example. |
| 90, Code and Standards | The exact code commitments, standards structure, and conduct-process detail were reduced to a short overview. |
| 93, Ethics Application | The original teaching contains 37 concrete cases; the earlier summary and single worked case could not substitute for that application range. |

## Boundary and extraction decisions

Original chapters begin at their large `READING N` heading, not at the first module. This preserves introductory/warm-up material. Readings 83 and 84 have heading-only first pages; their body starts on the next page. A chapter ends before the next actual chapter. The final chapter ends at source 1 page 281, source 2 page 361, source 3 page 226, and source 4 page 209.

Instructional references are source 1 pages 283-294, source 2 pages 363-368, source 3 pages 228-233, and source 4 pages 210-211. Front matter, indexes, repeated contents, and external-platform topic-quiz advertisements are not learning content. An external quiz notice shares reading 93's last instructional page, so the notice is removed at block level rather than dropping that page.

The Markdown conversions contain 9,617 replacement characters and 915 OCR picture-text blocks with no original image links. The cleaner text extracts still omit image-based mathematics. Neither representation alone can preserve the supplied knowledge reliably; the original PDFs are the authoritative import input.

Sorting PDF text blocks independently broke sentences interrupted by inline equations. `pdf_inline_regions.py` groups vertically connected text and mathematical fragments before conversion so their reading order remains intact. The post-processing pass converts mathematical regions to KaTeX, keeps captioned diagrams and charts, keeps the statistical reference tables, and rebuilds compact answer tables as selectable text. `docs/math-visual-classification.json` records the disposition and original source block IDs for every visual asset.

One known source error was corrected explicitly: unbiased sample variance does not imply unbiased sample standard deviation. The reading 3 replacement states the IID finite-variance condition, the n-1 variance result, and the generally downward-biased square root. The audit records the original sentence, replacement, and reason. No claim is made that all source calculations were independently verified.

## Reproducing the check

Run `scripts/validate-full-readings.py` with the bundled Python runtime and PyMuPDF. It reads the original PDFs and writes the independent inventory to `work/full-reading-source-inventory.json`. Use `--reuse-inventory` for subsequent content checks. `--inventory-only` generates source evidence without requiring an import. The result is saved to `work/full-reading-validation.json`.

`docs/full-reading-import-audit.json` retains the original block-to-output dispositions and source hashes; none of these internal source references belongs in the student interface. Build-integrated content checks verify all 365 learner-facing outcome questions, all 565 structured quiz questions, every KaTeX expression, and the complete visual classification through `npm run validate:full`.
