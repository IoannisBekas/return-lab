import { useEffect, useMemo, useState } from "react";
import { ReadingBlocks, ReadingFigureDialog, type ContentBlock } from "./FullReading";
import { MathText } from "./MathText";
import { FLASHCARDS, filterReferenceSections, isReferenceCardDue, rateReferenceCard, readReferenceReviews, saveReferenceReviews, type ReferenceContent, type ReferenceRating } from "./referenceStudy";
import "./ReferenceLibrary.css";

const CATEGORIES = [
  "All Topics",
  "Quantitative Methods",
  "Economics",
  "Financial Statement Analysis",
  "Corporate Issuers",
  "Equity Valuation",
  "Fixed Income",
  "Derivatives",
  "Portfolio Management"
];

const FLASHCARD_LESSONS: Record<string, string> = {
  "tvm-ear": "1.3", "tvm-perpetuity": "2.1", "quant-harmonic": "3.1", "quant-bayes": "4.1",
  "econ-elasticity": "12.1", "econ-fiscal-multiplier": "14.2", "fsa-dupont-3": "37.4", "fsa-dupont-5": "37.4", "fsa-ccc": "37.2",
  "corp-wacc": "25.1", "corp-dol": "43.2", "equity-ggm": "46.2", "equity-justified-pe": "46.3",
  "fi-bond-pv": "52.1", "fi-modified-duration": "57.1", "fi-approx-convexity": "58.1", "fi-forward-rate": "55.1",
  "deriv-put-call-parity": "74.1", "deriv-forward-price": "70.1", "pm-capm-sml": "84.2", "pm-beta": "84.1",
  "pm-sharpe-ratio": "84.2", "pm-treynor-ratio": "84.2", "pm-jensen-alpha": "84.2",
};

