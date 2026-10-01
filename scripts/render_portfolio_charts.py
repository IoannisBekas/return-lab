import fitz
import numpy as np

def render_1db9():
    # Figure 83.6: Two-asset portfolio risk-return curves
    # 2028 x 854
    w, h = 2028, 854
    
    x0, y0 = 120, 750
    x_max = 1900
    y_min = 100
    
    # Endpoints:
    # Asset A: low return, low risk -> (1200, 700)
    # Asset B: high return, high risk -> (1700, 160)
    # rho = -1: straight lines to zero-risk point on vertical axis (120, 480)
    xa, ya = 1200, 700
    xb, yb = 1700, 160
    xz, yz = 120, 480

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="40" y="40" width="1948" height="774" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">E(R_p)</text>
  <text x="{x_max - 20}" y="{y0 + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">σ_p</text>

  <!-- rho = +1 (Straight line between A and B) -->
  <line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="#0f172a" stroke-width="5" />
  <text x="1420" y="550" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">ρ = +1</text>

  <!-- rho = -1 (Straight lines from A to zero-risk, then to B) -->
  <line x1="{xa}" y1="{ya}" x2="{xz}" y2="{yz}" stroke="#0f172a" stroke-width="5" />
  <line x1="{xz}" y1="{yz}" x2="{xb}" y2="{yb}" stroke="#0f172a" stroke-width="5" />
  <text x="180" y="600" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">ρ = –1</text>

  <!-- rho = +0.5 curve (slight bow) -->
  <path d="M {xa} {ya} Q 1150 450 {xb} {yb}" fill="none" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <text x="980" y="470" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">ρ = +0.5</text>

  <!-- rho = 0 curve (moderate bow) -->
  <path d="M {xa} {ya} Q 950 460 {xb} {yb}" fill="none" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <text x="820" y="470" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">ρ = 0</text>

  <!-- rho = -0.5 curve (large bow) -->
  <path d="M {xa} {ya} Q 680 470 {xb} {yb}" fill="none" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <text x="520" y="470" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">ρ = –0.5</text>

  <!-- Asset Points -->
  <circle cx="{xa}" cy="{ya}" r="8" fill="#0f172a" />
  <text x="{xa + 25}" y="{ya + 40}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">100% Asset A</text>

  <circle cx="{xb}" cy="{yb}" r="8" fill="#0f172a" />
  <text x="{xb + 25}" y="{yb + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">100% Asset B</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/1db93d5da685ddbe21f7.png")
    print(f"Saved 1db93d5da685ddbe21f7.png ({pix.width}x{pix.height})")


def render_82dd():
    # Figure 83.2: Convex indifference curves
    # 1935 x 1327
    w, h = 1935, 1327
    x0, y0 = 160, 1180
    x_max = 1800
    y_min = 120

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="1835" height="1237" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">σ</text>

  <!-- Utility arrow showing increasing utility towards upper left -->
  <line x1="450" y1="800" x2="350" y2="400" stroke="#0284c7" stroke-width="4" />
  <polygon points="350,400 365,415 345,420" fill="#0284c7" />
  <text x="320" y="440" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">Increasing Utility</text>

  <!-- Curve I1 (highest utility) -->
  <path d="M {x0} 850 C 600 830, 1100 680, 1300 240" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="1310" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">I_1</text>

  <!-- Curve I2 -->
  <path d="M {x0} 980 C 650 960, 1250 780, 1480 240" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="1490" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">I_2</text>

  <!-- Curve I3 (lowest utility) -->
  <path d="M {x0} 1110 C 700 1090, 1400 880, 1660 240" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="1670" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">I_3</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/82dd442559bf99218e58.png")
    print(f"Saved 82dd442559bf99218e58.png ({pix.width}x{pix.height})")


