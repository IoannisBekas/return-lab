import { useEffect, useId, useState, type ReactNode } from "react";
import { MathText } from "./MathText";
import { calculateBinomial, calculateComposite, calculateForward, calculateParity, gipsAccounts, impliedSecondYearRate, parityPayoffs } from "./activityModels";
import "./ActivityLab.css";

type PracticeStep = { label: string; latex?: string; result: string };
type NumericExercise = { prompt: string; expected: number; unit: string; tolerance: number };

export function NumericCheck({ prompt, expected, unit, tolerance, disabled = false }: NumericExercise & { disabled?: boolean }) {
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<boolean | null>(null);
  useEffect(() => { setResult(null); }, [expected]);
  const valid = answer.trim() !== "" && Number.isFinite(Number(answer));
  return (
    <div className="activity-numeric">
      <label><span>{prompt} ({unit})</span><input type="number" step="any" value={answer} onChange={(event) => { setAnswer(event.target.value); setResult(null); }} /></label>
      <button type="button" disabled={!valid || disabled} onClick={() => setResult(Math.abs(Number(answer) - expected) <= tolerance)}>Check calculation</button>
      {result !== null ? <p className={result ? "activity-success" : "activity-feedback"} role="status">{result ? `Correct within ${tolerance} ${unit}.` : `Review the units and calculation, then try again. Accepted rounding is within ${tolerance} ${unit}.`}</p> : null}
    </div>
  );
}

export function PracticeSteps({ storageId, steps, hint, interpret, sanityCheck, numeric }: {
  storageId: string; steps: PracticeStep[]; hint: string; interpret: string; sanityCheck: string; numeric?: NumericExercise;
}) {
  const storageKey = `return-lab-practice-v1-${storageId}`;
  const [practice, setPractice] = useState(() => {
    try {
      const stored = JSON.parse(localStorage.getItem(storageKey) || "null") as { revealed?: unknown; attempts?: unknown; interpretation?: unknown } | null;
      return {
        revealed: typeof stored?.revealed === "number" && Number.isInteger(stored.revealed) ? Math.max(0, Math.min(steps.length, stored.revealed)) : 0,
        attempts: Array.isArray(stored?.attempts) ? stored.attempts.map((item: unknown) => typeof item === "string" ? item : "").slice(0, steps.length) : [] as string[],
        interpretation: typeof stored?.interpretation === "string" ? stored.interpretation : "",
      };
    } catch { return { revealed: 0, attempts: [] as string[], interpretation: "" }; }
  });
  const [compared, setCompared] = useState(false);
  useEffect(() => { try { localStorage.setItem(storageKey, JSON.stringify(practice)); } catch { /* Practice remains usable in this session. */ } }, [practice, storageKey]);
  const complete = practice.revealed === steps.length;
  return (
    <div className="activity-worked">
      <div className="activity-worked-intro"><strong>Try it before revealing the reasoning</strong><p>Your notes and revealed steps are saved on this device. Writing an attempt is optional.</p>{numeric ? <NumericCheck {...numeric} /> : null}</div>
      <ol className="gold-calculation-steps">
        {steps.map((step, index) => index <= practice.revealed ? (
          <li key={index}>
            <div><span>{index + 1}</span><strong>{step.label}</strong></div>
            {index < practice.revealed ? <>{step.latex ? <MathText display latex={step.latex} /> : null}<p>{step.result}</p>{practice.attempts[index] ? <p className="activity-saved-attempt"><strong>Your attempt: </strong>{practice.attempts[index]}</p> : null}</> : <section className="activity-step-attempt">
              <label><span>Your approach or calculation for step {index + 1}</span><textarea rows={3} value={practice.attempts[index] || ""} onChange={(event) => setPractice((current) => { const attempts = [...current.attempts]; attempts[index] = event.target.value; return { ...current, attempts }; })} /></label>
              <details><summary>Show a planning hint</summary><p>{hint}</p></details>
              <button type="button" onClick={() => setPractice((current) => ({ ...current, revealed: Math.min(steps.length, current.revealed + 1) }))}>Reveal step {index + 1}</button>
            </section>}
          </li>
        ) : null)}
      </ol>
      {complete ? <div className="activity-interpret"><label><span>Explain what the result means and one reason it could change.</span><textarea rows={3} value={practice.interpretation} onChange={(event) => { setPractice((current) => ({ ...current, interpretation: event.target.value })); setCompared(false); }} /></label><button type="button" onClick={() => setCompared(true)}>Compare interpretation</button>{compared ? <div className="gold-example-close" role="status"><section><strong>Interpret</strong><p>{interpret}</p></section><section><strong>Sanity check</strong><p>{sanityCheck}</p></section></div> : null}</div> : null}
      <div className="activity-worked-footer"><span>{practice.revealed}/{steps.length} steps revealed</span><button type="button" onClick={() => { setPractice({ revealed: 0, attempts: [], interpretation: "" }); setCompared(false); }}>Try the example again</button></div>
    </div>
  );
}

