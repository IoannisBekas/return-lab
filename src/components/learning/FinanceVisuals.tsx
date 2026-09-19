import { useId, useState, type ReactNode } from "react";
import "./FinanceVisuals.css";

const percent = (value: number) => `${(value * 100).toFixed(2)}%`;
const number = (value: number) => value.toLocaleString("en-US", { maximumFractionDigits: 2 });
const WIDTH = 600;
const HEIGHT = 240;

function Plot({ title, description, children, yLabel, yTicks, xLabel, xTicks }: {
  title: string;
  description: string;
  children: ReactNode;
  yLabel: string;
  yTicks: string[];
  xLabel: string;
  xTicks: string[];
}) {
  const id = useId();
  return (
    <div className="fv-plot">
      <p className="fv-axis-label">{yLabel}</p>
      <div className="fv-plot-body">
        <div className="fv-y-ticks" aria-hidden="true">{yTicks.map((tick, i) => <span key={i}>{tick}</span>)}</div>
        <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} role="img" aria-labelledby={`${id}-title`} aria-describedby={`${id}-desc`}>
          <title id={`${id}-title`}>{title}</title>
          <desc id={`${id}-desc`}>{description}</desc>
          {[0, 0.5, 1].map((ratio) => <line className="fv-grid-line" key={ratio} x1="0" x2={WIDTH} y1={ratio * HEIGHT} y2={ratio * HEIGHT} />)}
          <path className="fv-axis" d={`M0,0 V${HEIGHT} H${WIDTH}`} />
          {children}
        </svg>
        <div className="fv-x-ticks" aria-hidden="true">{xTicks.map((tick, i) => <span key={i}>{tick}</span>)}</div>
      </div>
      <p className="fv-axis-label fv-x-label">{xLabel}</p>
    </div>
  );
}

function DataTable({ caption, headers, rows }: { caption: string; headers: string[]; rows: (string | number)[][] }) {
  return (
    <details className="fv-data">
      <summary>View values as a table</summary>
      <div className="fv-table-scroll" tabIndex={0} role="region" aria-label={caption}>
        <table>
          <caption>{caption}</caption>
          <thead><tr>{headers.map((header) => <th scope="col" key={header}>{header}</th>)}</tr></thead>
          <tbody>{rows.map((row, i) => <tr key={i}>{row.map((cell, j) => j === 0 ? <th scope="row" key={j}>{cell}</th> : <td key={j}>{cell}</td>)}</tr>)}</tbody>
        </table>
      </div>
    </details>
  );
}

export type CashFlow = { period: number; amount: number; label: string };
export type CashFlowTimelineProps = {
  flows?: CashFlow[];
  title?: string;
  periodLabel?: string;
  valueLabel?: string;
};

const defaultFlows: CashFlow[] = [
  { period: 0, amount: -1000, label: "Initial investment" },
  { period: 1, amount: -500, label: "Additional contribution" },
  { period: 2, amount: 1800, label: "Final proceeds" },
];

