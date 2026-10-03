import { Component, lazy, Suspense, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import curriculumData from "./data/manifest.json";
import { getReadingProgress, rememberStudyPosition, readStudyState, studyPositionRoute, useStudyState } from "./lib/learning";

const GoldLesson = lazy(() => import("./components/learning/GoldLesson"));
const FullReading = lazy(() => import("./components/learning/FullReading"));
const ReferenceLibrary = lazy(() => import("./components/learning/ReferenceLibrary"));
const ReviewPage = lazy(() => import("./components/learning/ReviewPage"));
type AppRoute = number | "reference" | "review" | null;

type ModuleSummary = {
  id: string;
  title: string;
};

type Reading = {
  number: number;
  slug: string;
  title: string;
  topic: string;
  overview: string;
  chapterQuestionCount: number;
  modules: ModuleSummary[];
};

const curriculum = curriculumData as Reading[];
const topicOrder = [...new Set(curriculum.map((reading) => reading.topic))];
const topicIcons = [0, 1, 2, 3, 4, 5, 6, 7, 0, 2];
const progressKey = "return-lab-progress-v2";
const asset = (path: string) =>
  `${import.meta.env.BASE_URL}${path.replace(/^\//, "")}`;

function readCompletedReadings() {
  try {
    const stored: unknown = JSON.parse(localStorage.getItem(progressKey) || "[]");
    if (!Array.isArray(stored)) return [];
    return [...new Set(stored.filter(
      (value): value is number => Number.isInteger(value) && value >= 1 && value <= curriculum.length,
    ))].sort((a, b) => a - b);
  } catch {
    return [];
  }
}

class LessonErrorBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  render() {
    if (!this.state.failed) return this.props.children;
    return (
      <section className="deep-lesson-error" role="alert">
        <strong>The lesson file could not be loaded.</strong>
        <p>Your progress is safe. Check the connection and reload this reading.</p>
        <button type="button" onClick={() => window.location.reload()}>Retry lesson</button>
      </section>
    );
  }
}