def render_d55f():
    # Figure 83.4: Indifference curves tangent to CAL
    # 1930 x 1317
    w, h = 1930, 1317
    x0, y0 = 160, 1180
    x_max = 1800
    y_min = 120

    # Tangency point X on CAL: CAL passes through (160, 1060) and (1600, 560)
    # At x = 620: y = 1060 - (500/1440)*460 = 900
    x_tan, y_tan = 620, 900

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="1830" height="1227" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">σ</text>

  <!-- Curve I1 -->
  <path d="M {x0} 850 C 600 830, 1100 680, 1300 240" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="1310" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">I_1</text>

  <!-- Curve I2 (tangent at X) -->
  <path d="M {x0} 980 C 450 960, 1200 780, 1480 240" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="1490" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">I_2</text>

  <!-- Curve I3 -->
  <path d="M {x0} 1110 C 700 1090, 1400 880, 1660 240" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="1670" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">I_3</text>

  <!-- CAL Line -->
  <line x1="{x0}" y1="1060" x2="1600" y2="560" stroke="#0284c7" stroke-width="6" />
  <text x="1620" y="520" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Capital</text>
  <text x="1620" y="565" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Allocation</text>
  <text x="1620" y="610" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Line</text>

  <!-- Tangency point X -->
  <circle cx="{x_tan}" cy="{y_tan}" r="10" fill="#0284c7" stroke="#ffffff" stroke-width="3" />
  <text x="{x_tan}" y="{y_tan + 45}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">X</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/d55fad9de3c1cc8c86a2.png")
    print(f"Saved d55fad9de3c1cc8c86a2.png ({pix.width}x{pix.height})")


def render_b5e7():
    # Figure 83.5: Two investor curves tangent to CAL
    # 1925 x 1327
    w, h = 1925, 1327
    x0, y0 = 160, 1180
    x_max = 1800
    y_min = 120

    xa, ya = 460, 930
    xb, yb = 1200, 630

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="1825" height="1237" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">σ</text>

  <!-- CAL Line -->
  <line x1="{x0}" y1="1050" x2="1600" y2="470" stroke="#0284c7" stroke-width="6" />
  <text x="1620" y="430" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Capital</text>
  <text x="1620" y="475" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Allocation</text>
  <text x="1620" y="520" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Line</text>

  <!-- Investor A: high risk aversion (steep curve) -->
  <path d="M {x0} 1000 C 350 990, 850 850, 1180 240" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="1190" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">I_A</text>

  <!-- Investor B: lower risk aversion (flatter curve) -->
  <path d="M 350 720 C 650 730, 1300 680, 1680 240" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="1690" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">I_B</text>

  <!-- Tangency A -->
  <circle cx="{xa}" cy="{ya}" r="10" fill="#0284c7" stroke="#ffffff" stroke-width="3" />
  <text x="{xa}" y="{ya + 50}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">A</text>

  <!-- Tangency B -->
  <circle cx="{xb}" cy="{yb}" r="10" fill="#0284c7" stroke="#ffffff" stroke-width="3" />
  <text x="{xb}" y="{yb + 50}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">B</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b5e73489a1bc733e739c.png")
    print(f"Saved b5e73489a1bc733e739c.png ({pix.width}x{pix.height})")


def render_a2f5():
    # Figure 83.7: Markowitz portfolio theory (Minimum-variance frontier)
    # 2122 x 1330
    w, h = 2122, 1330
    x0, y0 = 160, 1180
    x_max = 1950
    y_min = 120

    x_gmvp, y_gmvp = 480, 680

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="2022" height="1240" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">σ</text>

  <!-- Upper Efficient Frontier (Solid) -->
  <path d="M {x_gmvp} {y_gmvp} C 500 500, 800 360, 1600 340" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Lower Inefficient Frontier (Dashed) -->
  <path d="M {x_gmvp} {y_gmvp} C 500 860, 800 1000, 1600 1020" fill="none" stroke="#94a3b8" stroke-width="5" stroke-dasharray="10 8" />

  <!-- GMVP Point -->
  <circle cx="{x_gmvp}" cy="{y_gmvp}" r="12" fill="#0284c7" stroke="#ffffff" stroke-width="3" />
  
  <!-- GMVP Label with pointer -->
  <text x="350" y="320" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Global Minimum-</text>
  <text x="350" y="365" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Variance Portfolio</text>
  <line x1="380" y1="390" x2="{x_gmvp - 20}" y2="{y_gmvp - 10}" stroke="#0f172a" stroke-width="3" />
  <polygon points="{x_gmvp - 20},{y_gmvp - 10} {x_gmvp - 35},{y_gmvp - 25} {x_gmvp - 25},{y_gmvp - 35}" fill="#0f172a" />

  <!-- Efficient Frontier Label -->
  <text x="1450" y="470" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">Efficient Frontier</text>
  <text x="1450" y="520" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30">(All Efficient Portfolios)</text>
  <line x1="1430" y1="460" x2="1320" y2="360" stroke="#0284c7" stroke-width="3" />

  <!-- Inefficient Portfolios Area -->
  <text x="1050" y="690" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Inefficient Portfolios</text>

  <!-- Scatter points of individual assets -->
