import fitz

def render_231d():
    # Figure 30.1: Reference table listing noncash expenses, gains, and losses adjustments to CFO (2482 x 1292)
    w, h = 2482, 1292
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2382" height="1192" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1241" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 30.1: Indirect Method — Adjustments from Net Income to CFO</text>
  <text x="1241" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Reconciliation of Net Income to Cash Flow from Operating Activities</text>
  
  <!-- Header -->
  <rect x="80" y="230" width="2322" height="65" fill="#0284c7" rx="12" />
  <text x="250" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Adjustment Category</text>
  <text x="750" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Item / Transaction</text>
  <text x="1200" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Adjustment to Net Income</text>
  <text x="1800" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Analytical Rationale</text>
"""
    rows = [
        ("Noncash Expenses", "Depreciation of PP&E and Amortization of Intangibles", "ADD BACK (+)", "Reduces net income but requires zero cash outflow in current period.", "#059669"),
        ("Noncash Expenses", "Impairment of PP&E, Intangibles, or Goodwill", "ADD BACK (+)", "Noncash write-down reducing book value; no cash impact.", "#059669"),
        ("Noncash Expenses", "Share-Based Compensation Expense", "ADD BACK (+)", "Equity grant expensed in income statement with no cash outflow.", "#059669"),
        ("Non-Operating Items", "Loss on Sale of Long-Term Assets / PP&E", "ADD BACK (+)", "Operating loss added back; full cash proceeds reflected in CFI.", "#059669"),
        ("Non-Operating Items", "Gain on Sale of Long-Term Assets / PP&E", "DEDUCT (–)", "Operating gain subtracted; full cash proceeds reflected in CFI.", "#e11d48"),
        ("Non-Operating Items", "Gain on Early Extinguishment of Debt", "DEDUCT (–)", "Financing gain removed from operating cash flow; cash in CFF.", "#e11d48"),
        ("Deferred Taxes", "Increase in Deferred Tax Liability (DTL)", "ADD BACK (+)", "Tax expense accrued on P&L exceeds actual cash taxes paid.", "#059669"),
        ("Deferred Taxes", "Increase in Deferred Tax Asset (DTA)", "DEDUCT (–)", "Actual cash taxes paid exceed tax expense recognized on P&L.", "#e11d48"),
        ("Working Capital", "Increase in Current Operating Assets (AR, Inventory)", "DEDUCT (–)", "Cash spent to build inventory or uncollected sales revenue.", "#e11d48"),
        ("Working Capital", "Increase in Current Operating Liabilities (AP, Accruals)", "ADD BACK (+)", "Cash conserved by delaying vendor payments or accruing costs.", "#059669")
    ]
    y_row = 310
    for i, (cat, item, adj, rat, col) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="80" y="{y_row}" width="2322" height="75" fill="{bg}" />
  <text x="110" y="{y_row + 47}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">{cat}</text>
  <text x="450" y="{y_row + 47}" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">{item}</text>
  <text x="1200" y="{y_row + 47}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{adj}</text>
  <text x="1450" y="{y_row + 47}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20">{rat}</text>
  <line x1="80" y1="{y_row + 75}" x2="2402" y2="{y_row + 75}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 75

    svg += """
  <!-- Summary Box -->
  <rect x="80" y="1100" width="2322" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1241" y="1145" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Formula: CFO = Net Income + Noncash Charges – Non-Operating Gains (+ Losses) – ΔOperating Assets + ΔOperating Liabilities</text>
  <text x="1241" y="1178" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Both Direct and Indirect methods yield identically matching total Cash Flow from Operating Activities.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/231daaffaea51011dc50.png")
    print(f"Saved 231daaffaea51011dc50.png ({pix.width}x{pix.height})")

