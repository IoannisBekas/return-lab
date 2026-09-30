import json
import glob

# Read existing math blocks directly or from backup
MATH_ASSETS = {
    "r1-q3": "3ec6268f12c7e133d611.png",
    "r1-q4": "1c6c9f7e119b585d1830.png",
    "r1-q6": "7960c885d7c1021a5ccf.png",
    "r1-q7": "6245af464970b5ba8a09.png",
    "r2-q4": "eae5d5799b43cb89de86.png",
    "r5-q1": "d679af8f7aa745329d0d.png",
    "r30-q6": "6159ea56ae62f3988634.png",
    "r35-q12": "b5ffc67af0ec8ba5115f.png",
    "r40-q2": "e630745521e6d69ab68b.png",
    "r40-q3": "6b743f1561694fe049aa.png",
    "r40-q4": "bda50c817dd110115564.png",
    "r46-q9": "b0aa6445d5f8b35cac38.png",
    "r46-q10": "c0d266656dd457a5c5ae.png",
    "r53-q1": "1faede774541a1a6ade5.png",
    "r55-q1": "1551933004a4d2ab1dfc.png",
    "r55-q4": "fa183ec49859908dbea5.png",
    "r55-q5": "6393c0bf4f3bae25e61e.png",
    "r57-q1": "1ee599d4c5c36e7a03b9.png",
    "r58-q2": "c2785f32c5de517653d6.png",
    "r83-q8": "ed991ff58fc0141c94c7.png",
    "r83-q9": "6988ab79d3f289854d92.png",
}