"""
    pts = [
        (650, 650), (750, 520), (820, 750), (950, 580), (1000, 480),
        (1050, 780), (1150, 620), (1200, 880), (1280, 500), (1300, 810),
        (1400, 430), (1450, 920), (1500, 660)
    ]
    for px, py in pts:
        svg += f"""  <circle cx="{px}" cy="{py}" r="7" fill="#475569" />\n"""

    svg += """  <!-- Label for individual asset -->
  <text x="1560" y="740" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Individual Assets</text>
  <line x1="1540" y1="730" x2="1465" y2="700" stroke="#475569" stroke-width="2" />
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/a2f54fe32d85ff40101f.png")
    print(f"Saved a2f54fe32d85ff40101f.png ({pix.width}x{pix.height})")


def render_b1f1():
    # Figure 84.1: Linear CAL
    # 2155 x 1412
    w, h = 2155, 1412
    x0, y0 = 240, 1240
    x_max = 2000
    y_min = 120

    rf_y = 1040
    p_x, p_y = 1100, 560
    a_x, a_y = 1450, 360

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="60" y="45" width="2035" height="1322" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 - 25}" y="{y_min + 30}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">E(R_p)</text>
  <text x="{x_max - 20}" y="{y0 + 65}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">σ</text>

  <!-- CAL Line -->
  <line x1="{x0}" y1="{rf_y}" x2="1850" y2="140" stroke="#0284c7" stroke-width="7" />

  <!-- Drop lines for Portfolio P -->
  <line x1="{x0}" y1="{p_y}" x2="{p_x}" y2="{p_y}" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />
  <line x1="{p_x}" y1="{p_y}" x2="{p_x}" y2="{y0}" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />

  <!-- Drop lines for Risky Asset A -->
  <line x1="{x0}" y1="{a_y}" x2="{a_x}" y2="{a_y}" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />
  <line x1="{a_x}" y1="{a_y}" x2="{a_x}" y2="{y0}" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />

  <!-- Y-Axis Ticks & Labels -->
  <text x="{x0 - 25}" y="{rf_y + 12}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">R_f</text>
  <circle cx="{x0}" cy="{rf_y}" r="10" fill="#0284c7" stroke="#ffffff" stroke-width="3" />

  <text x="{x0 - 25}" y="{p_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">E(R_portfolio)</text>
  <text x="{x0 - 25}" y="{a_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">E(R_A)</text>

  <!-- X-Axis Ticks & Labels -->
  <text x="{x0}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">0</text>
  <text x="{p_x}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">σ_portfolio = W_A σ_A</text>
  <text x="{a_x}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">σ_A</text>

  <!-- Points and annotations -->
  <!-- Rf -->
  <text x="{x0 + 40}" y="{rf_y + 80}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Risk-Free Asset</text>
  <line x1="{x0 + 35}" y1="{rf_y + 70}" x2="{x0 + 10}" y2="{rf_y + 10}" stroke="#0284c7" stroke-width="3" />

  <!-- P -->
  <circle cx="{p_x}" cy="{p_y}" r="10" fill="#0f172a" />
  <text x="{p_x + 35}" y="{p_y + 50}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Portfolio With W_A</text>
  <text x="{p_x + 35}" y="{p_y + 90}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Invested in Risky Asset</text>

  <!-- A -->
  <circle cx="{a_x}" cy="{a_y}" r="10" fill="#0f172a" />
  <text x="{a_x + 35}" y="{a_y + 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">Risky Asset (A)</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b1f1a12cd1d52c9b5334.png")
    print(f"Saved b1f1a12cd1d52c9b5334.png ({pix.width}x{pix.height})")


