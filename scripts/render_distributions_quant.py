import fitz
import numpy as np

def render_0a3a():
    # Figure 6.1: Normal vs. Lognormal Distributions (2155 x 840)
    w, h = 2155, 840
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  
  <!-- Left Card: Normal Distribution -->
  <rect x="40" y="40" width="1010" height="760" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  <text x="545" y="100" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Normal Distribution (Symmetric)</text>
  <text x="545" y="140" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Defined from –∞ to +∞ (Can take negative values)</text>
  
  <!-- Axes -->
  <line x1="120" y1="680" x2="980" y2="680" stroke="#0f172a" stroke-width="4" />
  <line x1="545" y1="680" x2="545" y2="200" stroke="#94a3b8" stroke-width="3" stroke-dasharray="6 6" />
  <text x="545" y="725" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Mean = Median = Mode (μ)</text>
  <text x="960" y="725" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="end">+∞</text>
  <text x="140" y="725" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26">–∞</text>
  
  <!-- Bell Curve -->
  <path d="M 140 675 C 320 675 420 230 545 230 C 670 230 770 675 960 675" fill="none" stroke="#0284c7" stroke-width="6" />
  <path d="M 140 675 C 320 675 420 230 545 230 C 670 230 770 675 960 675 Z" fill="#0284c7" fill-opacity="0.08" />
  <text x="750" y="320" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Skewness = 0</text>
  
  <!-- Right Card: Lognormal Distribution -->
  <rect x="1105" y="40" width="1010" height="760" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  <text x="1610" y="100" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Lognormal Distribution (Positively Skewed)</text>
  <text x="1610" y="140" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Bounded below by 0 (Ideal for Asset Prices: S_t ≥ 0)</text>
  
  <!-- Axes -->
  <line x1="1180" y1="680" x2="2040" y2="680" stroke="#0f172a" stroke-width="4" />
  <line x1="1200" y1="680" x2="1200" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="1200" y="725" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">0 (Lower Bound)</text>
  <text x="2020" y="725" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="end">+∞</text>
  
  <!-- Lognormal Curve -->
  <path d="M 1205 675 C 1240 650 1320 220 1420 220 C 1540 220 1680 620 2020 670" fill="none" stroke="#0284c7" stroke-width="6" />
  <path d="M 1205 675 C 1240 650 1320 220 1420 220 C 1540 220 1680 620 2020 670 L 1205 680 Z" fill="#0284c7" fill-opacity="0.08" />
  
  <!-- Mode, Median, Mean markers -->
  <line x1="1400" y1="680" x2="1400" y2="230" stroke="#e11d48" stroke-width="3" stroke-dasharray="5 5" />
  <line x1="1480" y1="680" x2="1480" y2="300" stroke="#d97706" stroke-width="3" stroke-dasharray="5 5" />
  <line x1="1580" y1="680" x2="1580" y2="400" stroke="#059669" stroke-width="3" stroke-dasharray="5 5" />
  <text x="1400" y="760" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Mode</text>
  <text x="1480" y="725" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Median</text>
  <text x="1580" y="760" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Mean</text>
  <text x="1750" y="320" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Mode &lt; Median &lt; Mean</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/0a3a511844bb550d3ed8.png")
    print(f"Saved 0a3a511844bb550d3ed8.png ({pix.width}x{pix.height})")

def render_1136():
    # Student's t-distribution curve with df=38 showing two-tailed ±2.024 (1685 x 1220)
    w, h = 1685, 1220
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1585" height="1120" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="842" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Two-Tailed Hypothesis Test: t-Distribution (df = 38)</text>
  <text x="842" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Significance Level α = 0.05 | Critical t-values = ±2.024</text>
  
  <!-- Axis -->
  <line x1="120" y1="920" x2="1565" y2="920" stroke="#0f172a" stroke-width="5" />
  <line x1="842" y1="920" x2="842" y2="280" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />
  <text x="842" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">0</text>
  <text x="842" y="1015" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Mean of t-distribution</text>
  
  <!-- Central Non-rejection Region Fill -->
  <!-- t-curve coordinates -->
  <!-- Left rejection: x=150 to x=460. Center: x=460 to x=1224. Right rejection: x=1224 to x=1535 -->
  <!-- Rejection left shade -->
  <path d="M 150 918 C 240 915 380 890 460 760 L 460 920 L 150 920 Z" fill="#ef4444" fill-opacity="0.25" />
  <!-- Rejection right shade -->
  <path d="M 1224 760 C 1304 890 1444 915 1535 918 L 1535 920 L 1224 920 Z" fill="#ef4444" fill-opacity="0.25" />
  <!-- Non-rejection shade -->
  <path d="M 460 760 C 580 560 720 320 842 320 C 964 320 1104 560 1224 760 L 1224 920 L 460 920 Z" fill="#0284c7" fill-opacity="0.1" />
  
  <!-- The Curve -->
  <path d="M 150 918 C 300 910 520 660 720 380 C 780 320 842 320 842 320 C 842 320 904 320 964 380 C 1164 660 1384 910 1535 918" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Critical lines -->
  <line x1="460" y1="920" x2="460" y2="760" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  <line x1="1224" y1="920" x2="1224" y2="760" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  
  <!-- Critical value labels -->
  <text x="460" y="970" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">–2.024</text>
  <text x="1224" y="970" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">+2.024</text>
  <text x="460" y="1015" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Lower Critical Value</text>
  <text x="1224" y="1015" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Upper Critical Value</text>
  
  <!-- Region text boxes -->
  <text x="300" y="840" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="300" y="875" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Area = 0.025 (α/2)</text>
  
  <text x="1380" y="840" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="1380" y="875" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Area = 0.025 (α/2)</text>
  
  <text x="842" y="580" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Fail to Reject H₀</text>
  <text x="842" y="630" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="middle">Confidence Level = 0.95 (1 – α)</text>
  
  <!-- Decision Rule box -->
  <rect x="250" y="1060" width="1185" height="75" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="842" y="1110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Decision Rule: Reject H₀ if test statistic &lt; –2.024 or test statistic &gt; +2.024</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/11369a9311fe8de699f7.png")
    print(f"Saved 11369a9311fe8de699f7.png ({pix.width}x{pix.height})")

