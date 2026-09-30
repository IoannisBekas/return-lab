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

export function SupplyDemandExplorer() {
  const [demandShift, setDemandShift] = useState(0);
  const [supplyShift, setSupplyShift] = useState(0);
  const id = useId();
  const demandPrice = (quantity: number) => 120 + demandShift - quantity;
  const supplyPrice = (quantity: number) => 20 + supplyShift + quantity;
  const equilibriumQuantity = Math.max(0, Math.min(100, (100 + demandShift - supplyShift) / 2));
  const equilibriumPrice = demandPrice(equilibriumQuantity);
  const priceChange = equilibriumPrice - 70;
  const quantityChange = equilibriumQuantity - 50;
  const direction = (label: string, change: number) => `${label} ${change > 0 ? "higher" : change < 0 ? "lower" : "unchanged"}`;
  const changeSummary = `${direction("Price", priceChange)} · ${direction("quantity", quantityChange)}`;
  const x = (quantity: number) => quantity / 100 * WIDTH;
  const y = (price: number) => HEIGHT - price / 140 * HEIGHT;
  const demandPath = `M${x(0)},${y(demandPrice(0))} L${x(100)},${y(demandPrice(100))}`;
  const supplyPath = `M${x(0)},${y(supplyPrice(0))} L${x(100)},${y(supplyPrice(100))}`;
  return (
    <figure className="finance-visual">
      <figcaption><h3>Trace a shock through price and quantity</h3><p>Shift demand or supply, then separate the curve movement from the movement along the other curve.</p></figcaption>
      <div className="fv-controls">
        <label htmlFor={`${id}-demand`}>Demand shift: <strong>{demandShift > 0 ? "+" : ""}{demandShift}</strong></label>
        <input id={`${id}-demand`} type="range" min="-20" max="20" step="5" value={demandShift} onChange={(event) => setDemandShift(Number(event.target.value))} />
        <label htmlFor={`${id}-supply`}>Supply cost shift: <strong>{supplyShift > 0 ? "+" : ""}{supplyShift}</strong></label>
        <input id={`${id}-supply`} type="range" min="-20" max="20" step="5" value={supplyShift} onChange={(event) => setSupplyShift(Number(event.target.value))} />
        <button type="button" onClick={() => { setDemandShift(0); setSupplyShift(0); }}>Reset market</button>
      </div>
      <ul className="fv-legend"><li><span className="fv-swatch fv-solid" />Demand</li><li><span className="fv-swatch fv-dashed" />Supply</li><li>● Equilibrium</li></ul>
      <Plot title="Supply and demand equilibrium" description={`Illustrative linear curves. Equilibrium quantity is ${number(equilibriumQuantity)} and price is ${number(equilibriumPrice)} after a demand shift of ${demandShift} and a supply cost shift of ${supplyShift}.`} yLabel="Price" yTicks={["140", "70", "0"]} xLabel="Quantity" xTicks={["0", "50", "100"]}>
        <path className="fv-line fv-primary" d={demandPath} />
        <path className="fv-line fv-comparison" d={supplyPath} />
        <circle className="fv-selected" cx={x(equilibriumQuantity)} cy={y(equilibriumPrice)} r="6" />
      </Plot>
      <dl className="fv-results"><div><dt>Equilibrium price</dt><dd>{number(equilibriumPrice)}</dd></div><div><dt>Equilibrium quantity</dt><dd>{number(equilibriumQuantity)}</dd></div><div><dt>From baseline</dt><dd>{changeSummary}</dd></div></dl>
      <p className="fv-note">The curves are deliberately linear and dimensionless. Use them to reason about direction; do not treat the displayed values as an empirical forecast.</p>
      <DataTable caption="Selected illustrative equilibrium" headers={["Input or result", "Value"]} rows={[["Demand intercept shift", demandShift], ["Supply cost shift", supplyShift], ["Equilibrium price", number(equilibriumPrice)], ["Equilibrium quantity", number(equilibriumQuantity)]]} />
    </figure>
  );
}

