from __future__ import annotations

import json
import re
from pathlib import Path


COURSE = Path("src/data/curriculum.json")


TOPIC_PROFILES = {
    "Quantitative Methods": {
        "context": "Quantitative analysis converts financial observations into comparable measures. The analyst must keep units and timing consistent, show the assumptions behind the calculation, and interpret the result rather than treating a computed number as self-explanatory.",
        "terms": [("Input", "An observed value or stated assumption used in the calculation."), ("Estimate", "A sample-based or model-based approximation of an unknown quantity."), ("Sensitivity", "How much the conclusion changes when an input or assumption changes.")],
        "scenario": "An analyst has a short return history and must choose a defensible measure before comparing two investments.",
        "mistakes": ["Mixing percentages, decimals, periods, or compounding conventions.", "Selecting a technique because it is familiar rather than because its assumptions fit the question.", "Reporting a precise output without discussing sampling error, model risk, or economic meaning."],
    },
    "Economics": {
        "context": "Economic analysis follows incentives through quantities, prices, income, expectations, and policy responses. A useful conclusion distinguishes an initial effect from later feedback and identifies which assumptions would make the outcome different.",
        "terms": [("Incentive", "A change in cost or benefit that can alter a decision."), ("Transmission", "The path through which a shock affects economic activity and asset prices."), ("Equilibrium", "A state in which planned demand and supply are mutually consistent.")],
        "scenario": "Growth is slowing while inflation remains above target, and an investor must trace the effects on companies, rates, and currencies.",
        "mistakes": ["Stopping at the first-round effect and ignoring behavioral or policy responses.", "Treating a directional relationship as a precise forecast.", "Using one indicator without checking whether other evidence confirms the same economic story."],
    },
    "Corporate Issuers": {
        "context": "Corporate decisions should be evaluated through incremental cash flow, risk, flexibility, governance, and stakeholder incentives. Accounting profit may help describe a decision, but value depends on cash flow timing and the return required for risk.",
        "terms": [("Incremental cash flow", "The cash flow that occurs because a decision is taken."), ("Agency conflict", "A situation in which a decision maker's incentives differ from those of a stakeholder."), ("Financial flexibility", "The ability to fund operations and opportunities under changing conditions.")],
        "scenario": "A company is deciding whether to fund a new project with internal cash, debt, or new equity while preserving operating liquidity.",
        "mistakes": ["Including sunk costs or excluding opportunity costs from a decision.", "Optimizing a single ratio while ignoring flexibility and downside risk.", "Assuming governance policies work without examining incentives, information, and enforcement."],
    },
    "Financial Statement Analysis": {
        "context": "Statement analysis follows an economic event through recognition, measurement, presentation, disclosure, and cash flow. Comparability often requires adjustments because firms can represent similar economics with different estimates or classifications.",
        "terms": [("Recognition", "The decision to record an item in the primary financial statements."), ("Measurement", "The amount and basis used to report a recognized item."), ("Earnings quality", "The degree to which reported earnings reflect sustainable performance and convert into cash.")],
        "scenario": "Two firms report similar earnings, but their cash conversion, estimates, and balance-sheet classifications differ materially.",
        "mistakes": ["Reading the primary statements without the related notes and accounting policies.", "Comparing ratios whose numerators, denominators, or accounting bases are inconsistent.", "Treating a noncash adjustment as irrelevant even when it changes future economics or risk."],
    },
    "Equity Investments": {
        "context": "Equity analysis connects industry structure and company economics with forecasts, required return, and value. A valuation is a conditional result: it is useful when the operating assumptions are explicit and internally consistent.",
        "terms": [("Value driver", "An operating or financial variable that materially affects estimated value."), ("Required return", "The return investors demand for time and risk."), ("Competitive advantage", "A condition that allows a company to sustain returns above competitive levels.")],
        "scenario": "An analyst must decide whether a company's market price is consistent with its expected growth, margins, reinvestment, and risk.",
        "mistakes": ["Extending recent growth without checking market size, competition, and reinvestment needs.", "Using peer multiples without normalizing fundamentals and accounting differences.", "Presenting one valuation result without sensitivity or a clear investment thesis."],
    },
    "Fixed Income": {
        "context": "Fixed-income analysis begins with promised and contingent cash flows, then applies rates appropriate for timing and risk. Price sensitivity also depends on how the curve moves and whether the issuer or borrower can change the cash-flow schedule.",
        "terms": [("Yield", "A rate that summarizes price and promised cash flows under stated assumptions."), ("Spread", "Additional yield relative to a selected benchmark."), ("Duration", "A measure of price sensitivity to a specified change in yield or the curve.")],
        "scenario": "A portfolio manager compares two bonds with different maturities, credit quality, liquidity, and embedded options after market yields change.",
        "mistakes": ["Discounting every cash flow with a rate that does not match its maturity or risk.", "Comparing yields that use different conventions or embedded-option assumptions.", "Using duration alone for large, nonparallel, or option-sensitive rate changes."],
    },
    "Derivatives": {
        "context": "Derivative analysis starts with the payoff and settlement terms, then uses replication or no-arbitrage to establish value. Because notional exposure can exceed invested cash, risk must be assessed from the full payoff rather than the initial payment.",
        "terms": [("Underlying", "The asset, rate, index, or event that determines a derivative's payoff."), ("Replication", "A portfolio constructed to match another position's future payoff."), ("No arbitrage", "The condition that equal future payoffs must have equal current values.")],
        "scenario": "A firm wants to change a market exposure with a derivative and must compare the hedge payoff with basis, liquidity, collateral, and counterparty risk.",
        "mistakes": ["Confusing the contract's price with its value after market conditions change.", "Ignoring payoff asymmetry, settlement timing, or the sign of a position.", "Measuring risk from cash paid instead of notional exposure and stressed payoff."],
    },
    "Alternative Investments": {
        "context": "Alternative-investment analysis combines asset economics with legal structure, fees, leverage, valuation method, and liquidity. Reported returns require special care when cash flows are irregular or asset values are appraised rather than continuously traded.",
        "terms": [("Illiquidity", "The cost or difficulty of exiting an investment quickly at a representative value."), ("Carried interest", "Performance compensation allocated to a manager under specified terms."), ("Appraisal smoothing", "Understatement of short-term volatility when valuations adjust slowly.")],
        "scenario": "An investor compares a public security with an alternative fund whose capital calls, fees, leverage, appraisals, and exit timing are uncertain.",
        "mistakes": ["Comparing reported returns without aligning fees, leverage, timing, and valuation methods.", "Treating illiquidity as only a volatility issue rather than a funding and control constraint.", "Assuming historical exits and valuations will remain available in stressed markets."],
    },
    "Portfolio Management": {
        "context": "Portfolio management translates an investor's objectives and constraints into exposures, implementation, monitoring, and rebalancing. Risk is a portfolio property because diversification depends on covariance as well as each holding's standalone volatility.",
        "terms": [("Risk tolerance", "The willingness and ability to accept uncertain outcomes."), ("Diversification", "Combining exposures so imperfect co-movement reduces portfolio risk."), ("Rebalancing", "Trading to restore intended exposures after market or client changes.")],
        "scenario": "An adviser must construct and maintain a portfolio for a client with a return goal, limited loss capacity, cash needs, taxes, and behavioral concerns.",
        "mistakes": ["Setting an allocation before defining the investor's objective and constraints.", "Assuming more holdings automatically create meaningful diversification.", "Changing strategy after short-term losses without testing whether objectives or assumptions changed."],
    },
    "Ethical and Professional Standards": {
        "context": "Ethical analysis identifies duties, stakeholders, conflicts, available actions, and the effect on trust. Intent alone is insufficient: professionals need reasonable diligence, clear communication, appropriate controls, and records that support the action taken.",
        "terms": [("Duty", "An obligation owed to a client, employer, market, profession, or other stakeholder."), ("Conflict of interest", "A circumstance in which competing interests may impair independent judgment."), ("Disclosure", "Clear communication of information a reasonable person needs to evaluate a decision or conflict.")],
        "scenario": "A professional faces pressure to act before all relevant facts are verified and must protect clients, market integrity, and independent judgment.",
        "mistakes": ["Choosing an action based only on personal intent rather than duties and foreseeable effects.", "Assuming disclosure cures conduct that remains misleading, unfair, or insufficiently diligent.", "Failing to document the facts, escalation, recommendation, and final action."],
    },
}


