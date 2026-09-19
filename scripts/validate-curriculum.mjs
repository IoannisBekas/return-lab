import { readFileSync } from "node:fs";

const curriculum = JSON.parse(
  readFileSync(new URL("../src/data/curriculum.json", import.meta.url), "utf8"),
);

const expected = Array.from({ length: 93 }, (_, index) => index + 1);
const actual = curriculum.map((reading) => reading.number);
const missing = expected.filter((number) => !actual.includes(number));
const duplicate = actual.filter((number, index) => actual.indexOf(number) !== index);
const emptyModules = curriculum.filter((reading) => !reading.modules?.length);
const emptyTeaching = curriculum.flatMap((reading) =>
  reading.modules.filter(
    (module) =>
      !module.title ||
      !module.explanation ||
      module.steps?.length < 3 ||
      !module.check,
  ),
);

if (
  curriculum.length !== 93 ||
  missing.length ||
  duplicate.length ||
  emptyModules.length ||
  emptyTeaching.length
) {
  console.error({
    readings: curriculum.length,
    missing,
    duplicate,
    emptyModules: emptyModules.map((reading) => reading.number),
    emptyTeaching: emptyTeaching.length,
  });
  process.exit(1);
}

console.log(
  `Validated ${curriculum.length} readings and ${curriculum.reduce((sum, reading) => sum + reading.modules.length, 0)} taught modules.`,
);
