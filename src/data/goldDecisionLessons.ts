import type { GoldLesson } from "./goldQuantLessons";

export type FrameworkKind = "process" | "formula-set" | "decision-tree";

export type AssessmentSkill =
  | "calculation"
  | "application"
  | "diagnosis"
  | "transfer";

export type AssessmentOptionId = "A" | "B" | "C" | "D";

export type SourceReference = {
  book: 2 | 4;
  readingId: 28 | 91;
  moduleIds: string[];
  outcomeIds: string[];
  locator: string;
  coverage: string[];
};

export type LearningObjective = {
  id: string;
  text: string;
};

export type FormulaVariable = {
  symbol: string;
  meaning: string;
  unit?: string;
};

export type LessonFormula = {
  name: string;
  latex: string;
  plainText: string;
  variables: FormulaVariable[];
  interpretation: string;
  conditions: string[];
};

export type DecisionFramework = {
  id: string;
  title: string;
  kind: FrameworkKind;
  purpose: string;
  steps: string[];
  formulas: LessonFormula[];
};

export type MiniExample = {
  title: string;
  setup: string;
  walkthrough: string[];
  takeaway: string;
};

export type ExplanatorySection = {
  moduleId: string;
  title: string;
  outcomeIds: string[];
  lead: string;
  paragraphs: string[];
  keyPoints: string[];
  miniExample?: MiniExample;
};

export type ComparisonTable = {
  id: string;
  title: string;
  caption: string;
  columns: string[];
  rows: string[][];
};

export type WorkedDecisionCase = {
  title: string;
  given: string[];
  find: string[];
  plan: string[];
  analysis: string[];
  decision: string[];
  sanityCheck: string[];
};

export type Misconception = {
  claim: string;
  correction: string;
  diagnostic: string;
};

export type AssessmentOption = {
  id: AssessmentOptionId;
  text: string;
  feedback: string;
};

export type AssessmentItem = {
  id: string;
  objectiveIds: string[];
  skill: AssessmentSkill;
  prompt: string;
  options: AssessmentOption[];
  correctOptionId: AssessmentOptionId;
  solution: string[];
};

export type DecisionLessonDetail = {
  readingId: 28 | 91;
  title: string;
  topic: "Financial Statement Analysis" | "Ethical and Professional Standards";
  sourceRefs: SourceReference[];
  objectives: LearningObjective[];
  decisionFrameworks: DecisionFramework[];
  explanatorySections: ExplanatorySection[];
  comparisonTables: ComparisonTable[];
  workedDecisionCase: WorkedDecisionCase;
  misconceptions: Misconception[];
  assessments: AssessmentItem[];
};

