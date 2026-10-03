import { useEffect, useState } from "react";
import curriculum from "../../data/manifest.json";
import sourceManifest from "../../data/sourceManifest.json";
import { rateQuestionReview, reviewQuestionRoute, useStudyState } from "../../lib/learning";
import { getReferenceDueCount } from "./referenceStudy";
import "./ReviewPage.css";

export default function ReviewPage() {
  const study = useStudyState();
  const [mode, setMode] = useState<"due" | "all">("due");
  const [flashcardDue, setFlashcardDue] = useState(getReferenceDueCount);
  const [now, setNow] = useState(Date.now);
  useEffect(() => {
    document.title = "Your Review Plan | Return Lab";
    const refresh = () => { setFlashcardDue(getReferenceDueCount()); setNow(Date.now()); };
    window.addEventListener("return-lab-reference-study", refresh);
    window.addEventListener("focus", refresh);
    const timer = window.setInterval(refresh, 60_000);
    return () => { clearInterval(timer); window.removeEventListener("return-lab-reference-study", refresh); window.removeEventListener("focus", refresh); document.title = "Return Lab | Finance Learning App"; };
  }, []);
  const all = Object.values(study.questions).sort((a, b) => Number(a.latestCorrect) - Number(b.latestCorrect) || a.dueAt - b.dueAt);
  const due = all.filter((question) => question.dueAt <= now);
  const questions = mode === "due" ? due : all;
  const firstAttempts = all.filter((question) => typeof question.firstCorrect === "boolean");
  const firstCorrect = firstAttempts.filter((question) => question.firstCorrect).length;
  const currentCorrect = all.filter((question) => question.latestCorrect).length;
  return (
    <main className="lesson-page review-page">
      <a className="back-link" href="#/">← All readings</a>
      <header className="review-intro"><span className="section-code">YOUR REVIEW PLAN</span><h1>Turn practice into understanding.</h1><p>Return to missed questions, review the relevant concept, and try again before revealing the answer. Correct answers return for later recall.</p></header>
      <dl className="review-stats"><div><dt>Questions due</dt><dd>{due.length}</dd></div><div><dt>First attempts</dt><dd>{firstCorrect}/{firstAttempts.length}</dd></div><div><dt>Latest practice</dt><dd>{currentCorrect}/{all.length}</dd></div><div><dt>Flashcards due</dt><dd>{flashcardDue}</dd></div></dl>
      <p className="review-score-note">Revealed answers stay in review and do not count as correct independent attempts. Reading completion and practice accuracy are tracked separately.</p>
      <div className="review-toolbar"><div role="group" aria-label="Review queue"><button type="button" aria-pressed={mode === "due"} onClick={() => { setMode("due"); setNow(Date.now()); }}>Due now ({due.length})</button><button type="button" aria-pressed={mode === "all"} onClick={() => setMode("all")}>All practiced ({all.length})</button></div><a href="#/reference?due=1">Review due formula flashcards →</a></div>
      {questions.length ? <div className="review-queue">{questions.map((question) => {
        const reading = curriculum.find((item) => item.number === question.readingId);
        const modules = sourceManifest.filter((module) => module.readingId === question.readingId && module.objectives.some((objective) => question.objectiveIds.includes(objective.id)));
        const similar = all.find((item) => item.questionId !== question.questionId && item.readingId === question.readingId && item.objectiveIds.some((id) => question.objectiveIds.includes(id)));
        return <article className="review-card" key={question.questionId}>
          <div className="review-card-meta"><span>{reading?.topic} · Reading {String(question.readingId).padStart(2, "0")}</span><strong>{question.latestCorrect ? "Recall again" : "Needs practice"}</strong></div>
          <h2>{question.prompt}</h2><p>{reading?.title} · {question.attempts.filter((attempt) => !attempt.revealed).length} independent attempt{question.attempts.filter((attempt) => !attempt.revealed).length === 1 ? "" : "s"}{question.firstCorrect === undefined ? " · Answer revealed" : question.firstCorrect ? " · First attempt correct" : " · First attempt incorrect"}</p>
          <div className="review-card-links"><a className="primary-action" href={reviewQuestionRoute(question)}>Try the question again →</a>{modules.map((module) => <a key={module.moduleId} href={`#/reading/${question.readingId}/section/full-module-${module.moduleId}`}>Review {module.moduleTitle} →</a>)}{similar ? <a href={reviewQuestionRoute(similar)}>Try a related question →</a> : null}</div>
          <div className="review-schedule"><span>{question.dueAt <= now ? "Due now" : `Next review: ${new Date(question.dueAt).toLocaleDateString()}`}</span><div role="group" aria-label="Schedule this question"><button type="button" onClick={() => rateQuestionReview(question.questionId, "again")}>Again · 1 day</button><button type="button" onClick={() => rateQuestionReview(question.questionId, "hard")}>Hard · 2 days</button><button type="button" onClick={() => rateQuestionReview(question.questionId, "good")}>Good · later</button></div></div>
        </article>;
      })}</div> : <section className="review-empty"><h2>{all.length ? "You’re caught up for now." : "Your review plan starts with practice."}</h2><p>{all.length ? "Your next reviews are scheduled. You can revisit all practiced questions or start another module." : "Answer a module quiz or application question. Missed and revealed questions will appear here with links to the relevant lesson."}</p><a className="primary-action" href="#/section/curriculum">Choose a reading →</a></section>}
    </main>
  );
}
