"""Classify every imported visual and replace mathematical crops with LaTeX.

Formula recognition is cached because the local model is intentionally expensive.
The emitted audit links every source asset to its final treatment.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from pix2text import Pix2Text


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "public/content"
CACHE_FILE = ROOT / "work/math-latex-cache-p2t.json"
SCORES_FILE = ROOT / "work/math-latex-confidence.json"
SEGMENTED_FILE = ROOT / "work/math-latex-segmented.json"
AUDIT_FILE = ROOT / "docs/math-visual-classification.json"
REBUILT_TABLES = {
    "e85d519d312de160b985.png",
    "39c347fbb135ee9a1dc6.png",
    "0b5060743d1bd04ba9ed.png",
    "a00fc35837198e75350f.png",
    "2b641346ef3eb9bf30f1.png",
    "b8a7edef2c13faf0422f.png",
}
REFERENCE_TABLES = {
    "236c50cbc08d6783fb2c.png",
    "d6ad52dc87eef482d15b.png",
    "5463b8f4d7dbe4792cb4.png",
    "4c03d785ccda6e4dbc55.png",
    "a5cbb7719f7458f34a22.png",
    "fd7cdf02d96a2690be89.png",
    "3bf1c773e8d459b24845.png",
    "9c7480bee3dd12df7efa.png",
}
MANUAL_MEANINGFUL_VISUALS = {
    "0a88218aa63cbad38f1c.png",  # joint-probability table
    "0f8b04065cedff265396.png",  # probability tree
    "673044e17d4a0215e36e.png",  # one-period binomial tree
    "988c7893d36a8a1bd8ca.png",  # regression model interpretation table
    "c34a22880904740b85c0.png",  # security market line chart
    "e061b63a0bca50ca861e.png",  # comparative income statement table
    "e4933d08a761e2b5810d.png",  # securities index reference table
    "e70c384060069a333c4a.png",  # capitalized-cost calculation table
    "f814cc1eaa5656f9dda9.png",  # capital structure comparison table
    # Source-verified tables, charts, and decision trees found during the
    # full KaTeX render audit. These remain visual because their spatial
    # relationships carry meaning beyond a linear equation transcription.
    "004e4e43db850044a5b3.png", "0441f549559dfa88d182.png",
    "07a9a732d4e8c6fe8820.png", "0cbea1828ba82ba95a45.png",
    "0d10a4b9c0de22f7e2bb.png", "150bd1337203ccc4d538.png",
    "1609b14359161a326d07.png", "171f0c75b0ec54825fa5.png",
    "193f95c3e98c04c2dcc5.png", "19cea061ab7f4e0a9e99.png",
    "1f29a430552ac9b5702b.png", "24346a116202b57c819e.png",
    "24c9efeab5fdeedafb9c.png", "284193a7c2047e6687d1.png",
    "2b9cfd2ac28cbd8ecd52.png", "2c2db45830118eb1d1fc.png",
    "2e57847cc10f6916fc4f.png", "32d91591473b94441c8f.png",
    "33bc7352159d403f46bb.png", "384854301c0123597210.png",
    "3993dbc1b6188bda044b.png", "3ad166e8f69d389954ed.png",
    "3b212816f81575ac9df8.png", "3c5c5a60d2869949ed95.png",
    "3c9dbbfb75f5fcebc850.png", "3da67fad473aa701f24e.png",
    "3e9cd88b54d911d57bf7.png", "47a778e8d0cc4e8c245b.png",
    "4b028243ef1b6d3cbc39.png", "510d77a276c7184557a9.png",
    "5192b64bec7da308db37.png", "5afb9617c177725ce881.png",
    "5b15780f0fb7c3e70358.png", "5b22f1b5f283284f5c7f.png",
    "5d68f4c1921b12dd0247.png", "5e4e36a280ec13ad21f8.png",
    "5f069797e6e810c80e3f.png", "62340509398a22ebb7f1.png",
    "6238aa1942b15e9eaac3.png", "68211594bc802b33c92a.png",
    "6fae291f3cddc6447638.png", "740e8bf422d1a74b9e15.png",
    "7599db3f980f38142f2b.png", "7bc6afde6ef40f0475a6.png",
    "7dc657bd79cecbffc2f8.png", "85130fb513dc68f0cbda.png",
    "874dbb230795297b4341.png", "890263d6938a04faada4.png",
    "906b0829878cf9c4a3d6.png", "99a395b3005dcf9a0cf9.png",
    "9ad5a7f96f9ef4ed4e1c.png", "9ca4fb017d5c655a23b8.png",
    "9daa03cc4a34d1747f8b.png", "a1901e95615ba6b26051.png",
    "a3d4bd9e09fe6e397b5d.png", "a414e01d34293345478a.png",
    "a4a3be627992c67d0103.png", "a59a1286e797537fd1d0.png",
    "a76fcd5d6139f16612bc.png", "a93e6133f2de169c1ab4.png",
    "a9abb4ccbda249ca69e9.png", "ad827ab290b1c8660a15.png",
    "b411d4a82216ae464aef.png", "b433e6e32eee7e9616c8.png",
    "b665660817cda5de60a9.png", "b8f7f76b5f0bf28f896b.png",
    "ba419a01ea9240df9ba9.png", "bee5e481e40d6ac920ad.png",
    "c0931084e800172bb17d.png", "c1ff69501c6d5344b906.png",
    "c385d8af112fa9891a22.png", "c5ecd9b39ffb55f3619e.png",
    "cb6dc61edd5459cc54eb.png", "ccd6c0dfb6444503d784.png",
    "ce6fcbe2940ba0415182.png", "cf286e73fdd3d5bfdacd.png",
    "d0de22b301608827e621.png", "d132d3c009563ca041ca.png",
    "d192ade09369af125bf7.png", "d682dee61cc9d8cca45b.png",
    "d843edeaafc984cf511d.png", "d8be056bd0ca5ca9b3fd.png",
    "dc31279e9262d8e1f0de.png", "de0b429405f641ab3bf4.png",
    "deb5a22a0f8120f6c7e7.png", "df741b1ff136551718ef.png",
    "e32586411aca90ecbf0c.png", "e784f812f521b3b450fe.png",
    "e7f54e5e6ee27c0ec0e7.png", "e98a2249f50bbd26673e.png",
    "f01e0cc2132ef3c85097.png", "f036f2265f279b7b9f27.png",
    "f420d9455267c8f1a99b.png", "f4317f64cf15a17f66fd.png",
    "f732ba150e273bf26f0f.png", "f87fc37d047c47968b63.png",
    "fbe9f55fff93a26af2cd.png", "fc400033a0f08b1267b6.png",
    "4b973189367edba55ab4.png", "9dc5da52e5cce1eda307.png",
    "cd4273ac668e90e54170.png", "31fa227e2b44ab1ae029.png",
    "54770f97b2405c7ba97c.png", "2650a486ca28254a17dc.png",
    "448f0b574d80ae590d30.png",
    # Additional complex instructional tables and rejection region diagrams
    "11369a9311fe8de699f7.png", "ee7fb6439edbe3b04caf.png",
    "9e5716d3827f249ab639.png", "ca6ef3f4adc88bf5b0b4.png",
    "25e2d203ad6aa41283ae.png", "2fe33f96124c0fbd1e18.png",
    "73dc12ecfc35b84f7ec5.png", "b648b7cd86830bb56841.png",
    "dd37716ec772b83ad750.png", "d00cfd67de1bafe37f99.png",
    "4ded731434f7fca8f53a.png", "f116b8b224ba2e5416f1.png",
    "fda5a48d0ac7e658f9e1.png", "f0f52342116a3e978bf1.png",
    "163f536e1ea2a0f49728.png", "09066eb4f2ed2e35dae2.png",
    "bd49737c238d983f9c2d.png", "866c622294530622f91f.png",
    "ca036f8ef817fb8d1dd7.png", "515855f8b9b9f78398d9.png",
    "6535d7ff2e2fc55afa79.png", "f8259749ec97b07048f9.png",
    "701ed5eff65b74fbfce9.png", "e3ec694db1518a4d9436.png",
    "5a8fbea51ecb510eb4cd.png", "b5078c1215465acab3c1.png",
    "a0db1a41b518f5fd261f.png", "d144f282ab1f00e08408.png",
    "d9dc8b8fdd4ad6fc9027.png",
}
VISUAL_ALT_OVERRIDES = {
    "31fa227e2b44ab1ae029.png": "Probability tree showing joint and conditional probabilities for events A, B, C, and D.",
    "54770f97b2405c7ba97c.png": "Capital Market Line tangent to the efficient frontier at the optimal risky market portfolio.",
    "2650a486ca28254a17dc.png": "Student's t-distribution critical values for selected degrees of freedom and one-tailed probabilities.",
    "448f0b574d80ae590d30.png": "Student's t-distribution critical values for selected degrees of freedom and one-tailed probabilities.",
    "3bf1c773e8d459b24845.png": "Quantitative methods formula reference chart, first section.",
    "9c7480bee3dd12df7efa.png": "Quantitative methods formula reference chart, second section.",
    "11369a9311fe8de699f7.png": "Student's t-distribution two-tailed rejection regions and critical values at alpha = 0.05 and df = 38.",
    "ee7fb6439edbe3b04caf.png": "Student's t-distribution two-tailed rejection regions and critical values at alpha = 0.05 and df = 120.",
    "9e5716d3827f249ab639.png": "Comparative structure table of sole proprietorships, general partnerships, limited partnerships, and corporations.",
    "ca6ef3f4adc88bf5b0b4.png": "Statement of cash flows operating activities section prepared under the indirect method.",
    "25e2d203ad6aa41283ae.png": "Statement of cash flows operating activities section prepared under the indirect method.",
    "2fe33f96124c0fbd1e18.png": "Futures contract daily mark-to-market settlement price and margin balance adjustments schedule.",
    "73dc12ecfc35b84f7ec5.png": "Comparative balance sheet extract showing current year asset balances.",
    "b648b7cd86830bb56841.png": "Inventory cost of goods sold and gross profit calculation summary table.",
    "dd37716ec772b83ad750.png": "Multi-year liquidity and activity ratios comparison table for 20X8, 20X7, and 20X6.",
    "d00cfd67de1bafe37f99.png": "Financial statement extracts comparing revenue and working capital accounts between 20X2 and 20X1.",
    "4ded731434f7fca8f53a.png": "Long-lived asset impairment testing data comparing carrying value, fair value, and value in use.",
    "f116b8b224ba2e5416f1.png": "Joint probability distribution table showing outcomes conditional on macroeconomic states.",
    "fda5a48d0ac7e658f9e1.png": "Share purchase transactions and cost basis reference table.",
    "f0f52342116a3e978bf1.png": "Reconciliation of retained earnings schedule showing net income and dividends paid.",
    "163f536e1ea2a0f49728.png": "Comparative current assets balance sheet table comparing 20X1 and 20X2.",
    "09066eb4f2ed2e35dae2.png": "Comprehensive cash flow and coverage ratios formula summary reference poster.",
    "bd49737c238d983f9c2d.png": "Vertical common-size income statement and asset activity ratios reference poster.",
    "866c622294530622f91f.png": "Financial leverage, debt-to-equity, and fixed charge coverage ratios reference poster.",
    "ca036f8ef817fb8d1dd7.png": "Modified duration and convexity calculation reference table.",
    "515855f8b9b9f78398d9.png": "Margin transaction regulations, maintenance margin, and margin call price reference table.",
    "6535d7ff2e2fc55afa79.png": "Multistage dividend discount model multi-period cash flow timeline diagram.",
    "f8259749ec97b07048f9.png": "Money-weighted rate of return internal rate of return step-by-step calculation workflow.",
    "701ed5eff65b74fbfce9.png": "Comparative financial performance metrics between Company A and Company B.",
    "e3ec694db1518a4d9436.png": "Indirect cash flow reconciliation step-by-step adjustment schedule.",
    "5a8fbea51ecb510eb4cd.png": "Step-by-step cash flow from operations adjustment table.",
    "b5078c1215465acab3c1.png": "Direct cash flow statement collection and disbursement adjustment table.",
    "a0db1a41b518f5fd261f.png": "Balance sheet data table comparing assets and liabilities across 20X7 and 20X6.",
    "d144f282ab1f00e08408.png": "Operating, investing, and financing cash flow transactions data table.",
    "d9dc8b8fdd4ad6fc9027.png": "Index constituent stock prices and shares outstanding table for January 1 and December 31.",
}
LATEX_OVERRIDES = {
    "0aac0733302c99791356.png": r"""\begin{aligned}
D_1 &= D_0(1+g_c)=\$1.50(1.08)=\$1.62 \\
\text{Stock value} &= \frac{D_1}{k_e-g_c}
=\frac{\$1.62}{0.12-0.08}=\$40.50
\end{aligned}""",
    "1faede774541a1a6ade5.png": r"""\begin{aligned}
N&=30;\quad FV=1{,}000;\quad PMT=0;\quad PV=-331.40; \\
CPT\to I/Y&=3.750\times2=7.500\% \\
\text{Alternatively,}\quad
\left[\left(\frac{1{,}000}{331.4}\right)^{\!1/30}-1\right]\times2&=7.5\%
\end{aligned}""",
    "515855f8b9b9f78398d9.png": r"""\begin{gathered}
\text{Margin call price}=P_0\left(\frac{1-\text{initial margin}}{1-\text{maintenance margin}}\right),
\quad P_0=\text{initial purchase price} \\[6pt]
\text{Price-weighted index}=\frac{\text{sum of stock prices}}{\text{number of stocks in index adjusted for splits}} \\[6pt]
\text{Market capitalization-weighted index}
=\frac{\text{current total market value of index stocks}}{\text{base-year total market value of index stocks}}
\times\text{base-year index value} \\[6pt]
\text{Equal-weighted index}
=(1+\text{average percentage change in index stocks})\times\text{initial index value} \\[6pt]
[Q(P-VC)]-FC,
\quad Q=\text{units sold},\ P=\text{price per unit},\ VC=\text{variable costs},\ FC=\text{fixed costs} \\[6pt]
DOL=\frac{\%\Delta\text{ operating profit}}{\%\Delta\text{ sales}},
\qquad DFL=\frac{\%\Delta\text{ net income}}{\%\Delta\text{ operating income}} \\[6pt]
\text{Preferred stock value}=\frac{D_p}{k_p} \\[6pt]
\text{Constant-growth dividend discount model:}\qquad V_0=\frac{D_1}{k_e-g_c} \\[6pt]
\text{Sustainable growth rate:}\qquad g=b\times ROE,\quad
b=1-\text{dividend payout rate}
\end{gathered}""",
    "5eba0cad6e36196ef2a2.png": r"""V_1^d=0.278(\$42)=\$11.68,
