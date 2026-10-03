import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import katex from "katex";
import { FLASHCARDS, filterReferenceSections, getReferenceDueCount, isReferenceCardDue, rateReferenceCard, readReferenceReviews, type ReferenceContent } from "../src/components/learning/referenceStudy";

const reference: ReferenceContent = JSON.parse(readFileSync("public/content/reference.json", "utf8"));
const results = (term: string, topic: string) => filterReferenceSections(reference, term, topic).flatMap((section) =>
  section.entries.map((entry) => ({ entry, blocks: section.blocks.slice(entry.start, entry.end) })));
for (const section of reference.sections) {
  assert.equal(section.entries[0].start, 0);
  assert.equal(section.entries.at(-1)?.end, section.blocks.length);
  for (const [index, entry] of section.entries.entries()) {
    assert.equal(entry.start, index ? section.entries[index - 1].end : 0, "Every reference block belongs to a complete entry");
    assert(entry.end > entry.start && entry.categories.length > 0);
    assert(/^#\/reading\/\d+\/section\/full-module-\d+\.\d+$/.test(entry.lessonHref));
  }
}
assert(results("", "Corporate Issuers").some(({ blocks }) => blocks.some((block) => block.type === "math")));
assert(results("WACC", "Corporate Issuers").some(({ blocks }) => blocks.some((block) => block.latex?.includes("WACC"))));
assert(results("DuPont", "Financial Statement Analysis").some(({ blocks }) => blocks.some((block) => block.latex?.includes("ROE"))));
assert.equal(results("duration", "Economics").length, 0, "Topic and query must both apply");
assert.equal(results("WACC", "Economics").length, 0);
const duration = results("duration", "Fixed Income");
assert(duration.some(({ blocks }) => blocks.some((block) => block.latex?.includes("YTM/2"))), "Semiannual duration keeps its equation");
assert(duration.some(({ blocks }) => blocks.some((block) => block.text?.includes("decimal"))), "Duration search keeps its assumptions");
assert(results("parity", "Derivatives").some(({ blocks }) => blocks.some((block) => block.text?.includes("European"))), "Parity keeps option conditions");
for (const card of FLASHCARDS) katex.renderToString(card.latex, { throwOnError: true, strict: "ignore" });

const now = 1_000_000;
const DAY = 86_400_000;
const id = FLASHCARDS[0].id;
assert(isReferenceCardDue({}, id, now));
const again = rateReferenceCard({}, id, "again", now);
assert.equal(again[id].dueAt, now + 600_000);
assert(!isReferenceCardDue(again, id, now));
assert(isReferenceCardDue(again, id, now + 600_000));
const hard = rateReferenceCard(again, id, "hard", now);
assert.equal(hard[id].dueAt, now + DAY);
const good = rateReferenceCard({}, id, "good", now);
assert.equal(good[id].dueAt, now + 3 * DAY);
const secondGood = rateReferenceCard(good, id, "good", now + 3 * DAY);
assert.equal(secondGood[id].intervalDays, 6);
assert.equal(secondGood[id].reviews, 2);
assert.equal(rateReferenceCard({ [id]: { ...good[id], intervalDays: 40 } }, id, "good", now)[id].intervalDays, 60);

const values = new Map<string, string>();
Object.defineProperty(globalThis, "localStorage", { value: { getItem: (key: string) => values.get(key) ?? null, setItem: (key: string, value: string) => values.set(key, value) }, configurable: true });
values.set("return-lab-mastered-flashcards-v1", JSON.stringify([id]));
const migrated = readReferenceReviews(now);
assert.equal(migrated[id].dueAt, now + 7 * DAY);
assert.equal(readReferenceReviews(now + DAY)[id].dueAt, now + 7 * DAY, "Migration due date must remain fixed");
assert.equal(getReferenceDueCount(now), FLASHCARDS.length - 1);
assert.equal(getReferenceDueCount(now + 7 * DAY), FLASHCARDS.length);
values.set("return-lab-reference-reviews-v1", JSON.stringify({ broken: { dueAt: "tomorrow" }, [id]: good[id] }));
assert.deepEqual(readReferenceReviews(now), good, "Ignore malformed stored review records");
values.set("return-lab-reference-reviews-v1", "invalid-json");
assert.deepEqual(readReferenceReviews(now), {});
console.log(`Reference regression passed: ${reference.sections.reduce((count, section) => count + section.entries.length, 0)} complete entries, category/search conjunction, formula conditions, ${FLASHCARDS.length} KaTeX flashcards, review intervals, and migration.`);