def render_7306():
    # Figure 30.2: U.S. GAAP cash flow classification chart (2064 x 1538)
    w, h = 2064, 1538
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1984" height="1458" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1032" y="120" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 30.2: Cash Flow Statement Classification (U.S. GAAP)</text>
  <text x="1032" y="170" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Categorization of Corporate Inflows and Outflows across Operating, Investing, and Financing</text>
  
  <!-- 3 Big Columns: CFO, CFI, CFF -->
  <!-- CFO Column -->
  <rect x="70" y="230" width="600" height="1150" fill="#f8fafc" stroke="#0284c7" stroke-width="3" rx="16" />
  <rect x="70" y="230" width="600" height="70" fill="#0284c7" rx="16" />
  <rect x="70" y="280" width="600" height="20" fill="#0284c7" />
  <text x="370" y="278" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Operating Activities (CFO)</text>
  <text x="370" y="340" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Daily Core Revenue-Producing Activities</text>
  
  <text x="100" y="400" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Cash Inflows (+):</text>
  <text x="100" y="445" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Cash received from customers</text>
  <text x="100" y="490" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Interest received on debt securities</text>
  <text x="100" y="535" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Dividends received on equity investments</text>
  <text x="100" y="580" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Proceeds from trading securities</text>
  
  <line x1="90" y1="620" x2="650" y2="620" stroke="#cbd5e1" stroke-width="2" />
  
  <text x="100" y="665" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Cash Outflows (–):</text>
  <text x="100" y="710" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Cash paid to suppliers for inventory</text>
  <text x="100" y="755" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Cash paid to employees (wages/salaries)</text>
  <text x="100" y="800" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Cash paid for operating expenses</text>
  <text x="100" y="845" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Interest paid on debt obligations</text>
  <text x="100" y="890" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Cash income taxes paid</text>
  <text x="100" y="935" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Purchases of trading securities</text>
  
  <!-- CFI Column -->
  <rect x="732" y="230" width="600" height="1150" fill="#f8fafc" stroke="#059669" stroke-width="3" rx="16" />
  <rect x="732" y="230" width="600" height="70" fill="#059669" rx="16" />
  <rect x="732" y="280" width="600" height="20" fill="#059669" />
  <text x="1032" y="278" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Investing Activities (CFI)</text>
  <text x="1032" y="340" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Acquisition &amp; Disposal of Long-Term Assets</text>
  
  <text x="760" y="400" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Cash Inflows (+):</text>
  <text x="760" y="445" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Proceeds from sale of PP&amp;E</text>
  <text x="760" y="490" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Proceeds from sale of intangible assets</text>
  <text x="760" y="535" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Sale of AFS or HTM securities</text>
  <text x="760" y="580" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Principal collected on loans made to others</text>
  
  <line x1="750" y1="620" x2="1310" y2="620" stroke="#cbd5e1" stroke-width="2" />
  
  <text x="760" y="665" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Cash Outflows (–):</text>
  <text x="760" y="710" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Capital expenditures (Purchase of PP&amp;E)</text>
  <text x="760" y="755" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Acquisition of intangible assets / patents</text>
  <text x="760" y="800" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Purchases of AFS or HTM securities</text>
  <text x="760" y="845" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Cash paid for acquisitions / business combinations</text>
  <text x="760" y="890" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Loans made to other entities (principal)</text>
  
  <!-- CFF Column -->
  <rect x="1394" y="230" width="600" height="1150" fill="#f8fafc" stroke="#d97706" stroke-width="3" rx="16" />
  <rect x="1394" y="230" width="600" height="70" fill="#d97706" rx="16" />
  <rect x="1394" y="280" width="600" height="20" fill="#d97706" />
  <text x="1694" y="278" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Financing Activities (CFF)</text>
  <text x="1694" y="340" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Transactions with Creditors &amp; Shareholders</text>
  
  <text x="1420" y="400" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Cash Inflows (+):</text>
  <text x="1420" y="445" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Proceeds from issuing common/preferred stock</text>
  <text x="1420" y="490" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Proceeds from issuing bonds, notes, debt</text>
  <text x="1420" y="535" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Cash received from bank term borrowings</text>
  
  <line x1="1410" y1="620" x2="1970" y2="620" stroke="#cbd5e1" stroke-width="2" />
  
  <text x="1420" y="665" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Cash Outflows (–):</text>
  <text x="1420" y="710" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Principal repayments on long-term debt</text>
  <text x="1420" y="755" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Principal portion of finance lease payments</text>
  <text x="1420" y="800" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Repurchase of company common stock (Treasury)</text>
  <text x="1420" y="845" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="21">• Cash dividends paid to shareholders</text>
  
  <!-- Note banner -->
  <rect x="70" y="1410" width="1924" height="60" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="10" />
  <text x="1032" y="1448" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Noncash Investing &amp; Financing: Significant noncash transactions (e.g., converting debt to equity) are disclosed in footnotes, not the cash flow body.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/73062f0a11eebaba6246.png")
    print(f"Saved 73062f0a11eebaba6246.png ({pix.width}x{pix.height})")

def render_8ba0():
    # Figure 30.3: Differences Between U.S. GAAP and IFRS Cash Flows (2068 x 1208)
    w, h = 2068, 1208
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1988" height="1128" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1034" y="115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Figure 30.3: Cash Flow Classification: U.S. GAAP vs. IFRS</text>
  <text x="1034" y="160" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">A key difference: U.S. GAAP is strictly prescriptive, whereas IFRS provides accounting policy choice</text>
  
  <!-- Header -->
  <rect x="70" y="210" width="1928" height="65" fill="#0284c7" rx="12" />
  <text x="250" y="253" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Cash Flow Item</text>
  <text x="750" y="253" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">U.S. GAAP Classification</text>
  <text x="1450" y="253" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">IFRS Classification Options</text>
