import { useEffect, useId, useMemo, useRef, useState } from "react";
import { MathText } from "./MathText";
import { completeModule, getSavedQuizQuestion, readStudyState, recordQuestionAttempt, registerQuestions, rememberQuizPosition, rememberStudyPosition, useStudyState } from "../../lib/learning";
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

function WorkedExampleStep({ step, index }: { step: NonNullable<ContentBlock["steps"]>[number]; index: number }) {
  const id = useId();
  const [shown, setShown] = useState(false);
  const [hint, setHint] = useState(false);
  const [response, setResponse] = useState("");
  return <div className="full-reading-worked-step"><div className="full-reading-worked-number">{index + 1}</div><div><h6>{step.title}</h6><label className="full-reading-step-response" htmlFor={id}>Try this step. Write your method, result, and units before comparing.<textarea id={id} value={response} onChange={(event) => setResponse(event.target.value)} rows={2} placeholder="My approach…" /></label><div className="full-reading-step-actions"><button type="button" onClick={() => setHint(!hint)} aria-expanded={hint}>{hint ? "Hide hint" : "Get a hint"}</button><button type="button" onClick={() => setShown(!shown)} aria-expanded={shown}>{shown ? "Hide this solution" : "Compare this step"}</button></div>{hint ? <p className="full-reading-step-hint">{step.body?.[0] || "Identify the inputs and their units, then choose the relationship needed for this step. Keep intermediate values unrounded."}</p> : null}<div className="full-reading-step-solution" hidden={!shown}>{step.body?.map((text) => <p key={text}>{text}</p>)}{step.rows?.length ? <div className="full-reading-worked-table" role="table">{step.rows.map((row, rowIndex) => <div className="full-reading-worked-row" role="row" key={rowIndex}>{row.map((cell, cellIndex) => <span role="cell" key={cellIndex}>{cell}</span>)}</div>)}</div> : null}{step.equations?.map((latex) => <div className="full-reading-worked-equation" key={latex}><MathText display latex={latex} /></div>)}{response.trim() ? <p className="full-reading-step-compare">Compare your reasoning and units with the solution. Explain any difference before continuing.</p> : null}</div></div></div>;
}