def render_1f29():
    # Chi-squared distribution curve with df=23 showing 11.689 and 38.076 (1747 x 1352)
    w, h = 1747, 1352
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1647" height="1252" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="873" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Chi-Square (χ²) Test of a Single Variance (df = 23)</text>
  <text x="873" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Two-Tailed Test at α = 0.05 | Asymmetric Rejection Regions</text>
  
  <!-- Axis -->
  <line x1="140" y1="1020" x2="1620" y2="1020" stroke="#0f172a" stroke-width="5" />
  <line x1="160" y1="1020" x2="160" y2="300" stroke="#0f172a" stroke-width="4" />
  <text x="160" y="1065" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">0</text>
  <text x="160" y="270" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">f(χ²)</text>
  
  <!-- Chi-squared curve df=23: peaks around x=21, asymmetric right skew -->
  <!-- Left rejection (0 to 11.689): x=160 to x=420 -->
  <!-- Center non-rejection (11.689 to 38.076): x=420 to x=1250 -->
  <!-- Right rejection (> 38.076): x=1250 to x=1580 -->
  <path d="M 160 1020 C 220 1020 320 850 420 620 L 420 1020 Z" fill="#ef4444" fill-opacity="0.25" />
  <path d="M 420 620 C 520 380 650 320 750 320 C 950 320 1150 550 1250 820 L 1250 1020 L 420 1020 Z" fill="#0284c7" fill-opacity="0.1" />
  <path d="M 1250 820 C 1350 930 1480 1000 1580 1018 L 1580 1020 L 1250 1020 Z" fill="#ef4444" fill-opacity="0.25" />
  
  <!-- Curve Stroke -->
  <path d="M 160 1020 C 220 1020 320 850 420 620 C 520 380 650 320 750 320 C 950 320 1150 550 1250 820 C 1350 930 1480 1000 1580 1018" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Critical boundary lines -->
  <line x1="420" y1="1020" x2="420" y2="620" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  <line x1="1250" y1="1020" x2="1250" y2="820" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  
  <!-- Critical values -->
  <text x="420" y="1065" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">11.689</text>
  <text x="420" y="1110" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">χ²_0.975 (Lower Critical)</text>
  
  <text x="1250" y="1065" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">38.076</text>
  <text x="1250" y="1110" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">χ²_0.025 (Upper Critical)</text>
  
  <!-- Labels -->
  <text x="300" y="900" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="300" y="940" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Area = 0.025</text>
  
  <text x="1420" y="920" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="1420" y="960" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Area = 0.025</text>
  
  <text x="820" y="580" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Fail to Reject H₀</text>
  <text x="820" y="630" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="middle">Confidence Region = 0.95</text>
  
  <!-- Decision Rule box -->
  <rect x="250" y="1180" width="1247" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="873" y="1235" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Decision Rule: Reject H₀ if χ² &lt; 11.689 or χ² &gt; 38.076</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/1f29a430552ac9b5702b.png")
    print(f"Saved 1f29a430552ac9b5702b.png ({pix.width}x{pix.height})")

def render_510d():
    # F-distribution curve df=(30, 40) showing upper 2.5% rejection region F > 1.94 (1475 x 1305)
    w, h = 1475, 1305
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1375" height="1205" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="737" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">F-Distribution: Test of Equal Variances</text>
  <text x="737" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">df₁ = 30, df₂ = 40 | Upper Critical Value F = 1.94</text>
  
  <!-- Axis -->
  <line x1="120" y1="980" x2="1355" y2="980" stroke="#0f172a" stroke-width="5" />
  <line x1="150" y1="980" x2="150" y2="280" stroke="#0f172a" stroke-width="4" />
  <text x="150" y="1030" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">0</text>
  <text x="150" y="250" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">f(F)</text>
  
  <!-- F curve: peaks at ~1.0, right-skewed -->
  <!-- Non-rejection (0 to 1.94): x=150 to x=950 -->
  <!-- Rejection (> 1.94): x=950 to x=1300 -->
  <path d="M 150 980 C 200 980 300 450 480 350 C 650 250 820 500 950 800 L 950 980 L 150 980 Z" fill="#0284c7" fill-opacity="0.1" />
  <path d="M 950 800 C 1050 900 1180 965 1300 978 L 1300 980 L 950 980 Z" fill="#ef4444" fill-opacity="0.25" />
  
  <path d="M 150 980 C 200 980 300 450 480 350 C 650 250 820 500 950 800 C 1050 900 1180 965 1300 978" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Rejection line -->
  <line x1="950" y1="980" x2="950" y2="800" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  <text x="950" y="1030" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">1.94</text>
  <text x="950" y="1075" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Critical Value (F_c)</text>
  
  <!-- Rejection Region Label -->
  <text x="1140" y="880" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="1140" y="920" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Area = 0.025</text>
  
  <!-- Non-rejection Label -->
  <text x="560" y="600" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Fail to Reject H₀</text>
  <text x="560" y="650" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Area = 0.975</text>
  
  <!-- Calculated F marker -->
  <line x1="680" y1="980" x2="680" y2="480" stroke="#059669" stroke-width="4" />
  <polygon points="680,480 670,500 690,500" fill="#059669" />
  <text x="680" y="440" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Calculated F = 1.28</text>
  
  <!-- Decision box -->
  <rect x="200" y="1130" width="1075" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="737" y="1185" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Decision Rule: Reject H₀ if F &gt; 1.94. Since 1.28 &lt; 1.94, Fail to Reject H₀.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/510d77a276c7184557a9.png")
    print(f"Saved 510d77a276c7184557a9.png ({pix.width}x{pix.height})")

def render_5651():
    # Figure 8.1: Flowchart 7-step hypothesis testing procedure (2492 x 1365)
    w, h = 2492, 1365
    steps = [
        ("Step 1", "State the Hypotheses", "Null hypothesis (H₀) and Alternative hypothesis (H₁)"),
        ("Step 2", "Identify the Test Statistic", "Select appropriate statistic (z, t, χ², or F)"),
        ("Step 3", "Specify the Level of Significance", "Determine α (e.g., 0.05, 0.01) based on risk"),
        ("Step 4", "State the Decision Rule", "Establish critical values and rejection regions"),
        ("Step 5", "Collect Data & Compute Statistic", "Calculate sample value from observed empirical data"),
        ("Step 6", "Make the Statistical Decision", "Reject H₀ or Fail to Reject H₀"),
        ("Step 7", "Make the Economic / Investment Decision", "Translate statistical outcome into actionable strategy")
    ]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2392" height="1265" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1246" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 8.1: Seven Steps in Hypothesis Testing</text>
  <text x="1246" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">The systematic scientific framework for financial hypothesis formulation and empirical testing</text>