export function ExploreChallenge({ storageId, prompt, choices, correctIndex, changeInstruction, changed, explanation, onStart }: {
  storageId: string; prompt: string; choices: string[]; correctIndex: number; changeInstruction: string; changed: boolean; explanation: string; onStart: () => void;
}) {
  const id = useId();
  const storageKey = `return-lab-challenge-v1-${storageId}`;
  const [prediction, setPrediction] = useState<number | null>(null);
  const [committed, setCommitted] = useState(false);
  const [reasoning, setReasoning] = useState(() => { try { return localStorage.getItem(storageKey) || ""; } catch { return ""; } });
  const [compared, setCompared] = useState(false);
  useEffect(() => { try { localStorage.setItem(storageKey, reasoning); } catch { /* Keep the activity usable without storage. */ } }, [reasoning, storageKey]);
  return (
    <section className="explore-challenge" aria-labelledby={`${id}-title`}>
      <h4 id={`${id}-title`}>Predict → change → explain</h4><p>{prompt}</p>
      <fieldset disabled={committed}><legend>Your prediction</legend>{choices.map((choice, index) => <label key={choice}><input type="radio" name={`${id}-prediction`} checked={prediction === index} onChange={() => setPrediction(index)} />{choice}</label>)}</fieldset>
      {!committed ? <button type="button" disabled={prediction === null} onClick={() => { onStart(); setCommitted(true); setCompared(false); }}>Commit prediction and start</button> : <><p className="activity-instruction"><strong>Change: </strong>{changeInstruction}</p><label><span>Explain the result using the model.</span><textarea rows={3} value={reasoning} onChange={(event) => { setReasoning(event.target.value); setCompared(false); }} /></label><button type="button" disabled={!changed || reasoning.trim().length < 15} onClick={() => setCompared(true)}>Compare reasoning</button>{!changed ? <p className="activity-help">Set the controls to the challenge values first.</p> : null}{compared ? <div className="activity-comparison" role="status"><strong>{prediction === correctIndex ? "Your prediction matched the model." : "Your prediction needs revision."}</strong><p>{explanation}</p><p>Compare this explanation with your own; the text response is for self-assessment.</p></div> : null}<button type="button" className="activity-secondary" onClick={() => { setPrediction(null); setCommitted(false); setCompared(false); onStart(); }}>Restart challenge</button></>}
    </section>
  );
}

function LabNumber({ label, value, setValue, min, max, step = 1 }: { label: string; value: number; setValue: (value: number) => void; min: number; max: number; step?: number }) {
  return <label><span>{label}</span><input type="number" min={min} max={max} step={step} value={value} onChange={(event) => { const next = event.target.valueAsNumber; if (Number.isFinite(next)) setValue(Math.max(min, Math.min(max, next))); }} /></label>;
}

function ModelLab({ id, title, intro, assumptions, children }: { id: string; title: string; intro: string; assumptions: string; children: ReactNode }) {
  return <section className="model-lab finance-visual" id="learning-lab" data-lab-id={id}><header><span className="section-code">APPLY THE MODEL</span><h3>{title}</h3><p>{intro}</p></header><p className="activity-assumptions"><strong>Assumptions: </strong>{assumptions}</p>{children}</section>;
}

const money = (value: number) => value.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const percentage = (value: number) => `${(value * 100).toFixed(4)}%`;

