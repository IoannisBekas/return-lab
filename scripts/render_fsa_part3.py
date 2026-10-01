import fitz

def render_a487():
    # Figure 37.1: Vertical common-size balance sheet (2285 x 2087)
    w, h = 2285, 2087
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2185" height="1987" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1142" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 37.1: Vertical Common-Size Balance Sheet</text>
  <text x="1142" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">All line items expressed as a percentage of Total Assets across three consecutive fiscal years</text>
  
  <!-- Table Header -->
  <rect x="80" y="230" width="2125" height="65" fill="#0284c7" rx="12" />
  <text x="250" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Balance Sheet Item</text>
  <text x="850" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Year 1 ($M)</text>
  <text x="1150" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Year 1 (%)</text>
  <text x="1450" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Year 2 (%)</text>
  <text x="1750" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Year 3 (%)</text>
  <text x="2000" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Trend</text>
"""
    items = [
        ("Cash and Cash Equivalents", "$1,250", "12.5%", "14.2%", "16.8%", "Liquidity expanding ↗"),
        ("Marketable Securities", "$800", "8.0%", "7.5%", "6.2%", "Portfolio reallocation ↘"),
        ("Accounts Receivable (Net)", "$2,100", "21.0%", "19.8%", "18.5%", "Improved collection cycle ↘"),
        ("Inventories", "$1,650", "16.5%", "15.0%", "13.5%", "Lean inventory turnover ↘"),
        ("Other Current Assets", "$400", "4.0%", "3.5%", "3.0%", "Stable ↔"),
        ("Total Current Assets", "$6,200", "62.0%", "60.0%", "58.0%", "High liquidity ↘"),
        ("Property, Plant & Equipment (Net)", "$3,100", "31.0%", "32.5%", "34.0%", "Capital investment ↗"),
        ("Goodwill & Intangible Assets", "$700", "7.0%", "7.5%", "8.0%", "Acquisition activity ↗"),
        ("TOTAL ASSETS", "$10,000", "100.0%", "100.0%", "100.0%", "Common-size Base = 100%"),
        ("Accounts Payable", "$1,400", "14.0%", "13.2%", "12.5%", "Supplier terms steady ↘"),
        ("Short-Term Notes Payable", "$600", "6.0%", "5.5%", "4.0%", "Short-term debt reduced ↘"),
        ("Current Maturities of Long-Term Debt", "$500", "5.0%", "4.5%", "4.0%", "Maturing debt paid ↘"),
        ("Total Current Liabilities", "$2,500", "25.0%", "23.2%", "20.5%", "Reduced short-term risk ↘"),
        ("Long-Term Debt", "$3,500", "35.0%", "33.8%", "31.5%", "Deleveraging ↘"),
        ("Deferred Tax Liabilities", "$400", "4.0%", "4.2%", "4.5%", "Capital investments ↗"),
        ("Total Liabilities", "$6,400", "64.0%", "61.2%", "56.5%", "Total leverage reduced ↘"),
        ("Common Stock & APIC", "$2,000", "20.0%", "19.5%", "19.0%", "No dilutive issuance ↔"),
        ("Retained Earnings", "$1,600", "16.0%", "19.3%", "24.5%", "Organic equity growth ↗"),
        ("TOTAL LIABILITIES & EQUITY", "$10,000", "100.0%", "100.0%", "100.0%", "Common-size Base = 100%")
    ]
    y_row = 310
    for i, (name, val, y1, y2, y3, tr) in enumerate(items):
        is_sub = "TOTAL" in name
        bg = "#e2e8f0" if is_sub else ("#f8fafc" if i % 2 == 0 else "#ffffff")
        fw = "bold" if is_sub else "normal"
        col = "#0284c7" if is_sub else "#0f172a"
        svg += f"""
  <rect x="80" y="{y_row}" width="2125" height="70" fill="{bg}" />
  <text x="110" y="{y_row + 45}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="{fw}">{name}</text>
  <text x="850" y="{y_row + 45}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{val}</text>
  <text x="1150" y="{y_row + 45}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="{fw}" text-anchor="middle">{y1}</text>
  <text x="1450" y="{y_row + 45}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="{fw}" text-anchor="middle">{y2}</text>
  <text x="1750" y="{y_row + 45}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="{fw}" text-anchor="middle">{y3}</text>
  <text x="2000" y="{y_row + 45}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">{tr}</text>
  <line x1="80" y1="{y_row + 70}" x2="2205" y2="{y_row + 70}" stroke="#cbd5e1" stroke-width="1.5" />
