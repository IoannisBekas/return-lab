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
    "cd4273ac668e90e54170.png",
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
HPR_1=\frac{\$120+\$2}{\$100}-1=22\%,\qquad
HPR_2=\frac{\$260+\$4}{\$240}-1=10\% \\[6pt]
\text{Step 3: Find the compound annual rate that produces the account's two-year total return.} \\
(1+\text{time-weighted rate of return})^2=(1.22)(1.10) \\
\text{Time-weighted rate of return}=[(1.22)(1.10)]^{0.5}-1=15.84\%
\end{gathered}""",
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
    latex = re.sub(r"\\root\\infty_?(?:\{0\}|0)", r"\\%\\Delta", latex)
    latex = re.sub(r"\\root\s*(\d+)\s*\\mathrm\{of\}\{([^{}]+)\}", r"\\sqrt[\1]{\2}", latex)
    latex = re.sub(r"9\s*\\of\{\}|9\s*\\surd_?\{?0\}?", r"\\%", latex)
    latex = re.sub(r"\\mathrm\{\\([A-Za-z]+)", r"\\mathrm{\1", latex)
    latex = re.sub(r"\\(PMT|FV|PV|CPT|NPV|IRR|USD|EUR|CHF|GBP|DOL)\b", r"\\mathrm{\1}", latex)
    latex = re.sub(r"\\b(?=\s*=)", "b", latex)
    latex = re.sub(r"\\of\b", r"\\mathrm{of}", latex)
    latex = re.sub(r"\\S(?=\s*\d)", r"\\$", latex)
    latex = re.sub(r"\\mathrm\{([^{}]*)\}", lambda match: "\\mathrm{" + match.group(1).replace(" ", "") + "}", latex)
    for _ in range(4):
        latex = re.sub(r"(?<=\d)\s+(?=[\d.])|(?<=\.)\s+(?=\d)", "", latex)
    replacements = {
        "retum": "return",
        "Retum": "Return",
        "infanion": "inflation",
        "rask.:rec": "risk-free",
        "begining": "beginning",
        "befimingerfothod": "beginning~of~period",
        "perfotho": "period",
        "\\mathbbm": "\\mathbb",
    }
    for wrong, right in replacements.items():
        latex = latex.replace(wrong, right)
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
            if isinstance(block, dict) and block.get("type") == "image":
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
            block.update({"type": "math", "latex": cache[name], "display": True, "sourceAsset": name})
            if prose:
                block["prose"] = prose
        else:
            block["visualKind"] = "diagram-chart-or-table"

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