/** Signed cash flows from the investor's perspective; equal dates are netted in the drawing. */
export function CashFlowTimeline({ flows = defaultFlows, title = "Put the cash flows on a timeline", periodLabel = "Year", valueLabel = "USD" }: CashFlowTimelineProps) {
  const id = useId();
  if (!flows.length || flows.some((flow) => !Number.isFinite(flow.period) || !Number.isFinite(flow.amount))) {
    return <p className="fv-message">Add at least one cash flow with a finite period and amount to display its timeline.</p>;
  }
  const totals = new Map<number, number>();
  flows.forEach(({ period, amount }) => totals.set(period, (totals.get(period) ?? 0) + amount));
  const points = [...totals].sort((a, b) => a[0] - b[0]);
  const first = points[0][0];
  const last = points[points.length - 1][0];
  const position = (period: number) => first === last ? 300 : 40 + (period - first) / (last - first) * 520;
  const description = points.map(([period, amount]) => `${periodLabel} ${period}: ${number(amount)} ${valueLabel}`).join(". ");
  return (
    <figure className="finance-visual">
      <figcaption><h3>{title}</h3><p>Read from the investor’s perspective: contributions are negative; money received is positive.</p></figcaption>
      <svg className="fv-timeline" viewBox="0 0 600 200" role="img" aria-labelledby={`${id}-title`} aria-describedby={`${id}-desc`}>
        <title id={`${id}-title`}>{title}</title>
        <desc id={`${id}-desc`}>{description}. Arrows show direction, not magnitude. Cash flows at the same time are combined.</desc>
        <defs><marker id={`${id}-arrow`} markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="currentColor" /></marker></defs>
        <line className="fv-axis" x1="20" x2="580" y1="100" y2="100" />
        {points.map(([period, amount]) => (
          <g key={period} className={amount < 0 ? "fv-outflow" : "fv-inflow"}>
            <circle cx={position(period)} cy="100" r="5" fill="currentColor" />
            {amount !== 0 && <line x1={position(period)} x2={position(period)} y1="100" y2={amount > 0 ? 30 : 170} stroke="currentColor" strokeWidth="3" markerEnd={`url(#${id}-arrow)`} />}
          </g>
        ))}
      </svg>
      <div className="fv-time-labels" aria-hidden="true">
        {points.filter((_, index) => points.length <= 8 || index === 0 || index === points.length - 1).map(([period]) => <span key={period} style={{ left: `${position(period) / 6}%` }}>{number(period)}</span>)}
      </div>
      <p className="fv-axis-label fv-x-label">Time ({periodLabel})</p>
      <ol className="fv-flow-list">
        {points.map(([period, amount]) => <li key={period}><span>{periodLabel} {number(period)}</span><strong>{amount > 0 ? "+" : ""}{number(amount)} {valueLabel}</strong><small>{amount < 0 ? "Paid out ↓" : amount > 0 ? "Received ↑" : "No net cash flow"}</small></li>)}
      </ol>
      <p className="fv-note">Horizontal spacing reflects time. Arrow length does not represent value; same-period cash flows are netted above.</p>
      <DataTable caption="Individual cash flows, before same-period netting" headers={[periodLabel, "Cash flow", `Amount (${valueLabel})`]} rows={flows.map((flow) => [flow.period, flow.label, number(flow.amount)])} />
    </figure>
  );
}

export type DurationPriceCurveProps = { faceValue?: number; couponRate?: number; maturityYears?: number; baseYield?: number };

function bondPrice(face: number, coupon: number, years: number, yieldRate: number) {
  return Array.from({ length: years }, (_, i) => (face * coupon + (i === years - 1 ? face : 0)) / (1 + yieldRate) ** (i + 1)).reduce((sum, cashFlow) => sum + cashFlow, 0);
}