function readRoute() {
  if (/^#\/reference(?:[/?]|$)/.test(window.location.hash)) return "reference";
  if (/^#\/review(?:[/?]|$)/.test(window.location.hash)) return "review";
  const match = window.location.hash.match(/^#\/reading\/(\d+)/);
  return match ? Number(match[1]) : null;
}

function readSection() {
  const match = window.location.hash.match(/\/section\/([^/?#]+)/);
  return match ? decodeURIComponent(match[1]) : null;
}

function scrollToRouteSection() {
  const section = readSection();
  if (!section) {
    window.scrollTo({ top: 0 });
    return;
  }

  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => {
      document.getElementById(section)?.scrollIntoView({ behavior: "smooth" });
    });
  });
}

function openReading(number: number) {
  window.location.hash = `/reading/${number}`;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function App() {
  const [readingNumber, setReadingNumber] = useState<AppRoute>(() =>
    readRoute(),
  );
  const reading = readingNumber === null
    ? null
    : curriculum.find((candidate) => candidate.number === readingNumber) || null;
  const [complete, setComplete] = useState<number[]>(readCompletedReadings);

  useEffect(() => {
    const updateRoute = () => {
      const route = readRoute();
      setReadingNumber(route);
      if (typeof route === "number") rememberStudyPosition(route, readSection() || undefined, new URLSearchParams(window.location.hash.split("?")[1]).get("question") || undefined);
      scrollToRouteSection();
    };
    window.addEventListener("hashchange", updateRoute);
    updateRoute();
    return () => window.removeEventListener("hashchange", updateRoute);
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(progressKey, JSON.stringify(complete));
    } catch {
      // Progress remains available for the current session when storage is blocked.
    }
  }, [complete]);

  const toggleComplete = (number: number) => {
    setComplete((current) =>
      current.includes(number)
        ? current.filter((item) => item !== number)
        : [...current, number].sort((a, b) => a - b),
    );
  };

  return (
    <>
      <Header completed={complete.length} />
      {readingNumber === "reference" ? (
        <LessonErrorBoundary><Suspense fallback={<p className="deep-lesson-loading" aria-live="polite">Loading the reference…</p>}><ReferenceLibrary /></Suspense></LessonErrorBoundary>
      ) : readingNumber === "review" ? (
        <LessonErrorBoundary><Suspense fallback={<p className="deep-lesson-loading" aria-live="polite">Preparing your review…</p>}><ReviewPage /></Suspense></LessonErrorBoundary>
      ) : readingNumber !== null && reading ? (
        <LessonPage
          key={reading.number}
          complete={complete.includes(reading.number)}
          onToggleComplete={() => toggleComplete(reading.number)}
          reading={reading}
        />
      ) : readingNumber !== null ? (
        <ReadingLoadState error={`Reading ${readingNumber} is not available.`} />
      ) : (
        <HomePage complete={complete} />
      )}
      <Footer />
    </>
  );
}

function ReadingLoadState({ error }: { error: string }) {
  return (
    <main className="reading-load-state" aria-live="polite">
      <span className="section-code">{error ? "READING UNAVAILABLE" : "LOADING LESSON"}</span>
      <h1>{error || "Preparing the reading…"}</h1>
      {error ? <a href="#/">Return to the curriculum</a> : null}
    </main>
  );
}

function Header({ completed }: { completed: number }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuButton = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    const close = () => setMenuOpen(false);
    const escape = (event: KeyboardEvent) => { if (event.key === "Escape" && menuButton.current?.getAttribute("aria-expanded") === "true") { close(); menuButton.current.focus(); } };
    window.addEventListener("hashchange", close);
    window.addEventListener("keydown", escape);
    return () => { window.removeEventListener("hashchange", close); window.removeEventListener("keydown", escape); };
  }, []);
  return (
    <header className="site-header">
      <a className="brand" href="#/" aria-label="Return Lab home">
        <img src={asset("assets/generated/brand-mark.png")} alt="" />
        <span>RETURN LAB</span>
      </a>
      <button ref={menuButton} className="mobile-menu-toggle" type="button" aria-expanded={menuOpen} aria-controls="primary-navigation" onClick={() => setMenuOpen((open) => !open)}>{menuOpen ? "Close menu" : "Menu"}</button>
      <nav id="primary-navigation" className={menuOpen ? "is-open" : ""} aria-label="Primary navigation" onClick={() => setMenuOpen(false)}>
        <a href="#/section/curriculum">Curriculum</a>
        <a href="#/section/topics">Topics</a>
        <a href="#/reference">Reference</a>
        <a href="#/review">Review</a>
        <a href="#/section/progress">Progress</a>
      </nav>
      <div className="header-progress">
        <span>{completed}/93</span>
        <small>readings read</small>
      </div>
    </header>
  );
}

function HomePage({ complete }: { complete: number[] }) {
  const study = useStudyState();
  const [query, setQuery] = useState("");
  const [topic, setTopic] = useState("All topics");

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return curriculum.filter((reading) => {
      const inTopic = topic === "All topics" || reading.topic === topic;
      const haystack = [
        reading.title,
        reading.topic,
        ...reading.modules.map((module) => module.title),
      ]
        .join(" ")
        .toLowerCase();
      return inTopic && (!needle || haystack.includes(needle));
    });
  }, [query, topic]);

  const nextReading = curriculum.find(
    (reading) => !complete.includes(reading.number),
  );
  const resumeReading = curriculum.find((reading) => reading.number === study.resume?.readingId);
  const dueReviews = Object.values(study.questions).filter((question) => question.dueAt <= Date.now()).length;
  const mastered = curriculum.filter((reading) => getReadingProgress(study, reading.number, complete.includes(reading.number)).status === "Mastered").length;

  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">FINANCE / EXPLAINED AS A SYSTEM</p>
          <h1>Learn every measure behind the number.</h1>
          <p className="hero-intro">
            Ninety-three readings. One connected learning path. Build your
            understanding with clear explanations, precise notation, worked
            examples, and practice with step-by-step feedback.
          </p>
          <div className="hero-actions">
            <button
              className="primary-action"
              onClick={() => { if (study.resume) window.location.hash = studyPositionRoute(study.resume).slice(1); else openReading(nextReading?.number || 1); }}
              type="button"
            >
              {resumeReading ? `Resume reading ${String(resumeReading.number).padStart(2, "0")}` : complete.length ? "Continue learning" : "Start reading 01"}
              <span aria-hidden="true">→</span>
            </button>
            <a href="#/section/curriculum">Explore all readings</a>
          </div>
          {resumeReading ? <p className="resume-context">{resumeReading.title}{study.resume?.questionId ? " · saved question" : study.resume?.sectionId ? " · saved section" : ""}</p> : null}
          <dl className="hero-stats">
            <div>
              <dt>93</dt>
              <dd>readings</dd>
            </div>
            <div>
              <dt>152</dt>
              <dd>taught modules</dd>
            </div>
            <div>
              <dt>365</dt>
              <dd>learning outcomes</dd>
            </div>
          </dl>
        </div>
        <HeroMedia />
      </section>

      <section className="progress-strip" id="progress">
        <div>
          <span className="section-code">YOUR PROGRESS</span>
          <strong>{Math.round((complete.length / 93) * 100)}%</strong>
        </div>
        <div className="progress-bar" aria-label={`${complete.length} of 93 readings read`}>
          <span style={{ width: `${(complete.length / 93) * 100}%` }} />
        </div>
        <p>{complete.length} read · {mastered} mastered<br /><a href="#/review">{dueReviews} question{dueReviews === 1 ? "" : "s"} due for review →</a></p>
      </section>
      <section className="study-dashboard" aria-label="Your study plan">
        <div><span className="section-code">YOUR NEXT SESSION</span><h2>{resumeReading ? resumeReading.title : "Start with a single module."}</h2><p>Study a module, check your understanding, then revisit the concepts that need practice.</p></div>
        <div className="study-dashboard-actions"><a className="primary-action" href={study.resume ? studyPositionRoute(study.resume) : "#/reading/1"}>{resumeReading ? "Resume saved position" : "Start learning"} →</a><a href="#/review">Review mistakes and due questions →</a><button type="button" onClick={() => openReading(nextReading?.number || 1)}>Next unread reading →</button></div>
      </section>

      <section className="topic-section" id="topics">
        <div className="section-heading">
          <p className="eyebrow">TEN TOPICS / ONE CURRICULUM</p>
          <h2>See how the sections connect.</h2>
        </div>
        <div className="topic-grid">
          {topicOrder.map((name, index) => {
            const readings = curriculum.filter((item) => item.topic === name);
            const completed = readings.filter((item) =>
              complete.includes(item.number),
            ).length;
            return (
              <button
                className={topic === name ? "topic-card selected" : "topic-card"}
                key={name}
                onClick={() => {
                  setTopic(topic === name ? "All topics" : name);
                  document.querySelector("#curriculum")?.scrollIntoView({
                    behavior: "smooth",
                  });
                }}
                type="button"
              >
                <img src={asset(`assets/icons/icon-${topicIcons[index]}.png`)} alt="" />
                <span>{String(readings.length).padStart(2, "0")} readings</span>
                <h3>{name}</h3>
                <small>{completed}/{readings.length} complete</small>
              </button>
            );
          })}
        </div>
      </section>

      <section className="curriculum-section" id="curriculum">
        <div className="curriculum-title">
          <div>
            <span className="section-code">FULL LEARNING PATH</span>
            <h2>Every reading has a deep lesson.</h2>
          </div>
          <p>
            Search titles and module names, or focus the list by topic.
            Work through the lessons in order or return to a concept you
            want to strengthen.
          </p>
        </div>

        <div className="curriculum-tools">
          <label>
            <span>Search the curriculum</span>
            <input
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Try duration, cash flow, ethics..."
              type="search"
              value={query}
            />
          </label>
          <label>
            <span>Topic</span>
            <select onChange={(event) => setTopic(event.target.value)} value={topic}>
              <option>All topics</option>
              {topicOrder.map((name) => <option key={name}>{name}</option>)}
            </select>
          </label>
          <button onClick={() => { setQuery(""); setTopic("All topics"); }} type="button">
            Clear filters
          </button>
        </div>

        <p className="result-count">Showing {filtered.length} of 93 readings</p>
        <div className="reading-list">
          {filtered.map((reading) => (
            <article className="reading-card" key={reading.number}>
              <div className="reading-number">
                {String(reading.number).padStart(2, "0")}
              </div>
              <div className="reading-body">
                <p>{reading.topic}</p>
                <h3>{reading.title}</h3>
                <span>
                  Complete lesson · guided practice
                </span>
                <ul>
                  {reading.modules.slice(0, 3).map((module) => (
                    <li key={module.id}>{module.title}</li>
                  ))}
                </ul>
              </div>
              <div className="reading-actions">
                <span className={getReadingProgress(study, reading.number, complete.includes(reading.number)).status === "Mastered" || complete.includes(reading.number) ? "status done" : "status"}>
                  {getReadingProgress(study, reading.number, complete.includes(reading.number)).status}
                </span>
                <button onClick={() => openReading(reading.number)} type="button">
                  Open lesson <span aria-hidden="true">→</span>
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

function LessonPage({
  reading,
  complete,
  onToggleComplete,
}: {
  reading: Reading;
  complete: boolean;
  onToggleComplete: () => void;
}) {
  const previous = curriculum[reading.number - 2];
  const next = curriculum[reading.number];
  const study = useStudyState();
  const progress = getReadingProgress(study, reading.number, complete);
  const [outlineOpen, setOutlineOpen] = useState(false);
  const [guidedOpen, setGuidedOpen] = useState(() => /\/section\/(deep-|assessment-|learning-lab)/.test(window.location.hash));

  useEffect(() => {
    const update = () => { if (/\/section\/(deep-|assessment-|learning-lab)/.test(window.location.hash)) setGuidedOpen(true); setOutlineOpen(false); };
    window.addEventListener("hashchange", update);
    let timer: ReturnType<typeof setTimeout>;
    const saveVisibleSection = () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        const sections = Array.from(document.querySelectorAll<HTMLElement>(".lesson-content [id]"))
          .filter((element) => /^(full-module-|deep-module-|assessment-|full-quiz$|full-review$|deep-assessment$|knowledge-check$|return-lab$|learning-lab$)/.test(element.id));
        const visible = sections.filter((element) => { const box = element.getBoundingClientRect(); return box.top <= 180 && box.bottom > 100; }).pop();
        if (visible) rememberStudyPosition(reading.number, visible.id, visible.id === "full-quiz" ? readStudyState().quizPositions[reading.number] : undefined);
      }, 350);
    };
    window.addEventListener("scroll", saveVisibleSection, { passive: true });
    return () => { clearTimeout(timer); window.removeEventListener("hashchange", update); window.removeEventListener("scroll", saveVisibleSection); };
  }, [reading.number]);

  useEffect(() => {
    document.title = `${String(reading.number).padStart(2, "0")} ${reading.title} | Return Lab`;
    return () => {
      document.title = "Return Lab | Finance Learning App";
    };
  }, [reading]);

  return (
    <main className="lesson-page">
      <a className="back-link" href="#/">← All readings</a>
      <header className="lesson-hero">
        <div className="lesson-index">{String(reading.number).padStart(2, "0")}</div>
        <div>
          <p>{reading.topic}</p>
          <h1>{reading.title}</h1>
          <strong>Complete lesson · guided practice</strong>
          <p className="reading-mastery-summary">{progress.status}{progress.total ? ` · ${progress.correct}/${progress.total} practice questions correct` : ""}</p>
        </div>
        <button
          className={complete ? "complete-action is-complete" : "complete-action"}
          onClick={onToggleComplete}
          type="button"
        >
          {complete ? "✓ Marked as read" : "Mark as read"}
        </button>
      </header>

      <div className="lesson-layout">
        <aside className="lesson-outline">
          <button className="lesson-outline-toggle" type="button" aria-expanded={outlineOpen} aria-controls="lesson-outline-links" onClick={() => setOutlineOpen((open) => !open)}>In this reading <span aria-hidden="true">{outlineOpen ? "−" : "+"}</span></button>
          <span className="section-code desktop-outline-heading">IN THIS READING</span>
          <ol id="lesson-outline-links" className={outlineOpen ? "is-open" : ""} onClick={() => setOutlineOpen(false)}>
            <li><a href={`#/reading/${reading.number}/section/overview`}>Core idea</a></li>
            <li><a href={`#/reading/${reading.number}/section/full-reading`}>Complete lesson</a></li>
            {reading.modules.map((module) => (
              <li key={module.id}><a href={`#/reading/${reading.number}/section/full-module-${module.id}`}>{module.id} {module.title}</a></li>
            ))}
            <li><a href={`#/reading/${reading.number}/section/full-quiz`}>Module quiz</a></li>
            <li><a href={`#/reading/${reading.number}/section/deep-dive`}>Guided examples and practice</a></li>
            <li><a href={`#/reading/${reading.number}/section/deep-assessment`}>Application check</a></li>
            {reading.number === 1 ? <li><a href={`#/reading/${reading.number}/section/return-lab`}>Interactive return lab</a></li> : null}
            {[70, 74, 75, 92].includes(reading.number) ? <li><a href={`#/reading/${reading.number}/section/learning-lab`}>Interactive learning lab</a></li> : null}
            <li><a href={`#/reading/${reading.number}/section/knowledge-check`}>Reflection check</a></li>
            <li><a href="#/reference">Formula and statistical reference</a></li>
            <li><a href="#/review">My review plan</a></li>
          </ol>
        </aside>

        <div className="lesson-content">
          <section className="overview-card" id="overview">
            <span className="section-code">CORE IDEA</span>
            <h2>{reading.overview}</h2>
            <div>
              <p><strong>What you will learn</strong></p>
              <p>
                {reading.modules.map((module) => module.title).join("; ")}. Explore the concepts, learn when each method applies, and put your understanding into practice.
              </p>
            </div>
          </section>

          <LessonErrorBoundary key={`full-${reading.number}`}>
            <Suspense fallback={<p className="deep-lesson-loading" aria-live="polite">Loading the complete reading…</p>}>
              <FullReading readingId={reading.number} />
            </Suspense>
          </LessonErrorBoundary>

          <section className="guided-study-toggle"><h2>Guided examples and application practice</h2><p>Work through examples, explore the interactive lab, and complete the application check. Mastery requires attempting both the module quiz and application check, with at least 80% correct.</p><button type="button" aria-expanded={guidedOpen} aria-controls="guided-study-content" onClick={() => setGuidedOpen((open) => !open)}>{guidedOpen ? "Hide guided practice" : "Open guided practice"}</button></section>
          {guidedOpen ? <div id="guided-study-content"><LessonErrorBoundary key={reading.number}>
            <Suspense fallback={<p className="deep-lesson-loading" aria-live="polite">Loading the lesson…</p>}>
              <GoldLesson readingId={reading.number} />
            </Suspense>
          </LessonErrorBoundary></div> : null}

          {reading.number === 1 ? <ReturnCalculator /> : null}
          <KnowledgeCheck reading={reading} />

          <nav className="lesson-pagination" aria-label="Reading navigation">
            {previous ? (
              <button onClick={() => openReading(previous.number)} type="button">
                <span>PREVIOUS</span>
                {previous.title}
              </button>
            ) : <span />}
            {next ? (
              <button onClick={() => openReading(next.number)} type="button">
                <span>NEXT</span>
                {next.title}
              </button>
            ) : <a href="#/">Return to curriculum</a>}
          </nav>
        </div>
      </div>
    </main>
  );
}

