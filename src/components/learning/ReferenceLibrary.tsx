import { useEffect, useMemo, useState } from "react";
import { ReadingBlocks, ReadingFigureDialog, type ContentBlock } from "./FullReading";
import { MathText } from "./MathText";
import "./ReferenceLibrary.css";

type ReferenceContent = {
  title: string;
  sections: { id: string; title: string; blocks: ContentBlock[] }[];
};

type FormulaFlashcard = {
  id: string;
  category: string;
  title: string;
  prompt: string;
  latex: string;
  variables: string;
  takeaway: string;
};

const FLASHCARDS: FormulaFlashcard[] = [
  {
    id: "tvm-ear",
    category: "Quantitative Methods",
    title: "Effective Annual Rate (EAR)",
    prompt: "How is the Effective Annual Rate computed from a stated annual rate with m compounding periods per year?",
    latex: "\\text{EAR} = \\left(1 + \\frac{r_s}{m}\\right)^{\\!m} - 1",
    variables: "r_s = stated annual interest rate; m = compounding frequency per year.",
    takeaway: "As compounding frequency increases, EAR increases. For continuous compounding: EAR = e^{r_s} - 1."
  },
  {
    id: "tvm-perpetuity",
    category: "Quantitative Methods",
    title: "Present Value of a Perpetuity",
    prompt: "What is the valuation formula for an ordinary constant perpetuity and a growing perpetuity?",
    latex: "PV = \\frac{PMT}{r} \\quad \\text{and} \\quad PV_0 = \\frac{PMT_1}{r - g}",
    variables: "PMT = constant periodic cash flow; r = discount rate; g = constant perpetual growth rate (r > g).",
    takeaway: "A perpetual preferred stock is valued as an ordinary perpetuity. Common stock dividends are modeled as a growing perpetuity (Gordon Growth Model)."
  },
  {
    id: "quant-harmonic",
    category: "Quantitative Methods",
    title: "Harmonic Mean",
    prompt: "How is the harmonic mean defined, and when is it most appropriately applied in finance?",
    latex: "\\overline{X}_H = \\frac{n}{\\sum_{i=1}^n \\frac{1}{X_i}}",
    variables: "n = number of observations; X_i = individual price or rate observations.",
    takeaway: "Harmonic Mean ≤ Geometric Mean ≤ Arithmetic Mean. The harmonic mean is standard for averaging cost per share under dollar-cost averaging."
  },
  {
    id: "quant-bayes",
    category: "Quantitative Methods",
    title: "Bayes' Formula",
    prompt: "How does Bayes' theorem update the prior probability of an event given new conditioning information?",
    latex: "P(A \\mid B) = \\frac{P(B \\mid A) \\times P(A)}{P(B)}",
    variables: "P(A) = prior probability; P(B | A) = likelihood of observing B given A; P(B) = total unconditional probability of B.",
    takeaway: "Allows analysts to revise earnings surprise or default forecasts upon observing subsequent company announcements."
  },
  {
    id: "econ-elasticity",
    category: "Economics",
    title: "Price Elasticity of Demand",
    prompt: "What is the formula for own-price elasticity of demand, and how does it determine revenue changes?",
    latex: "\\epsilon_{p} = \\frac{\\% \\Delta Q}{\\% \\Delta P} = \\frac{\\Delta Q}{\\Delta P} \\times \\frac{P}{Q}",
    variables: "Q = quantity demanded; P = market price; ΔQ/ΔP = slope derivative of the demand curve.",
    takeaway: "Demand is elastic when |ε| > 1 (price cut raises total revenue). Demand is inelastic when |ε| < 1 (price rise raises total revenue)."
  },
  {
    id: "econ-fiscal-multiplier",
    category: "Economics",
    title: "Fiscal Multiplier",
    prompt: "What is the fiscal spending multiplier formula accounting for income tax rates?",
    latex: "\\text{Fiscal Multiplier} = \\frac{1}{1 - \\text{MPC}(1 - t)}",
    variables: "MPC = marginal propensity to consume; t = marginal income tax rate.",
    takeaway: "Tax cuts and public spending stimulate GDP by a multiple greater than 1.0, dampened by higher savings rates or tax brackets."
  },
  {
    id: "fsa-dupont-3",
    category: "Financial Statement Analysis",
    title: "Three-Stage DuPont ROE Decomposition",
    prompt: "How does the traditional three-stage DuPont model break down Return on Equity?",
    latex: "\\text{ROE} = \\left(\\frac{\\text{Net Income}}{\\text{Revenue}}\\right) \\times \\left(\\frac{\\text{Revenue}}{\\text{Assets}}\\right) \\times \\left(\\frac{\\text{Assets}}{\\text{Equity}}\\right)",
    variables: "Net Profit Margin = Net Income / Revenue; Asset Turnover = Revenue / Assets; Financial Leverage = Assets / Equity.",
    takeaway: "Separates operational profitability, asset utilization efficiency, and financial balance sheet leverage."
  },
  {
    id: "fsa-dupont-5",
    category: "Financial Statement Analysis",
    title: "Five-Stage DuPont ROE Decomposition",
    prompt: "How does the five-stage DuPont model separate operating efficiency from financing and tax effects?",
    latex: "\\text{ROE} = \\frac{\\text{NI}}{\\text{EBT}} \\times \\frac{\\text{EBT}}{\\text{EBIT}} \\times \\frac{\\text{EBIT}}{\\text{Rev}} \\times \\frac{\\text{Rev}}{\\text{Assets}} \\times \\frac{\\text{Assets}}{\\text{Equity}}",
    variables: "Tax Burden × Interest Burden × Operating EBIT Margin × Asset Turnover × Financial Leverage.",
    takeaway: "Reveals whether high ROE is driven by genuine operating profitability or aggressive debt financing and tax benefits."
  },
  {
    id: "fsa-ccc",
    category: "Financial Statement Analysis",
    title: "Cash Conversion Cycle (CCC)",
    prompt: "What is the formula for the cash conversion cycle in days of working capital?",
    latex: "\\text{CCC} = \\text{DSO} + \\text{DOH} - \\text{DOP}",
    variables: "DSO = Days Sales Outstanding (365 / Receivables Turnover); DOH = Days of Inventory on Hand (365 / Inventory Turnover); DOP = Days of Payables (365 / Payables Turnover).",
    takeaway: "Measures the time elapsed between paying for inventory materials and collecting cash from customer receivables."
  },
  {
    id: "corp-wacc",
    category: "Corporate Issuers",
    title: "Weighted Average Cost of Capital (WACC)",
    prompt: "How is a company's overall weighted average cost of capital computed?",
    latex: "\\text{WACC} = w_d r_d (1 - t) + w_p r_p + w_e r_e",
    variables: "w = target market value weights; r_d = pre-tax cost of debt; t = marginal corporate tax rate; r_p = cost of preferred stock; r_e = cost of common equity.",
    takeaway: "Debt interest is tax-deductible under most regimes, creating an after-tax shield r_d(1 − t). Preferred stock and common equity dividends receive no tax deduction."
  },
  {
    id: "corp-dol",
    category: "Corporate Issuers",
    title: "Degree of Operating Leverage (DOL)",
    prompt: "What is the equation for the Degree of Operating Leverage at a given unit sales volume?",
    latex: "\\text{DOL} = \\frac{\\% \\Delta \\text{EBIT}}{\\% \\Delta \\text{Revenue}} = \\frac{Q(P - V)}{Q(P - V) - F}",
    variables: "Q = sales quantity; P = price per unit; V = variable cost per unit; F = fixed operating costs.",
    takeaway: "Higher fixed operating costs increase operating leverage, magnifying EBIT swings in response to shifts in revenue."
  },
  {
    id: "equity-ggm",
    category: "Equity Valuation",
    title: "Gordon Constant Growth Model",
    prompt: "How is the intrinsic value of a dividend-paying stock calculated under constant growth assumptions?",
    latex: "V_0 = \\frac{D_1}{r - g} = \\frac{D_0 (1 + g)}{r - g}",
    variables: "D_1 = expected dividend next year; r = required rate of return on equity; g = constant sustainable dividend growth rate (r > g).",
    takeaway: "Sustainable growth g = Retention Rate × ROE = (1 − Dividend Payout Ratio) × ROE."
  },
  {
    id: "equity-justified-pe",
    category: "Equity Valuation",
    title: "Justified Forward P/E Ratio",
    prompt: "What is the formula for the fundamental justified forward price-to-earnings ratio?",
    latex: "\\frac{P_0}{E_1} = \\frac{D_1 / E_1}{r - g} = \\frac{1 - b}{r - (\\text{ROE} \\times b)}",
    variables: "1 − b = dividend payout ratio; b = earnings retention rate; r = required return; g = sustainable growth rate.",
    takeaway: "The justified forward P/E is directly related to dividend payout and growth, and inversely related to the equity discount rate."
  },
  {
    id: "fi-bond-pv",
    category: "Fixed Income",
    title: "Bond Pricing Equation",
    prompt: "What is the fundamental discounting equation for a fixed-rate option-free bond?",
    latex: "PV = \\sum_{t=1}^n \\frac{PMT}{(1 + y)^t} + \\frac{FV}{(1 + y)^n}",
    variables: "PMT = coupon payment per period; FV = face par value; y = yield to maturity per period; n = total periods to maturity.",
    takeaway: "Bond price and yield have an inverse convex relationship. When coupon rate > YTM, bond trades at a premium; when coupon rate < YTM, bond trades at a discount."
  },
  {
    id: "fi-modified-duration",
    category: "Fixed Income",
    title: "Modified Duration & Percentage Price Change",
    prompt: "How is modified duration calculated from Macaulay duration, and how does it estimate price sensitivity?",
    latex: "\\text{ModDur} = \\frac{\\text{MacDur}}{1 + y/m} \\implies \\% \\Delta P \\approx -\\text{ModDur} \\times \\Delta y",
    variables: "MacDur = weighted average time to receipt of cash flows; y/m = periodic yield to maturity; Δy = yield change in decimal.",
    takeaway: "Provides a first-order linear approximation of bond price sensitivity to parallel yield curve shifts. Convexity adjustment refines larger shifts."
  },
  {
    id: "fi-approx-convexity",
    category: "Fixed Income",
    title: "Approximate Convexity",
    prompt: "What is the numerical approximation formula for bond convexity using price shocks?",
    latex: "\\text{Convexity} = \\frac{V_- + V_+ - 2V_0}{(\\Delta y)^2 V_0}",
    variables: "V_- = price after yield decrease; V_+ = price after yield increase; V_0 = baseline price; Δy = basis point yield change as a decimal.",
    takeaway: "Total estimated price change combining duration and convexity: %ΔP ≈ (−ModDur × Δy) + [0.5 × Convexity × (Δy)^2]."
  },
  {
    id: "fi-forward-rate",
    category: "Fixed Income",
    title: "Spot to Forward Rate Relationship",
    prompt: "What is the no-arbitrage relationship linking multi-period spot rates to implied forward rates?",
    latex: "(1 + s_B)^B = (1 + s_A)^A \\times \\left(1 + f_{A, B-A}\\right)^{B-A}",
    variables: "s_B = B-period zero-coupon spot rate; s_A = A-period spot rate (A < B); f_{A, B-A} = implied forward rate between year A and year B.",
    takeaway: "When the spot yield curve is upward sloping, implied forward rates exceed spot rates (f > s). When spot curve is inverted, forward rates lie below spot rates."
  },
  {
    id: "deriv-put-call-parity",
    category: "Derivatives",
    title: "Put-Call Parity for European Options",
    prompt: "What is the fundamental put-call parity relationship linking stock, bond, call, and put prices?",
    latex: "S_0 + P_0 = C_0 + \\frac{X}{(1 + r)^T}",
    variables: "S_0 = current underlying stock price; P_0 = European put price; C_0 = European call price; X = strike price; r = risk-free rate; T = time to expiration.",
    takeaway: "Fiduciary Call (Call + Zero-Coupon Bond) = Protective Put (Stock + Put). Prevents arbitrage and allows synthetic creation of any leg."
  },
  {
    id: "deriv-forward-price",
    category: "Derivatives",
    title: "Forward Contract Pricing",
    prompt: "How is the no-arbitrage forward price of an underlying asset with carry benefits and costs calculated?",
    latex: "F_0(T) = (S_0 - \\gamma + \\theta)(1 + r)^T",
    variables: "S_0 = spot price; γ = present value of cash flows/dividends; θ = present value of storage costs; r = annual risk-free rate; T = maturity in years.",
    takeaway: "The value of a forward contract at initiation is zero (V_0 = 0). The forward price F_0(T) is set so that no cash changes hands today."
  },
  {
    id: "pm-capm-sml",
    category: "Portfolio Management",
    title: "Capital Asset Pricing Model (CAPM)",
    prompt: "What is the equation of the Security Market Line (SML) expressing expected return as a function of systematic risk?",
    latex: "E(R_i) = R_f + \\beta_i \\left[E(R_m) - R_f\\right]",
    variables: "R_f = risk-free rate; β_i = asset beta; E(R_m) = expected return on the market portfolio; E(R_m) − R_f = market risk premium.",
    takeaway: "Only systematic risk (Beta) is priced by the market. Unsystematic (firm-specific) risk can be eliminated through diversification."
  },
  {
    id: "pm-beta",
    category: "Portfolio Management",
    title: "Asset Beta (β)",
    prompt: "How is an asset's beta derived from covariance with the market portfolio?",
    latex: "\\beta_i = \\frac{\\text{Cov}(R_i, R_m)}{\\sigma_m^2} = \\frac{\\rho_{i,m} \\sigma_i}{\\sigma_m}",
    variables: "Cov(R_i, R_m) = covariance between asset and market returns; σ_m^2 = market portfolio variance; ρ_{i,m} = correlation with the market; σ_i, σ_m = standard deviations.",
    takeaway: "A beta of 1.0 indicates average market risk. Beta > 1.0 indicates cyclical/high sensitivity; Beta < 1.0 indicates defensive characteristics."
  },
  {
    id: "pm-sharpe-ratio",
    category: "Portfolio Management",
    title: "Sharpe Ratio",
    prompt: "What is the formula for the Sharpe ratio, and which risk measure does it incorporate?",
    latex: "S_p = \\frac{R_p - R_f}{\\sigma_p}",
    variables: "R_p = portfolio mean return; R_f = risk-free rate; σ_p = total risk (standard deviation of portfolio return).",
    takeaway: "Measures excess return per unit of total risk. Appropriate for evaluating non-diversified portfolios or a client's entire wealth allocation."
  },
  {
    id: "pm-treynor-ratio",
    category: "Portfolio Management",
    title: "Treynor Ratio",
    prompt: "How is the Treynor ratio computed, and when is it preferred over the Sharpe ratio?",
    latex: "T_p = \\frac{R_p - R_f}{\\beta_p}",
    variables: "R_p = portfolio mean return; R_f = risk-free rate; β_p = systematic risk (Beta).",
    takeaway: "Measures excess return per unit of systematic risk. Appropriate when evaluating a portfolio intended to be added to an already well-diversified fund."
  },
  {
    id: "pm-jensen-alpha",
    category: "Portfolio Management",
    title: "Jensen's Alpha (α)",
    prompt: "What is the formula for Jensen's alpha, and how is it interpreted on the Security Market Line?",
    latex: "\\alpha_p = R_p - \\left(R_f + \\beta_p \\left[R_m - R_f\\right]\\right)",
    variables: "R_p = actual realized portfolio return; R_f + β_p[R_m − R_f] = CAPM required return for the portfolio's beta.",
    takeaway: "Alpha > 0 indicates manager outperformance (plots above SML). Alpha < 0 indicates underperformance relative to systematic risk."
  }
];

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