export function ForwardPricingLab() {
  const [spot, setSpot] = useState(100);
  const [rate, setRate] = useState(5);
  const [years, setYears] = useState(1);
  const [delivery, setDelivery] = useState(102);
  const [oneYear, setOneYear] = useState(4);
  const [twoYear, setTwoYear] = useState(5);
  const { forward, longValue } = calculateForward(spot, rate / 100, years, delivery)!;
  const forwardRate = impliedSecondYearRate(oneYear / 100, twoYear / 100)!;
  return <ModelLab id="forward-pricing-lab" title="Forward price and an existing contract’s value" intro="Change the spot, financing rate, and delivery price. A fair delivery price and the current value of an old contract answer different questions." assumptions="No asset income or storage costs, annual effective compounding, common delivery date, and frictionless borrowing, lending, and short selling. Values are per unit of underlying.">
    <div className="activity-input-grid"><LabNumber label="Spot price (currency/unit)" value={spot} setValue={setSpot} min={1} max={1000} /><LabNumber label="Annual financing rate (%)" value={rate} setValue={setRate} min={-10} max={25} step={0.5} /><LabNumber label="Years to delivery" value={years} setValue={setYears} min={0.25} max={5} step={0.25} /><LabNumber label="Existing delivery price K" value={delivery} setValue={setDelivery} min={1} max={2000} /></div>
    <MathText display latex={String.raw`F_0=S_0(1+r)^T,\qquad V_{\mathrm{long}}=\frac{F_0-K}{(1+r)^T}`} />
    <NumericCheck prompt="Calculate the current value of the existing long forward" expected={longValue} unit="currency/unit" tolerance={0.02} />
    <details className="activity-model-result"><summary>Reveal model values and interpretation</summary><dl className="fv-results"><div><dt>Fair delivery price</dt><dd>{money(forward)}</dd></div><div><dt>Old long contract value</dt><dd>{money(longValue)}</dd></div><div><dt>Old short contract value</dt><dd>{money(-longValue)}</dd></div></dl><p>{longValue > 0 ? "The old long contract has a delivery price below the current fair price, so it has positive value." : longValue < 0 ? "The old long contract has a delivery price above the current fair price, so it has negative value." : "The delivery price equals the current fair price; the old contract has zero value."} A new contract struck at the fair price starts at zero value in this model.</p></details>
    <h4>Implied second-year interest rate</h4><div className="activity-input-grid"><LabNumber label="One-year spot rate (%)" value={oneYear} setValue={setOneYear} min={-5} max={25} step={0.5} /><LabNumber label="Two-year spot rate (%)" value={twoYear} setValue={setTwoYear} min={-5} max={25} step={0.5} /></div><MathText display latex={String.raw`(1+s_2)^2=(1+s_1)(1+f_{1,2})`} /><p>Under the same annual compounding convention, the implied second-year rate is <strong>{percentage(forwardRate)}</strong>. It reconciles the accumulation factors; it is not a forecast.</p>
    <ExploreChallenge storageId="forward" prompt="Before testing it, predict what happens to the value of an existing long forward if its delivery price K rises while spot, rate, and maturity stay fixed." choices={["The value rises", "The value falls", "The value stays unchanged"]} correctIndex={1} changeInstruction="Keep spot 100, rate 5%, and maturity 1 year; change K from 102 to 110." changed={spot === 100 && rate === 5 && years === 1 && delivery === 110} explanation="The long pays more at delivery for the same asset. Its value falls from 2.86 to −4.76 currency/unit because the delivery obligation is subtracted and discounted." onStart={() => { setSpot(100); setRate(5); setYears(1); setDelivery(102); }} />
  </ModelLab>;
}