"""
        y_row += 72

    svg += """
  <!-- Summary Footer -->
  <rect x="80" y="1880" width="2125" height="75" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1142" y="1928" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Analytical Utility: Vertical common-size balance sheets normalize for company size, enabling cross-sectional and time-series structural comparison.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/a487e195393d5926f459.png")
    print(f"Saved a487e195393d5926f459.png ({pix.width}x{pix.height})")

def render_5418():
    # Figure 37.1 (cont.): Vertical common-size income statement (2290 x 1982)
    w, h = 2290, 1982
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2190" height="1882" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1145" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 37.1 (cont.): Vertical Common-Size Income Statement</text>
  <text x="1145" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">All line items expressed as a percentage of Total Revenue / Sales across three consecutive fiscal years</text>
  
  <!-- Table Header -->
  <rect x="80" y="230" width="2130" height="65" fill="#0284c7" rx="12" />
  <text x="250" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Income Statement Line Item</text>
  <text x="850" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Year 1 ($M)</text>
  <text x="1150" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Year 1 (%)</text>
  <text x="1450" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Year 2 (%)</text>
  <text x="1750" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Year 3 (%)</text>
  <text x="2000" y="273" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Margin Trend</text>
"""
    items = [
        ("Revenue (Sales)", "$25,000", "100.0%", "100.0%", "100.0%", "Base = 100.0%"),
        ("Cost of Goods Sold (COGS)", "$15,000", "60.0%", "58.5%", "56.0%", "Input efficiency ↗"),
        ("GROSS PROFIT", "$10,000", "40.0%", "41.5%", "44.0%", "Gross margin expanding ↗"),
        ("Selling, General & Administrative (SG&A)", "$4,250", "17.0%", "16.8%", "16.5%", "Operating leverage ↗"),
        ("Research & Development (R&D)", "$1,500", "6.0%", "6.2%", "6.5%", "Innovation investment ↗"),
        ("Depreciation & Amortization Expense", "$1,000", "4.0%", "4.0%", "4.0%", "Stable asset intensity ↔"),
        ("OPERATING INCOME (EBIT)", "$3,250", "13.0%", "14.5%", "17.0%", "Operating margin expanding ↗"),
        ("Interest Expense", "$500", "2.0%", "1.8%", "1.4%", "Debt service declining ↘"),
        ("Interest Income", "$125", "0.5%", "0.6%", "0.8%", "Higher cash balances ↗"),
        ("INCOME BEFORE TAXES (EBT)", "$2,875", "11.5%", "13.3%", "16.4%", "Pre-tax profitability ↗"),
        ("Income Tax Expense", "$690", "2.8%", "3.1%", "3.8%", "Effective tax rate ~23–24%"),
        ("NET INCOME", "$2,185", "8.7%", "10.2%", "12.6%", "Net profit margin expanding ↗")
    ]
    y_row = 310
    for i, (name, val, y1, y2, y3, tr) in enumerate(items):
        is_bold = name.isupper()
        bg = "#e2e8f0" if is_bold else ("#f8fafc" if i % 2 == 0 else "#ffffff")
        fw = "bold" if is_bold else "normal"
        col = "#0284c7" if is_bold else "#0f172a"
        svg += f"""
  <rect x="80" y="{y_row}" width="2130" height="95" fill="{bg}" />
  <text x="110" y="{y_row + 58}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="{fw}">{name}</text>
  <text x="850" y="{y_row + 58}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">{val}</text>
  <text x="1150" y="{y_row + 58}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="{fw}" text-anchor="middle">{y1}</text>
  <text x="1450" y="{y_row + 58}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="{fw}" text-anchor="middle">{y2}</text>
  <text x="1750" y="{y_row + 58}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="{fw}" text-anchor="middle">{y3}</text>
  <text x="2000" y="{y_row + 58}" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{tr}</text>
  <line x1="80" y1="{y_row + 95}" x2="2210" y2="{y_row + 95}" stroke="#cbd5e1" stroke-width="1.5" />
