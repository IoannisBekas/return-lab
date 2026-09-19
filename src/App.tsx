import { useEffect, useMemo, useState } from "react";
import curriculumData from "./data/curriculum.json";

type ModuleLesson = {
  id: string;
  title: string;
  explanation: string;
  steps: string[];
  check: string;
};

type Reading = {
  number: number;
  slug: string;
  title: string;
  topic: string;
  overview: string;
  example: string;
  modules: ModuleLesson[];
};

const curriculum = curriculumData as Reading[];
const topicOrder = [...new Set(curriculum.map((reading) => reading.topic))];
const topicIcons = [0, 1, 2, 3, 4, 5, 6, 7, 0, 2];
const progressKey = "return-lab-progress-v2";
const asset = (path: string) =>
  `${import.meta.env.BASE_URL}${path.replace(/^\//, "")}`;

function readRoute() {
  const match = window.location.hash.match(/^#\/reading\/(\d+)/);
  return match ? Number(match[1]) : null;
}

function openReading(number: number) {
  window.location.hash = `/reading/${number}`;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function App() {
  const [readingNumber, setReadingNumber] = useState<number | null>(() =>
    readRoute(),
  );
  const [complete, setComplete] = useState<number[]>(() => {
    try {
      return JSON.parse(localStorage.getItem(progressKey) || "[]");
    } catch {
      return [];
    }
  });

  useEffect(() => {
    const updateRoute = () => setReadingNumber(readRoute());
    window.addEventListener("hashchange", updateRoute);
    return () => window.removeEventListener("hashchange", updateRoute);
  }, []);

  useEffect(() => {
    localStorage.setItem(progressKey, JSON.stringify(complete));
  }, [complete]);

  const toggleComplete = (number: number) => {
    setComplete((current) =>
      current.includes(number)
        ? current.filter((item) => item !== number)
        : [...current, number].sort((a, b) => a - b),
    );
  };

  const reading = curriculum.find((item) => item.number === readingNumber);

  return (
    <>
      <Header completed={complete.length} />
      {reading ? (
        <LessonPage
          complete={complete.includes(reading.number)}
          onToggleComplete={() => toggleComplete(reading.number)}
          reading={reading}
        />
      ) : (
        <HomePage complete={complete} />
      )}
      <Footer />
    </>
  );
}

function Header({ completed }: { completed: number }) {
  return (
    <header className="site-header">
      <a className="brand" href="#/" aria-label="Return Lab home">
        <img src={asset("assets/generated/brand-mark.png")} alt="" />
        <span>RETURN LAB</span>
      </a>
      <nav aria-label="Primary navigation">
        <a href="#curriculum">Curriculum</a>
        <a href="#topics">Topics</a>
        <a href="#progress">Progress</a>
      </nav>
      <div className="header-progress">
        <span>{completed}/93</span>
        <small>readings complete</small>
      </div>
    </header>
  );
}

function HomePage({ complete }: { complete: number[] }) {
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

  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">FINANCE / EXPLAINED AS A SYSTEM</p>
          <h1>Learn every measure behind the number.</h1>
          <p className="hero-intro">
            Ninety-three readings. One connected learning path. Each lesson
            turns the supplied curriculum outline into original explanations,
            a reasoning process, an applied example, and a knowledge check.
          </p>
          <div className="hero-actions">
            <button
              className="primary-action"
              onClick={() => openReading(nextReading?.number || 1)}
              type="button"
            >
              {complete.length ? "Continue learning" : "Start reading 01"}
              <span aria-hidden="true">→</span>
            </button>
            <a href="#curriculum">Explore all readings</a>
          </div>
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
              <dt>10</dt>
              <dd>connected topics</dd>
            </div>
          </dl>
        </div>
        <div className="hero-media">
          <video
            autoPlay
            loop
            muted
            playsInline
            poster={asset("assets/world/return-machine-poster.png")}
          >
            <source
              media="(max-width: 720px)"
              src={asset("assets/world/return-machine-mobile.mp4")}
              type="video/mp4"
            />
            <source src={asset("assets/world/return-machine.mp4")} type="video/mp4" />
          </video>
          <div className="orbit-label">A connected model of finance</div>
        </div>
      </section>

      <section className="progress-strip" id="progress">
        <div>
          <span className="section-code">YOUR PROGRESS</span>
          <strong>{Math.round((complete.length / 93) * 100)}%</strong>
        </div>
        <div className="progress-bar" aria-label={`${complete.length} of 93 readings complete`}>
          <span style={{ width: `${(complete.length / 93) * 100}%` }} />
        </div>
        <p>{complete.length} complete / {93 - complete.length} remaining</p>
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
            <h2>Every reading has a lesson.</h2>
          </div>
          <p>
            Search titles and module names, or focus the list by topic. The
            source books remain local; this repository contains an original
            educational treatment of their curriculum structure.
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
                <span>{reading.modules.length} taught {reading.modules.length === 1 ? "module" : "modules"}</span>
                <ul>
                  {reading.modules.slice(0, 3).map((module) => (
                    <li key={module.id}>{module.title}</li>
                  ))}
                </ul>
              </div>
              <div className="reading-actions">
                <span className={complete.includes(reading.number) ? "status done" : "status"}>
                  {complete.includes(reading.number) ? "Complete" : "Ready"}
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
          <strong>{reading.modules.length} taught {reading.modules.length === 1 ? "module" : "modules"}</strong>
        </div>
        <button
          className={complete ? "complete-action is-complete" : "complete-action"}
          onClick={onToggleComplete}
          type="button"
        >
          {complete ? "✓ Reading complete" : "Mark reading complete"}
        </button>
      </header>

      <div className="lesson-layout">
        <aside className="lesson-outline">
          <span className="section-code">IN THIS READING</span>
          <ol>
            <li><a href="#overview">Core idea</a></li>
            {reading.modules.map((module) => (
              <li key={module.id}><a href={`#module-${module.id}`}>{module.id} {module.title}</a></li>
            ))}
            {reading.number === 1 ? <li><a href="#return-lab">Interactive return lab</a></li> : null}
            <li><a href="#knowledge-check">Knowledge check</a></li>
          </ol>
        </aside>

        <div className="lesson-content">
          <section className="overview-card" id="overview">
            <span className="section-code">CORE IDEA</span>
            <h2>{reading.overview}</h2>
            <div>
              <p><strong>Why it matters</strong></p>
              <p>{reading.example}</p>
            </div>
          </section>

          {reading.modules.map((module, index) => (
            <section className="module-section" id={`module-${module.id}`} key={module.id}>
              <div className="module-heading">
                <span>{module.id}</span>
                <div>
                  <p>MODULE {index + 1} OF {reading.modules.length}</p>
                  <h2>{module.title}</h2>
                </div>
              </div>
              <p className="module-explanation">{module.explanation}</p>
              <div className="reasoning-grid">
                <article>
                  <span>HOW TO REASON</span>
                  <ol>
                    {module.steps.map((step) => <li key={step}>{step}</li>)}
                  </ol>
                </article>
                <article className="practice-card">
                  <span>PRACTICE PROMPT</span>
                  <p>{reading.example}</p>
                </article>
              </div>
              <details>
                <summary>Self-check</summary>
                <p>{module.check}</p>
              </details>
            </section>
          ))}

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
  const first = beforeFlow / Math.max(start, 0.01) - 1;
  const second = end / Math.max(beforeFlow + flow, 0.01) - 1;
  const twr = (1 + first) * (1 + second) - 1;
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
          <article><span>PERIOD 1</span><strong>{percent(first)}</strong></article>
          <article><span>PERIOD 2</span><strong>{percent(second)}</strong></article>
          <article className="featured-result"><span>CUMULATIVE TWR</span><strong>{percent(twr)}</strong></article>
        </div>
      </div>
    </section>
  );
}

function KnowledgeCheck({ reading }: { reading: Reading }) {
  const [answer, setAnswer] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);
  const choices = [
    reading.overview,
    "The reading is mainly a list of market prices with no decision framework.",
    "The result can be applied without defining inputs, assumptions, or limitations.",
  ];

  return (
    <section className="knowledge-check" id="knowledge-check">
      <span className="section-code">KNOWLEDGE CHECK</span>
      <h2>Which statement best captures this reading?</h2>
      <div className="answer-list">
        {choices.map((choice, index) => (
          <label className={answer === index ? "selected" : ""} key={choice}>
            <input
              checked={answer === index}
              name={`check-${reading.number}`}
              onChange={() => { setAnswer(index); setChecked(false); }}
              type="radio"
            />
            <span>{String.fromCharCode(65 + index)}</span>
            {choice}
          </label>
        ))}
      </div>
      <button disabled={answer === null} onClick={() => setChecked(true)} type="button">
        Check answer
      </button>
      {checked ? (
        <p className={answer === 0 ? "check-result correct" : "check-result"} role="status">
          {answer === 0
            ? "Correct. Now return to each module and test whether you can explain the process without the notes."
            : "Revisit the core idea. A useful analysis always defines its inputs, logic, purpose, and limits."}
        </p>
      ) : null}
    </section>
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
        An independent learning application with original explanations based
        on the curriculum structure supplied by the project owner.
      </p>
      <small>Source books and copied question banks are not stored in this repository.</small>
    </footer>
  );
}

export default App;