"""
    items = [
        ("Interest Received", "Operating (CFO)", "Operating (CFO) OR Investing (CFI)", "Under IFRS, interest received can be CFI because it represents a return on investment."),
        ("Interest Paid", "Operating (CFO)", "Operating (CFO) OR Financing (CFF)", "Under IFRS, interest paid can be CFF because it is the cost of obtaining debt financing."),
        ("Dividends Received", "Operating (CFO)", "Operating (CFO) OR Investing (CFI)", "Under IFRS, dividends received can be CFI because they represent return on equity investments."),
        ("Dividends Paid", "Financing (CFF)", "Operating (CFO) OR Financing (CFF)", "Under IFRS, dividends paid can be CFO to assist users in assessing capacity to pay dividends out of operating flows."),
        ("Taxes Paid", "Operating (CFO)", "Operating (CFO) unless specifically identified with Investing or Financing", "Under IFRS, capital gains tax on sale of PP&E can be classified under CFI.")
    ]
    y_row = 290
    for i, (item, gaap, ifrs, note) in enumerate(items):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="70" y="{y_row}" width="1928" height="150" fill="{bg}" />
  <text x="100" y="{y_row + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">{item}</text>
  <text x="750" y="{y_row + 55}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">{gaap}</text>
  <text x="1450" y="{y_row + 55}" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">{ifrs}</text>
  <text x="750" y="{y_row + 105}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle" font-style="italic">{note}</text>
  <line x1="70" y1="{y_row + 150}" x2="1998" y2="{y_row + 150}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 155

    svg += """
  <!-- Footer Note -->
  <rect x="70" y="1060" width="1928" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1034" y="1112" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Analyst Rule: When comparing companies under different standards, adjust IFRS cash flows to U.S. GAAP format for true comparability.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/8ba02df1ece03fdf5894.png")
    print(f"Saved 8ba02df1ece03fdf5894.png ({pix.width}x{pix.height})")

def render_123f():
    # Figure 32.2: Effects of Inventory Valuation Methods (2472 x 560)
    w, h = 2472, 560
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="30" y="30" width="2412" height="500" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1236" y="85" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Figure 32.2: Financial Statement Effects of FIFO vs. LIFO (During Inflation &amp; Stable/Growing Quantities)</text>
  
  <!-- Table Header -->
  <rect x="60" y="120" width="2352" height="65" fill="#0284c7" rx="12" />
  <text x="250" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Financial Metric</text>
  <text x="750" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">FIFO (First-In, First-Out)</text>
  <text x="1350" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">LIFO (Last-In, First-Out)</text>
  <text x="1950" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">LIFO Effect / Difference</text>
"""
    rows = [
        ("Cost of Goods Sold (COGS)", "Lower (Oldest cheaper costs to P&L)", "Higher (Most recent expensive costs to P&L)", "LIFO COGS = FIFO COGS – ΔLIFO Reserve", "#e11d48"),
        ("Ending Inventory (Balance Sheet)", "Higher (Recent inventory at current prices)", "Lower (Carried at historical old prices)", "FIFO Inv = LIFO Inv + LIFO Reserve", "#059669"),
        ("Gross Profit & Net Income", "Higher (Lower COGS increases margins)", "Lower (Higher COGS decreases margins)", "LIFO reduces earnings during inflation", "#e11d48"),
        ("Income Taxes Paid", "Higher (Higher taxable income)", "Lower (Tax savings: LIFO conformity rule)", "Cash tax savings is primary reason firms use LIFO", "#059669"),
        ("Cash Flow from Operations (CFO)", "Lower (Higher cash income taxes paid)", "Higher (Lower cash taxes paid = Tax Shield)", "LIFO produces higher real cash flow", "#059669"),
        ("Working Capital", "Higher (Higher ending inventory)", "Lower (Lower inventory valuation)", "LIFO understates current working capital", "#e11d48")
    ]
    y_row = 195
    for i, (m, fifo, lifo, eff, col) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="60" y="{y_row}" width="2352" height="48" fill="{bg}" />
  <text x="90" y="{y_row + 33}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">{m}</text>
  <text x="750" y="{y_row + 33}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{fifo}</text>
  <text x="1350" y="{y_row + 33}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{lifo}</text>
  <text x="1950" y="{y_row + 33}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">{eff}</text>
  <line x1="60" y1="{y_row + 48}" x2="2412" y2="{y_row + 48}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 48

    svg += """
  <!-- Footer Note -->
  <text x="1236" y="505" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Under falling prices (deflation), all relationships reverse completely.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/123fa52a8926520c282f.png")
    print(f"Saved 123fa52a8926520c282f.png ({pix.width}x{pix.height})")