export function CashFlowBridge() {
  const [netIncome, setNetIncome] = useState(100);
  const [noncashCharges, setNoncashCharges] = useState(20);
  const [workingCapitalIncrease, setWorkingCapitalIncrease] = useState(15);
  const id = useId();
  const operatingCashFlow = netIncome + noncashCharges - workingCapitalIncrease;
  return (
    <figure className="finance-visual">
      <figcaption><h3>Bridge accrual earnings to operating cash flow</h3><p>Change the inputs and follow why noncash charges are added back while an increase in operating working capital absorbs cash.</p></figcaption>
      <div className="fv-controls">
        <label htmlFor={`${id}-income`}>Net income: <strong>{number(netIncome)}</strong></label>
        <input id={`${id}-income`} type="range" min="20" max="180" step="5" value={netIncome} onChange={(event) => setNetIncome(Number(event.target.value))} />
        <label htmlFor={`${id}-noncash`}>Noncash charges: <strong>{number(noncashCharges)}</strong></label>
        <input id={`${id}-noncash`} type="range" min="0" max="60" step="5" value={noncashCharges} onChange={(event) => setNoncashCharges(Number(event.target.value))} />
        <label htmlFor={`${id}-working-capital`}>Change in operating working capital (increase +): <strong>{number(workingCapitalIncrease)}</strong></label>
        <input id={`${id}-working-capital`} type="range" min="-40" max="60" step="5" value={workingCapitalIncrease} onChange={(event) => setWorkingCapitalIncrease(Number(event.target.value))} />
        <button type="button" onClick={() => { setNetIncome(100); setNoncashCharges(20); setWorkingCapitalIncrease(15); }}>Reset bridge</button>
      </div>
      <div className="fv-bridge" role="img" aria-label={`Net income ${number(netIncome)}, plus noncash charges ${number(noncashCharges)}, minus the working capital change ${number(workingCapitalIncrease)}, equals operating cash flow ${number(operatingCashFlow)}.`}>
        <article><span>Start</span><strong>{number(netIncome)}</strong><small>Net income</small></article>
        <b aria-hidden="true">+</b>
        <article><span>Adjust</span><strong>{number(noncashCharges)}</strong><small>Noncash charges</small></article>
        <b aria-hidden="true">−</b>
        <article><span>Adjust</span><strong>{number(workingCapitalIncrease)}</strong><small>Change in working capital</small></article>
        <b aria-hidden="true">=</b>
        <article className="fv-bridge-result"><span>Result</span><strong>{number(operatingCashFlow)}</strong><small>Operating cash flow</small></article>
      </div>
      <p className="fv-note">Simplified indirect-method bridge: CFO = net income + noncash charges − change in operating working capital. A positive increase absorbs cash; a negative change is a decrease and releases cash. Classification differences, taxes, gains, losses, and other adjustments can matter in a full statement.</p>
      <DataTable caption="Operating cash flow bridge" headers={["Line", "Effect"]} rows={[["Net income", number(netIncome)], ["Add noncash charges", number(noncashCharges)], ["Subtract working-capital change", number(-workingCapitalIncrease)], ["Operating cash flow", number(operatingCashFlow)]]} />
    </figure>
  );
}

export type OptionStrategy = "call" | "put" | "covered-call" | "protective-put" | "bull-spread";