function ReturnCalculator() {
  const [start, setStart] = useState(1000);
  const [beforeFlow, setBeforeFlow] = useState(1100);
  const [flow, setFlow] = useState(900);
  const [end, setEnd] = useState(1800);
  const investedAfterFlow = beforeFlow + flow;
  const isValid =
    [start, beforeFlow, flow, end].every(Number.isFinite) &&
    start > 0 &&
    beforeFlow >= 0 &&
    investedAfterFlow > 0 &&
    end >= 0;
  const first = isValid ? beforeFlow / start - 1 : null;
  const second = isValid ? end / investedAfterFlow - 1 : null;
  const twr = first === null || second === null ? null : (1 + first) * (1 + second) - 1;
  const percent = (value: number) => `${(value * 100).toFixed(2)}%`;

  return (
    <section className="return-calculator" id="return-lab">
      <div>
        <span className="section-code">INTERACTIVE RETURN LAB</span>
        <h2>See how a cash flow changes the result.</h2>
      </div>
      <div className="calculator-grid">
        <div className="calculator-inputs">
          {[
            ["Starting value", start, setStart],
            ["Value before deposit", beforeFlow, setBeforeFlow],
            ["Deposit", flow, setFlow],
            ["Ending value", end, setEnd],
          ].map(([label, value, setter]) => (
            <label key={String(label)}>
              {String(label)}
              <input
                type="number"
                value={Number(value)}
                onChange={(event) => (setter as (value: number) => void)(Number(event.target.value))}
              />
            </label>
          ))}
        </div>
        <div className="calculator-results">
          {isValid && first !== null && second !== null && twr !== null ? (
            <>
              <article><span>PERIOD 1</span><strong>{percent(first)}</strong></article>
              <article><span>PERIOD 2</span><strong>{percent(second)}</strong></article>
              <article className="featured-result"><span>CUMULATIVE TWR</span><strong>{percent(twr)}</strong></article>
            </>
          ) : (
            <p className="calculator-error" role="alert">
              Enter a positive starting value and keep the portfolio value after the cash flow above zero. Returns are undefined when a period begins with no invested capital.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

function KnowledgeCheck({ reading }: { reading: Reading }) {
  const storageKey = `return-lab-retrieval-v1-${reading.number}`;
  const [response, setResponse] = useState(() => {
    try {
      return localStorage.getItem(storageKey) || "";
    } catch {
      return "";
    }
  });
  const [revealed, setRevealed] = useState(false);

  useEffect(() => {
    try {
      localStorage.setItem(storageKey, response);
    } catch {
      // The exercise still works when browser storage is unavailable.
    }
  }, [response, storageKey]);

  return (
    <section className="knowledge-check" id="knowledge-check">
      <span className="section-code">REFLECTION CHECK</span>
      <h2>Explain the reading without looking back.</h2>
      <p className="retrieval-prompt">
        In three to five sentences, explain how {reading.title.toLowerCase()} changes an analyst&apos;s decision. Include one method, one assumption, and one limitation.
      </p>
      <label className="retrieval-response">
        <span>Your explanation</span>
        <textarea
          onChange={(event) => {
            setResponse(event.target.value);
            setRevealed(false);
          }}
          rows={6}
          value={response}
        />
      </label>
      <button disabled={response.trim().length < 20} onClick={() => setRevealed(true)} type="button">
        Compare with the checklist
      </button>
      {revealed ? (
        <div className="check-result correct" role="status">
          <strong>Strong answers should include</strong>
          <ul>
            <li>{reading.overview}</li>
            <li>A named method from at least one module: {reading.modules.map((module) => module.title).join(", ")}.</li>
            <li>The inputs or assumptions that make the method valid and one reason the conclusion could change.</li>
          </ul>
        </div>
      ) : null}
    </section>
  );
}

function HeroMedia() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [reducedMotion] = useState(() => window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  const [paused, setPaused] = useState(reducedMotion);

  const togglePlayback = () => {
    const video = videoRef.current;
    if (!video) return;
    if (video.paused) {
      void video.play().then(() => setPaused(false));
    } else {
      video.pause();
      setPaused(true);
    }
  };

  return (
    <div className="hero-media">
      {reducedMotion ? (
        <img
          className="hero-poster"
          src={asset("assets/world/return-machine-poster.png")}
          alt="Abstract return machine connecting finance concepts"
        />
      ) : (
        <video
          autoPlay
          loop
          muted
          onPause={() => setPaused(true)}
          onPlay={() => setPaused(false)}
          playsInline
          poster={asset("assets/world/return-machine-poster.png")}
          ref={videoRef}
        >
          <source
            media="(max-width: 720px)"
            src={asset("assets/world/return-machine-mobile.mp4")}
            type="video/mp4"
          />
          <source src={asset("assets/world/return-machine.mp4")} type="video/mp4" />
        </video>
      )}
      {!reducedMotion ? (
        <button className="hero-media-control" onClick={togglePlayback} type="button">
          {paused ? "Play motion" : "Pause motion"}
        </button>
      ) : null}
      <div className="orbit-label">A connected model of finance</div>
    </div>
  );
}

function Footer() {
  return (
    <footer>
      <a className="brand" href="#/">
        <img src={asset("assets/generated/brand-mark.png")} alt="" />
        <span>RETURN LAB</span>
      </a>
      <p>
        An independent finance course with structured lessons, worked
        applications, practice sets, answer explanations, and progress tracking.
      </p>
      <small>93 readings · 152 modules · 365 learning outcomes<a className="reference-footer-link" href="#/reference">Formula and statistical reference ↗</a></small>
    </footer>
  );
}

export default App;