def render_b373():
    # Figure 32.1: Diagram illustrating inventory cost flow under FIFO and LIFO (2070 x 1600)
    w, h = 2070, 1600
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1990" height="1520" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1035" y="125" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 32.1: FIFO vs. LIFO Cost Allocation (Rising Prices)</text>
  <text x="1035" y="175" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Comparison of how purchased inventory batches are allocated between COGS and Ending Inventory</text>
  
  <!-- Left Side: FIFO -->
  <rect x="80" y="240" width="920" height="1180" fill="#f8fafc" stroke="#0284c7" stroke-width="3" rx="16" />
  <rect x="80" y="240" width="920" height="70" fill="#0284c7" rx="16" />
  <rect x="80" y="290" width="920" height="20" fill="#0284c7" />
  <text x="540" y="288" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">FIFO (First-In, First-Out)</text>
  
  <!-- Right Side: LIFO -->
  <rect x="1070" y="240" width="920" height="1180" fill="#f8fafc" stroke="#e11d48" stroke-width="3" rx="16" />
  <rect x="1070" y="240" width="920" height="70" fill="#e11d48" rx="16" />
  <rect x="1070" y="290" width="920" height="20" fill="#e11d48" />
  <text x="1530" y="288" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">LIFO (Last-In, First-Out)</text>
  
  <!-- Batches illustration: -->
  <!-- Batch 1: 100 units @ $10 (Oldest) -->
  <!-- Batch 2: 100 units @ $12 -->
  <!-- Batch 3: 100 units @ $15 (Newest) -->
  <!-- Total purchased: 300 units. Units sold: 200 units. Ending inventory: 100 units. -->
  
  <!-- FIFO Content -->
  <!-- COGS (200 units sold) = Batch 1 ($10) + Batch 2 ($12) = $2,200 -->
  <rect x="120" y="370" width="840" height="380" fill="#eff6ff" stroke="#0284c7" stroke-width="2.5" rx="12" />
  <text x="540" y="420" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">COGS (Oldest Units Sold)</text>
  <rect x="160" y="450" width="760" height="110" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="8" />
  <text x="540" y="495" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Batch 1: 100 units @ $10.00 = $1,000</text>
  <text x="540" y="535" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">(First in → First out to Income Statement)</text>
  
  <rect x="160" y="580" width="760" height="110" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="8" />
  <text x="540" y="625" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Batch 2: 100 units @ $12.00 = $1,200</text>
  <text x="540" y="665" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">(Second in → Second out to Income Statement)</text>
  <text x="540" y="730" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Total FIFO COGS = $2,200 (Lower)</text>
  
  <!-- Ending Inventory (100 units) = Batch 3 ($15) = $1,500 -->
  <rect x="120" y="800" width="840" height="260" fill="#ecfdf5" stroke="#10b981" stroke-width="2.5" rx="12" />
  <text x="540" y="850" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Ending Inventory (Newest Units Retained)</text>
  <rect x="160" y="880" width="760" height="110" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="8" />
  <text x="540" y="925" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Batch 3: 100 units @ $15.00 = $1,500</text>
  <text x="540" y="965" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">(Recent purchase reflects current replacement cost on Balance Sheet)</text>
  <text x="540" y="1035" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Total FIFO Ending Inventory = $1,500 (Higher)</text>
  
  <text x="540" y="1150" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">FIFO Summary: Higher NI ($) | Lower Cash Flow (Taxes)</text>
  
  
  <!-- LIFO Content -->
  <!-- COGS (200 units sold) = Batch 3 ($15) + Batch 2 ($12) = $2,700 -->
  <rect x="1110" y="370" width="840" height="380" fill="#fef2f2" stroke="#ef4444" stroke-width="2.5" rx="12" />
  <text x="1530" y="420" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">COGS (Newest Units Sold)</text>
  <rect x="1150" y="450" width="760" height="110" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="8" />
  <text x="1530" y="495" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Batch 3: 100 units @ $15.00 = $1,500</text>
  <text x="1530" y="535" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">(Last in → First out to Income Statement)</text>
  
  <rect x="1150" y="580" width="760" height="110" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="8" />
  <text x="1530" y="625" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Batch 2: 100 units @ $12.00 = $1,200</text>
  <text x="1530" y="665" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">(Second last in → Second out to Income Statement)</text>
  <text x="1530" y="730" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Total LIFO COGS = $2,700 (Higher by $500)</text>
  
  <!-- Ending Inventory (100 units) = Batch 1 ($10) = $1,000 -->
  <rect x="1110" y="800" width="840" height="260" fill="#fffbeb" stroke="#f59e0b" stroke-width="2.5" rx="12" />
  <text x="1530" y="850" fill="#92400e" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Ending Inventory (Oldest Units Retained)</text>
  <rect x="1150" y="880" width="760" height="110" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="8" />
  <text x="1530" y="925" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Batch 1: 100 units @ $10.00 = $1,000</text>
  <text x="1530" y="965" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">(Oldest historical purchase stays on Balance Sheet)</text>
  <text x="1530" y="1035" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Total LIFO Ending Inventory = $1,000 (Lower by $500)</text>
  
  <text x="1530" y="1150" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">LIFO Summary: Lower NI ($) | Higher Cash Flow (Tax Savings)</text>
  
  <!-- LIFO Reserve Equation Banner -->
  <rect x="80" y="1450" width="1910" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1035" y="1490" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">LIFO Reserve = FIFO Inventory ($1,500) – LIFO Inventory ($1,000) = $500</text>
  <text x="1035" y="1520" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">LIFO COGS ($2,700) = FIFO COGS ($2,200) + ΔLIFO Reserve ($500)</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b37305a00c0bfecd1165.png")
    print(f"Saved b37305a00c0bfecd1165.png ({pix.width}x{pix.height})")