"""
        y_row += 100

    svg += """
  <!-- Summary Footer -->
  <rect x="80" y="1750" width="2130" height="90" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1145" y="1795" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Common-Size Profitability Trend: Expanding Gross Margin (+4.0%) and Operating Leverage increased Net Profit Margin from 8.7% to 12.6%.</text>
  <text x="1145" y="1825" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Vertical common-size income statement isolates operational cost improvements from revenue scale effects.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/54183e56771cf041f20a.png")
    print(f"Saved 54183e56771cf041f20a.png ({pix.width}x{pix.height})")

def render_5ed7():
    # Figure 37.2: Horizontal common-size balance sheet data table (1672 x 555)
    w, h = 1672, 555
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="30" y="30" width="1612" height="495" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="836" y="85" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Figure 37.2: Horizontal Common-Size Balance Sheet Data</text>
  
  <!-- Table Header -->
  <rect x="60" y="120" width="1552" height="65" fill="#0284c7" rx="12" />
  <text x="220" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Balance Sheet Item</text>
  <text x="600" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Base Year (Year 1)</text>
  <text x="950" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Year 2 Index (Base = 100)</text>
  <text x="1350" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Year 3 Index (Base = 100)</text>
"""
    rows = [
        ("Cash and Cash Equivalents", "$1,000  (100.0)", "125.0  (+25.0%)", "155.0  (+55.0%)"),
        ("Accounts Receivable", "$2,000  (100.0)", "110.0  (+10.0%)", "122.0  (+22.0%)"),
        ("Inventory", "$1,500  (100.0)", "105.0  (+5.0%)", "112.0  (+12.0%)"),
        ("Net Property, Plant & Equipment", "$5,000  (100.0)", "108.0  (+8.0%)", "120.0  (+20.0%)"),
        ("Total Assets", "$9,500  (100.0)", "110.5  (+10.5%)", "124.5  (+24.5%)")
    ]
    y_row = 195
    for i, (item, b, y2, y3) in enumerate(rows):
        is_tot = "Total" in item
        bg = "#e2e8f0" if is_tot else ("#f8fafc" if i % 2 == 0 else "#ffffff")
        fw = "bold" if is_tot else "normal"
        col = "#0284c7" if is_tot else "#0f172a"
        svg += f"""
  <rect x="60" y="{y_row}" width="1552" height="50" fill="{bg}" />
  <text x="90" y="{y_row + 35}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="{fw}">{item}</text>
  <text x="600" y="{y_row + 35}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{b}</text>
  <text x="950" y="{y_row + 35}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="{fw}" text-anchor="middle">{y2}</text>
  <text x="1350" y="{y_row + 35}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="{fw}" text-anchor="middle">{y3}</text>
  <line x1="60" y1="{y_row + 50}" x2="1612" y2="{y_row + 50}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 50

    svg += """
  <!-- Footer Note -->
  <text x="836" y="500" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Horizontal common-size analysis highlights growth rates relative to a base period, identifying emerging operational imbalances.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/5ed743d32ffb2b595cd6.png")
    print(f"Saved 5ed743d32ffb2b595cd6.png ({pix.width}x{pix.height})")

def render_f61a():
    # Figure 37.3: Stacked bar chart composition of current assets (1817 x 1587)
    w, h = 1817, 1587
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1717" height="1487" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="908" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 37.3: Current Asset Composition (Stacked Bar Chart)</text>
  <text x="908" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Proportional breakdown of Current Assets across Year 1, Year 2, and Year 3</text>
  
  <!-- Legend -->
  <rect x="350" y="230" width="1117" height="60" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="10" />
  <rect x="380" y="247" width="26" height="26" fill="#0284c7" rx="4" />
  <text x="420" y="268" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Cash &amp; Equivalents</text>
  
  <rect x="680" y="247" width="26" height="26" fill="#059669" rx="4" />
  <text x="720" y="268" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Marketable Securities</text>
  
  <rect x="990" y="247" width="26" height="26" fill="#f59e0b" rx="4" />
  <text x="1030" y="268" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Accounts Receivable</text>
  
  <rect x="1300" y="247" width="26" height="26" fill="#e11d48" rx="4" />
  <text x="1340" y="268" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Inventory</text>
  
  <!-- Axes -->
  <line x1="200" y1="1280" x2="1600" y2="1280" stroke="#0f172a" stroke-width="4" />
  <line x1="200" y1="1280" x2="200" y2="340" stroke="#0f172a" stroke-width="4" />
  <text x="200" y="320" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">% of Total Current Assets</text>
  
  <!-- Y-axis ticks 0% to 100% -->
  <!-- 0% at y=1280, 25% at y=1045, 50% at y=810, 75% at y=575, 100% at y=340 -->
  <line x1="190" y1="1280" x2="200" y2="1280" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="1045" x2="200" y2="1045" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="810" x2="200" y2="810" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="575" x2="200" y2="575" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="340" x2="200" y2="340" stroke="#0f172a" stroke-width="3" />
  
  <text x="175" y="1290" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">0%</text>
  <text x="175" y="1055" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">25%</text>
  <text x="175" y="820" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">50%</text>
  <text x="175" y="585" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">75%</text>
  <text x="175" y="350" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">100%</text>
  
  <!-- Horizontal gridlines -->
  <line x1="200" y1="1045" x2="1600" y2="1045" stroke="#f1f5f9" stroke-width="2" />
  <line x1="200" y1="810" x2="1600" y2="810" stroke="#f1f5f9" stroke-width="2" />
  <line x1="200" y1="575" x2="1600" y2="575" stroke="#f1f5f9" stroke-width="2" />
  <line x1="200" y1="340" x2="1600" y2="340" stroke="#f1f5f9" stroke-width="2" />
  
  <!-- 3 Bars: Width = 260. Centers: x = 450, 900, 1350 -->
  <!-- BAR 1: Year 1 (Cash 20%, Sec 13%, AR 34%, Inv 33%) -->
  <!-- Inv: 0 to 33% -> y from 1280 to 970 (h=310) -->
  <rect x="320" y="970" width="260" height="310" fill="#e11d48" />
  <text x="450" y="1135" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Inv: 33%</text>
  <!-- AR: 33% to 67% -> y from 970 to 650 (h=320) -->
  <rect x="320" y="650" width="260" height="320" fill="#f59e0b" />
  <text x="450" y="820" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">AR: 34%</text>
  <!-- Sec: 67% to 80% -> y from 650 to 528 (h=122) -->
  <rect x="320" y="528" width="260" height="122" fill="#059669" />
  <text x="450" y="595" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Sec: 13%</text>
  <!-- Cash: 80% to 100% -> y from 528 to 340 (h=188) -->
  <rect x="320" y="340" width="260" height="188" fill="#0284c7" />
  <text x="450" y="440" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Cash: 20%</text>
  <text x="450" y="1330" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Year 1</text>
  
  <!-- BAR 2: Year 2 (Cash 24%, Sec 12%, AR 33%, Inv 31%) -->
  <rect x="770" y="989" width="260" height="291" fill="#e11d48" />
  <text x="900" y="1145" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Inv: 31%</text>
  
  <rect x="770" y="679" width="260" height="310" fill="#f59e0b" />
  <text x="900" y="845" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">AR: 33%</text>
  
  <rect x="770" y="566" width="260" height="113" fill="#059669" />
  <text x="900" y="630" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Sec: 12%</text>
  
  <rect x="770" y="340" width="260" height="226" fill="#0284c7" />
  <text x="900" y="460" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Cash: 24%</text>
  <text x="900" y="1330" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Year 2</text>
  
  <!-- BAR 3: Year 3 (Cash 29%, Sec 11%, AR 32%, Inv 28%) -->
  <rect x="1220" y="1017" width="260" height="263" fill="#e11d48" />
  <text x="1350" y="1160" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Inv: 28%</text>
  
  <rect x="1220" y="716" width="260" height="301" fill="#f59e0b" />
  <text x="1350" y="875" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">AR: 32%</text>
  
  <rect x="1220" y="613" width="260" height="103" fill="#059669" />
  <text x="1350" y="670" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Sec: 11%</text>
  
  <rect x="1220" y="340" width="260" height="273" fill="#0284c7" />
  <text x="1350" y="485" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Cash: 29%</text>
  <text x="1350" y="1330" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Year 3</text>
  
  <!-- Summary Box -->
  <rect x="200" y="1390" width="1400" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="908" y="1435" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Trend Analysis: Cash proportion expands from 20% to 29%, while inventory declines from 33% to 28%.</text>
  <text x="908" y="1468" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Indicates strengthening liquidity and more conservative short-term asset management.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/f61a2df07126ade2843a.png")
    print(f"Saved f61a2df07126ade2843a.png ({pix.width}x{pix.height})")

def render_738b():
    # Figure 37.3 (cont.) / 37.4: Stacked bar chart / line graph trends in capital structure (1825 x 1572)
    w, h = 1825, 1572
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1725" height="1472" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="912" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 37.4: Capital Structure Composition Over Time</text>
  <text x="912" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Proportional financing breakdown: Short-Term Debt, Long-Term Debt, and Common Equity</text>
  
  <!-- Legend -->
  <rect x="400" y="230" width="1025" height="60" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="10" />
  <rect x="450" y="247" width="26" height="26" fill="#0284c7" rx="4" />
  <text x="490" y="268" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Common Equity</text>
  
  <rect x="760" y="247" width="26" height="26" fill="#e11d48" rx="4" />
  <text x="800" y="268" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Long-Term Debt</text>
  
  <rect x="1080" y="247" width="26" height="26" fill="#f59e0b" rx="4" />
  <text x="1120" y="268" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Short-Term Debt</text>
  
  <!-- Axes -->
  <line x1="200" y1="1280" x2="1620" y2="1280" stroke="#0f172a" stroke-width="4" />
  <line x1="200" y1="1280" x2="200" y2="340" stroke="#0f172a" stroke-width="4" />
  <text x="200" y="320" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">% of Total Capital</text>
  
  <!-- Ticks -->
  <line x1="190" y1="1280" x2="200" y2="1280" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="1045" x2="200" y2="1045" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="810" x2="200" y2="810" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="575" x2="200" y2="575" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="340" x2="200" y2="340" stroke="#0f172a" stroke-width="3" />
  
  <text x="175" y="1290" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">0%</text>
  <text x="175" y="1055" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">25%</text>
  <text x="175" y="820" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">50%</text>
  <text x="175" y="585" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">75%</text>
  <text x="175" y="350" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="end">100%</text>
  
  <!-- Horizontal gridlines -->
  <line x1="200" y1="1045" x2="1620" y2="1045" stroke="#f1f5f9" stroke-width="2" />
  <line x1="200" y1="810" x2="1620" y2="810" stroke="#f1f5f9" stroke-width="2" />
  <line x1="200" y1="575" x2="1620" y2="575" stroke="#f1f5f9" stroke-width="2" />
  <line x1="200" y1="340" x2="1620" y2="340" stroke="#f1f5f9" stroke-width="2" />
  
  <!-- 3 Bars: Centers at x = 450, 910, 1370 -->
  <!-- BAR 1: Year 1 (ST Debt 15%, LT Debt 50%, Equity 35%) -->
  <rect x="320" y="1139" width="260" height="141" fill="#f59e0b" />
  <text x="450" y="1215" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">ST Debt: 15%</text>
  
  <rect x="320" y="669" width="260" height="470" fill="#e11d48" />
  <text x="450" y="915" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">LT Debt: 50%</text>
  
  <rect x="320" y="340" width="260" height="329" fill="#0284c7" />
  <text x="450" y="515" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Equity: 35%</text>
  <text x="450" y="1330" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Year 1</text>
  
  <!-- BAR 2: Year 2 (ST Debt 12%, LT Debt 46%, Equity 42%) -->
  <rect x="780" y="1167" width="260" height="113" fill="#f59e0b" />
  <text x="910" y="1230" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">ST Debt: 12%</text>
  
  <rect x="780" y="735" width="260" height="432" fill="#e11d48" />
  <text x="910" y="960" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">LT Debt: 46%</text>
  
  <rect x="780" y="340" width="260" height="395" fill="#0284c7" />
  <text x="910" y="545" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Equity: 42%</text>
  <text x="910" y="1330" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Year 2</text>
  
  <!-- BAR 3: Year 3 (ST Debt 8%, LT Debt 40%, Equity 52%) -->
  <rect x="1240" y="1205" width="260" height="75" fill="#f59e0b" />
  <text x="1370" y="1250" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">ST: 8%</text>
  
  <rect x="1240" y="829" width="260" height="376" fill="#e11d48" />
  <text x="1370" y="1025" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">LT Debt: 40%</text>
  
  <rect x="1240" y="340" width="260" height="489" fill="#0284c7" />
  <text x="1370" y="595" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Equity: 52%</text>
  <text x="1370" y="1330" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Year 3</text>
  
  <!-- Summary Box -->
  <rect x="200" y="1390" width="1420" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="910" y="1435" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Capital Structure Trend: Firm progressively deleveraged over the 3-year period.</text>
  <text x="910" y="1468" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Equity increased from 35% to 52%, while total debt declined from 65% to 48%, strengthening solvency.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/738bcc4c48c2bf85ae21.png")
    print(f"Saved 738bcc4c48c2bf85ae21.png ({pix.width}x{pix.height})")

def render_64b3():
    # Figure 42.1: Comparison reference table classifying American Depository Receipts (2068 x 598)
    w, h = 2068, 598
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="30" y="30" width="2008" height="538" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1034" y="85" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Figure 42.1: American Depository Receipts (ADRs) Classification</text>
  
  <!-- Table Header -->
  <rect x="60" y="120" width="1948" height="65" fill="#0284c7" rx="12" />
  <text x="200" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">ADR Program Type</text>
  <text x="560" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Trading Market</text>
  <text x="960" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">SEC Registration (Form F-6)</text>
  <text x="1400" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Capital Raising (New Shares)?</text>
  <text x="1800" y="163" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Reporting Compliance</text>
"""
    rows = [
        ("Rule 144A (Private)", "Private Portal (QIBs only)", "Exempt from SEC registration", "Yes (Private placement to QIBs)", "Home country standards"),
        ("Level I (Unsponsored)", "Over-the-Counter (OTC Pink)", "Basic Form F-6; No Form 20-F", "No (Existing shares only)", "Exemption under Rule 12g3-2(b)"),
        ("Level II (Sponsored)", "Major Exchanges (NYSE, NASDAQ)", "Full SEC registration (Form 20-F)", "No (Existing shares only)", "Full SEC annual reporting (20-F)"),
        ("Level III (Sponsored)", "Major Exchanges (NYSE, NASDAQ)", "Full SEC registration (Form F-1/20-F)", "Yes (Public equity offering in U.S.)", "Highest compliance (Full GAAP/IFRS)")
    ]
    y_row = 195
    for i, (prog, mkt, sec, cap, rep) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="60" y="{y_row}" width="1948" height="75" fill="{bg}" />
  <text x="90" y="{y_row + 47}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">{prog}</text>
  <text x="560" y="{y_row + 47}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{mkt}</text>
  <text x="960" y="{y_row + 47}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{sec}</text>
  <text x="1400" y="{y_row + 47}" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{cap}</text>
  <text x="1800" y="{y_row + 47}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{rep}</text>
  <line x1="60" y1="{y_row + 75}" x2="2008" y2="{y_row + 75}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 75

    svg += """
  <!-- Footer Note -->
  <text x="1034" y="535" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Takeaway: Only Level III ADRs and Rule 144A offerings permit foreign corporations to raise new capital in the United States.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/64b39c2a18f778e736ac.png")
    print(f"Saved 64b39c2a18f778e736ac.png ({pix.width}x{pix.height})")

def render_8378():
    # Figure 44.1: Porter's generic competitive strategies grid (2432 x 2788)
    w, h = 2432, 2788
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="60" y="60" width="2312" height="2668" fill="#ffffff" stroke="#cbd5e1" stroke-width="4" rx="24" />
  
  <text x="1216" y="160" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="54" font-weight="bold" text-anchor="middle">Figure 44.1: Porter's Generic Competitive Strategies</text>
  <text x="1216" y="220" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" text-anchor="middle">Strategic Advantage (Source of Value) vs. Strategic Target (Competitive Scope)</text>
  
  <!-- Column Headers (Source of Advantage) -->
  <rect x="420" y="290" width="900" height="90" fill="#0284c7" rx="14" />
  <text x="870" y="348" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Low Cost Position</text>
  
  <rect x="1360" y="290" width="900" height="90" fill="#059669" rx="14" />
  <text x="1810" y="348" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Product Uniqueness / Differentiation</text>
  
  <!-- Row Headers (Competitive Scope) -->
  <rect x="120" y="420" width="260" height="1060" fill="#0f172a" rx="14" />
  <text x="250" y="960" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle" transform="rotate(-90 250 960)">Broad Market Scope</text>
  
  <rect x="120" y="1520" width="260" height="1060" fill="#475569" rx="14" />
  <text x="250" y="2060" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle" transform="rotate(-90 250 2060)">Narrow Market Scope (Niche)</text>
  
  <!-- Quadrant 1: Cost Leadership (Top-Left) -->
  <rect x="420" y="420" width="900" height="1060" fill="#f0f9ff" stroke="#0284c7" stroke-width="4" rx="20" />
  <text x="870" y="500" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">1. COST LEADERSHIP</text>
  <text x="870" y="555" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Broad Scope + Lowest Cost of Production</text>
  
  <foreignObject x="470" y="600" width="800" height="840">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 26px; color: #334155; line-height: 1.6;">
      <p><b>Core Objective:</b> Become the lowest-cost producer in the industry across a broad customer base.</p>
      <p><b>Key Strategic Levers:</b></p>
      <ul>
        <li>Economies of scale and large-scale manufacturing capacity</li>
        <li>Aggressive pursuit of cost reductions from experience curve</li>
        <li>Tight overhead, labor, and working capital cost control</li>
        <li>High operational efficiency, standard designs, and supply chain clout</li>
      </ul>
      <p><b>Competitive Defense:</b> Can withstand price wars initiated by competitors; earns normal returns when industry prices collapse.</p>
      <p><b>Primary Risk:</b> Technological change that nullifies past scale investments; competitor imitation; neglect of product features.</p>
    </div>
  </foreignObject>
  
  <!-- Quadrant 2: Differentiation (Top-Right) -->
  <rect x="1360" y="420" width="900" height="1060" fill="#ecfdf5" stroke="#059669" stroke-width="4" rx="20" />
  <text x="1810" y="500" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">2. DIFFERENTIATION</text>
  <text x="1810" y="555" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Broad Scope + Premium Unique Attributes</text>
  
  <foreignObject x="1410" y="600" width="800" height="840">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 26px; color: #334155; line-height: 1.6;">
      <p><b>Core Objective:</b> Create products or services perceived industry-wide as unique, commanding price premiums.</p>
      <p><b>Key Strategic Levers:</b></p>
      <ul>
        <li>Superior product quality, advanced engineering, and R&amp;D</li>
        <li>Strong brand equity, prestige marketing, and design appeal</li>
        <li>Exceptional customer service, warranty, and dealer networks</li>
        <li>Patented technologies and intellectual property moats</li>
      </ul>
      <p><b>Competitive Defense:</b> Customer brand loyalty insulates firm from rival pricing; higher margins absorb supplier cost spikes.</p>
      <p><b>Primary Risk:</b> Price premium exceeds perceived value; customer tastes evolve; counterfeit or low-cost imitation.</p>
    </div>
  </foreignObject>
  
  <!-- Quadrant 3: Cost Focus (Bottom-Left) -->
  <rect x="420" y="1520" width="900" height="1060" fill="#fffbeb" stroke="#d97706" stroke-width="4" rx="20" />
  <text x="870" y="1600" fill="#b45309" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">3. COST FOCUS</text>
  <text x="870" y="1655" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Narrow Niche + Lowest Cost in Segment</text>
  
  <foreignObject x="470" y="1700" width="800" height="840">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 26px; color: #334155; line-height: 1.6;">
      <p><b>Core Objective:</b> Target a specific, narrow customer niche or geographic territory and serve it at lower cost than broad competitors.</p>
      <p><b>Key Strategic Levers:</b></p>
      <ul>
        <li>Tailoring production strictly to the unique needs of a neglected buyer group</li>
        <li>Eliminating costly features that broad-market producers bundle</li>
        <li>Focusing marketing and distribution within a localized regional hub</li>
        <li>Low overhead structure specialized for niche delivery</li>
      </ul>
      <p><b>Competitive Defense:</b> Broad leaders cannot match low-cost focus without alienating their core mainstream customers.</p>
      <p><b>Primary Risk:</b> The narrow segment disappears or merges into the mainstream; broad-cost leaders adapt sub-brands.</p>
    </div>
  </foreignObject>
  
  <!-- Quadrant 4: Differentiation Focus (Bottom-Right) -->
  <rect x="1360" y="1520" width="900" height="1060" fill="#fdf2f8" stroke="#be185d" stroke-width="4" rx="20" />
  <text x="1810" y="1600" fill="#831843" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">4. DIFFERENTIATION FOCUS</text>
  <text x="1810" y="1655" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Narrow Niche + Highly Customized Uniqueness</text>
  
  <foreignObject x="1410" y="1700" width="800" height="840">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 26px; color: #334155; line-height: 1.6;">
      <p><b>Core Objective:</b> Serve the specialized, bespoke needs of a specific target demographic better than any generalist.</p>
      <p><b>Key Strategic Levers:</b></p>
      <ul>
        <li>Deep domain expertise and customized formulation</li>
        <li>High-touch personal relationship management</li>
        <li>Luxury, artisanal, or mission-critical industrial customization</li>
        <li>Intimate understanding of buyer workflow and requirements</li>
      </ul>
      <p><b>Competitive Defense:</b> High switching costs and passionate customer loyalty prevent defection to generic providers.</p>
      <p><b>Primary Risk:</b> Niche becomes large enough to attract broad differentiators; out-focused by sub-specialists.</p>
    </div>
  </foreignObject>
  
  <!-- Bottom Warning Banner -->
  <rect x="120" y="2610" width="2140" height="85" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="14" />
  <text x="1216" y="2662" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Porter's Warning: "Stuck in the Middle" — Firms that fail to commit to either Cost Leadership or Differentiation suffer low profitability and competitive failure.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/8378d34541a04269f36e.png")
    print(f"Saved 8378d34541a04269f36e.png ({pix.width}x{pix.height})")

def render_9a09():
    # Figure 46.1: Dividend payment timeline sequence (1957 x 485)
    w, h = 1957, 485
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="30" y="30" width="1897" height="425" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="978" y="80" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Figure 46.1: Dividend Payment Chronology</text>
  
  <!-- Main Timeline Bar -->
  <line x1="120" y1="240" x2="1837" y2="240" stroke="#0f172a" stroke-width="6" />
  
  <!-- Milestone 1: Declaration Date -->
  <circle cx="250" cy="240" r="14" fill="#0284c7" />
  <rect x="100" y="120" width="300" height="85" fill="#eff6ff" stroke="#0284c7" stroke-width="2" rx="10" />
  <text x="250" y="155" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Declaration Date</text>
  <text x="250" y="185" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Board announces dividend</text>
  <text x="250" y="300" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Creates legal liability</text>
  
  <!-- Milestone 2: Ex-Dividend Date -->
  <circle cx="750" cy="240" r="14" fill="#ef4444" />
  <rect x="580" y="120" width="340" height="85" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="10" />
  <text x="750" y="155" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Ex-Dividend Date</text>
  <text x="750" y="185" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" text-anchor="middle">1 business day before Record Date</text>
  <text x="750" y="300" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Stock price drops by dividend</text>
  <text x="750" y="328" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">(Buyer on/after does not receive)</text>
  
  <!-- Milestone 3: Holder-of-Record Date -->
  <circle cx="1250" cy="240" r="14" fill="#d97706" />
  <rect x="1090" y="120" width="320" height="85" fill="#fffbeb" stroke="#d97706" stroke-width="2" rx="10" />
  <text x="1250" y="155" fill="#92400e" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Holder-of-Record Date</text>
  <text x="1250" y="185" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Shareholder registry finalized</text>
  <text x="1250" y="300" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">T+1 Settlement alignment</text>
  
  <!-- Milestone 4: Payment Date -->
  <circle cx="1700" cy="240" r="14" fill="#059669" />
  <rect x="1550" y="120" width="300" height="85" fill="#ecfdf5" stroke="#059669" stroke-width="2" rx="10" />
  <text x="1700" y="155" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Payment Date</text>
  <text x="1700" y="185" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="18" text-anchor="middle">Cash disbursed to holders</text>
  <text x="1700" y="300" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Cash outflow (CFF)</text>
  
  <!-- Bottom banner -->
  <rect x="100" y="370" width="1750" height="60" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="10" />
  <text x="978" y="408" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Exam Rule: Under standard T+1 settlement, the ex-dividend date is exactly ONE business day prior to the record date.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/9a0929da76789e85810f.png")
    print(f"Saved 9a0929da76789e85810f.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_a487()
    render_5418()
    render_5ed7()
    render_f61a()
    render_738b()
    render_64b3()
    render_8378()
    render_9a09()