"""
    # 7 steps layout: 4 on top row, 3 on bottom row with curved connector
    # Top row: 4 cards
    xs_top = [100, 680, 1260, 1840]
    for i in range(4):
        x = xs_top[i]
        s_num, s_title, s_desc = steps[i]
        svg += f"""
  <rect x="{x}" y="260" width="530" height="340" fill="#f8fafc" stroke="#0284c7" stroke-width="3" rx="16" />
  <rect x="{x}" y="260" width="530" height="70" fill="#0284c7" rx="16" />
  <rect x="{x}" y="310" width="530" height="20" fill="#0284c7" />
  <text x="{x + 265}" y="308" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">{s_num}</text>
  <text x="{x + 265}" y="390" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">{s_title}</text>
  <foreignObject x="{x + 30}" y="420" width="470" height="160">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 22px; color: #475569; text-align: center; line-height: 1.4;">
      {s_desc}
    </div>
  </foreignObject>
"""
        if i < 3:
            # arrow right
            svg += f"""
  <line x1="{x + 530}" y1="430" x2="{xs_top[i+1]}" y2="430" stroke="#0284c7" stroke-width="4" marker-end="url(#arrow)" />
  <polygon points="{xs_top[i+1]},430 {xs_top[i+1]-16},420 {xs_top[i+1]-16},440" fill="#0284c7" />
"""
    
    # Down arrow from step 4 to step 5
    svg += f"""
  <path d="M 2105 600 L 2105 690 L 1950 690 L 1950 760" fill="none" stroke="#0284c7" stroke-width="4" />
  <polygon points="1950,760 1940,744 1960,744" fill="#0284c7" />
"""

    # Bottom row: 3 cards right-to-left or left-to-right (Step 5, 6, 7)
    xs_bot = [1680, 1000, 320]
    for j in range(3):
        idx = 4 + j
        x = xs_bot[j]
        s_num, s_title, s_desc = steps[idx]
        is_final = (idx == 6)
        border_col = "#059669" if is_final else "#0284c7"
        head_col = "#059669" if is_final else "#0284c7"
        svg += f"""
  <rect x="{x}" y="760" width="550" height="340" fill="#f8fafc" stroke="{border_col}" stroke-width="3" rx="16" />
  <rect x="{x}" y="760" width="550" height="70" fill="{head_col}" rx="16" />
  <rect x="{x}" y="810" width="550" height="20" fill="{head_col}" />
  <text x="{x + 275}" y="808" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">{s_num}</text>
  <text x="{x + 275}" y="890" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">{s_title}</text>
  <foreignObject x="{x + 30}" y="920" width="490" height="160">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 22px; color: #475569; text-align: center; line-height: 1.4;">
      {s_desc}
    </div>
  </foreignObject>
"""
        if j < 2:
            # arrow left from xs_bot[j] to xs_bot[j+1]
            svg += f"""
  <line x1="{x}" y1="930" x2="{xs_bot[j+1] + 550}" y2="930" stroke="#0284c7" stroke-width="4" />
  <polygon points="{xs_bot[j+1] + 550},930 {xs_bot[j+1] + 566},920 {xs_bot[j+1] + 566},940" fill="#0284c7" />
"""

    svg += """
  <!-- Bottom banner -->
  <rect x="100" y="1180" width="2292" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1246" y="1235" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Hypothesis testing requires formulating H₀ and H₁ prior to examining sample data to prevent data snooping bias.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/56512ee0e05d283785ae.png")
    print(f"Saved 56512ee0e05d283785ae.png ({pix.width}x{pix.height})")

def render_6224():
    # Figure 8.2: Standard normal distribution bell curve showing two-tailed ±1.96 (1550 x 985)
    w, h = 1550, 985
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1450" height="885" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="775" y="120" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 8.2: Two-Tailed Hypothesis Test (Standard Normal z-Distribution)</text>
  <text x="775" y="165" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Significance Level α = 0.05 | Critical z-values = ±1.96</text>
  
  <!-- Axis -->
  <line x1="120" y1="720" x2="1430" y2="720" stroke="#0f172a" stroke-width="5" />
  <line x1="775" y1="720" x2="775" y2="240" stroke="#94a3b8" stroke-width="3" stroke-dasharray="6 6" />
  <text x="775" y="765" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">0</text>
  <text x="775" y="805" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">μ = 0 (z-score)</text>
  
  <!-- Shades -->
  <!-- Left rejection: x=140 to x=430 -->
  <path d="M 140 718 C 220 715 350 685 430 560 L 430 720 L 140 720 Z" fill="#ef4444" fill-opacity="0.25" />
  <!-- Right rejection: x=1120 to x=1410 -->
  <path d="M 1120 560 C 1200 685 1330 715 1410 718 L 1410 720 L 1120 720 Z" fill="#ef4444" fill-opacity="0.25" />
  <!-- Center non-rejection -->
  <path d="M 430 560 C 530 400 660 260 775 260 C 890 260 1020 400 1120 560 L 1120 720 L 430 720 Z" fill="#0284c7" fill-opacity="0.1" />
  
  <!-- Bell Curve Line -->
  <path d="M 140 718 C 220 715 350 685 430 560 C 530 400 660 260 775 260 C 890 260 1020 400 1120 560 C 1200 685 1330 715 1410 718" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Critical boundary lines -->
  <line x1="430" y1="720" x2="430" y2="560" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  <line x1="1120" y1="720" x2="1120" y2="560" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  
  <text x="430" y="765" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">–1.96</text>
  <text x="1120" y="765" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">+1.96</text>
  
  <!-- Labels -->
  <text x="280" y="640" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="280" y="675" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Area = 0.025 (α/2)</text>
  
  <text x="1270" y="640" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="1270" y="675" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Area = 0.025 (α/2)</text>
  
  <text x="775" y="470" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Do Not Reject H₀</text>
  <text x="775" y="515" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Non-Rejection Region = 0.95 (1 – α)</text>
  
  <!-- Bottom decision banner -->
  <rect x="200" y="845" width="1150" height="65" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="10" />
  <text x="775" y="888" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Decision: Reject H₀ if test statistic z &lt; –1.96 or z &gt; +1.96</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/62247c76b2a3dfe8951a.png")
    print(f"Saved 62247c76b2a3dfe8951a.png ({pix.width}x{pix.height})")