def render_0832():
    # Figure 33.3: Corporate spinoff structure diagram (2225 x 810)
    w, h = 2225, 810
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="2145" height="730" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1112" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Figure 33.3: Corporate Spinoff Transaction Structure</text>
  <text x="1112" y="155" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Parent corporation separates a division into a newly independent company, distributing shares pro-rata</text>
  
  <!-- Left Box: Parent Corporation -->
  <rect x="100" y="240" width="550" height="280" fill="#f8fafc" stroke="#0284c7" stroke-width="3" rx="16" />
  <text x="375" y="300" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Parent Corporation</text>
  <text x="375" y="345" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• Retains core business operations</text>
  <text x="375" y="385" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• Relinquishes control of subsidiary</text>
  <text x="375" y="425" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• No cash transaction / Tax-free</text>
  
  <!-- Center Arrow 1: Assets transferred -->
  <line x1="650" y1="380" x2="850" y2="380" stroke="#0284c7" stroke-width="4" />
  <polygon points="850,380 834,370 834,390" fill="#0284c7" />
  <text x="750" y="360" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Assets &amp; Liabilities</text>
  <text x="750" y="415" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Carved Out</text>
  
  <!-- Middle Box: Spun-Off Entity -->
  <rect x="850" y="240" width="550" height="280" fill="#ecfdf5" stroke="#10b981" stroke-width="3" rx="16" />
  <text x="1125" y="300" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Spun-Off Entity (NewCo)</text>
  <text x="1125" y="345" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• Independent legal corporate identity</text>
  <text x="1125" y="385" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• Separate management and board</text>
  <text x="1125" y="425" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• New ticker listed on public exchange</text>
  
  <!-- Right Box: Shareholders -->
  <rect x="1600" y="240" width="525" height="280" fill="#eff6ff" stroke="#0284c7" stroke-width="3" rx="16" />
  <text x="1862" y="300" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Existing Shareholders</text>
  <text x="1862" y="345" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• Maintain 100% of Parent shares</text>
  <text x="1862" y="385" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• Receive NewCo shares pro-rata</text>
  <text x="1862" y="425" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">• Can trade or hold independently</text>
  
  <!-- Pro-rata distribution arrow -->
  <path d="M 1400 380 Q 1500 380 1600 380" fill="none" stroke="#059669" stroke-width="4" />
  <polygon points="1600,380 1584,370 1584,390" fill="#059669" />
  <text x="1500" y="360" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">100% Pro-Rata</text>
  <text x="1500" y="415" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Share Distribution</text>
  
  <!-- Summary Box -->
  <rect x="100" y="580" width="2025" height="120" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1112" y="625" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Distinctive Feature: Unlike an Equity Carve-Out (which raises cash via an IPO) or a Divestiture (asset sale to third party),</text>
  <text x="1112" y="665" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">a Spinoff generates NO cash for the parent. Instead, it unlocks shareholder value by allowing both businesses to be valued on pure-play multiples.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/08322fe07c856e19deab.png")
    print(f"Saved 08322fe07c856e19deab.png ({pix.width}x{pix.height})")

def render_0e59():
    # Figure 34.1: Financial statement impact table Finance vs Operating Leases (2064 x 920)
    w, h = 2064, 920
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1984" height="840" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1032" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 34.1: Lessee Accounting: Finance vs. Operating Leases</text>
  
  <!-- Table Header -->
  <rect x="70" y="150" width="1924" height="65" fill="#0284c7" rx="12" />
  <text x="220" y="193" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Financial Statement Dimension</text>
  <text x="800" y="193" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Finance Lease (IFRS 16 &amp; U.S. GAAP)</text>
  <text x="1500" y="193" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Operating Lease (U.S. GAAP Only)</text>
