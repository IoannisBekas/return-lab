import { useEffect, useState } from "react";
import { ReadingBlocks, ReadingFigureDialog, type ContentBlock } from "./FullReading";

type ReferenceContent = {
  title: string;
  sections: { id: string; title: string; blocks: ContentBlock[] }[];
};

export default function ReferenceLibrary() {
  const [content, setContent] = useState<ReferenceContent | null>(null);
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [zoomed, setZoomed] = useState<ContentBlock | null>(null);

  useEffect(() => {
    document.title = "Formula and Statistical Reference | Return Lab";
    const controller = new AbortController();
    setFailed(false);
    void fetch(`${import.meta.env.BASE_URL}content/reference.json`, { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error("Reference unavailable");
        const data = await response.json() as ReferenceContent;
        if (!Array.isArray(data.sections)) throw new Error("Reference unavailable");
        if (!controller.signal.aborted) setContent(data);
      })
      .catch(() => {
        if (!controller.signal.aborted) setFailed(true);
      });
    return () => {
      controller.abort();
      document.title = "Return Lab | Finance Learning App";
    };
  }, [attempt]);

  useEffect(() => {
    if (!content) return;
    const match = window.location.hash.match(/\/section\/([^/?#]+)/);
    if (!match) return;
    const frame = window.requestAnimationFrame(() => document.getElementById(decodeURIComponent(match[1]))?.scrollIntoView());
    return () => window.cancelAnimationFrame(frame);
  }, [content]);

  return (
    <main className="lesson-page reference-page">
      <a className="back-link" href="#/">← All readings</a>
      <header className="reference-intro">
        <span className="section-code">STUDY REFERENCE</span>
        <h1>{content?.title || "Formula and statistical reference"}</h1>
        <p>Find the typeset equations and statistical tables you need while working through a lesson. Select a table to enlarge it.</p>
      </header>
      {failed ? (
        <section className="full-reading-state" role="alert"><h2>The reference could not be loaded.</h2><p>Check your connection and try again.</p><button type="button" onClick={() => setAttempt((value) => value + 1)}>Retry reference</button></section>
      ) : !content ? <p className="deep-lesson-loading" aria-live="polite">Loading the reference…</p> : (
        <div className="lesson-layout">
          <aside className="lesson-outline"><span className="section-code">REFERENCE SECTIONS</span><ol>{content.sections.map((section) => <li key={section.id}><a href={`#/reference/section/${section.id}`}>{section.title}</a></li>)}</ol></aside>
          <div className="lesson-content full-reading reference-content">
            {content.sections.map((section) => <section className="full-reading-module" id={section.id} key={section.id}><header><h2>{section.title}</h2></header><div className="full-reading-prose"><ReadingBlocks blocks={section.blocks} onZoom={setZoomed} headingLevel={3} /></div></section>)}
            <ReadingFigureDialog figure={zoomed} onClose={() => setZoomed(null)} />
          </div>
        </div>
      )}
    </main>
  );
}