def render_38bb():
    # Figure 84.2: Multiple CALs and tangent indifference curve
    # 2050 x 1417
    w, h = 2050, 1417
    x0, y0 = 160, 1260
    x_max = 1900
    y_min = 120
    rf_y = 1100

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="1950" height="1327" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">σ</text>

  <!-- CAL A (Steepest, highest Sharpe ratio) -->
  <line x1="{x0}" y1="{rf_y}" x2="1800" y2="160" stroke="#0284c7" stroke-width="6" />
  <text x="1820" y="160" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">CAL_A</text>
  <circle cx="1550" cy="300" r="9" fill="#0284c7" />
  <text x="1580" y="312" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">A</text>

  <!-- CAL B -->
  <line x1="{x0}" y1="{rf_y}" x2="1800" y2="440" stroke="#0284c7" stroke-width="5" />
  <text x="1820" y="440" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">CAL_B</text>
  <circle cx="1400" cy="600" r="9" fill="#0284c7" />
  <text x="1430" y="612" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">B</text>

  <!-- CAL C -->
  <line x1="{x0}" y1="{rf_y}" x2="1800" y2="680" stroke="#0284c7" stroke-width="5" />
  <text x="1820" y="680" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">CAL_C</text>
  <circle cx="1300" cy="810" r="9" fill="#0284c7" />
  <text x="1330" y="822" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">C</text>

  <!-- Indifference Curve tangent to CAL_A -->
  <path d="M 450 720 C 700 730, 1100 660, 1380 180" fill="none" stroke="#0f172a" stroke-width="5" />
  <text x="820" y="550" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" transform="rotate(-30 820 550)">Indifference Curve</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/38bbc7eb089de5e88e55.png")
    print(f"Saved 38bbc7eb089de5e88e55.png ({pix.width}x{pix.height})")


def render_5477():
    # Figure 84.3: Capital Market Line (CML)
    # 2042 x 1400
    w, h = 2042, 1400
    x0, y0 = 160, 1260
    x_max = 1900
    y_min = 120
    rf_y = 1100
    
    # Tangency Market Portfolio M
    xm, ym = 1000, 520

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="1942" height="1310" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">σ</text>

  <!-- Efficient Frontier Curve -->
  <path d="M 780 920 C 760 700, 850 540, {xm} {ym} C 1150 500, 1450 360, 1750 360" fill="none" stroke="#0f172a" stroke-width="6" />
  <text x="1760" y="420" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">Efficient</text>
  <text x="1760" y="465" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">Frontier</text>

  <!-- Capital Market Line (CML) -->
  <line x1="{x0}" y1="{rf_y}" x2="1600" y2="120" stroke="#0284c7" stroke-width="7" />
  <text x="1350" y="160" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Capital Market Line</text>

  <!-- Rf Point -->
  <circle cx="{x0}" cy="{rf_y}" r="10" fill="#0284c7" stroke="#ffffff" stroke-width="3" />
  <text x="{x0 - 25}" y="{rf_y + 12}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">R_f</text>
  <text x="{x0 + 35}" y="{rf_y + 55}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Risk-Free Asset</text>

  <!-- Market Portfolio Tangency M -->
  <circle cx="{xm}" cy="{ym}" r="12" fill="#0284c7" stroke="#ffffff" stroke-width="3" />
  <text x="{xm - 30}" y="{ym - 40}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Optimal Risky Portfolio</text>
  <text x="{xm - 30}" y="{ym}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">(Market Portfolio)</text>
  <line x1="{xm - 20}" y1="{ym - 20}" x2="{xm - 10}" y2="{ym - 10}" stroke="#0284c7" stroke-width="3" />

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/54770f97b2405c7ba97c.png")
    print(f"Saved 54770f97b2405c7ba97c.png ({pix.width}x{pix.height})")


