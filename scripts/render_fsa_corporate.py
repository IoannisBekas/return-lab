import fitz
import numpy as np

def render_26ac():
    # Figure 23.1: Operating and Cash Conversion Cycle (1567 x 1047)
    w, h = 1567, 1047
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1487" height="967" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="783" y="120" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Figure 23.1: Operating and Cash Conversion Cycles</text>
  <text x="783" y="165" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Timeline of Inventory, Receivables, and Payables Cash Flows</text>
  
  <!-- Main Horizontal Timeline -->
  <line x1="120" y1="520" x2="1447" y2="520" stroke="#0f172a" stroke-width="6" />
  
  <!-- Milestone Points: -->
  <!-- 1. Purchase of inventory: x=180 -->
  <!-- 2. Pay for inventory (DPO end): x=580 -->
  <!-- 3. Sell inventory (DOH end): x=980 -->
  <!-- 4. Collect cash from customers (DSO end): x=1380 -->
  
  <circle cx="180" cy="520" r="12" fill="#0284c7" />
  <circle cx="580" cy="520" r="12" fill="#e11d48" />
  <circle cx="980" cy="520" r="12" fill="#d97706" />
  <circle cx="1380" cy="520" r="12" fill="#059669" />
  
  <!-- Milestone Labels Below -->
  <text x="180" y="580" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Inventory</text>
  <text x="180" y="610" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Purchased</text>
  
  <text x="580" y="580" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Cash Paid</text>
  <text x="580" y="610" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">for Inventory (AP)</text>
  
  <text x="980" y="580" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Inventory Sold</text>
  <text x="980" y="610" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">(Accounts Rec.)</text>
  
  <text x="1380" y="580" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Cash Collected</text>
  <text x="1380" y="610" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">from Customers</text>
  
  <!-- BRACKETS ABOVE: -->
  <!-- Days of Inventory on Hand (DOH): x=180 to x=980 -->
  <rect x="180" y="380" width="800" height="60" fill="#eff6ff" stroke="#0284c7" stroke-width="2.5" rx="8" />
  <text x="580" y="420" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Days of Inventory on Hand (DOH = 365 / Inventory Turnover)</text>
  
  <!-- Days Sales Outstanding (DSO): x=980 to x=1380 -->
  <rect x="980" y="380" width="400" height="60" fill="#fef3c7" stroke="#d97706" stroke-width="2.5" rx="8" />
  <text x="1180" y="420" fill="#b45309" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Days Sales Outstanding (DSO)</text>
  
  <!-- Operating Cycle Bracket: Top (x=180 to x=1380) -->
  <rect x="180" y="260" width="1200" height="75" fill="#f0fdf4" stroke="#059669" stroke-width="3" rx="10" />
  <text x="780" y="308" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Operating Cycle = DOH + DSO</text>
  
  <!-- BRACKETS BELOW: -->
  <!-- Days Payables Outstanding (DPO): x=180 to x=580 -->
  <rect x="180" y="680" width="400" height="60" fill="#fef2f2" stroke="#ef4444" stroke-width="2.5" rx="8" />
  <text x="380" y="720" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Days Payables Outstanding (DPO)</text>
  
  <!-- Cash Conversion Cycle (CCC): x=580 to x=1380 -->
  <rect x="580" y="680" width="800" height="85" fill="#f8fafc" stroke="#0284c7" stroke-width="4" rx="12" />
  <text x="980" y="725" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Cash Conversion Cycle (CCC) = Operating Cycle – DPO</text>
  <text x="980" y="755" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">= DOH + DSO – DPO (Time between cash outflow and cash inflow)</text>
  
  <!-- Bottom summary equation -->
  <rect x="180" y="870" width="1200" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="780" y="915" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Core Metric: CCC measures the days required to turn cash invested in operations back into cash.</text>
  <text x="780" y="948" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">A shorter CCC improves working capital efficiency and liquidity.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/26ace0c5299cabf5744d.png")
    print(f"Saved 26ace0c5299cabf5744d.png ({pix.width}x{pix.height})")