const reading28: DecisionLessonDetail = {
  readingId: 28,
  title: "Analyzing Income Statements",
  topic: "Financial Statement Analysis",
  sourceRefs: [
    {
      book: 2,
      readingId: 28,
      moduleIds: ["28.1"],
      outcomeIds: ["28.a"],
      locator: "Reading 28, Module 28.1 and its key-concept review",
      coverage: [
        "contract and performance-obligation analysis",
        "transaction-price allocation",
        "point-in-time versus over-time recognition",
        "principal-agent presentation",
      ],
    },
    {
      book: 2,
      readingId: 28,
      moduleIds: ["28.2"],
      outcomeIds: ["28.b"],
      locator: "Reading 28, Module 28.2 and its key-concept review",
      coverage: [
        "matching and period costs",
        "capitalization versus immediate expense",
        "estimate changes and analytical effects",
      ],
    },
    {
      book: 2,
      readingId: 28,
      moduleIds: ["28.3"],
      outcomeIds: ["28.c"],
      locator: "Reading 28, Module 28.3 and its key-concept review",
      coverage: [
        "continuing and discontinued operations",
        "unusual or infrequent items",
        "retrospective and prospective accounting changes",
      ],
    },
    {
      book: 2,
      readingId: 28,
      moduleIds: ["28.4"],
      outcomeIds: ["28.d"],
      locator: "Reading 28, Module 28.4 and its key-concept review",
      coverage: [
        "basic and diluted earnings per share",
        "weighted-average shares",
        "if-converted and treasury-stock methods",
        "antidilution",
      ],
    },
    {
      book: 2,
      readingId: 28,
      moduleIds: ["28.5"],
      outcomeIds: ["28.e"],
      locator: "Reading 28, Module 28.5 and its key-concept review",
      coverage: [
        "vertical common-size analysis",
        "gross, operating, pretax, and net margins",
        "time-series and peer comparison",
      ],
    },
  ],
  objectives: [
    {
      id: "28.a",
      text: "Determine how much revenue belongs in a reporting period by separating cash collection from fulfillment and control transfer.",
    },
    {
      id: "28.b",
      text: "Classify a cost as matched, period expense, or capitalized asset and trace the effect through income, cash-flow classification, assets, and ratios.",
    },
    {
      id: "28.c",
      text: "Separate sustainable operating earnings from discontinued activities, unusual items, estimate revisions, policy changes, and corrections.",
    },
    {
      id: "28.d",
      text: "Calculate basic and diluted earnings per share and exclude securities that would increase rather than reduce earnings per share.",
    },
    {
      id: "28.e",
      text: "Use common-size statements and margins to identify operating drivers instead of relying on company size or one headline profit number.",
    },
  ],
  decisionFrameworks: [
    {
      id: "28-revenue-model",
      title: "Revenue recognition as a fulfillment decision",
      kind: "process",
      purpose:
        "Determine what the customer has purchased, how the price is assigned, and when each promised item becomes earned revenue.",
      steps: [
        "Confirm that an enforceable customer arrangement exists and collection is sufficiently probable.",
        "Separate promises that provide distinct goods or services to the customer.",
        "Estimate the amount expected from the customer, including constrained variable consideration.",
        "Allocate that amount using relative stand-alone selling prices.",
        "Recognize each allocation when control transfers, either at one point or as progress is made over time.",
      ],
      formulas: [
        {
          name: "Relative stand-alone price allocation",
          latex: String.raw`P_i=P_{contract}\times\frac{SSP_i}{\sum_{j=1}^{n}SSP_j}`,
          plainText:
            "allocated price for item i = contract price × item i stand-alone price / total stand-alone prices",
          variables: [
            { symbol: "P_i", meaning: "transaction price allocated to item i", unit: "currency" },
            { symbol: "P_contract", meaning: "total consideration expected under the contract", unit: "currency" },
            { symbol: "SSP_i", meaning: "observable or estimated stand-alone selling price of item i", unit: "currency" },
          ],
          interpretation:
            "A bundled discount is distributed across the promises in proportion to their stand-alone values unless evidence supports a more specific allocation.",
          conditions: [
            "The promises have already been identified as distinct performance obligations.",
            "Variable consideration is included only to the extent a major reversal is not expected.",
          ],
        },
        {
          name: "Current-period revenue for an over-time obligation",
          latex: String.raw`Revenue_t=(P_i\times Progress_{to\ date,t})-Revenue_{recognized\ before\ t}`,
          plainText:
            "current revenue = allocated price × cumulative progress − revenue recognized in earlier periods",
          variables: [
            { symbol: "Progress_to date,t", meaning: "cumulative measure of fulfilled work at date t", unit: "percent" },
            { symbol: "Revenue_recognized before t", meaning: "cumulative revenue through the prior period", unit: "currency" },
          ],
          interpretation:
            "A cumulative progress measure must be converted into the incremental amount earned in the current reporting period.",
          conditions: [
            "The obligation qualifies for over-time recognition.",
            "The selected input or output measure faithfully represents performance.",
          ],
        },
      ],
    },
    {
      id: "28-cost-classification",
      title: "Cost recognition and normalization",
      kind: "decision-tree",
      purpose:
        "Place a cost in the period that consumes its benefit, then make peer results comparable when accounting choices differ.",
      steps: [
        "Ask whether the cost creates a probable, measurable benefit controlled beyond the current period.",
        "If it does, record an asset and allocate its cost as the benefit is consumed; otherwise expense it now.",
        "If the cost is directly associated with recognized revenue, match the cost to that revenue.",
        "Rebuild income, assets, cash-flow classification, and ratios on a common policy before comparing firms.",
      ],
      formulas: [],
    },
    {
      id: "28-eps-model",
      title: "Basic-to-diluted EPS bridge",
      kind: "formula-set",
      purpose:
        "Move from earnings currently available to common holders to the earnings and shares that would exist under dilutive conversion or exercise.",
      steps: [
        "Calculate income available to common shareholders and time-weighted common shares.",
        "Evaluate each potential common security separately under the relevant conversion assumption.",
        "Include instruments in order of greatest dilution and stop when the next instrument would increase EPS.",
        "Confirm that final diluted EPS does not exceed basic EPS for a profitable issuer.",
      ],
      formulas: [
        {
          name: "Basic earnings per share",
          latex: String.raw`EPS_{basic}=\frac{NI-D_{preferred}}{WASO}`,
          plainText:
            "basic EPS = (net income − preferred dividends) / weighted-average common shares",
          variables: [
            { symbol: "NI", meaning: "net income attributable before preferred distributions", unit: "currency" },
            { symbol: "D_preferred", meaning: "preferred dividends for the period", unit: "currency" },
            { symbol: "WASO", meaning: "time-weighted common shares outstanding", unit: "shares" },
          ],
          interpretation:
            "The denominator represents common capital exposed to the period's earnings, adjusted for the timing of share issues and repurchases.",
          conditions: [
            "Stock splits and stock dividends are reflected as if they occurred at the start of all comparative periods.",
          ],
        },
        {
          name: "Incremental shares from options or warrants",
          latex: String.raw`Shares_{incremental}=N\times\frac{P_{average}-X}{P_{average}}`,
          plainText:
            "incremental shares = instruments × (average market price − exercise price) / average market price",
          variables: [
            { symbol: "N", meaning: "shares obtainable through exercise", unit: "shares" },
            { symbol: "P_average", meaning: "average market price during the reporting period", unit: "currency per share" },
            { symbol: "X", meaning: "exercise price", unit: "currency per share" },
          ],
          interpretation:
            "The treasury-stock method assumes exercise proceeds repurchase shares at the period's average market price, leaving only the net share increase.",
          conditions: [
            "Use this expression only when the average market price exceeds the exercise price.",
          ],
        },
        {
          name: "If-converted EPS for convertible debt",
          latex: String.raw`EPS_{if\ converted}=\frac{NI-D_{preferred}+Interest\,(1-T)}{WASO+Shares_{conversion}}`,
          plainText:
            "if-converted EPS = (income available to common + after-tax interest saved) / (weighted shares + conversion shares)",
          variables: [
            { symbol: "T", meaning: "applicable income-tax rate", unit: "percent" },
            { symbol: "Interest", meaning: "interest avoided under assumed conversion", unit: "currency" },
            { symbol: "Shares_conversion", meaning: "common shares issued under assumed conversion", unit: "shares" },
          ],
          interpretation:
            "Debt conversion changes both the numerator and denominator because the company avoids after-tax interest while issuing new shares.",
          conditions: [
            "Exclude the instrument if assumed conversion would raise EPS rather than lower it.",
          ],
        },
      ],
    },
    {
      id: "28-margin-model",
      title: "Common-size profitability bridge",
      kind: "formula-set",
      purpose:
        "Translate statement subtotals into comparable percentages and locate where profitability changes arise.",
      steps: [
        "Set revenue equal to 100% and divide every operating line by revenue.",
        "Compare gross margin first to isolate pricing and production economics.",
        "Compare operating margin next to add operating-cost structure.",
        "Compare pretax and net margins last to incorporate financing, unusual items, and taxes.",
      ],
      formulas: [
        {
          name: "Gross profit margin",
          latex: String.raw`Gross\ margin=\frac{Revenue-COGS}{Revenue}`,
          plainText: "gross margin = (revenue − cost of goods sold) / revenue",
          variables: [
            { symbol: "COGS", meaning: "cost assigned to goods or services sold", unit: "currency" },
          ],
          interpretation:
            "Gross margin reflects selling-price strength and direct production or service-delivery cost.",
          conditions: ["Compare firms only after checking classification consistency."],
        },
        {
          name: "Operating profit margin",
          latex: String.raw`Operating\ margin=\frac{Operating\ income}{Revenue}`,
          plainText: "operating margin = operating income / revenue",
          variables: [],
          interpretation:
            "The gap between gross and operating margin shows the burden of operating overhead and investment in functions such as research or selling.",
          conditions: ["Normalize material nonrecurring operating items before forecasting."],
        },
      ],
    },
  ],
  explanatorySections: [
    {
      moduleId: "28.1",
      title: "Revenue follows performance, not the cash receipt",
      outcomeIds: ["28.a"],
      lead:
        "The analyst's first question is not “When did cash arrive?” but “What did the seller promise, and when did the customer obtain the promised value?”",
      paragraphs: [
        "Cash, receivables, contract liabilities, and revenue can move at different times. Collection before fulfillment creates an obligation to the customer rather than immediate income. Fulfillment before collection can create a receivable and revenue. This distinction is central when subscriptions, construction projects, licenses, warranties, or bundled services stretch across reporting periods.",
        "A bundle must be decomposed into distinct promises before the transaction price is assigned. Relative stand-alone prices prevent management from directing an arbitrary share of a discount toward whichever promise would accelerate revenue. After allocation, each promise is recognized at a point in time or over time according to transfer of control and a faithful measure of progress.",
        "Presentation also matters. A principal controls the promised good or service and normally reports gross revenue and the related expense. An agent arranges for another party to provide it and normally reports the net fee. Profit dollars can be identical under both presentations while reported revenue and margins differ sharply, so analysts must understand the business role before comparing margins.",
      ],
      keyPoints: [
        "Cash received in advance normally creates a contract liability until performance occurs.",
        "Revenue estimates should be constrained when a later reversal is reasonably possible.",
        "For over-time recognition, current revenue equals cumulative earned revenue less amounts recognized previously.",
        "Gross-versus-net presentation changes revenue and percentage margins even when profit is unchanged.",
      ],
      miniExample: {
        title: "Allocate a bundled annual contract",
        setup:
          "A customer pays 90 for equipment and one year of monitoring. Separate prices are 80 for equipment and 40 for monitoring. Equipment is delivered immediately; three months of monitoring are complete at period-end.",
        walkthrough: [
          "Allocate 90 × 80/120 = 60 to equipment and 90 × 40/120 = 30 to monitoring.",
          "Recognize all 60 allocated to delivered equipment.",
          "Recognize 30 × 3/12 = 7.5 for monitoring; defer the remaining 22.5.",
        ],
        takeaway:
          "The 90 cash receipt becomes 67.5 of current revenue and 22.5 of a remaining customer obligation.",
      },
    },
    {
      moduleId: "28.2",
      title: "Expense timing reveals the assumed life of a benefit",
      outcomeIds: ["28.b"],
      lead:
        "A cost belongs in current profit when its benefit is consumed now; it belongs on the balance sheet only when a controlled future benefit can be supported.",
      paragraphs: [
        "Direct costs tied to current revenue are matched to that revenue. General administrative costs and uncertain expenditures are period expenses because no sufficiently measurable future resource has been created. A qualifying long-lived cost is initially recorded as an asset and then allocated through depreciation or amortization as the benefit is used.",
        "Capitalization defers expense rather than eliminating it. Relative to immediate expensing, it raises current income, assets, and equity, moves the acquisition cash outflow from operating to investing classification, and creates lower income in later periods through depreciation or amortization. Total cash flow does not improve merely because the statement category changes.",
        "Analysts should inspect estimate assumptions as closely as the initial classification. Extending an asset's useful life, increasing residual value, or lowering a warranty or bad-debt estimate can lift current profit without stronger operations. Peer comparisons require a normalization that removes these policy and estimate differences.",
      ],
      keyPoints: [
        "Capitalize only when recognition of an asset is justified; managerial preference is not enough.",
        "Immediate expensing is more conservative in the acquisition period but may make later margins appear stronger.",
        "Capitalization generally raises CFO and lowers CFI relative to immediate expensing, with no change in total cash paid.",
        "Ratio direction can reverse over time because both the earnings numerator and asset or equity denominator change.",
      ],
    },
    {
      moduleId: "28.3",
      title: "Rebuild sustainable earnings before forecasting",
      outcomeIds: ["28.c"],
      lead:
        "Reported net income mixes recurring operations with events that may not belong in a forward-looking earnings base.",
      paragraphs: [
        "A discontinued component is separated from continuing operations because its future contribution should disappear. Unusual or infrequent items may remain within continuing operations, so an analyst must judge recurrence instead of relying on the label management uses. Repeated restructuring charges are poor candidates for automatic exclusion.",
        "The treatment of an accounting change tells the analyst how to compare periods. A new accounting policy and correction of a prior error generally rebuild comparative history so like is compared with like. A revised estimate reflects new information and affects the current and future periods without rewriting what was reasonably estimated before.",
        "Normalization is an analytical bridge, not permission to discard every loss. Remove an item from forecast earnings only after understanding its cause, cash effect, recurrence, and connection to the operating model. Keep a reconciliation from reported to adjusted figures so the judgment is visible.",
      ],
      keyPoints: [
        "Discontinued operations are separated below continuing income and presented after tax.",
        "An unusual operating item can still be relevant if the business produces similar charges repeatedly.",
        "Policy changes and error corrections usually affect comparative periods; estimate changes work forward.",
        "A high-quality adjustment has a stated reason, amount, tax effect, and recurrence assumption.",
      ],
    },
    {
      moduleId: "28.4",
      title: "EPS measures a claim on earnings, not simply earnings divided by year-end shares",
      outcomeIds: ["28.d"],
      lead:
        "The numerator belongs to common holders and the denominator represents the time-weighted common capital that participated during the period.",
      paragraphs: [
        "Basic EPS removes preferred distributions from net income and uses weighted-average common shares. New shares enter for the fraction of the period outstanding. Repurchases leave for the remaining fraction. Stock splits and stock dividends are different: they restate the share count for all presented periods because each old share has been divided into more units without a new capital contribution.",
        "Diluted EPS asks what earnings and shares would look like if potential common instruments had converted or been exercised. Convertible debt adds back after-tax interest and adds conversion shares. Convertible preferred adds back its dividend and adds conversion shares. Options and warrants add only the net shares left after assumed exercise proceeds repurchase shares at the average market price.",
        "Potential shares are included only when they reduce EPS for a profitable company. This antidilution test prevents a hypothetical transaction that improves per-share results from being presented as dilution. The result should always be reconciled from basic EPS so the source of dilution is clear.",
      ],
      keyPoints: [
        "Use average, not closing, market price in the treasury-stock calculation.",
        "Evaluate numerator and denominator effects together for convertible debt.",
        "Exclude out-of-the-money options and other antidilutive instruments.",
        "For a profitable issuer, diluted EPS should be less than or equal to basic EPS.",
      ],
    },
    {
      moduleId: "28.5",
      title: "Margins turn an income statement into an operating story",
      outcomeIds: ["28.e"],
      lead:
        "Common-sizing removes the scale difference between firms, but useful interpretation still requires a bridge from one margin level to the next.",
      paragraphs: [
        "Set revenue to 100% and express each income-statement line as a share of revenue. A higher gross margin can reflect pricing power, product mix, or lower direct costs. A widening gap between gross and operating margin can signal heavier selling, administration, or research spending. The net margin adds financing, nonoperating items, and taxes.",
        "A margin change is a question, not an answer. The analyst should identify whether price, volume, mix, unit cost, fixed-cost absorption, classification, or a nonrecurring item moved the ratio. Time-series analysis shows how one firm's economics change; cross-sectional analysis tests the result against peers with similar businesses and accounting.",
        "Common-size analysis can expose strategy. A company may accept a lower current operating margin because research spending is building future products, while another may show a high margin because it is underinvesting. Ratios must be connected to the business model and cash evidence before they support a valuation conclusion.",
      ],
      keyPoints: [
        "Revenue is the usual denominator for operating lines; the effective tax rate instead relates tax expense to pretax income.",
        "Gross margin isolates price and direct cost before operating overhead.",
        "Peer comparison requires similar revenue presentation, especially principal-versus-agent treatment.",
        "Use several periods and a driver bridge rather than ranking firms by one ratio.",
      ],
    },
  ],
  comparisonTables: [
    {
      id: "28-cost-timing",
      title: "Three paths for cost recognition",
      caption:
        "The accounting path follows consumption of economic benefit; the analytical task is to make timing differences comparable.",
      columns: ["Path", "When appropriate", "Current-period effect", "Later-period effect"],
      rows: [
        [
          "Match to revenue",
          "The cost is directly associated with units or service recognized now",
          "Expense moves with the related revenue",
          "Unsold or unperformed portion remains an asset where recognition criteria are met",
        ],
        [
          "Expense immediately",
          "Benefit is consumed now or a future resource cannot be demonstrated",
          "Lower current income and no new long-lived asset",
          "No depreciation or amortization from this outlay",
        ],
        [
          "Capitalize and allocate",
          "A measurable controlled benefit extends beyond the current period",
          "Higher current income than immediate expensing and a larger asset base",
          "Depreciation or amortization reduces later income as the benefit is consumed",
        ],
      ],
    },
    {
      id: "28-reporting-changes",
      title: "Classifying items outside the recurring earnings base",
      caption:
        "Classification determines presentation; recurrence and cash consequences determine the analyst's forecast adjustment.",
      columns: ["Item", "Reporting logic", "Forecast question"],
      rows: [
        [
          "Discontinued component",
          "Separated from continuing operations and shown after tax",
          "Which stranded costs or cash flows remain after disposal?",
        ],
        [
          "Unusual or infrequent item",
          "Usually remains within continuing pretax income",
          "Does the business model make a similar charge likely to recur?",
        ],
        [
          "Change in accounting estimate",
          "Applied to the current and future periods",
          "Did new information justify the estimate, or is the change biased?",
        ],
        [
          "Policy change or error correction",
          "Comparative periods are generally recast for consistency",
          "How do the restated trends differ from the originally reported pattern?",
        ],
      ],
    },
    {
      id: "28-principal-agent",
      title: "Principal versus agent presentation",
      caption:
        "The same economics can produce very different reported revenue and margins.",
      columns: ["Role", "What the firm controls", "Revenue presentation", "Analytical consequence"],
      rows: [
        [
          "Principal",
          "The promised good or service before transfer",
          "Gross customer consideration with the provider cost shown separately",
          "Higher revenue and a lower percentage margin than an otherwise identical net presentation",
        ],
        [
          "Agent",
          "The arranging service rather than the underlying good or service",
          "Net fee or commission retained by the firm",
          "Lower revenue and a higher percentage margin even when profit dollars are unchanged",
        ],
      ],
    },
  ],
  workedDecisionCase: {
    title: "From contract economics to diluted EPS: Helio Systems",
    given: [
      "Helio collects 360,000 at the start of a contract that includes delivered monitoring hardware and 24 months of cloud support.",
      "The stand-alone prices are 240,000 for the hardware and 160,000 for support. Twelve months of support are complete at year-end.",
      "Cost of goods sold is 150,000 and other operating costs before depreciation are 60,000.",
      "Helio places 90,000 of qualifying equipment in service on the first day of the year. It has a three-year life, no residual value, and straight-line depreciation.",
      "Ignore interest and tax. Helio has 3,000 of preferred dividends and 30,000 weighted-average common shares.",
      "Six thousand options are outstanding at an exercise price of 12; the average common-share price is 15.",
    ],
    find: [
      "Current revenue and the remaining contract liability",
      "Operating income, gross margin, and operating margin",
      "Basic and diluted EPS",
      "What the reported figures imply for an analyst comparing Helio with a firm that expenses a similar outlay immediately",
    ],
    plan: [
      "Allocate the contract price using relative stand-alone prices, then recognize the delivered hardware and half of support.",
      "Depreciate the qualifying equipment over its useful life and construct the income bridge.",
      "Calculate basic EPS, apply the treasury-stock method, and verify that the options dilute EPS.",
      "Separate economic cash flow from accounting timing before drawing the comparison conclusion.",
    ],
    analysis: [
      "The stand-alone total is 400,000. Hardware receives 360,000 × 240,000/400,000 = 216,000; support receives 144,000.",
      "Hardware revenue is 216,000. One-half of support is earned, adding 72,000. Current revenue is 288,000 and the unearned contract balance is 72,000.",
      "Annual depreciation is 90,000/3 = 30,000. Operating income is 288,000 − 150,000 − 60,000 − 30,000 = 48,000.",
      "Gross margin is (288,000 − 150,000)/288,000 = 47.9%. Operating margin is 48,000/288,000 = 16.7%.",
      "Basic EPS is (48,000 − 3,000)/30,000 = 1.50.",
      "Incremental option shares are 6,000 × (15 − 12)/15 = 1,200. Diluted EPS is 45,000/31,200 = 1.44, so the options are dilutive.",
      "If the 90,000 outlay had been an immediate period expense, current income would be 60,000 lower than under three-year capitalization. Total cash paid would be unchanged, but operating and investing cash-flow classification would differ.",
    ],
    decision: [
      "Use 288,000, not the 360,000 cash receipt, as current revenue because 72,000 of support remains unperformed.",
      "Report basic EPS of 1.50 and diluted EPS of approximately 1.44.",
      "When comparing Helio with a peer, normalize legitimate cost-timing and presentation differences before treating Helio's higher current earnings or CFO as stronger economics.",
    ],
    sanityCheck: [
      "Allocated prices sum to the 360,000 contract price.",
      "Recognized support equals one-half of its allocation because one-half of the service period is complete.",
      "Gross margin exceeds operating margin because operating costs and depreciation enter below gross profit.",
      "Diluted EPS is below basic EPS, consistent with inclusion of dilutive options.",
      "Accounting classification changes the timing and location of reported amounts, not the 90,000 cash outflow itself.",
    ],
  },
  misconceptions: [
    {
      claim: "Revenue equals the cash collected from the customer during the period.",
      correction:
        "Revenue follows satisfaction of customer promises. Cash received first can remain a liability, while revenue earned before collection can create a receivable.",
      diagnostic:
        "Ask whether any promised good or service remains undelivered at period-end.",
    },
    {
      claim: "Capitalizing a cost improves cash generation because current profit and CFO are higher.",
      correction:
        "Capitalization changes expense timing and usually moves the acquisition outflow from CFO to CFI; total cash paid is unchanged.",
      diagnostic:
        "Reconcile CFO plus CFI and compare the cash balance under both policies.",
    },
    {
      claim: "Every item labeled unusual should be removed from forecast earnings.",
      correction:
        "The analyst must test recurrence and business-model connection. Repeated restructuring or litigation can be economically persistent.",
      diagnostic:
        "Review several years of disclosures and cash flows for similarly described charges.",
    },
    {
      claim: "All potential common shares belong in diluted EPS.",
      correction:
        "Only instruments that reduce EPS are included. Antidilutive options or convertibles are excluded from the diluted result.",
      diagnostic:
        "Calculate each instrument's incremental earnings per share or treasury-stock effect before inclusion.",
    },
    {
      claim: "The larger company is more profitable because it reports more profit dollars.",
      correction:
        "Scale and profitability are different. Common-size margins show profit per unit of revenue, while absolute profit shows total size.",
      diagnostic:
        "Convert both statements to percentages and bridge gross, operating, and net margins.",
    },
  ],
  assessments: [
    {
      id: "28-assessment-1",
      objectiveIds: ["28.a"],
      skill: "calculation",
      prompt:
        "A customer pays 500,000 for a machine and two years of maintenance. Their stand-alone prices are 360,000 and 240,000. The machine is delivered immediately, and 25% of maintenance has been provided by year-end. How much revenue should be recognized by year-end?",
      options: [
        {
          id: "A",
          text: "300,000",
          feedback:
            "This is only the amount allocated to the machine: 500,000 × 360,000/600,000. It omits maintenance already performed.",
        },
        {
          id: "B",
          text: "350,000",
          feedback:
            "Correct. The machine receives 300,000 and maintenance receives 200,000; 25% of maintenance adds 50,000 of revenue.",
        },
        {
          id: "C",
          text: "420,000",
          feedback:
            "This uses the stand-alone machine price rather than its allocated contract price, then adds part of maintenance.",
        },
        {
          id: "D",
          text: "500,000",
          feedback:
            "Cash collection does not make unperformed maintenance revenue. The remaining service allocation stays deferred.",
        },
      ],
      correctOptionId: "B",
      solution: [
        "Total stand-alone prices are 600,000.",
        "Allocate 500,000 × 360,000/600,000 = 300,000 to the machine.",
        "Allocate 200,000 to maintenance and recognize 25%, or 50,000.",
        "Total recognized revenue is 300,000 + 50,000 = 350,000.",
      ],
    },
    {
      id: "28-assessment-2",
      objectiveIds: ["28.b", "28.e"],
      skill: "diagnosis",
      prompt:
        "Two otherwise identical firms pay 120,000 for the same four-year resource on the first day of the year. Firm C qualifies and capitalizes it with straight-line allocation; Firm E records the full amount as an operating expense. Before tax, which year-one comparison is most accurate?",
      options: [
        {
          id: "A",
          text: "Firm C has higher income and assets, lower CFO, higher CFI, and higher asset turnover.",
          feedback:
            "Income and assets are higher, but the cash-flow and asset-turnover directions are reversed. Capitalization normally shifts the outflow to CFI and raises assets.",
        },
        {
          id: "B",
          text: "Firm C has lower income and assets, higher CFO, lower CFI, and lower asset turnover.",
          feedback:
            "The cash-flow and turnover directions fit capitalization, but current income and assets should be higher, not lower.",
        },
        {
          id: "C",
          text: "Both firms have the same income and assets because total cash paid and economic benefit are identical.",
          feedback:
            "Total cash is identical, but recognition timing changes current expense, reported assets, and several ratios.",
        },
        {
          id: "D",
          text: "Firm C has higher income and assets, higher CFO, lower CFI, and lower asset turnover.",
          feedback:
            "Correct. Firm C records 30,000 of year-one allocation rather than 120,000, reports the unconsumed asset, and classifies the acquisition as investing cash flow.",
        },
      ],
      correctOptionId: "D",
      solution: [
        "Firm C records 120,000/4 = 30,000 of expense, 90,000 less than Firm E.",
        "Firm C therefore has income and ending assets 90,000 higher before tax and other effects.",
        "Capitalization generally places the payment in CFI rather than CFO, raising CFO and lowering CFI relative to Firm E.",
        "The larger asset denominator makes Firm C's asset turnover lower, all else equal.",
      ],
    },
    {
      id: "28-assessment-3",
      objectiveIds: ["28.d"],
      skill: "calculation",
      prompt:
        "A profitable company reports net income of 480,000, preferred dividends of 30,000, and 250,000 weighted-average common shares. It has 50,000 options with an exercise price of 18; the average share price is 30. What is diluted EPS?",
      options: [
        {
          id: "A",
          text: "1.80",
          feedback:
            "This is basic EPS: (480,000 − 30,000)/250,000. It omits the dilutive option effect.",
        },
        {
          id: "B",
          text: "1.50",
          feedback:
            "This treats all 50,000 option shares as incremental and ignores the assumed repurchase funded by exercise proceeds.",
        },
        {
          id: "C",
          text: "1.67",
          feedback:
            "Correct. Incremental shares are 50,000 × (30 − 18)/30 = 20,000, so diluted EPS is 450,000/270,000 = 1.67.",
        },
        {
          id: "D",
          text: "1.78",
          feedback:
            "This divides total net income by diluted shares. Preferred dividends must be removed because the numerator belongs to common shareholders.",
        },
      ],
      correctOptionId: "C",
      solution: [
        "Income available to common is 480,000 − 30,000 = 450,000.",
        "Incremental option shares are 50,000 × (30 − 18)/30 = 20,000.",
        "The diluted denominator is 250,000 + 20,000 = 270,000 shares.",
        "Diluted EPS is 450,000/270,000 = 1.6667, or 1.67.",
      ],
    },
  ],
};