export function PutCallParityLab() {
  const [spot, setSpot] = useState(100);
  const [strike, setStrike] = useState(102);
  const [rate, setRate] = useState(2);
  const [years, setYears] = useState(1);
  const [call, setCall] = useState(8);
  const [put, setPut] = useState(10);
  const { pvStrike, fairPut, gap, validCall } = calculateParity(spot, strike, rate / 100, years, call, put)!;
  return <ModelLab id="put-call-parity-lab" title="Match the packages in put–call parity" intro="Compare a protective put with a fiduciary call. First match their cash flows, then compare their costs." assumptions="European call and put with the same underlying, strike, and expiry; no dividends, transaction costs, or trading restrictions; annual effective risk-free compounding.">
    <div className="activity-input-grid"><LabNumber label="Spot price" value={spot} setValue={setSpot} min={1} max={500} /><LabNumber label="Common strike" value={strike} setValue={setStrike} min={1} max={500} /><LabNumber label="Annual risk-free rate (%)" value={rate} setValue={setRate} min={0} max={25} step={0.5} /><LabNumber label="Years to expiry" value={years} setValue={setYears} min={0.25} max={3} step={0.25} /><LabNumber label="Call price" value={call} setValue={setCall} min={0} max={500} step={0.5} /><LabNumber label="Quoted put price" value={put} setValue={setPut} min={0} max={500} step={0.5} /></div>
    <MathText display latex={String.raw`c+\frac{K}{(1+r)^T}=p+S_0`} />
    {!validCall ? <p className="activity-feedback" role="alert">The call quote violates its no-income European bounds. Set it between {money(Math.max(0, spot - pvStrike))} and {money(spot)} before interpreting a fair put price.</p> : <><NumericCheck prompt="Calculate the put price required by parity" expected={fairPut} unit="currency/unit" tolerance={0.02} /><details className="activity-model-result"><summary>Reveal the package comparison</summary><dl className="fv-results"><div><dt>Fair put</dt><dd>{money(fairPut)}</dd></div><div><dt>Stock + quoted put</dt><dd>{money(spot + put)}</dd></div><div><dt>Call + strike bond</dt><dd>{money(call + pvStrike)}</dd></div></dl><p>{Math.abs(gap) < 0.005 ? "The packages have equal current costs within rounding." : gap > 0 ? `The protective-put package is more expensive by ${money(gap)}. Under these assumptions, sell that package and buy the fiduciary-call package.` : `The fiduciary-call package is more expensive by ${money(-gap)}. Under these assumptions, sell that package and buy the protective-put package.`} Both packages have the same terminal payoff below.</p></details></>}
    <div className="activity-table-scroll" tabIndex={0} role="region" aria-label="Parity terminal cash flows"><table><caption>Payoff per unit at the common expiry</caption><thead><tr><th scope="col">Terminal stock price</th><th scope="col">Stock + put</th><th scope="col">Call + strike payment</th></tr></thead><tbody>{[Math.max(0, strike - 20), strike, strike + 20].map((terminal) => { const payoffs = parityPayoffs(terminal, strike); return <tr key={terminal}><th scope="row">{money(terminal)}</th><td>{money(payoffs.protectivePut)}</td><td>{money(payoffs.fiduciaryCall)}</td></tr>; })}</tbody></table></div>
  </ModelLab>;
}

export function BinomialLab() {
  const [spot, setSpot] = useState(100);
  const [strike, setStrike] = useState(100);
  const [up, setUp] = useState(1.2);
  const [down, setDown] = useState(0.9);
  const [rate, setRate] = useState(5);
  const [type, setType] = useState<"call" | "put">("call");
  const growth = 1 + rate / 100;
  const model = calculateBinomial(spot, strike, up, down, rate / 100, type);
  return <ModelLab id="binomial-lab" title="Price and replicate a one-period option" intro="Calculate both state payoffs, check whether the model admits risk-neutral weights, and audit the stock-and-cash replication." assumptions="One period, two stock states, no income, European exercise, frictionless financing and stock trading. The risk-free input is the return over this period, not an annual rate.">
    <div className="activity-input-grid"><LabNumber label="Initial stock price" value={spot} setValue={setSpot} min={1} max={500} /><LabNumber label="Strike" value={strike} setValue={setStrike} min={1} max={500} /><LabNumber label="Up multiplier u" value={up} setValue={setUp} min={1.01} max={2} step={0.01} /><LabNumber label="Down multiplier d" value={down} setValue={setDown} min={0.1} max={0.99} step={0.01} /><LabNumber label="Period risk-free return (%)" value={rate} setValue={setRate} min={-5} max={30} step={0.5} /><label><span>Option type</span><select value={type} onChange={(event) => setType(event.target.value as "call" | "put")}><option value="call">Call</option><option value="put">Put</option></select></label></div>
    <MathText display latex={String.raw`q=\frac{1+r-d}{u-d},\qquad V_0=\frac{qV_u+(1-q)V_d}{1+r}`} />
    {!model ? <p className="activity-feedback" role="alert">These inputs fail d &lt; 1 + r &lt; u: {down.toFixed(2)} &lt; {growth.toFixed(3)} &lt; {up.toFixed(2)} is false. Adjust the state multipliers or risk-free return. Do not cap an invalid pricing weight.</p> : <><NumericCheck prompt={`Calculate the ${type} value today`} expected={model.value} unit="currency/unit" tolerance={0.02} /><details className="activity-model-result"><summary>Reveal the pricing and replication</summary><dl className="fv-results"><div><dt>Risk-neutral up weight</dt><dd>{model.q.toFixed(4)}</dd></div><div><dt>Option value</dt><dd>{money(model.value)}</dd></div><div><dt>Stock units Δ</dt><dd>{model.delta.toFixed(4)}</dd></div></dl><p>Hold {model.delta.toFixed(4)} stock units and {model.cash >= 0 ? `lend ${money(model.cash)}` : `borrow ${money(-model.cash)}`} today. Initial cost is {money(model.delta * spot + model.cash)}. These weights price matched cash flows; q is not a real-world probability forecast.</p><div className="activity-table-scroll" tabIndex={0} role="region" aria-label="Binomial state replication"><table><caption>Both terminal states must match</caption><thead><tr><th scope="col">State</th><th scope="col">Stock price</th><th scope="col">Option payoff</th><th scope="col">Stock + cash payoff</th></tr></thead><tbody><tr><th scope="row">Up</th><td>{money(model.stockUp)}</td><td>{money(model.payoffUp)}</td><td>{money(model.delta * model.stockUp + model.cash * growth)}</td></tr><tr><th scope="row">Down</th><td>{money(model.stockDown)}</td><td>{money(model.payoffDown)}</td><td>{money(model.delta * model.stockDown + model.cash * growth)}</td></tr></tbody></table></div></details></>}
  </ModelLab>;
}

