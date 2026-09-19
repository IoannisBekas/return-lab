/** Original teaching and examples, checked against the supplied 2026 source books.
 * pdfPage is the one-based physical PDF page, including front matter.
 * These are enrichment records, not a claim of full exam-objective assessment coverage.
 */
export interface GoldSourceRef {
  book: number;
  pdfPage: number;
  heading: string;
}

export interface GoldFormula {
  id: string;
  title: string;
  latex: string;
  variables: { symbol: string; meaning: string; unit: string }[];
  assumptions: string[];
  domain: string;
  interpretation: string;
}

export interface GoldWorkedExample {
  id: string;
  title: string;
  given: string[];
  find: string;
  plan: string;
  calculate: { description: string; latex: string; result: string }[];
  interpret: string;
  sanityCheck: string;
}

export interface GoldAssessment {
  id: string;
  objectiveId: string;
  prompt: string;
  options: { id: string; text: string; feedback: string }[];
  correctOptionId: string;
  solution: string;
}

export interface GoldLesson {
  readingId: number;
  title: string;
  sourceRefs: GoldSourceRef[];
  objectives: { id: string; description: string }[];
  sections: { heading: string; body: string[] }[];
  formulas: GoldFormula[];
  workedExamples: GoldWorkedExample[];
  misconceptions: { claim: string; correction: string }[];
  assessments: GoldAssessment[];
}