const reading91: DecisionLessonDetail = {
  readingId: 91,
  title: "Guidance for Standards I–VII",
  topic: "Ethical and Professional Standards",
  sourceRefs: [
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.1"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.1",
      coverage: ["Knowledge of the Law", "Independence and Objectivity"],
    },
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.2"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.2",
      coverage: ["Misrepresentation", "Misconduct", "Competence"],
    },
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.3"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.3",
      coverage: ["Material Nonpublic Information", "Market Manipulation"],
    },
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.4"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.4",
      coverage: ["Loyalty, Prudence, and Care", "Fair Dealing"],
    },
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.5"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.5",
      coverage: ["Suitability", "Performance Presentation", "Preservation of Confidentiality"],
    },
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.6"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.6",
      coverage: ["Loyalty to Employer", "Additional Compensation", "Responsibilities of Supervisors"],
    },
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.7"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.7",
      coverage: ["Diligence and Reasonable Basis", "Communication", "Record Retention"],
    },
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.8"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.8",
      coverage: ["Conflicts", "Priority of Transactions", "Referral Fees"],
    },
    {
      book: 4,
      readingId: 91,
      moduleIds: ["91.9"],
      outcomeIds: ["91.a", "91.b", "91.c"],
      locator: "Reading 91, Module 91.9",
      coverage: ["Program Conduct", "References to CFA Institute, the designation, and candidacy"],
    },
  ],
  objectives: [
    {
      id: "91.a",
      text: "Apply the relevant professional duty to a fact pattern, including cases in which several duties overlap.",
    },
    {
      id: "91.b",
      text: "Recommend a control that prevents, detects, escalates, or documents a potential violation.",
    },
    {
      id: "91.c",
      text: "Distinguish compliant conduct from a violation and explain why motive, disclosure, or a good outcome does not always cure the conduct.",
    },
    {
      id: "91.integration",
      text: "Separate mandatory conduct from recommended practice and choose the first action that protects clients, markets, employers, and the profession.",
    },
  ],
  decisionFrameworks: [
    {
      id: "91-facts-duty-action",
      title: "Facts → duty → action → control",
      kind: "decision-tree",
      purpose:
        "Prevent ethics questions from becoming a memory contest by connecting the decisive fact to the protected stakeholder and required action.",
      steps: [
        "State only the relevant facts: who knows what, who benefits, who may be harmed, what has been disclosed, and when each event occurs.",
        "Identify every applicable law, professional duty, client mandate, employer policy, and market-integrity concern.",
        "Apply the strictest applicable requirement and test whether intent is legally or professionally relevant to that duty.",
        "Choose the action that stops or avoids harm first; disclosure is useful only where the duty permits the underlying conduct.",
        "Add a preventive control and preserve the record that supports the decision.",
      ],
      formulas: [],
    },
    {
      id: "91-information-test",
      title: "Information-status matrix",
      kind: "decision-tree",
      purpose:
        "Distinguish prohibited use of material nonpublic information from legitimate mosaic research.",
      steps: [
        "Ask whether a reasonable investor would consider the information important or whether it would likely affect price.",
        "Ask whether the information has been broadly disseminated rather than selectively shared.",
        "If both material and nonpublic, do not trade, recommend, or cause others to act; contact compliance and seek public dissemination.",
        "If a nonpublic fact is immaterial, it may be combined with public evidence in a documented independent analysis.",
      ],
      formulas: [],
    },
    {
      id: "91-conflict-priority-test",
      title: "Conflict, disclosure, and transaction priority",
      kind: "process",
      purpose:
        "Determine whether a conflict should be avoided, disclosed, consented to, or subjected to trading controls.",
      steps: [
        "Identify beneficial ownership, compensation, gifts, referral arrangements, outside activities, and issuer relationships.",
        "Avoid the conflict where practical; otherwise disclose it prominently and early to every affected party.",
        "Give client and employer transactions a fair opportunity before beneficial-owner accounts trade.",
        "Use preclearance, restricted lists, duplicate confirmations, and periodic holdings reports to make the rule enforceable.",
      ],
      formulas: [],
    },
  ],
  explanatorySections: [
    {
      moduleId: "91.1",
      title: "Standard I(A)–I(B): lawful conduct and independent judgment",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "Professionalism begins by locating the strictest applicable rule and protecting analysis from pressure, gifts, and pay arrangements.",
      paragraphs: [
        "For Knowledge of the Law, map every governing regime before acting. When requirements conflict, follow the one that demands more protective conduct. A professional who knows of unlawful or noncompliant activity must refuse participation, escalate through appropriate channels, and dissociate if the activity continues. External reporting may be encouraged or legally required, but it is not a universal substitute for stopping one's own involvement.",
        "Independence and Objectivity focuses on whether a benefit or pressure could reasonably distort judgment. The source matters: lavish issuer-paid travel, allocation of scarce investments, outcome-linked research compensation, or vendor incentives create stronger threats than ordinary business hospitality. A client gift can still require employer disclosure because it may influence treatment of that client.",
      ],
      keyPoints: [
        "Apply the strictest of applicable law, regulation, professional standard, and binding policy.",
        "Dissociation means taking practical steps to stop being associated with the questionable activity.",
        "Disclosure can reveal a gift or issuer-paid report, but it does not rescue compensation designed to dictate the conclusion.",
        "Useful controls include compliance consultation, gift limits, travel policy, IPO restrictions, and documented preapproval.",
      ],
    },
    {
      moduleId: "91.2",
      title: "Standard I(C)–I(E): truthful representation, integrity, and competence",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "These duties ask whether the professional presents work honestly, behaves with integrity, and possesses the capability required for the role.",
      paragraphs: [
        "Misrepresentation includes false claims, selective omission that makes a message misleading, unsupported guarantees, unsuitable benchmarks, and presenting another person's analysis or model as one's own. Attribution and retained source records let readers separate original judgment from borrowed work. Facts from recognized reporting services may be treated differently from another analyst's interpretation, but a professional should never imply authorship of work not performed.",
        "Misconduct covers dishonesty, fraud, deceit, and conduct that meaningfully damages professional reputation, integrity, or competence. It is not a tool for punishing every private disagreement. Competence is role-specific: taking a new assignment creates a duty to acquire or obtain the skills needed to perform it. A poor investment outcome by itself does not prove incompetence if the process was capable and reasonable.",
      ],
      keyPoints: [
        "A technically true statement can still mislead through omitted context.",
        "Third-party marketing and research require review; outsourcing does not outsource responsibility.",
        "Maintain a source trail for data, models, charts, and prior research.",
        "Before accepting unfamiliar duties, arrange training, supervision, or qualified support.",
      ],
    },
    {
      moduleId: "91.3",
      title: "Standard II: information integrity and honest markets",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "Market integrity is threatened either by unfair informational advantage or by conduct designed to create a false picture of price or activity.",
      paragraphs: [
        "Materiality depends on importance to a reasonable investor and likely price impact; public status requires broad marketplace availability, not a private call or large investor meeting. When information is both material and nonpublic, the professional must not trade, recommend, or cause others to trade related securities. The appropriate response is to contact compliance, seek public dissemination, and follow information-barrier and restricted-list procedures.",
        "Mosaic research remains legitimate when a conclusion comes from public evidence plus nonmaterial nonpublic observations. The work should be documented so the basis is visible. Market Manipulation is distinct: it targets transactions or communications intended to mislead participants about price, volume, or market conditions. Genuine investment activity can move a price without becoming manipulation; deceptive intent is the dividing fact.",
      ],
      keyPoints: [
        "Test materiality and public status separately.",
        "The prohibition reaches related funds and derivatives, not only the issuer's common shares.",
        "A successful mosaic has an independent analytical bridge, not a hidden material tip.",
        "Information-based and transaction-based schemes can both manipulate a market when designed to deceive.",
      ],
    },
    {
      moduleId: "91.4",
      title: "Standard III(A)–III(B): client loyalty and fair access",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "Client duties govern whose interests control the decision and how investment opportunities are distributed among eligible clients.",
      paragraphs: [
        "Loyalty, Prudence, and Care requires decisions for the client's benefit, within the governing mandate, and with the care appropriate to the relationship. For a pension or trust, the ultimate beneficiaries—not the executive who hired the manager—are the central clients. Brokerage or soft-dollar benefits must support the client investment process rather than subsidize the manager.",
        "Fair Dealing means a fair process, not perfectly simultaneous receipt by every client. New recommendations and material changes need dissemination and allocation procedures that do not favor selected accounts. Suitability or mandate can justify different treatment after all eligible clients receive a fair opportunity. Controls include distribution lists, time-stamped releases, allocation formulas, and post-trade reviews.",
      ],
      keyPoints: [
        "Identify the true beneficiary and the portfolio mandate before acting.",
        "A manager cannot use client assets to buy a benefit mainly for the manager or another client.",
        "Fair does not mean identical; it means objective eligibility, timing, and allocation rules.",
        "Oversubscribed trades should follow a documented allocation method rather than relationship value.",
      ],
    },
    {
      moduleId: "91.5",
      title: "Standard III(C)–III(E): suitability, performance, and confidentiality",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "Advice must fit the client's full circumstances, performance must be presented fairly, and entrusted information must remain protected.",
      paragraphs: [
        "Suitability begins with a reasonable inquiry into objectives, risk capacity and willingness, liquidity, taxes, time horizon, constraints, and experience. An investment is judged in the context of the whole portfolio and current investment policy. A client-directed trade that conflicts with the plan should trigger discussion and documentation; a materially portfolio-changing request may require an updated mandate.",
        "Performance Presentation prohibits cherry-picking and misleading composites, periods, benchmarks, or claims. The audience should receive enough context to understand what the number represents. Preservation of Confidentiality continues after the relationship ends. Disclosure is limited to client permission, a valid legal requirement, or an applicable exception involving unlawful client activity; firm gossip or commercial convenience is not enough.",
      ],
      keyPoints: [
        "Update client information before material advice, not only at account opening.",
        "Portfolio context can make a standalone risky asset suitable as a diversifier—or unsuitable because it compounds an existing exposure.",
        "Performance evidence needs complete accounts, relevant periods, suitable benchmarks, and clear limitations.",
        "When law and confidentiality intersect, consult compliance or counsel and disclose only through proper channels.",
      ],
    },
    {
      moduleId: "91.6",
      title: "Standard IV: duties within the employment relationship",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "Employer duties protect the firm's legitimate business, expose outside incentives, and require supervisors to build systems that can prevent and detect misconduct.",
      paragraphs: [
        "Loyalty does not prevent planning a future departure, but it does prohibit diverting clients, records, confidential models, or paid work while still employed. Firm records belong to the employer unless an agreement says otherwise. Additional Compensation Arrangements require written disclosure and consent before accepting a benefit that could conflict with the employer's interests, including performance bonuses offered directly by a client.",
        "A supervisor remains responsible after delegating tasks. The supervisor must make reasonable efforts to establish, communicate, monitor, and enforce adequate procedures. Discovering a possible violation requires prompt investigation and steps that prevent further harm; merely sending a warning while allowing the conduct to continue is insufficient.",
      ],
      keyPoints: [
        "Preparations to compete later are different from soliciting clients or taking employer property now.",
        "Outside compensation can be cash, benefits, services, or other valuable consideration.",
        "Consent should be obtained from the employer before the arrangement begins.",
        "Supervision requires prevention and monitoring, not only escalation after a breach.",
      ],
    },
    {
      moduleId: "91.7",
      title: "Standard V: research quality, communication, and the evidence trail",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "A recommendation is defensible only when the research basis, communication, and retained record all tell the same story.",
      paragraphs: [
        "Diligence and Reasonable Basis requires enough investigation for the decision and scrutiny of third-party research, including assumptions, methods, data quality, objectivity, and timeliness. Communication then distinguishes fact from opinion and explains the process, significant risks, limitations, and material changes. Model output without assumptions and uncertainty can mislead even when the arithmetic is correct.",
        "Record Retention supports the analysis, recommendation, actions, and communications across channels. Research notes and client communications generally belong to the firm. A departing analyst cannot take those materials without permission; the analysis must be rebuilt from information the new firm may properly use. When no law or policy sets a period, a seven-year retention period is a recommended benchmark rather than a universal statutory rule.",
      ],
      keyPoints: [
        "The depth of diligence should rise with complexity, uncertainty, and consequence.",
        "A third-party rating is an input to evaluate, not a substitute for reasonable review.",
        "Communicate assumptions, material risks, liquidity or capacity constraints, and meaningful process changes.",
        "Preserve the evidence before, during, and after the recommendation—not only the final report.",
      ],
    },
    {
      moduleId: "91.8",
      title: "Standard VI: conflicts, transaction priority, and referral economics",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "Conflicts become manageable only when they are avoided where practical, disclosed clearly, and backed by procedures that prevent self-preference.",
      paragraphs: [
        "Avoid or Disclose Conflicts covers ownership, board service, market-making, compensation design, outside activities, and other interests that could impair judgment or duties. A useful disclosure is prominent, timely, plain, and specific enough for the recipient to judge the incentive. A vague boilerplate statement does not explain the conflict.",
        "Priority of Transactions gives client and employer activity a fair opportunity before accounts in which the professional is a beneficial owner. A family account that is itself a client account receives ordinary client treatment; it is not automatically pushed behind all other clients. Referral compensation—paid or received, monetary or nonmonetary—must be disclosed to the parties who need it to evaluate cost and possible bias.",
      ],
      keyPoints: [
        "Disclosure does not cure front-running or misuse of client information.",
        "Beneficial ownership can exist without the ability to sell immediately.",
        "Preclearance, blackout periods, duplicate confirmations, and holdings reports reinforce priority.",
        "Referral disclosure should identify the nature and value of the consideration where possible.",
      ],
    },
    {
      moduleId: "91.9",
      title: "Standard VII: program integrity and accurate use of professional status",
      outcomeIds: ["91.a", "91.b", "91.c"],
      lead:
        "Candidates and members may discuss the profession and program, but must protect confidential exam information and describe status without exaggeration.",
      paragraphs: [
        "Program Conduct protects exam security and the integrity of CFA Institute activities. Cheating, ignoring test-center rules, soliciting secure content, or revealing tested or omitted topics compromises the program. Criticism of policies or the exam is permitted when it does not reveal confidential content.",
        "References to CFA Institute, the designation, and candidacy must be factually accurate. Passing an exam level does not create a partial designation, and the charter cannot be used to imply guaranteed performance, superior returns, or a level of competence beyond what the designation establishes. Active use also depends on satisfying membership requirements.",
      ],
      keyPoints: [
        "Do not reveal specific or broad exam content, including what was absent.",
        "A candidate may state the level passed and current candidacy accurately.",
        "CFA is used as an adjective, not as a noun or a promised investment outcome.",
        "Firms should review biographies, advertisements, and digital profiles for correct references.",
      ],
    },
  ],
  comparisonTables: [
    {
      id: "91-module-map",
      title: "Nine distinct decision modules",
      caption:
        "Use the governing question to locate the duty; then select the control that addresses the actual risk.",
      columns: ["Module", "Governing question", "Violation signal", "First-line control"],
      rows: [
        ["91.1", "Which rule is strictest, and could an incentive distort judgment?", "Participation in a known breach or compromising benefit", "Compliance advice, dissociation, gift and travel approval"],
        ["91.2", "Is the message honest, the conduct trustworthy, and the professional capable?", "Misleading omission, uncredited work, deceit, or unsupported role", "Source records, communication review, training and supervision"],
        ["91.3", "Is information material and nonpublic, or is market activity designed to deceive?", "Trading on a protected fact or manufactured price or volume", "Information barriers, restricted lists, surveillance"],
        ["91.4", "Whose interest governs, and did eligible clients receive a fair opportunity?", "Manager benefit, favored dissemination, or arbitrary allocation", "Mandate checks, distribution lists, allocation policy"],
        ["91.5", "Does advice fit the client, is performance fair, and may information be shared?", "Stale client facts, cherry-picking, or unauthorized disclosure", "IPS updates, composite controls, access permissions"],
        ["91.6", "Does conduct respect the employer and are supervisors preventing violations?", "Diverted business, undisclosed pay, or ineffective oversight", "Written consent, compliance procedures, active monitoring"],
        ["91.7", "Is there a reasonable basis, clear communication, and a retained record?", "Unsupported research, hidden assumptions, or missing evidence", "Research checklist, model review, retention schedule"],
        ["91.8", "Could a personal incentive or trade disadvantage a client or hide a referral cost?", "Front-running, vague disclosure, or undisclosed compensation", "Preclearance, blackout periods, conflict disclosure"],
        ["91.9", "Does conduct protect program security and describe status accurately?", "Exam-content disclosure or exaggerated designation claim", "Candidate training and marketing review"],
      ],
    },
    {
      id: "91-disclosure-limits",
      title: "When disclosure helps—and when it does not",
      caption:
        "Disclosure informs affected parties about a permitted conflict; it does not legalize conduct that remains prohibited.",
      columns: ["Situation", "Is disclosure central?", "What remains required"],
      rows: [
        ["Personal ownership while publishing research", "Yes", "Prominent disclosure plus employer controls and independent analysis"],
        ["Client offers additional performance compensation", "Yes, with written employer consent", "Obtain consent before accepting the arrangement"],
        ["Referral fee", "Yes", "Tell relevant employers, clients, or prospects enough to evaluate cost and bias"],
        ["Possession of material nonpublic information", "No; a private disclosure does not cure it", "Do not act or cause others to act; contact compliance and seek public dissemination"],
        ["Personal trade before client orders", "No; later disclosure does not cure priority", "Delay the beneficial-owner trade until clients and employer have a fair opportunity"],
        ["Market manipulation", "No", "Do not engage in activity intended to mislead the market"],
      ],
    },
  ],
  workedDecisionCase: {
    title: "The private product failure: a multi-standard response",
    given: [
      "Nadia is an analyst covering Aster Robotics and beneficially owns Aster shares through a trust.",
      "Aster offers Nadia a weekend at a luxury resort before an investor presentation. Her employer has not approved the trip.",
      "During a private facility visit, Aster's chief engineer says that its only regulator has rejected the company's flagship device. No public announcement has been made.",
      "Nadia's portfolio manager asks her to downgrade Aster immediately and sell client positions before the market opens.",
      "Nadia has prior public research on Aster, but it does not include the rejection. Her firm's compliance manual provides a restricted-list process.",
    ],
    find: [
      "Which facts activate independence, market-integrity, conflict, diligence, communication, and priority duties",
      "What Nadia may and may not do before public dissemination",
      "What controls and records should be created",
      "What changes after the information becomes broadly public",
    ],
    plan: [
      "Separate the gift, information, beneficial ownership, requested trade, and research-basis facts.",
      "Apply the materiality/public-status test before considering any recommendation or trade.",
      "Choose actions that stop harm before considering disclosure or later research steps.",
      "Document the escalation and define the conditions for resuming coverage.",
    ],
    analysis: [
      "The luxury trip is an issuer benefit large enough to threaten independent judgment. Nadia should decline it and follow employer gift and travel procedures.",
      "Regulatory rejection of the flagship product would matter to a reasonable investor and has not been broadly disseminated. It is material nonpublic information.",
      "Nadia cannot sell personally, recommend a downgrade, or cause client sales while the information remains material and nonpublic. Acting for clients rather than herself does not remove the prohibition.",
      "Her trust interest is a conflict that requires employer disclosure and, if she later publishes after the information is public, clear disclosure to readers. That disclosure does not permit trading on the protected information.",
      "She should contact compliance immediately, request that Aster disseminate the information publicly, and support placing Aster and related instruments on the restricted list. The private statement and all escalation steps should be recorded securely.",
      "After broad dissemination, Nadia may update the research if she rebuilds the recommendation on a reasonable basis, distinguishes fact from judgment, explains the product and valuation risks, and gives eligible clients fair access before any beneficial-owner trade.",
    ],
    decision: [
      "Decline the trip, make no trade or recommendation, and do not relay the tip beyond personnel who need it for compliance or legal response.",
      "Notify compliance, seek public dissemination, restrict the security and related instruments, disclose the trust interest to the employer, and preserve the decision record.",
      "Resume research and client action only after public dissemination and a documented, independently supported reassessment.",
    ],
    sanityCheck: [
      "A private disclosure to clients would not make the information public.",
      "A good client outcome would not excuse trading on material nonpublic information.",
      "Disclosing the trust interest addresses a conflict but does not cure the information violation.",
      "Declining the trip removes an independence threat but does not resolve the trading restriction.",
      "Once public, the rejection becomes a research input; it does not automatically dictate a rating without valuation and risk analysis.",
    ],
  },
  misconceptions: [
    {
      claim: "The law of the country where the analyst is standing always controls.",
      correction:
        "The professional must identify every applicable regime and follow the strictest applicable requirement when they differ.",
      diagnostic:
        "List residence, business location, client jurisdiction, market rules, professional standards, and binding firm policy before selecting the rule.",
    },
    {
      claim: "Disclosure fixes any conflict or ethical problem.",
      correction:
        "Disclosure can manage a permitted conflict, but it cannot cure conduct such as trading on protected information, front-running, or manipulation.",
      diagnostic:
        "Ask whether the underlying action is allowed once informed consent exists. If the rule forbids the action itself, disclosure is insufficient.",
    },
    {
      claim: "Any nonpublic detail makes the mosaic theory unavailable.",
      correction:
        "A documented conclusion may combine public information with nonmaterial nonpublic observations. The prohibition attaches when information is both material and nonpublic.",
      diagnostic:
        "Test each nonpublic fact for investor importance and likely price impact before using it.",
    },
    {
      claim: "Fair dealing requires every client to receive and act on a recommendation at the same instant.",
      correction:
        "The duty requires an objective and fair dissemination and allocation process. Different mandates and suitability can produce different actions.",
      diagnostic:
        "Look for favoritism, advance notice, arbitrary allocation, or an undisclosed delay rather than demanding literal simultaneity.",
    },
    {
      claim: "A supervisor complies by reporting a violation and telling the employee to stop.",
      correction:
        "The supervisor must also investigate and take reasonable steps that prevent further harm while the matter is resolved.",
      diagnostic:
        "Ask whether risky access, trading, publication, or client contact continues unchanged after the warning.",
    },
    {
      claim: "Candidates may discuss which exam topics appeared as long as they do not quote a question.",
      correction:
        "Revealing broad or specific tested content—or content omitted—can compromise program integrity even without quoting exact wording.",
      diagnostic:
        "Separate opinions about the exam process from information that reveals confidential exam coverage or construction.",
    },
  ],
  assessments: [
    {
      id: "91-assessment-1",
      objectiveIds: ["91.a", "91.c"],
      skill: "application",
      prompt:
        "Local law allows trading after confidential information is shared with a large group of institutional investors, even if it has not reached the broader market. An analyst receives clearly price-sensitive information in that meeting. The professional standards treat it as nonpublic. What is the best action?",
      options: [
        {
          id: "A",
          text: "Trade because the law where the meeting occurred permits transactions after institutional disclosure.",
          feedback:
            "This applies the less demanding requirement and ignores the stricter professional restriction on material nonpublic information.",
        },
        {
          id: "B",
          text: "Refrain from acting, contact compliance, and encourage broad public dissemination before reconsidering a trade.",
          feedback:
            "Correct. The analyst follows the stricter applicable requirement and takes steps to protect market integrity.",
        },
        {
          id: "C",
          text: "Trade only for client accounts because the information may improve client outcomes without personal benefit.",
          feedback:
            "The prohibition covers acting or causing others to act; using the information for clients remains prohibited.",
        },
        {
          id: "D",
          text: "Publish a downgrade without trading because a recommendation is outside the restriction on securities transactions.",
          feedback:
            "Causing others to act through a recommendation is also prohibited while the information is material and nonpublic.",
        },
      ],
      correctOptionId: "B",
      solution: [
        "The information is material because it is clearly price-sensitive.",
        "Institutional disclosure is not broad marketplace dissemination under the stated professional rule.",
        "The stricter applicable rule governs, so neither personal trades, client trades, nor recommendations may be based on the information.",
        "Compliance escalation and an effort to obtain public dissemination address the risk without misusing the information.",
      ],
    },
    {
      id: "91-assessment-2",
      objectiveIds: ["91.a", "91.b", "91.c"],
      skill: "diagnosis",
      prompt:
        "An analyst combines public filings, commercially available satellite images, and a supplier employee's private comment that one weekly shipment was slightly delayed. The comment is not important by itself. The documented combination supports a negative forecast. May the analyst issue the forecast and trade?",
      options: [
        {
          id: "A",
          text: "No, because using any nonpublic observation automatically makes the completed forecast material nonpublic information.",
          feedback:
            "This is too broad. A nonmaterial nonpublic observation may contribute to a legitimate mosaic when the conclusion comes from analysis.",
        },
        {
          id: "B",
          text: "No, because commercially available alternative data cannot support a recommendation until the issuer confirms it publicly.",
          feedback:
            "Commercially available data can be analyzed without issuer confirmation, subject to lawful acquisition and a reasonable research basis.",
        },
        {
          id: "C",
          text: "Yes, if the private comment is genuinely nonmaterial and the analyst documents the independent mosaic and research basis.",
          feedback:
            "Correct. Public evidence plus a nonmaterial nonpublic fact can support action when the analytical process, data rights, and basis are sound.",
        },
        {
          id: "D",
          text: "Yes, but only after the analyst discloses the supplier employee's identity and exact comment to every client.",
          feedback:
            "Client disclosure is not what makes the mosaic permissible and could create separate confidentiality or sourcing concerns.",
        },
      ],
      correctOptionId: "C",
      solution: [
        "The public filings and commercially available images are public research inputs.",
        "The private comment is stipulated to be nonmaterial by itself.",
        "A documented analytical combination can therefore qualify as mosaic research rather than use of material nonpublic information.",
        "The analyst still needs lawful data acquisition, diligence, source records, and clear communication of forecast assumptions.",
      ],
    },
    {
      id: "91-assessment-3",
      objectiveIds: ["91.a", "91.b", "91.c"],
      skill: "transfer",
      prompt:
        "A portfolio manager finishes a buy recommendation, purchases the security for a spouse's account in which the manager is a beneficial owner, and sends client orders the next morning. The report prominently discloses the family holding. Which conclusion is best?",
      options: [
        {
          id: "A",
          text: "The manager violated transaction priority because disclosure does not give the beneficial-owner account precedence over clients.",
          feedback:
            "Correct. Clients and the employer need a fair opportunity before the manager's beneficial-owner account trades on the recommendation.",
        },
        {
          id: "B",
          text: "The manager complied because a spouse's account is always treated as an ordinary client account for allocation purposes.",
          feedback:
            "A family account can be an ordinary client account, but the facts specify beneficial ownership and a personal trade ahead of client orders.",
        },
        {
          id: "C",
          text: "The manager complied because prominent ownership disclosure removes the conflict before clients read the recommendation.",
          feedback:
            "Disclosure informs readers about bias but does not cure trading ahead of clients.",
        },
        {
          id: "D",
          text: "The manager violated only fair dealing because transaction priority applies solely to the manager's directly titled accounts.",
          feedback:
            "Transaction priority reaches accounts in which the manager is a beneficial owner, including the spouse's account described here.",
        },
      ],
      correctOptionId: "A",
      solution: [
        "The completed recommendation creates an opportunity clients have not yet received.",
        "The spouse's account is expressly one in which the manager has beneficial ownership.",
        "Trading that account first disadvantages clients and violates transaction priority.",
        "Prominent conflict disclosure remains necessary but does not reverse the sequence or cure the priority breach.",
      ],
    },
  ],
};