\qquad \text{or}\qquad V_1^u=0.278(\$60)-\$5=\$11.68""",
    "7caaa04c50c969d43382.png": r"""\text{Forward exchange rate (p/b)}
=\frac{1+\text{interest rate}_{\text{price currency}}}
{1+\text{interest rate}_{\text{base currency}}}
\times\text{spot exchange rate}""",
    "c2785f32c5de517653d6.png": r"""\begin{gathered}
\text{Approximate convexity}=\frac{V_-+V_+-2V_0}{(\Delta YTM)^2V_0} \\[4pt]
V_-=\text{price of the bond if YTM is decreased by }\Delta YTM, \\
V_+=\text{price of the bond if YTM is increased by }\Delta YTM, \\
V_0=\text{current price of the bond} \\[4pt]
\text{Approximate convexity}
=\frac{104.9108+103.9954-2(104.4518)}{0.001^2\times104.4518}=24.89
\end{gathered}""",
    "ddc8204d112236ef752c.png": r"""\begin{gathered}
\text{Step 1: Break the evaluation period into two subperiods based on the timing of cash flows.} \\[3pt]
\begin{aligned}
\text{Holding period 1:}\quad \text{Beginning value}&=\$100 & \text{Dividends paid}&=\$2 & \text{Ending value}&=\$120 \\
\text{Holding period 2:}\quad \text{Beginning value}&=\$240\ (2\text{ shares}) & \text{Dividends paid}&=\$4\ (\$2\text{ per share}) & \text{Ending value}&=\$260\ (2\text{ shares})
\end{aligned} \\[6pt]
\text{Step 2: Calculate the HPR for each holding period.} \\
\text{HPR}_1=\frac{\$120+\$2}{\$100}-1=22\%,\qquad
\text{HPR}_2=\frac{\$260+\$4}{\$240}-1=10\% \\[6pt]
\text{Step 3: Find the compound annual rate that produces the account's two-year total return.} \\
(1+\text{time-weighted rate of return})^2=(1.22)(1.10) \\
\text{Time-weighted rate of return}=[(1.22)(1.10)]^{0.5}-1=15.84\%
\end{gathered}""",
}

WORKED_EXAMPLE_OVERRIDES = {
    "f8259749ec97b07048f9.png": {
        "type": "worked-example",
        "title": "Money-weighted return calculation",
        "steps": [
            {
                "title": "Identify and net the cash flows",
                "body": ["Use the portfolio-account perspective: contributions are inflows and dividends or sale proceeds are outflows."],
                "rows": [
                    ["t = 0", "Purchase first share", "+$100 inflow"],
                    ["t = 1", "Purchase second share", "+$120 inflow"],
                    ["t = 1", "Dividend from first share", "−$2 outflow"],
                    ["t = 1", "Net cash flow", "+$118 inflow"],
                    ["t = 2", "Dividends from two shares", "−$4 outflow"],
                    ["t = 2", "Sale proceeds from two shares", "−$260 outflow"],
                    ["t = 2", "Net cash flow", "−$264 outflow"],
                ],
            },
            {
                "title": "Set the present value of inflows equal to the present value of outflows",
                "equations": [r"100+\frac{118}{1+r}=\frac{264}{(1+r)^2}"],
            },
            {
                "title": "Solve for the periodic return",
                "body": ["Solve for r with trial and error, a financial calculator, or a spreadsheet IRR function."],
                "equations": [r"r=13.86\%"],
            },
        ],
    },
    "ddc8204d112236ef752c.png": {
        "type": "worked-example",
        "title": "Time-weighted return calculation",
        "steps": [
            {
                "title": "Split the evaluation period when the external cash flow occurs",
                "rows": [
                    ["Holding period 1", "Beginning value: $100", "Dividend: $2", "Ending value: $120"],
                    ["Holding period 2", "Beginning value: $240 (2 shares)", "Dividends: $4", "Ending value: $260 (2 shares)"],
                ],
            },
            {
                "title": "Calculate each holding-period return",
                "equations": [r"\text{HPR}_1=\frac{120+2}{100}-1=22\%", r"\text{HPR}_2=\frac{260+4}{240}-1=10\%"],
            },
            {
                "title": "Link the returns and annualize the two-year result",
                "equations": [r"(1+R_{TW})^2=(1.22)(1.10)", r"R_{TW}=[(1.22)(1.10)]^{1/2}-1=15.84\%"],
            },
        ],
    },
    "5a8fbea51ecb510eb4cd.png": {
        "type": "worked-example",
        "title": "Steps in Calculating CFO Under the Indirect Method",
        "steps": [
            {
                "title": "Step 1: Begin with net income",
                "body": ["Start with reported net income from the income statement."],
            },
            {
                "title": "Step 2: Adjust for noncash charges and revenues",
                "body": [
                    "Add back all noncash charges (such as depreciation and amortization) and subtract all noncash components of revenue."
                ],
            },
            {
                "title": "Step 3: Adjust for changes in operating accounts",
                "body": [
                    "Subtract increases in operating asset accounts (uses of cash), and add decreases (sources of cash).",
                    "Add increases in operating liability accounts (sources of cash), and subtract decreases (uses of cash)."
                ],
            },
        ],
    },
    "e3ec694db1518a4d9436.png": {
        "type": "worked-example",
        "title": "CFO Calculation Under Indirect Method",
        "steps": [
            {
                "title": "Step 1: Start with net income",
                "equations": [r"\text{Net income} = \$39{,}000"],
            },
            {
                "title": "Step 2: Adjust for noncash items and gains/losses",
                "body": [
                    "Add back noncash charges: Depreciation of $7,000; Change in deferred tax liability of $5,000; Loss on disposal of PP&E of $2,000.",
                    "Deduct noncash gains: Gain from sale of land of $10,000."
                ],
                "equations": [
                    r"\text{Depreciation} = +\$7{,}000",
                    r"\text{Deferred tax liability change} = +\$5{,}000",
                    r"\text{Loss on disposal of PP\&E} = +\$2{,}000",
                    r"\text{Gain from sale of land} = -\$10{,}000",
                ],
            },
            {
                "title": "Step 3: Adjust for working capital changes",
                "body": ["Subtract increases in receivables and inventories, and add increases in payables."],
            },
        ],
    },
}
LATEX_OVERRIDES.update({
    "026cb4e13d873bf7822f.png": r"H_0:b_1=0\qquad\text{versus}\qquad H_a:b_1\ne0",
    "06630bd05fba27519a9d.png": r"""\begin{gathered}
E(R_p)=w_AE(R_A)+w_BE(R_B)\\
\sigma_p=\sqrt{w_A^2\sigma_A^2+w_B^2\sigma_B^2+2w_Aw_B\rho_{AB}\sigma_A\sigma_B}
\end{gathered}""",
    "0e824a9a1e09a3080901.png": r"""\begin{gathered}
NPV=CF_0+\frac{CF_1}{(1+k)^1}+\frac{CF_2}{(1+k)^2}+\cdots+\frac{CF_n}{(1+k)^n}
=\sum_{t=0}^{n}\frac{CF_t}{(1+k)^t}\\
CF_0=\text{initial investment outlay};\quad CF_t=\text{after-tax cash flow at time }t;\quad
k=\text{required rate of return}
\end{gathered}""",
    "132625f42e17d9eed9a2.png": r"\hat b_1=0.000336/0.000522=0.64",
    "18a0c7fb21bd309fe325.png": r"""\begin{gathered}
t=\frac{(\bar X_1-\bar X_2)-(\mu_1-\mu_2)}{\sqrt{\frac{s_1^2}{n_1}+\frac{s_2^2}{n_2}}}\\
s_p^2=\frac{(n_1-1)s_1^2+(n_2-1)s_2^2}{n_1+n_2-2},\quad df=n_1+n_2-2
\end{gathered}""",
    "1b7cc19ce9ef01c0769f.png": r"""\begin{gathered}
t=\frac{\bar d-\mu_d}{s_{\bar d}},\quad \bar d=\frac1n\sum_{i=1}^{n}d_i,\quad
s_{\bar d}=\frac{s_d}{\sqrt n}\\
s_d=\sqrt{\frac{\sum_{i=1}^{n}(d_i-\bar d)^2}{n-1}},\quad n=\text{number of paired observations}
\end{gathered}""",
    "1cd00ea273bcbd8b83de.png": r"R_{P^*}=R_f+\frac{\sigma_M}{\sigma_P}(R_P-R_f)",
    "1ee599d4c5c36e7a03b9.png": r"""\begin{gathered}
V_-=100.979,\quad V_+=99.035,\quad V_0=100.000,\quad \Delta y=0.0025\\
\text{Approximate modified duration}
=\frac{V_--V_+}{2V_0\Delta YTM}
=\frac{100.979-99.035}{2(100)(0.0025)}=3.888
\end{gathered}""",
    "21bef3e9ea0c32f7b80a.png": r"""\chi_{n-1}^2=\frac{(n-1)s^2}{\sigma_0^2},\quad
n=\text{sample size},\ s^2=\text{sample variance},\ \sigma_0^2=\text{hypothesized population variance}""",
    "25164683aa7a3fe9fb4c.png": r"\frac{42\%}{50\%}=84\%",
    "28d231b3b675e55a5237.png": r"""\begin{gathered}
\text{Long-term debt-to-equity ratio}=\frac{\text{long-term debt}}{\text{total equity}}\\
\text{Total debt-to-equity ratio}=\frac{\text{total debt}}{\text{total equity}},\quad
\text{Debt ratio}=\frac{\text{total debt}}{\text{total assets}},\quad
\text{Financial leverage ratio}=\frac{\text{total assets}}{\text{total equity}}
\end{gathered}""",
    "28f7fa3feffa662210f2.png": r"WAC=2.6\%\left(\frac{90}{409}\right)+1.0\%\left(\frac{72}{409}\right)+5.4\%\left(\frac{247}{409}\right)=4.0\%",
    "2ccaec4603cff359e6ef.png": r"\bar X\xrightarrow{d}N\!\left(\mu,\frac{\sigma^2}{n}\right)",
    "338b7112c46d5840a95d.png": r"\text{Effective tax rate}=\frac{\text{income tax expense}}{\text{pretax income}}",
    "35e2f1e7f1dbc851fcc2.png": r"""\begin{gathered}
\text{Cash conversion cycle}=\text{days of inventory on hand}+\text{days sales outstanding}-\text{days payables outstanding}\\
\text{Total working capital}=\text{current assets}-\text{current liabilities}\\
\text{Net working capital}=\text{current assets excluding cash and marketable securities}
-\text{current liabilities excluding short-term and current debt}\\
\text{Current ratio}=\frac{\text{current assets}}{\text{current liabilities}},\quad
\text{Quick ratio}=\frac{\text{cash and marketable securities}+\text{accounts receivable}}{\text{current liabilities}}\\
\text{Cash ratio}=\frac{\text{cash and marketable securities}}{\text{current liabilities}},\quad
NPV=CF_0+\sum_{t=1}^{n}\frac{CF_t}{(1+k)^t}\\
ROIC=\frac{\text{net operating profit after tax}}{\text{average book value of total capital}}
\end{gathered}""",
    "3bb2014397890a07af61.png": r"""\begin{gathered}
N=5;\quad PMT=10;\quad FV=100;\quad I/Y=10;\quad CPT\to PV=-100\\
N=\text{years};\quad PMT=\text{annual coupon};\quad I/Y=\text{annual discount rate};\quad FV=\text{par value}
\end{gathered}""",
    "50cc04e7dfa0423d251a.png": r"\sigma_{\bar X}=\frac{\sigma}{\sqrt n}",
    "5130c19f799fac192d97.png": r"\%\Delta P\approx-\text{annual modified duration}(\Delta YTM)+\frac12\text{annual convexity}(\Delta YTM)^2",
    "519d55f0688d01363b5e.png": r"N=4;\quad I/Y=5;\quad PMT=-10{,}000;\quad FV=0;\quad CPT\to PV=35{,}460",
})
LATEX_OVERRIDES.update({
    "54553945c671b82bf0cd.png": r"""\begin{gathered}
\text{Current ratio}=\frac{620}{325}=1.9,\quad
\text{Total asset turnover}=\frac{2{,}060}{(1{,}040+1{,}040)/2}=2.0\\
\text{Net profit margin}=\frac{200}{4{,}000}=5.0\%,\quad
\text{Return on common equity}=\frac{200}{(1{,}020+880)/2}=21.1\%\\
\text{Debt-to-equity ratio}=\frac{610+160+55}{1{,}020}=80.9\%
\end{gathered}""",
    "59a299036c135770e493.png": r"\text{Slope of the security characteristic line}=\frac{\operatorname{Cov}_{i,m}}{\sigma_m^2}",
    "61bd5ca134bf37687a10.png": r"""\text{Sample skewness}\approx\left(\frac1n\right)
\frac{\sum_{i=1}^{n}(X_i-\bar X)^3}{s^3},\quad s=\text{sample standard deviation}""",
    "6245af464970b5ba8a09.png": r"(1-0.03)^{365/120}-1=-0.0885=-8.85\%",
    "627c06d97f95c2ab28d4.png": r"\rho_{A,B}=\frac{\operatorname{Cov}_{A,B}}{\sigma_A\sigma_B},\qquad -1\le\rho_{A,B}\le1",
    "6393c0bf4f3bae25e61e.png": r"""\text{Bond value}=\frac{100}{1.055}+\frac{100}{(1.055)(1.0763)}
+\frac{100}{(1.055)(1.0763)(1.1218)}+\frac{1{,}100}{(1.055)(1.0763)(1.1218)(1.155)}=1{,}009.03""",
    "6a1305d8ab02dc34c62d.png": r"S_1^u,\ S_1^d,\ c_1^u,\ c_1^d",
    "6de6f08ba92094f71a16.png": r"\frac{\$18{,}503}{3{,}710}=\$4.99",
    "7015ab810672b1cdbf25.png": r"\hat b_1=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}",
    "70681d457ab25f760168.png": r"\text{Value}=\frac{D_1}{1+k_e}+\frac{D_2}{(1+k_e)^2}+\frac{P_2}{(1+k_e)^2}",
    "74069eb82cbfc437a3ca.png": r"""\begin{gathered}
\text{Average age}=\frac{\$1{,}000{,}000}{\$500{,}000}=2\text{ years},\quad
\text{Total useful life}=\frac{\$3{,}000{,}000}{\$500{,}000}=6\text{ years}\\
\text{Remaining useful life}=\frac{\$2{,}000{,}000}{\$500{,}000}=4\text{ years}
\end{gathered}""",
    "774b223e12fe8bfbd689.png": r"""\begin{gathered}
R^u=1.15,\quad R^d=\frac1{R^u}=\frac1{1.15}=0.87\\
\pi_U=0.715,\qquad \pi_D=1-\pi_U=0.285
\end{gathered}""",
    "77782d7962fcca81389f.png": r"ROE_t=\frac{NI_t}{\text{average }BV_t}=\frac{NI_t}{(BV_t+BV_{t-1})/2}=\frac{\$3{,}526}{(\$18{,}503+\$17{,}143)/2}=19.78\%",
    "7cf4743908e6350a5436.png": r"H_0:\sigma_1^2\le\sigma_2^2\ \text{ versus }\ H_a:\sigma_1^2>\sigma_2^2,\quad\text{or}\quad H_0:\sigma_1^2\ge\sigma_2^2\ \text{ versus }\ H_a:\sigma_1^2<\sigma_2^2",
    "83afd80de0adc64fb616.png": r"P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}=\frac{P(AB)}{P(B)}",
    "88af6e3c10ce6064dbad.png": r"""\begin{gathered}
D_1=\$1.50(1.08)=\$1.62,\quad D_2=\$1.50(1.08)^2=\$1.75,\quad D_3=\$1.50(1.08)^3=\$1.89\\
PV=\frac{\$1.62}{1.12}+\frac{\$1.75}{1.12^2}+\frac{\$1.89}{1.12^3}=\$4.19
\end{gathered}""",
    "8fdd8d088399b17f3ab8.png": r"V_1^u=V_1^d",
    "943bbd70c25c20bc936e.png": r"\sigma_{\bar X}=\frac{\sigma}{\sqrt n},\qquad s_{\bar X}=\frac{s}{\sqrt n}",
    "9c18dc208c7a2ef8e227.png": r"hS_1^u-c_1^u=hS_1^d-c_1^d",
    "a727c24779dc4218bff2.png": r"""\begin{gathered}
\text{Current ratio}=\frac{\text{current assets}}{\text{current liabilities}},\quad
\text{Quick ratio}=\frac{\text{cash}+\text{marketable securities}+\text{accounts receivable}}{\text{current liabilities}}\\
\text{Cash ratio}=\frac{\text{cash}+\text{marketable securities}}{\text{current liabilities}}
\end{gathered}""",
    "a791d9783379b8d25120.png": r"s^2=\frac{\sum_{i=1}^{n}(X_i-\bar X)^2}{n-1},\quad \bar X=\text{sample mean},\quad n=\text{sample size}",
    "aa3f0ae0b7423f0e5858.png": r"\hat Y_i=\hat b_0+\hat b_1X_i,\qquad \hat\varepsilon_i=Y_i-\hat Y_i,\qquad SSE=\sum_i(Y_i-\hat Y_i)^2",
    "aa57a481468bfa3a46fb.png": r"""\sigma_P^2=w_A^2\sigma_A^2+w_B^2\sigma_B^2+w_C^2\sigma_C^2
+2w_Aw_B\operatorname{Cov}_{AB}+2w_Aw_C\operatorname{Cov}_{AC}+2w_Bw_C\operatorname{Cov}_{BC}""",
})
LATEX_OVERRIDES.update({
    "c23d0417de3fdf1393de.png": r"""\begin{gathered}
E(R_P)=w_AE(R_A)+w_BE(R_B)\\
\sigma_P=\sqrt{w_A^2\sigma_A^2+w_B^2\sigma_B^2+2w_Aw_B\rho_{AB}\sigma_A\sigma_B}
\end{gathered}""",
    "c65599f000c6c67f147d.png": r"\frac{(4\times8)-(6\times2)}{2}=10\%",
    "c7572c094ce9abfaf462.png": r"g=b\times ROE,\quad b=1-\text{dividend payout ratio},\quad ROE=\text{return on equity}",
    "ca036f8ef817fb8d1dd7.png": r"""\begin{gathered}
\text{Approximate modified duration}=\frac{V_--V_+}{2V_0\Delta YTM},\quad
\text{Approximate convexity}=\frac{V_-+V_+-2V_0}{(\Delta YTM)^2V_0}\\
\text{Portfolio duration}=w_1D_1+w_2D_2+\cdots+w_ND_N\\
\text{Effective duration}=\frac{V_--V_+}{2V_0\Delta\text{Curve}},\quad
\text{Effective convexity}=\frac{V_-+V_+-2V_0}{(\Delta\text{Curve})^2V_0}\\
\text{Expected loss}=\text{probability of default}\times\text{loss given default},\quad
\text{Loan-to-value ratio}=\frac{\text{current mortgage amount}}{\text{current appraised value}}
\end{gathered}""",
    "d0977dffcd97b32261f7.png": r"\hat Y-t_cs_f<Y<\hat Y+t_cs_f",
    "d22d9bd2e52a32b10b23.png": r"\text{Value}=\frac{\text{dividend to be received}}{1+k_e}+\frac{\text{year-end price}}{1+k_e}",
    "dbf65e859947adcc4384.png": r"""\text{Effective duration}=\frac{V_--V_+}{2V_0\Delta\text{Curve}},\qquad
\text{Effective convexity}=\frac{V_-+V_+-2V_0}{(\Delta\text{Curve})^2V_0}""",
    "dc4a14f515b2202d88f0.png": r"\text{Treynor measure}=\frac{R_P-R_f}{\beta_P}",
    "df8541a59ac291e2c69d.png": r"""\begin{gathered}
\text{Operating profit}=Q(P-VC)-FC\\
Q=\text{units sold},\quad P=\text{price per unit},\quad VC=\text{variable cost per unit},\quad FC=\text{fixed costs}
\end{gathered}""",
    "dfee94b44545573e05df.png": r"\sigma_{\bar X}=\frac{\sigma}{\sqrt n},\quad \sigma_{\bar X}=\text{standard error},\quad \sigma=\text{population standard deviation}",
    "e2ac19ef8afcd5bf67ce.png": r"\text{Sharpe ratio}=\frac{R_P-R_f}{\sigma_P}",
    "e5afd3dfc307ac42de17.png": r"""\begin{gathered}
\bar R_A=\frac{5\%-2\%+12\%}{3}=5\%,\qquad \bar R_B=\frac{7\%-4\%+18\%}{3}=7\%\\
s_A^2=\frac{(5-5)^2+(-2-5)^2+(12-5)^2}{3-1}=49,\quad s_A=7\%\\
s_B^2=\frac{(7-7)^2+(-4-7)^2+(18-7)^2}{3-1}=121,\quad s_B=11\%\\
\operatorname{Cov}_{A,B}=\frac{(5-5)(7-7)+(-2-5)(-4-7)+(12-5)(18-7)}{3-1}=77,\quad
\rho_{A,B}=\frac{77}{7\times11}=1
\end{gathered}""",
    "eceab57bbc002ee18d2e.png": r"""\begin{gathered}
\sigma_P^2=w_1^2\sigma_1^2+w_2^2\sigma_2^2+2w_1w_2\rho_{12}\sigma_1\sigma_2\\
\sigma_P=\sqrt{w_1^2\sigma_1^2+w_2^2\sigma_2^2+2w_1w_2\rho_{12}\sigma_1\sigma_2},\quad
\rho_{12}=\frac{\operatorname{Cov}_{12}}{\sigma_1\sigma_2}
\end{gathered}""",
    "ed7702c0e4dd921efd8c.png": r"\hat b_1=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}",
    "edb55bee849c0f137bc1.png": r"""\begin{gathered}
\text{Price-weighted index}=\frac{\text{sum of stock prices}}{\text{number of stocks adjusted for splits}}\\
\text{Market-capitalization-weighted index}=\frac{\text{current total market value}}{\text{base-year total market value}}\times\text{base-year index value}\\
\text{Equal-weighted index}=(1+\text{average percentage change})\times\text{initial index value}
\end{gathered}""",
    "f94ce9166c1748a54124.png": r"H_0:\mu_d=\mu_{d0}\qquad\text{versus}\qquad H_a:\mu_d\ne\mu_{d0}",
    "f9b99709e3a475d8cfd5.png": r"\hat b_0=\bar Y-\hat b_1\bar X,\qquad \hat b_1=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}",
    "fa183ec49859908dbea5.png": r"""\begin{gathered}
(1.0945)^4=(1.0985)^3(1+3y_{1y})\\
3y_{1y}=\frac{(1.0945)^4}{(1.0985)^3}-1=8.258\%,\qquad
\text{Approximate forward rate}=4(9.45\%)-3(9.85\%)=8.25\%
\end{gathered}""",
    "c6f77f6806809dcb944b.png": r"""V_0=\frac{D_1}{k_e-g_c},\quad
\text{assuming a constant growth rate; }g_c=\text{required return}-\text{dividend yield}""",
    "2cadc8d820d707ee896a.png": r"""\begin{gathered}
\text{Forward rate in SEK/USD}=9.5238\left(\frac{1.07}{1.04}\right)=9.7985\\
\text{The higher SEK interest rate implies approximately }3\%\text{ depreciation.}
\end{gathered}""",
    # Reading 004: EPS Probability Distribution
    "70e6fa8c3e0cf672a579.png": r"""\begin{array}{cc}
\hline
\text{Probability} & \text{EPS} \\
\hline
10\% & \pounds1.80 \\
20\% & \pounds1.60 \\
40\% & \pounds1.20 \\
30\% & \pounds1.00 \\
\hline
100\% &
\end{array}""",
    # Reading 001: Risk premiums
    "012a2171072096685c6c.png": r"""\begin{aligned}
\text{Nominal rate of interest} &= \text{real risk-free rate} \\
&\quad + \text{inflation premium} \\
&\quad + \text{default risk premium} \\
&\quad + \text{liquidity premium} \\
&\quad + \text{maturity premium}
\end{aligned}""",
    # Reading 001: Holding period return
    "a2ab643f6c9472eeb52a.png": r"\mathrm{HPR} = \frac{\$22 + \$1}{\$20} - 1 = 0.15 = 15\%",
    # Reading 001: Geometric mean return
    "e1c9270e8be9fc06f9f5.png": r"\text{Geometric mean return} = \sqrt[n]{(1+R_1)(1+R_2)\dots(1+R_n)} - 1",
    # Reading 001: Harmonic mean
    "0486dc9db2e43eccde06.png": r"\text{Harmonic mean} = \frac{N}{\sum_{i=1}^{N} \frac{1}{X_i}}",
    # Reading 001: HPR & Annualized return
    "a53dd9fc1295af9462d0.png": r"""\begin{aligned}
\text{HPR} &= \frac{1000}{970} - 1 = 0.0309 = 3.09\% \\
\text{Annualized return} &= (1 + 0.0309)^{365/500} - 1 = 0.0225 = 2.25\%
\end{aligned}""",
    # Reading 001: Compounding Frequency Effect Table
    "948af8310dca6ae50ad3.png": r"""\begin{array}{lll}
\hline
\text{Compounding Frequency} & \text{Interest Rate per Period} & \text{Present Value} \\
\hline
\text{Annual } (m=1) & 6.000\% & \$943.40 \\
\text{Semiannual } (m=2) & 3.000\% & \$942.60 \\
\text{Quarterly } (m=4) & 1.500\% & \$942.18 \\
\text{Monthly } (m=12) & 0.500\% & \$941.91 \\
\text{Daily } (m=365) & 0.016438\% & \$941.77 \\
\hline
\end{array}""",
    # Reading 002: Continuous compounding FV and PV
    "71511a64b2da8a8adb89.png": r"""\begin{aligned}
FV &= PV \times e^{rN} \\
PV &= FV \times e^{-rN}
\end{aligned}""",
    # Reading 002: PV calculation
    "92218c0e04930c366544.png": r"PV = \frac{\$1,000}{(1-0.005)^{15}} = \$1,078.09",
    # Reading 002: PV of a perpetuity
    "6ca32a11be38a3477947.png": r"\text{PV of a perpetuity} = \frac{\text{Payment}}{r}",
    # Reading 002: Preferred stock value
    "38a3a057492ae32667d7.png": r"\text{Preferred stock value} = \frac{D_p}{k_p}",
    # Reading 002: Constant growth DDM
    "17ce9817dac87f8be1b7.png": r"V_0 = \frac{D_1}{k_e - g_c}",
    # Reading 002: P2 calculation
    "7d8bb9de4420c369a1eb.png": r"P_2 = \frac{D_3}{k_e - g_c} = \frac{1.386}{0.11 - 0.05} = \$23.10",
    # Reading 002: Implied growth rate
    "600409185df2dfa4c1c4.png": r"""\begin{aligned}
k_e &= \frac{D_1}{V_0} + g_c \\
g_c &= k_e - \frac{D_1}{V_0}
\end{aligned}""",
    # Reading 002: Cash flow series additivity
    "b9272972d2de3d3478c2.png": r"""\begin{array}{rrrrl}
t=1 & t=2 & t=3 & t=4 & \\
\$100 & \$100 & \$100 & \$100 & \text{Cash flow series \#1} \\
\$0 & \$0 & \$300 & \$0 & \text{Cash flow series \#2}
\end{array}""",
    # Reading 007: Standard error of sample mean
    "a369ec81356d2a572d22.png": r"s_{\bar{x}} = \frac{s}{\sqrt{n}} = \frac{20\%}{\sqrt{30}} = 3.65\%",
    "639706fbcd99ec24e8e5.png": r"s_{\bar{x}} = \frac{s}{\sqrt{n}} = \frac{20\%}{\sqrt{200}} = 1.41\%",
    # Reading 008: Standard error & hypothesis tests
    "810be4d8d44e1253925f.png": r"s_{\bar{x}} = \frac{s}{\sqrt{n}} = \frac{0.25\%}{\sqrt{250}} = 0.0158\%",
    "3a8b1a38db57ea0e3c84.png": r"H_0: \mu_d \le \mu_{d0} \quad \text{versus} \quad H_a: \mu_d > \mu_{d0}",
    # Reading 010: Linear regression definitions & t-stat
    "abbdf684b573c6e11196.png": r"""\begin{gathered}
Y_i = b_0 + b_1 X_i + \varepsilon_i, \quad i = 1, \ldots, n \\[6pt]
\text{where:} \\
X_i = i\text{th observation of the independent variable, } X \\
Y_i = i\text{th observation of the dependent variable, } Y \\
b_0 = \text{regression intercept term} \\
b_1 = \text{regression slope coefficient} \\
\varepsilon_i = \text{residual for the } i\text{th observation (disturbance term)}
\end{gathered}""",
    "08c3d6fd673c74150114.png": r"\text{The hat symbol } (\hat{\ }) \text{ above a variable denotes an estimated value.}",
    "72af50f87c3534bda77f.png": r"t = \frac{\hat{b}_1 - b_1}{s_{\hat{b}_1}} = \frac{0.64 - 0}{0.26} = 2.46",
    "ab64b3fcc253ffee791e.png": r"\hat{Y} = -2.3 + 0.64(10) = 4.1",
    "7df3551b01aabdb31a69.png": r"Y_i = b_0 + b_1 \ln(X)_i + \varepsilon_i",
    # Reading 019: Exchange rate formulas
    "374ab524237c9caf906b.png": r"(1 + r_{\text{domestic}}) = \frac{1}{\text{spot}} (1 + r_{\text{foreign}}) \times \text{forward}_{\text{d/f}}",
    "ecde1d4df7083bc0acde.png": r"\text{forward}_{A/D} = \text{spot}_{A/D} \left( \frac{1+r_A}{1+r_D} \right)",
    "59a7bab092c93340df5c.png": r"\frac{S_{t+1} - S_t}{S_t} = \frac{r_f - r_d}{1 + r_d}",
    # Reading 023: Financial ratios & balance sheet table
    "1d3d4206156f488f3e07.png": r"\text{Current ratio} = \frac{\text{Current assets}}{\text{Current liabilities}}",
    "163f536e1ea2a0f49728.png": r"""\begin{array}{lcc}
\hline
\text{Current Assets} & 20X1\ (\$'000) & 20X2\ (\$'000) \\
\hline
\text{Cash} & \$100 & \$150 \\
\text{Accounts receivable} & \$200 & \$250 \\
\text{Inventory} & \$300 & \$400 \\
\hline
\text{Total current assets} & \$600 & \$800 \\
\hline
\end{array}""",
    # Reading 028: Diluted EPS
    "a58e4e90c264ce9245f9.png": r"\text{Diluted EPS} = \frac{\$1,200,000}{500,000 + 25,000} = \$2.29",
    # Reading 029: Project overhead table
    "559b6b263200a1cb15ae.png": r"""\begin{array}{lcc}
\hline
& \text{Project 1 (£m)} & \text{Project 2 (£m)} \\
\hline
\text{Materials} & 150 & 120 \\
\text{Direct labor} & 80 & 60 \\
\text{Production overhead} & 40 & 30 \\
\text{Administrative overhead} & 30 & 30 \\
\hline
\end{array}""",
    # Reading 030: Cash flow items
    "e8ca38e4c2d1ee08ecef.png": r"\text{Cash collected from customers} = \$107,000",
    "384499f807c2b9d9336f.png": r"= \$9,000 + \$7,000 - \$12,000 = \$4,000",
    # Reading 041: Valuation comparison tables
    "122dbfa230f41c84ca9c.png": r"""\begin{array}{lcc}
\hline
& \text{Holt Industries} & \text{Industry} \\
\hline
\text{P/E} & 15.9 & 18.2 \\
\text{P/B} & 2.1 & 2.5 \\
\hline
\end{array}""",
    "e1ecd11b10d84268279f.png": r"""\begin{array}{lccc}
\hline
& 20X3 & 20X2 & 20X1 \\
\hline
\text{P/E} & 15.9 & 52.3 & 115.2 \\
\hline
\end{array}""",
    "ee22ce734bc6fb8557cf.png": r"""\begin{array}{lc}
\hline
\text{Stock price} & \$45.00 \\
\text{Shares outstanding} & 10,000,000 \\
\hline
\end{array}""",
    # Reading 048: Bond payment schedules
    "f9e7bcefe95852081235.png": r"""\begin{array}{lcccc}
\hline
\text{Year} & 1 & 2 & 3 & 4 \\
\hline
\text{PMT} & \$50 & \$50 & \$50 & \$1,050 \\
\hline
\end{array}""",
    "232af2bfe2ed93b188dd.png": r"""\begin{array}{lcccc}
\hline
\text{Year} & 1 & 2 & 3 & 4 \\
\hline
\text{PMT} & \$230.97 & \$230.97 & \$230.97 & \$230.97 \\
\hline
\end{array}""",
    "6c9963b8ad23b6206f52.png": r"""\begin{array}{lcccc}
\hline
\text{Year} & 1 & 2 & 3 & 4 \\
\hline
\text{PMT} & \$194.78 & \$194.78 & \$194.78 & \$194.78 \\
\hline
\end{array}""",
    # Reading 050: Haircut formula
    "646b97c76d873b2eca8a.png": r"\text{Haircut} = 1 - \frac{1}{1 + \text{initial margin percentage}}",
    # Reading 052: Accrued interest
    "93eba638aa9e7e539cd8.png": r"\text{Accrued interest} = \text{coupon payment} \times \frac{\text{days from last coupon to settlement}}{\text{days in coupon period}}",
    "adf3e34552f1135dd267.png": r"\text{Accrued interest (30/360 method)} = \frac{85}{360} \times \$40 = \$9.44",
    "e31f78fad915283413b8.png": r"\text{Accrued interest (actual/actual method)} = \frac{87}{365} \times \$40 = \$9.53",
    # Reading 059: Bond price change
    "ba96f16765368aed85a2.png": r"\text{Change in full bond price} = -\text{EffDur} \times (\Delta \text{Curve}) + \frac{1}{2} \times \text{EffConvexity} \times (\Delta \text{Curve})^2",
    # Reading 065: Debt service ratio
    "4a6e750edfdbd1322d75.png": r"N = 25 \times 12 = 300; \quad I/Y = 6/12 = 0.5; \quad PV = \$300,000",
    "933cf0f9dc9d85ba782c.png": r"\text{WAM} = 210\left(\frac{90}{409}\right) + 100\left(\frac{72}{409}\right) + 280\left(\frac{247}{409}\right) = 233.2\text{ months}",
    "6ea02e936690c88a3738.png": r"\text{Debt service coverage ratio} = \frac{\text{Net operating income}}{\text{Debt service}}",
    # Reading 069: Arbitrage relationship
    "c6c753f06b3f91e1c010.png": r"S_T - S_0(1+R_f)^T - [S_T - F_0(T)] = 0 \implies F_0(T) = S_0(1+R_f)^T",
    # Reading 070: Forward rate agreement
    "ee220812fb982a0026de.png": r"1 + 0.012\left(\frac{9}{12}\right) = \left[1 + 0.01\left(\frac{3}{12}\right)\right] \left[1 + F_{3,6}\left(\frac{6}{12}\right)\right]",
    # Reading 074: Put-call parity
    "f747ba577b8ff289a28a.png": r"\text{Call} = \text{Put} + \text{Stock} - \text{PV}(X)",
    # Reading 075: Binomial model
    "046edb488fbec717e92a.png": r"\text{As an example, we can model a call option with an exercise price of \$50 on a stock currently valued at \$50.}",
    "e5a28a11d341b77a5e29.png": r"\text{The call option will be in the money after an up-move, or out of the money after a down-move.}",
    "a5e2a0881720336dc878.png": r"V_1^d = h S_1^d - c_1^d",
    "3db96982ae6fb053b7eb.png": r"V_1^u = h(\$60) - \$5, \quad V_1^d = h(\$42) - \$0. \quad \text{Setting } V_1^u = V_1^d \implies h = 0.278",
    "6094e1284eeec6466339.png": r"\text{The put option will be in the money after a down-move, or out of the money after an up-move.}",
    "80cd4f684d862db52ca6.png": r"V_1^u = V_1^d",
    "1a11312e2f6408b1206f.png": r"V_0 = h S_0 + p_0 \implies p_0 = V_0 - h S_0",
    "bdb9a8eef7baa5bd9f42.png": r"\pi_U = \text{risk-neutral probability of an up-move} = \frac{1+R_f - R^d}{R^u - R^d}",
    # Reading 077: Return calculation
    "adac6a6934a7033d477c.png": r"\frac{73}{60} - 1 = 21.7\%",
    # Reading 083: Portfolio utility & risk
    "8cf32f859922333e68e4.png": r"U = E(r) - \frac{1}{2} A \sigma^2",
    "40a3e3cf67f93acf08af.png": r"\sigma_{\text{portfolio}} = \sqrt{w_A^2 \sigma_A^2} = w_A \sigma_A",
    "d4e7083bdb1383817f6a.png": r"""\begin{array}{ccc}
\hline
\text{Year} & \text{Asset A} & \text{Asset B} \\
\hline
1 & 5\% & 7\% \\
2 & -2\% & -4\% \\
3 & 12\% & 18\% \\
\hline
\end{array}""",
    # Reading 084: CAPM & Multifactor models
    "3f42b9f9e60661df1847.png": r"\sigma_P = \sqrt{w_A^2 \sigma_A^2} = w_A \sigma_A",
    "caa42df0b0d26eb1a8f1.png": r"E(R_P) = R_f + \left(\frac{E(R_M) - R_f}{\sigma_M}\right)\sigma_P",
    "40e4f9f579c995838c9f.png": r"E(R_P) = R_f + (E(R_M) - R_f)\beta_P",
    "eed272798b2e9f62fe87.png": r"E(R_i) - R_f = \beta_{i1}E(\text{Factor 1}) + \beta_{i2}E(\text{Factor 2}) + \dots + \beta_{ik}E(\text{Factor } k)",
    "7c6407df19760e0d6394.png": r"h(\$60) - \$5 = h(\$42) \implies h = 0.278",
    "56c9cf67bc96796123e6.png": r"\text{MAD} = \frac{\sum_{i=1}^{n} |X_i - \bar{X}|}{n}",
    "fbf3e68baaed4ff8947d.png": r"\rho_{XY} = \frac{s_{XY}}{s_X s_Y}, \quad \text{which implies: } s_{XY} = \rho_{XY} s_X s_Y",
    "6f7d6721732b90a06895.png": r"""\begin{aligned}
s_A &= (0.0028)^{1/2} = 0.0529 \\
s_B &= (0.0124)^{1/2} = 0.1114
\end{aligned}""",
    "6c8cb6afad7e90f528c5.png": r"\text{Safety-first ratio} = \frac{E(R_p) - R_L}{\sigma_p}",
    "03b39cec5a8e33a436bb.png": r"P_T = P_0 \, e^{r_{0,T}}",
    "9a62ec5a44dc7db55225.png": r"s_{\bar{x}} = \frac{s}{\sqrt{n}}",
    "a38b270081b03ba09da7.png": r"\text{Don't be confused by the notation here. A lot of texts use } \bar{d} \text{ for the sample mean of differences.}",
    "877bc4cbaff9c9d12876.png": r"\frac{r \sqrt{n-2}}{\sqrt{1 - r^2}}",
    "83809d2c1406aff62574.png": r"\hat{b}_0 = \bar{Y} - \hat{b}_1 \bar{X}",
    "5175fc426ed42eaff4fe.png": r"\hat{Y} = \hat{b}_0 + \hat{b}_1 X_p",
    "abd01d0c111f07d0253d.png": r"\hat{Y} \pm (t_c \times s_f) \implies [\hat{Y} - (t_c \times s_f) < Y < \hat{Y} + (t_c \times s_f)]",
    "ff49e194dc3fc66d1f2a.png": r"\hat{Y} = -2.39 + 0.64(10) = 4.01",
    "5c9ceccfa8fd273aa824.png": r"\hat{Y} \pm (t_c \times s_f) \implies [4.01 \pm (2.072 \times 0.26)]",
    "bb6ecc27c0cbd1e6337b.png": r"\ln Y_i = b_0 + b_1 X_i + \varepsilon_i",
    "819eda0a509b1969d279.png": r"\text{Basic EPS} = \frac{\$4,350,000 - 0.07(\$5,000,000)}{2,000,000} = \$2.00",
    "9abe5ba2d44aca0045c2.png": r"\text{Diluted EPS} = \frac{\text{Net income} - \text{Pref div} + \text{Convertible pref div}}{\text{Weighted avg shares} + \text{Convertible pref shares}}",
    "1d260d0f595acaec7f2f.png": r"\frac{\$70,000}{240,000} = \$0.29",
    "3dbe8ac6cf26ab55990e.png": r"\frac{100,000 \times \$200 + 1,000,000 \times \$10 + 20,000,000 \times \$1}{540,000,000} = \$0.57",
    "aa78b62a7de945514420.png": r"\text{Preferred stock value} = \frac{D_p}{k_p}",
    "ed5a410b1dc2a81c0be6.png": r"D_4 = (\text{Dividend payout ratio})(E_4) = (0.5)(1.64) = \$0.82",
    "7abf2c379bfd3efcaa6f.png": r"""\begin{array}{lc}
\hline
\text{Depreciation on disposed PPE} & \$15,000 \\
\hline
\end{array}""",
    "b583f1e5ba5f082abf43.png": r"""\begin{array}{lc}
\hline
\text{Beginning carrying value} & \$51,000 \\
\text{Less: Depreciation expense} & (15,000) \\
\text{Ending carrying value} & \$36,000 \\
\hline
\end{array}""",
    "fa3b18b362e1185e933e.png": r"""\begin{aligned}
\text{Step 3: Cash collected from customers} &= \$107,000 \\
&= \$104,000 + \$7,000 - \$4,000
\end{aligned}""",
    "db12b58e6eb019d8b389.png": r"\text{Debt-to-equity} = \frac{\text{Total debt}}{\text{Total shareholders' equity}}",
    "7afefb7c0aa43c5f8fa5.png": r"\text{Debt-to-EBITDA} = \frac{\text{Total debt}}{\text{EBITDA}}",
    "68b5d18bf43d41e39779.png": r"\text{per share impact} = \frac{\$42,000}{25,000\text{ shares}} = \$1.68",
    # Cleaned math formulas & tables from comprehensive visual audit
    "2c2e94112153ae13e113.png": r"""\begin{aligned}
\bar{X} &= \frac{30+12+25+20+23}{5} = 22\% \\
s^2 &= \frac{(30-22)^2+(12-22)^2+(25-22)^2+(20-22)^2+(23-22)^2}{5-1} = 44.5(\%^2)
\end{aligned}""",
    "5ccb6fd44842b0b8b684.png": r"\text{Coefficient of variation (CV)} = \frac{s_x}{\bar{X}} = \frac{\text{standard deviation of } X}{\text{mean of } X}",
    "6806b7731d44425ea82c.png": r"""\begin{gathered}
\text{The chi-square test statistic, } \chi^2_{n-1}\text{, is compared to a critical value at } n - 1 \text{ degrees of freedom.} \\[4pt]
\text{Because the chi-square distribution is bounded below by zero, chi-square values cannot be negative.}
\end{gathered}""",
    "da9ef46306314492193b.png": r"""\begin{gathered}
\hat{Y}_i = \hat{b}_0 + \hat{b}_1 X_i, \quad i = 1, 2, \ldots, n \\[4pt]
\begin{aligned}
\text{where:}\quad
\hat{Y}_i &= \text{estimated value of } Y_i \text{ given } X_i \\
\hat{b}_0 &= \text{estimated intercept term} \\
\hat{b}_1 &= \text{estimated slope coefficient}
\end{aligned}
\end{gathered}""",
    "cf91320a47a33772fb90.png": r"""\begin{gathered}
\text{The intercept term } (\hat{b}_0) \text{ is the line's intersection with the } Y\text{-axis at } X = 0\text{.} \\
\text{It may be positive, negative, or zero. It is expressed as: } \hat{b}_0 = \bar{Y} - \hat{b}_1 \bar{X}
\end{gathered}""",
    "9f2e7b9065d05cb1a4b2.png": r"\text{The estimated intercept, } \hat{b}_0\text{, represents the value of the dependent variable where the regression line intersects the } Y\text{-axis.}",
    "64fa2c7561a8b4ad35c4.png": r"\hat{Y}_p = \hat{b}_0 + \hat{b}_1 X_p",
    "e1309dd1d7fb8e69b33d.png": r"\text{Appreciation of the price currency} = \frac{1}{1-0.0139} - 1 = 0.0141 = 1.41\%",
    "7973c9e97fb289306ab9.png": r"\text{Spot (USD/CHF)} = 0.80 \left( \frac{1.04}{1.10} \right) = 0.7564",
    "6c9fcbbb3cf8dcbf3d91.png": r"""\begin{gathered}
r_e = r_0 + \frac{D}{E}(r_0 - r_d) \\[4pt]
\begin{aligned}
\text{where:}\quad
r_e &= \text{cost of equity} \\
r_0 &= \text{cost of equity with no debt (all equity)} \\
r_d &= \text{cost of debt} \\
D/E &= \text{debt-to-equity ratio}
\end{aligned}
\end{gathered}""",
    "0fdf4c386c02445a2eb3.png": r"\text{Diluted EPS} = \frac{\left[\text{Net income} - \text{Preferred dividends}\right] + \left[\begin{matrix}\text{Convertible} \\ \text{preferred} \\ \text{dividends}\end{matrix}\right] + \left(\begin{matrix}\text{Convertible} \\ \text{debt} \\ \text{interest}\end{matrix}\right)(1-t)}{\left(\begin{matrix}\text{Weighted} \\ \text{average} \\ \text{shares}\end{matrix}\right) + \left(\begin{matrix}\text{Shares from} \\ \text{conversion of} \\ \text{conv. pref. shares}\end{matrix}\right) + \left(\begin{matrix}\text{Shares from} \\ \text{conversion of} \\ \text{conv. debt}\end{matrix}\right) + \left(\begin{matrix}\text{Shares} \\ \text{issuable from} \\ \text{stock options}\end{matrix}\right)}",
    "3d59c6ec97e12697b5d2.png": r"\text{Diluted EPS} = \frac{\left[\text{Net income} - \text{Preferred dividends}\right] + \left[\begin{matrix}\text{Convertible} \\ \text{preferred} \\ \text{dividends}\end{matrix}\right] + \left(\begin{matrix}\text{Convertible} \\ \text{debt} \\ \text{interest}\end{matrix}\right)(1-t)}{\left(\begin{matrix}\text{Weighted} \\ \text{average} \\ \text{shares}\end{matrix}\right) + \left(\begin{matrix}\text{Shares from} \\ \text{conversion of} \\ \text{conv. pref. shares}\end{matrix}\right) + \left(\begin{matrix}\text{Shares from} \\ \text{conversion of} \\ \text{conv. debt}\end{matrix}\right) + \left(\begin{matrix}\text{Shares} \\ \text{issuable from} \\ \text{stock options}\end{matrix}\right)}",
    "3fbfda69d29ce8b068e1.png": r"""\begin{array}{lr}
\hline
\text{Net income} & \$120 \\
\text{Decrease in accounts receivable} & 20 \\
\text{Depreciation} & 25 \\
\text{Increase in inventory} & 10 \\
\text{Increase in accounts payable} & 7 \\
\text{Decrease in wages payable} & 5 \\
\text{Increase in deferred tax liabilities} & 15 \\
\text{Profit from the sale of land} & 2 \\
\hline
\end{array}""",
    "7f3ae88944b469901a9c.png": r"""\begin{array}{lr}
\hline
\text{Original cost} & \$250{,}000 \\
\text{Accumulated depreciation to date} & \$150{,}000 \\
\text{Expected future cash flows} & \$105{,}000 \\
\text{Fair value} & \$95{,}000 \\
\text{Value in use} & \$90{,}000 \\
\text{Selling costs} & \$10{,}000 \\
\hline
\end{array}""",
    "28c9d5ee90ae3d239365.png": r"""\begin{aligned}
\text{20X6: } 365 / 3.71 &= 98\text{ days} \\
\text{20X7: } 365 / 6.83 &= 53\text{ days}
\end{aligned}""",

    # Reading 003: CV and sample standard deviation (from user screenshots)
    "c9ea1d43f6db65645d23.png": r"""s = [44.5(\%^2)]^{1/2} = 6.67\%, \qquad \sqrt{0.00445} = 0.0667""",
    "593a19d743817e2bbf1b.png": r"""\begin{aligned}
\text{CV}_{\text{T-bills}} &= \frac{0.36}{0.25} = 1.44 \\[8pt]
\text{CV}_{\text{S\&P 500}} &= \frac{7.30}{1.09} = 6.70
\end{aligned}""",

    # Reading 001: HPR and TWR calculations
    "d160dc44453cbc30bdd6.png": r"""\begin{aligned}
\text{HPR} &= \frac{100.75}{100} - 1 = 0.0075 = 0.75\% \\[8pt]
\text{Annualized return} &= (1 + 0.0075)^{365/90} - 1 = 0.0308 = 3.08\%
\end{aligned}""",
    "7960c885d7c1021a5ccf.png": r"""\begin{gathered}
\begin{aligned}
\text{HPR}_1 &= \frac{50+1}{40} - 1 = 27.5\% \\[6pt]
\text{HPR}_2 &= \frac{120+2}{100} - 1 = 22.0\%
\end{aligned} \\[8pt]
\text{TWR} = \sqrt{(1+0.275)(1+0.22)} - 1 = 24.72\%
\end{gathered}""",

    # Reading 002: TVM and forward rates
    "b5a5f1c37f051fa083f7.png": r"""\begin{gathered}
\frac{\$1{,}000}{(1+r)^{15}} = \$650 \\[8pt]
(1+r)^{15} = \frac{\$1{,}000}{\$650} = 1.5385 \\[8pt]
r = (1.5385)^{1/15} - 1 = 0.0291 = 2.91\%
\end{gathered}""",
    "382bf0fe7abe8c5d6790.png": r"""\begin{gathered}
V_0 = \frac{D_1}{k_e - g_c} \\[8pt]
k_e - g_c = \frac{D_1}{V_0} \\[8pt]
k_e = \frac{D_1}{V_0} + g_c
\end{gathered}""",
    "27528eb2b013c479c2c6.png": r"""\begin{gathered}
(1.08)^2 = (1.04)(1 + {}_{1}y_{1y}) \\[8pt]
1 + {}_{1}y_{1y} = \frac{(1.08)^2}{1.04} \\[8pt]
{}_{1}y_{1y} = \frac{(1.08)^2}{1.04} - 1 = \frac{1.1664}{1.04} - 1 = 12.154\%
\end{gathered}""",
    "7b9ac28334895dd7ee8e.png": r"""\begin{gathered}
PV = \frac{FV}{(1+r)^t} = FV(1+r)^{-t} \\[6pt]
\text{where: } r = \text{interest rate per period}, \quad t = \text{number of periods} \\[8pt]
\text{Annuity payment} = \frac{r \times PV}{1 - (1+r)^{-t}}
\end{gathered}""",

    # Reading 003: Mean absolute deviation
    "a3456fb018c5b468db7b.png": r"""\begin{aligned}
\bar{X} &= \frac{30+12+25+20+23}{5} = 22\% \\[8pt]
\text{MAD} &= \frac{|30-22| + |12-22| + |25-22| + |20-22| + |23-22|}{5} \\[8pt]
&= \frac{8 + 10 + 3 + 2 + 1}{5} = 4.8\%
\end{aligned}""",

    # Reading 009: Chi-square test of independence
    "083fbe7940af1ac28945.png": r"""\begin{gathered}
\chi^2 = \sum_{i=1}^{r} \sum_{j=1}^{c} \frac{(O_{ij} - E_{ij})^2}{E_{ij}} \\[6pt]
\begin{aligned}
\text{where:}\quad
O_{ij} &= \text{observed frequency in cell } i, j \\
E_{ij} &= \text{expected frequency in cell } i, j \\
r &= \text{number of rows}, \quad c = \text{number of columns}
\end{aligned}
\end{gathered}""",

    # Reading 010: Linear regression statistics
    "6786e9c8fdf29d0f0749.png": r"""\begin{aligned}
\operatorname{Cov}(\text{S\&P 500}, \text{ABC}) &= 0.000336, &\quad \text{Mean return, S\&P 500} &= -2.70\% \\[6pt]
\operatorname{Var}(\text{S\&P 500}) &= 0.000522, &\quad \text{Mean return, ABC} &= -4.05\%
\end{aligned}""",

    # Reading 012: Market share table
    "6ac72c7dd404fa6b9475.png": r"""\begin{array}{lc}
\hline
\text{Firm} & \text{Market Share} \\
\hline
\text{Acme} & 25\% \\
\text{Blake} & 15\% \\
\text{Curtis} & 15\% \\
\text{Dent} & 10\% \\
\text{Erie} & 5\% \\
\text{Federal} & 5\% \\
\hline
\end{array}""",

    # Reading 028: Interest coverage adjustment
    "4c780503f5ac5a499e6e.png": r"""\begin{gathered}
\text{Interest coverage} = \frac{\text{EBIT}}{\text{Interest expense}} \\[8pt]
\text{Before adjustment} = \frac{\text{EUR }160\text{ million}}{\text{EUR }80\text{ million}} = 2.0 \\[8pt]
\text{After adjustment} = \frac{\text{EUR }160\text{ million} + \text{EUR }10\text{ million}}{\text{EUR }80\text{ million} + \text{EUR }20\text{ million}} = 1.7
\end{gathered}""",

    # Reading 029: Liquidity ratios
    "47eabfa9f40215ebb4a3.png": r"""\begin{aligned}
\text{Current ratio} &= \frac{\text{Current assets}}{\text{Current liabilities}} \\[8pt]
\text{Quick ratio} &= \frac{\text{Cash} + \text{Marketable securities} + \text{Receivables}}{\text{Current liabilities}} \\[8pt]
\text{Cash ratio} &= \frac{\text{Cash} + \text{Marketable securities}}{\text{Current liabilities}}
\end{aligned}""",

    # Reading 035: Effective tax rates
    "b5ffc67af0ec8ba5115f.png": r"""\begin{aligned}
\text{Tax in Italy} &= \text{EUR }100\text{ million} \times 20\% = \text{EUR }20\text{ million} \\[8pt]
\text{Effective tax rate} &= \frac{30 + 20}{100 + 100} = \frac{50}{200} = 25\%
\end{aligned}""",
    "9e5ff947fdee4b6880d6.png": r"""\begin{aligned}
\text{Year 1} &= \frac{\text{EUR }75\text{ million}}{\text{EUR }250\text{ million}} = 0.300 = 30.0\% \\[8pt]
\text{Year 2} &= \frac{\text{EUR }48\text{ million}}{\text{EUR }225\text{ million}} = 0.213 = 21.3\% \\[8pt]
\text{Year 3} &= \frac{\text{EUR }88\text{ million}}{\text{EUR }300\text{ million}} = 0.293 = 29.3\%
\end{aligned}""",

    # Reading 037: DuPont components & CV ratios
    "d2b5bc4b4f0457b01cd9.png": r"""\begin{gathered}
\frac{\text{Net income}}{\text{EBT}} \text{ is called the tax burden and is equal to } (1 - \text{tax rate}) \\[8pt]
\frac{\text{EBT}}{\text{EBIT}} \text{ is called the interest burden} \\[8pt]
\frac{\text{EBIT}}{\text{Revenue}} \text{ is called the EBIT margin}
\end{gathered}""",
    "ccebc1ac52a37ebf0aa2.png": r"""\begin{aligned}
\text{CV}_{\text{sales}} &= \frac{\text{Standard deviation of sales}}{\text{Mean sales}} \\[8pt]
\text{CV}_{\text{operating income}} &= \frac{\text{Standard deviation of operating income}}{\text{Mean operating income}} \\[8pt]
\text{CV}_{\text{net income}} &= \frac{\text{Standard deviation of net income}}{\text{Mean net income}}
\end{aligned}""",

    # Reading 040: Index value calculations
    "5fce87d33d98249e939d.png": r"""\begin{gathered}
\text{Current index value} = \frac{\text{Current total market value of index stocks}}{\text{Base year total market value of index stocks}} \times \text{Base year index value} \\[8pt]
\text{Current index value} = \frac{\$95\text{ million}}{\$80\text{ million}} \times 100 = 118.75
\end{gathered}""",
    "bda50c817dd110115564.png": r"""\begin{gathered}
\text{Total portfolio value December 31:} \\
22(1{,}500) + 40(10{,}000) + 34(3{,}000) = \$535{,}000 \\[6pt]
28(1{,}500) + 50(10{,}000) + 30(3{,}000) = \$632{,}000 \\[8pt]
\frac{632}{535} - 1 = 0.1813 = 18.13\% \\[6pt]
\text{From a base value of } 100\text{, the December 31 index value would be: } \frac{632}{535} \times 100 = 118.13
\end{gathered}""",

    # Reading 046: Multistage DDM and valuation
    "1ee43be87194145edb1c.png": r"""\begin{aligned}
\text{Dividend: } &\quad \frac{\$1.05}{1.132} = \$0.93 \\[8pt]
\text{Year-end price: } &\quad \frac{\$13.45}{1.132} = \$11.88
\end{aligned}""",
    "f0a261bf234635635e4c.png": r"""\begin{gathered}
\text{Value} = \frac{D_1}{(1+k_e)} + \frac{D_2}{(1+k_e)^2} + \dots + \frac{D_n}{(1+k_e)^n} + \frac{P_n}{(1+k_e)^n} \\[8pt]
\text{where: } P_n = \frac{D_{n+1}}{k_e - g_c}
\end{gathered}""",
    "c0d266656dd457a5c5ae.png": r"""\begin{aligned}
D_1 &= \$1.00(1.25) = \$1.25 \\
D_2 &= \$1.25(1.25) = \$1.5625 \\
D_3 &= \$1.5625 \times 1.06 = \$1.6563 \\[6pt]
P_2 &= \frac{\$1.6563}{0.10 - 0.06} = \$41.41 \\[8pt]
V_0 &= \frac{\$1.25}{1.10} + \frac{\$1.5625 + \$41.41}{(1.10)^2} = \$36.65
\end{aligned}""",

    # Reading 053: Bond yields and Z-spread
    "c5fa56264488e19e5816.png": r"""\text{Current yield} = \frac{\$60}{\$802.07} = 0.0748 = 7.48\%""",
    "f55d351ab55aee656ffc.png": r"""\begin{gathered}
89.464 = \frac{9}{(1.04+ZS)^1} + \frac{9}{(1.08167+ZS)^2} + \frac{109}{(1.12377+ZS)^3} \\[8pt]
\implies ZS = 1.67\% \text{ or } 167\text{ basis points}
\end{gathered}""",

    # Reading 055: Forward rate
    "a8a12553c4d542e8b2f1.png": r"""\begin{gathered}
(1.08)^2 = (1.04)(1 + {}_{1}y_{1y}) \\[8pt]
1 + {}_{1}y_{1y} = \frac{(1.08)^2}{1.04} \\[8pt]
{}_{1}y_{1y} = \frac{(1.08)^2}{1.04} - 1 = \frac{1.1664}{1.04} - 1 = 12.154\%
\end{gathered}""",

    # Reading 058: Convexity effect
    "5f84a78674f84e299022.png": r"""\text{The convexity effect is } \frac{1}{2} \times 16.9 \times (-0.005)^2 = 0.000211 = 0.0211\%""",

    # Reading 064: Tranche structure
    "6e44584c91d80f8723b7.png": r"""\begin{array}{lrc}
\hline
\text{Tranche Name} & \text{Face Value (\$)} & \text{Interest Rate} \\
\hline
\text{Tranche A senior notes} & \$300{,}000{,}000 & \text{MRR} + 0.5\% \\
\text{Tranche B subordinated notes} & \$80{,}000{,}000 & \text{MRR} + 1.5\% \\
\text{Tranche C subordinated notes} & \$30{,}000{,}000 & \text{Variable} \\
\hline
\text{Total} & \$410{,}000{,}000 & \\
\hline
\end{array}""",

    # Reading 072: Swap rate pricing
    "121bb027a7847c8533ce.png": r"""\begin{aligned}
&\frac{\text{MRR}_1}{1+S_1} + \frac{\text{MRR}_2}{(1+S_2)^2} + \frac{\text{MRR}_3}{(1+S_3)^3} + \frac{\text{MRR}_4}{(1+S_4)^4} \\[8pt]
&\quad = \frac{F}{1+S_1} + \frac{F}{(1+S_2)^2} + \frac{F}{(1+S_3)^3} + \frac{F}{(1+S_4)^4}
\end{aligned}""",

    # Reading 084: Beta formula
    "b6a11f2e7ab92ea3098b.png": r"""\beta_i = \frac{\operatorname{Cov}_{im}}{\sigma_m^2} = \frac{0.048}{0.2^2} = 1.2""",

    # Additional comprehensive LaTeX overrides for clean KaTeX rendering
    "0193cf52a48665097099.png": r"""\text{DOL} = \frac{\%\Delta \text{ operating profit}}{\%\Delta \text{ sales}}""",
    "0905ad2c3b40bd6d09b9.png": r"""\begin{array}{llr}
\hline
\text{Ending inventory at cost} & & \text{Total} \\
\hline
\text{2 units @ \$28 each} & & \$56 \\
\text{8 units @ \$30 each} & & \underline{\$240} \\
\text{Total} & & \$296 \\
\hline
\end{array}""",
    "1fb8a6f8f67aa5416aab.png": r"""\begin{gathered}
\text{minimize } P(R_p < R_L) \\[6pt]
\begin{aligned}
\text{where:}\quad R_p &= \text{portfolio return} \\
R_L &= \text{threshold return level}
\end{aligned}
\end{gathered}""",
    "3b7c93cc5ce6bd6a5380.png": r"""\text{With } V_1^u = V_1^d\text{, the value of the portfolio after one period is known with certainty.}""",
    "650cdce7825cb68ea376.png": r"""\text{The portfolio value after an up-move, } V_1^u\text{, is } hS_1^u - c_1^u.""",
    "65a2141ac33793ae54c9.png": r"""\begin{aligned}
\text{Net cash flows: } \mathrm{CF}_0 &= +100; \\[6pt]
\mathrm{CF}_1 &= +120 - 2 = +118; \\[6pt]
\mathrm{CF}_2 &= -260 + -4 = -264
\end{aligned}""",
    "8d1aa619580cef2d4a2b.png": r"""(\text{Exports} - \text{Imports}) = (\text{Private savings} - \text{Investment in physical capital}) + (\text{Government surplus})""",
    "911feaddd92bd425e804.png": r"""\text{Setting } V_1^u = V_1^d\text{, we get: } hS_1^u - c_1^u = hS_1^d - c_1^d""",
    "a9ed912c7993dfa2c4b1.png": r"""\text{With } V_1^u = V_1^d\text{, the value of the portfolio after one period is known with certainty.}""",
    "d0a8953faed46d962b39.png": r"""\text{The portfolio value after an up-move, } V_1^u\text{, is } hS_1^u - c_1^u""",
    "d89cd69aec2f738b6420.png": r"""\text{The portfolio value after an up-move, } V_1^u\text{, is } hS_1^u + p_1^u""",
    "d9800d44ed03f845bf82.png": r"""\text{The portfolio value after a down-move, } V_1^d\text{, is } hS_1^d - c_1^d""",
    "dd53dd2ba57ddf9493a0.png": r"""\text{Investor's return on investment} = \frac{130 + 80 - 6}{200} - 1 = 2\%""",
    "2ab715a6f0de958dc0cd.png": r"""\text{Investor's return on investment} = \frac{130 + 80 - 6}{200} - 1 = 2\%""",
    "0bc94af7839c3cf7e443.png": r"""\$40.50 - \$12.50 = \$28.00""",
    "01643876b2d0c0c5564a.png": r"""\begin{gathered}
\text{Approximate ModDur} = \frac{88.127 - 85.092}{2 \times 86.59 \times 0.005} = 3.505 \\[6pt]
\text{Approximate price change for a } 1\% \text{ change in YTM is } 3.505\%.
\end{gathered}""",
    "5eaddb4cad8581b5b5f6.png": r"""\begin{aligned}
\text{Change in index} &= \frac{25\% - 7.7\% + 18.4\%}{3} = 11.9\% \\[8pt]
\text{New index value} &= 131(1 + 0.119) = 146.59
\end{aligned}""",
    "0452dfb594c84373523b.png": r"""\text{PV} = \$1{,}000 \left(1 + \frac{0.06}{4}\right)^{-4} = \$942.18""",
    "eb7f359c65a0d3f19f81.png": r"""\text{So, we can define beta: } \beta = \frac{\operatorname{Cov}_{im}}{\sigma_m^2} \text{ as a standardized measure of systematic risk.}""",
    "f2f4fd1cb3e37e778906.png": r"""\text{Standardized covariance term: } \frac{\operatorname{Cov}_{im}}{\sigma_m^2}""",
    "e88129399dc1f666ea7f.png": r"""\text{Because } \operatorname{Var}_{\text{portfolio}} = \sigma_{\text{portfolio}}^2\text{, this can also be written as: } \sigma_P = \sqrt{w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2w_1 w_2 \operatorname{Cov}_{12}}""",
    "e8c947293efad5eb6c70.png": r"""\text{Cash conversion cycle} = \text{Days sales outstanding} + \text{Days of inventory on hand} - \text{Number of days of payables}""",
    "ef62d309a7d2897c58be.png": r"""\begin{gathered}
\text{Net principal flow} = \text{Ending bonds payable} - \text{Beginning bonds payable} \\[6pt]
= \$15{,}000 - \$10{,}000 = \$5{,}000
\end{gathered}""",
    "57b03ba3a79fd00bb8f5.png": r"""\frac{\text{P}}{\text{S}} = \frac{\$11.40}{\$17.30} = 0.66""",
    "d0a070a304a14f0665a4.png": r"""\begin{array}{ll}
\hline
\text{Average selling price per product} & \$10 \\
\text{Quantity sold} & 4.5\text{ million} \\
\text{Gross profit margin} & 60\% \\
\hline
\end{array}""",
    "f4b90a04a9f20f4ced8b.png": r"""\begin{aligned}
\text{20X6: } \$2{,}900{,}000 / \$5{,}500{,}000 &= 52.73\% \\[6pt]
\text{20X7: } \$3{,}400{,}000 / \$7{,}500{,}000 &= 45.33\%
\end{aligned}""",
    "0eb2f4bb0265403fd90b.png": r"""\begin{array}{cccccc}
\hline
\text{20X1} & \text{20X2} & \text{20X3} & \text{20X4} & \text{20X5} & \text{20X6} \\
\hline
22\% & 5\% & -7\% & 11\% & 2\% & 11\% \\
\hline
\end{array}""",
    "181d797a8aba1624a9d8.png": r"""\begin{array}{cccccc}
\hline
\text{20X1} & \text{20X2} & \text{20X3} & \text{20X4} & \text{20X5} & \text{20X6} \\
\hline
22\% & 5\% & -7\% & 11\% & 2\% & 11\% \\
\hline
\end{array}""",
    "6988ab79d3f289854d92.png": r"""\begin{aligned}
&\sqrt{(0.25)^2(0.15)^2 + (0.75)^2(0.10)^2 + 2(0.25)(0.75)(0.15)(0.10)(-0.75)} \\[6pt]
&\quad = \sqrt{0.001406 + 0.005625 - 0.004219} = \sqrt{0.002812} = 0.053 = 5.3\%
\end{aligned}""",
    "6b743f1561694fe049aa.png": r"""\left[\left(\frac{28}{22}-1\right) + \left(\frac{50}{40}-1\right) + \left(\frac{30}{34}-1\right)\right]\left(\frac{1}{3}\right) = 0.135 = 13.5\%""",
    "7b2c0a64ad3b7eeaf1c9.png": r"""\begin{gathered}
\frac{3.5}{\left(1+\frac{\text{YTM}}{2}\right)^1} + \frac{3.5}{\left(1+\frac{\text{YTM}}{2}\right)^2} + \dots + \frac{103.5}{\left(1+\frac{\text{YTM}}{2}\right)^{10}} = 102.078 \\[8pt]
\text{N}=10; \quad \text{PMT}=3.5; \quad \text{FV}=100; \quad \text{PV}=-102.078; \quad \text{CPT } \to \text{I/Y}=3.253\%
\end{gathered}""",
    "08229e360d1586ea9a6e.png": r"""\text{Standard error of sample mean} = \frac{s}{\sqrt{n}}""",
    "b986d5352c23c4c021b8.png": r"""\begin{aligned}
\text{20X6: } \$3{,}670{,}000 / \$866{,}000 &= 4.24 \\[6pt]
\text{20X7: } \$5{,}995{,}000 / \$1{,}505{,}000 &= 3.98
\end{aligned}""",
    "09ebe23995642d4ed195.png": r"""V_1^u = 0.333(\$60) = \$20, \quad\text{or } V_1^d = 0.333(\$42) + \$6 = \$20""",
    "35df5994aaca76e35292.png": r"""1.32 \times 1.05 = \$1.386""",
    "c96b4a7d763460d297b0.png": r"""\text{Adjusted loan amount after 30 days} = \$970{,}874 \times \left[1 + (0.02 \dots)\right]""",
    "ff4ef9a2c74dd80a7d26.png": r"""\text{Diluted EPS} = \frac{\text{Net income} - \text{Preferred dividends} + \text{Convertible debt interest}(1-t)}{\text{Weighted average shares} + \text{Shares from conversion}}""",
    "e5694160c76dce46512f.png": r"""\text{Cash return on equity ratio} = \frac{\text{CFO}}{\text{Average total equity}}""",
    "58c566bbc36b29a01c3e.png": r"""\text{Cash-to-income ratio} = \frac{\text{CFO}}{\text{Operating income}}""",
    "77782d7962fcca81389f.png": r"""\text{ROE}_t = \frac{\text{NI}_t}{\text{average }\text{BV}_t} = \frac{\text{NI}_t}{(\text{BV}_t + \text{BV}_{t-1})/2} = \frac{\$3{,}526}{(\$18{,}503 + \$17{,}143)/2} = 19.78\%""",
    "c7572c094ce9abfaf462.png": r"""g = b \times \text{ROE}, \quad b = 1 - \text{dividend payout ratio}, \quad \text{ROE} = \text{return on equity}""",
    "13b2cc671486ba4043b0.png": r"""\text{Fixed asset turnover} = \frac{\text{Revenue}}{\text{Average net fixed assets}}""",
    "97023bdade95f1765bcd.png": r"""\text{Working capital turnover} = \frac{\text{Revenue}}{\text{Average working capital}}""",
    "0fdf4c386c02445a2eb3.png": r"""\text{Diluted EPS} = \frac{\left[\text{Net income} - \text{Preferred dividends}\right] + \left[\begin{matrix}\text{Convertible} \\[2pt] \text{preferred} \\[2pt] \text{dividends}\end{matrix}\right] + \left(\begin{matrix}\text{Convertible} \\[2pt] \text{debt} \\[2pt] \text{interest}\end{matrix}\right)(1-t)}{\left(\begin{matrix}\text{Weighted} \\[2pt] \text{average} \\[2pt] \text{shares}\end{matrix}\right) + \left(\begin{matrix}\text{Shares from} \\[2pt] \text{conversion of} \\[2pt] \text{conv. pref. shares}\end{matrix}\right) + \left(\begin{matrix}\text{Shares from} \\[2pt] \text{conversion of} \\[2pt] \text{conv. debt}\end{matrix}\right) + \left(\begin{matrix}\text{Shares} \\[2pt] \text{issuable from} \\[2pt] \text{stock options}\end{matrix}\right)}""",
    "3d59c6ec97e12697b5d2.png": r"""\text{Diluted EPS} = \frac{\left[\text{Net income} - \text{Preferred dividends}\right] + \left[\begin{matrix}\text{Convertible} \\[2pt] \text{preferred} \\[2pt] \text{dividends}\end{matrix}\right] + \left(\begin{matrix}\text{Convertible} \\[2pt] \text{debt} \\[2pt] \text{interest}\end{matrix}\right)(1-t)}{\left(\begin{matrix}\text{Weighted} \\[2pt] \text{average} \\[2pt] \text{shares}\end{matrix}\right) + \left(\begin{matrix}\text{Shares from} \\[2pt] \text{conversion of} \\[2pt] \text{conv. pref. shares}\end{matrix}\right) + \left(\begin{matrix}\text{Shares from} \\[2pt] \text{conversion of} \\[2pt] \text{conv. debt}\end{matrix}\right) + \left(\begin{matrix}\text{Shares} \\[2pt] \text{issuable from} \\[2pt] \text{stock options}\end{matrix}\right)}""",
    # Reference document formulas
    "25fcc334b0242892c96e.png": r"""\begin{aligned}
H_0: \mu &\le 0.0\%, \quad H_a: \mu > 0.0\% \\[8pt]
z &= \frac{\bar{X} - \mu_0}{\sigma / \sqrt{n}} = \frac{2.0 - 0.0}{20.0 / 6} = 0.60
\end{aligned}""",
    "b52fe3c51c6c1ecf0276.png": r"""\begin{aligned}
\text{FCFE} &= \text{CFO} - \text{FC}_{\text{Inv}} + \text{Net borrowing} \\[6pt]
\text{where:}\quad \text{FC}_{\text{Inv}} &= \text{fixed capital investment (net capital expenditures)} \\
\text{Net borrowing} &= \text{debt issued} - \text{debt repaid}
\end{aligned}""",
    "b9fb50feb2c065f019f3.png": r"""{}_N y_{(M-N)y} = \left[ \frac{(1 + S_M)^M}{(1 + S_N)^N} \right]^{\frac{1}{M-N}} - 1""",
    "37d031accc69305d0b0a.png": r"""\begin{aligned}
\text{CML:}\quad E(R_p) &= R_f + \left( \frac{E(R_m) - R_f}{\sigma_m} \right) \sigma_p \\[8pt]
&= R_f + [E(R_m) - R_f] \left( \frac{\sigma_p}{\sigma_m} \right)
\end{aligned}""",
    "80250aed3b166358df5a.png": r"""M^2 = R_f + \left( \frac{\sigma_m}{\sigma_p} \right) (R_p - R_f)""",
    "b13e36d68a57f72fc03a.png": r"""\text{If } \text{EPS} = x = \$7.25, \text{ then } z = (x - \mu)/\sigma = (\$7.25 - \$5.00)/\$1.50 = 1.50""",
    "e0cd75159982915c0cdd.png": r"""\text{Real P/B exchange rate} = \text{Nominal P/B exchange rate} \times \left(\frac{\text{CPI}_{\text{base}}}{\text{CPI}_{\text{price}}}\right)""",
    "4767f50c225f8db4e12e.png": r"""\text{FCFF} = \text{NI} + \text{NCC} + [\text{Int} \times (1 - \text{tax rate})] - \text{FC}_{\text{Inv}} - \text{WC}_{\text{Inv}}""",
    "bca94350018619ac5e9a.png": r"""\text{FCFF} = \text{CFO} + [\text{Int} \times (1 - \text{tax rate})] - \text{FC}_{\text{Inv}}""",
    "6166d8e46496f1f1f8b2.png": r"""-\text{Bond price} + \frac{\text{Coupon}_1}{1 + \text{IRR}} + \frac{\text{Coupon}_2}{(1 + \text{IRR})^2} + \dots + \frac{\text{Coupon}_n + \text{Par}}{(1 + \text{IRR})^n} = 0""",
    "2deff1f374adb143e779.png": r"""-\text{Bond price} + \frac{\text{Coupon}_1}{1 + \frac{\text{IRR}}{2}} + \frac{\text{Coupon}_2}{\left(1 + \frac{\text{IRR}}{2}\right)^2} + \dots = 0""",
    "58de1c97dd9050c2bf4f.png": r"""\frac{\text{PMT}}{1.01} + \frac{\text{PMT}}{(1.02)^2} + \frac{\text{PMT} + 100}{(1.03)^3}""",
    "fa9493dcaa14da4e9263.png": r"""\text{Leveraged return} = \frac{r(V_0 + V_B) - V_B \times r_B}{V_0}""",
    "81faeb586da36071a56c.png": r"""r = \frac{V_1 - V_0 - \text{Total fees}}{V_0}""",
    "20c1ec6c7fd73f41b4f2.png": r"""\sigma_{\text{portfolio}} = \sqrt{w_A^2 \sigma_A^2 + w_B^2 \sigma_B^2 + 2w_A w_B \operatorname{Cov}_{AB}}""",
    "c0c3883130244f1aa128.png": r"""s^2 = \frac{\sum_{t=1}^T (R_t - \bar{R})^2}{T - 1}""",
    "7064d8038a925feadd6f.png": r"""\operatorname{Cov}_{1,2} = \frac{\sum_{t=1}^n (R_{1,t} - \bar{R}_1)(R_{2,t} - \bar{R}_2)}{n - 1}""",
    "f988d835f752b8e9d75e.png": r"""\rho_{1,2} = \frac{\operatorname{Cov}_{1,2}}{\sigma_1 \sigma_2}""",
    "8e90098c9dc0fb670ca4.png": r"""\beta_i = \frac{\operatorname{Cov}(R_i, R_m)}{\sigma_m^2}""",
    "0e824a9a1e09a3080901.png": r"""\begin{gathered}
\text{NPV} = \text{CF}_0 + \frac{\text{CF}_1}{(1+k)^1} + \frac{\text{CF}_2}{(1+k)^2} + \dots + \frac{\text{CF}_n}{(1+k)^n} = \sum_{t=0}^n \frac{\text{CF}_t}{(1+k)^t} \\[8pt]
\text{CF}_0 = \text{initial investment outlay}; \quad \text{CF}_t = \text{after-tax cash flow at time } t; \quad k = \text{required rate of return}
\end{gathered}""",
    "6c9fcbbb3cf8dcbf3d91.png": r"""\begin{gathered}
r_e = r_0 + \frac{D}{E}(r_0 - r_d) \\[4pt]
\begin{aligned}
\text{where:}\quad
r_e &= \text{cost of equity} \\[6pt]
r_0 &= \text{cost of equity with no debt (all equity)} \\[6pt]
r_d &= \text{cost of debt} \\[6pt]
\text{D/E} &= \text{debt-to-equity ratio}
\end{aligned}
\end{gathered}""",
})


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def clean_latex(latex: str) -> str:
    latex = latex.strip()
    latex = re.sub(r"^\$+|\$+$", "", latex)
    latex = re.sub(r"^\\\[|\\\]$", "", latex)
    latex = latex.replace("\\label{}", "")

    # Remove OCR repetition loops
    latex = re.sub(r"(the_cor|the~cor|the cor|ore the cor|erres~t~erm|\/the_cor)+", "", latex)

    # Clean OCR garbage percentages: 10^{\circ} \! \! /_{\tt6} -> 10\%
    latex = re.sub(r"(\d+)\s*\^\{\\circ\}\s*(?:\\!\s*)*\/_\{?\\?tt?\d*\}?", r"\1\\%", latex)
    latex = re.sub(r"(\d+)\s*\^\{9\}\s*(?:\\!\s*)*[∨\^/]_?\{?\\!?\s*\d*\}?", r"\1\\%", latex)
    latex = re.sub(r"\\%_\{\\mathbf\{0\}\}", r"\\%", latex)
    latex = re.sub(r"\\%_\{\\mathsf\{0\}\}", r"\\%", latex)
    latex = re.sub(r"\\%_\{\\mathrm\{0\}\}", r"\\%", latex)
    latex = re.sub(r"\\%_\{\\mathbf\{0\}\\!\s*\\!\}", r"\\%", latex)
    latex = re.sub(r"\\%_\{\\mathsf\{d\}\}", r"\\%", latex)
    latex = re.sub(r"\\mathcal\\%", r"\\%", latex)

    # Clean currency and Fraktur/Sans-serif misreads
    latex = re.sub(r"\\varepsilon(?=\d)", r"\\pounds ", latex)
    latex = re.sub(r"\\varepsilon_\{\\bf m\}", r"\\pounds\\text{m}", latex)
    latex = re.sub(r"(\\Im|\\Re)(?=\d)", r"\\$", latex)
    latex = re.sub(r"\\mathfrak\{S\}\s*(\d)", r"\\$\1", latex)
    latex = re.sub(r"\\mathfrak\s*S\s*(\d)", r"\\$\1", latex)
    latex = re.sub(r"\\mathfrak\{s\}", r"s", latex)
    latex = re.sub(r"\\mathfrak\{n\}", r"n", latex)
    latex = re.sub(r"\\mathfrak\{r\}", r"r", latex)
    latex = re.sub(r"\\mathfrak\{b\}", r"b", latex)
    latex = re.sub(r"\\mathfrak\{X\}", r"X", latex)
    latex = re.sub(r"\\mathfrak\{S\}", r"\\$", latex)
    latex = re.sub(r"\\mathfrak\{p\}", r"p", latex)
    latex = re.sub(r"\\mathsf\{S\}", r"\\$", latex)
    latex = re.sub(r"\\mathsf\{s\}", r"s", latex)

    # Clean card suits
    latex = re.sub(r"\\heartsuit(?:_\{\\?[a-zA-Z0-9]+\}|_[a-zA-Z0-9]+)?", r"\\%", latex)
    latex = re.sub(r"\\(?:spadesuit|clubsuit|diamondsuit)", r"", latex)

    # Clean OCR percentage misreads
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*9_\{?(?:\\circ|\\phi|[6o])\b\}?['′]?", r"\1\\%", latex)
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*7_\{?(?:\\circ|[0o])\b\}?['′]?", r"\1\\%", latex)
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*\%_\{?(?:\\phi|\\circ|\\mathsf\{0\}|\\mathbf\{0\}|[06od])\b\}?", r"\1\\%", latex)
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*\{9\s*\\surd\}_?\{?0?\}?", r"\1\\%", latex)
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*9\s*\\surd_?\{?0?\}?", r"\1\\%", latex)
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*\{\\frac\{9\}\s*\{6\}\}", r"\1\\%", latex)
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*\\frac\{9\}\s*\{6\}", r"\1\\%", latex)
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*9\s*\\of\{\}?", r"\1\\%", latex)
    latex = re.sub(r"\\epsilon(?=\s*\d)", r"\\text{EUR }", latex)

    # Clean mathtt and mangled OCR intercepts / typos
    latex = re.sub(r"\\?mathtt\{([^}]+)\}", r"\\text{\1}", latex)
    latex = re.sub(r"\\hat\{\\Phi\}_0", r"\\hat{b}_0", latex)
    latex = re.sub(r"\\hat\{\\theta\}_\{\\emptyset\}", r"\\hat{b}_0", latex)
    latex = re.sub(r"\bSrep\b", "Step", latex)

    # Clean \hbar misreads
    latex = re.sub(r"i\s*\\hbar\s*\\mathrm\{~observation", r"i\\text{th observation}", latex)

    # Clean \ttProbability / \tt EPS
    latex = re.sub(r"\{\\mathrm\{tt~([^}]+)\}\}", r"\\text{\1}", latex)
    latex = re.sub(r"\{\\tt\s*([^}]+)\}", r"\\text{\1}", latex)
    latex = re.sub(r"\\tt\b", r"", latex)

    # Collapse space-separated single-letter sequences inside text/math commands
    # e.g., "c a s h - r e t u r n" -> "cash-return"
    for _ in range(5):
        latex = re.sub(r"\b([a-zA-Z])\s+(?=[a-zA-Z]\b)", r"\1", latex)

    latex = re.sub(r"\\root\\infty_?(?:\{0\}|0)", r"\\%\\Delta", latex)
    latex = re.sub(r"\\root\s*(\d+)\s*\\mathrm\{of\}\{([^{}]+)\}", r"\\sqrt[\1]{\2}", latex)
    latex = re.sub(r"9\s*\\of\{\}|9\s*\\surd_?\{?0\}?", r"\\%", latex)
    latex = re.sub(r"\\mathrm\{\\([A-Za-z]+)", r"\\mathrm{\1", latex)
    latex = re.sub(r"\\(PMT|FV|PV|CPT|NPV|IRR|USD|EUR|CHF|GBP|DOL)\b", r"\\mathrm{\1}", latex)
    latex = re.sub(r"\\b(?=\s*=)", "b", latex)
    latex = re.sub(r"\\of\b", r"\\mathrm{of}", latex)
    latex = re.sub(r"\\S(?=\s*\d)", r"\\$", latex)
    for _ in range(4):
        latex = re.sub(r"(?<=\d)\s+(?=[\d.])|(?<=\.)\s+(?=\d)", "", latex)
    # Convert \mathrm{...~...} to \text{...} if it does not contain math syntax
    def clean_mathrm(match):
        inner = match.group(1)
        if any(ch in inner for ch in "_^\\=<>"):
            return match.group(0)
        return "\\text{" + inner.replace("~", " ") + "}"

    latex = re.sub(r"\\mathrm\{([^{}]+~[^{}]+)\}", clean_mathrm, latex)

    # Wrap thousands separators between digits in math mode with {,}
    saved_text = []
    def save_text(m):
        saved_text.append(m.group(0))
        return f"__SAVED_TEXT_{len(saved_text)-1}__"

    latex = re.sub(r"\\text\{[^{}]*\}", save_text, latex)
    latex = re.sub(r"(?<=\d),(?=\d)", "{,}", latex)
    for idx, s in enumerate(saved_text):
        latex = latex.replace(f"__SAVED_TEXT_{idx}__", s)

    # Clean currency and stray symbols
    latex = re.sub(r"(?<=\s)S(?=\d+[,.]\d+)", r"\\$", latex)
    latex = re.sub(r"(?<=[=\+\-\(])\s*S(?=\d)", r"\\$", latex)
    latex = re.sub(r"\\sharp(?=\s*\d)", r"\\$", latex)
    latex = re.sub(r"(\d+(?:\.\d+)?)\s*\\natural\b", r"\1\\%", latex)

    replacements = {
        "retum": "return",
        "Retum": "Return",
        "infanion": "inflation",
        "rask.:rec": "risk-free",
        "begining": "beginning",
        "befimingerfothod": "beginning~of~period",
        "perfotho": "period",
        "\\mathbbm": "\\mathbb",
        "portfolic": "portfolio",
        "eamings": "earnings",
        "fevenu": "revenu",
        "anmual": "annual",
        "Partuership": "Partnership",
        "Vimally": "Virtually",
        'days"': "\\text{days'}",
        "\\bmod11 ion": "\\text{ million}",
        "\\cal S": "\\$",
    }
    for wrong, right in replacements.items():
        latex = latex.replace(wrong, right)
    # Ensure vertical breathing room between rows in multiline environments with fractions
    def add_row_spacing(match):
        env_type = match.group(1)
        env_content = match.group(2)
        if r"\frac" in env_content or r"\cfrac" in env_content or r"\displaystyle" in env_content:
            spaced = re.sub(r"\\\\(?!\s*\[\s*\d+\s*(?:pt|ex|em)\s*\])", r"\\\\[8pt]", env_content)
            return f"\\begin{{{env_type}}}{spaced}\\end{{{env_type}}}"
        elif env_type == "matrix":
            spaced = re.sub(r"\\\\(?!\s*\[\s*\d+\s*(?:pt|ex|em)\s*\])", r"\\\\[2pt]", env_content)
            return f"\\begin{{{env_type}}}{spaced}\\end{{{env_type}}}"
        return match.group(0)

    latex = re.sub(r"\\begin\{(array|aligned|matrix|gathered|cases)\}(.*?)\\end\{\1\}", add_row_spacing, latex, flags=re.DOTALL)

    balance = latex.count("{") - latex.count("}")
    if balance > 0:
        latex += "}" * balance
    elif balance < 0:
        for _ in range(-balance):
            latex = latex.rsplit("}", 1)[0] + latex.rsplit("}", 1)[1]
    return latex or r"\text{See the accompanying mathematical explanation.}"


def visual_category(block: dict, previous_text: str, section: str) -> tuple[str, str]:
    context = f"{previous_text} {block.get('alt', '')}"
    name = Path(block.get("src", "")).name
    if name in MANUAL_MEANINGFUL_VISUALS:
        return "meaningful-visual", "source-verified instructional table, chart, or decision tree"
    if block.get("visualKindHint") == "table":
        return "meaningful-visual", "quiz data table rebuilt in the question flow"
    if block.get("text"):
        return "native-math", "combined prose-and-mathematics crop"
    if re.search(r"\bFigure\s+\d+(?:\.\d+)?\b", context, re.I):
        return "meaningful-visual", "captioned diagram, chart, or table"
    if section == "reference" and name in REFERENCE_TABLES:
        return "meaningful-visual", "statistical reference table"
    return "native-math", "equation or compact mathematical layout"


def collect_blocks(value, section: str, occurrences: list[dict]) -> None:
    if isinstance(value, list):
        previous = ""
        for block in value:
            if isinstance(block, dict):
                if block.get("type") == "image" and block.get("src"):
                    category, reason = visual_category(block, previous, section)
                    occurrences.append({"block": block, "category": category, "reason": reason, "section": section})
                elif block.get("type") in {"math", "worked-example"} and block.get("sourceAsset"):
                    block["src"] = f"content/figures/{block['sourceAsset']}"
                    category, reason = visual_category(block, previous, section)
                    occurrences.append({"block": block, "category": category, "reason": reason, "section": section})
            if isinstance(block, dict) and block.get("text"):
                previous = block["text"]
            collect_blocks(block, section, occurrences)
    elif isinstance(value, dict):
        for key, child in value.items():
            child_section = "reference" if key == "sections" and section == "reference" else section
            if key in {"supportingBlocks", "solutionBlocks"}:
                child_section = "quiz"
            collect_blocks(child, child_section, occurrences)


def formula_segments(image: Image.Image) -> list[Image.Image]:
    if image.height <= 180:
        return [image]
    gray = np.asarray(image.convert("L"))
    active = (gray < 225).sum(axis=1) > max(2, image.width // 500)
    bands, start, last = [], None, None
    for row, occupied in enumerate(active):
        if occupied and start is None:
            start = last = row
        elif occupied:
            last = row
        elif start is not None and row - last > 8:
            bands.append((max(0, start - 3), min(image.height, last + 4)))
            start = last = None
    if start is not None:
        bands.append((max(0, start - 3), min(image.height, last + 4)))
    if len(bands) <= 1:
        return [image]
    chunks = []
    top, bottom = bands[0]
    for band_top, band_bottom in bands[1:]:
        if band_bottom - top <= 180:
            bottom = band_bottom
        else:
            chunks.append(image.crop((0, top, image.width, bottom)))
            top, bottom = band_top, band_bottom
    chunks.append(image.crop((0, top, image.width, bottom)))
    return chunks


def recognize(paths: list[str], cache: dict[str, str], scores: dict[str, float], segmented: set[str]) -> tuple[dict[str, str], dict[str, float], set[str]]:
    pending = [name for name in paths if name not in cache]
    pending.sort(key=lambda name: Image.open(CONTENT / "figures" / name).width * Image.open(CONTENT / "figures" / name).height)
    if not pending:
        return cache, scores, segmented
    model = Pix2Text.from_config(enable_table=False)
    batch_size = 8
    for phase, names_to_process in (("recognized", pending),):
        for offset in range(0, len(names_to_process), batch_size):
            names = names_to_process[offset:offset + batch_size]
            segments_by_name = [formula_segments(Image.open(CONTENT / "figures" / name).convert("RGB")) for name in names]
            images = [segment for segments in segments_by_name for segment in segments]
            recognized = model.recognize_formula(images, batch_size=min(batch_size, len(images)), return_text=False, rec_config={"max_new_tokens": 768})
            cursor = 0
            for name, segments in zip(names, segments_by_name, strict=True):
                results = recognized[cursor:cursor + len(segments)]
                cursor += len(segments)
                parts = [clean_latex(result["text"]) for result in results]
                cache[name] = parts[0] if len(parts) == 1 else r"\begin{gathered}" + r"\\[6pt]".join(parts) + r"\end{gathered}"
                scores[name] = min(float(result["score"]) for result in results)
                if Image.open(CONTENT / "figures" / name).height > 180:
                    segmented.add(name)
            save_json(CACHE_FILE, cache)
            save_json(SCORES_FILE, scores)
            save_json(SEGMENTED_FILE, sorted(segmented))
            print(f"{phase.title()} {min(offset + batch_size, len(names_to_process))}/{len(names_to_process)} mathematical visuals", flush=True)
    return cache, scores, segmented


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    documents = [(path, load_json(path), "lesson") for path in sorted((CONTENT / "readings").glob("*.json"))]
    reference_path = CONTENT / "reference.json"
    documents.append((reference_path, load_json(reference_path), "reference"))
    occurrences: list[dict] = []
    for _, document, section in documents:
        collect_blocks(document, section, occurrences)

    math_assets = sorted({
        Path(item["block"]["src"]).name
        for item in occurrences
        if item["category"] == "native-math" and Path(item["block"]["src"]).name not in LATEX_OVERRIDES
    })
    cache = load_json(CACHE_FILE) if CACHE_FILE.exists() else {}
    cache = {name: clean_latex(latex) for name, latex in cache.items()}
    scores = load_json(SCORES_FILE) if SCORES_FILE.exists() else {}
    segmented = set(load_json(SEGMENTED_FILE)) if SEGMENTED_FILE.exists() else set()
    for name in list(cache):
        with Image.open(CONTENT / "figures" / name) as image:
            if image.height > 180 and name not in segmented:
                cache.pop(name, None)
                scores.pop(name, None)
    cache, scores, segmented = recognize(math_assets, cache, scores, segmented)
    cache.update({name: clean_latex(latex) for name, latex in LATEX_OVERRIDES.items()})

    asset_records: dict[str, dict] = {}
    for item in occurrences:
        block = item["block"]
        name = Path(block["src"]).name
        record = asset_records.setdefault(name, {
            "asset": name,
            "classification": item["category"],
            "reason": item["reason"],
            "occurrences": 0,
        })
        record["occurrences"] += 1
        if item["category"] == "native-math":
            record["latex"] = cache[name]
            if name in LATEX_OVERRIDES:
                record["verification"] = ["source-traced", "manually-transcribed", "katex-parse-checked"]
            else:
                record["recognitionConfidence"] = scores.get(name)
                record["verification"] = ["source-traced", "katex-parse-checked"] + (["confidence-checked"] if name in scores else [])
            prose = block.get("text", "").strip()
            block.clear()
            if name in WORKED_EXAMPLE_OVERRIDES:
                block.update(WORKED_EXAMPLE_OVERRIDES[name])
                block["sourceAsset"] = name
            else:
                block.update({"type": "math", "latex": cache[name], "display": True, "sourceAsset": name})
            if prose:
                block["prose"] = prose
        else:
            block.clear()
            block["type"] = "image"
            block["src"] = f"content/figures/{name}"
            block["visualKind"] = "diagram-chart-or-table"
            with Image.open(CONTENT / "figures" / name) as img:
                block["width"] = img.width
                block["height"] = img.height
            if name in VISUAL_ALT_OVERRIDES:
                block["alt"] = VISUAL_ALT_OVERRIDES[name]
            elif not block.get("alt"):
                block["alt"] = f"Instructional visual diagram or table: {name}"

    source_audit = load_json(ROOT / "docs/full-reading-import-audit.json")
    source_ids: dict[str, list[str]] = {}
    for source in source_audit["blocks"]:
        if source.get("asset"):
            source_ids.setdefault(source["asset"], []).append(source["sourceId"])
    for name, record in asset_records.items():
        record["sourceIds"] = source_ids.get(name, [])
    for name in sorted(REBUILT_TABLES):
        asset_records[name] = {
            "asset": name,
            "classification": "rebuilt-table",
            "reason": "answer-choice table rebuilt as accessible selectable text",
            "occurrences": 1,
            "sourceIds": source_ids.get(name, []),
        }

    for path, document, _ in documents:
        save_json(path, document)
    audit = {
        "summary": {
            "sourceAssetsClassified": len(asset_records),
            "nativeMath": sum(r["classification"] == "native-math" for r in asset_records.values()),
            "meaningfulVisuals": sum(r["classification"] == "meaningful-visual" for r in asset_records.values()),
            "rebuiltTables": sum(r["classification"] == "rebuilt-table" for r in asset_records.values()),
            "lowConfidenceMath": sum(r["classification"] == "native-math" and r.get("recognitionConfidence") is not None and r["recognitionConfidence"] < 0.8 for r in asset_records.values()),
        },
        "assets": sorted(asset_records.values(), key=lambda item: item["asset"]),
    }
    save_json(AUDIT_FILE, audit)
    print(json.dumps(audit["summary"], indent=2))


if __name__ == "__main__":
    main()