def render_0c67():
    # Figure 84.5: Diversification curve
    # 1647 x 1187
    w, h = 1647, 1187
    x0, y0 = 180, 1050
    x_max = 1500
    y_min = 120

    y_mkt = 780

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="1547" height="1097" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">σ (Risk)</text>
  <text x="{x0 + 400}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Number of securities in the portfolio</text>

  <!-- Market Risk line across -->
  <line x1="{x0}" y1="{y_mkt}" x2="{x_max}" y2="{y_mkt}" stroke="#0f172a" stroke-width="4" />
  <text x="{x0 - 20}" y="{y_mkt - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">Market Risk</text>
  <text x="{x0 - 20}" y="{y_mkt + 25}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="end">(σ_mkt)</text>

  <!-- Total Risk curve decaying from (220, 160) to (1400, y_mkt + 5) -->
  <path d="M 220 160 C 230 480, 500 {y_mkt - 20}, 1400 {y_mkt - 5}" fill="none" stroke="#0284c7" stroke-width="7" />

  <!-- Arrow pointing to curve -->
  <text x="1100" y="360" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Total Risk</text>
  <text x="1100" y="405" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">(unsystematic risk + systematic risk)</text>
  <line x1="900" y1="420" x2="600" y2="520" stroke="#0f172a" stroke-width="3" />
  <polygon points="600,520 618,510 610,528" fill="#0f172a" />

  <!-- Double arrow: Unsystematic Risk -->
  <line x1="420" y1="520" x2="420" y2="{y_mkt - 10}" stroke="#dc2626" stroke-width="4" />
  <polygon points="420,520 412,535 428,535" fill="#dc2626" />
  <polygon points="420,{y_mkt - 10} 412,{y_mkt - 25} 428,{y_mkt - 25}" fill="#dc2626" />
  <text x="445" y="650" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Unsystematic Risk</text>

  <!-- Double arrow: Systematic Risk -->
  <line x1="420" y1="{y_mkt + 10}" x2="420" y2="{y0 - 10}" stroke="#0284c7" stroke-width="4" />
  <polygon points="420,{y_mkt + 10} 412,{y_mkt + 25} 428,{y_mkt + 25}" fill="#0284c7" />
  <polygon points="420,{y0 - 10} 412,{y0 - 25} 428,{y0 - 25}" fill="#0284c7" />
  <text x="445" y="910" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Systematic Risk</text>

  <!-- ~30 mark on x-axis -->
  <line x1="1400" y1="{y_mkt}" x2="1400" y2="{y0}" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <text x="1400" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">≈ 30</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/0c67b0ae6bfd5406b1b5.png")
    print(f"Saved 0c67b0ae6bfd5406b1b5.png ({pix.width}x{pix.height})")


def render_b8a8():
    # Figure 84.6: Security Characteristic Line (SCL)
    # 2342 x 1450
    w, h = 2342, 1450
    x0, y0 = 240, 1300
    x_max = 2150
    y_min = 120

    alpha_y = 1220

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="60" y="45" width="2222" height="1360" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 - 25}" y="{y_min + 20}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">Asset Excess Return</text>
  <text x="{x0 - 25}" y="{y_min + 70}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">(R_i – R_f)</text>

  <text x="{x_max - 20}" y="{y0 + 65}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">Market Excess Return (R_m – R_f)</text>

  <!-- Alpha intercept -->
  <line x1="{x0 - 15}" y1="{alpha_y}" x2="{x0 + 15}" y2="{alpha_y}" stroke="#0f172a" stroke-width="4" />
  <text x="{x0 - 30}" y="{alpha_y + 12}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">α_i</text>

  <!-- SCL Line -->
  <line x1="{x0}" y1="{alpha_y}" x2="1600" y2="160" stroke="#0284c7" stroke-width="7" />
  <text x="1630" y="200" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">Security</text>
  <text x="1630" y="250" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">Characteristic</text>
  <text x="1630" y="300" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">Line</text>

  <!-- Slope triangle at (850, 740) -->
  <polygon points="850,740 970,740 970,650" fill="#e0f2fe" opacity="0.6" />
  <line x1="850" y1="740" x2="970" y2="740" stroke="#0f172a" stroke-width="3" />
  <line x1="970" y1="740" x2="970" y2="650" stroke="#0f172a" stroke-width="3" />

  <text x="1010" y="710" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">β_i = Slope = Cov(i,m) / σ_m²</text>

  <!-- Scatter points -->