const STORAGE_KEY_MASTERED = "return-lab-mastered-flashcards-v1";

export default function ReferenceLibrary() {
  const [content, setContent] = useState<ReferenceContent | null>(null);
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [zoomed, setZoomed] = useState<ContentBlock | null>(null);

  // Tools state:
  const [mode, setMode] = useState<"browse" | "flashcards">("browse");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All Topics");

  // Flashcards state:
  const [cardIndex, setCardIndex] = useState(0);
  const [isRevealed, setIsRevealed] = useState(false);
  const [masteredIds, setMasteredIds] = useState<string[]>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY_MASTERED);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY_MASTERED, JSON.stringify(masteredIds));
    } catch {
      // Storage unavailable fallback
    }
  }, [masteredIds]);

  useEffect(() => {
    document.title = "Formula and Statistical Reference | Return Lab";
    const controller = new AbortController();
    setFailed(false);
    void fetch(`${import.meta.env.BASE_URL}content/reference.json`, { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error("Reference unavailable");
        const data = (await response.json()) as ReferenceContent;
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
    if (!content || mode !== "browse") return;
    const match = window.location.hash.match(/\/section\/([^/?#]+)/);
    if (!match) return;
    const frame = window.requestAnimationFrame(() =>
      document.getElementById(decodeURIComponent(match[1]))?.scrollIntoView()
    );
    return () => window.cancelAnimationFrame(frame);
  }, [content, mode]);

  // Flashcards filtered list:
  const filteredFlashcards = useMemo(() => {
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

  const activeCard = filteredFlashcards[cardIndex] || filteredFlashcards[0] || null;

  const toggleMastered = (id: string) => {
    setMasteredIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleNextCard = () => {
    setIsRevealed(false);
    setCardIndex((prev) => (prev + 1) % Math.max(1, filteredFlashcards.length));
  };

  const handlePrevCard = () => {
    setIsRevealed(false);
    setCardIndex((prev) =>
      prev === 0 ? Math.max(0, filteredFlashcards.length - 1) : prev - 1
    );
  };

  const handleShuffle = () => {
    setIsRevealed(false);
    const randomIndex = Math.floor(Math.random() * filteredFlashcards.length);
    setCardIndex(randomIndex);
  };

  // Filtered reference sections for browse mode:
  const filteredSections = useMemo(() => {
    if (!content) return [];
    const query = searchQuery.trim().toLowerCase();
    if (!query && selectedCategory === "All Topics") return content.sections;

    return content.sections
      .map((section) => {
        const matchesCategory =
          selectedCategory === "All Topics" ||
          section.title.toLowerCase().includes(selectedCategory.toLowerCase());

        const matchingBlocks = section.blocks.filter((b) => {
          if (!query) return true;
          const text = (b.text || "").toLowerCase();
          const prose = (b.prose || "").toLowerCase();
          const latex = (b.latex || "").toLowerCase();
          const alt = (b.alt || "").toLowerCase();
          return (
            text.includes(query) ||
            prose.includes(query) ||
            latex.includes(query) ||
            alt.includes(query)
          );
        });

        if (!matchesCategory && query.length === 0) return null;
        if (matchingBlocks.length === 0 && query.length > 0) return null;

        return {
          ...section,
          blocks: query.length > 0 ? matchingBlocks : section.blocks,
        };
      })
      .filter((s): s is NonNullable<typeof s> => s !== null);
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
              onClick={() => setMode("browse")}
              type="button"
            >
              📖 Browse Reference
            </button>
            <button
              className={`reference-mode-btn ${mode === "flashcards" ? "active" : ""}`}
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
        <div className="reference-chips" role="radiogroup" aria-label="Topic categories">
          {CATEGORIES.map((cat) => (
            <button
              className={`reference-chip ${selectedCategory === cat ? "active" : ""}`}
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
      </section>

      {searchQuery && (
        <p className="reference-search-summary" aria-live="polite">
          Searching for &ldquo;{searchQuery}&rdquo; &middot;{" "}
          {mode === "flashcards"
            ? `${filteredFlashcards.length} flashcard(s) match`
            : `${filteredSections.reduce((acc, s) => acc + s.blocks.length, 0)} formula block(s) match`}
        </p>
      )}

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
                  Card {cardIndex + 1} of {filteredFlashcards.length}
                </span>
                <span className="flashcard-mastery-count">
                  {masteredIds.filter((id) =>
                    filteredFlashcards.some((c) => c.id === id)
                  ).length}{" "}
                  / {filteredFlashcards.length} Mastered
                </span>
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
                  </div>
                )}

                <div className="flashcard-bottom-controls">
                  <div className="flashcard-rating-actions">
                    <button
                      className={`flashcard-rate-btn needs-review ${
                        !masteredIds.includes(activeCard.id) ? "active" : ""
                      }`}
                      onClick={() => {
                        if (masteredIds.includes(activeCard.id)) {
                          toggleMastered(activeCard.id);
                        }
                      }}
                      type="button"
                    >
                      Needs Review
                    </button>
                    <button
                      className={`flashcard-rate-btn mastered ${
                        masteredIds.includes(activeCard.id) ? "active" : ""
                      }`}
                      onClick={() => {
                        if (!masteredIds.includes(activeCard.id)) {
                          toggleMastered(activeCard.id);
                        }
                      }}
                      type="button"
                    >
                      &#10003; Mastered
                    </button>
                  </div>

                  <div className="flashcard-nav-buttons">
                    <button
                      disabled={filteredFlashcards.length <= 1}
                      onClick={handlePrevCard}
                      type="button"
                    >
                      &#8592; Previous
                    </button>
                    <button onClick={handleShuffle} type="button">
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
              <h3>No flashcards match your current filters.</h3>
              <p>Try clearing your search query or selecting &ldquo;All Topics&rdquo;.</p>
              <button
                onClick={() => {
                  setSearchQuery("");
                  setSelectedCategory("All Topics");
                }}
                type="button"
              >
                Reset Filters
              </button>
            </div>
          )}
        </section>
      ) : (
        /* Standard Browse Reference Mode */
        <div className="lesson-layout">
          <aside className="lesson-outline">
            <span className="section-code">REFERENCE SECTIONS</span>
            <ol>
              {filteredSections.map((section) => (
                <li key={section.id}>
                  <a href={`#/reference/section/${section.id}`}>{section.title}</a>
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
                    <ReadingBlocks blocks={section.blocks} onZoom={setZoomed} headingLevel={3} />
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