export function DurationPriceCurve({ faceValue = 100, couponRate = 0.05, maturityYears = 10, baseYield = 0.05 }: DurationPriceCurveProps) {
  const [shockBps, setShockBps] = useState(0);
  const controlId = useId();
  if (![faceValue, couponRate, maturityYears, baseYield].every(Number.isFinite) || faceValue <= 0 || couponRate < 0 || !Number.isInteger(maturityYears) || maturityYears < 1 || maturityYears > 100 || baseYield <= -0.5 || baseYield > 1) {
    return <p className="fv-message">This annual-coupon model needs positive face value, a nonnegative coupon, 1–100 whole years, and a yield above −50% and at most 100%.</p>;
  }
  const currentPrice = bondPrice(faceValue, couponRate, maturityYears, baseYield);
  const weightedPresentValue = Array.from({ length: maturityYears }, (_, i) => (i + 1) * (faceValue * couponRate + (i === maturityYears - 1 ? faceValue : 0)) / (1 + baseYield) ** (i + 1)).reduce((sum, value) => sum + value, 0);
  const modifiedDuration = weightedPresentValue / currentPrice / (1 + baseYield);
  const radius = 0.02;
  const samples = Array.from({ length: 81 }, (_, i) => {
    const yieldRate = baseYield - radius + i / 80 * radius * 2;
    return { yieldRate, exact: bondPrice(faceValue, couponRate, maturityYears, yieldRate), estimate: currentPrice * (1 - modifiedDuration * (yieldRate - baseYield)) };
  });
  const allPrices = samples.flatMap((sample) => [sample.exact, sample.estimate]);
  const low = Math.min(...allPrices);
  const high = Math.max(...allPrices);
  const padding = (high - low) * 0.08;
  const bottom = low - padding;
  const top = high + padding;
  const x = (yieldRate: number) => (yieldRate - baseYield + radius) / (2 * radius) * WIDTH;
  const y = (price: number) => HEIGHT - (price - bottom) / (top - bottom) * HEIGHT;
  const path = (key: "exact" | "estimate") => samples.map((sample, i) => `${i ? "L" : "M"}${x(sample.yieldRate)},${y(sample[key])}`).join(" ");
  const selectedYield = baseYield + shockBps / 10000;
  const exact = bondPrice(faceValue, couponRate, maturityYears, selectedYield);
  const estimate = currentPrice * (1 - modifiedDuration * shockBps / 10000);
  return (
    <figure className="finance-visual">
      <figcaption><h3>Duration is a straight-line approximation</h3><p>Move the yield and compare the repriced bond with its duration estimate.</p></figcaption>
      <div className="fv-controls">
        <label htmlFor={controlId}>Yield change: <strong>{shockBps > 0 ? "+" : ""}{shockBps} basis points</strong></label>
        <input id={controlId} type="range" min="-200" max="200" step="10" value={shockBps} onChange={(event) => setShockBps(Number(event.target.value))} aria-valuetext={`${shockBps} basis points; yield ${percent(selectedYield)}`} />
        <button type="button" onClick={() => setShockBps(0)}>Reset yield</button>
      </div>
      <ul className="fv-legend"><li><span className="fv-swatch fv-solid" />Exact price</li><li><span className="fv-swatch fv-dashed" />Duration estimate</li><li>● Selected yield</li></ul>
      <Plot title="Bond price versus yield" description={`Annual ${percent(couponRate)} coupon, ${maturityYears} years remaining. The exact price curve is convex; the duration estimate is tangent at ${percent(baseYield)}. At ${percent(selectedYield)} yield, exact price is ${number(exact)} and the estimate is ${number(estimate)}.`} yLabel={`Price per ${number(faceValue)} face value`} yTicks={[number(top), number((top + bottom) / 2), number(bottom)]} xLabel="Annual yield to maturity" xTicks={[percent(baseYield - radius), percent(baseYield), percent(baseYield + radius)]}>
        <path className="fv-line fv-primary" d={path("exact")} />
        <path className="fv-line fv-comparison" d={path("estimate")} />
        <circle className="fv-selected" cx={x(selectedYield)} cy={y(exact)} r="6" />
      </Plot>
      <dl className="fv-results"><div><dt>Exact price</dt><dd>{number(exact)}</dd></div><div><dt>Duration estimate</dt><dd>{number(estimate)}</dd></div><div><dt>Modified duration</dt><dd>{number(modifiedDuration)} years</dd></div></dl>
      <p className="fv-note">Annual coupons, fixed cash flows, no embedded options; valuation is immediately after a coupon payment. ΔP/P ≈ −modified duration × Δyield. The yield change is entered as a decimal (100 bp = 0.01). The approximation can become unreliable for large changes.</p>
      <DataTable caption="Selected yield and bond valuation" headers={["Measure", "Value"]} rows={[["Yield", percent(selectedYield)], ["Exact price", number(exact)], ["Duration estimate", number(estimate)], ["Exact minus estimate", number(exact - estimate)], ["Exact price change", percent(exact / currentPrice - 1)]]} />
    </figure>
  );
}

export type EfficientFrontierProps = { returnA?: number; returnB?: number; volatilityA?: number; volatilityB?: number };