export function OptionPayoffExplorer() {
  const [strategy, setStrategy] = useState<OptionStrategy>("call");
  const [spot, setSpot] = useState(100);
  const id = useId();

  // Strategy payoff and profit models (underlying baseline $100):
  const strike = 100;
  const premium = 6;

  const calculateStrategy = (underlying: number, strat: OptionStrategy) => {
    if (strat === "call") {
      const intrinsic = Math.max(underlying - strike, 0);
      const profit = intrinsic - premium;
      return { intrinsic, profit };
    }
    if (strat === "put") {
      const intrinsic = Math.max(strike - underlying, 0);
      const profit = intrinsic - premium;
      return { intrinsic, profit };
    }
    if (strat === "covered-call") {
      // Long stock at 100 + Short call at K=105 (prem 4)
      const stockProfit = underlying - 100;
      const shortCallProfit = 4 - Math.max(underlying - 105, 0);
      const totalProfit = stockProfit + shortCallProfit;
      return { intrinsic: Math.max(0, underlying - 96), profit: totalProfit };
    }
    if (strat === "protective-put") {
      // Long stock at 100 + Long put at K=95 (prem 4)
      const stockProfit = underlying - 100;
      const longPutProfit = Math.max(95 - underlying, 0) - 4;
      const totalProfit = stockProfit + longPutProfit;
      return { intrinsic: Math.max(underlying - 95, 0), profit: totalProfit };
    }
    // Bull call spread: Long call K1=95 (prem 7) + Short call K2=105 (prem 2), net cost = 5
    const c1 = Math.max(underlying - 95, 0) - 7;
    const c2 = 2 - Math.max(underlying - 105, 0);
    const totalProfit = c1 + c2;
    return { intrinsic: Math.max(underlying - 95, 0) - Math.max(underlying - 105, 0), profit: totalProfit };
  };

  const samples = Array.from({ length: 101 }, (_, index) => {
    const underlying = 50 + index;
    return { underlying, value: calculateStrategy(underlying, strategy).profit };
  });

  const x = (underlying: number) => (underlying - 50) / 100 * WIDTH;
  const y = (value: number) => HEIGHT - (value + 20) / 70 * HEIGHT;
  const path = samples.map((sample, index) => `${index ? "L" : "M"}${x(sample.underlying)},${Math.max(0, Math.min(HEIGHT, y(sample.value)))}`).join(" ");

  const currentResult = calculateStrategy(spot, strategy);
  const selectedProfit = currentResult.profit;

  const metadata: Record<OptionStrategy, { title: string; breakeven: string; maxGain: string; maxLoss: string; description: string }> = {
    call: {
      title: "Long Call",
      breakeven: `${strike + premium}`,
      maxGain: "Unlimited",
      maxLoss: `−${premium}`,
      description: `Strike ${strike}, premium ${premium}. Profit turns positive when the underlying exceeds ${strike + premium}.`,
    },
    put: {
      title: "Long Put",
      breakeven: `${strike - premium}`,
      maxGain: `${strike - premium}`,
      maxLoss: `−${premium}`,
      description: `Strike ${strike}, premium ${premium}. Profit turns positive when the underlying drops below ${strike - premium}.`,
    },
    "covered-call": {
      title: "Covered Call (Long Stock + Short Call)",
      breakeven: "96",
      maxGain: "+9 (above 105)",
      maxLoss: "−96 (if stock hits 0)",
      description: "Generates income ($4 premium) while capping upside at strike $105. Downside is cushioned by the premium received.",
    },
    "protective-put": {
      title: "Protective Put (Long Stock + Long Put)",
      breakeven: "104",
      maxGain: "Unlimited",
      maxLoss: "−9 (below 95)",
      description: "Floors downside risk at strike $95 for an upfront cost of $4 premium. Preserves unlimited upside participation above $104.",
    },
    "bull-spread": {
      title: "Bull Call Spread (Long 95 Call / Short 105 Call)",
      breakeven: "100",
      maxGain: "+5 (above 105)",
      maxLoss: "−5 (below 95)",
      description: "Moderately bullish strategy with capped upside (+5) and strictly capped downside loss (−5), reducing upfront option cost.",
    },
  };

  const meta = metadata[strategy];

  return (
    <figure className="finance-visual">
      <figcaption>
        <h3>Interactive Option Payoffs & Strategies</h3>
        <p>Explore directional positions and multi-leg strategies. Observe how premium payments and strikes define breakeven points and risk profiles.</p>
      </figcaption>
      <div className="fv-controls">
        <div className="fv-segmented" role="group" aria-label="Option strategy">
          <button type="button" aria-pressed={strategy === "call"} onClick={() => setStrategy("call")}>Long call</button>
          <button type="button" aria-pressed={strategy === "put"} onClick={() => setStrategy("put")}>Long put</button>
          <button type="button" aria-pressed={strategy === "covered-call"} onClick={() => setStrategy("covered-call")}>Covered call</button>
          <button type="button" aria-pressed={strategy === "protective-put"} onClick={() => setStrategy("protective-put")}>Protective put</button>
          <button type="button" aria-pressed={strategy === "bull-spread"} onClick={() => setStrategy("bull-spread")}>Bull call spread</button>
        </div>
        <label htmlFor={`${id}-spot`}>Expiration price: <strong>{number(spot)}</strong></label>
        <input id={`${id}-spot`} type="range" min="50" max="150" step="1" value={spot} onChange={(event) => setSpot(Number(event.target.value))} />
        <button type="button" onClick={() => { setSpot(100); setStrategy("call"); }}>Reset position</button>
      </div>
      <Plot
        title={`${meta.title} profit at expiration`}
        description={`${meta.description} At an underlying price of ${spot}, net profit is ${number(selectedProfit)}.`}
        yLabel="Net Profit / Loss ($)"
        yTicks={["+50", "0", "−20"]}
        xLabel="Underlying Price at Expiration ($)"
        xTicks={["50", "100", "150"]}
      >
        <line className="fv-zero-line" x1="0" x2={WIDTH} y1={y(0)} y2={y(0)} />
        <path className="fv-line fv-primary" d={path} />
        <circle className="fv-selected" cx={x(spot)} cy={Math.max(0, Math.min(HEIGHT, y(selectedProfit)))} r="6" />
      </Plot>
      <dl className="fv-results">
        <div><dt>Net Profit / (Loss)</dt><dd>{number(selectedProfit)}</dd></div>
        <div><dt>Breakeven Point</dt><dd>${meta.breakeven}</dd></div>
        <div><dt>Risk / Return Profile</dt><dd>Max Gain: {meta.maxGain} · Max Loss: {meta.maxLoss}</dd></div>
      </dl>
      <p className="fv-note">European contracts evaluated strictly at expiration. Financing costs, transaction commissions, and intermediate early exercises are excluded for clean pedagogical comparison.</p>
      <DataTable
        caption="Strategy performance summary"
        headers={["Strategy", "Underlying Price", "Net Profit", "Breakeven", "Max Gain", "Max Loss"]}
        rows={[[meta.title, number(spot), number(selectedProfit), `$${meta.breakeven}`, meta.maxGain, meta.maxLoss]]}
      />
    </figure>
  );
}