export function ReadingBlocks({ blocks, onZoom, headingLevel = 4, objectiveAnchors = false }: { blocks: ContentBlock[]; onZoom: (block: ContentBlock) => void; headingLevel?: 3 | 4; objectiveAnchors?: boolean }) {
  return blocks.map((block, index) => {
    if (block.type === "math" && block.latex) return <div className="full-reading-math" key={index}>{block.prose ? <p>{block.prose}</p> : null}<MathText display={block.display !== false} latex={block.latex} /></div>;
    if (block.type === "worked-example" && block.steps) return <section className="full-reading-worked" key={index}><h5>{block.title || "Worked example"}</h5><p className="full-reading-worked-intro">Work one step at a time. Hints and solutions are available whenever you need them.</p>{block.steps.map((step, stepIndex) => <WorkedExampleStep step={step} index={stepIndex} key={stepIndex} />)}</section>;
    if (block.type === "image" && block.src) {
      return <figure className="full-reading-figure" key={index}><button className="full-reading-image-button" onClick={() => onZoom(block)} type="button" aria-label={`Enlarge ${block.alt || "instructional visual"}`}><img alt={block.alt || "Instructional diagram, chart, or table"} src={asset(block.src)} width={block.width} height={block.height} decoding="async" /><span className="full-reading-zoom-hint">Enlarge ↗</span></button></figure>;
    }
    if (block.type === "question") return <h4 className="full-reading-learning-question" id={objectiveAnchors && block.objectiveId ? `full-objective-${block.objectiveId}` : undefined} key={index}>{block.text}</h4>;
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

function ReadingQuiz({ readingId, quizSets, onZoom, checkpoint = false }: { readingId: number; quizSets: QuizSet[]; onZoom: (block: ContentBlock) => void; checkpoint?: boolean }) {
  const questions = useMemo(() => quizSets.flatMap((set) => set.questions.map((question) => ({ ...question, setTitle: set.title, moduleId: set.moduleId }))), [quizSets]);
  const storageKey = `return-lab-imported-quiz-v1-${readingId}`;
  const [currentId, setCurrentId] = useState(() => new URLSearchParams(window.location.hash.split("?")[1] || "").get("question") || getSavedQuizQuestion(readingId) || "");
  const [filterMode, setFilterMode] = useState<"all" | "unanswered" | "incorrect">("all");
  const study = useStudyState();
  const [answers, setAnswers] = useState<Record<string, QuizAnswer>>(() => {
    try {
      const value: unknown = JSON.parse(localStorage.getItem(storageKey) || "{}");
      return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, QuizAnswer> : {};
    } catch { return {}; }
  });
  const questionIds = questions.map((question) => question.id).join("|");
  useEffect(() => { try { localStorage.setItem(storageKey, JSON.stringify(answers)); } catch { /* Quiz remains usable without storage. */ } }, [answers, storageKey]);
  useEffect(() => {
    const syncQuestion = () => {
      const params = new URLSearchParams(window.location.hash.split("?")[1] || "");
      const requested = params.get("question");
      if (requested && params.get("retry") === "1" && questions.some((question) => question.id === requested)) {
        setAnswers((value) => ({ ...value, [requested]: { checked: false } }));
        params.delete("retry");
        window.history.replaceState(null, "", `${window.location.hash.split("?")[0]}?${params}`);
      }
      if (requested && questions.some((question) => question.id === requested)) { setCurrentId(requested); setFilterMode("all"); }
    };
    syncQuestion();
    window.addEventListener("hashchange", syncQuestion);
    return () => window.removeEventListener("hashchange", syncQuestion);
  }, [questionIds]);
  useEffect(() => { setFilterMode("all"); }, [questionIds]);
  const current = Math.max(0, questions.findIndex((question) => question.id === currentId));
  const setCurrent = (index: number) => {
    const item = questions[index];
    if (!item) return;
    setCurrentId(item.id);
    rememberQuizPosition(readingId, item.id);
    const query = new URLSearchParams({ question: item.id });
    if (checkpoint) query.set("module", item.moduleId);
    window.history.replaceState(null, "", `#/reading/${readingId}/section/full-quiz?${query}`);
  };
  if (!questions.length) return null;
  const question = questions[current];
  const answer = answers[question.id];
  const correct = answer?.selected === question.correctOptionId;
  const attempted = questions.filter((item) => answers[item.id]?.checked).length;
  const score = questions.filter((item) => answers[item.id]?.checked && answers[item.id]?.selected === item.correctOptionId).length;
  const needsReview = (item: QuizQuestion) => {
    const record = study.questions[`quiz:${readingId}:${item.id}`];
    return record ? !record.latestCorrect : Boolean(answers[item.id]?.checked && answers[item.id]?.selected !== item.correctOptionId);
  };
  const incorrectCount = questions.filter(needsReview).length;
  const unansweredCount = questions.length - attempted;
  const complete = attempted === questions.length;
  const records = questions.map((item) => study.questions[`quiz:${readingId}:${item.id}`]).filter(Boolean);
  const firstAttempts = records.filter((record) => typeof record.firstCorrect === "boolean");
  const history = study.questions[`quiz:${readingId}:${question.id}`];
  const similar = questions.find((item) => item.id !== question.id && item.objectiveIds.some((objective) => question.objectiveIds.includes(objective)));
  const choose = (selected: string) => { setCurrent(current); setAnswers((value) => ({ ...value, [question.id]: { selected, checked: false } })); };
  const retry = () => setAnswers((value) => ({ ...value, [question.id]: { checked: false } }));
  const reset = () => { setAnswers((value) => { const next = { ...value }; questions.forEach((item) => delete next[item.id]); return next; }); setCurrent(0); setFilterMode("all"); };
  const check = (revealed = false) => {
    setCurrent(current);
    setAnswers((value) => ({ ...value, [question.id]: revealed ? { checked: true, revealed: true } : { ...value[question.id], checked: true } }));
    recordQuestionAttempt({ questionId: `quiz:${readingId}:${question.id}`, readingId, prompt: question.prompt, sectionId: "full-quiz", objectiveIds: question.objectiveIds, correct: !revealed && correct, revealed });
  };

  const matchingIndices = questions
    .map((q, i) => ({ q, i }))
    .filter(({ q }) => {
      const ans = answers[q.id];
      if (filterMode === "unanswered") return !ans?.checked;
      if (filterMode === "incorrect") return needsReview(q);
      return true;
    })
    .map(({ i }) => i);

  const prevIndex = matchingIndices.filter((i) => i < current).pop();
  const nextIndex = matchingIndices.find((i) => i > current);

  return (
    <section className="full-reading-quiz" id="full-quiz" aria-labelledby="full-quiz-title">
      <header><div><span className="section-code">{checkpoint ? "MODULE CHECKPOINT" : "KNOWLEDGE CHECK"}</span><h3 id="full-quiz-title">Choose, commit, then learn from the result.</h3></div><strong>{score}/{questions.length} correct this round</strong></header>
      {firstAttempts.length ? <p className="full-quiz-history-summary">First attempts: {firstAttempts.filter((record) => record.firstCorrect).length}/{firstAttempts.length} correct · Latest attempts: {records.filter((record) => record.latestCorrect).length}/{records.length} correct. Retrying preserves this history.</p> : null}
      
      <div className="full-quiz-filters" role="group" aria-label="Filter questions">
        <button className={filterMode === "all" ? "active" : ""} onClick={() => setFilterMode("all")} type="button">All ({questions.length})</button>
        <button className={filterMode === "unanswered" ? "active" : ""} onClick={() => {
          setFilterMode("unanswered");
          const firstUnanswered = questions.findIndex((q) => !answers[q.id]?.checked);
          if (firstUnanswered !== -1) setCurrent(firstUnanswered);
        }} type="button">Unanswered ({unansweredCount})</button>
        <button className={filterMode === "incorrect" ? "active" : ""} onClick={() => {
          setFilterMode("incorrect");
          const firstIncorrect = questions.findIndex(needsReview);
          if (firstIncorrect !== -1) setCurrent(firstIncorrect);
        }} type="button">Needs Review ({incorrectCount})</button>
      </div>

      <div className="full-quiz-progress"><span>Question {current + 1} of {questions.length}</span><span>{attempted} answered</span></div>
      <div className="full-quiz-progress-bar" aria-label={`${attempted} of ${questions.length} questions answered`}><span style={{ width: `${attempted / questions.length * 100}%` }} /></div>
      {!matchingIndices.length ? <p className="full-quiz-empty" role="status">{filterMode === "incorrect" ? "No questions need correction. Use All to practice again." : `Every question in this ${checkpoint ? "checkpoint" : "quiz"} has been answered. Use All to review your feedback.`}</p> : <article className="full-quiz-card">
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
        {!answer?.checked ? <div className="full-quiz-actions"><button disabled={!answer?.selected} onClick={() => check()} type="button">Check answer</button><button className="secondary" onClick={() => check(true)} type="button">Reveal answer</button></div> : null}
        {answer?.checked ? <div className={`full-quiz-feedback${correct ? " correct" : answer.revealed ? " revealed" : ""}`} role="status"><strong>{answer.revealed ? `Answer: ${question.correctOptionId}` : correct ? "Correct" : `The correct answer is ${question.correctOptionId}`}</strong>{question.explanation ? <p>{question.explanation}</p> : null}{question.solutionBlocks.length ? <details><summary>Show the step-by-step solution</summary><ol className="full-quiz-steps">{question.solutionBlocks.map((block, index) => <li key={index}><div className="full-reading-prose"><ReadingBlocks blocks={[block]} onZoom={onZoom} /></div></li>)}</ol></details> : null}{!correct ? <div className="full-quiz-remediation"><span>Revisit the explanation:</span>{question.objectiveIds.length ? question.objectiveIds.map((objective) => <a key={objective} href={`#/reading/${readingId}/section/full-objective-${objective}`}>Concept {objective} →</a>) : <a href={`#/reading/${readingId}/section/full-module-${question.moduleId}`}>Review this module →</a>}{similar ? <a href={`#/reading/${readingId}/section/full-quiz?question=${encodeURIComponent(similar.id)}&retry=1`}>Try a related question →</a> : null}</div> : null}<button className="secondary" type="button" onClick={retry}>Try this question again</button></div> : null}
        {history?.attempts.length ? <details className="full-quiz-attempt-history"><summary>Question history ({history.attempts.length} {history.attempts.length === 1 ? "attempt" : "attempts"})</summary><p>First answer: {history.firstCorrect === undefined ? "not yet submitted" : history.firstCorrect ? "correct" : "incorrect"}. Latest answer: {history.latestCorrect ? "correct" : "needs review"}.</p><ol>{history.attempts.map((item, index) => <li key={`${item.at}-${index}`}>{item.revealed ? "Answer revealed" : item.correct ? "Correct" : "Incorrect"} · {new Date(item.at).toLocaleString(undefined, { dateStyle: "short", timeStyle: "short" })}</li>)}</ol></details> : null}
      </article>}
      <nav className="full-quiz-navigation" aria-label="Quiz question navigation">
        <button type="button" disabled={prevIndex === undefined} onClick={() => prevIndex !== undefined && setCurrent(prevIndex)}>← Previous</button>
        <div>{questions.map((item, index) => {
          const ans = answers[item.id];
          const isChecked = ans?.checked;
          const isCorrect = isChecked && ans?.selected === item.correctOptionId;
          const isIncorrect = isChecked && ans?.selected !== item.correctOptionId;
          const isFilteredOut = (filterMode === "unanswered" && isChecked) || (filterMode === "incorrect" && !needsReview(item));
          return (
            <button
              aria-label={`Question ${index + 1}${isChecked ? (isCorrect ? ", correct" : ", incorrect") : ", unanswered"}`}
              className={`${index === current ? "current" : ""} ${isChecked ? "answered" : ""} ${isCorrect ? "is-correct" : isIncorrect ? "is-incorrect" : ""} ${isFilteredOut ? "filtered-out" : ""}`}
              key={item.id}
              onClick={() => setCurrent(index)}
              type="button"
            >
              {index + 1}{isCorrect ? " ✓" : isIncorrect ? " ✗" : ""}
            </button>
          );
        })}</div>
        <button type="button" disabled={nextIndex === undefined} onClick={() => nextIndex !== undefined && setCurrent(nextIndex)}>Next →</button>
      </nav>
      {complete ? <div className="full-quiz-final" role="status"><span>This round</span><strong>{score} / {questions.length}</strong><p>{Math.round(score / questions.length * 100)}% correct{incorrectCount ? " — revisit the linked explanations and try those questions again." : " — explain the reasoning once more without the options."}</p><button type="button" onClick={reset}>{checkpoint ? "Retry this checkpoint" : "Retry the full quiz"}</button></div> : null}
    </section>
  );
}

export default function FullReading({ readingId }: { readingId: number }) {
  const [content, setContent] = useState<ReadingContent | null>(null);
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [zoomed, setZoomed] = useState<ContentBlock | null>(null);
  const [view, setView] = useState<"sessions" | "all">("sessions");
  const [activeSection, setActiveSection] = useState("");
  const [checkpointModule, setCheckpointModule] = useState<string | null>(null);
  const study = useStudyState();
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
    registerQuestions(readingId, content.quizSets.flatMap((set) => set.questions.map((question) => `quiz:${readingId}:${question.id}`)));
    const syncSection = () => {
      const match = window.location.hash.match(/\/section\/([^/?#]+)/);
      const section = match ? decodeURIComponent(match[1]) : "";
      const query = new URLSearchParams(window.location.hash.split("?")[1] || "");
      const requestedModule = query.get("module");
      const module = content.modules.find((item) => section === `full-module-${item.id}` || (section.startsWith("full-objective-") && item.blocks.some((block) => block.objectiveId === section.slice("full-objective-".length))));
      const validCheckpoint = requestedModule && content.modules.some((item) => item.id === requestedModule) ? requestedModule : null;
      if (query.get("view") === "all") setView("all");
      else if (module || section === "full-review" || section === "full-quiz") setView("sessions");
      setCheckpointModule(section === "full-quiz" ? validCheckpoint : null);
      if (module) setActiveSection(module.id);
      else if (section === "full-review" || section === "full-quiz") setActiveSection(section);
      else {
        const saved = readStudyState();
        const rememberedModule = saved.resume?.readingId === readingId ? content.modules.find((item) => saved.resume?.sectionId === `full-module-${item.id}`) : undefined;
        const firstUnread = content.modules.find((item) => !saved.completedModules[readingId]?.includes(item.id));
        setActiveSection((previous) => previous || rememberedModule?.id || firstUnread?.id || content.modules[0]?.id || "full-quiz");
      }
    };
    syncSection();
    window.addEventListener("hashchange", syncSection);
    return () => window.removeEventListener("hashchange", syncSection);
  }, [content, readingId]);
  useEffect(() => {
    if (!content || !activeSection) return;
    const match = window.location.hash.match(/\/section\/([^/?#]+)/);
    if (!match) return;
    const frame = window.requestAnimationFrame(() => document.getElementById(decodeURIComponent(match[1]))?.scrollIntoView());
    return () => window.cancelAnimationFrame(frame);
  }, [content, activeSection, view, checkpointModule]);
  if (failed) return <section className="full-reading-state" id="full-reading" role="alert"><span className="section-code">COMPLETE LESSON</span><h2>The reading could not be loaded.</h2><p>Check your connection and try again.</p><button type="button" onClick={() => setAttempt((value) => value + 1)}>Retry reading</button></section>;
  if (!content) return <section className="full-reading-state" id="full-reading" aria-live="polite"><span className="section-code">COMPLETE LESSON</span><p>Loading the complete reading…</p></section>;
  const activeModule = content.modules.find((module) => module.id === activeSection);
  const quizScope = view === "sessions" ? checkpointModule || activeModule?.id : null;
  const visibleQuizSets = quizScope ? content.quizSets.filter((set) => set.moduleId === quizScope) : content.quizSets;
  const quizVisible = view === "all" || activeSection === "full-quiz" || Boolean(activeModule);
  const completedModules = study.completedModules[readingId] || [];
  const moduleTime = (module: ReadingContent["modules"][number]) => {
    const words = module.blocks.reduce((total, block) => total + [block.text, block.prose, block.title, ...(block.steps || []).flatMap((step) => [step.title, ...(step.body || []), ...(step.rows || []).flat()])].filter(Boolean).join(" ").split(/\s+/).length, 0);
    const questionCount = content.quizSets.filter((set) => set.moduleId === module.id).reduce((total, set) => total + set.questions.length, 0);
    return Math.max(3, Math.ceil(words / 200 + questionCount * 1.5 + module.blocks.filter((block) => block.type === "math" || block.type === "worked-example").length * 0.25));
  };
  const recapFor = (module: ReadingContent["modules"][number]) => {
    const objectives = new Set(module.blocks.map((block) => block.objectiveId).filter(Boolean));
    let relevant = false;
    return content.review.filter((block) => { if (block.type === "question") relevant = objectives.has(block.objectiveId); return relevant; });
  };
  const navigateModule = (moduleId: string) => {
    rememberStudyPosition(readingId, `full-module-${moduleId}`);
    window.location.hash = `/reading/${readingId}/section/full-module-${moduleId}`;
  };
  const finishModule = (moduleId: string) => {
    completeModule(readingId, moduleId);
    const nextModule = content.modules[content.modules.findIndex((module) => module.id === moduleId) + 1];
    if (nextModule) navigateModule(nextModule.id);
    else { rememberStudyPosition(readingId, content.review.length ? "full-review" : "full-quiz"); window.location.hash = `/reading/${readingId}/section/${content.review.length ? "full-review" : "full-quiz"}`; }
  };
  return (
    <section className="full-reading" id="full-reading" aria-labelledby="full-reading-title">
      <header className="full-reading-intro"><span className="section-code">COMPLETE LESSON</span><h2 id="full-reading-title">Build the whole picture.</h2><p>Study one module, recall its key ideas, then take a short checkpoint. Estimated times include practice and vary with your pace.</p><div className="full-reading-session-tools" role="group" aria-label="Reading view"><button type="button" aria-pressed={view === "sessions"} onClick={() => { setView("sessions"); if (!activeModule) navigateModule(content.modules[0]?.id || ""); }}>Study in sessions</button><button type="button" aria-pressed={view === "all"} onClick={() => { setView("all"); window.location.hash = `/reading/${readingId}/section/full-reading?view=all`; }}>Browse full reading</button><span>{completedModules.length}/{content.modules.length} modules read</span></div><nav aria-label="Complete lesson sections" className="full-reading-navigation">{content.modules.map((module) => <a href={`#/reading/${readingId}/section/full-module-${module.id}`} aria-current={view === "sessions" && activeSection === module.id ? "step" : undefined} key={module.id}><span>{completedModules.includes(module.id) ? "✓ " : ""}{module.id}</span><div>{module.title}<small>About {moduleTime(module)} min · including checkpoint</small></div></a>)}{content.review.length ? <a href={`#/reading/${readingId}/section/full-review`} aria-current={activeSection === "full-review" ? "step" : undefined}><span>REVIEW</span>Key concepts</a> : null}{content.quizSets.length ? <a href={`#/reading/${readingId}/section/full-quiz`} aria-current={activeSection === "full-quiz" ? "step" : undefined}><span>QUIZ</span>Full knowledge check</a> : null}</nav></header>
      {content.introduction?.length ? <div className="full-reading-prose" hidden={view === "sessions" && activeSection !== content.modules[0]?.id}><ReadingBlocks blocks={content.introduction} onZoom={setZoomed} headingLevel={3} /></div> : null}
      {content.modules.map((module) => <article className="full-reading-module" id={`full-module-${module.id}`} hidden={view === "sessions" && activeSection !== module.id} key={module.id}><header><span className="section-code">MODULE {module.id} · ABOUT {moduleTime(module)} MIN</span><h3>{module.title}</h3></header><div className="full-reading-prose"><ReadingBlocks blocks={module.blocks} onZoom={setZoomed} objectiveAnchors /></div><div className="full-reading-module-recap"><h4>Pause and recall</h4><p>Explain these ideas in your own words before opening the recap.</p><ul>{module.blocks.filter((block) => block.type === "question").map((block, index) => <li key={block.objectiveId || index}>{block.text}</li>)}</ul>{recapFor(module).length ? <details><summary>Compare with the module recap</summary><div className="full-reading-prose"><ReadingBlocks blocks={recapFor(module)} onZoom={setZoomed} /></div></details> : null}<div className="full-reading-module-actions"><a href={`#/reading/${readingId}/section/full-quiz?module=${encodeURIComponent(module.id)}`}>Take this module’s checkpoint →</a><button type="button" onClick={() => finishModule(module.id)}>{completedModules.includes(module.id) ? "Continue to the next session →" : "Mark module read and continue →"}</button></div><small>Marking a module read records study completion. Quiz answers track understanding separately.</small></div></article>)}
      {content.review.length ? <section className="full-reading-review" id="full-review" hidden={view === "sessions" && activeSection !== "full-review"}><header><span className="section-code">REVIEW</span><h3>Key concepts</h3></header><div className="full-reading-prose"><ReadingBlocks blocks={content.review} onZoom={setZoomed} /></div><a className="full-reading-next-action" href={`#/reading/${readingId}/section/full-quiz`}>Take the full knowledge check →</a></section> : null}
      <div className="full-reading-quiz-container" hidden={!quizVisible}><ReadingQuiz readingId={readingId} quizSets={visibleQuizSets} checkpoint={Boolean(quizScope)} onZoom={setZoomed} />{quizScope ? <div className="full-reading-session-finish"><button type="button" onClick={() => finishModule(quizScope)}>{completedModules.includes(quizScope) ? "Continue to the next session →" : "Mark module read and continue →"}</button><a href={`#/reading/${readingId}/section/full-module-${quizScope}`}>Back to module explanation</a></div> : null}</div><ReadingFigureDialog figure={zoomed} onClose={() => setZoomed(null)} />
    </section>
  );
}