"""
    rows = [
        ("Balance Sheet Recognition", "Recognize Right-of-Use (ROU) Asset and Lease Liability at PV of payments", "Recognize Right-of-Use (ROU) Asset and Lease Liability at PV of payments"),
        ("Income Statement Pattern", "Front-loaded expense: Interest Expense (declining) + Amortization (straight-line)", "Level / Constant: Single lease expense (straight-line) recognized each period"),
        ("Operating Income (EBIT / EBITDA)", "Higher: Entire lease payment excluded from operating expenses (interest & deprec.)", "Lower: Entire single lease payment included inside operating expenses"),
        ("Cash Flow from Operations (CFO)", "Higher: Only interest portion is CFO; principal repayment is in CFF", "Lower: Full lease payment is classified as operating cash outflow (CFO)"),
        ("Cash Flow from Financing (CFF)", "Lower: Principal repayment portion reduces CFF each period", "Unaffected: Zero impact on financing cash flows"),
        ("Leverage Ratios (Debt / Equity)", "Higher: Lease liability increases recognized debt obligations", "Higher: Lease liability recognized on balance sheet increases debt")
    ]
    y_row = 230
    for i, (dim, fin, op) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="70" y="{y_row}" width="1924" height="85" fill="{bg}" />
  <text x="100" y="{y_row + 52}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">{dim}</text>
  <text x="800" y="{y_row + 52}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{fin}</text>
  <text x="1500" y="{y_row + 52}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{op}</text>
  <line x1="70" y1="{y_row + 85}" x2="1994" y2="{y_row + 85}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 85

    svg += """
  <!-- Footer Note -->
  <text x="1032" y="835" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Under IFRS 16, all lessee leases are accounted for under the single Finance Lease model (no operating lease classification exists for lessees).</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/0e599b3fe938861a8d0f.png")
    print(f"Saved 0e599b3fe938861a8d0f.png ({pix.width}x{pix.height})")

def render_aa19():
    # Figure 34.2: Lessee lease accounting diagram detailing right-of-use asset and lease liability (1787 x 710)
    w, h = 1787, 710
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1707" height="630" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="893" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 34.2: Amortization of Right-of-Use Asset vs. Lease Liability</text>
  <text x="893" y="155" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Initial recognition at PV of lease payments; divergence during lease term</text>
  
  <!-- Axes -->
  <line x1="180" y1="560" x2="1600" y2="560" stroke="#0f172a" stroke-width="4" />
  <line x1="180" y1="560" x2="180" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="180" y="175" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Carrying Value ($)</text>
  <text x="1600" y="605" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">Lease Term (Years)</text>
  
  <!-- Inception Point: PV of lease payments -->
  <circle cx="180" cy="240" r="9" fill="#0f172a" />
  <text x="160" y="248" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="end">PV of Lease Payments</text>
  <text x="180" y="605" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Inception (t=0)</text>
  
  <!-- Right-of-Use Asset: Straight-line depreciation to 0 -->
  <line x1="180" y1="240" x2="1500" y2="560" stroke="#0284c7" stroke-width="5" />
  <text x="1250" y="440" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">ROU Asset (Straight-Line Amortization)</text>
  
  <!-- Lease Liability: Amortized cost curve (drops slower initially, then accelerates) -->
  <path d="M 180 240 Q 900 320 1500 560" fill="none" stroke="#e11d48" stroke-width="5" />
  <text x="800" y="320" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Lease Liability (Effective Interest Amortization)</text>
  
  <!-- Maturity Point -->
  <circle cx="1500" cy="560" r="9" fill="#059669" />
  <text x="1500" y="605" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Lease Expiration ($0)</text>
  
  <!-- Divergence Callout -->
  <rect x="500" y="390" width="500" height="60" fill="#eff6ff" stroke="#cbd5e1" stroke-width="1.5" rx="8" />
  <text x="750" y="428" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Carrying Value of ROU Asset &lt; Lease Liability</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/aa19dd3e7ccbe523e642.png")
    print(f"Saved aa19dd3e7ccbe523e642.png ({pix.width}x{pix.height})")

