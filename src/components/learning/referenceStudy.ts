import type { ContentBlock } from "./FullReading";

export type ReferenceEntry = {
  id: string;
  title: string;
  categories: string[];
  start: number;
  end: number;
  lessonHref: string;
};
export type ReferenceSection = { id: string; title: string; blocks: ContentBlock[]; entries: ReferenceEntry[] };
export type ReferenceContent = { title: string; sections: ReferenceSection[] };

// Search an entire entry so its equation, assumptions, and definitions stay together.
export function filterReferenceSections(content: ReferenceContent, query: string, category: string) {
  const term = query.trim().toLowerCase();
  return content.sections.map((section) => ({
    ...section,
    entries: section.entries.filter((entry) => {
      if (category !== "All Topics" && !entry.categories.includes(category)) return false;
      const text = [entry.title, ...entry.categories, ...section.blocks.slice(entry.start, entry.end)
        .flatMap((block) => [block.text, block.prose, block.latex, block.alt])].join(" ").toLowerCase();
      return !term || text.includes(term);
    }),
  })).filter((section) => section.entries.length > 0);
}

export type ReferenceRating = "again" | "hard" | "good";
export type ReferenceCardReview = { dueAt: number; intervalDays: number; reviews: number; lastRating: ReferenceRating };
export type ReferenceReviews = Record<string, ReferenceCardReview>;
export const REFERENCE_STUDY_EVENT = "return-lab-reference-study";
const STORAGE_KEY = "return-lab-reference-reviews-v1";
const LEGACY_KEY = "return-lab-mastered-flashcards-v1";
const DAY = 86_400_000;

export function readReferenceReviews(now = Date.now()): ReferenceReviews {
  try {
    const value: unknown = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if (value && typeof value === "object" && !Array.isArray(value)) {
      return Object.fromEntries(Object.entries(value).filter(([, item]) => item &&
        Number.isFinite(item.dueAt) && Number.isFinite(item.intervalDays) && item.intervalDays > 0 &&
        Number.isInteger(item.reviews) && item.reviews > 0 && ["again", "hard", "good"].includes(item.lastRating)));
    }
    const mastered: unknown = JSON.parse(localStorage.getItem(LEGACY_KEY) || "[]");
    if (!Array.isArray(mastered)) return {};
    const migrated: ReferenceReviews = Object.fromEntries(mastered.filter((id) => typeof id === "string").map((id) =>
      [id, { dueAt: now + 7 * DAY, intervalDays: 7, reviews: 1, lastRating: "good" }]));
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(migrated)); } catch { /* Continue without persistence. */ }
    return migrated;
  } catch { return {}; }
}

export function rateReferenceCard(reviews: ReferenceReviews, id: string, rating: ReferenceRating, now = Date.now()): ReferenceReviews {
  const previous = reviews[id];
  const intervalDays = rating === "again" ? 10 / (24 * 60) : rating === "hard" ? 1 :
    previous ? Math.min(60, Math.max(3, previous.intervalDays * 2)) : 3;
  return { ...reviews, [id]: { dueAt: now + intervalDays * DAY, intervalDays, reviews: (previous?.reviews || 0) + 1, lastRating: rating } };
}

export function saveReferenceReviews(reviews: ReferenceReviews) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(reviews)); } catch { /* Reviews remain usable for this session. */ }
  window.dispatchEvent(new Event(REFERENCE_STUDY_EVENT));
}

export function isReferenceCardDue(reviews: ReferenceReviews, id: string, now = Date.now()) {
  return !reviews[id] || reviews[id].dueAt <= now;
}

export function getReferenceDueCount(now = Date.now()) {
  const reviews = readReferenceReviews(now);
  return FLASHCARDS.filter((card) => isReferenceCardDue(reviews, card.id, now)).length;
}

export type FormulaFlashcard = {
  id: string;
  category: string;
  title: string;
  prompt: string;
  latex: string;
  variables: string;
  takeaway: string;
};

export const FLASHCARDS: FormulaFlashcard[] = [
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