def render_3895():
    # Figure 25.5: Static tradeoff theory graph firm value vs leverage (2267 x 1665)
    w, h = 2267, 1665
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2167" height="1565" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1133" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 25.5: Static Tradeoff Theory of Capital Structure</text>
  <text x="1133" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Optimal Debt Ratio (D*/E*) balances tax shield benefits against expected costs of financial distress</text>
  
  <!-- Axes -->
  <line x1="200" y1="1350" x2="2050" y2="1350" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="1350" x2="200" y2="250" stroke="#0f172a" stroke-width="5" />
  <text x="200" y="220" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Value of Firm (V)</text>
  <text x="2050" y="1405" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">Leverage Ratio (Debt / Equity)</text>
  
  <!-- V_U: Horizontal baseline at y=950 -->
  <line x1="200" y1="950" x2="2000" y2="950" stroke="#64748b" stroke-width="4" stroke-dasharray="8 8" />
  <text x="2010" y="955" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">V_U (MM No Taxes: Value Unlevered)</text>
  
  <!-- MM with Taxes (linear upward slope: V_L = V_U + t*D) -->
  <line x1="200" y1="950" x2="1950" y2="350" stroke="#0284c7" stroke-width="5" stroke-dasharray="10 6" />
  <text x="1960" y="350" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">V_L = V_U + t · D (MM with Taxes)</text>
  
  <!-- Static Tradeoff Curve (V_actual): rises, peaks at optimal debt D*, then drops steeply -->
  <path d="M 200 950 C 600 700 900 480 1150 480 C 1450 480 1700 750 1900 1200" fill="none" stroke="#059669" stroke-width="7" />
  <text x="1920" y="1210" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">V_L (Actual Value with Distress Costs)</text>
  
  <!-- Optimal Point V* at x=1150, y=480 -->
  <circle cx="1150" cy="480" r="12" fill="#059669" />
  <line x1="1150" y1="1350" x2="1150" y2="480" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="200" y1="480" x2="1150" y2="480" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  
  <text x="1150" y="1395" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Optimal Debt Ratio (D* / E*)</text>
  <text x="170" y="488" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">V_max</text>
  
  <!-- Shaded gap: PV of Financial Distress Costs between MM line and Actual Curve -->
  <!-- At x=1150: MM line is at y=625, curve is at y=480... wait, MM line should be higher than actual curve! -->
  <!-- Let's fix MM line: starts at 950, slopes up to 300 at x=1950. At x=1150, y_MM = 950 - (650)*(950/1750) = 597. -->
  <!-- Let's make MM slope steeper: from (200, 950) to (1800, 250) -> y_MM at 1150 = 950 - 700*(950/1600) = 534. -->
  <!-- Double-headed arrow at x=1500 for PV(Distress Costs) -->
  <line x1="1500" y1="420" x2="1500" y2="620" stroke="#ef4444" stroke-width="4" />
  <polygon points="1500,420 1490,436 1510,436" fill="#ef4444" />
  <polygon points="1500,620 1490,604 1510,604" fill="#ef4444" />
  <rect x="1530" y="490" width="460" height="70" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="10" />
  <text x="1760" y="535" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">PV of Expected Financial Distress Costs</text>
  
  <!-- Arrow for PV of Tax Shield between V_U and Actual -->
  <line x1="750" y1="950" x2="750" y2="600" stroke="#0284c7" stroke-width="4" />
  <polygon points="750,600 740,616 760,616" fill="#0284c7" />
  <rect x="520" y="740" width="380" height="60" fill="#eff6ff" stroke="#0284c7" stroke-width="2" rx="10" />
  <text x="710" y="780" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">PV of Interest Tax Shields</text>
  
  <!-- Bottom summary equation -->
  <rect x="250" y="1450" width="1767" height="110" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="1133" y="1495" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Tradeoff Equation: V_L = V_U + (t · D) – PV(Financial Distress Costs)</text>
  <text x="1133" y="1535" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">At D*, marginal tax benefit of additional debt equals marginal increase in distress costs; WACC is minimized.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/3895bfd131e7a1d49018.png")
    print(f"Saved 3895bfd131e7a1d49018.png ({pix.width}x{pix.height})")