export function EfficientFrontier({ returnA = 0.06, returnB = 0.10, volatilityA = 0.10, volatilityB = 0.20 }: EfficientFrontierProps) {
  const [correlation, setCorrelation] = useState(0.2);
  const [weightB, setWeightB] = useState(50);
  const id = useId();
  if (![returnA, returnB, volatilityA, volatilityB].every(Number.isFinite) || returnA >= returnB || volatilityA <= 0 || volatilityB <= 0 || volatilityA > 1 || volatilityB > 1) {
    return <p className="fv-message">This two-asset example needs asset B’s expected return above asset A’s, with each volatility greater than 0% and at most 100%.</p>;
  }
  const portfolio = (weight: number) => ({
    risk: Math.sqrt(Math.max(0, (1 - weight) ** 2 * volatilityA ** 2 + weight ** 2 * volatilityB ** 2 + 2 * (1 - weight) * weight * correlation * volatilityA * volatilityB)),
    expectedReturn: (1 - weight) * returnA + weight * returnB,
  });
  const denominator = volatilityA ** 2 + volatilityB ** 2 - 2 * correlation * volatilityA * volatilityB;
  // With identical risk and perfect correlation, the higher-return endpoint dominates.
  const minimumWeight = denominator === 0 ? 1 : Math.max(0, Math.min(1, (volatilityA ** 2 - correlation * volatilityA * volatilityB) / denominator));
  const selected = portfolio(weightB / 100);
  const minimum = portfolio(minimumWeight);
  const maxRisk = Math.max(volatilityA, volatilityB) * 1.08;
  const padding = (returnB - returnA) * 0.15;
  const minReturn = returnA - padding;
  const maxReturn = returnB + padding;
  const x = (risk: number) => risk / maxRisk * WIDTH;
  const y = (expectedReturn: number) => HEIGHT - (expectedReturn - minReturn) / (maxReturn - minReturn) * HEIGHT;
  const curve = (start: number, end: number) => Array.from({ length: 101 }, (_, i) => {
    const point = portfolio(start + (end - start) * i / 100);
    return `${i ? "L" : "M"}${x(point.risk)},${y(point.expectedReturn)}`;
  }).join(" ");
  const efficient = weightB / 100 >= minimumWeight - 1e-9;
  return (
    <figure className="finance-visual">
      <figcaption><h3>Two assets, many possible portfolios</h3><p>Change correlation to see diversification. Then choose a weight and locate your portfolio.</p></figcaption>
      <div className="fv-controls">
        <label htmlFor={`${id}-correlation`}>Correlation: <strong>{correlation.toFixed(1)}</strong></label>
        <input id={`${id}-correlation`} type="range" min="-1" max="1" step="0.1" value={correlation} onChange={(event) => setCorrelation(Number(event.target.value))} />
        <label htmlFor={`${id}-weight`}>Asset B: <strong>{weightB}%</strong> · Asset A: {100 - weightB}%</label>
        <input id={`${id}-weight`} type="range" min="0" max="100" step="1" value={weightB} onChange={(event) => setWeightB(Number(event.target.value))} />
        <button type="button" onClick={() => { setCorrelation(0.2); setWeightB(50); }}>Reset portfolio</button>
      </div>
      <ul className="fv-legend"><li><span className="fv-swatch fv-solid" />Efficient segment</li><li><span className="fv-swatch fv-dashed" />Dominated segment</li><li>● Your portfolio</li><li>◇ Minimum variance</li></ul>
      <Plot title="Two-asset risk and return opportunity set" description={`Long-only portfolios of asset A and asset B with correlation ${correlation.toFixed(1)}. At ${weightB}% in B, expected return is ${percent(selected.expectedReturn)} and volatility is ${percent(selected.risk)}. The selected portfolio is ${efficient ? "on the efficient segment" : "dominated by another portfolio in this set"}. Minimum-variance weight in B is ${percent(minimumWeight)}.`} yLabel="Expected annual return" yTicks={[percent(maxReturn), percent((maxReturn + minReturn) / 2), percent(minReturn)]} xLabel="Annual volatility (standard deviation)" xTicks={["0%", percent(maxRisk / 2), percent(maxRisk)]}>
        <path className="fv-line fv-comparison" d={curve(0, minimumWeight)} />
        <path className="fv-line fv-primary" d={curve(minimumWeight, 1)} />
        <path className="fv-minimum" d={`M${x(minimum.risk)},${y(minimum.expectedReturn) - 8} l8,8 l-8,8 l-8,-8 Z`} />
        <circle className="fv-selected" cx={x(selected.risk)} cy={y(selected.expectedReturn)} r="6" />
      </Plot>
      <dl className="fv-results"><div><dt>Expected return</dt><dd>{percent(selected.expectedReturn)}</dd></div><div><dt>Volatility</dt><dd>{percent(selected.risk)}</dd></div><div><dt>Within this set</dt><dd>{efficient ? "Efficient segment" : "Dominated segment"}</dd></div></dl>
      <p className="fv-note">A: {percent(returnA)} expected return, {percent(volatilityA)} volatility. B: {percent(returnB)} expected return, {percent(volatilityB)} volatility. Weights sum to 100%; no short selling or risk-free asset. These are illustrative assumptions, not forecasts. “Efficient” describes only this two-asset set.</p>
      <DataTable caption="Two-asset portfolio examples at the selected correlation" headers={["Weight in B", "Expected return", "Volatility"]} rows={[0, 0.25, 0.5, 0.75, 1].map((weight) => { const point = portfolio(weight); return [percent(weight), percent(point.expectedReturn), percent(point.risk)]; })} />
    </figure>
  );
}

