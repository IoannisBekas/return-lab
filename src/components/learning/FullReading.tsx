import { useEffect, useRef, useState } from "react";
import { MathText } from "./MathText";
import "./FullReading.css";

export type ContentBlock = {
  type: "paragraph" | "heading" | "question" | "image" | "math" | "worked-example";
  text?: string;
  prose?: string;
  latex?: string;
  display?: boolean;
  objectiveId?: string;
  level?: number;
  src?: string;
  alt?: string;
  width?: number;
  height?: number;
  visualKind?: string;
  sourceAsset?: string;
  title?: string;
  steps?: Array<{ title: string; body?: string[]; rows?: string[][]; equations?: string[] }>;
};

type QuizOption = { id: string; text: string };
type QuizQuestion = { id: string; number: number; objectiveIds: string[]; prompt: string; supportingBlocks: ContentBlock[]; options: QuizOption[]; correctOptionId: string; explanation: string; solutionBlocks: ContentBlock[] };
type QuizSet = { id: string; title: string; moduleId: string; questions: QuizQuestion[] };
type ReadingContent = { readingId: number; title: string; introduction?: ContentBlock[]; modules: { id: string; title: string; blocks: ContentBlock[] }[]; review: ContentBlock[]; quizSets: QuizSet[] };
type QuizAnswer = { selected?: string; checked: boolean; revealed?: boolean };

const asset = (path: string) => `${import.meta.env.BASE_URL}${path.replace(/^\//, "")}`;

export function ReadingBlocks({ blocks, onZoom, headingLevel = 4 }: { blocks: ContentBlock[]; onZoom: (block: ContentBlock) => void; headingLevel?: 3 | 4 }) {
  return blocks.map((block, index) => {
    if (block.type === "math" && block.latex) return <div className="full-reading-math" key={index}>{block.prose ? <p>{block.prose}</p> : null}<MathText display={block.display !== false} latex={block.latex} /></div>;
    if (block.type === "worked-example" && block.steps) return <section className="full-reading-worked" key={index}><h5>{block.title || "Worked example"}</h5>{block.steps.map((step, stepIndex) => <div className="full-reading-worked-step" key={stepIndex}><div className="full-reading-worked-number">{stepIndex + 1}</div><div><h6>{step.title}</h6>{step.body?.map((text) => <p key={text}>{text}</p>)}{step.rows?.length ? <div className="full-reading-worked-table" role="table">{step.rows.map((row, rowIndex) => <div className="full-reading-worked-row" role="row" key={rowIndex}>{row.map((cell, cellIndex) => <span role="cell" key={cellIndex}>{cell}</span>)}</div>)}</div> : null}{step.equations?.map((latex) => <div className="full-reading-worked-equation" key={latex}><MathText display latex={latex} /></div>)}</div></div>)}</section>;
    if (block.type === "image" && block.src) {
      return <figure className="full-reading-figure" key={index}><button className="full-reading-image-button" onClick={() => onZoom(block)} type="button" aria-label={`Enlarge ${block.alt || "instructional visual"}`}><img alt={block.alt || "Instructional diagram, chart, or table"} src={asset(block.src)} width={block.width} height={block.height} loading="lazy" decoding="async" /><span className="full-reading-zoom-hint">Enlarge ↗</span></button></figure>;
    }
    if (block.type === "question") return <h4 className="full-reading-learning-question" key={index}>{block.text}</h4>;
    if (block.type === "heading") {
      if (headingLevel === 3) return <h3 key={index}>{block.text}</h3>;
      return block.level && block.level >= 4 ? <h5 key={index}>{block.text}</h5> : <h4 key={index}>{block.text}</h4>;
    }
    return <p key={index}>{block.text}</p>;
  });
}

export function ReadingFigureDialog({ figure, onClose }: { figure: ContentBlock | null; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => { if (figure) dialog.current?.showModal(); else dialog.current?.close(); }, [figure]);
  return <dialog className="full-reading-dialog" ref={dialog} onClose={onClose} aria-label="Enlarged instructional visual"><header><span>Instructional visual</span><button type="button" onClick={onClose} autoFocus>Close ×</button></header><div>{figure?.src ? <img src={asset(figure.src)} alt={figure.alt || "Instructional diagram, chart, or table"} /> : null}</div></dialog>;
}