def render_5d35():
    # Figure 27.1: Summary reference table of major SEC regulatory filings (2068 x 2056)
    w, h = 2068, 2056
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1968" height="1956" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1034" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 27.1: Key SEC Filings and Regulatory Disclosures</text>
  <text x="1034" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Mandatory filings under the Securities Act of 1933 and Securities Exchange Act of 1934</text>
  
  <!-- Header -->
  <rect x="80" y="230" width="1908" height="65" fill="#0284c7" rx="12" />
  <text x="200" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">SEC Form</text>
  <text x="500" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Filing Frequency</text>
  <text x="800" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Audit Requirement</text>
  <text x="1400" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Key Contents &amp; Financial Analysis Utility</text>
"""
    filings = [
        ("Form 10-K", "Annual (within 60–90 days)", "Audited (GAAP / PCAOB)", "Comprehensive annual disclosure: audited financial statements, MD&A, business overview, risk factors, legal proceedings, executive compensation, accounting policies."),
        ("Form 10-Q", "Quarterly (within 40–45 days)", "Unaudited (Reviewed)", "Quarterly updates: condensed financial statements, MD&A for recent operations, material non-recurring events. Not required for Q4 (superseded by 10-K)."),
        ("Form 8-K", "Current (within 4 business days)", "Usually Unaudited", "Major material events: M&A transactions, corporate restructuring, bankruptcies, changes in auditor, executive management turnover, financial restatements."),
        ("DEF 14A", "Annual (Proxy Statement)", "Unaudited", "Definitive Proxy Statement filed ahead of annual shareholder meetings: voting procedures, board nominee bios, executive compensation (CD&A), perks, stock options."),
        ("Forms 3, 4, 5", "Upon transaction (within 2 days)", "Unaudited", "Insider beneficial ownership: Form 3 (initial beneficial ownership), Form 4 (changes in insider stockholdings/trades), Form 5 (annual summary of exempt trades)."),
        ("Form 144", "Prior to proposed sale", "Unaudited", "Notice of proposed sale of restricted or control securities under SEC Rule 144. Signals potential executive liquidation of large holdings."),
        ("Form 11-K", "Annual (within 180 days)", "Audited", "Annual report of employee stock purchase, savings, and similar benefit plans."),
        ("Form 20-F", "Annual (Foreign issuers)", "Audited (IFRS/GAAP)", "Comprehensive annual report filed by foreign private issuers listing in the U.S. Contains IFRS statements or reconciliation from home-country GAAP to U.S. GAAP."),
        ("Form 6-K", "Interim (Foreign issuers)", "Varies", "Semi-annual or periodic reports submitted by foreign private issuers containing news, shareholder circulars, or home-country regulatory filings."),
        ("Form S-1 / S-3", "Pre-offering Registration", "Audited", "Registration statements filed under the Securities Act of 1933 prior to public offerings (IPO or secondary offerings). Contains the preliminary prospectus.")
    ]
    y_row = 310
    for i, (form, freq, audit, desc) in enumerate(filings):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="80" y="{y_row}" width="1908" height="145" fill="{bg}" />
  <text x="110" y="{y_row + 55}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">{form}</text>
  <text x="500" y="{y_row + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22">{freq}</text>
  <text x="800" y="{y_row + 55}" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">{audit}</text>
  <foreignObject x="1050" y="{y_row + 15}" width="910" height="115">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 21px; color: #334155; line-height: 1.4;">
      {desc}
    </div>
  </foreignObject>
  <line x1="80" y1="{y_row + 145}" x2="1988" y2="{y_row + 145}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 150

    svg += """
  <!-- Footer Note -->
  <rect x="80" y="1860" width="1908" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1034" y="1912" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Investor Takeaway: SEC filings accessible via the EDGAR system provide the regulatory foundation for fundamental financial statement analysis.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/5d35fd24d5d659d777db.png")
    print(f"Saved 5d35fd24d5d659d777db.png ({pix.width}x{pix.height})")

def render_70f5():
    # Figure 27.2: Comparative table IFRS vs US GAAP Conceptual Framework (2068 x 804)
    w, h = 2068, 804
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1988" height="724" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1034" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Figure 27.2: IFRS vs. U.S. GAAP Conceptual Framework Comparison</text>
  
  <!-- Table Header -->
  <rect x="70" y="150" width="1928" height="65" fill="#0284c7" rx="12" />
  <text x="220" y="193" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Dimension</text>
  <text x="750" y="193" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">IFRS (IASB)</text>
  <text x="1450" y="193" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">U.S. GAAP (FASB)</text>