export default function ReferenceLibrary() {
  const [content, setContent] = useState<ReferenceContent | null>(null);
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [zoomed, setZoomed] = useState<ContentBlock | null>(null);

  // Tools state:
  const [mode, setMode] = useState<"browse" | "flashcards">(() => window.location.hash.includes("due=1") ? "flashcards" : "browse");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All Topics");
  const [outlineOpen, setOutlineOpen] = useState(false);

  // Flashcards state:
  const [cardIndex, setCardIndex] = useState(0);
  const [isRevealed, setIsRevealed] = useState(false);
  const [reviews, setReviews] = useState(readReferenceReviews);
  const [queueMode, setQueueMode] = useState<"due" | "all">("due");
  const [now, setNow] = useState(Date.now);
  const [ratingMessage, setRatingMessage] = useState("");

  useEffect(() => {
    saveReferenceReviews(reviews);
  }, [reviews]);

  useEffect(() => {
    const update = () => setNow(Date.now());
    const timer = window.setInterval(update, 30_000);
    window.addEventListener("focus", update);
    return () => { window.clearInterval(timer); window.removeEventListener("focus", update); };
  }, []);

  useEffect(() => {
    const openDueQueue = () => {
      if (!window.location.hash.includes("due=1")) return;
      setMode("flashcards"); setQueueMode("due"); setCardIndex(0); setIsRevealed(false);
      setSearchQuery(""); setSelectedCategory("All Topics");
    };
    window.addEventListener("hashchange", openDueQueue);
    return () => window.removeEventListener("hashchange", openDueQueue);
  }, []);

  useEffect(() => {
    document.title = "Formula and Statistical Reference | Return Lab";
    const controller = new AbortController();
    setFailed(false);
    void fetch(`${import.meta.env.BASE_URL}content/reference.json`, { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error("Reference unavailable");
        const data = (await response.json()) as ReferenceContent;
        if (!Array.isArray(data.sections) || data.sections.some((section) => !Array.isArray(section.entries))) throw new Error("Reference unavailable");
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
    if (!content || mode !== "browse") return;
    const match = window.location.hash.match(/\/section\/([^/?#]+)/);
    if (!match) return;
    const frame = window.requestAnimationFrame(() =>
      document.getElementById(decodeURIComponent(match[1]))?.scrollIntoView()
    );
    return () => window.cancelAnimationFrame(frame);
  }, [content, mode]);

  const matchingFlashcards = useMemo(() => {
    return FLASHCARDS.filter((card) => {
      const matchesCategory =
        selectedCategory === "All Topics" || card.category === selectedCategory;
      const q = searchQuery.trim().toLowerCase();
      const matchesSearch =
        !q ||
        card.title.toLowerCase().includes(q) ||
        card.prompt.toLowerCase().includes(q) ||
        card.variables.toLowerCase().includes(q) ||
        card.takeaway.toLowerCase().includes(q);
      return matchesCategory && matchesSearch;
    });
  }, [selectedCategory, searchQuery]);

  const dueCount = matchingFlashcards.filter((card) => isReferenceCardDue(reviews, card.id, now)).length;
  const filteredFlashcards = useMemo(() => matchingFlashcards.filter((card) =>
    queueMode === "all" || isReferenceCardDue(reviews, card.id, now)
  ), [matchingFlashcards, queueMode, reviews, now]);
  const activeIndex = Math.min(cardIndex, Math.max(0, filteredFlashcards.length - 1));
  const activeCard = filteredFlashcards[activeIndex] || null;
  const nextDue = matchingFlashcards.reduce((earliest, card) => Math.min(earliest, reviews[card.id]?.dueAt ?? now), Infinity);
  const lessonModule = activeCard ? FLASHCARD_LESSONS[activeCard.id] : "";
  useEffect(() => setIsRevealed(false), [activeCard?.id]);

  const rateCard = (rating: ReferenceRating) => {
    if (!activeCard || !isRevealed) return;
    const updated = rateReferenceCard(reviews, activeCard.id, rating);
    setReviews(updated);
    setRatingMessage(`${activeCard.title}: next review ${new Date(updated[activeCard.id].dueAt).toLocaleString()}.`);
    setIsRevealed(false);
    setNow(Date.now());
    // Removing a due card shifts the next card into the same position.
    setCardIndex(queueMode === "due" ? Math.min(activeIndex, Math.max(0, filteredFlashcards.length - 2)) :
      (activeIndex + 1) % Math.max(1, filteredFlashcards.length));
  };

  const handleNextCard = () => {
    setIsRevealed(false);
    setCardIndex((activeIndex + 1) % Math.max(1, filteredFlashcards.length));
  };

  const handlePrevCard = () => {
    setIsRevealed(false);
    setCardIndex(activeIndex === 0 ? Math.max(0, filteredFlashcards.length - 1) : activeIndex - 1);
  };

  const handleShuffle = () => {
    setIsRevealed(false);
    const randomIndex = Math.floor(Math.random() * filteredFlashcards.length);
    setCardIndex(randomIndex);
  };

  const filteredSections = useMemo(() => {
    return content ? filterReferenceSections(content, searchQuery, selectedCategory) : [];
  }, [content, searchQuery, selectedCategory]);

  return (
    <main className="lesson-page reference-page">
      <a className="back-link" href="#/">
        ← All readings
      </a>
      <header className="reference-intro">
        <span className="section-code">STUDY REFERENCE</span>
        <h1>{content?.title || "Formula and statistical reference"}</h1>
        <p>
          Master the core CFA mathematical frameworks, typeset formulas, and
          standard statistical distribution tables.
        </p>
        <p className="reference-formula-hint">Long formulas scroll horizontally so their symbols stay readable.</p>
      </header>

      {/* Global Reference Tools Bar */}
      <section className="reference-tools-bar" aria-label="Reference study tools">
        <div className="reference-tools-top">
          <div className="reference-search-wrapper">
            <input
              aria-label="Search reference formulas"
              className="reference-search-input"
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setCardIndex(0);
                setIsRevealed(false);
              }}
              placeholder="Search by formula name, concept, or symbol (e.g. Sharpe, DuPont, Duration)..."
              type="search"
              value={searchQuery}
            />
          </div>

          <div className="reference-mode-switch" role="group" aria-label="View mode">
            <button
              className={`reference-mode-btn ${mode === "browse" ? "active" : ""}`}
              aria-pressed={mode === "browse"}
              onClick={() => setMode("browse")}
              type="button"
            >
              📖 Browse Reference
            </button>
            <button
              className={`reference-mode-btn ${mode === "flashcards" ? "active" : ""}`}
              aria-pressed={mode === "flashcards"}
              onClick={() => {
                setMode("flashcards");
                setCardIndex(0);
                setIsRevealed(false);
              }}
              type="button"
            >
              🎴 Formula Flashcards ({FLASHCARDS.length})
            </button>
            <button
              className="reference-print-btn"
              onClick={() => window.print()}
              title="Print reference sheets"
              type="button"
            >
              🖨️ Print Sheet
            </button>
          </div>
        </div>

        {/* Category Filter Chips */}
        <div className="reference-chips" role="group" aria-label="Topic categories">
          {CATEGORIES.map((cat) => (
            <button
              className={`reference-chip ${selectedCategory === cat ? "active" : ""}`}
              aria-pressed={selectedCategory === cat}
              key={cat}
              onClick={() => {
                setSelectedCategory(cat);
                setCardIndex(0);
                setIsRevealed(false);
              }}
              type="button"
            >
              {cat}
            </button>
          ))}
        </div>
        {mode === "flashcards" && <div className="reference-review-queue" role="group" aria-label="Flashcard queue">
          <button type="button" aria-pressed={queueMode === "due"} className={queueMode === "due" ? "active" : ""} onClick={() => { setQueueMode("due"); setCardIndex(0); setIsRevealed(false); }}>Due now ({dueCount})</button>
          <button type="button" aria-pressed={queueMode === "all"} className={queueMode === "all" ? "active" : ""} onClick={() => { setQueueMode("all"); setCardIndex(0); setIsRevealed(false); }}>All cards ({matchingFlashcards.length})</button>
          <p>Recall the answer first, then reveal and rate it. Reviews are saved in this browser.</p>
        </div>}
      </section>

      {searchQuery && (
        <p className="reference-search-summary" aria-live="polite">
          Searching for &ldquo;{searchQuery}&rdquo; &middot;{" "}
          {mode === "flashcards"
            ? `${filteredFlashcards.length} flashcard(s) match`
            : `${filteredSections.reduce((acc, s) => acc + s.entries.length, 0)} complete reference entries match`}
        </p>
      )}
      {mode === "flashcards" && <p className="flashcard-review-message" role="status">{ratingMessage}</p>}

      {failed ? (
        <section className="full-reading-state" role="alert">
          <h2>The reference could not be loaded.</h2>
          <p>Check your connection and try again.</p>
          <button type="button" onClick={() => setAttempt((value) => value + 1)}>
            Retry reference
          </button>
        </section>
      ) : !content ? (
        <p className="deep-lesson-loading" aria-live="polite">
          Loading the reference…
        </p>
      ) : mode === "flashcards" ? (
        /* Flashcard Study Mode */
        <section className="reference-flashcard-stage" aria-label="Formula flashcards study view">
          {activeCard ? (
            <>
              <div className="flashcard-status-bar">
                <span className="flashcard-category-tag">{activeCard.category}</span>
                <span>
                  Card {activeIndex + 1} of {filteredFlashcards.length}
                </span>
                <span className="flashcard-mastery-count">{reviews[activeCard.id] ? `Reviewed ${reviews[activeCard.id].reviews} time(s)` : "New card"}</span>
              </div>

              <article className="flashcard-card">
                <div className="flashcard-prompt-area">
                  <span className="section-code">FORMULA FOCUS</span>
                  <h3>{activeCard.title}</h3>
                  <p>{activeCard.prompt}</p>

                  {!isRevealed ? (
                    <button
                      className="flashcard-reveal-btn"
                      onClick={() => setIsRevealed(true)}
                      type="button"
                    >
                      Reveal Formula &amp; Interpretation &#8595;
                    </button>
                  ) : null}
                </div>

                {isRevealed && (
                  <div className="flashcard-answer-box" role="region" aria-label="Formula answer">
                    <MathText display latex={activeCard.latex} />
                    <p className="flashcard-variables">
                      <strong>Variables: </strong>
                      {activeCard.variables}
                    </p>
                    <div className="flashcard-takeaway">
                      <strong>Key Exam Insight: </strong>
                      {activeCard.takeaway}
                    </div>
                    <a className="reference-lesson-link" href={`#/reading/${lessonModule.split(".")[0]}/section/full-module-${lessonModule}`}>Revisit the lesson ↗</a>
                    {reviews[activeCard.id] && <p className="flashcard-next-review">Scheduled review: {new Date(reviews[activeCard.id].dueAt).toLocaleString()}</p>}
                  </div>
                )}

                <div className="flashcard-bottom-controls">
                  {isRevealed && <div className="flashcard-rating-actions" role="group" aria-label="How well did you recall the formula?">
                    <button className="flashcard-rate-btn needs-review" onClick={() => rateCard("again")} type="button">Again <small>10 minutes</small></button>
                    <button className="flashcard-rate-btn hard" onClick={() => rateCard("hard")} type="button">Hard <small>1 day</small></button>
                    <button className="flashcard-rate-btn mastered" onClick={() => rateCard("good")} type="button">Good <small>{Math.min(60, Math.max(3, (reviews[activeCard.id]?.intervalDays || 1.5) * 2))} days</small></button>
                  </div>}

                  <div className="flashcard-nav-buttons">
                    <button
                      disabled={filteredFlashcards.length <= 1}
                      onClick={handlePrevCard}
                      type="button"
                    >
                      &#8592; Previous
                    </button>
                    <button disabled={filteredFlashcards.length <= 1} onClick={handleShuffle} type="button">
                      &#128256; Shuffle
                    </button>
                    <button
                      disabled={filteredFlashcards.length <= 1}
                      onClick={handleNextCard}
                      type="button"
                    >
                      Next &#8594;
                    </button>
                  </div>
                </div>
              </article>
            </>
          ) : (
            <div className="full-reading-state">
              <h3>{matchingFlashcards.length ? "Your review queue is up to date." : "No flashcards match your current filters."}</h3>
              <p>{matchingFlashcards.length ? `Next review: ${new Date(nextDue).toLocaleString()}. You can still practice every card.` : "Try clearing your search or selecting All Topics."}</p>
              {matchingFlashcards.length ? <button type="button" onClick={() => { setQueueMode("all"); setCardIndex(0); }}>Practice all cards</button> :
              <button
                onClick={() => {
                  setSearchQuery("");
                  setSelectedCategory("All Topics");
                }}
                type="button"
              >
                Reset Filters
              </button>}
            </div>
          )}
        </section>
      ) : (
        /* Standard Browse Reference Mode */
        <div className="lesson-layout">
          <button className="reference-outline-toggle" type="button" aria-expanded={outlineOpen} aria-controls="reference-outline" onClick={() => setOutlineOpen((value) => !value)}>Reference sections {outlineOpen ? "−" : "+"}</button>
          <aside className={`lesson-outline ${outlineOpen ? "reference-outline-open" : ""}`} id="reference-outline">
            <span className="section-code">REFERENCE SECTIONS</span>
            <ol>
              {filteredSections.map((section) => (
                <li key={section.id}>
                  <a href={`#/reference/section/${section.id}`} onClick={() => setOutlineOpen(false)}>{section.title}</a>
                </li>
              ))}
            </ol>
          </aside>
          <div className="lesson-content full-reading reference-content">
            {filteredSections.length > 0 ? (
              filteredSections.map((section) => (
                <section className="full-reading-module" id={section.id} key={section.id}>
                  <header>
                    <h2>{section.title}</h2>
                  </header>
                  <div className="full-reading-prose">
                    {section.entries.map((entry) => <article className="reference-entry" key={entry.id} id={entry.id}>
                      <ReadingBlocks blocks={section.blocks.slice(entry.start, entry.end)} onZoom={setZoomed} headingLevel={3} />
                      <a className="reference-lesson-link" href={entry.lessonHref}>Study the related lesson ↗</a>
                    </article>)}
                  </div>
                </section>
              ))
            ) : (
              <div className="full-reading-state">
                <h3>No reference sections match your search.</h3>
                <p>Try clearing the search query or adjusting the category filter.</p>
                <button
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedCategory("All Topics");
                  }}
                  type="button"
                >
                  Clear Filters
                </button>
              </div>
            )}
            <ReadingFigureDialog figure={zoomed} onClose={() => setZoomed(null)} />
          </div>
        </div>
      )}
    </main>
  );
}