def render_d08a():
    # Figure 8.6: F-distribution curve showing right-skewed shape, lower bound 0 (1497 x 1315)
    w, h = 1497, 1315
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1397" height="1215" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="748" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 8.6: The F-Distribution</text>
  <text x="748" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Asymmetric, Bounded at Zero, Determined by df₁ and df₂</text>
  
  <!-- Axis -->
  <line x1="120" y1="980" x2="1375" y2="980" stroke="#0f172a" stroke-width="5" />
  <line x1="160" y1="980" x2="160" y2="280" stroke="#0f172a" stroke-width="4" />
  <text x="160" y="1030" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">0</text>
  <text x="160" y="250" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">f(F)</text>
  <text x="1350" y="1030" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">F</text>
  
  <!-- Curve Fill & Path -->
  <!-- Mode around F=1.0 at x=450 -->
  <path d="M 160 980 C 220 980 320 400 480 330 C 650 250 850 540 1020 820 L 1020 980 L 160 980 Z" fill="#0284c7" fill-opacity="0.1" />
  <path d="M 1020 820 C 1120 910 1240 965 1340 978 L 1340 980 L 1020 980 Z" fill="#ef4444" fill-opacity="0.25" />
  
  <path d="M 160 980 C 220 980 320 400 480 330 C 650 250 850 540 1020 820 C 1120 910 1240 965 1340 978" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Critical line -->
  <line x1="1020" y1="980" x2="1020" y2="820" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  <text x="1020" y="1030" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">F_α</text>
  <text x="1020" y="1075" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Critical Value</text>
  
  <!-- Equal variances point: F=1 -->
  <line x1="520" y1="980" x2="520" y2="350" stroke="#64748b" stroke-width="3" stroke-dasharray="5 5" />
  <text x="520" y="1030" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">1.0</text>
  <text x="520" y="1075" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Equal Variances (s₁² = s₂²)</text>
  
  <!-- Rejection label -->
  <text x="1180" y="900" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Rejection Region</text>
  <text x="1180" y="940" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Area = α</text>
  
  <!-- Non-rejection label -->
  <text x="680" y="600" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Non-Rejection Region</text>
  <text x="680" y="650" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Area = 1 – α</text>
  
  <!-- Key Properties Callout -->
  <rect x="180" y="1130" width="1137" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="748" y="1170" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Key Property: F-statistic = s₁² / s₂² (with s₁² ≥ s₂² by convention for one-tailed tests).</text>
  <text x="748" y="1205" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Always non-negative (F ≥ 0). Approaches normal distribution as df₁, df₂ → ∞.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/d08a345f77902d0c0c6d.png")
    print(f"Saved d08a345f77902d0c0c6d.png ({pix.width}x{pix.height})")

def render_ee7f():
    # Student's t-distribution curve with df=120 showing two-tailed ±1.980 (1752 x 1235)
    w, h = 1752, 1235
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1652" height="1135" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="876" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Decision Rule for Two-Tailed t-Test (df = 120)</text>
  <text x="876" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Significance Level α = 0.05 | Critical t-values = ±1.980</text>
  
  <!-- Axis -->
  <line x1="120" y1="920" x2="1632" y2="920" stroke="#0f172a" stroke-width="5" />
  <line x1="876" y1="920" x2="876" y2="280" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />
  <text x="876" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">0</text>
  
  <!-- Shades -->
  <!-- Left rejection: x=140 to x=480 -->
  <path d="M 140 918 C 240 915 390 885 480 750 L 480 920 L 140 920 Z" fill="#ef4444" fill-opacity="0.25" />
  <!-- Right rejection: x=1272 to x=1612 -->
  <path d="M 1272 750 C 1362 885 1512 915 1612 918 L 1612 920 L 1272 920 Z" fill="#ef4444" fill-opacity="0.25" />
  <!-- Center non-rejection -->
  <path d="M 480 750 C 600 550 750 310 876 310 C 1002 310 1152 550 1272 750 L 1272 920 L 480 920 Z" fill="#0284c7" fill-opacity="0.1" />
  
  <path d="M 140 918 C 300 910 520 660 740 370 C 800 310 876 310 876 310 C 876 310 952 310 1012 370 C 1232 660 1452 910 1612 918" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Critical lines -->
  <line x1="480" y1="920" x2="480" y2="750" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  <line x1="1272" y1="920" x2="1272" y2="750" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  
  <text x="480" y="970" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">–1.980</text>
  <text x="1272" y="970" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">+1.980</text>
  <text x="480" y="1015" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Lower Critical Value</text>
  <text x="1272" y="1015" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Upper Critical Value</text>
  
  <!-- Test statistic marker: -5.474 (far in left tail) -->
  <line x1="220" y1="920" x2="220" y2="550" stroke="#e11d48" stroke-width="5" />
  <polygon points="220,550 210,570 230,570" fill="#e11d48" />
  <text x="220" y="510" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">t-statistic = –5.474</text>
  <text x="220" y="540" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">(Falls in Rejection Region)</text>
  
  <!-- Labels -->
  <text x="350" y="840" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="350" y="875" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Area = 0.025</text>
  
  <text x="1430" y="840" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="1430" y="875" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Area = 0.025</text>
  
  <text x="876" y="580" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Fail to Reject H₀</text>
  <text x="876" y="630" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="middle">Confidence Level = 0.95</text>
  
  <!-- Decision box -->
  <rect x="250" y="1060" width="1252" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="876" y="1115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Decision: Since t = –5.474 &lt; –1.980, Reject H₀. Conclude abnormal returns are significantly different.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/ee7fb6439edbe3b04caf.png")
    print(f"Saved ee7fb6439edbe3b04caf.png ({pix.width}x{pix.height})")