export function SMLSecurityMarketLine() {
  const [rf, setRf] = useState(3.5);
  const [rm, setRm] = useState(9.5);
  const [beta, setBeta] = useState(1.2);
  const [forecastReturn, setForecastReturn] = useState(12.0);
  const id = useId();

  const marketPremium = rm - rf;
  const requiredReturn = rf + beta * marketPremium;
  const alpha = forecastReturn - requiredReturn;

  const maxBeta = 2.5;
  const maxReturn = 22.0;

  const x = (b: number) => (b / maxBeta) * WIDTH;
  const y = (ret: number) => HEIGHT - (ret / maxReturn) * HEIGHT;

  const smlPath = `M${x(0)},${y(rf)} L${x(maxBeta)},${y(rf + maxBeta * marketPremium)}`;

  const valuationStatus =
    alpha > 0.05
      ? { text: "Undervalued / Attractive (Alpha > 0)", class: "fv-positive", badge: "BUY / OVERWEIGHT" }
      : alpha < -0.05
      ? { text: "Overvalued / Costly (Alpha < 0)", class: "fv-negative", badge: "SELL / UNDERWEIGHT" }
      : { text: "Fairly Priced on SML (Alpha ≈ 0)", class: "fv-neutral", badge: "HOLD / NEUTRAL" };

  return (
    <figure className="finance-visual">
      <figcaption>
        <h3>Capital Asset Pricing Model & Security Market Line</h3>
        <p>Plot an asset against the Security Market Line (SML). Compare its forecasted return against the return required for its systematic risk (Beta).</p>
      </figcaption>
      <div className="fv-controls">
        <label htmlFor={`${id}-rf`}>Risk-free rate (R<sub>f</sub>): <strong>{rf.toFixed(1)}%</strong></label>
        <input id={`${id}-rf`} type="range" min="1.0" max="8.0" step="0.5" value={rf} onChange={(e) => setRf(Number(e.target.value))} />

        <label htmlFor={`${id}-rm`}>Expected market return E(R<sub>m</sub>): <strong>{rm.toFixed(1)}%</strong></label>
        <input id={`${id}-rm`} type="range" min="5.0" max="16.0" step="0.5" value={rm} onChange={(e) => setRm(Number(e.target.value))} />

        <label htmlFor={`${id}-beta`}>Asset systematic risk (Beta β): <strong>{beta.toFixed(2)}</strong></label>
        <input id={`${id}-beta`} type="range" min="0.0" max="2.5" step="0.1" value={beta} onChange={(e) => setBeta(Number(e.target.value))} />

        <label htmlFor={`${id}-forecast`}>Analyst forecast return E(R<sub>i</sub>): <strong>{forecastReturn.toFixed(1)}%</strong></label>
        <input id={`${id}-forecast`} type="range" min="1.0" max="20.0" step="0.5" value={forecastReturn} onChange={(e) => setForecastReturn(Number(e.target.value))} />

        <button type="button" onClick={() => { setRf(3.5); setRm(9.5); setBeta(1.2); setForecastReturn(12.0); }}>
          Reset SML parameters
        </button>
      </div>

      <ul className="fv-legend">
        <li><span className="fv-swatch fv-solid" />Security Market Line (SML)</li>
        <li><span className="fv-swatch fv-dashed" />Required return reference</li>
        <li>● Market Portfolio (β = 1.0)</li>
        <li>◆ Evaluated Asset</li>
      </ul>

      <Plot
        title="Security Market Line (SML)"
        description={`SML with Rf = ${rf}%, Rm = ${rm}%, Market Risk Premium = ${marketPremium.toFixed(1)}%. Asset Beta is ${beta.toFixed(2)}, required return is ${requiredReturn.toFixed(2)}%, forecast return is ${forecastReturn.toFixed(2)}%, and Jensen's alpha is ${alpha > 0 ? "+" : ""}${alpha.toFixed(2)}%.`}
        yLabel="Expected / Required Return (%)"
        yTicks={[`${maxReturn.toFixed(0)}%`, `${(maxReturn / 2).toFixed(0)}%`, "0%"]}
        xLabel="Systematic Risk (Beta β)"
        xTicks={["0.0", "1.0 (Market)", `${maxBeta.toFixed(1)}`]}
      >
        <path className="fv-line fv-primary" d={smlPath} />
        {/* Market Portfolio dot at (1.0, rm) */}
        <circle cx={x(1.0)} cy={y(rm)} r="5" fill="#285d70" />
        <line x1={x(beta)} x2={x(beta)} y1={HEIGHT} y2={y(forecastReturn)} stroke="#485257" strokeDasharray="3 3" />
        <line x1="0" x2={x(beta)} y1={y(requiredReturn)} y2={y(requiredReturn)} stroke="#a52f45" strokeDasharray="3 3" />
        {/* Evaluated asset diamond */}
        <path
          d={`M${x(beta)},${y(forecastReturn) - 7} l7,7 l-7,7 l-7,-7 Z`}
          fill={alpha >= 0 ? "#137333" : "#c5221f"}
          stroke="#fff"
          strokeWidth="1.5"
        />
      </Plot>

      <dl className="fv-results">
        <div><dt>CAPM Required Return (k<sub>i</sub>)</dt><dd>{requiredReturn.toFixed(2)}%</dd></div>
        <div><dt>Jensen&apos;s Alpha (α)</dt><dd>{alpha > 0 ? "+" : ""}{alpha.toFixed(2)}%</dd></div>
        <div>
          <dt>Valuation Assessment</dt>
          <dd><span className={`fv-alpha-badge ${valuationStatus.class}`}>{valuationStatus.badge}</span></dd>
        </div>
      </dl>

      <p className="fv-note">
        <strong>Takeaway:</strong> Assets plotting <em>above</em> the SML provide higher return than required for their systematic risk and are <strong>undervalued</strong>. Assets plotting <em>below</em> the SML offer insufficient return for their beta and are <strong>overvalued</strong>.
      </p>

      <DataTable
        caption="SML and Asset Parameters"
        headers={["Parameter", "Symbol / Formula", "Value"]}
        rows={[
          ["Risk-Free Rate", "R_f", `${rf.toFixed(2)}%`],
          ["Market Expected Return", "E(R_m)", `${rm.toFixed(2)}%`],
          ["Market Risk Premium", "E(R_m) − R_f", `${marketPremium.toFixed(2)}%`],
          ["Asset Beta", "β_i", beta.toFixed(2)],
          ["Required Return", "R_f + β_i × [E(R_m) − R_f]", `${requiredReturn.toFixed(2)}%`],
          ["Forecast Return", "E(R_i)", `${forecastReturn.toFixed(2)}%`],
          ["Jensen's Alpha", "E(R_i) − k_i", `${alpha > 0 ? "+" : ""}${alpha.toFixed(2)}%`],
          ["Conclusion", "Pricing Status", valuationStatus.text],
        ]}
      />
    </figure>
  );
}

