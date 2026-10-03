import assert from "node:assert/strict";
import { calculateBinomial, calculateComposite, calculateForward, calculateParity, gipsAccounts, impliedSecondYearRate, parityPayoffs } from "../src/components/learning/activityModels";

const close = (actual: number, expected: number, label: string) => assert.ok(Math.abs(actual - expected) < 1e-8, `${label}: ${actual} differs from ${expected}`);

const forward = calculateForward(110, 0.05, 1, 105)!;
close(forward.forward, 115.5, "Fair forward price");
close(forward.longValue, 10, "Existing forward value");
close(forward.longValue + forward.shortValue, 0, "Long/short values offset");
close(calculateForward(100, 0.05, 1, 105)!.longValue, 0, "New fair contract begins at zero");
assert.equal(calculateForward(100, -1, 1, 100), null, "Reject undefined accumulation factor");
assert.equal(calculateForward(NaN, 0.05, 1, 100), null, "Reject nonfinite inputs");
close(impliedSecondYearRate(0.04, 0.05)!, 0.06009615384615397, "Implied forward interest rate");

const parity = calculateParity(100, 102, 0.02, 1, 8, 10)!;
close(parity.pvStrike, 100, "Strike present value");
close(parity.fairPut, 8, "Fair matching put");
close(parity.gap, 2, "Quoted parity violation");
close(calculateParity(100, 102, 0.02, 1, 8, 8)!.gap, 0, "Matched packages have equal prices");
assert.equal(calculateParity(100, 102, 0.02, 1, 101, 8)!.validCall, false, "Reject call quote above stock price");
assert.equal(calculateParity(150, 100, 0, 1, 8, 8)!.validCall, false, "Reject call quote below intrinsic bound");
for (const terminal of [0, 40, 101, 102, 103, 500]) {
  const payoffs = parityPayoffs(terminal, 102);
  close(payoffs.protectivePut, payoffs.fiduciaryCall, `Parity replication at stock ${terminal}`);
}

const call = calculateBinomial(100, 100, 1.2, 0.9, 0.05, "call")!;
close(call.q, 0.5, "Risk-neutral weight");
close(call.value, 9.523809523809524, "Known binomial call value");
close(call.delta, 2 / 3, "Replicating hedge ratio");
close(call.cash, -57.14285714285714, "Replicating borrowing");
for (const type of ["call", "put"] as const) {
  const model = calculateBinomial(100, 100, 1.2, 0.9, 0.05, type)!;
  close(model.delta * model.stockUp + model.cash * model.growth, model.payoffUp, `${type}: up-state replication`);
  close(model.delta * model.stockDown + model.cash * model.growth, model.payoffDown, `${type}: down-state replication`);
  close(model.delta * 100 + model.cash, model.value, `${type}: replication cost matches option value`);
}
assert.equal(calculateBinomial(100, 100, 1.2, 0.9, 0.5, "call"), null, "Reject risk-neutral weight above one");
assert.equal(calculateBinomial(100, 100, 1.2, 0.9, -0.2, "call"), null, "Reject risk-neutral weight below zero");
assert.equal(calculateBinomial(100, 100, 0.9, 0.9, 0.05, "call"), null, "Reject collapsed two-state model");

const validComposite = calculateComposite(gipsAccounts, ["A", "B", "E"]);
assert.equal(validComposite.correct, true, "Include both winning and losing qualifying accounts");
close(validComposite.assets, 24, "Eligible beginning assets");
close(validComposite.gain, 1.48, "Eligible gain");
close(validComposite.return!, 0.06166666666666667, "Eligible composite return");
const cherryPicked = calculateComposite(gipsAccounts, ["A", "B"]);
assert.equal(cherryPicked.correct, false, "Underperformance cannot remove an eligible account");
close(cherryPicked.return!, 0.08, "Selection-biased reported return");
assert.equal(calculateComposite(gipsAccounts, ["A", "B", "C", "E"]).correct, false, "Exclude nondiscretionary account");
assert.equal(calculateComposite(gipsAccounts, ["A", "B", "D", "E"]).correct, false, "Exclude different-strategy account");
assert.equal(calculateComposite(gipsAccounts, []).return, null, "Empty group has no defined return");

console.log("Learning activity checks passed: forward prices and values, parity, binomial replication and invalid inputs, and composite eligibility.");