def render_fd24():
    # Figure 8.4: Chi-square (χ²) curve df=10 showing rejection boundaries 3.247 and 20.483 (1522 x 1215)
    w, h = 1522, 1215
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1422" height="1115" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="761" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 8.4: Two-Tailed Chi-Square Test (df = 10)</text>
  <text x="761" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Significance Level α = 0.05 | Rejection Regions: Lower 2.5% and Upper 2.5%</text>
  
  <!-- Axis -->
  <line x1="120" y1="920" x2="1400" y2="920" stroke="#0f172a" stroke-width="5" />
  <line x1="140" y1="920" x2="140" y2="280" stroke="#0f172a" stroke-width="4" />
  <text x="140" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">0</text>
  
  <!-- Shades -->
  <!-- Left rejection (0 to 3.247): x=140 to x=320 -->
  <path d="M 140 920 C 180 920 250 820 320 620 L 320 920 Z" fill="#ef4444" fill-opacity="0.25" />
  <!-- Center non-rejection (3.247 to 20.483): x=320 to x=1050 -->
  <path d="M 320 620 C 400 420 520 320 620 320 C 780 320 950 560 1050 820 L 1050 920 L 320 920 Z" fill="#0284c7" fill-opacity="0.1" />
  <!-- Right rejection (> 20.483): x=1050 to x=1360 -->
  <path d="M 1050 820 C 1150 900 1260 915 1360 918 L 1360 920 L 1050 920 Z" fill="#ef4444" fill-opacity="0.25" />
  
  <path d="M 140 920 C 180 920 250 820 320 620 C 400 420 520 320 620 320 C 780 320 950 560 1050 820 C 1150 900 1260 915 1360 918" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Boundary lines -->
  <line x1="320" y1="920" x2="320" y2="620" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  <line x1="1050" y1="920" x2="1050" y2="820" stroke="#ef4444" stroke-width="4" stroke-dasharray="6 6" />
  
  <text x="320" y="970" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">3.247</text>
  <text x="320" y="1010" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">χ²_0.975</text>
  
  <text x="1050" y="970" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">20.483</text>
  <text x="1050" y="1010" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">χ²_0.025</text>
  
  <!-- Labels -->
  <text x="240" y="820" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="240" y="855" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Area = 0.025</text>
  
  <text x="1200" y="840" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Reject H₀</text>
  <text x="1200" y="875" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Area = 0.025</text>
  
  <text x="680" y="580" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Fail to Reject H₀</text>
  <text x="680" y="630" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Confidence Region = 0.95</text>
  
  <!-- Decision banner -->
  <rect x="200" y="1060" width="1122" height="75" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="761" y="1110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Decision Rule: Reject H₀ if test statistic χ² &lt; 3.247 or χ² &gt; 20.483</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/fd24dc32709058032574.png")
    print(f"Saved fd24dc32709058032574.png ({pix.width}x{pix.height})")

def render_026b():
    # Figure 10.5: Residual plot independence and constant variance (homoskedasticity) (1850 x 2082)
    w, h = 1850, 2082
    np.random.seed(42)
    n_points = 120
    x_pts = np.random.uniform(250, 1600, n_points)
    # constant variance uniform/normal band
    y_pts = 1041 + np.random.normal(0, 140, n_points)
    
    dots_svg = ""
    for xp, yp in zip(x_pts, y_pts):
        dots_svg += f'<circle cx="{xp:.1f}" cy="{yp:.1f}" r="8" fill="#0284c7" opacity="0.8" />\n'
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1750" height="1982" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="925" y="140" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="bold" text-anchor="middle">Figure 10.5: Residual Plot — Independence and Homoskedasticity</text>
  <text x="925" y="200" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" text-anchor="middle">Residuals exhibit constant variance and no pattern across values of the independent variable</text>
  
  <!-- Outer Frame -->
  <line x1="200" y1="1800" x2="1680" y2="1800" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="1800" x2="200" y2="280" stroke="#0f172a" stroke-width="5" />
  
  <!-- Center Zero Line (Residual = 0) -->
  <line x1="200" y1="1041" x2="1680" y2="1041" stroke="#0f172a" stroke-width="4" stroke-dasharray="10 8" />
  
  <!-- Horizontal boundary band -->
  <line x1="200" y1="650" x2="1680" y2="650" stroke="#0284c7" stroke-width="3" stroke-dasharray="6 6" opacity="0.5" />
  <line x1="200" y1="1432" x2="1680" y2="1432" stroke="#0284c7" stroke-width="3" stroke-dasharray="6 6" opacity="0.5" />
  
  <text x="170" y="1051" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">0</text>
  <text x="170" y="660" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="end">+2 s_e</text>
  <text x="170" y="1442" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="end">–2 s_e</text>
  
  <text x="150" y="260" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Residual (e_i)</text>
  <text x="940" y="1870" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Independent Variable (X_i)</text>
  
  {dots_svg}
  
  <!-- Summary Box -->
  <rect x="250" y="1910" width="1350" height="90" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="925" y="1965" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Ideal Diagnostic: Random scatter around zero demonstrates homoskedasticity and uncorrelated errors.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/026b7fda06c5d5aea4d2.png")
    print(f"Saved 026b7fda06c5d5aea4d2.png ({pix.width}x{pix.height})")

def render_5635():
    # Figure 10.9: Log-Lin Model, EPS Data (2155 x 1167)
    w, h = 2155, 1167
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2055" height="1067" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1077" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 10.9: Log-Linear Regression Model (ln EPS vs. Time)</text>
  <text x="1077" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">ln(Y_t) = b₀ + b₁ · t | Models a constant percentage growth rate over time</text>
  
  <!-- Axes -->
  <line x1="200" y1="920" x2="1950" y2="920" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="920" x2="200" y2="250" stroke="#0f172a" stroke-width="5" />
  <text x="200" y="220" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">ln(EPS_t)</text>
  <text x="1950" y="975" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">Time (Quarter t)</text>
  
  <!-- Fitted Line -->
  <line x1="200" y1="820" x2="1850" y2="300" stroke="#0284c7" stroke-width="6" />
  
  <!-- Scatter Points oscillating tightly around fitted line -->
  <!-- slope = -520 / 1650 = -0.315 per px -->