FORMULA_RULES = [
    (("interest rates and return",), "Required return", "r = real risk-free rate + inflation premium + risk premiums", "Each premium compensates the investor for a distinct source of risk.", "A 2% real rate, 3% expected inflation, and 1.5% combined risk premiums imply an approximate required return of 6.5%."),
    (("time-weighted",), "Time-weighted return", "TWR = Π(1 + subperiod return) − 1", "Break the history at external cash flows so their timing does not determine manager performance.", "Subperiod returns of 10% and −5% produce (1.10 × 0.95) − 1 = 4.5%."),
    (("common measures of return",), "Holding-period return", "HPR = (ending value + income − beginning value) / beginning value", "Include distributions received during the measurement period.", "A position bought for 100, sold for 106, and paying 2 has an 8% holding-period return."),
    (("discounted cash flow",), "Present value", "PV = Σ CFₜ / (1 + r)ᵗ", "Discount each dated cash flow at a rate consistent with its timing and risk.", "At 5%, 105 received in one year has a present value of 100."),
    (("central tendency",), "Sample mean", "x̄ = Σxᵢ / n", "Pair a location measure with dispersion and distribution shape.", "Returns of 2%, 4%, and 9% have an arithmetic mean of 5%."),
    (("skewness", "kurtosis", "correlation"), "Correlation", "ρₓᵧ = Cov(X,Y) / (σₓσᵧ)", "Correlation measures linear co-movement and stays between −1 and +1.", "A positive covariance with positive standard deviations produces positive correlation, but does not prove causation."),
    (("probability", "bayes"), "Bayes' rule", "P(A|B) = P(B|A)P(A) / P(B)", "Update the prior probability using how likely the evidence is under each state.", "If evidence is much more likely when A is true, the posterior probability of A rises above its prior."),
    (("portfolio return and risk", "portfolio standard"), "Two-asset portfolio variance", "σ²ₚ = w₁²σ₁² + w₂²σ₂² + 2w₁w₂σ₁σ₂ρ₁₂", "The covariance term explains why portfolio risk is not a weighted average of asset volatilities.", "When correlation is below +1, combining the assets can reduce risk relative to holding either exposure alone."),
    (("sampling",), "Standard error of the mean", "SE(x̄) = s / √n", "A larger representative sample generally reduces uncertainty around the estimated mean.", "If sample standard deviation is 12% and n is 36, the estimated standard error is 2%."),
    (("hypothesis", "independence"), "Decision rule", "Reject H₀ when p-value < significance level", "Choose the significance level and tail before looking at the test result.", "At a 5% significance level, a p-value of 3% leads to rejection of the null hypothesis."),
    (("regression", "anova", "goodness of fit"), "Simple regression", "ŷ = b₀ + b₁x", "The slope estimates the expected change in y for a one-unit change in x under the model.", "With b₀ = 1 and b₁ = 0.8, x = 5 produces a predicted value of 5."),
    (("breakeven",), "Breakeven quantity", "Q = fixed costs / (price − variable cost per unit)", "The denominator is contribution margin per unit.", "Fixed costs of 100,000 and contribution margin of 20 require 5,000 units to break even."),
    (("foreign exchange",), "Cross rate", "A/C = (A/B) × (B/C)", "Align currencies so the intermediate unit cancels.", "If A/B is 2 and B/C is 3, then A/C is 6 under consistent quote direction."),
    (("capital investments", "capital allocation"), "Net present value", "NPV = Σ CFₜ / (1 + r)ᵗ − initial investment", "A positive NPV indicates expected value creation under the stated cash flows and required return.", "An investment of 95 that pays 105 in one year has NPV 5 when the required return is 5%."),
    (("cost of capital",), "Weighted-average cost of capital", "WACC = wₑrₑ + w-dr-d(1 − tax rate)", "Use market-value weights and component costs consistent with the project's operating risk.", "With equal debt and equity weights, 10% equity cost, 6% debt cost, and 25% tax, WACC is 7.25%."),
    (("earnings per share",), "Basic EPS", "EPS = (net income − preferred dividends) / weighted-average common shares", "Use the shares outstanding during the period rather than only the closing balance.", "Income available to common of 12 million over 6 million weighted shares gives EPS of 2."),
    (("cash flow", "cfo"), "Indirect operating cash flow", "CFO = net income + noncash charges − increases in operating working capital", "Adjust for noncash recognition and the cash tied up in operating balances.", "Net income of 100, depreciation of 20, and a 15 increase in receivables produce CFO of 105, all else equal."),
    (("inventory", "fifo", "lifo"), "Inventory roll-forward", "ending inventory = beginning inventory + purchases − cost of sales", "Cost-flow assumptions determine which costs remain in inventory and which enter profit.", "Beginning inventory of 40 plus purchases of 90 and cost of sales of 100 leaves ending inventory of 30."),
    (("financial ratios", "dupont"), "Three-part DuPont", "ROE = net margin × asset turnover × financial leverage", "The decomposition separates profitability, efficiency, and financing effects.", "A 10% margin, 1.2 turnover, and 1.5 leverage produce ROE of 18%."),
    (("dividend discount",), "Constant-growth dividend model", "V₀ = D₁ / (r − g)", "Required return must exceed the sustainable perpetual growth rate.", "A next dividend of 3, required return of 9%, and growth of 3% imply value of 50."),
    (("relative valuation",), "Justified price multiple", "value = normalized fundamental × justified multiple", "The comparison is valid only when growth, risk, accounting, and capital structure are sufficiently aligned.", "Normalized EPS of 4 and a justified P/E of 15 imply equity value of 60 per share."),
    (("bond valuation", "prices and yields"), "Bond price", "P = Σ couponₜ/(1+y)ᵗ + principal/(1+y)ⁿ", "Use the yield periodicity that matches coupon frequency.", "A one-year zero-coupon payment of 105 discounted at 5% is worth 100."),
    (("duration",), "Duration price approximation", "ΔP/P ≈ −modified duration × Δy", "The negative sign captures the inverse price-yield relationship.", "Modified duration of 5 and a 0.50% yield rise imply an approximate 2.5% price decline."),
    (("convexity",), "Duration-convexity approximation", "ΔP/P ≈ −ModDur·Δy + 0.5·Convexity·(Δy)²", "Convexity improves the estimate when the yield change is larger.", "For a positive-convexity bond, the convexity term offsets part of a duration-estimated loss when yields rise."),
    (("forward contract", "carrying costs", "arbitrage"), "Forward price without income", "F₀(T) = S₀(1 + r)ᵀ", "The forward price reflects the cost of carrying the underlying to maturity.", "Spot of 100 financed for one year at 5% implies a no-arbitrage forward price of 105."),
    (("put-call parity",), "European put-call parity", "c + PV(X) = p + S₀", "The two sides have identical expiration payoffs when exercise terms match.", "If one side is cheaper, buying it and selling the expensive side creates an arbitrage before costs."),
    (("binomial",), "Risk-neutral probability", "π = (1 + r − d) / (u − d)", "Discount the probability-weighted derivative payoff after defining consistent up and down factors.", "Once π is found, value equals the discounted expected option payoff across the two states."),
    (("performance appraisal",), "Money-weighted return", "0 = Σ CFₜ / (1 + IRR)ᵗ", "The internal rate of return incorporates the timing and amount of investor-controlled cash flows.", "Earlier large contributions give more weight to the returns earned after those contributions."),
    (("capm", "sml"), "Capital asset pricing model", "E(Rᵢ) = Rf + βᵢ[E(Rm) − Rf]", "Only systematic risk earns a risk premium in the model.", "With a 3% risk-free rate, beta 1.2, and 5% market premium, required return is 9%."),
]


