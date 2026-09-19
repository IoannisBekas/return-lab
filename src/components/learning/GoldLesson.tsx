import { useEffect, useMemo, useState } from "react";
import {
  goldDecisionLessonDetails,
  type AssessmentItem,
  type DecisionLessonDetail,
  type LessonFormula,
} from "../../data/goldDecisionLessons";
import {
  goldQuantLessons,
  type GoldAssessment,
  type GoldFormula,
  type GoldLesson as GoldQuantLesson,
} from "../../data/goldQuantLessons";
import sourceManifestData from "../../data/sourceManifest.json";
import objectiveQuestionsData from "../../data/objectiveQuestions.json";
import type {
  DeepAssessment,
  DeepLesson,
  DeepWorkedExample,
} from "../../data/deepLessonTypes";
import {
  CashFlowBridge,
  CashFlowTimeline,
  DurationPriceCurve,
  EfficientFrontier,
  EthicsDecisionFlow,
  OptionPayoffExplorer,
  SupplyDemandExplorer,
} from "./FinanceVisuals";
import { MathText } from "./MathText";
import "./GoldLesson.css";

const quantLessonsByReading = new Map(
  goldQuantLessons.map((lesson) => [lesson.readingId, lesson]),
);
const decisionLessonsByReading = new Map<number, DecisionLessonDetail>(
  goldDecisionLessonDetails.map((lesson) => [lesson.readingId, lesson]),
);

type SourceManifestEntry = {
  readingId: number;
  objectives: { id: string; sourceStatement: string }[];
};

type DeepDataModule = Record<string, DeepLesson[]>;

const sourceManifest = sourceManifestData as SourceManifestEntry[];
const objectiveQuestions = new Map((objectiveQuestionsData as { id: string; question: string }[]).map((item) => [item.id, item.question]));
const deepDataLoaders = import.meta.glob<DeepDataModule>("../../data/deep/*.ts");

function deepDataPath(readingId: number) {
  if (readingId >= 2 && readingId <= 11) return "../../data/deep/quantitative.ts";
  if (readingId >= 12 && readingId <= 19) return "../../data/deep/economics.ts";
  if (readingId >= 20 && readingId <= 26) return "../../data/deep/corporate.ts";
  if (readingId === 27 || (readingId >= 29 && readingId <= 38)) return "../../data/deep/financialStatements.ts";
  if (readingId >= 39 && readingId <= 46) return "../../data/deep/equity.ts";
  if (readingId >= 47 && readingId <= 65 && readingId !== 57) return "../../data/deep/fixedIncome.ts";
  if (readingId >= 66 && readingId <= 75) return "../../data/deep/derivatives.ts";
  if (readingId >= 76 && readingId <= 82) return "../../data/deep/alternatives.ts";
  if ((readingId >= 84 && readingId <= 90) || readingId === 92 || readingId === 93) return "../../data/deep/portfolioEthics.ts";
  return null;
}

async function loadUniversalLesson(readingId: number) {
  const path = deepDataPath(readingId);
  const loader = path ? deepDataLoaders[path] : undefined;
  if (!loader) throw new Error(`Deep lesson data for reading ${readingId} is not available.`);
  const module = await loader();
  const lessons = Object.values(module).find((value) => Array.isArray(value));
  const lesson = lessons?.find((candidate) => candidate.readingId === readingId);
  if (!lesson) throw new Error(`Deep lesson ${readingId} is missing from ${path}.`);
  return lesson;
}

type AssessmentView = {
  id: string;
  objective: string;
  skill?: string;
  prompt: string;
  options: { id: string; text: string; feedback: string }[];
  correctOptionId: string;
  solution: string[];
};

export const goldReadingIds = [1, 28, 57, 83, 91] as const;

export function hasGoldLesson(readingId: number) {
  return quantLessonsByReading.has(readingId) || decisionLessonsByReading.has(readingId);
}