"""
    pts = [
        (250, 790), (320, 810), (400, 740), (480, 720), (560, 690),
        (640, 710), (720, 640), (800, 620), (880, 580), (960, 610),
        (1040, 540), (1120, 520), (1200, 480), (1280, 500), (1360, 430),
        (1440, 420), (1520, 390), (1600, 410), (1680, 340), (1760, 320)
    ]
    for xp, yp in pts:
        svg += f'  <circle cx="{xp}" cy="{yp}" r="9" fill="#0f172a" />\n'
        
    svg += """
  <!-- Callout label -->
  <rect x="1200" y="260" width="650" height="110" fill="#f8fafc" stroke="#0284c7" stroke-width="3" rx="14" />
  <text x="1525" y="305" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Slope b₁ ≈ Constant Growth Rate</text>
  <text x="1525" y="345" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">1-unit increase in t → b₁ × 100% change in EPS</text>
  
  <!-- Bottom banner -->
  <rect x="200" y="1010" width="1750" height="80" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1077" y="1060" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Transforming exponential earnings growth into natural logs linearizes the time series for OLS estimation.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/563550489501c9e73a39.png")
    print(f"Saved 563550489501c9e73a39.png ({pix.width}x{pix.height})")

def render_9da1():
    # Figure 10.1: Scatter Plot of ABC Excess Returns vs. S&P 500 Index Excess Returns (2497 x 1482)
    w, h = 2497, 1482
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2397" height="1382" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1248" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 10.1: Scatter Plot — Stock ABC vs. S&amp;P 500 Excess Returns</text>
  <text x="1248" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Monthly observations showing positive correlation between stock and market excess returns</text>
  
  <!-- Axes passing through (0, 0) at (1000, 780) -->
  <line x1="250" y1="780" x2="2250" y2="780" stroke="#0f172a" stroke-width="4" />
  <line x1="1000" y1="1300" x2="1000" y2="260" stroke="#0f172a" stroke-width="4" />
  
  <text x="2250" y="830" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">S&amp;P 500 Excess Return (R_m – R_f) %</text>
  <text x="980" y="250" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">ABC Excess Return (R_i – R_f) %</text>
  
  <text x="975" y="815" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="end">0.0%</text>
  
  <!-- Scatter dots with positive slope -->
"""
    np.random.seed(101)
    x_m = np.random.normal(0, 4, 45)
    y_abc = 0.8 * x_m + np.random.normal(0, 2.5, 45)
    for xm, yabc in zip(x_m, y_abc):
        px = 1000 + xm * 100
        py = 780 - yabc * 45
        svg += f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="10" fill="#0284c7" opacity="0.85" stroke="#0f172a" stroke-width="2" />\n'
        
    svg += """
  <!-- Highlighted Point -->
  <circle cx="1200" cy="730" r="14" fill="#e11d48" stroke="#ffffff" stroke-width="3" />
  <line x1="1200" y1="730" x2="1400" y2="600" stroke="#e11d48" stroke-width="3" />
  <rect x="1400" y="550" width="450" height="90" fill="#f8fafc" stroke="#e11d48" stroke-width="2" rx="10" />
  <text x="1625" y="590" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Sample Observation: Month t</text>
  <text x="1625" y="625" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Market Excess = +2.0%, ABC Excess = +1.1%</text>

  <!-- Bottom banner -->
  <rect x="250" y="1320" width="2000" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1248" y="1375" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Visual inspection of raw scatter data confirms a positive linear relationship suitable for OLS regression.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/9da1c0fc74f15ff5640f.png")
    print(f"Saved 9da1c0fc74f15ff5640f.png ({pix.width}x{pix.height})")

def render_c8eb():
    # Figure 10.6: Geometric partition diagram showing total deviation = explained + unexplained (1897 x 855)
    w, h = 1897, 855
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1817" height="775" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="948" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Figure 10.6: Partition of Total Variation in Regression (SST = SSR + SSE)</text>
  <text x="948" y="155" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Total Deviation (Y_i – Ȳ) = Explained Deviation (Ŷ_i – Ȳ) + Residual Error (Y_i – Ŷ_i)</text>
  
  <!-- Axis -->
  <line x1="150" y1="720" x2="1750" y2="720" stroke="#0f172a" stroke-width="4" />
  <line x1="150" y1="720" x2="150" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="1750" y="765" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">X (Independent Variable)</text>
  <text x="150" y="170" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Y</text>
  
  <!-- Mean line Ȳ -->
  <line x1="150" y1="560" x2="1750" y2="560" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />
  <text x="160" y="545" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Ȳ (Sample Mean of Y)</text>
  
  <!-- Regression Line Ŷ = b0 + b1 X -->
  <line x1="200" y1="680" x2="1700" y2="280" stroke="#0284c7" stroke-width="5" />
  <text x="1710" y="275" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Ŷ = b₀ + b₁X</text>
  
  <!-- Specific observation point at x=1250 -->
  <!-- Ȳ is at y=560 -->
  <!-- Ŷ is at y=400 -->
  <!-- Actual Y_i is at y=260 -->
  <line x1="1250" y1="720" x2="1250" y2="260" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4 4" />
  <text x="1250" y="760" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">X_i</text>
  
  <!-- Points -->
  <circle cx="1250" cy="560" r="7" fill="#94a3b8" />
  <circle cx="1250" cy="400" r="8" fill="#0284c7" />
  <circle cx="1250" cy="260" r="10" fill="#e11d48" />
  <text x="1280" y="265" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Actual Point (X_i, Y_i)</text>
  <text x="1280" y="405" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Predicted Point (X_i, Ŷ_i)</text>
  
  <!-- Deviation Brackets -->
  <!-- Residual Error (Y_i - Ŷ_i): y=260 to y=400 -->
  <line x1="1230" y1="260" x2="1230" y2="400" stroke="#e11d48" stroke-width="4" />
  <line x1="1220" y1="260" x2="1240" y2="260" stroke="#e11d48" stroke-width="3" />
  <line x1="1220" y1="400" x2="1240" y2="400" stroke="#e11d48" stroke-width="3" />
  <text x="1210" y="340" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="end">Unexplained Error (Y_i – Ŷ_i)</text>
  
  <!-- Regression Explained (Ŷ_i - Ȳ): y=400 to y=560 -->
  <line x1="1230" y1="400" x2="1230" y2="560" stroke="#0284c7" stroke-width="4" />
  <line x1="1220" y1="560" x2="1240" y2="560" stroke="#0284c7" stroke-width="3" />
  <text x="1210" y="490" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="end">Explained by Model (Ŷ_i – Ȳ)</text>
  
  <!-- Total Deviation bracket on right side: y=260 to y=560 -->
  <line x1="1600" y1="260" x2="1600" y2="560" stroke="#0f172a" stroke-width="4" />
  <line x1="1590" y1="260" x2="1610" y2="260" stroke="#0f172a" stroke-width="3" />
  <line x1="1590" y1="560" x2="1610" y2="560" stroke="#0f172a" stroke-width="3" />
  <text x="1625" y="420" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Total Deviation (Y_i – Ȳ)</text>
  
  <!-- Bottom summary equation -->
  <rect x="250" y="630" width="800" height="65" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="10" />
  <text x="650" y="672" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">∑(Y_i – Ȳ)² [SST] = ∑(Ŷ_i – Ȳ)² [SSR] + ∑(Y_i – Ŷ_i)² [SSE]</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/c8eb2e282deb8c77134a.png")
    print(f"Saved c8eb2e282deb8c77134a.png ({pix.width}x{pix.height})")

