import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";

const sourceUrl = new URL("../src/data/curriculum.json", import.meta.url);
const outputUrl = new URL("../src/data/readings/", import.meta.url);
const manifestUrl = new URL("../src/data/manifest.json", import.meta.url);
const curriculum = JSON.parse(readFileSync(sourceUrl, "utf8"));

rmSync(outputUrl, { force: true, recursive: true });
mkdirSync(outputUrl, { recursive: true });

const manifest = curriculum.map((reading) => {
  const filename = `${String(reading.number).padStart(3, "0")}.json`;
  writeFileSync(new URL(filename, outputUrl), `${JSON.stringify(reading, null, 2)}\n`);

  return {
    number: reading.number,
    slug: reading.slug,
    title: reading.title,
    topic: reading.topic,
    overview: reading.overview,
    example: reading.example,
    chapterQuestionCount: reading.chapterQuestionCount,
    modules: reading.modules.map(({ id, title }) => ({ id, title })),
  };
});

writeFileSync(manifestUrl, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`Split ${curriculum.length} readings into lazy-loadable course files.`);
