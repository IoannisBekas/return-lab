const finite = (...values: number[]) => values.every(Number.isFinite);

export function calculateForward(spot: number, annualRate: number, years: number, delivery: number) {
  if (!finite(spot, annualRate, years, delivery) || spot <= 0 || delivery < 0 || annualRate <= -1 || years < 0) return null;
  const growth = (1 + annualRate) ** years;
  const forward = spot * growth;
  const longValue = (forward - delivery) / growth;
  return { forward, longValue, shortValue: -longValue };
}

export function impliedSecondYearRate(oneYearSpot: number, twoYearSpot: number) {
  if (!finite(oneYearSpot, twoYearSpot) || oneYearSpot <= -1 || twoYearSpot <= -1) return null;
  return (1 + twoYearSpot) ** 2 / (1 + oneYearSpot) - 1;
}

export function calculateParity(spot: number, strike: number, annualRate: number, years: number, call: number, put: number) {
  if (!finite(spot, strike, annualRate, years, call, put) || spot <= 0 || strike < 0 || annualRate <= -1 || years < 0 || call < 0 || put < 0) return null;
  const pvStrike = strike / (1 + annualRate) ** years;
  const fairPut = call + pvStrike - spot;
  const callLowerBound = Math.max(0, spot - pvStrike);
  return { pvStrike, fairPut, gap: spot + put - (call + pvStrike), callLowerBound, validCall: call >= callLowerBound - 1e-9 && call <= spot };
}

export function parityPayoffs(terminalStock: number, strike: number) {
  return { protectivePut: terminalStock + Math.max(strike - terminalStock, 0), fiduciaryCall: Math.max(terminalStock - strike, 0) + strike };
}

export function calculateBinomial(spot: number, strike: number, up: number, down: number, periodRate: number, type: "call" | "put") {
  const growth = 1 + periodRate;
  if (!finite(spot, strike, up, down, periodRate) || spot <= 0 || strike < 0 || down <= 0 || !(down < growth && growth < up)) return null;
  const stockUp = spot * up;
  const stockDown = spot * down;
  const payoff = (terminal: number) => type === "call" ? Math.max(terminal - strike, 0) : Math.max(strike - terminal, 0);
  const payoffUp = payoff(stockUp);
  const payoffDown = payoff(stockDown);
  const q = (growth - down) / (up - down);
  const value = (q * payoffUp + (1 - q) * payoffDown) / growth;
  const delta = (payoffUp - payoffDown) / (stockUp - stockDown);
  const cash = (payoffDown - delta * stockDown) / growth;
  return { growth, stockUp, stockDown, payoffUp, payoffDown, q, value, delta, cash };
}

export const gipsAccounts = [
  { id: "A", assets: 8, return: 5, strategy: "Core equity", discretionary: true, eligible: true, reason: "Same strategy, discretionary, fee-paying." },
  { id: "B", assets: 12, return: 10, strategy: "Core equity", discretionary: true, eligible: true, reason: "Same strategy, discretionary, fee-paying." },
  { id: "C", assets: 5, return: 7, strategy: "Core equity", discretionary: false, eligible: false, reason: "Nondiscretionary; it does not meet this composite’s definition." },
  { id: "D", assets: 10, return: 12, strategy: "Government bonds", discretionary: true, eligible: false, reason: "Different strategy; it does not belong in this composite." },
  { id: "E", assets: 4, return: -3, strategy: "Core equity", discretionary: true, eligible: true, reason: "Same strategy, discretionary, fee-paying. A loss is not an exclusion criterion." },
];

export function calculateComposite(accounts: { id: string; assets: number; return: number; eligible: boolean }[], included: string[]) {
  const selected = accounts.filter((account) => included.includes(account.id));
  const assets = selected.reduce((sum, account) => sum + account.assets, 0);
  const gain = selected.reduce((sum, account) => sum + account.assets * account.return / 100, 0);
  const correct = accounts.every((account) => included.includes(account.id) === account.eligible) && included.every((id) => accounts.some((account) => account.id === id));
  return { assets, gain, return: assets > 0 ? gain / assets : null, correct };
}