"""
    pts = [
        (380, 1180), (450, 1080), (520, 880), (620, 950), (660, 680),
        (720, 770), (780, 660), (840, 560), (920, 720), (950, 690),
        (1010, 820), (1080, 580), (1150, 420), (1240, 310), (1300, 410),
        (1380, 460), (1440, 220)
    ]
    for px, py in pts:
        svg += f"""  <circle cx="{px}" cy="{py}" r="9" fill="#0f172a" stroke="#ffffff" stroke-width="2" />\n"""

    svg += "</svg>"
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b8a8e0722a8acfaa2703.png")
    print(f"Saved b8a8e0722a8acfaa2703.png ({pix.width}x{pix.height})")


def render_9bc5():
    # Figure 84.9: Side-by-side CML vs SML
    # 1600 x 2154
    w, h = 1600, 2154
    
    x0 = 160
    x_max = 1450

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- PANEL 1: CML -->
  <rect x="50" y="45" width="1500" height="980" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="800" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">(a) Capital Market Line</text>

  <!-- Axes (Panel 1) -->
  <line x1="{x0}" y1="920" x2="{x0}" y2="180" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="920" x2="{x_max}" y2="920" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="220" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="970" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">σ</text>

  <!-- Efficient Frontier -->
  <path d="M 520 820 C 500 680, 580 500, 680 440 C 800 380, 1100 280, 1300 280" fill="none" stroke="#0f172a" stroke-width="5" />

  <!-- CML Line -->
  <line x1="{x0}" y1="800" x2="1150" y2="240" stroke="#0284c7" stroke-width="6" />
  <text x="1170" y="240" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">CML</text>

  <!-- Points on CML -->
  <!-- Rf -->
  <circle cx="{x0}" cy="800" r="8" fill="#0284c7" />
  <text x="{x0 - 20}" y="810" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">R_f</text>

  <!-- D (Lending) -->
  <circle cx="380" cy="670" r="8" fill="#0284c7" />
  <text x="380" y="640" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">D</text>
  <text x="380" y="740" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">P_(M+T-bills)</text>

  <!-- M (Market Portfolio) -->
  <circle cx="680" cy="440" r="9" fill="#0284c7" />
  <text x="660" y="420" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">M</text>
  <line x1="{x0}" y1="440" x2="680" y2="440" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <line x1="680" y1="440" x2="680" y2="920" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <text x="{x0 - 20}" y="450" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">E(R_M)</text>
  <text x="680" y="960" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">σ_M</text>

  <!-- E (Borrowing / Margin) -->
  <circle cx="950" cy="330" r="8" fill="#0284c7" />
  <text x="970" y="360" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">E</text>
  <text x="950" y="270" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">P_(M w/Margin)</text>

  <!-- Inefficient Points A, B, C -->
  <circle cx="900" cy="410" r="7" fill="#0f172a" />
  <text x="925" y="415" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">A</text>

  <circle cx="1100" cy="440" r="7" fill="#0f172a" />
  <text x="1125" y="445" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">B (β = 1)</text>

  <circle cx="1200" cy="560" r="7" fill="#0f172a" />
  <text x="1225" y="565" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">C</text>


  <!-- PANEL 2: SML -->
  <rect x="50" y="1080" width="1500" height="980" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="800" y="1145" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">(b) Security Market Line</text>

  <!-- Axes (Panel 2) -->
  <line x1="{x0}" y1="1955" x2="{x0}" y2="1215" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="1955" x2="{x_max}" y2="1955" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="1255" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="2005" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">β</text>

  <!-- SML Line -->
  <line x1="{x0}" y1="1835" x2="1150" y2="1315" stroke="#0284c7" stroke-width="6" />
  <text x="1170" y="1315" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">SML</text>

  <!-- Rf -->
  <text x="{x0 - 20}" y="1845" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">R_f</text>

  <!-- Points on SML: C, D, B, A, E -->
  <circle cx="240" cy="1800" r="7" fill="#0284c7" />
  <text x="220" y="1780" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">C</text>

  <circle cx="310" cy="1760" r="7" fill="#0284c7" />
  <text x="330" y="1780" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">D</text>

  <circle cx="580" cy="1600" r="9" fill="#0284c7" />
  <text x="560" y="1575" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">B</text>
  <line x1="{x0}" y1="1600" x2="580" y2="1600" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <line x1="580" y1="1600" x2="580" y2="1955" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <text x="{x0 - 20}" y="1610" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">E(R_M)</text>
  <text x="580" y="1995" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">β_M = 1</text>

  <circle cx="750" cy="1510" r="7" fill="#0284c7" />
  <text x="770" y="1535" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">A</text>

  <circle cx="950" cy="1405" r="7" fill="#0284c7" />
  <text x="970" y="1430" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">E</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/9bc56c65e5dbd991498b.png")
    print(f"Saved 9bc56c65e5dbd991498b.png ({pix.width}x{pix.height})")


def render_db07():
    # Figure 84.10: Risk-adjusted performance / Sharpe ratio
    # 2312 x 1127
    w, h = 2312, 1127
    x0, y0 = 160, 980
    x_max = 2100
    y_min = 100
    rf_y = 850

    p1_x, p1_y = 480, 680
    p2_x, p2_y = 650, 360
    m_x, m_y = 800, 520

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="2212" height="1037" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">σ</text>

  <!-- Efficient Frontier -->
  <path d="M 640 850 C 620 720, 700 580, {m_x} {m_y} C 1000 440, 1400 260, 1750 260" fill="none" stroke="#0f172a" stroke-width="5" />

  <!-- CAL Line passing through P2 -->
  <line x1="{x0}" y1="{rf_y}" x2="880" y2="130" stroke="#0284c7" stroke-width="6" />
  
  <!-- CML Line passing through P1 and tangent at M -->
  <line x1="{x0}" y1="{rf_y}" x2="1550" y2="130" stroke="#0284c7" stroke-width="6" />

  <!-- Formula Callouts at Top -->
  <text x="800" y="90" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">CAL slope = (R_P2 – R_f) / σ_P2</text>
  <text x="1650" y="90" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">CML slope = (R_M – R_f) / σ_M = (R_P1 – R_f) / σ_P1</text>

  <!-- Points and drop lines -->
  <!-- Rf -->
  <circle cx="{x0}" cy="{rf_y}" r="8" fill="#0284c7" />
  <text x="{x0 - 20}" y="{rf_y + 12}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">R_f</text>

  <!-- P1 -->
  <circle cx="{p1_x}" cy="{p1_y}" r="8" fill="#0284c7" />
  <line x1="{x0}" y1="{p1_y}" x2="{p1_x}" y2="{p1_y}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <line x1="{p1_x}" y1="{p1_y}" x2="{p1_x}" y2="{y0}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <text x="{p1_x + 20}" y="{p1_y + 12}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">P1</text>
  <text x="{x0 - 20}" y="{p1_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">R_P1</text>
  <text x="{p1_x}" y="{y0 + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">σ_P1</text>

  <!-- P2 -->
  <circle cx="{p2_x}" cy="{p2_y}" r="8" fill="#0284c7" />
  <line x1="{x0}" y1="{p2_y}" x2="{p2_x}" y2="{p2_y}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <line x1="{p2_x}" y1="{p2_y}" x2="{p2_x}" y2="{y0}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <text x="{p2_x + 20}" y="{p2_y + 12}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">P2</text>
  <text x="{x0 - 20}" y="{p2_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">R_P2</text>
  <text x="{p2_x}" y="{y0 + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">σ_P2</text>

  <!-- M -->
  <circle cx="{m_x}" cy="{m_y}" r="9" fill="#0284c7" />
  <line x1="{x0}" y1="{m_y}" x2="{m_x}" y2="{m_y}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <line x1="{m_x}" y1="{m_y}" x2="{m_x}" y2="{y0}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <text x="{x0 - 20}" y="{m_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">R_M</text>
  <text x="{m_x}" y="{y0 + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">σ_M</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/db07dafad4c5b4570ed2.png")
    print(f"Saved db07dafad4c5b4570ed2.png ({pix.width}x{pix.height})")


def render_c34a():
    # SML Stock A & B Alpha Plot
    # 1742 x 1067
    w, h = 1742, 1067
    x0, y0 = 160, 920
    x_max = 1550
    y_min = 100

    rf_y = 800

    # Betas: 0.8 at x=550, 1.0 at x=850, 1.2 at x=1150
    # SML line: from (160, 800) to (1400, 220) -> slope = -580/1240 = -0.4677
    # At x=550: y_sml = 800 - 0.4677*390 = 618
    # At x=850: y_sml = 800 - 0.4677*690 = 477
    # At x=1150: y_sml = 800 - 0.4677*990 = 337
    
    # Point B: beta=0.8, above SML (say y=260)
    # Point A: beta=1.0, below SML (say y=620)
    # Point C: beta=1.2, on SML (y=337)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="50" y="45" width="1642" height="977" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <text x="{x0 + 15}" y="{y_min - 15}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">E(R)</text>
  <text x="{x_max - 20}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Beta Risk (β)</text>

  <!-- Rf tick -->
  <text x="{x0 - 20}" y="{rf_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">7%</text>
  <line x1="{x0 - 10}" y1="{rf_y}" x2="{x0}" y2="{rf_y}" stroke="#0f172a" stroke-width="3" />

  <!-- SML Line -->
  <line x1="{x0}" y1="{rf_y}" x2="1350" y2="240" stroke="#0284c7" stroke-width="6" />
  <text x="1370" y="240" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">SML</text>

  <!-- Stock B (Undervalued, Alpha > 0) -->
  <line x1="550" y1="260" x2="550" y2="{y0}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <circle cx="550" cy="260" r="10" fill="#166534" />
  <text x="550" y="220" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">B</text>
  <rect x="580" y="235" width="220" height="50" fill="#f0fdf4" rx="8" />
  <text x="690" y="270" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Undervalued (α &gt; 0)</text>

  <!-- Stock A (Overvalued, Alpha < 0) -->
  <line x1="850" y1="620" x2="850" y2="{y0}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <circle cx="850" cy="620" r="10" fill="#dc2626" />
  <text x="850" y="585" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">A</text>
  <rect x="880" y="595" width="220" height="50" fill="#fef2f2" rx="8" />
  <text x="990" y="630" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Overvalued (α &lt; 0)</text>

  <!-- Stock C (Fairly valued, on SML) -->
  <line x1="1150" y1="337" x2="1150" y2="{y0}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6" />
  <circle cx="1150" cy="337" r="10" fill="#0284c7" />
  <text x="1150" y="300" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">C</text>
  <rect x="1180" y="310" width="200" height="50" fill="#f0f9ff" rx="8" />
  <text x="1280" y="345" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Fairly Valued (α = 0)</text>

  <!-- X-Axis ticks -->
  <text x="550" y="{y0 + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">0.8</text>
  <text x="850" y="{y0 + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">1.0</text>
  <text x="1150" y="{y0 + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">1.2</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/c34a22880904740b85c0.png")
    print(f"Saved c34a22880904740b85c0.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_1db9()
    render_82dd()
    render_d55f()
    render_b5e7()
    render_a2f5()
    render_b1f1()
    render_38bb()
    render_5477()
    render_0c67()
    render_b8a8()
    render_9bc5()
    render_db07()
    render_c34a()