function visualFor(readingId: number) {
  if (readingId === 1) {
    return (
      <CashFlowTimeline
        flows={[
          { period: 0, amount: -1000, label: "Initial contribution" },
          { period: 1, amount: -900, label: "Additional contribution" },
          { period: 2, amount: 1800, label: "Final portfolio value" },
        ]}
        title="Investor cash flows for money-weighted return"
      />
    );
  }
  if (readingId === 57) return <DurationPriceCurve />;
  if (readingId === 83) return <EfficientFrontier />;
  if (readingId === 91) return <EthicsDecisionFlow />;
  if ([2, 24, 46, 52, 69, 70, 77].includes(readingId)) return <CashFlowTimeline />;
  if ([12, 13, 14, 15, 17, 18, 19].includes(readingId)) return <SupplyDemandExplorer />;
  if ([27, 28, 30, 31, 36, 37, 38].includes(readingId)) return <CashFlowBridge />;
  if ([56, 58, 59].includes(readingId)) return <DurationPriceCurve />;
  if ([73, 74, 75].includes(readingId)) return <OptionPayoffExplorer />;
  if ([84, 86, 88].includes(readingId)) return <EfficientFrontier />;
  if ([89, 90, 92, 93].includes(readingId)) return <EthicsDecisionFlow />;
  return null;
}