def render_d795():
    # Figure 10.2: Estimated ordinary least squares (OLS) regression line fitted through scatter plot (2012 x 1224)
    w, h = 2012, 1224
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1912" height="1124" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1006" y="125" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 10.2: Estimated OLS Regression Equation</text>
  <text x="1006" y="175" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Ŷ_i = b₀ + b₁X_i | Minimizing the sum of squared vertical residuals (SSE)</text>
  
  <!-- Axes passing through (0, 0) at (800, 680) -->
  <line x1="200" y1="680" x2="1850" y2="680" stroke="#0f172a" stroke-width="4" />
  <line x1="800" y1="1080" x2="800" y2="240" stroke="#0f172a" stroke-width="4" />
  
  <text x="1850" y="730" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">S&amp;P 500 Excess Return (X)</text>
  <text x="780" y="235" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">ABC Excess Return (Y)</text>
  
  <!-- OLS Line: Y = b0 + b1 * X. Intercept b0 at y=640 (slightly above zero) -->
  <line x1="250" y1="920" x2="1750" y2="300" stroke="#0284c7" stroke-width="6" />
  
  <!-- Scatter dots with vertical residual lines to regression line -->
"""
    pts = [
        (400, 880, 858), (550, 750, 796), (700, 720, 734), (850, 600, 672),
        (1000, 620, 610), (1150, 520, 548), (1300, 460, 486), (1450, 450, 424),
        (1600, 340, 362), (1700, 310, 321)
    ]
    for xp, yp, y_line in pts:
        # vertical residual dashed line
        svg += f'  <line x1="{xp}" y1="{yp}" x2="{xp}" y2="{y_line}" stroke="#ef4444" stroke-width="2.5" stroke-dasharray="4 4" />\n'
        svg += f'  <circle cx="{xp}" cy="{yp}" r="8" fill="#0f172a" />\n'
        
    svg += """
  <!-- Intercept Callout -->
  <circle cx="800" cy="640" r="10" fill="#059669" />
  <line x1="800" y1="640" x2="620" y2="520" stroke="#059669" stroke-width="3" />
  <rect x="360" y="470" width="260" height="70" fill="#f8fafc" stroke="#059669" stroke-width="2" rx="10" />
  <text x="490" y="515" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Intercept b₀ (Alpha)</text>

  <!-- Slope Triangle -->
  <polygon points="1200,527 1400,527 1400,445" fill="#0284c7" fill-opacity="0.15" stroke="#0284c7" stroke-width="2" />
  <text x="1300" y="560" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">ΔX = 1 unit</text>
  <text x="1420" y="490" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Slope b₁ (Beta)</text>
  
  <!-- Residual legend -->
  <rect x="1200" y="860" width="650" height="110" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <line x1="1230" y1="915" x2="1300" y2="915" stroke="#ef4444" stroke-width="3" stroke-dasharray="5 5" />
  <text x="1320" y="922" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Vertical dashed lines = Residual errors (e_i)</text>
  <text x="1320" y="955" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20">OLS solves min ∑(e_i)² = min ∑(Y_i – Ŷ_i)²</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/d7950b109124bca7e783.png")
    print(f"Saved d7950b109124bca7e783.png ({pix.width}x{pix.height})")

def render_e378():
    # Figure 10.4: Heteroskedasticity residual plot fan-shaped (1760 x 2087)
    w, h = 1760, 2087
    np.random.seed(42)
    n_points = 140
    x_pts = np.random.uniform(250, 1550, n_points)
    # residual standard deviation expands as x increases: fan shape!
    y_pts = []
    for xp in x_pts:
        scale = 30 + 0.28 * (xp - 250)
        y_pts.append(1043 + np.random.normal(0, scale))
        
    dots_svg = ""
    for xp, yp in zip(x_pts, y_pts):
        dots_svg += f'<circle cx="{xp:.1f}" cy="{yp:.1f}" r="8" fill="#e11d48" opacity="0.8" />\n'
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1660" height="1987" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="880" y="140" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="bold" text-anchor="middle">Figure 10.4: Residual Plot — Heteroskedasticity</text>
  <text x="880" y="200" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" text-anchor="middle">Non-constant error variance: Residual dispersion expands with independent variable X</text>
  
  <!-- Outer Axes -->
  <line x1="200" y1="1800" x2="1600" y2="1800" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="1800" x2="200" y2="280" stroke="#0f172a" stroke-width="5" />
  
  <!-- Center Zero Line -->
  <line x1="200" y1="1043" x2="1600" y2="1043" stroke="#0f172a" stroke-width="4" stroke-dasharray="10 8" />
  
  <!-- Fan-shaped boundary envelope lines -->
  <line x1="250" y1="1000" x2="1550" y2="550" stroke="#e11d48" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="250" y1="1086" x2="1550" y2="1536" stroke="#e11d48" stroke-width="3" stroke-dasharray="6 6" />
  
  <text x="170" y="1053" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">0</text>
  <text x="150" y="260" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Residual (e_i)</text>
  <text x="900" y="1870" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Independent Variable (X_i)</text>
  
  {dots_svg}
  
  <!-- Warning callout -->
  <rect x="250" y="1910" width="1260" height="95" fill="#fef2f2" stroke="#f87171" stroke-width="2" rx="14" />
  <text x="880" y="1950" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Violation of Regression Assumption: Heteroskedasticity causes biased standard errors.</text>
  <text x="880" y="1985" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">t-statistics and F-statistics become unreliable (typically inflated t-stats, Type I error risk).</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/e378b5d3ab7a386e8075.png")
    print(f"Saved e378b5d3ab7a386e8075.png ({pix.width}x{pix.height})")