EXPLANATION_TEXTS = {
    "r1-q2": "A real interest rate is a nominal interest rate adjusted to remove the effect of expected inflation (Nominal Rate − Inflation Premium = Real Rate). In contrast, the real risk-free rate represents the single-period return on a completely default-free security in the absence of inflation, and a general risk-free rate includes an inflation premium.",
    "r1-q3": "The harmonic mean is calculated as the number of observations divided by the sum of their reciprocals: H = 3 / (1/3 + 1/4 + 1/5) = 3 / (20/60 + 15/60 + 12/60) = 3 / (47/60) = 180 / 47 ≈ 3.8298, or 3.83.",
    "r1-q4": "Because investment returns compound over multiple sequential periods, the geometric mean return is the appropriate measure of compound annual growth rate. The arithmetic mean overstates terminal compounding performance, while the harmonic mean is suited for dollar-cost averaging rather than multi-year investment growth.",
    "r1-q6": "The time-weighted rate of return measures compound growth independent of cash flow timing. For Period 1: HPR_1 = (P1 + D1 − P0) / P0 = (50 + 1 − 40) / 40 = 27.50%. For Period 2: HPR_2 = (P2 + D2 − P1) / P1 = (60 + 1 − 50) / 50 = 22.00%. The annualized time-weighted return is [(1 + 0.2750)(1 + 0.2200)]^(1/2) − 1 = (1.5555)^0.5 − 1 ≈ 24.72%, or 24.7%.",
    "r1-q7": "Annualizing a holding period return on a 365-day basis using compound annualization gives: Annualized Return = (1 + HPR)^(365 / days) − 1 = (1 − 0.03)^(365 / 120) − 1 = (0.97)^3.04167 − 1 ≈ 0.91147 − 1 = −8.85%, which is closest to −9.0%.",
    "r1-q8": "The continuously compounded rate of return is the natural logarithm of the ending price divided by the beginning price: r_cc = ln(S1 / S0) = ln(23 / 20) = ln(1.15) ≈ 0.13976, or 13.98%.",
    "r2-q1": "A preferred stock paying a constant indefinite dividend is valued as a perpetuity: PV = Dividend / Required Rate of Return = $9.00 / 0.11 = $81.82.",
    "r2-q4": "The compound annual growth rate is found by solving PV × (1 + r)^n = FV: r = (FV / PV)^(1/n) − 1 = (€7M / €5M)^(1/3) − 1 = (1.40)^(1/3) − 1 ≈ 1.1187 − 1 = 11.87%, which rounds to 12%.",
    "r5-q1": "From the relationship Cov(A,B) = Corr(A,B) × σ_A × σ_B, we can solve for Stock A's standard deviation: σ_A = Cov(A,B) / [Corr(A,B) × σ_B] = 0.0043 / [0.50 × 0.26] = 0.0043 / 0.13 = 0.033077 (3.31%). The variance is σ_A^2 = (0.033077)^2 ≈ 0.001094, or 0.0011.",
    "r6-q1": "A lognormal distribution is bounded below by zero, meaning that a lognormally distributed variable cannot take negative values (P(X < 0) = 0). It is skewed to the right (positively skewed), so its mean exceeds its median and mode, making it an appropriate model for asset prices.",
    "r7-q2": "By standard statistical convention, a sample size of n ≥ 30 is generally considered sufficiently large for the central limit theorem to ensure that the distribution of the sample mean is approximately normal, regardless of the underlying population's distribution.",
    "r8-q2": "The power of a statistical test is defined as 1 − P(Type II error) = 1 − β. Given β = 0.15, the power of the test is 1 − 0.15 = 0.850. Power represents the probability of correctly rejecting a false null hypothesis.",
    "r8-q4": "An F-test (using the F-distributed ratio of sample variances, s1^2 / s2^2) is used to test hypotheses regarding the equality of variances of two independent, normally distributed populations. The t-test is used for population means, and the chi-square test is used for a single population variance.",
    "r8-q5": "A chi-square (χ²) test statistic, calculated as (n − 1)s^2 / σ_0^2 with n − 1 degrees of freedom, is used to test hypotheses concerning the variance of a single normally distributed population.",
    "r18-q3": "The inverse of the exchange rate USD/GBP gives the quote in GBP/USD: GBP/USD = 1 / (USD/GBP) = 1 / 1.3110 ≈ 0.762776, or 0.7628.",
    "r19-q3": "Forward points are quoted in units of the last decimal place (1 point = 0.0001 for a four-decimal rate). A quote of −42.5 points equals −0.00425. Thus, the forward rate is Spot + Forward Points = 1.3050 + (−0.00425) = 1.30075, or 1.3008.",
    "r24-q3": "The net present value discounts each cash flow at the 10% cost of capital: NPV = −$5,000 + $3,000 / (1.10)^1 + $2,000 / (1.10)^2 + $2,000 / (1.10)^3 = −$5,000 + $2,727.27 + $1,652.89 + $1,502.63 = $5,882.79 − $5,000 = +$882.79, or approximately +$883.",
    "r30-q6": "Under the indirect method, Cash Flow from Operations begins with Net Income ($78,000), adds back non-cash Depreciation ($12,000), deducts the unrealized gain on trading securities (−$15,000), subtracts the increase in Accounts Receivable ($121,000 − $69,000 = −$52,000), and adds the increase in Accounts Payable ($72,000 − $43,000 = +$29,000): CFO = $78,000 + $12,000 − $15,000 − $52,000 + $29,000 = $52,000.",
    "r30-q10": "Under U.S. GAAP, interest paid is strictly classified as an operating cash flow (CFO), because it affects net income. In contrast, issuing bonds and paying dividends to shareholders are classified as financing activities (CFF).",
    "r30-q12": "Cash received from issuing debt securities (such as bonds or notes payable) represents capital obtained from creditors and is classified as a cash flow from financing activities (CFF).",
    "r30-q13": "Purchases and sales of long-term productive assets, property, plant, and equipment (PPE), including land, are classified as cash flows from investing activities (CFI).",
    "r31-q3": "The reinvestment ratio is defined as Cash Flow from Operations (CFO) divided by cash paid for long-term productive assets (capital expenditures). It measures the extent to which operating cash flows can sustain capital investment and asset acquisition without needing external debt or equity financing.",
    "r34-q7": "For a lessor, lease receipts represent operational income from leasing assets to customers and are classified under operating cash flows (CFO).",
    "r35-q6": "Deferred tax assets (DTAs) and deferred tax liabilities (DTLs) are measured using the enacted tax rate expected to apply when the temporary difference reverses. A higher tax rate increases the future tax deduction value represented by a DTA, increasing its carrying balance on the balance sheet.",
    "r35-q12": "Effective tax rate is Total Tax Expense divided by Total Pretax Income: German tax = €100M × 30% = €30M. Italian tax = €100M × 20% = €20M. Total tax = €30M + €20M = €50M. Total pretax income = €100M + €100M = €200M. Effective tax rate = €50M / €200M = 25.0%.",
    "r37-q9": "The cash conversion cycle equals Days of Sales Outstanding (DSO) + Days of Inventory on Hand (DOH) − Number of Days of Payables: DSO = 365 / 10 = 36.5 days; DOH = 365 / 5 = 73.0 days; Days of Payables = 365 / 9 = 40.56 days. Cash Conversion Cycle = 36.5 + 73.0 − 40.56 = 68.94 ≈ 69 days.",
    "r37-q11": "Operating profit (EBIT) = Sales − COGS − Operating Expenses = $1,000 − $400 − $300 = $300. The interest coverage ratio is EBIT / Interest Expense = $300 / $100 = 3.0 times.",
    "r39-q8": "The primary market is where issuers sell newly created securities to investors for the first time (such as in an IPO or seasoned offering), raising capital for the issuer. The secondary market involves trading existing securities between investors.",
    "r40-q2": "In a price-weighted index, the index level is proportional to the sum of share prices. Initial index value = (22 + 40 + 34) / 3 = 96 / 3 = 32. Ending index value = (28 + 50 + 30) / 3 = 108 / 3 = 36. The return is (36 − 32) / 32 = 4 / 32 = 12.5%.",
    "r40-q3": "An equal-weighted index calculates the arithmetic average return of the component assets: Stock 1 Return = (28 − 22) / 22 = 6 / 22 ≈ +27.27%; Stock 2 Return = (50 − 40) / 40 = 10 / 40 = +25.00%; Stock 3 Return = (30 − 34) / 34 = −4 / 34 ≈ −11.76%. Equal-weighted index return = (27.27% + 25.00% − 11.76%) / 3 = 40.51% / 3 ≈ 13.50%.",
    "r40-q4": "The return on a value-weighted index equals the change in total market capitalization divided by beginning total market cap. Initial Market Cap = 22(1,500) + 40(10,000) + 34(3,000) = $33,000 + $400,000 + $102,000 = $535,000. Ending Market Cap = 28(1,500) + 50(10,000) + 30(3,000) = $42,000 + $500,000 + $90,000 = $632,000. Return = ($632,000 − $535,000) / $535,000 = $97,000 / $535,000 ≈ 18.13%, which is closest to 18.0%.",
    "r46-q6": "Perpetual preferred stock is valued by discounting its constant dividend stream: Value = Dividend / Required Return = $7.00 / 0.0775 = $90.32.",
    "r46-q7": "The intrinsic value for a one-year holding period is the present value of the expected dividend plus ending price: V_0 = (D_1 + P_1) / (1 + r) = ($2.00 + $40.00) / 1.15 = $42.00 / 1.15 ≈ $36.52.",
    "r46-q8": "Using the Gordon constant growth model, first determine next year's dividend D_1 = D_0(1 + g) = $1.00 × 1.05 = $1.05. Then: V_0 = D_1 / (r − g) = $1.05 / (0.10 − 0.05) = $1.05 / 0.05 = $21.00.",
    "r46-q9": "First, find the dividend in Year 3: D_3 = D_2(1 + g) = $1.56 × 1.05 = $1.638. Next, calculate terminal stock price at Year 2: P_2 = D_3 / (k_e − g) = $1.638 / (0.11 − 0.05) = $1.638 / 0.06 = $27.30. Finally, discount cash flows back to t = 0: V_0 = $1.25 / (1.11)^1 + ($1.56 + $27.30) / (1.11)^2 = $1.1261 + $28.86 / 1.2321 = $1.1261 + $23.4234 = $24.55.",
    "r46-q10": "Step 1: Forecast non-constant dividends: D_1 = $1.00(1.25) = $1.25; D_2 = $1.25(1.25) = $1.5625. Step 2: Forecast the first constant growth dividend: D_3 = $1.5625(1.06) = $1.65625. Step 3: Compute terminal value at t = 2: P_2 = D_3 / (r − g) = $1.65625 / (0.10 − 0.06) = $41.40625. Step 4: Discount all cash flows to present: V_0 = $1.25 / 1.10 + ($1.5625 + $41.40625) / (1.10)^2 = $1.1364 + $42.96875 / 1.21 = $1.1364 + $35.5114 = $36.65.",
    "r46-q13": "The justified forward P/E ratio based on fundamentals is P_0 / E_1 = (Payout Ratio) / (r − g) = 0.60 / (0.15 − 0.07) = 0.60 / 0.08 = 7.5×.",
    "r50-q4": "The haircut is the percentage discount applied to the market value of the collateral: Haircut = 1 − (1 / Initial Margin) = 1 − (1 / 1.01) = 1 − 0.990099 = 0.009901, or 0.99%.",
    "r52-q1": "The bond's price is the present value of its 20 annual coupon payments of 10 plus the par value of 100 discounted at the 15% yield: Price = Σ [10 / (1.15)^t] + 100 / (1.15)^20 = 10 × [(1 − (1.15)^−20) / 0.15] + 100 / (1.15)^20 = 10 × 6.25933 + 6.11003 = 62.5933 + 6.1100 = 68.703.",
    "r52-q2": "With semiannual compounding over 5 years (n = 10 periods), the coupon is £50 per period (£1,000 × 5%) and the semiannual yield is 7.5% (15% / 2). Value = Σ [50 / (1.075)^t] + 1,000 / (1.075)^10 = 50 × [(1 − (1.075)^−10) / 0.075] + 1,000 / (1.075)^10 = 50 × 6.86408 + 485.194 = £343.204 + £485.194 = £828.40.",
    "r53-q1": "For a 15-year zero coupon bond with semiannual compounding, there are n = 30 semiannual periods. Solving $331.40 = $1,000 / (1 + r/2)^30 gives: (1 + r/2)^30 = 1,000 / 331.40 = 3.01750. Taking the 30th root: 1 + r/2 = (3.01750)^(1/30) = 1.03750, so r/2 = 3.750% per half-year. Annualized on a semiannual bond basis: YTM = 3.750% × 2 = 7.500%.",
    "r53-q2": "Yield to call (YTC) is calculated using the cash flows to the call date: 4 semiannual periods (2 years), semiannual coupon payment of 3.5625% (7.125% / 2), call price of 101, and current price of 102.347. Solving 102.347 = Σ [3.5625 / (1 + y)^t] + 101 / (1 + y)^4 yields a semiannual rate of y ≈ 3.167%. Annualized on a bond equivalent basis, YTC = 3.167% × 2 = 6.334%, or closest to 6.3%.",
    "r54-q2": "A bond equivalent yield (BEY) is an annualized add-on yield based on a 365-day year (or 366 days in a leap year). Money market discount yields and 360-day add-on yields understate the true annual yield compared to a bond equivalent basis.",
    "r55-q1": "Discount each annual cash flow ($4,000 coupon in years 1 and 2, and $104,000 coupon plus principal in year 3) by its respective zero-coupon spot rate: Price = $4,000 / (1.032)^1 + $4,000 / (1.034)^2 + $104,000 / (1.035)^3 = $3,875.97 + $3,741.24 + $93,802.07 = $101,419.28, which rounds to $101,420.",
    "r55-q4": "Under the no-arbitrage condition, investing for 4 years at the 4-year spot rate equals investing for 3 years at the 3-year spot rate followed by 1 year at the forward rate f(3,1): (1 + s_4)^4 = (1 + s_3)^3 × (1 + f(3,1)). Rearranging: 1 + f(3,1) = (1.0945)^4 / (1.0985)^3 = 1.43521 / 1.32575 = 1.082579, so f(3,1) = 8.258%.",
    "r55-q5": "The cash flows are $100 at Year 1, $100 at Year 2, $100 at Year 3, and $1,100 at Year 4. Discounting each cash flow using the path of forward rates: Year 1 PV = 100 / 1.055 = $94.79; Year 2 PV = 100 / (1.055 × 1.0763) = $88.07; Year 3 PV = 100 / (1.055 × 1.0763 × 1.1218) = $78.50; Year 4 PV = 1,100 / (1.055 × 1.0763 × 1.1218 × 1.155) = $747.67. Total Value = $94.79 + $88.07 + $78.50 + $747.67 = $1,009.03, which is closest to $1,009.",
    "r57-q1": "Approximate modified duration is calculated as (V_− − V_+) / (2 × V_0 × Δy). Because the bond trades at par (V_0 = 100), when yield decreases by 25 bps to 13.75%, the bond price rises to V_− = 100.979. When yield increases by 25 bps to 14.25%, the price falls to V_+ = 99.035. Approximate modified duration = (100.979 − 99.035) / (2 × 100.0 × 0.0025) = 1.944 / 0.500 = 3.888.",
    "r57-q3": "The linear duration estimate for percentage price change is: %ΔP ≈ −Modified Duration × Δy. With Δy = −110 bps = −0.0110: %ΔP ≈ −7.87 × (−0.0110) = +0.08657, or +8.657%. A decrease in yield leads to an increase in bond price.",
    "r58-q2": "Approximate convexity is calculated using the formula: Convexity = (V_− + V_+ − 2V_0) / [(Δy)^2 × V_0]. Given V_0 = 104.4518, V_− = 104.9108, V_+ = 103.9954, and Δy = 0.0010: Convexity = (104.9108 + 103.9954 − 2 × 104.4518) / [(0.001)^2 × 104.4518] = (208.9062 − 208.9036) / (0.000001 × 104.4518) = 0.0026 / 0.0001044518 ≈ 24.89.",
    "r66-q1": "A derivative is a financial instrument whose value and contractual payoff are derived from the performance of an underlying asset, index, interest rate, or other reference benchmark. Derivatives do not necessarily increase risk (they are widely used to hedge risk) and typically have defined expiration dates.",
    "r67-q8": "A forward commitment is a binding contractual agreement between counterparties to engage in a transaction at a future date on terms established today. Interest rate swaps, forward contracts, and futures contracts are forward commitments. Options and credit default swaps are contingent claims.",
    "r83-q8": "First calculate the standard deviation for each stock: σ_A = √(0.09) = 0.30; σ_B = √(0.04) = 0.20. The correlation coefficient is Corr(A,B) = Cov(A,B) / (σ_A × σ_B) = 0.006 / (0.30 × 0.20) = 0.006 / 0.060 = 0.10.",
    "r83-q9": "The portfolio variance for a two-asset portfolio is: σ_p^2 = w_A^2 × σ_A^2 + w_B^2 × σ_B^2 + 2 × w_A × w_B × σ_A × σ_B × ρ = (0.25)^2(0.15)^2 + (0.75)^2(0.10)^2 + 2(0.25)(0.75)(0.15)(0.10)(−0.75) = 0.00140625 + 0.00562500 − 0.00421875 = 0.00281250. Taking the square root: σ_p = √(0.00281250) ≈ 0.05303, or 5.3%.",
    "r84-q9": "Using the Capital Asset Pricing Model (CAPM): E(R_i) = R_f + β_i × [E(R_m) − R_f] = 6% + 1.2 × (12% − 6%) = 6% + 1.2 × (6%) = 6% + 7.2% = 13.2%.",
    "r84-q10": "Using the Capital Asset Pricing Model (CAPM): E(R_i) = R_f + β_i × [E(R_m) − R_f] = 7% + 0.7 × (14% − 7%) = 7% + 0.7 × (7%) = 7% + 4.9% = 11.9%.",
    "r86-q5": "Return objectives (such as targeting an 8% minimum total return) and risk tolerance form the investment objectives section of an Investment Policy Statement (IPS). Portfolio constraints encompass the five RRTTLL factors: Liquidity, Time horizon, Tax concerns, Legal/regulatory factors, and Unique circumstances."
}

updated_files = 0
updated_questions = 0

for file_path in sorted(glob.glob('public/content/readings/*.json')):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    for qset in data.get('quizSets', []):
        for q in qset.get('questions', []):
            qid = q.get('id')
            if qid in EXPLANATION_TEXTS:
                q['explanation'] = EXPLANATION_TEXTS[qid]
                
                # Check if this question has a math block with sourceAsset
                existing_math = [b for b in q.get('solutionBlocks', []) if b.get('type') == 'math']
                if existing_math:
                    mb = existing_math[0]
                    q['solutionBlocks'] = [
                        {"type": "paragraph", "text": EXPLANATION_TEXTS[qid]},
                        mb
                    ]
                else:
                    # For non-math questions, provide a clean paragraph solutionBlock
                    q['solutionBlocks'] = [
                        {"type": "paragraph", "text": EXPLANATION_TEXTS[qid]}
                    ]
                
                modified = True
                updated_questions += 1
                
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        updated_files += 1

print(f"Polished {updated_questions} questions across {updated_files} reading files.")