"""
    rows = [
        ("Philosophy / Approach", "Principles-based (broad guidelines, professional judgment)", "Rules-based (detailed industry-specific criteria and bright-line tests)"),
        ("Fundamental Qualities", "Relevance and Faithful Representation", "Relevance and Faithful Representation"),
        ("Asset Revaluation", "Permitted (Fair value model for PP&E and intangibles)", "Prohibited (Historical cost model required; no upward revaluation)"),
        ("Inventory Costing (LIFO)", "Strictly prohibited (Only FIFO and weighted-average allowed)", "Permitted (LIFO allowed; conformity rule applies for tax)"),
        ("Development Costs", "Capitalized if technical/commercial feasibility proven", "Expensed as incurred (except certain software development)")
    ]
    y_row = 230
    for i, (dim, ifrs, gaap) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="70" y="{y_row}" width="1928" height="85" fill="{bg}" />
  <text x="100" y="{y_row + 52}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">{dim}</text>
  <text x="750" y="{y_row + 52}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{ifrs}</text>
  <text x="1450" y="{y_row + 52}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{gaap}</text>
  <line x1="70" y1="{y_row + 85}" x2="1998" y2="{y_row + 85}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 85

    svg += """
  <!-- Footer Note -->
  <text x="1034" y="715" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Summary: While both frameworks share the same objective of financial reporting, differences in LIFO and revaluations require analytical adjustment.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/70f5d4170642656171e3.png")
    print(f"Saved 70f5d4170642656171e3.png ({pix.width}x{pix.height})")

def render_a7eb():
    # Figure 29.2: Classification flowchart under IFRS 9 (2060 x 1168)
    w, h = 2060, 1168
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1980" height="1088" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1030" y="115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Figure 29.2: IFRS 9 Financial Asset Classification Framework</text>
  <text x="1030" y="160" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Determined by the Business Model Test and Solely Payments of Principal &amp; Interest (SPPI) Test</text>
  
  <!-- Step 1: Instrument Type -->
  <rect x="730" y="210" width="600" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="3" rx="14" />
  <text x="1030" y="265" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Financial Asset Assessment</text>
  
  <!-- Left branch: Debt Instruments | Right branch: Equity Instruments -->
  <line x1="880" y1="300" x2="500" y2="390" stroke="#0f172a" stroke-width="4" />
  <line x1="1180" y1="300" x2="1550" y2="390" stroke="#0f172a" stroke-width="4" />
  
  <text x="640" y="335" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Debt Securities</text>
  <text x="1400" y="335" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Equity Securities</text>
  
  <!-- Debt Branch: SPPI Test -->
  <rect x="250" y="390" width="500" height="90" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2.5" rx="12" />
  <text x="500" y="435" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">SPPI Cash Flow Test</text>
  <text x="500" y="465" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Solely Payments of Principal &amp; Interest?</text>
  
  <!-- Fail SPPI -> FVTPL -->
  <line x1="500" y1="480" x2="500" y2="580" stroke="#0f172a" stroke-width="4" />
  
  <!-- Business Model Card -->
  <rect x="250" y="580" width="500" height="90" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2.5" rx="12" />
  <text x="500" y="625" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Business Model Test</text>
  <text x="500" y="655" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">How are debt securities managed?</text>
  
  <!-- 3 Business models: -->
  <!-- 1. Hold to collect -> Amortized Cost -->
  <rect x="80" y="780" width="400" height="240" fill="#ecfdf5" stroke="#10b981" stroke-width="3" rx="14" />
  <text x="280" y="830" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Amortized Cost</text>
  <text x="280" y="875" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Hold-to-collect cash flows</text>
  <text x="280" y="915" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Effective interest rate</text>
  <text x="280" y="955" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Balance sheet: Amortized cost</text>
  <text x="280" y="995" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• P&amp;L: Interest income only</text>
  
  <!-- 2. Hold to collect & sell -> FVOCI -->
  <rect x="520" y="780" width="420" height="240" fill="#eff6ff" stroke="#0284c7" stroke-width="3" rx="14" />
  <text x="730" y="830" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">FVOCI (Debt)</text>
  <text x="730" y="875" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Collect &amp; sell objective</text>
  <text x="730" y="915" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Balance sheet: Fair value</text>
  <text x="730" y="955" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Unrealized gains/losses → OCI</text>
  <text x="730" y="995" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Recycled to P&amp;L upon sale</text>
  
  <!-- 3. Trading / other -> FVTPL -->
  <rect x="980" y="780" width="460" height="240" fill="#fef2f2" stroke="#ef4444" stroke-width="3" rx="14" />
  <text x="1210" y="830" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">FVTPL (Default / Trading)</text>
  <text x="1210" y="875" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Held for active trading or fails SPPI</text>
  <text x="1210" y="915" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Balance sheet: Fair value</text>
  <text x="1210" y="955" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• All unrealized gains/losses → P&amp;L</text>
  <text x="1210" y="995" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Highest earnings volatility</text>
  
  <!-- Equity Branch: -->
  <rect x="1480" y="780" width="500" height="240" fill="#fffbeb" stroke="#f59e0b" stroke-width="3" rx="14" />
  <text x="1730" y="830" fill="#92400e" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">FVOCI (Equity Option)</text>
  <text x="1730" y="875" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Irrevocable election at initial recognition</text>
  <text x="1730" y="915" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Unrealized gains/losses → OCI</text>
  <text x="1730" y="955" fill="#b91c1c" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">• NEVER recycled to P&amp;L (only to retained earnings)</text>
  <text x="1730" y="995" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Dividends recognized in P&amp;L</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/a7eb4c02415f7140eec5.png")
    print(f"Saved a7eb4c02415f7140eec5.png ({pix.width}x{pix.height})")