function ReadingQuiz({ readingId, quizSets, onZoom }: { readingId: number; quizSets: QuizSet[]; onZoom: (block: ContentBlock) => void }) {
  const questions = quizSets.flatMap((set) => set.questions.map((question) => ({ ...question, setTitle: set.title })));
  const storageKey = `return-lab-imported-quiz-v1-${readingId}`;
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<string, QuizAnswer>>(() => {
    try {
      const value: unknown = JSON.parse(localStorage.getItem(storageKey) || "{}");
      return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, QuizAnswer> : {};
    } catch { return {}; }
  });
  useEffect(() => { try { localStorage.setItem(storageKey, JSON.stringify(answers)); } catch { /* Quiz remains usable without storage. */ } }, [answers, storageKey]);
  if (!questions.length) return null;
  const question = questions[current];
  const answer = answers[question.id];
  const correct = answer?.selected === question.correctOptionId;
  const attempted = questions.filter((item) => answers[item.id]?.checked).length;
  const score = questions.filter((item) => answers[item.id]?.checked && answers[item.id]?.selected === item.correctOptionId).length;
  const complete = attempted === questions.length;
  const choose = (selected: string) => setAnswers((value) => ({ ...value, [question.id]: { selected, checked: false } }));
  const retry = () => setAnswers((value) => ({ ...value, [question.id]: { checked: false } }));
  const reset = () => { setAnswers({}); setCurrent(0); };
  return (
    <section className="full-reading-quiz" id="full-quiz" aria-labelledby="full-quiz-title">
      <header><div><span className="section-code">KNOWLEDGE CHECK</span><h3 id="full-quiz-title">Choose, commit, then learn from the result.</h3></div><strong>{score}/{questions.length} correct</strong></header>
      <div className="full-quiz-progress"><span>Question {current + 1} of {questions.length}</span><span>{attempted} answered</span></div>
      <div className="full-quiz-progress-bar" aria-label={`${attempted} of ${questions.length} questions answered`}><span style={{ width: `${attempted / questions.length * 100}%` }} /></div>
      <article className="full-quiz-card">
        <p className="full-quiz-set">{question.setTitle}</p><h4 id={`${question.id}-prompt`}>{question.prompt}</h4>
        {question.supportingBlocks.length ? <div className="full-reading-prose full-quiz-support"><ReadingBlocks blocks={question.supportingBlocks} onZoom={onZoom} /></div> : null}
        <div className="full-quiz-options" role="radiogroup" aria-labelledby={`${question.id}-prompt`}>
          {question.options.map((option) => {
            const selected = answer?.selected === option.id;
            const isCorrectOption = option.id === question.correctOptionId;
            const status = answer?.checked ? (isCorrectOption ? "Correct answer" : selected ? "Your answer — incorrect" : "Not the best answer") : "";
            return <label className={`${selected ? "selected" : ""}${answer?.checked && isCorrectOption ? " correct" : ""}${answer?.checked && selected && !isCorrectOption ? " incorrect" : ""}`} key={option.id}><input checked={selected} disabled={answer?.checked} name={`${question.id}-answer`} onChange={() => choose(option.id)} type="radio" /><span className="full-quiz-option-id">{option.id}</span><span>{option.text}{status ? <small>{status}</small> : null}</span></label>;
          })}
        </div>
        {!answer?.checked ? <div className="full-quiz-actions"><button disabled={!answer?.selected} onClick={() => setAnswers((value) => ({ ...value, [question.id]: { ...value[question.id], checked: true } }))} type="button">Check answer</button><button className="secondary" onClick={() => setAnswers((value) => ({ ...value, [question.id]: { checked: true, revealed: true } }))} type="button">Reveal answer</button></div> : null}
        {answer?.checked ? <div className={`full-quiz-feedback${correct ? " correct" : answer.revealed ? " revealed" : ""}`} role="status"><strong>{answer.revealed ? `Answer: ${question.correctOptionId}` : correct ? "Correct" : `The correct answer is ${question.correctOptionId}`}</strong>{question.explanation ? <p>{question.explanation}</p> : null}{question.solutionBlocks.length ? <details><summary>Show the step-by-step solution</summary><ol className="full-quiz-steps">{question.solutionBlocks.map((block, index) => <li key={index}><div className="full-reading-prose"><ReadingBlocks blocks={[block]} onZoom={onZoom} /></div></li>)}</ol></details> : null}<button className="secondary" type="button" onClick={retry}>Try this question again</button></div> : null}
      </article>
      <nav className="full-quiz-navigation" aria-label="Quiz question navigation"><button type="button" disabled={current === 0} onClick={() => setCurrent((value) => value - 1)}>← Previous</button><div>{questions.map((item, index) => <button aria-label={`Question ${index + 1}${answers[item.id]?.checked ? ", answered" : ""}`} className={index === current ? "current" : answers[item.id]?.checked ? "answered" : ""} key={item.id} onClick={() => setCurrent(index)} type="button">{index + 1}</button>)}</div><button type="button" disabled={current === questions.length - 1} onClick={() => setCurrent((value) => value + 1)}>Next →</button></nav>
      {complete ? <div className="full-quiz-final" role="status"><span>Final score</span><strong>{score} / {questions.length}</strong><p>{Math.round(score / questions.length * 100)}% correct</p><button type="button" onClick={reset}>Retry the full quiz</button></div> : null}
    </section>
  );
}