export function YieldCurveTermStructure() {
  const [curveType, setCurveType] = useState<"normal" | "inverted" | "flat" | "humped">("normal");
  const [shiftBps, setShiftBps] = useState(0);
  const id = useId();

  const baseSpots: Record<string, number[]> = {
    normal: [3.2, 3.6, 4.0, 4.4, 4.7, 5.0, 5.3, 5.5],
    inverted: [5.5, 5.1, 4.7, 4.3, 4.0, 3.8, 3.7, 3.6],
    flat: [4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5],
    humped: [3.5, 4.8, 5.1, 4.9, 4.6, 4.3, 4.1, 4.0],
  };

  const maturities = [1, 2, 3, 5, 7, 10, 20, 30];
  const spotRates = baseSpots[curveType].map((rate) => rate + shiftBps / 100);

  // Calculate 1-year forward rates: f(t-1, 1) = [(1 + s_t)^t / (1 + s_{t-1})^{t-1}] - 1
  const forwards = spotRates.map((s, idx) => {
    if (idx === 0) return s;
    const t = maturities[idx];
    const prevT = maturities[idx - 1];
    const prevS = spotRates[idx - 1];
    const compoundT = Math.pow(1 + s / 100, t);
    const compoundPrev = Math.pow(1 + prevS / 100, prevT);
    const annualizedFwd = (Math.pow(compoundT / compoundPrev, 1 / (t - prevT)) - 1) * 100;
    return annualizedFwd;
  });

  const slope2_10 = (spotRates[5] - spotRates[1]) * 100; // 10Y minus 2Y in bps
  const fwd1y1y = ((Math.pow(1 + spotRates[1] / 100, 2) / (1 + spotRates[0] / 100)) - 1) * 100;

  const minRate = 1.0;
  const maxRate = 8.0;

  const x = (tenor: number) => (Math.log(tenor) / Math.log(30)) * WIDTH;
  const y = (rate: number) => HEIGHT - ((rate - minRate) / (maxRate - minRate)) * HEIGHT;

  const spotPath = spotRates.map((r, i) => `${i ? "L" : "M"}${x(maturities[i])},${y(r)}`).join(" ");
  const forwardPath = forwards.map((r, i) => `${i ? "L" : "M"}${x(maturities[i])},${Math.max(0, Math.min(HEIGHT, y(r)))}`).join(" ");

  const curveDescriptions: Record<string, string> = {
    normal: "Upward sloping: Long-term yields exceed short-term rates due to positive maturity/term premium and healthy economic expansion expectations.",
    inverted: "Inverted: Short-term rates exceed long-term yields. Historically a reliable harbinger of economic deceleration or monetary policy tightening.",
    flat: "Flat: Yields are uniform across tenors, often reflecting transitional monetary phases between tightening and easing cycles.",
    humped: "Humped: Intermediate yields peak above both short- and long-term rates, reflecting medium-term inflation pressure or expected rate hikes followed by cuts.",
  };

  return (
    <figure className="finance-visual">
      <figcaption>
        <h3>Term Structure of Interest Rates & Implied Forwards</h3>
        <p>Explore yield curve shapes and shifts. Follow how spot rate curves imply forward rates via no-arbitrage relationships.</p>
      </figcaption>
      <div className="fv-controls">
        <div className="fv-segmented" role="group" aria-label="Yield curve shape">
          <button type="button" aria-pressed={curveType === "normal"} onClick={() => setCurveType("normal")}>Normal</button>
          <button type="button" aria-pressed={curveType === "inverted"} onClick={() => setCurveType("inverted")}>Inverted</button>
          <button type="button" aria-pressed={curveType === "flat"} onClick={() => setCurveType("flat")}>Flat</button>
          <button type="button" aria-pressed={curveType === "humped"} onClick={() => setCurveType("humped")}>Humped</button>
        </div>
        <label htmlFor={`${id}-shift`}>Parallel curve shift: <strong>{shiftBps > 0 ? "+" : ""}{shiftBps} bps</strong></label>
        <input id={`${id}-shift`} type="range" min="-150" max="150" step="10" value={shiftBps} onChange={(e) => setShiftBps(Number(e.target.value))} />
        <button type="button" onClick={() => { setCurveType("normal"); setShiftBps(0); }}>Reset curve</button>
      </div>

      <ul className="fv-legend">
        <li><span className="fv-swatch fv-solid" />Spot Yield Curve</li>
        <li><span className="fv-swatch fv-dashed" style={{ borderColor: "#d97706" }} />Implied Forward Rates</li>
      </ul>

      <Plot
        title="Yield Curve and Forward Rates"
        description={`${curveDescriptions[curveType]} At 2Y spot rate ${spotRates[1].toFixed(2)}% and 10Y spot rate ${spotRates[5].toFixed(2)}%, the 2Y-10Y slope is ${slope2_10.toFixed(0)} bps.`}
        yLabel="Annualized Yield (%)"
        yTicks={[`${maxRate.toFixed(1)}%`, `${((maxRate + minRate) / 2).toFixed(1)}%`, `${minRate.toFixed(1)}%`]}
        xLabel="Maturity Tenor (Logarithmic Scale)"
        xTicks={["1Y", "5Y", "30Y"]}
      >
        <path className="fv-line fv-primary" d={spotPath} />
        <path className="fv-line fv-forward-line" d={forwardPath} />
        {maturities.map((tenor, i) => (
          <circle key={tenor} cx={x(tenor)} cy={y(spotRates[i])} r="4" fill="#285d70" />
        ))}
      </Plot>

      <dl className="fv-results">
        <div><dt>2Y / 10Y Slope Spread</dt><dd>{slope2_10 > 0 ? "+" : ""}{slope2_10.toFixed(0)} bps</dd></div>
        <div><dt>1Y Implied Forward Rate (1y1y)</dt><dd>{fwd1y1y.toFixed(2)}%</dd></div>
        <div><dt>Market Curve Status</dt><dd>{curveType.toUpperCase()}</dd></div>
      </dl>

      <p className="fv-note">
        <strong>Interpretation:</strong> When the spot curve is upward sloping, implied forward rates lie <em>above</em> the spot curve (forward rate &gt; spot rate). When the spot curve is inverted, forward rates lie <em>below</em> spot rates.
      </p>

      <DataTable
        caption="Spot Rates and Implied Forward Rates by Maturity"
        headers={["Maturity", "Spot Rate", "Implied Forward Rate"]}
        rows={maturities.map((m, i) => [
          `${m} Year${m > 1 ? "s" : ""}`,
          `${spotRates[i].toFixed(2)}%`,
          `${forwards[i].toFixed(2)}%`,
        ])}
      />
    </figure>
  );
}

