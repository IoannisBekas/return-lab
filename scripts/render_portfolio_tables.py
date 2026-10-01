import fitz

def render_64ea():
    # Figure 83.1: Historical risk-return of major asset classes
    # 2407 x 812
    w, h = 2407, 812
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="2307" height="722" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Header -->
  <rect x="50" y="45" width="900" height="110" fill="#f1f5f9" rx="16" />
  <rect x="950" y="45" width="700" height="110" fill="#0284c7" />
  <rect x="1650" y="45" width="707" height="110" fill="#0284c7" rx="16" />

  <text x="500" y="115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Asset Class</text>
  
  <text x="1300" y="90" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Average Annual Return</text>
  <text x="1300" y="132" fill="#e0f2fe" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="500" text-anchor="middle">(Geometric Mean)</text>

  <text x="2003" y="90" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Standard Deviation</text>
  <text x="2003" y="132" fill="#e0f2fe" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="500" text-anchor="middle">(Annualized Monthly)</text>

  <line x1="50" y1="155" x2="2357" y2="155" stroke="#cbd5e1" stroke-width="3" />
  <line x1="950" y1="45" x2="950" y2="767" stroke="#cbd5e1" stroke-width="3" />
  <line x1="1650" y1="45" x2="1650" y2="767" stroke="#cbd5e1" stroke-width="3" />

  <!-- Rows -->
"""
    rows = [
        ("Small-cap stocks", "12.1%", "31.7%"),
        ("Large-cap stocks", "10.2%", "19.8%"),
        ("Long-term corporate bonds", "6.1%", "8.3%"),
        ("Long-term government bonds", "5.5%", "9.9%"),
        ("Treasury bills", "3.4%", "3.1%"),
        ("Inflation", "2.9%", "4.0%"),
    ]

    for i, (asset, ret, sd) in enumerate(rows):
        y_top = 155 + i * 102
        y_text = y_top + 64
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        svg += f"""  <rect x="50" y="{y_top}" width="2307" height="102" fill="{bg}" />
  <text x="100" y="{y_text}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">{asset}</text>
  <text x="1300" y="{y_text}" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">{ret}</text>
  <text x="2003" y="{y_text}" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="36" text-anchor="middle">{sd}</text>\n"""
        if i < len(rows) - 1:
            svg += f"""  <line x1="50" y1="{y_top + 102}" x2="2357" y2="{y_top + 102}" stroke="#e2e8f0" stroke-width="2" />\n"""

    svg += "</svg>"
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/64eafcc24c6871ad8c1d.png")
    print(f"Saved 64eafcc24c6871ad8c1d.png ({pix.width}x{pix.height})")


def render_c54b():
    # Figure 85.1: Comparative classification table contrasting investors
    # 2417 x 1102
    w, h = 2417, 1102
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="2317" height="1012" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Headers -->
  <!-- Col 0: 480, Col 1: 450, Col 2: 450, Col 3: 450, Col 4: 487 -->
  <rect x="50" y="45" width="480" height="120" fill="#f1f5f9" rx="16" />
  <rect x="530" y="45" width="1837" height="120" fill="#0284c7" rx="16" />

  <text x="290" y="118" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Investor</text>
  
  <text x="755" y="95" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Risk</text>
  <text x="755" y="135" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Tolerance</text>

  <text x="1215" y="95" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Investment</text>
  <text x="1215" y="135" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Horizon</text>

  <text x="1675" y="95" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Liquidity</text>
  <text x="1675" y="135" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Needs</text>

  <text x="2128" y="95" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Income</text>
  <text x="2128" y="135" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Needs</text>

  <line x1="50" y1="165" x2="2367" y2="165" stroke="#cbd5e1" stroke-width="3" />
  <line x1="530" y1="45" x2="530" y2="1057" stroke="#cbd5e1" stroke-width="3" />
  <line x1="990" y1="45" x2="990" y2="1057" stroke="#e2e8f0" stroke-width="2" />
  <line x1="1450" y1="45" x2="1450" y2="1057" stroke="#e2e8f0" stroke-width="2" />
  <line x1="1900" y1="45" x2="1900" y2="1057" stroke="#e2e8f0" stroke-width="2" />

  <!-- Rows -->
"""
    rows = [
        ("Individuals", "Depends on individual", "Depends on individual", "Depends on individual", "Depends on individual"),
        ("Banks", "Low", "Short", "High", "Pay interest"),
        ("Endowments", "High", "Long", "Low", "Spending level"),
        ("Insurance", "Low", "Long (life) / Short (P&C)", "High", "Low"),
        ("Mutual funds", "Depends on fund", "Depends on fund", "High", "Depends on fund"),
        ("Defined benefit pensions", "High", "Long", "Low", "Depends on age"),
    ]

    for i, (inv, rt, ih, ln, ineed) in enumerate(rows):
        y_top = 165 + i * 148
        y_text = y_top + 86
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        svg += f"""  <rect x="50" y="{y_top}" width="2317" height="148" fill="{bg}" />
  <text x="90" y="{y_text}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">{inv}</text>
  <text x="755" y="{y_text}" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="middle">{rt}</text>
  <text x="1215" y="{y_text}" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="middle">{ih}</text>
  <text x="1675" y="{y_text}" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="middle">{ln}</text>
  <text x="2128" y="{y_text}" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="32" text-anchor="middle">{ineed}</text>\n"""
        if i < len(rows) - 1:
            svg += f"""  <line x1="50" y1="{y_top + 148}" x2="2367" y2="{y_top + 148}" stroke="#e2e8f0" stroke-width="2" />\n"""

    svg += "</svg>"
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/c54ba02affce59fbccc9.png")
    print(f"Saved c54ba02affce59fbccc9.png ({pix.width}x{pix.height})")