export type EthicsDecisionStep = { title: string; question: string; guidance: string };
export type EthicsDecisionFlowProps = { scenario?: string; steps?: EthicsDecisionStep[] };

const ethicsSteps: EthicsDecisionStep[] = [
  { title: "Establish the facts", question: "What is known, and what still needs verification?", guidance: "Separate evidence from assumptions. Identify the people affected, the timeline, and any information that is missing." },
  { title: "Identify duties", question: "Which obligations and conflicts are relevant?", guidance: "Consider duties to clients, employers, market integrity, and the profession. Identify the applicable standard and any legal or policy requirements." },
  { title: "Compare actions", question: "What could you do, and who could be affected?", guidance: "Compare feasible actions, including seeking advice, disclosure, declining the activity, or escalation. Disclosure alone does not resolve every conflict." },
  { title: "Act and document", question: "Which action best meets the relevant obligations?", guidance: "Explain the action using the verified facts and applicable duties. Record the reasons and consult appropriate guidance when uncertainty remains." },
  { title: "Reflect and follow up", question: "Did the action address the issue, and what should change?", guidance: "Review outcomes and new information. Consider whether procedures, communication, or further action are needed." },
];

export function EthicsDecisionFlow({ scenario = "An analyst receives a valuable gift from a company they cover immediately before publishing a research report.", steps = ethicsSteps }: EthicsDecisionFlowProps) {
  const [active, setActive] = useState(0);
  const id = useId();
  if (!steps.length) return <p className="fv-message">Add reasoning steps to display this decision guide.</p>;
  const selectedIndex = Math.min(active, steps.length - 1);
  const step = steps[selectedIndex];
  return (
    <figure className="finance-visual">
      <figcaption><h3>Reason through an ethical decision</h3><p>{scenario}</p></figcaption>
      <p className="fv-note">A reasoning guide, not an automated ruling. The facts, applicable duties and context determine the conclusion.</p>
      <ol className="fv-decision-flow" aria-label="Ethical reasoning steps">
        {steps.map((item, index) => <li key={index}><button type="button" aria-current={index === selectedIndex ? "step" : undefined} aria-controls={`${id}-panel`} onClick={() => setActive(index)}><span>{index + 1}</span>{item.title}</button></li>)}
      </ol>
      <section className="fv-decision-panel" id={`${id}-panel`} aria-labelledby={`${id}-question`} aria-live="polite" aria-atomic="true">
        <span className="fv-axis-label">Step {selectedIndex + 1} of {steps.length}</span>
        <h4 id={`${id}-question`}>{step.question}</h4><p>{step.guidance}</p>
      </section>
      <details className="fv-data"><summary>Read the complete reasoning sequence</summary><ol>{steps.map((item, index) => <li key={index}><strong>{item.title}: </strong>{item.question} {item.guidance}</li>)}</ol></details>
    </figure>
  );
}