export const goldQuantLessons: GoldLesson[] = [
  {
    readingId: 1,
    title: "Returns: choose the question before the calculation",
    sourceRefs: [
      { book: 1, pdfPage: 14, heading: "LOS 1.a — Interest rates and return measurement" },
      { book: 1, pdfPage: 15, heading: "LOS 1.b — Return measurement over time" },
      { book: 1, pdfPage: 19, heading: "LOS 1.c — Money-weighted and time-weighted returns" },
      { book: 1, pdfPage: 22, heading: "LOS 1.d — Annualized and continuously compounded returns" },
      { book: 1, pdfPage: 24, heading: "LOS 1.e — Major return measures" },
    ],
    objectives: [
      { id: "1.a", description: "Distinguish a required return, discount rate, and opportunity cost; explain the sources of an interest-rate premium." },
      { id: "1.b", description: "Choose and calculate a holding-period return or a suitable arithmetic, geometric, or harmonic average." },
      { id: "1.c", description: "Use valuations and investor cash flows to distinguish time-weighted performance from money-weighted experience." },
      { id: "1.d", description: "Convert a holding-period return to an annualized or continuously compounded measure with an explicit time convention." },
      { id: "1.e", description: "Distinguish gross, net, pretax, after-tax, nominal, real, and leveraged returns." },
    ],
    sections: [
      {
        heading: "What must this investment compensate you for?",
        body: [
          "The same interest rate can answer three questions. A required return is the minimum compensation an investor demands. A discount rate translates future money into a present value. An opportunity cost describes the return forgone by choosing another use of capital. The label depends on the decision; the arithmetic can be identical.",
          "An introductory rate decomposition starts with a real risk-free rate, adds expected inflation, and adds premiums for default, illiquidity, and maturity risk. This is an additive approximation, not the exact multiplicative equation for real versus nominal returns. Keep compensation for an identified risk separate from a forecast of what an investment will actually earn.",
        ],
      },
      {
        heading: "Averages answer different questions",
        body: [
          "A holding-period return includes both price change and distributions. Once returns from equal-length periods are known, the arithmetic mean describes the average observation; the geometric mean describes the constant compounded rate that reproduces the ending wealth. A gain followed by an equally large percentage loss does not restore the starting balance because the two percentages apply to different amounts.",
          "Use a harmonic mean of prices when equal currency amounts are invested at different positive prices: cheaper purchases acquire more units. It is not a substitute for compounding a return history. Outliers can motivate a trimmed or winsorized mean, but record the treatment: deleting extremes and replacing extremes are different procedures and can conceal important investment losses.",
        ],
      },
      {
        heading: "Separate the portfolio path from the investor's cash-flow timing",
        body: [
          "For a true time-weighted return, break the history at every external deposit or withdrawal. Value the portfolio immediately before the flow, then use the post-flow value as the next interval's starting capital. Link the interval growth factors. A table of cash flows without these valuations cannot determine the exact time-weighted return.",
          "For a money-weighted return, record contributions as negative investor cash flows and distributions or the final realizable value as positive flows. Solve for the rate that makes their discounted sum zero. With regular spacing this is periodic IRR; dated cash flows require a date-based convention. Nonconventional flows may have multiple roots or no admissible root, so a numerical result needs a domain and convergence check.",
          "TWR is useful for comparing managers when clients control contributions. MWR describes the experience of the capital actually invested and is also relevant when a manager controls capital-call timing. Compare measures on the same horizon: a two-year cumulative TWR and an annual IRR are not directly comparable.",
        ],
      },
      {
        heading: "Put time, fees, inflation, and borrowing on the label",
        body: [
          "Annualization compounds the observed growth factor to a one-year equivalent; it does not predict that the return will repeat. State the day-count convention if the input period is measured in days. Log returns add across consecutive periods, while ordinary returns compound. A log return is not defined when wealth has fallen to zero.",
          "In the source's portfolio-performance convention, gross return already deducts transaction costs but precedes management and administration fees; net return also deducts those fees. After-tax returns depend on the applicable income and gain taxes. Real returns measure purchasing-power growth by dividing nominal wealth growth by the inflation factor.",
          "Borrowing changes the denominator to the investor's own capital. Deduct borrowing interest before dividing the investment gain by that equity. The same leverage that magnifies a favorable outcome can magnify a loss; the asset return and equity return must therefore be labeled separately.",
        ],
      },
    ],
    formulas: [
      {
        id: "hpr",
        title: "Holding-period return",
        latex: String.raw`R=\frac{V_1-V_0+D}{V_0}`,
        variables: [
          { symbol: "V_0", meaning: "Beginning investment value", unit: "currency" },
          { symbol: "V_1", meaning: "Ending value excluding distributions counted in D", unit: "same currency" },
          { symbol: "D", meaning: "Income distributed during the period", unit: "same currency" },
          { symbol: "R", meaning: "Return over this holding period", unit: "decimal return" },
        ],
        assumptions: ["No external contributions or withdrawals within the interval.", "Distributions are counted once; the simple formula does not add interim reinvestment income."],
        domain: "V0 > 0; all amounts refer to the same investment and period.",
        interpretation: "An increase from 80 to 84 plus a distribution of 2 gives a 7.5% holding-period return.",
      },
      {
        id: "return-averages",
        title: "Arithmetic versus geometric mean",
        latex: String.raw`\bar R_A=\frac{1}{n}\sum_{t=1}^{n}R_t,\qquad \bar R_G=\left[\prod_{t=1}^{n}(1+R_t)\right]^{1/n}-1`,
        variables: [
          { symbol: "R_t", meaning: "Return in interval t", unit: "decimal return" },
          { symbol: "n", meaning: "Number of equal-length intervals", unit: "periods" },
          { symbol: "\\bar R_A, \\bar R_G", meaning: "Arithmetic and compounded mean return", unit: "decimal per interval" },
        ],
        assumptions: ["Intervals have equal lengths.", "The geometric wealth interpretation follows consecutive reinvested returns with no external flows."],
        domain: "n >= 1; Rt >= -1 for a conventional nonnegative-wealth path. A -100% return yields a -100% geometric mean; returns below -100% need a different leverage/wealth model.",
        interpretation: "The arithmetic mean averages observations; the geometric mean reproduces compound wealth. They coincide for a constant return series.",
      },
      {
        id: "harmonic-price",
        title: "Average unit cost for equal cash purchases",
        latex: String.raw`P_H=\frac{n}{\sum_{i=1}^{n}1/P_i}`,
        variables: [
          { symbol: "P_i", meaning: "Purchase price on occasion i", unit: "currency per unit" },
          { symbol: "n", meaning: "Number of equal-cash purchases", unit: "purchases" },
          { symbol: "P_H", meaning: "Total cash invested divided by total units bought", unit: "currency per unit" },
        ],
        assumptions: ["Each purchase invests the same currency amount.", "Fractional units are available and transaction costs are ignored."],
        domain: "Every Pi > 0; n >= 1.",
        interpretation: "Equal cash purchases at 20 and 30 have an average unit cost of 24, because more units are bought at 20.",
      },
      {
        id: "twr-irr",
        title: "Linked return and periodic money-weighted return",
        latex: String.raw`R_{TW}=\prod_{j=1}^{k}(1+r_j)-1,\qquad 0=\sum_{t=0}^{T}\frac{CF_t}{(1+i)^t}`,
        variables: [
          { symbol: "r_j", meaning: "Portfolio return between external cash-flow events", unit: "decimal per subperiod" },
          { symbol: "CF_t", meaning: "Investor contribution (negative) or receipt (positive)", unit: "currency" },
          { symbol: "i", meaning: "Periodic internal rate of return", unit: "decimal per equally spaced period" },
          { symbol: "R_{TW}", meaning: "Linked cumulative time-weighted return", unit: "decimal over full horizon" },
        ],
        assumptions: ["TWR uses valuations at each external flow.", "IRR's t values describe equally spaced periods; final portfolio value is treated as a terminal receipt."],
        domain: "Nonzero valid opening values for subperiods; search i > -1 and verify a near-zero NPV. Cash-flow sign changes do not guarantee a unique root.",
        interpretation: "TWR removes the effect of how much money enters each interval; IRR incorporates the timing and amounts of the investor's capital.",
      },
      {
        id: "annual-log",
        title: "Annualized and log return",
        latex: String.raw`R_{ann}=(1+R_H)^{1/\tau}-1,\qquad r_{log}=\ln(1+R_H)`,
        variables: [
          { symbol: "R_H", meaning: "Return over the observed holding period", unit: "decimal" },
          { symbol: "\\tau", meaning: "Length of observed period in years", unit: "years" },
          { symbol: "R_{ann}", meaning: "Equivalent annual compound return", unit: "decimal per year" },
          { symbol: "r_{log}", meaning: "Continuously compounded return over the observed period", unit: "log return" },
        ],
        assumptions: ["A year-fraction convention is stated.", "Annualizing an observed return expresses an equivalent rate, not a forecast."],
        domain: "tau > 0; RH > -1 for a finite log return. Annual log return is rlog/tau.",
        interpretation: "A 4% six-month return annualizes to 8.16%; its six-month log return is about 3.9221%.",
      },
      {
        id: "real-leveraged",
        title: "Purchasing power and return on equity",
        latex: String.raw`R_{real}=\frac{1+R_{nom}}{1+\pi}-1,\qquad R_E=\frac{(E+B)R_A-B r_B}{E}`,
        variables: [
          { symbol: "R_{nom}, R_{real}, \\pi", meaning: "Nominal return, real return, and inflation over the same period", unit: "decimal returns" },
          { symbol: "E, B", meaning: "Investor equity and borrowing at the beginning", unit: "currency" },
          { symbol: "R_A, r_B, R_E", meaning: "Asset return, borrowing rate, and return on investor equity", unit: "decimal over same period" },
        ],
        assumptions: ["The inflation index represents the purchasing power being measured.", "For leverage, borrowing remains fixed during the period; its interest is paid at the end and fees/taxes are excluded."],
        domain: "Inflation > -100%; E > 0; B >= 0.",
        interpretation: "Real return divides wealth growth by price growth. Leveraged return deducts financing cost before measuring the gain against the investor's own capital.",
      },
    ],
    workedExamples: [
      {
        id: "returns-timing",
        title: "More money arrives before the losing year",
        given: ["At time 0, the investor contributes 1,000.", "At the end of year 1 the portfolio is worth 1,100, immediately before a 900 contribution.", "At the end of year 2 the portfolio is liquidated for 1,800. There are no other distributions or fees."],
        find: "Cumulative and annualized TWR, annual MWR, and an explanation of their difference.",
        plan: "Calculate returns between flows, link and annualize them, then solve the investor cash-flow equation using -1,000, -900, and +1,800.",
        calculate: [
          { description: "Separate the two performance intervals.", latex: String.raw`r_1=1100/1000-1=0.10,\quad r_2=1800/(1100+900)-1=-0.10`, result: "+10% in year 1; -10% in year 2." },
          { description: "Link growth factors, then express the two-year result annually.", latex: String.raw`R_{TW}=1.10(0.90)-1=-0.01,\quad R_{TW,ann}=\sqrt{0.99}-1`, result: "Cumulative TWR = -1.0000%; annualized TWR = -0.5013%." },
          { description: "Solve the periodic investor cash-flow equation.", latex: String.raw`-1000-\frac{900}{1+i}+\frac{1800}{(1+i)^2}=0`, result: "Annual MWR = -3.4903%. The admissible root has 1 + i > 0." },
        ],
        interpret: "The larger contribution arrives before the loss. Consequently more investor capital experiences -10% than +10%, and MWR is below annualized TWR. The manager's linked two-year path remains -1% regardless of that contribution's size, provided subperiod returns remain the same.",
        sanityCheck: "Without the second contribution, 1,000 would grow to 990. That is a 1% cumulative loss, matching TWR. Substitute the unrounded MWR into NPV to recover approximately zero.",
      },
      {
        id: "returns-average",
        title: "A symmetric pair of percentages loses money",
        given: ["Two consecutive annual returns are +20% and -20%.", "Starting capital is 100, with no external flows."],
        find: "Arithmetic mean, geometric mean, and ending capital.",
        plan: "Average the two observations separately from linking their wealth factors.",
        calculate: [
          { description: "Calculate the ordinary average.", latex: String.raw`\bar R_A=(0.20-0.20)/2=0`, result: "Arithmetic mean = 0%." },
          { description: "Compound and take the two-year growth factor's square root.", latex: String.raw`V_2=100(1.20)(0.80)=96,\quad \bar R_G=\sqrt{0.96}-1`, result: "Ending capital = 96; geometric mean = -2.0204% per year." },
        ],
        interpret: "Zero average annual percentage return does not mean zero wealth change. The second loss is applied to 120, so it removes 24 after the first gain added only 20.",
        sanityCheck: "Compounding -2.0204% twice approximately reproduces 96; compounding 0% would incorrectly reproduce 100.",
      },
    ],
    misconceptions: [
      { claim: "A 20% gain followed by a 20% loss breaks even.", correction: "The loss applies to a larger base. Link growth factors: 1.20 × 0.80 = 0.96." },
      { claim: "IRR and TWR must agree because they use the same portfolio.", correction: "External cash-flow timing changes the investor's exposure. Compare the two measures on the same annualized or cumulative basis." },
      { claim: "A high annualized short-period return is a forecast for the year.", correction: "Annualization is a unit conversion based on compounding, not evidence that performance will recur." },
      { claim: "Subtracting inflation always gives the exact real return.", correction: "Subtraction is an approximation. Exact purchasing-power growth is (1 + nominal return)/(1 + inflation) - 1." },
    ],
    assessments: [
      {
        id: "r1-average-check", objectiveId: "1.b",
        prompt: "An investment earns +25% in year 1 and -20% in year 2, with no flows. Which pair gives the arithmetic and geometric mean annual returns?",
        options: [
          { id: "a", text: "Arithmetic 2.5%; geometric 0.0%", feedback: "Correct. The average is (25 - 20)/2, while 1.25 × 0.80 = 1.00." },
          { id: "b", text: "Arithmetic 0.0%; geometric 2.5%", feedback: "This reverses the meanings: wealth breaks even, while the ordinary mean is positive." },
          { id: "c", text: "Arithmetic 2.5%; geometric 5.0%", feedback: "The 5% sum of the returns is neither a compounded return nor a geometric annual mean." },
          { id: "d", text: "Arithmetic 5.0%; geometric 0.0%", feedback: "The geometric result is right, but the arithmetic sum must be divided by two years." },
        ],
        correctOptionId: "a", solution: "Arithmetic = (0.25 - 0.20)/2 = 0.025. Geometric = sqrt(1.25 × 0.80) - 1 = 0.",
      },
      {
        id: "r1-timing-check", objectiveId: "1.c",
        prompt: "A manager earns +10% then -10% in two equal years. A client doubles the capital immediately before year 2. Which statement best explains the resulting performance measures?",
        options: [
          { id: "a", text: "TWR rises because the deposit increases the account balance.", feedback: "TWR adjusts for external deposits, so a larger balance does not itself represent performance." },
          { id: "b", text: "Annual MWR exceeds annualized TWR because more capital was invested.", feedback: "More capital experiences the losing year, which pulls MWR downward rather than upward." },
          { id: "c", text: "Annual MWR falls below annualized TWR because more capital faces the loss.", feedback: "Correct. The investor's capital is concentrated in the weaker interval while TWR links the two interval returns." },
          { id: "d", text: "Annual MWR equals annualized TWR because the intervals have equal length.", feedback: "Equal interval lengths do not remove the effect of different amounts invested in those intervals." },
        ],
        correctOptionId: "c", solution: "TWR compounds to 1.10 × 0.90 - 1 = -1% over two years. Weighting more invested capital toward the second year's loss makes annual MWR lower than sqrt(0.99) - 1.",
      },
      {
        id: "r1-real-check", objectiveId: "1.e",
        prompt: "A portfolio's one-year nominal return after fees is 8%, and the relevant inflation rate is 3%. What is its exact real return, rounded to two decimals?",
        options: [
          { id: "a", text: "5.00%", feedback: "This subtracts inflation and is an approximation, not the requested exact purchasing-power return." },
          { id: "b", text: "4.85%", feedback: "Correct. Divide 1.08 by 1.03 and subtract one: 0.0485437." },
          { id: "c", text: "7.77%", feedback: "This divides the return 0.08 by 1.03; purchasing-power adjustment must divide the entire wealth factor 1.08." },
          { id: "d", text: "11.24%", feedback: "Multiplying 1.08 by 1.03 adds price inflation to wealth growth rather than removing it." },
        ],
        correctOptionId: "b", solution: "Real return = 1.08/1.03 - 1 = 0.0485437, or 4.85%.",
      },
    ],
  },
  {
    readingId: 57,
    title: "Duration: translate a yield move into price risk",
    sourceRefs: [
      { book: 3, pdfPage: 96, heading: "LOS 57.a — Modified duration" },
      { book: 3, pdfPage: 97, heading: "Approximate modified duration" },
      { book: 3, pdfPage: 98, heading: "Money duration" },
      { book: 3, pdfPage: 99, heading: "PVBP and LOS 57.b — Duration properties" },
    ],
    objectives: [
      { id: "57.a", description: "Calculate modified duration, money duration, and PVBP with consistent yield, time, and price units." },
      { id: "57.b", description: "Explain how coupon, maturity, and yield affect price sensitivity, including the limits of the usual rules." },
    ],
    sections: [
      {
        heading: "One risk, three useful scales",
        body: [
          "Modified duration measures the local slope of the bond's price-yield relationship as a proportional price change. Money duration scales that sensitivity by the full market value of a position. PVBP expresses approximately how much currency is at risk for a one-basis-point yield move. The three numbers describe the same local exposure at different scales.",
          "Keep Macaulay duration in years and yield quoted annually with its compounding frequency. For a semiannual bond, divide annual Macaulay duration by 1 + YTM/2 to obtain annual modified duration. If duration is instead supplied in coupon periods, convert it to years first. Do not divide an already annual duration by two again.",
        ],
      },
      {
        heading: "Use decimals and the full position value",
        body: [
          "A 40-basis-point rise is +0.004, not 0.40. Multiply it by negative modified duration to estimate the proportional price change. Multiplying again by the full position value gives the currency change. A price quoted per 100 of face value is not the whole portfolio value: first multiply that quote by face amount/100.",
          "Full price includes accrued interest. Money duration based on clean price alone understates the relevant value between coupon dates. PVBP is usually quoted as a positive magnitude; use the yield direction and position sign to determine whether the actual change is a gain or loss.",
        ],
      },
      {
        heading: "What changes duration?",
        body: [
          "For otherwise comparable fixed-cash-flow bonds, a lower coupon puts more of the present value farther in the future, increasing sensitivity. A lower yield generally increases duration. Longer maturity usually increases duration, but very long discount coupon bonds can violate that simple maturity rule. A zero-coupon bond's Macaulay duration equals its remaining maturity.",
          "A floating-rate note resets its coupon, so reference-rate price risk is often closer to the time until its next reset than to its final maturity. That observation does not remove credit-spread or liquidity risk. Keep the risk being shocked explicit.",
        ],
      },
      {
        heading: "A local estimate, not a complete repricing model",
        body: [
          "Modified duration is a tangent-line approximation. For a conventional option-free bond with positive convexity, the tangent understates the gain when yield falls and overstates the loss when yield rises. The error grows with the size of the yield move. Use convexity or direct repricing for a larger move.",
          "Yield-based duration assumes the promised cash-flow schedule stays fixed as yield changes. Bonds whose cash flows change with exercise or prepayment need an appropriate effective-duration or scenario approach. A single yield shock also cannot describe every nonparallel change in the term structure.",
        ],
      },
    ],
    formulas: [
      {
        id: "modified-duration", title: "Annual modified duration",
        latex: String.raw`D_{mod}=\frac{D_{Mac}}{1+y/m},\qquad \frac{\Delta P}{P}\approx-D_{mod}\Delta y`,
        variables: [
          { symbol: "D_{Mac}", meaning: "Macaulay duration already measured in years", unit: "years" },
          { symbol: "y", meaning: "Annual nominal YTM compounded m times a year", unit: "decimal per year" },
          { symbol: "m", meaning: "Coupon/compounding periods per year", unit: "periods per year" },
          { symbol: "D_{mod}", meaning: "Sensitivity to the annual quoted yield", unit: "years; proportional price change per unit annual yield" },
          { symbol: "\\Delta y", meaning: "Change in annual quoted yield", unit: "decimal; 1 bp = 0.0001" },
        ],
        assumptions: ["Cash flows do not change with the yield shock.", "Yield convention and duration units match; the move is small for the linear price estimate."],
        domain: "m > 0; 1 + y/m > 0; full price P > 0.",
        interpretation: "Modified duration 5 implies approximately a 0.05% price loss for a one-basis-point increase in yield.",
      },
      {
        id: "approx-duration", title: "Estimate duration by repricing",
        latex: String.raw`D_{mod}\approx\frac{P_{-}-P_{+}}{2P_0\Delta y}`,
        variables: [
          { symbol: "P_0", meaning: "Current full price", unit: "currency or price per 100" },
          { symbol: "P_{-},P_{+}", meaning: "Prices after equal downward/upward yield shocks", unit: "same units as P0" },
          { symbol: "\\Delta y", meaning: "Positive magnitude of each annual yield shock", unit: "decimal" },
        ],
        assumptions: ["Reprice the same fixed cash flows at symmetric yield changes.", "Prices use the same settlement date and quoting basis."],
        domain: "P0 > 0; delta y > 0; small enough shock for a local estimate.",
        interpretation: "Subtract the lower-price upward-shock value from the higher-price downward-shock value, then normalize by price and shock size.",
      },
      {
        id: "money-duration", title: "Currency exposure and one-basis-point exposure",
        latex: String.raw`MD=D_{mod}V_{full},\qquad \Delta V\approx-MD\Delta y,\qquad PVBP\approx MD\times0.0001`,
        variables: [
          { symbol: "V_{full}", meaning: "Full market value of the entire position", unit: "currency" },
          { symbol: "MD", meaning: "Money duration for a unit change in annual yield", unit: "currency per unit decimal yield" },
          { symbol: "PVBP", meaning: "Magnitude of a one-basis-point price change", unit: "currency per basis point" },
          { symbol: "\\Delta V", meaning: "Estimated signed change in position value", unit: "currency" },
        ],
        assumptions: ["A positive long position in a fixed-cash-flow bond.", "Duration is annual and full value includes accrued interest."],
        domain: "Use 0.0001 for one basis point, not 0.01. Position value must not be confused with a quote per 100.",
        interpretation: "Money duration is not the loss from a 1% move; multiply it by 0.01 for that move. PVBP is money duration divided by 10,000.",
      },
    ],
    workedExamples: [
      {
        id: "duration-position", title: "From annual Macaulay duration to a currency loss",
        given: ["Face amount = 1,000,000; full price = 102 per 100 of face.", "Annual Macaulay duration = 5.20 years; nominal annual YTM = 8%, compounded semiannually.", "Consider a +40 bp yield change, with fixed cash flows."],
        find: "Annual modified duration, money duration, PVBP, and the estimated change in full value.",
        plan: "Convert the quote into position value, convert Macaulay to modified duration, then apply the decimal yield shock.",
        calculate: [
          { description: "Compute position value and annual sensitivity.", latex: String.raw`V_{full}=1{,}000{,}000\frac{102}{100}=1{,}020{,}000,\quad D_{mod}=\frac{5.20}{1+0.08/2}=5.00`, result: "Full value = 1,020,000; annual modified duration = 5.00." },
          { description: "Scale duration into currency and basis points.", latex: String.raw`MD=5(1{,}020{,}000)=5{,}100{,}000,\quad PVBP\approx5{,}100{,}000(0.0001)=510`, result: "Money duration = 5,100,000 per unit yield; PVBP approximately 510 per bp." },
          { description: "Apply the 40 bp increase.", latex: String.raw`\Delta V\approx-5{,}100{,}000(0.004)=-20{,}400,\quad V_{new}\approx999{,}600`, result: "Estimated price loss = 2.00%, or 20,400; estimated new full value = 999,600." },
        ],
        interpret: "Higher required yield lowers the value of the fixed cash flows. The 20,400 loss is a first-order estimate; direct repricing can differ because of convexity.",
        sanityCheck: "40 bp × 510 per bp = 20,400. The estimated loss is 20,400/1,020,000 = 2%, matching 5 × 0.4%.",
      },
    ],
    misconceptions: [
      { claim: "A 50 bp change is 0.50 in the formula.", correction: "50 bp = 0.50 percentage points = 0.005 as a decimal yield change." },
      { claim: "A six-year duration means every cash flow arrives in six years.", correction: "Duration summarizes timing or sensitivity; coupon and principal payments can occur on many dates." },
      { claim: "Money duration and PVBP are interchangeable numbers.", correction: "Their yield units differ by a factor of 10,000. Label currency per unit decimal yield versus currency per basis point." },
      { claim: "Longer maturity always means higher duration.", correction: "It is a useful general tendency with other factors held fixed, but some very long discount coupon bonds are exceptions." },
    ],
    assessments: [
      {
        id: "r57-sign", objectiveId: "57.a",
        prompt: "A bond has annual modified duration 4.8. If its annual quoted yield falls by 25 bp, what is the duration-only estimate of the percentage price change?",
        options: [
          { id: "a", text: "-1.20%", feedback: "The magnitude is right, but a yield decline raises the price of these fixed cash flows." },
          { id: "b", text: "+12.00%", feedback: "This uses a yield move ten times too large: 25 bp is 0.0025." },
          { id: "c", text: "+0.12%", feedback: "This uses a yield move ten times too small: 25 bp is 0.0025." },
          { id: "d", text: "+1.20%", feedback: "Correct. -4.8 × (-0.0025) = +0.012." },
        ],
        correctOptionId: "d", solution: "Delta yield = -0.0025; proportional price change is approximately -4.8 × -0.0025 = 0.012, or +1.20%.",
      },
      {
        id: "r57-pvbp", objectiveId: "57.a",
        prompt: "A long bond position has full market value 750,000 and annual modified duration 6.4. What is its approximate PVBP?",
        options: [
          { id: "a", text: "48 currency units per bp", feedback: "The result is ten times too small. One basis point is 0.0001, not 0.00001." },
          { id: "b", text: "480 currency units per bp", feedback: "Correct. 750,000 × 6.4 × 0.0001 = 480." },
          { id: "c", text: "4,800 currency units per bp", feedback: "This corresponds to 10 basis points, not one." },
          { id: "d", text: "48,000 currency units per bp", feedback: "This is the approximate change for a full percentage-point yield move, or 100 bp." },
        ],
        correctOptionId: "b", solution: "Money duration = 4,800,000; PVBP = 4,800,000/10,000 = 480.",
      },
      {
        id: "r57-coupon", objectiveId: "57.b",
        prompt: "Two option-free bonds have the same maturity, YTM, and coupon frequency. One pays a 2% coupon and the other an 8% coupon. Which usually has greater percentage price sensitivity to the same small yield move?",
        options: [
          { id: "a", text: "The 2% bond, because more value is concentrated later.", feedback: "Correct. The smaller early coupons leave a larger proportion of present value in later cash flows." },
          { id: "b", text: "The 8% bond, because its periodic cash payments are larger.", feedback: "Larger earlier payments reduce the weighted timing of value, usually lowering duration." },
          { id: "c", text: "Both equally, because remaining maturities are identical.", feedback: "Maturity alone does not determine duration; the distribution of coupon cash flows also matters." },
          { id: "d", text: "Both equally, because their quoted yields are identical.", feedback: "Equal yields do not offset the different timing weights created by the coupon rates." },
        ],
        correctOptionId: "a", solution: "With maturity, YTM, and frequency held fixed, the lower-coupon bond has higher duration and therefore greater local percentage price sensitivity.",
      },
    ],
  },
  {
    readingId: 83,
    title: "Portfolio risk: combine exposures, then choose a trade-off",
    sourceRefs: [
      { book: 4, pdfPage: 67, heading: "LOS 83.a — Historical risk and return" },
      { book: 4, pdfPage: 68, heading: "LOS 83.b — Risk aversion" },
      { book: 4, pdfPage: 69, heading: "LOS 83.c — Utility and the capital allocation line" },
      { book: 4, pdfPage: 72, heading: "LOS 83.d — Historical means, variances, and covariance" },
      { book: 4, pdfPage: 75, heading: "LOS 83.e — Portfolio standard deviation" },
      { book: 4, pdfPage: 76, heading: "LOS 83.f — Diversification and correlation" },
      { book: 4, pdfPage: 79, heading: "LOS 83.g — Minimum-variance and efficient frontiers" },
    ],
    objectives: [
      { id: "83.a", description: "Compare major asset classes using risk, return, liquidity, and distribution characteristics." },
      { id: "83.b", description: "Explain why risk aversion permits taking risk when expected compensation is sufficient." },
      { id: "83.c", description: "Select a feasible portfolio using investor preferences and a capital allocation line." },
      { id: "83.d", description: "Calculate historical sample means, variances, covariance, and correlation with consistent units." },
      { id: "83.e", description: "Calculate a two-asset portfolio's standard deviation using weights and covariance." },
      { id: "83.f", description: "Explain what lower correlation can and cannot do for diversification." },
      { id: "83.g", description: "Distinguish the global minimum-variance portfolio, minimum-variance frontier, and efficient frontier." },
    ],
    sections: [
      {
        heading: "Start with characteristics, not a league table",
        body: [
          "Cash-like bills, bonds, and equities expose investors to different risks and sources of return. Compare credit quality, maturity, liquidity, inflation exposure, and the uncertainty of cash flows alongside a historical mean and standard deviation. A historical ranking is evidence about a particular sample, not a guaranteed future ordering.",
          "Standard deviation counts variation on both sides of the mean. It does not describe every downside hazard. Skewness, heavy tails, stale valuations, and difficulty selling an asset can make two investments with similar measured volatility behave very differently during stress.",
        ],
      },
      {
        heading: "Measure co-movement from matched observations",
        body: [
          "Use returns from the same dates and equal-length intervals. Subtract each asset's own mean, multiply the paired deviations, and average those products using the sample denominator n - 1. Positive covariance means above-average outcomes tend to occur together; negative covariance means they tend to offset.",
          "Correlation divides covariance by the product of the two standard deviations. It is unitless and bounded between -1 and +1. Zero correlation means no linear co-movement, not necessarily independence. Estimated correlations can change, particularly during market stress.",
        ],
      },
      {
        heading: "Average returns; combine variances and cross terms",
        body: [
          "Expected portfolio return is a weighted average of expected asset returns. Portfolio volatility is generally not a weighted average of individual volatilities because the covariance term changes how shocks combine. First calculate variance, then take its square root to recover standard deviation.",
          "For positive weights, reducing correlation while holding asset volatilities fixed reduces portfolio variance. Correlation below +1 lowers volatility relative to the weighted average of standalone volatilities, but need not make the portfolio safer than the least volatile asset. At correlation -1, only the particular offsetting weights cancel volatility completely.",
        ],
      },
      {
        heading: "Risk aversion is a trade-off, not a ban on risky assets",
        body: [
          "A risk-averse investor prefers less risk when expected returns are equal, but may accept additional risk for sufficient expected return. In a simple mean-variance utility model, a larger positive risk-aversion coefficient gives the variance penalty greater weight. Use one return-unit convention throughout; changing from decimals to whole percentages without rescaling changes the model.",
          "Combining a chosen risky portfolio with a risk-free asset creates a capital allocation line. Moving along it changes the amount invested in risk, while the risky portfolio's composition stays fixed. The investor chooses the feasible mix reaching the highest indifference curve. A less risk-averse investor generally chooses more risky exposure under the same opportunities and borrowing assumptions.",
        ],
      },
      {
        heading: "Separate the opportunity set from investor preference",
        body: [
          "The minimum-variance frontier contains the lowest-variance risky portfolio for each feasible expected return. Its leftmost point is the global minimum-variance portfolio. The efficient frontier is the upper branch: moving below that branch accepts less expected return than another feasible portfolio at the same risk.",
          "Being efficient does not select a single best portfolio for everyone. It eliminates dominated choices; preferences and constraints determine the final selection. An efficient frontier built from estimates is conditional on those estimates and its investment constraints.",
        ],
      },
    ],
    formulas: [
      {
        id: "sample-risk", title: "Sample variance, covariance, and correlation",
        latex: String.raw`\bar R=\frac{1}{n}\sum_{t=1}^{n}R_t,\quad s^2=\frac{\sum_{t=1}^{n}(R_t-\bar R)^2}{n-1},\quad s_{AB}=\frac{\sum_{t=1}^{n}(R_{At}-\bar R_A)(R_{Bt}-\bar R_B)}{n-1},\quad \rho_{AB}=\frac{s_{AB}}{s_A s_B}`,
        variables: [
          { symbol: "R_{At}, R_{Bt}", meaning: "Paired observations of two asset returns", unit: "decimal per period" },
          { symbol: "n", meaning: "Number of paired observations", unit: "observations" },
          { symbol: "s^2, s_{AB}", meaning: "Sample variance and sample covariance", unit: "squared decimal return" },
          { symbol: "s_A,s_B", meaning: "Sample standard deviations", unit: "decimal return" },
          { symbol: "\\rho_{AB}", meaning: "Sample linear correlation", unit: "unitless" },
        ],
        assumptions: ["Both series use matching dates, horizons, and return definitions.", "n - 1 is used for sample estimates; a known population uses its population definition instead."],
        domain: "n >= 2; correlation requires positive standard deviations for both assets.",
        interpretation: "Covariance retains the return scale; correlation standardizes the co-movement. A sample estimate is not a guarantee of future dependence.",
      },
      {
        id: "portfolio-risk", title: "Two-asset expected return and standard deviation",
        latex: String.raw`E(R_p)=w_A\mu_A+w_B\mu_B,\qquad \sigma_p=\sqrt{w_A^2\sigma_A^2+w_B^2\sigma_B^2+2w_Aw_B\sigma_A\sigma_B\rho_{AB}}`,
        variables: [
          { symbol: "w_A,w_B", meaning: "Fractions of portfolio market value", unit: "decimal weights" },
          { symbol: "\\mu_A,\\mu_B", meaning: "Expected asset returns for the same horizon", unit: "decimal return" },
          { symbol: "\\sigma_A,\\sigma_B,\\sigma_p", meaning: "Asset and portfolio standard deviations", unit: "decimal return" },
          { symbol: "\\rho_{AB}", meaning: "Correlation of the asset returns", unit: "unitless" },
        ],
        assumptions: ["This lesson uses a fully invested, long-only two-asset portfolio.", "Weights are initial weights over the return interval and inputs describe the same horizon."],
        domain: "wA + wB = 1; each weight is in [0,1]; volatilities >= 0; correlation in [-1,1].",
        interpretation: "The cross term measures how the two positions reinforce or offset each other. Taking the square root is essential before reporting volatility.",
      },
      {
        id: "utility-cal", title: "Risk preference and a capital allocation line",
        latex: String.raw`U=E(R_c)-\frac{A}{2}\sigma_c^2,\qquad E(R_c)=R_f+a[E(R_p)-R_f],\qquad \sigma_c=a\sigma_p`,
        variables: [
          { symbol: "A", meaning: "Risk-aversion coefficient in this decimal-return convention", unit: "preference parameter" },
          { symbol: "a", meaning: "Fraction invested in the chosen risky portfolio", unit: "decimal weight" },
          { symbol: "R_f", meaning: "Risk-free return over the same horizon", unit: "decimal return" },
          { symbol: "E(R_c), \\sigma_c", meaning: "Complete portfolio expected return and standard deviation", unit: "decimal return" },
          { symbol: "U", meaning: "Mean-variance utility score", unit: "decimal-return-equivalent score, not a realized return" },
        ],
        assumptions: ["The simplified preference model values mean and variance only.", "The risk-free asset has zero variance over the chosen horizon; this example excludes borrowing and short positions."],
        domain: "A > 0 for a risk-averse investor; 0 <= a <= 1 here; use decimal returns and squared decimal variance throughout.",
        interpretation: "The CAL supplies feasible mixes; utility ranks them for one investor. More risk aversion raises the penalty for a given variance.",
      },
    ],
    workedExamples: [
      {
        id: "portfolio-two-assets", title: "Diversification helps without making risk disappear",
        given: ["Asset A: expected annual return 9%, annual standard deviation 20%.", "Asset B: expected annual return 4%, annual standard deviation 10%.", "Weights: 60% in A and 40% in B; correlation = 0.25."],
        find: "Portfolio expected return and standard deviation, and the change in volatility if correlation becomes +1.",
        plan: "Average expected returns with portfolio weights. Add both weighted variances and the covariance cross term, then take the square root. Recalculate the correlation term for +1.",
        calculate: [
          { description: "Calculate expected return.", latex: String.raw`E(R_p)=0.60(0.09)+0.40(0.04)=0.07`, result: "Expected annual return = 7.00%." },
          { description: "Combine variances and covariance in decimal units.", latex: String.raw`\sigma_p^2=0.60^2(0.20)^2+0.40^2(0.10)^2+2(0.60)(0.40)(0.20)(0.10)(0.25)=0.0184`, result: "Variance = 0.0184 squared decimal return." },
          { description: "Convert variance to volatility and compare with perfect positive correlation.", latex: String.raw`\sigma_p=\sqrt{0.0184}=0.1356466,\quad \sigma_{p,\rho=1}=0.60(0.20)+0.40(0.10)=0.16`, result: "Volatility = 13.5647%; at correlation +1 it is 16.00%." },
        ],
        interpret: "Imperfect correlation lowers volatility from the 16% weighted-average benchmark to about 13.56%. It does not make this portfolio less volatile than Asset B alone, whose volatility is 10%.",
        sanityCheck: "With these weights and volatilities, sigma must lie between |0.60×0.20 - 0.40×0.10| = 8% and 16%. The calculated 13.56% lies within those bounds.",
      },
      {
        id: "portfolio-cal-mix", title: "Choose how much of the risky portfolio to hold",
        given: ["Use the previous risky portfolio: expected return 7%, variance 0.0184.", "Risk-free annual return = 2%; borrowing is excluded.", "Compare 50% risky/50% risk-free against 100% risky for an investor with A = 6, using decimal-return utility."],
        find: "Which of these two feasible mixes has higher utility?",
        plan: "Calculate each complete portfolio's expected return and variance, then apply the same utility function. This comparison does not claim either mix is the unrestricted optimum.",
        calculate: [
          { description: "Calculate the half-risky mix.", latex: String.raw`E(R_c)=0.02+0.5(0.07-0.02)=0.045,\quad \sigma_c^2=0.5^2(0.0184)=0.0046`, result: "Expected return = 4.5%; variance = 0.0046; volatility about 6.7823%." },
          { description: "Compare preference scores.", latex: String.raw`U_{half}=0.045-\frac{6}{2}(0.0046)=0.0312,\quad U_{all}=0.07-\frac{6}{2}(0.0184)=0.0148`, result: "Half-risky utility = 0.0312; all-risky utility = 0.0148." },
        ],
        interpret: "For these preferences, the half-risky mix ranks higher despite its lower expected return. The lower variance more than compensates in the investor's utility calculation.",
        sanityCheck: "Halving the risky weight halves volatility but quarters variance. A utility score is not a forecast of the portfolio's realized percentage return.",
      },
    ],
    misconceptions: [
      { claim: "Portfolio standard deviation is always the weighted average of asset standard deviations.", correction: "That equality holds for long-only weights when returns are perfectly positively correlated. Otherwise include the covariance term." },
      { claim: "Zero correlation eliminates all risk or proves independence.", correction: "Zero correlation removes the linear covariance term. The individual variance terms remain, and nonlinear dependence may remain." },
      { claim: "A risk-averse investor must choose the least risky asset.", correction: "Risk aversion compares compensation with additional risk. The preferred portfolio can include risky assets when expected return justifies them." },
      { claim: "Every minimum-variance-frontier portfolio is efficient.", correction: "The lower branch is dominated; the efficient risky frontier is the upper branch beginning at the global minimum-variance portfolio." },
    ],
    assessments: [
      {
        id: "r83-zero-correlation", objectiveId: "83.e",
        prompt: "Two assets each have 20% standard deviation and zero correlation. A portfolio holds equal weights. What is its standard deviation, rounded to two decimals?",
        options: [
          { id: "a", text: "0.00%", feedback: "Zero correlation does not cancel the two positive variance terms." },
          { id: "b", text: "10.00%", feedback: "This keeps only one asset's weighted volatility instead of adding both weighted variances." },
          { id: "c", text: "14.14%", feedback: "Correct. sqrt(0.5²×0.2² + 0.5²×0.2²) = sqrt(0.02)." },
          { id: "d", text: "20.00%", feedback: "This weighted-average result would apply at correlation +1, not zero." },
        ],
        correctOptionId: "c", solution: "Variance = 0.01 + 0.01 = 0.02. Its square root is 0.141421, or 14.14%.",
      },
      {
        id: "r83-risk-preference", objectiveId: "83.b",
        prompt: "A risk-averse investor compares two portfolios with the same expected return of 6%. X has 8% standard deviation and Y has 12%. Other relevant characteristics are identical. Which choice is consistent with risk aversion?",
        options: [
          { id: "a", text: "Prefer X because it offers the same expected return with less risk.", feedback: "Correct. With expected return and other characteristics held fixed, lower variance gives the higher utility." },
          { id: "b", text: "Prefer Y because its larger volatility creates a higher expected return.", feedback: "The question already fixes both expected returns at 6%; more volatility does not change that input." },
          { id: "c", text: "Be indifferent because both portfolios have the same expected return.", feedback: "Ignoring the risk difference would describe risk neutrality in this comparison, not risk aversion." },
          { id: "d", text: "Reject both because risk aversion rules out all uncertain portfolios.", feedback: "Risk aversion allows taking risk for compensation; it does not require avoiding all risky investments." },
        ],
        correctOptionId: "a", solution: "At the same mean, the utility penalty A×variance/2 is smaller for X whenever A > 0.",
      },
      {
        id: "r83-sample-variance", objectiveId: "83.d",
        prompt: "Three equally spaced sample returns are 0%, 2%, and 4%. What is their sample standard deviation?",
        options: [
          { id: "a", text: "1.63%", feedback: "This uses the population denominator n = 3. The question asks for a sample estimate using n - 1." },
          { id: "b", text: "2.00%", feedback: "Correct. Deviations are -0.02, 0, and +0.02; divide their squared sum by 2, then take the square root." },
          { id: "c", text: "2.83%", feedback: "This takes the square root of the squared-deviation sum without dividing by n - 1." },
          { id: "d", text: "4.00%", feedback: "This is the range from the lowest to highest return, not the sample standard deviation." },
        ],
        correctOptionId: "b", solution: "Mean = 2%. Sample variance = (0.0004 + 0 + 0.0004)/2 = 0.0004. Sample standard deviation = 0.02, or 2%.",
      },
    ],
  },
];