function QuantFormulaCard({ formula }: { formula: GoldFormula }) {
  return (
    <article className="gold-formula-card">
      <header>
        <span>FORMULA · {formula.id}</span>
        <h3>{formula.title}</h3>
      </header>
      <MathText display latex={formula.latex} />
      <p className="gold-formula-meaning">{formula.interpretation}</p>
      <div className="gold-table-scroll" tabIndex={0} role="region" aria-label={`${formula.title} variables`}>
        <table>
          <caption>Variables and units</caption>
          <thead><tr><th scope="col">Symbol</th><th scope="col">Meaning</th><th scope="col">Unit</th></tr></thead>
          <tbody>
            {formula.variables.map((variable) => (
              <tr key={`${formula.id}-${variable.symbol}`}>
                <th scope="row"><MathText latex={variable.symbol} /></th>
                <td>{variable.meaning}</td>
                <td>{variable.unit}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="gold-formula-conditions">
        <div><strong>Valid domain</strong><p>{formula.domain}</p></div>
        <div><strong>Assumptions</strong><ul>{formula.assumptions.map((item) => <li key={item}>{item}</li>)}</ul></div>
      </div>
    </article>
  );
}

function DecisionFormulaCard({ formula }: { formula: LessonFormula }) {
  return (
    <article className="gold-formula-card">
      <header><span>DECISION FORMULA</span><h3>{formula.name}</h3></header>
      <MathText display latex={formula.latex} />
      <p className="gold-formula-meaning">{formula.interpretation}</p>
      <div className="gold-table-scroll" tabIndex={0} role="region" aria-label={`${formula.name} variables`}>
        <table>
          <caption>Variables and units</caption>
          <thead><tr><th scope="col">Symbol</th><th scope="col">Meaning</th><th scope="col">Unit</th></tr></thead>
          <tbody>{formula.variables.map((variable) => <tr key={`${formula.name}-${variable.symbol}`}><th scope="row"><MathText latex={variable.symbol} /></th><td>{variable.meaning}</td><td>{variable.unit || "context dependent"}</td></tr>)}</tbody>
        </table>
      </div>
      <div className="gold-formula-conditions"><div><strong>Conditions</strong><ul>{formula.conditions.map((item) => <li key={item}>{item}</li>)}</ul></div></div>
    </article>
  );
}

function QuantWorkedExample({ example }: { example: GoldQuantLesson["workedExamples"][number] }) {
  return (
    <article className="gold-worked-example">
      <header><span>WORKED EXAMPLE · {example.id}</span><h3>{example.title}</h3></header>
      <div className="gold-example-brief">
        <section><strong>Given</strong><ul>{example.given.map((item) => <li key={item}>{item}</li>)}</ul></section>
        <section><strong>Find</strong><p>{example.find}</p></section>
        <section><strong>Plan</strong><p>{example.plan}</p></section>
      </div>
      <ol className="gold-calculation-steps">
        {example.calculate.map((step, index) => (
          <li key={`${example.id}-${index}`}>
            <div><span>{index + 1}</span><strong>{step.description}</strong></div>
            <MathText display latex={step.latex} />
            <p>{step.result}</p>
          </li>
        ))}
      </ol>
      <div className="gold-example-close">
        <section><strong>Interpret</strong><p>{example.interpret}</p></section>
        <section><strong>Sanity check</strong><p>{example.sanityCheck}</p></section>
      </div>
    </article>
  );
}

function AssessmentSet({ readingId, items }: { readingId: number; items: AssessmentView[] }) {
  const storageKey = `return-lab-assessments-v1-${readingId}`;
  const [answers, setAnswers] = useState<Record<string, { selected: string; checked: boolean }>>(() => {
    try {
      const stored: unknown = JSON.parse(localStorage.getItem(storageKey) || "{}");
      if (!stored || typeof stored !== "object" || Array.isArray(stored)) return {};
      const valid: Record<string, { selected: string; checked: boolean }> = {};
      for (const item of items) {
        const candidate = (stored as Record<string, unknown>)[item.id];
        if (!candidate || typeof candidate !== "object" || Array.isArray(candidate)) continue;
        const selected = (candidate as Record<string, unknown>).selected;
        const checked = (candidate as Record<string, unknown>).checked;
        if (typeof selected === "string" && typeof checked === "boolean" && item.options.some((option) => option.id === selected)) {
          valid[item.id] = { selected, checked };
        }
      }
      return valid;
    } catch {
      return {};
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(answers));
    } catch {
      // Assessments remain usable if browser storage is unavailable.
    }
  }, [answers, storageKey]);

  const score = items.filter((item) => answers[item.id]?.checked && answers[item.id]?.selected === item.correctOptionId).length;
  const attempted = items.filter((item) => answers[item.id]?.checked).length;

  return (
    <section className="gold-assessments" id="deep-assessment">
      <header>
        <div><span className="section-code">APPLICATION CHECK</span><h2>Test the decision, not the wording.</h2></div>
        <strong>{score}/{items.length} correct · {attempted}/{items.length} checked</strong>
      </header>
      <div className="gold-mastery-bar" aria-label={`${score} of ${items.length} questions correct`}><span style={{ width: `${score / items.length * 100}%` }} /></div>
      {items.map((item, itemIndex) => {
        const answer = answers[item.id];
        const selectedOption = item.options.find((option) => option.id === answer?.selected);
        const correct = answer?.selected === item.correctOptionId;
        const promptId = `${item.id}-prompt`;
        return (
          <article className="gold-question" key={item.id}>
            <p className="gold-question-meta">QUESTION {itemIndex + 1}{item.skill ? ` · ${item.skill.toUpperCase()}` : ""}</p>
            <h3 id={promptId}><span>{itemIndex + 1}</span>{item.prompt}</h3>
            <div aria-labelledby={promptId} className="gold-options" role="radiogroup">
              {item.options.map((option) => (
                <label className={answer?.selected === option.id ? "selected" : ""} key={option.id}>
                  <input
                    checked={answer?.selected === option.id}
                    name={`${item.id}-answer`}
                    onChange={() => setAnswers((current) => ({ ...current, [item.id]: { selected: option.id, checked: false } }))}
                    type="radio"
                  />
                  <span>{option.id}</span>
                  <span>{option.text}</span>
                </label>
              ))}
            </div>
            <button
              disabled={!answer?.selected}
              onClick={() => setAnswers((current) => ({ ...current, [item.id]: { ...current[item.id], checked: true } }))}
              type="button"
            >
              Check answer
            </button>
            {answer?.checked && selectedOption ? (
              <div className={correct ? "gold-feedback correct" : "gold-feedback"} role="status">
                <strong>{correct ? "Correct" : `Review the ${item.correctOptionId} option`}</strong>
                <p>{selectedOption.feedback}</p>
                <details><summary>Show the complete reasoning</summary><ol>{item.solution.map((step) => <li key={step}>{step}</li>)}</ol></details>
              </div>
            ) : null}
          </article>
        );
      })}
    </section>
  );
}

function quantAssessments(items: GoldAssessment[]): AssessmentView[] {
  return items.map((item) => ({
    id: item.id,
    objective: item.objectiveId,
    prompt: item.prompt,
    options: item.options,
    correctOptionId: item.correctOptionId,
    solution: [item.solution],
  }));
}

function decisionAssessments(items: AssessmentItem[]): AssessmentView[] {
  return items.map((item) => ({
    id: item.id,
    objective: item.objectiveIds.join(", "),
    skill: item.skill,
    prompt: item.prompt,
    options: item.options,
    correctOptionId: item.correctOptionId,
    solution: item.solution,
  }));
}

function deepAssessments(items: DeepAssessment[]): AssessmentView[] {
  return items.map((item) => ({
    id: item.id,
    objective: item.objectiveIds.join(", "),
    skill: item.skill,
    prompt: item.prompt,
    options: item.options,
    correctOptionId: item.correctOptionId,
    solution: item.solution,
  }));
}

function QuantLesson({ lesson }: { lesson: GoldQuantLesson }) {
  return (
    <section className="gold-lesson" id="deep-dive">
      <header className="gold-intro">
        <div><span className="gold-badge">GUIDED EXAMPLES AND PRACTICE</span><h2>{lesson.title}</h2></div>
        <p>Learn the concepts and notation, follow the worked examples, and check your understanding with guided practice.</p>
      </header>
      <section className="gold-objectives">
        <span className="section-code">QUESTIONS THIS LESSON ANSWERS</span>
        <ol>{lesson.objectives.map((objective) => <li key={objective.id}><span>{objectiveQuestions.get(objective.id) || objective.description}</span></li>)}</ol>
      </section>
      <div className="gold-explanations">
        {lesson.sections.map((section, index) => <article key={section.heading}><span>{String(index + 1).padStart(2, "0")}</span><div><h3>{section.heading}</h3>{section.body.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}</div></article>)}
      </div>
      {visualFor(lesson.readingId)}
      <section className="gold-formulas"><div className="gold-section-heading"><span className="section-code">FORMULA LAB</span><h2>Read the notation and its limits.</h2></div>{lesson.formulas.map((formula) => <QuantFormulaCard formula={formula} key={formula.id} />)}</section>
      <section className="gold-examples"><div className="gold-section-heading"><span className="section-code">GUIDED PRACTICE</span><h2>Make every step auditable.</h2></div>{lesson.workedExamples.map((example) => <QuantWorkedExample example={example} key={example.id} />)}</section>
      <Misconceptions items={lesson.misconceptions} />
      <AssessmentSet items={quantAssessments(lesson.assessments)} readingId={lesson.readingId} />
    </section>
  );
}

function Misconceptions({ items }: { items: { claim: string; correction: string; diagnostic?: string }[] }) {
  return (
    <section className="gold-misconceptions">
      <div className="gold-section-heading"><span className="section-code">COMMON TRAPS</span><h2>Diagnose the tempting wrong idea.</h2></div>
      <div>{items.map((item) => <article key={item.claim}><h3>{item.claim}</h3><p>{item.correction}</p>{item.diagnostic ? <small>{item.diagnostic}</small> : null}</article>)}</div>
    </section>
  );
}

function DecisionLesson({ lesson }: { lesson: DecisionLessonDetail }) {
  return (
    <section className="gold-lesson" id="deep-dive">
      <header className="gold-intro">
        <div><span className="gold-badge">GUIDED EXAMPLES AND PRACTICE</span><h2>{lesson.title}</h2></div>
        <p>Use the frameworks to separate facts, classifications, judgments, and effects before choosing an answer.</p>
      </header>
      <section className="gold-objectives"><span className="section-code">QUESTIONS THIS LESSON ANSWERS</span><ol>{lesson.objectives.map((objective) => <li key={objective.id}><span>{objectiveQuestions.get(objective.id) || objective.text}</span></li>)}</ol></section>
      <div className="gold-explanations">
        {lesson.explanatorySections.map((section) => (
          <article id={`deep-module-${section.moduleId}`} key={section.moduleId}>
            <span>{section.moduleId}</span>
            <div><h3>{section.title}</h3><p className="gold-lead">{section.lead}</p>{section.paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}<ul>{section.keyPoints.map((point) => <li key={point}>{point}</li>)}</ul>{section.miniExample ? <aside><strong>{section.miniExample.title}</strong><p>{section.miniExample.setup}</p><ol>{section.miniExample.walkthrough.map((step) => <li key={step}>{step}</li>)}</ol><p>{section.miniExample.takeaway}</p></aside> : null}</div>
          </article>
        ))}
      </div>
      {visualFor(lesson.readingId)}
      <section className="gold-frameworks">
        <div className="gold-section-heading"><span className="section-code">DECISION FRAMEWORKS</span><h2>Follow a repeatable path.</h2></div>
        {lesson.decisionFrameworks.map((framework) => <article key={framework.id}><header><span>{framework.kind}</span><h3>{framework.title}</h3><p>{framework.purpose}</p></header><ol>{framework.steps.map((step) => <li key={step}>{step}</li>)}</ol>{framework.formulas.map((formula) => <DecisionFormulaCard formula={formula} key={formula.name} />)}</article>)}
      </section>
      <section className="gold-comparisons">
        <div className="gold-section-heading"><span className="section-code">COMPARISON TABLES</span><h2>Keep similar cases distinct.</h2></div>
        {lesson.comparisonTables.map((table) => <div className="gold-table-scroll" tabIndex={0} role="region" aria-label={table.title} key={table.id}><table><caption><strong>{table.title}</strong><span>{table.caption}</span></caption><thead><tr>{table.columns.map((column) => <th scope="col" key={column}>{column}</th>)}</tr></thead><tbody>{table.rows.map((row, rowIndex) => <tr key={`${table.id}-${rowIndex}`}>{row.map((cell, cellIndex) => cellIndex === 0 ? <th scope="row" key={cellIndex}>{cell}</th> : <td key={cellIndex}>{cell}</td>)}</tr>)}</tbody></table></div>)}
      </section>
      <section className="gold-worked-example gold-decision-case">
        <header><span>INTEGRATED DECISION CASE</span><h3>{lesson.workedDecisionCase.title}</h3></header>
        <div className="gold-case-grid"><CaseList title="Given" items={lesson.workedDecisionCase.given} /><CaseList title="Find" items={lesson.workedDecisionCase.find} /><CaseList title="Plan" items={lesson.workedDecisionCase.plan} /><CaseList title="Analysis" items={lesson.workedDecisionCase.analysis} /><CaseList title="Decision" items={lesson.workedDecisionCase.decision} /><CaseList title="Sanity check" items={lesson.workedDecisionCase.sanityCheck} /></div>
      </section>
      <Misconceptions items={lesson.misconceptions} />
      <AssessmentSet items={decisionAssessments(lesson.assessments)} readingId={lesson.readingId} />
    </section>
  );
}

function CaseList({ title, items }: { title: string; items: string[] }) {
  return <section><strong>{title}</strong><ol>{items.map((item) => <li key={item}>{item}</li>)}</ol></section>;
}

function LearningMap({ lesson }: { lesson: DeepLesson }) {
  return (
    <section className="gold-learning-map" aria-labelledby={`learning-map-${lesson.readingId}`}>
      <div className="gold-section-heading">
        <span className="section-code">CONCEPT MAP</span>
        <h2 id={`learning-map-${lesson.readingId}`}>Follow the reading from idea to decision.</h2>
      </div>
      <div className="gold-learning-map-track">
        {lesson.sections.map((section, index) => (
          <article key={section.moduleId}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <small>{section.moduleId}</small>
            <h3>{section.title}</h3>
            <p>{section.lead}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function DeepWorkedExampleCard({ example }: { example: DeepWorkedExample }) {
  return (
    <article className="gold-worked-example">
      <header><span>WORKED EXAMPLE · {example.moduleIds.join(" + ")}</span><h3>{example.title}</h3></header>
      <div className="gold-example-brief">
        <section><strong>Given</strong><ul>{example.given.map((item) => <li key={item}>{item}</li>)}</ul></section>
        <section><strong>Find</strong><p>{example.find}</p></section>
        <section><strong>Plan</strong><p>{example.plan}</p></section>
      </div>
      <ol className="gold-calculation-steps">
        {example.steps.map((step, index) => (
          <li key={`${example.id}-${index}`}>
            <div><span>{index + 1}</span><strong>{step.label}</strong></div>
            {step.latex ? <MathText display latex={step.latex} /> : null}
            <p>{step.result}</p>
          </li>
        ))}
      </ol>
      <div className="gold-example-close">
        <section><strong>Interpret</strong><p>{example.interpret}</p></section>
        <section><strong>Sanity check</strong><p>{example.sanityCheck}</p></section>
      </div>
    </article>
  );
}

function UniversalLesson({ readingId }: { readingId: number }) {
  const [lesson, setLesson] = useState<DeepLesson | null>(null);
  const [error, setError] = useState("");
  const sourceEntries = useMemo(
    () => sourceManifest.filter((entry) => entry.readingId === readingId),
    [readingId],
  );

  useEffect(() => {
    let active = true;
    setLesson(null);
    setError("");
    void loadUniversalLesson(readingId)
      .then((loadedLesson) => {
        if (active) setLesson(loadedLesson);
      })
      .catch((reason: unknown) => {
        if (active) setError(reason instanceof Error ? reason.message : "The deep lesson could not be loaded.");
      });
    return () => {
      active = false;
    };
  }, [readingId]);

  useEffect(() => {
    if (!lesson) return;
    const match = window.location.hash.match(/\/section\/([^/?#]+)/);
    if (!match) return;
    window.requestAnimationFrame(() => {
      document.getElementById(decodeURIComponent(match[1]))?.scrollIntoView({ behavior: "smooth" });
    });
  }, [lesson]);

  if (error) return (
    <section className="deep-lesson-error" role="alert">
      <strong>The lesson data could not be loaded.</strong>
      <p>{error}</p>
      <button type="button" onClick={() => window.location.reload()}>Retry lesson</button>
    </section>
  );
  if (!lesson) return <p className="deep-lesson-loading" aria-live="polite">Loading the lesson…</p>;

  const objectives = sourceEntries.flatMap((entry) => entry.objectives);

  return (
    <section className="gold-lesson" id="deep-dive">
      <header className="gold-intro">
        <div><span className="gold-badge">GUIDED EXAMPLES AND PRACTICE</span><h2>{lesson.title}</h2></div>
        <p>Build your understanding one concept at a time, follow worked examples, and test how you would apply each method.</p>
      </header>
      <section className="gold-objectives">
        <span className="section-code">QUESTIONS THIS LESSON ANSWERS</span>
        <ol>{objectives.map((objective) => <li key={objective.id}><span>{objectiveQuestions.get(objective.id) || objective.sourceStatement}</span></li>)}</ol>
      </section>
      <LearningMap lesson={lesson} />
      <div className="gold-explanations">
        {lesson.sections.map((section, index) => (
          <article id={`deep-module-${section.moduleId}`} key={section.moduleId}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <div>
              <p className="gold-section-kicker">MODULE {section.moduleId}</p>
              <h3>{section.title}</h3>
              <p className="gold-lead">{section.lead}</p>
              {section.paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
              <ul>{section.keyPoints.map((point) => <li key={point}>{point}</li>)}</ul>
              {section.miniExample ? (
                <aside>
                  <strong>{section.miniExample.title}</strong>
                  <p>{section.miniExample.setup}</p>
                  <ol>{section.miniExample.walkthrough.map((step) => <li key={step}>{step}</li>)}</ol>
                  <p>{section.miniExample.takeaway}</p>
                </aside>
              ) : null}
            </div>
          </article>
        ))}
      </div>
      {visualFor(lesson.readingId)}
      {lesson.formulas.length ? (
        <section className="gold-formulas">
          <div className="gold-section-heading"><span className="section-code">FORMULA LAB</span><h2>Read the notation and its limits.</h2></div>
          {lesson.formulas.map((formula) => <QuantFormulaCard formula={formula} key={formula.id} />)}
        </section>
      ) : null}
      <section className="gold-examples">
        <div className="gold-section-heading"><span className="section-code">GUIDED PRACTICE</span><h2>Make every step auditable.</h2></div>
        {lesson.workedExamples.map((example) => <DeepWorkedExampleCard example={example} key={example.id} />)}
      </section>
      <Misconceptions items={lesson.misconceptions} />
      <AssessmentSet items={deepAssessments(lesson.assessments)} readingId={lesson.readingId} />
    </section>
  );
}

export default function GoldLesson({ readingId }: { readingId: number }) {
  const quant = useMemo(() => quantLessonsByReading.get(readingId), [readingId]);
  useEffect(() => {
    const match = window.location.hash.match(/\/section\/([^/?#]+)/);
    if (!match) return;
    window.requestAnimationFrame(() => {
      document.getElementById(decodeURIComponent(match[1]))?.scrollIntoView({ behavior: "smooth" });
    });
  }, [readingId]);
  if (quant) return <QuantLesson lesson={quant} />;
  const decision = decisionLessonsByReading.get(readingId);
  if (decision) return <DecisionLesson lesson={decision} />;
  return <UniversalLesson readingId={readingId} />;
}