def render_19ce():
    # Line chart comparing straight-line accounting depreciation against accelerated (1690 x 1182)
    w, h = 1690, 1182
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1610" height="1102" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="845" y="115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Depreciation: Straight-Line vs. Accelerated (DDB)</text>
  <text x="845" y="160" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Annual Depreciation Expense and Creation of Deferred Tax Liabilities (DTL)</text>
  
  <!-- Axes -->
  <line x1="160" y1="920" x2="1520" y2="920" stroke="#0f172a" stroke-width="4" />
  <line x1="160" y1="920" x2="160" y2="220" stroke="#0f172a" stroke-width="4" />
  <text x="160" y="195" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Annual Depreciation Expense ($)</text>
  <text x="1520" y="965" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">Year</text>
  
  <!-- Year markers 1 to 5 -->
  <!-- x = 320, 580, 840, 1100, 1360 -->
  <line x1="320" y1="920" x2="320" y2="935" stroke="#0f172a" stroke-width="3" />
  <line x1="580" y1="920" x2="580" y2="935" stroke="#0f172a" stroke-width="3" />
  <line x1="840" y1="920" x2="840" y2="935" stroke="#0f172a" stroke-width="3" />
  <line x1="1100" y1="920" x2="1100" y2="935" stroke="#0f172a" stroke-width="3" />
  <line x1="1360" y1="920" x2="1360" y2="935" stroke="#0f172a" stroke-width="3" />
  
  <text x="320" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Year 1</text>
  <text x="580" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Year 2</text>
  <text x="840" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Year 3</text>
  <text x="1100" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Year 4</text>
  <text x="1360" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Year 5</text>
  
  <!-- Straight-Line (Constant horizontal line at y=580) -->
  <line x1="200" y1="580" x2="1480" y2="580" stroke="#0284c7" stroke-width="6" />
  <text x="1490" y="588" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Straight-Line (Financial Reporting)</text>
  
  <!-- Accelerated Depreciation (DDB: starts high at y=300, drops to y=820) -->
  <path d="M 220 300 Q 580 480 840 680 T 1420 840" fill="none" stroke="#e11d48" stroke-width="6" />
  <text x="1430" y="845" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Accelerated / MACRS (Tax Return)</text>
  
  <!-- Shaded Area 1: DTL Created (Years 1-2) -->
  <rect x="240" y="380" width="380" height="90" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="10" />
  <text x="430" y="420" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Tax Deprec &gt; Book Deprec</text>
  <text x="430" y="450" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">→ Creates Deferred Tax Liability (DTL)</text>
  
  <!-- Shaded Area 2: DTL Reverses (Years 4-5) -->
  <rect x="940" y="650" width="380" height="90" fill="#eff6ff" stroke="#0284c7" stroke-width="2" rx="10" />
  <text x="1130" y="690" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Book Deprec &gt; Tax Deprec</text>
  <text x="1130" y="720" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">→ DTL Reverses (Cash Taxes Rise)</text>
  
  <!-- Bottom summary banner -->
  <rect x="160" y="1010" width="1360" height="90" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="840" y="1050" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Core Tax Principle: Accelerated tax depreciation defers cash taxes into the future, creating an interest-free loan from the government.</text>
  <text x="840" y="1080" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Total cumulative depreciation across asset life is identical under both accounting methods.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/19cea061ab7f4e0a9e99.png")
    print(f"Saved 19cea061ab7f4e0a9e99.png ({pix.width}x{pix.height})")

def render_dc6c():
    # Figure 35.1: Matrix table comparing balance sheet carrying value to tax base (2160 x 700)
    w, h = 2160, 700
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="30" y="30" width="2100" height="640" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1080" y="95" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 35.1: Deferred Tax Matrix: Carrying Value vs. Tax Base</text>
  
  <!-- Table Header -->
  <rect x="60" y="140" width="2040" height="70" fill="#0284c7" rx="12" />
  <text x="250" y="185" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Balance Sheet Item</text>
  <text x="750" y="185" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Carrying Value vs. Tax Base</text>
  <text x="1350" y="185" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Deferred Tax Result</text>
  <text x="1850" y="185" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Typical Real-World Example</text>
"""
    rows = [
        ("Asset", "Carrying Value &gt; Tax Base", "Deferred Tax Liability (DTL)", "Accelerated depreciation for tax, straight-line for books", "#e11d48"),
        ("Asset", "Carrying Value &lt; Tax Base", "Deferred Tax Asset (DTA)", "Impairment loss recognized on books but not yet deductible for tax", "#059669"),
        ("Liability", "Carrying Value &gt; Tax Base", "Deferred Tax Asset (DTA)", "Warranty reserves or unearned revenue taxed on receipt", "#059669"),
        ("Liability", "Carrying Value &lt; Tax Base", "Deferred Tax Liability (DTL)", "Research and development costs capitalized for tax purposes", "#e11d48")
    ]
    y_row = 220
    for i, (item, rel, res, ex, col) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="60" y="{y_row}" width="2040" height="85" fill="{bg}" />
  <text x="100" y="{y_row + 52}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">{item}</text>
  <text x="750" y="{y_row + 52}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">{rel}</text>
  <text x="1350" y="{y_row + 52}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">{res}</text>
  <text x="1850" y="{y_row + 52}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">{ex}</text>
  <line x1="60" y1="{y_row + 85}" x2="2100" y2="{y_row + 85}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 85

    svg += """
  <!-- Footer Note -->
  <text x="1080" y="605" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Rule of Thumb: DTA represents future tax deductions/savings; DTL represents future cash tax obligations.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/dc6c750096c7c0ed372b.png")
    print(f"Saved dc6c750096c7c0ed372b.png ({pix.width}x{pix.height})")