export default function FullReading({ readingId }: { readingId: number }) {
  const [content, setContent] = useState<ReadingContent | null>(null);
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [zoomed, setZoomed] = useState<ContentBlock | null>(null);
  useEffect(() => {
    const controller = new AbortController(); setContent(null); setFailed(false);
    void fetch(asset(`content/readings/${String(readingId).padStart(3, "0")}.json`), { signal: controller.signal }).then(async (response) => {
      if (!response.ok) throw new Error("Reading unavailable");
      const data = await response.json() as ReadingContent;
      if (data.readingId !== readingId || !Array.isArray(data.modules) || !Array.isArray(data.review) || !Array.isArray(data.quizSets)) throw new Error("Reading unavailable");
      if (!controller.signal.aborted) setContent(data);
    }).catch(() => { if (!controller.signal.aborted) setFailed(true); });
    return () => controller.abort();
  }, [readingId, attempt]);
  useEffect(() => {
    if (!content) return;
    const match = window.location.hash.match(/\/section\/([^/?#]+)/); if (!match) return;
    const frame = window.requestAnimationFrame(() => document.getElementById(decodeURIComponent(match[1]))?.scrollIntoView());
    return () => window.cancelAnimationFrame(frame);
  }, [content]);
  if (failed) return <section className="full-reading-state" id="full-reading" role="alert"><span className="section-code">COMPLETE LESSON</span><h2>The reading could not be loaded.</h2><p>Check your connection and try again.</p><button type="button" onClick={() => setAttempt((value) => value + 1)}>Retry reading</button></section>;
  if (!content) return <section className="full-reading-state" id="full-reading" aria-live="polite"><span className="section-code">COMPLETE LESSON</span><p>Loading the complete reading…</p></section>;
  return (
    <section className="full-reading" id="full-reading" aria-labelledby="full-reading-title">
      <header className="full-reading-intro"><span className="section-code">COMPLETE LESSON</span><h2 id="full-reading-title">Build the whole picture.</h2><p>Work through each module, then use the review and quiz to check your understanding.</p><nav aria-label="Complete lesson sections" className="full-reading-navigation">{content.modules.map((module) => <a href={`#/reading/${readingId}/section/full-module-${module.id}`} key={module.id}><span>{module.id}</span>{module.title}</a>)}{content.review.length ? <a href={`#/reading/${readingId}/section/full-review`}><span>REVIEW</span>Key concepts</a> : null}{content.quizSets.length ? <a href={`#/reading/${readingId}/section/full-quiz`}><span>QUIZ</span>Knowledge check</a> : null}</nav></header>
      {content.introduction?.length ? <div className="full-reading-prose"><ReadingBlocks blocks={content.introduction} onZoom={setZoomed} headingLevel={3} /></div> : null}
      {content.modules.map((module) => <article className="full-reading-module" id={`full-module-${module.id}`} key={module.id}><header><span className="section-code">MODULE {module.id}</span><h3>{module.title}</h3></header><div className="full-reading-prose"><ReadingBlocks blocks={module.blocks} onZoom={setZoomed} /></div></article>)}
      {content.review.length ? <section className="full-reading-review" id="full-review"><header><span className="section-code">REVIEW</span><h3>Key concepts</h3></header><div className="full-reading-prose"><ReadingBlocks blocks={content.review} onZoom={setZoomed} /></div></section> : null}
      <ReadingQuiz readingId={readingId} quizSets={content.quizSets} onZoom={setZoomed} /><ReadingFigureDialog figure={zoomed} onClose={() => setZoomed(null)} />
    </section>
  );
}