def render_e9fe():
    # Figure 10.3: Nonlinear Relationship scatter plot fitted incorrectly with linear line (1830 x 2145)
    w, h = 1830, 2145
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1730" height="2045" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="915" y="140" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="bold" text-anchor="middle">Figure 10.3: Nonlinear Relationship Misspecification</text>
  <text x="915" y="200" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" text-anchor="middle">Linear OLS line fitted to inherently curved / parabolic data generates systematic error patterns</text>
  
  <!-- Outer Axes -->
  <line x1="200" y1="1850" x2="1650" y2="1850" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="1850" x2="200" y2="280" stroke="#0f172a" stroke-width="5" />
  <text x="150" y="260" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Y (Dependent Variable)</text>
  <text x="925" y="1920" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">X (Independent Variable)</text>
  
  <!-- Erroneous Linear Regression Line -->
  <line x1="250" y1="1500" x2="1600" y2="600" stroke="#e11d48" stroke-width="6" stroke-dasharray="10 8" />
  <text x="1610" y="590" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Linear Fit (Misspecified)</text>
  
  <!-- Parabolic Data Curve Path -->
  <path d="M 250 1700 Q 925 500 1600 500" fill="none" stroke="#0284c7" stroke-width="4" stroke-dasharray="6 6" />
  
  <!-- Scatter dots following U-shape / curve -->
"""
    np.random.seed(55)
    xs = np.linspace(250, 1600, 60)
    for xp in xs:
        # normalized u = (xp - 250) / 1350
        u = (xp - 250) / 1350
        # curve drops then flattens/rises or inverted U
        # let's do curve where residuals are positive, then negative, then positive
        yp = 1650 - 2400 * u + 1500 * (u ** 2) + np.random.normal(0, 35)
        svg += f'  <circle cx="{xp:.1f}" cy="{yp:.1f}" r="8" fill="#0f172a" opacity="0.85" />\n'
        
    svg += """
  <!-- Callout box -->
  <rect x="250" y="1960" width="1330" height="95" fill="#fef2f2" stroke="#f87171" stroke-width="2" rx="14" />
  <text x="915" y="2000" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Diagnostic: Residuals show non-random signs (+, –, +), signaling functional misspecification.</text>
  <text x="915" y="2035" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Remedy: Use log-lin, lin-log, or polynomial regression to capture true curvature.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/e9fe437d2cbb78649eeb.png")
    print(f"Saved e9fe437d2cbb78649eeb.png ({pix.width}x{pix.height})")

def render_79f7():
    # Figure 10.7: ANOVA Table for a Simple Linear Regression (2064 x 560)
    w, h = 2064, 560
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="30" y="30" width="2004" height="500" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1032" y="85" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Figure 10.7: ANOVA Table Structure for Simple Linear Regression</text>
  
  <!-- Table Header -->
  <rect x="60" y="120" width="1944" height="65" fill="#0284c7" rx="12" />
  <text x="250" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Source of Variation</text>
  <text x="650" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Degrees of Freedom (df)</text>
  <text x="1050" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Sum of Squares (SS)</text>
  <text x="1450" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Mean Square (MS)</text>
  <text x="1800" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">F-Statistic</text>
  
  <!-- Row 1: Regression -->
  <rect x="60" y="195" width="1944" height="75" fill="#f8fafc" />
  <text x="250" y="242" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Regression (Explained)</text>
  <text x="650" y="242" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">k = 1</text>
  <text x="1050" y="242" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">SSR = ∑(Ŷ_i – Ȳ)²</text>
  <text x="1450" y="242" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">MSR = SSR / 1</text>
  <text x="1800" y="242" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">F = MSR / MSE</text>
  <line x1="60" y1="270" x2="2004" y2="270" stroke="#e2e8f0" stroke-width="2" />
  
  <!-- Row 2: Residual -->
  <rect x="60" y="272" width="1944" height="75" fill="#ffffff" />
  <text x="250" y="319" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Residual (Unexplained Error)</text>
  <text x="650" y="319" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">n – k – 1 = n – 2</text>
  <text x="1050" y="319" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">SSE = ∑(Y_i – Ŷ_i)²</text>
  <text x="1450" y="319" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">MSE = SSE / (n – 2)</text>
  <text x="1800" y="319" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">—</text>
  <line x1="60" y1="347" x2="2004" y2="347" stroke="#e2e8f0" stroke-width="2" />
  
  <!-- Row 3: Total -->
  <rect x="60" y="349" width="1944" height="75" fill="#f1f5f9" />
  <text x="250" y="396" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Total</text>
  <text x="650" y="396" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">n – 1</text>
  <text x="1050" y="396" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">SST = ∑(Y_i – Ȳ)²</text>
  <text x="1450" y="396" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">—</text>
  <text x="1800" y="396" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">—</text>
  <line x1="60" y1="424" x2="2004" y2="424" stroke="#cbd5e1" stroke-width="3" />
  
  <!-- Key Formulas Footer -->
  <text x="1032" y="475" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Coefficient of Determination: R² = SSR / SST = 1 – (SSE / SST) | Standard Error of Estimate: s_e = √MSE</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/79f79c5f771dc0c6d232.png")
    print(f"Saved 79f79c5f771dc0c6d232.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_0a3a()
    render_1136()
    render_1f29()
    render_510d()
    render_5651()
    render_6224()
    render_d08a()
    render_ee7f()
    render_fd24()
    render_026b()
    render_5635()
    render_9da1()
    render_c8eb()
    render_d795()
    render_e378()
    render_e9fe()
    render_79f7()