def formula_for(title: str, steps: list[str]) -> dict:
    lowered = title.lower()
    for keywords, label, expression, interpretation, example in FORMULA_RULES:
        if any(keyword in lowered for keyword in keywords):
            return {"label": label, "expression": expression, "interpretation": interpretation, "example": example}
    return {
        "label": "Analytical decision rule",
        "expression": "evidence + assumptions → analysis → decision + limitation",
        "interpretation": "A defensible conclusion makes the evidence and assumptions visible, follows a repeatable process, and states what could change the decision.",
        "example": f"For {title.lower()}, an analyst applies the stated process, compares the result with an alternative, and records the most important limitation.",
    }


def rotate_choices(correct: str, distractors: list[str], seed: int) -> tuple[list[str], int]:
    choices = [correct, *distractors]
    shift = seed % len(choices)
    choices = choices[shift:] + choices[:shift]
    return choices, choices.index(correct)


def enrich_module(module: dict, reading: dict, module_index: int) -> dict:
    profile = TOPIC_PROFILES[reading["topic"]]
    title = module["title"]
    steps = module["steps"]
    formula = formula_for(title, steps)
    terms = [
        {"term": title, "definition": module["explanation"]},
        *({"term": term, "definition": definition} for term, definition in profile["terms"]),
    ]
    objectives = [
        f"Explain {title.lower()} in plain language and connect it to the reading's central problem.",
        f"Apply the {formula['label'].lower()} or analytical decision rule with clearly labeled inputs.",
        "Interpret the result, challenge its assumptions, and identify one condition that would change the conclusion.",
    ]
    lesson = [
        module["explanation"],
        profile["context"],
        f"For {title.lower()}, begin by asking what decision is being made and what evidence is available. Then follow the three-step method below. The final answer should state both the conclusion and the most important reason it may fail.",
    ]
    scenario = profile["scenario"]
    analysis = " ".join(f"Step {index + 1}: {step}" for index, step in enumerate(steps))
    result = f"A complete response uses {formula['label'].lower()}, gives a direction or value supported by the inputs, and explains how the decision changes when the key assumption changes. {formula['example']}"

    questions = []
    q1_correct = module["explanation"]
    q1_choices, q1_index = rotate_choices(
        q1_correct,
        [
            "The topic is used only to memorize terminology; inputs and decisions do not affect the result.",
            "The strongest conclusion is always the result with the largest numerical value, regardless of risk or assumptions.",
            "Historical observations determine future outcomes exactly when the calculation is performed correctly.",
        ],
        reading["number"] + module_index,
    )
    questions.append({"question": f"Which statement best explains the purpose of {title}?", "choices": q1_choices, "correct": q1_index, "explanation": f"The correct statement identifies the analytical relationship and its purpose. {module['explanation']}"})

    q2_correct = " → ".join(steps)
    q2_choices, q2_index = rotate_choices(
        q2_correct,
        [
            "Choose the preferred conclusion → search only for confirming evidence → omit uncertainty",
            "Calculate first → define the question afterward → assume the output is decision-ready",
            "Copy a benchmark result → ignore differences in inputs → report false precision",
        ],
        reading["number"] + module_index + 1,
    )
    questions.append({"question": "Which workflow produces the most defensible analysis?", "choices": q2_choices, "correct": q2_index, "explanation": "A sound workflow defines the concept and inputs before calculation or judgment, then interprets the result with its limitation."})

    q3_correct = formula["interpretation"]
    q3_choices, q3_index = rotate_choices(
        q3_correct,
        [
            "Once a result is calculated, changing the assumptions cannot affect the conclusion.",
            "The decision rule is valid only when it produces the outcome the analyst expected in advance.",
            "A precise estimate removes the need to examine data quality, incentives, or model risk.",
        ],
        reading["number"] + module_index + 2,
    )
    questions.append({"question": f"How should an analyst interpret the {formula['label'].lower()}?", "choices": q3_choices, "correct": q3_index, "explanation": f"The interpretation connects the method with its economic meaning. {formula['interpretation']}"})

    return {
        **module,
        "objectives": objectives,
        "lesson": lesson,
        "keyTerms": terms,
        "formula": formula,
        "workedExample": {"scenario": scenario, "analysis": analysis, "result": result},
        "mistakes": profile["mistakes"],
        "questions": questions,
        "summary": [module["explanation"], f"Use this sequence: {'; '.join(steps)}", f"Decision check: {module['check']}"],
    }


def main() -> None:
    readings = json.loads(COURSE.read_text(encoding="utf-8"))
    for reading in readings:
        reading["modules"] = [
            enrich_module(module, reading, index)
            for index, module in enumerate(reading["modules"])
        ]
        reading["chapterQuestionCount"] = sum(len(module["questions"]) for module in reading["modules"])
    COURSE.write_text(json.dumps(readings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    questions = sum(reading["chapterQuestionCount"] for reading in readings)
    print(f"Enriched {len(readings)} chapters with {questions} original practice questions.")


if __name__ == "__main__":
    main()

