import { useEffect, useMemo, useState } from "react";
import {
  goldDecisionLessonsByReading,
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
import {
  CashFlowTimeline,
  DurationPriceCurve,
  EfficientFrontier,
  EthicsDecisionFlow,
} from "./FinanceVisuals";
import { MathText } from "./MathText";
import "./GoldLesson.css";

const quantLessonsByReading = new Map(
  goldQuantLessons.map((lesson) => [lesson.readingId, lesson]),
);
const decisionLessonsByReading = new Map<number, DecisionLessonDetail>(
  goldDecisionLessonDetails.map((lesson) => [lesson.readingId, lesson]),
);

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
  return null;
}

function SourceRefs({ lesson }: { lesson: GoldQuantLesson | DecisionLessonDetail }) {
  return (
    <details className="gold-sources">
      <summary>Source map and verification scope</summary>
      <ul>
        {lesson.sourceRefs.map((source, index) => (
          <li key={`${source.book}-${index}`}>
            {"pdfPage" in source ? (
              <>
                <strong>Book {source.book}, PDF page {source.pdfPage}</strong>
                <span>{source.heading}</span>
              </>
            ) : (
              <>
                <strong>Book {source.book}: {source.locator}</strong>
                <span>Outcomes {source.outcomeIds.join(", ")} · modules {source.moduleIds.join(", ")}</span>
              </>
            )}
          </li>
        ))}
      </ul>
      <p>
        Source pages were used to verify concepts, notation, and scope. The teaching copy, examples, visuals, and questions on this page are original.
      </p>
    </details>
  );
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
      return JSON.parse(localStorage.getItem(storageKey) || "{}");
    } catch {
      return {};
    }
  });

  useEffect(() => {
    localStorage.setItem(storageKey, JSON.stringify(answers));
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
        return (
          <article className="gold-question" key={item.id}>
            <p className="gold-question-meta">OBJECTIVE {item.objective}{item.skill ? ` · ${item.skill.toUpperCase()}` : ""}</p>
            <h3><span>{itemIndex + 1}</span>{item.prompt}</h3>
            <div className="gold-options">
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

function QuantLesson({ lesson }: { lesson: GoldQuantLesson }) {
  return (
    <section className="gold-lesson" id="deep-dive">
      <header className="gold-intro">
        <div><span className="gold-badge">SOURCE-VERIFIED DEEP LESSON</span><h2>{lesson.title}</h2></div>
        <p>Every objective below is connected to explanation, formal notation, assumptions, a worked application, misconceptions, and assessment.</p>
      </header>
      <section className="gold-objectives">
        <span className="section-code">YOU WILL BE ABLE TO</span>
        <ol>{lesson.objectives.map((objective) => <li key={objective.id}><strong>{objective.id}</strong><span>{objective.description}</span></li>)}</ol>
      </section>
      <SourceRefs lesson={lesson} />
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
  const sourceMappedLesson = goldDecisionLessonsByReading.get(lesson.readingId);
  return (
    <section className="gold-lesson" id="deep-dive">
      <header className="gold-intro">
        <div><span className="gold-badge">SOURCE-VERIFIED DEEP LESSON</span><h2>{lesson.title}</h2></div>
        <p>Use the frameworks to separate facts, classifications, judgments, and effects before choosing an answer.</p>
      </header>
      <section className="gold-objectives"><span className="section-code">YOU WILL BE ABLE TO</span><ol>{lesson.objectives.map((objective) => <li key={objective.id}><strong>{objective.id}</strong><span>{objective.text}</span></li>)}</ol></section>
      {sourceMappedLesson ? <SourceRefs lesson={sourceMappedLesson} /> : null}
      <div className="gold-explanations">
        {lesson.explanatorySections.map((section) => (
          <article key={section.moduleId}>
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

export default function GoldLesson({ readingId }: { readingId: number }) {
  const quant = useMemo(() => quantLessonsByReading.get(readingId), [readingId]);
  if (quant) return <QuantLesson lesson={quant} />;
  const decision = decisionLessonsByReading.get(readingId);
  if (decision) return <DecisionLesson lesson={decision} />;
  return null;
}