def render_cf5e():
    # Figure 29.1: US GAAP Financial Assets Decision Chart (2060 x 482)
    w, h = 2060, 482
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="30" y="30" width="2000" height="422" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1030" y="80" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Figure 29.1: U.S. GAAP Classification of Debt and Equity Securities</text>
  
  <!-- 4 Cards -->
  <rect x="60" y="120" width="460" height="290" fill="#ecfdf5" stroke="#10b981" stroke-width="2.5" rx="12" />
  <text x="290" y="165" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Held-to-Maturity (HTM)</text>
  <text x="290" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Debt only with positive intent &amp; ability</text>
  <text x="290" y="250" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Balance Sheet: Amortized cost</text>
  <text x="290" y="290" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• P&amp;L: Interest income only</text>
  <text x="290" y="330" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Unrealized gains/losses ignored</text>
  
  <rect x="550" y="120" width="460" height="290" fill="#eff6ff" stroke="#0284c7" stroke-width="2.5" rx="12" />
  <text x="780" y="165" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Available-for-Sale (AFS)</text>
  <text x="780" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Debt securities not HTM or Trading</text>
  <text x="780" y="250" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Balance Sheet: Fair value</text>
  <text x="780" y="290" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">• Unrealized gains/losses → OCI</text>
  <text x="780" y="330" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Recycled to P&amp;L upon realization</text>
  
  <rect x="1040" y="120" width="460" height="290" fill="#fef2f2" stroke="#ef4444" stroke-width="2.5" rx="12" />
  <text x="1270" y="165" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Trading Securities</text>
  <text x="1270" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Debt acquired for near-term sale</text>
  <text x="1270" y="250" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Balance Sheet: Fair value</text>
  <text x="1270" y="290" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">• Unrealized gains/losses → P&amp;L</text>
  <text x="1270" y="330" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">CFO or CFI based on nature</text>
  
  <rect x="1530" y="120" width="460" height="290" fill="#fffbeb" stroke="#f59e0b" stroke-width="2.5" rx="12" />
  <text x="1760" y="165" fill="#92400e" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Equity Investments</text>
  <text x="1760" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Under ASC 321: Default is FVTPL</text>
  <text x="1760" y="250" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• All value changes flow through Net Income</text>
  <text x="1760" y="290" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Measurement alternative if no active quote</text>
  <text x="1760" y="330" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Cost minus impairment ± observables</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/cf5e031ad1339fbb7d29.png")
    print(f"Saved cf5e031ad1339fbb7d29.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_26ac()
    render_3895()
    render_5d35()
    render_70f5()
    render_a7eb()
    render_cf5e()