def render_fc07():
    # Figure 36.1: Spectrum of financial reporting quality (2422 x 1052)
    w, h = 2422, 1052
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2322" height="952" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1211" y="125" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 36.1: The Spectrum of Financial Reporting Quality</text>
  <text x="1211" y="175" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Evaluating reporting compliance and earnings quality from superior transparency to outright fraud</text>
  
  <!-- Spectrum Arrow Bar -->
  <rect x="100" y="240" width="2222" height="40" fill="url(#grad)" rx="8" />
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981" />
      <stop offset="35%" stop-color="#0284c7" />
      <stop offset="65%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#ef4444" />
    </linearGradient>
  </defs>
  
  <text x="120" y="225" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Highest Quality (Transparent &amp; Sustainable)</text>
  <text x="2300" y="225" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="end">Lowest Quality (Fraudulent)</text>
  
  <!-- 5 Quality Tier Cards -->
  <!-- Tier 1 -->
  <rect x="100" y="320" width="420" height="520" fill="#f0fdf4" stroke="#10b981" stroke-width="3" rx="14" />
  <text x="310" y="375" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Level 1: High Quality</text>
  <text x="310" y="420" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">GAAP Compliant &amp; High Earnings Quality</text>
  <text x="130" y="480" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Compliant with GAAP/IFRS</text>
  <text x="130" y="525" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Unbiased, decision-useful</text>
  <text x="130" y="570" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Sustainable earnings &amp; cash flows</text>
  <text x="130" y="615" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Adequate return on capital</text>
  
  <!-- Tier 2 -->
  <rect x="550" y="320" width="420" height="520" fill="#f0f9ff" stroke="#0284c7" stroke-width="3" rx="14" />
  <text x="760" y="375" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Level 2: Modest Quality</text>
  <text x="760" y="420" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">GAAP Compliant but Low Earnings Quality</text>
  <text x="580" y="480" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Financial reporting is honest</text>
  <text x="580" y="525" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Underlying earnings are weak</text>
  <text x="580" y="570" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Non-sustainable return on capital</text>
  <text x="580" y="615" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Earnings below cost of capital</text>
  
  <!-- Tier 3 -->
  <rect x="1000" y="320" width="420" height="520" fill="#fffbeb" stroke="#f59e0b" stroke-width="3" rx="14" />
  <text x="1210" y="375" fill="#92400e" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Level 3: Biased Choices</text>
  <text x="1210" y="420" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Within GAAP but Biased Accounting</text>
  <text x="1030" y="480" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Aggressive or conservative bias</text>
  <text x="1030" y="525" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Aggressive: inflate current earnings</text>
  <text x="1030" y="570" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Conservative: delay recognition</text>
  <text x="1030" y="615" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Earnings smoothing tactics</text>
  
  <!-- Tier 4 -->
  <rect x="1450" y="320" width="420" height="520" fill="#fef2f2" stroke="#ef4444" stroke-width="3" rx="14" />
  <text x="1660" y="375" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Level 4: Non-Compliant</text>
  <text x="1660" y="420" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">GAAP Departures / Misstatements</text>
  <text x="1480" y="480" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Non-compliant accounting</text>
  <text x="1480" y="525" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Improper revenue recognition</text>
  <text x="1480" y="570" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Capitalizing operating costs</text>
  <text x="1480" y="615" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Requires financial restatement</text>
  
  <!-- Tier 5 -->
  <rect x="1900" y="320" width="420" height="520" fill="#fdf2f8" stroke="#be185d" stroke-width="3" rx="14" />
  <text x="2110" y="375" fill="#831843" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Level 5: Fictitious</text>
  <text x="2110" y="420" fill="#be185d" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Outright Fraud &amp; Embezzlement</text>
  <text x="1930" y="480" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Fabricated sales transactions</text>
  <text x="1930" y="525" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Fictitious assets recorded</text>
  <text x="1930" y="570" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Off-balance sheet sham entities</text>
  <text x="1930" y="615" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20">• Severe criminal liability</text>
  
  <!-- Footer Note -->
  <rect x="100" y="870" width="2220" height="75" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1211" y="915" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Key Distinction: Financial reporting quality concerns how faithfully statements reflect reality; Earnings quality concerns profitability and sustainability.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/fc07326a2f0b8fbbbfb4.png")
    print(f"Saved fc07326a2f0b8fbbbfb4.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_231d()
    render_7306()
    render_8ba0()
    render_123f()
    render_b373()
    render_0832()
    render_0e59()
    render_aa19()
    render_19ce()
    render_dc6c()
    render_fc07()