const sourcePages: Record<string, number> = {
  "28.1": 25,
  "28.2": 29,
  "28.3": 39,
  "28.4": 42,
  "28.5": 49,
  "91.1": 167,
  "91.2": 171,
  "91.3": 173,
  "91.4": 175,
  "91.5": 177,
  "91.6": 180,
  "91.7": 183,
  "91.8": 187,
  "91.9": 189,
};

function toGoldLesson(detail: DecisionLessonDetail): GoldLesson {
  const frameworkSections = detail.decisionFrameworks.map((framework) => ({
    heading: framework.title,
    body: [
      framework.purpose,
      ...framework.steps.map((step, index) => `${index + 1}. ${step}`),
    ],
  }));
  const lessonSections = detail.explanatorySections.map((section) => ({
    heading: `${section.moduleId} · ${section.title}`,
    body: [
      section.lead,
      ...section.paragraphs,
      ...section.keyPoints.map((point) => `Key point: ${point}`),
      ...(section.miniExample
        ? [
            `${section.miniExample.title}: ${section.miniExample.setup}`,
            ...section.miniExample.walkthrough,
            `Takeaway: ${section.miniExample.takeaway}`,
          ]
        : []),
    ],
  }));
  const tableSections = detail.comparisonTables.map((table) => ({
    heading: table.title,
    body: [
      table.caption,
      ...table.rows.map((row) =>
        row
          .map((cell, index) => `${table.columns[index]}: ${cell}`)
          .join(" | "),
      ),
    ],
  }));

  return {
    readingId: detail.readingId,
    title: detail.title,
    sourceRefs: detail.sourceRefs.map((sourceRef) => {
      const primaryModuleId = sourceRef.moduleIds[0];
      return {
        book: sourceRef.book,
        pdfPage: sourcePages[primaryModuleId],
        heading: `${sourceRef.locator} — ${sourceRef.coverage.join(", ")}`,
      };
    }),
    objectives: detail.objectives.map((objective) => ({
      id: objective.id,
      description: objective.text,
    })),
    sections: [...frameworkSections, ...lessonSections, ...tableSections],
    formulas: detail.decisionFrameworks.flatMap((framework) =>
      framework.formulas.map((formula, index) => ({
        id: `${framework.id}-${index + 1}`,
        title: formula.name,
        latex: formula.latex,
        variables: formula.variables.map((variable) => ({
          symbol: variable.symbol,
          meaning: variable.meaning,
          unit: variable.unit ?? "not applicable",
        })),
        assumptions: formula.conditions,
        domain:
          formula.conditions.join(" ") ||
          "Apply within the decision context and factual conditions described in the lesson.",
        interpretation: formula.interpretation,
      })),
    ),
    workedExamples: [
      {
        id: `${detail.readingId}-integrated-case`,
        title: detail.workedDecisionCase.title,
        given: detail.workedDecisionCase.given,
        find: detail.workedDecisionCase.find.join(" "),
        plan: detail.workedDecisionCase.plan.join(" "),
        calculate: detail.workedDecisionCase.analysis.map((result, index) => ({
          description: `Analysis step ${index + 1}`,
          latex: "",
          result,
        })),
        interpret: detail.workedDecisionCase.decision.join(" "),
        sanityCheck: detail.workedDecisionCase.sanityCheck.join(" "),
      },
    ],
    misconceptions: detail.misconceptions.map(({ claim, correction }) => ({
      claim,
      correction,
    })),
    assessments: detail.assessments.map((assessment) => ({
      id: assessment.id,
      objectiveId: assessment.objectiveIds.join(", "),
      prompt: assessment.prompt,
      options: assessment.options,
      correctOptionId: assessment.correctOptionId,
      solution: assessment.solution.join(" "),
    })),
  };
}

/**
 * Rich authoring records retain decision frameworks and comparison-table data.
 * The compatible export below converts the same content to the shared GoldLesson
 * shape used by the quantitative exemplars.
 */
export const goldDecisionLessonDetails: DecisionLessonDetail[] = [reading28, reading91];

export const goldDecisionLessons: GoldLesson[] =
  goldDecisionLessonDetails.map(toGoldLesson);

export const goldDecisionLessonsByReading: ReadonlyMap<number, GoldLesson> =
  new Map(goldDecisionLessons.map((lesson) => [lesson.readingId, lesson]));
