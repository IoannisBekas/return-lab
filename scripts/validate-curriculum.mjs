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
      !module.check ||
      module.objectives?.length < 3 ||
      module.lesson?.length < 3 ||
      module.keyTerms?.length < 4 ||
      !module.formula?.expression ||
      !module.workedExample?.result ||
      module.mistakes?.length < 3 ||
      module.questions?.length < 3 ||
      module.questions.some(
        (question) =>
          question.choices?.length < 4 ||
          question.correct < 0 ||
          question.correct >= question.choices.length ||
          !question.explanation,
      ) ||
      module.summary?.length < 3,
  ),
);
const questionCount = curriculum.reduce(
  (total, reading) =>
    total + reading.modules.reduce((sum, module) => sum + module.questions.length, 0),
  0,
);

if (
  curriculum.length !== 93 ||
  missing.length ||
  duplicate.length ||
  emptyModules.length ||
  emptyTeaching.length ||
  questionCount !== 456
) {
  console.error({
    readings: curriculum.length,
    missing,
    duplicate,
    emptyModules: emptyModules.map((reading) => reading.number),
    emptyTeaching: emptyTeaching.length,
    questionCount,
  });
  process.exit(1);
}

console.log(
  `Validated ${curriculum.length} chapters, ${curriculum.reduce((sum, reading) => sum + reading.modules.length, 0)} complete modules, and ${questionCount} original practice questions.`,
);