def render_9622():
    # Figure 86.1: Strategic Asset Allocation (Vermont Pension)
    # 2064 x 2326
    w, h = 2064, 2326
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- Description Banner -->
  <rect x="60" y="50" width="1944" height="150" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />
  <text x="90" y="105" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Vermont Pension Investment Committee (Strategic Asset Allocation)</text>
  <text x="90" y="155" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="28">Manages retirement assets for teachers, state, and municipal employees.</text>

  <!-- Table Card -->
  <rect x="60" y="230" width="1944" height="1940" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Table Header -->
  <rect x="60" y="230" width="1944" height="90" fill="#0284c7" rx="16" />
  <text x="120" y="288" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">Asset Class</text>
  <text x="1860" y="288" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Target</text>
"""
    y = 360

    def draw_section(title, items, total_label, total_val):
        nonlocal y
        # Section header
        svg_sec = f"""  <rect x="60" y="{y}" width="1944" height="65" fill="#f1f5f9" />
  <text x="120" y="{y + 44}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">{title}</text>\n"""
        y += 65
        for name, pct in items:
            svg_sec += f"""  <text x="140" y="{y + 45}" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="30">{name}</text>
  <text x="1860" y="{y + 45}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">{pct}</text>
  <line x1="120" y1="{y + 60}" x2="1940" y2="{y + 60}" stroke="#f1f5f9" stroke-width="2" />\n"""
            y += 65
        # Section Total
        svg_sec += f"""  <rect x="60" y="{y}" width="1944" height="65" fill="#e0f2fe" />
  <text x="120" y="{y + 44}" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">{total_label}</text>
  <text x="1860" y="{y + 44}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">{total_val}</text>\n"""
        y += 85
        return svg_sec

    growth_items = [
        ("Passive global equities", "24%"),
        ("Active global equities", "5%"),
        ("Large cap U.S. equities", "4%"),
        ("Small-/mid-cap U.S. equities", "3%"),
        ("Non-U.S. developed market equities", "5%"),
        ("International small-cap equities", "2%"),
        ("Private equity", "10%"),
        ("Core plus fixed income", "6%"),
        ("Emerging market debt", "4%"),
        ("Private debt", "5%"),
        ("Non-core real estate", "3%"),
    ]
    svg += draw_section("Growth Assets", growth_items, "Total Growth Assets", "71%")

    downturn_items = [
        ("Core fixed income", "14%"),
        ("Short-term quality credit", "5%"),
    ]
    svg += draw_section("Downturn Hedging Assets", downturn_items, "Total Downturn Hedging", "19%")

    inflation_items = [
        ("Core real estate", "5%"),
        ("U.S. TIPS", "3%"),
        ("Infrastructure / farmland", "2%"),
    ]
    svg += draw_section("Inflation Hedging Assets", inflation_items, "Total Inflation Hedging", "10%")

    svg += f"""  <!-- Source Footer -->
  <text x="120" y="{y + 35}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24">Source: State of Vermont, Office of the State Treasurer. Target allocation policy.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/96221fade382c1158c5b.png")
    print(f"Saved 96221fade382c1158c5b.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_64ea()
    render_c54b()
    render_9622()