export function GipsLab() {
  const [included, setIncluded] = useState<string[]>([]);
  const [checked, setChecked] = useState(false);
  const { assets, gain, correct, return: compositeReturn } = calculateComposite(gipsAccounts, included);
  return <ModelLab id="gips-composite-lab" title="Define the composite before seeing the return" intro="Select the segregated accounts that belong to the Core Equity composite. Apply the same eligibility rules to winning and losing accounts." assumptions="This simplified, single-period composite contains same-strategy, discretionary, fee-paying segregated accounts. All accounts are fee-paying, have positive beginning assets, and have no external cash flows. Beginning-value weighting illustrates aggregation; this exercise does not establish GIPS compliance.">
    <fieldset className="activity-composite"><legend>Select every eligible account</legend>{gipsAccounts.map((account) => <label key={account.id}><input type="checkbox" checked={included.includes(account.id)} onChange={() => { setIncluded((current) => current.includes(account.id) ? current.filter((id) => id !== account.id) : [...current, account.id]); setChecked(false); }} /><span><strong>Account {account.id} · {account.strategy}</strong><small>{account.discretionary ? "Discretionary" : "Nondiscretionary"} · {account.assets} million beginning assets · {account.return}% return</small></span></label>)}</fieldset>
    <button type="button" onClick={() => setChecked(true)}>Check composite membership</button>
    {checked ? <div className="activity-comparison" role="status"><strong>{correct ? "Correct: A, B, and E meet the stated definition." : "Review the membership rules, then revise your selection."}</strong><ul>{gipsAccounts.map((account) => <li key={account.id}><strong>{account.id}: </strong>{account.reason}</li>)}</ul></div> : null}
    <MathText display latex={String.raw`R_C=\frac{\sum_i V_{i,0}R_i}{\sum_i V_{i,0}}`} />
    <dl className="fv-results"><div><dt>Your selected beginning assets</dt><dd>{assets} million</dd></div><div><dt>Your selected gain</dt><dd>{money(gain)} million</dd></div><div><dt>Your selected group’s return</dt><dd>{compositeReturn !== null ? percentage(compositeReturn) : "Select accounts"}</dd></div></dl><p className="fv-note">Including A and B while omitting E produces 8.00%; including all three eligible accounts produces 6.1667%. Choosing membership based on performance changes the record rather than measuring the defined strategy.</p>
    <p className="activity-help">Membership rules: <a href="https://www.gipsstandards.org/standards/gips-standards-for-firms/gips-standards-handbook-for-firms/" target="_blank" rel="noreferrer">GIPS Standards Handbook for Firms</a>. Non-fee-paying discretionary accounts may also be included under the relevant requirements; this exercise’s accounts are all fee-paying.</p>
  </ModelLab>;
}