export function DuPontDecomposition() {
  const [taxBurden, setTaxBurden] = useState(0.75);
  const [interestBurden, setInterestBurden] = useState(0.85);
  const [ebitMargin, setEbitMargin] = useState(0.12);
  const [assetTurnover, setAssetTurnover] = useState(1.10);
  const [financialLeverage, setFinancialLeverage] = useState(2.20);
  const id = useId();

  const operatingROA = ebitMargin * assetTurnover;
  const netProfitMargin = taxBurden * interestBurden * ebitMargin;
  const roa = netProfitMargin * assetTurnover;
  const roe = roa * financialLeverage;

  return (
    <figure className="finance-visual">
      <figcaption>
        <h3>Five-Stage DuPont Analysis Framework</h3>
        <p>Decompose Return on Equity (ROE) into operational efficiency, asset utilization, tax efficiency, and financial leverage.</p>
      </figcaption>

      <div className="fv-controls">
        <label htmlFor={`${id}-tax`}>Tax Burden (Net Income / EBT): <strong>{taxBurden.toFixed(2)}</strong></label>
        <input id={`${id}-tax`} type="range" min="0.50" max="0.95" step="0.01" value={taxBurden} onChange={(e) => setTaxBurden(Number(e.target.value))} />

        <label htmlFor={`${id}-interest`}>Interest Burden (EBT / EBIT): <strong>{interestBurden.toFixed(2)}</strong></label>
        <input id={`${id}-interest`} type="range" min="0.50" max="1.00" step="0.01" value={interestBurden} onChange={(e) => setInterestBurden(Number(e.target.value))} />

        <label htmlFor={`${id}-margin`}>EBIT Operating Margin (EBIT / Revenue): <strong>{(ebitMargin * 100).toFixed(1)}%</strong></label>
        <input id={`${id}-margin`} type="range" min="0.02" max="0.30" step="0.01" value={ebitMargin} onChange={(e) => setEbitMargin(Number(e.target.value))} />

        <label htmlFor={`${id}-turnover`}>Asset Turnover (Revenue / Assets): <strong>{assetTurnover.toFixed(2)}x</strong></label>
        <input id={`${id}-turnover`} type="range" min="0.30" max="3.00" step="0.05" value={assetTurnover} onChange={(e) => setAssetTurnover(Number(e.target.value))} />

        <label htmlFor={`${id}-leverage`}>Financial Leverage (Assets / Equity): <strong>{financialLeverage.toFixed(2)}x</strong></label>
        <input id={`${id}-leverage`} type="range" min="1.00" max="5.00" step="0.10" value={financialLeverage} onChange={(e) => setFinancialLeverage(Number(e.target.value))} />

        <button
          type="button"
          onClick={() => {
            setTaxBurden(0.75);
            setInterestBurden(0.85);
            setEbitMargin(0.12);
            setAssetTurnover(1.10);
            setFinancialLeverage(2.20);
          }}
        >
          Reset DuPont parameters
        </button>
      </div>

      <div className="fv-dupont-flow">
        <div className="fv-dupont-factor">
          <span>1. Tax Burden</span>
          <strong>{taxBurden.toFixed(2)}</strong>
          <small>Net Income / EBT (Retention of earnings after taxes)</small>
        </div>
        <div className="fv-dupont-factor">
          <span>2. Interest Burden</span>
          <strong>{interestBurden.toFixed(2)}</strong>
          <small>EBT / EBIT (Share of operating profit left after interest)</small>
        </div>
        <div className="fv-dupont-factor">
          <span>3. EBIT Margin</span>
          <strong>{(ebitMargin * 100).toFixed(1)}%</strong>
          <small>EBIT / Revenue (Core operating profitability)</small>
        </div>
        <div className="fv-dupont-factor">
          <span>4. Asset Turnover</span>
          <strong>{assetTurnover.toFixed(2)}x</strong>
          <small>Revenue / Assets (Efficiency in generating revenue)</small>
        </div>
        <div className="fv-dupont-factor">
          <span>5. Leverage</span>
          <strong>{financialLeverage.toFixed(2)}x</strong>
          <small>Assets / Equity (Balance sheet leverage multiplier)</small>
        </div>
        <div className="fv-dupont-factor fv-dupont-hero">
          <span>Result: ROE</span>
          <strong>{(roe * 100).toFixed(2)}%</strong>
          <small>Return on Equity = Factor 1 × 2 × 3 × 4 × 5</small>
        </div>
      </div>

      <dl className="fv-results">
        <div><dt>Operating ROA (EBIT Margin × Turnover)</dt><dd>{(operatingROA * 100).toFixed(2)}%</dd></div>
        <div><dt>Net Profit Margin (Tax × Interest × EBIT Margin)</dt><dd>{(netProfitMargin * 100).toFixed(2)}%</dd></div>
        <div><dt>Return on Assets (ROA)</dt><dd>{(roa * 100).toFixed(2)}%</dd></div>
      </dl>

      <p className="fv-note">
        <strong>Strategic Insight:</strong> A company can boost ROE through higher margins, faster asset turnover, or greater financial leverage. However, leverage increases debt service risks, while margin and turnover improvements reflect genuine operational excellence.
      </p>

      <DataTable
        caption="DuPont Five-Factor Calculation Table"
        headers={["Step / Component", "Ratio Formula", "Metric Value"]}
        rows={[
          ["1. Tax Retention", "Net Income / EBT", taxBurden.toFixed(3)],
          ["2. Interest Preservation", "EBT / EBIT", interestBurden.toFixed(3)],
          ["3. Operating Margin", "EBIT / Revenue", `${(ebitMargin * 100).toFixed(2)}%`],
          ["4. Total Asset Turnover", "Revenue / Total Assets", `${assetTurnover.toFixed(2)}x`],
          ["5. Financial Leverage", "Total Assets / Total Equity", `${financialLeverage.toFixed(2)}x`],
          ["Net Profit Margin", "Step 1 × Step 2 × Step 3", `${(netProfitMargin * 100).toFixed(2)}%`],
          ["Return on Assets (ROA)", "Net Profit Margin × Asset Turnover", `${(roa * 100).toFixed(2)}%`],
          ["Return on Equity (ROE)", "ROA × Financial Leverage", `${(roe * 100).toFixed(2)}%`],
        ]}
      />
    </figure>
  );
}

