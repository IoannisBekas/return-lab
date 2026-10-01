import fitz
import numpy as np

def render_b71b():
    # Figure 24.1: Capital budgeting cash flow timeline
    # 1110 x 666
    w, h = 1110, 666
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="24" />

  <!-- Table Container -->
  <rect x="180" y="70" width="750" height="526" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Header -->
  <rect x="180" y="70" width="375" height="95" fill="#f1f5f9" rx="16" />
  <rect x="555" y="70" width="375" height="95" fill="#0284c7" rx="16" />
  <text x="367" y="132" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Year</text>
  <text x="742" y="132" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Cash Flow</text>

  <line x1="180" y1="165" x2="930" y2="165" stroke="#cbd5e1" stroke-width="3" />
  <line x1="555" y1="70" x2="555" y2="596" stroke="#cbd5e1" stroke-width="3" />

  <!-- Rows -->
  <!-- Year 0: -$100 (Outflow / Red) -->
  <rect x="180" y="165" width="750" height="107" fill="#ffffff" />
  <text x="367" y="235" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">0</text>
  <text x="742" y="235" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">–$100</text>
  <line x1="180" y1="272" x2="930" y2="272" stroke="#e2e8f0" stroke-width="2" />

  <!-- Year 1: $25 -->
  <rect x="180" y="272" width="750" height="107" fill="#f8fafc" />
  <text x="367" y="342" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">1</text>
  <text x="742" y="342" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">+$25</text>
  <line x1="180" y1="379" x2="930" y2="379" stroke="#e2e8f0" stroke-width="2" />

  <!-- Year 2: $50 -->
  <rect x="180" y="379" width="750" height="107" fill="#ffffff" />
  <text x="367" y="449" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">2</text>
  <text x="742" y="449" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">+$50</text>
  <line x1="180" y1="486" x2="930" y2="486" stroke="#e2e8f0" stroke-width="2" />

  <!-- Year 3: $75 -->
  <rect x="180" y="486" width="750" height="110" fill="#f8fafc" />
  <text x="367" y="556" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">3</text>
  <text x="742" y="556" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">+$75</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b71b7cae1deda1f0d8cf.png")
    print(f"Saved b71b7cae1deda1f0d8cf.png ({pix.width}x{pix.height})")


def render_3d8e():
    # Figure 25.1: Modigliani-Miller Proposition I (Pie charts)
    # 1952 x 680
    w, h = 1952, 680
    
    r = 230
    c1_x, cy = 480, 340
    c2_x = 1472
    
    # Left pie: 40% equity, 60% debt
    # 40% = 144 degrees -> angle from 0 to 144
    rad1 = np.deg2rad(144)
    x1_e = c1_x + r * np.cos(rad1)
    y1_e = cy + r * np.sin(rad1)
    
    # Right pie: 60% equity, 40% debt
    # 60% = 216 degrees
    rad2 = np.deg2rad(216)
    x2_e = c2_x + r * np.cos(rad2)
    y2_e = cy + r * np.sin(rad2)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- LEFT PIE: 40% Equity / 60% Debt -->
  <!-- 60% Debt wedge (base full circle) -->
  <circle cx="{c1_x}" cy="{cy}" r="{r}" fill="#0284c7" stroke="#ffffff" stroke-width="4" />
  <!-- 40% Equity wedge -->
  <path d="M {c1_x} {cy} L {c1_x + r} {cy} A {r} {r} 0 0 1 {x1_e:.1f} {y1_e:.1f} Z" fill="#38bdf8" stroke="#ffffff" stroke-width="4" />
  
  <text x="{c1_x - 90}" y="{cy - 40}" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">60%</text>
  <text x="{c1_x - 90}" y="{cy + 10}" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Debt</text>

  <text x="{c1_x + 100}" y="{cy + 80}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">40%</text>
  <text x="{c1_x + 100}" y="{cy + 130}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Equity</text>

  <!-- EQUALS SIGN -->
  <rect x="916" y="295" width="120" height="24" fill="#0f172a" rx="6" />
  <rect x="916" y="360" width="120" height="24" fill="#0f172a" rx="6" />

  <!-- RIGHT PIE: 60% Equity / 40% Debt -->
  <circle cx="{c2_x}" cy="{cy}" r="{r}" fill="#38bdf8" stroke="#ffffff" stroke-width="4" />
  <!-- 40% Debt wedge -->
  <path d="M {c2_x} {cy} L {c2_x + r} {cy} A {r} {r} 0 0 1 {x2_e:.1f} {y2_e:.1f} Z" fill="#0284c7" stroke="#ffffff" stroke-width="4" />

  <text x="{c2_x - 90}" y="{cy - 40}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">60%</text>
  <text x="{c2_x - 90}" y="{cy + 10}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Equity</text>

  <text x="{c2_x + 90}" y="{cy + 80}" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">40%</text>
  <text x="{c2_x + 90}" y="{cy + 130}" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Debt</text>

  <text x="{c1_x}" y="630" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Firm Value (V_L)</text>
  <text x="{c2_x}" y="630" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Firm Value (V_U)</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/3d8e55b607417527f927.png")
    print(f"Saved 3d8e55b607417527f927.png ({pix.width}x{pix.height})")


def render_d28e():
    # Figure 25.2: MM Proposition II (Without Taxes)
    # 1695 x 1135
    w, h = 1695, 1135
    
    x0, y0 = 180, 960
    x_max = 1500
    y_min = 160
    
    y_rd = 820
    y_wacc = 680
    y_re_end = 280

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="60" y="50" width="1575" height="1035" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <!-- Axis Labels -->
  <text x="{x0 - 25}" y="{y_min + 20}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Cost of</text>
  <text x="{x0 - 25}" y="{y_min + 65}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">capital</text>

  <text x="{x_max - 20}" y="{y0 + 75}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">D/E</text>

  <!-- 1. Cost of debt (rd) dashed flat line -->
  <line x1="{x0}" y1="{y_rd}" x2="1350" y2="{y_rd}" stroke="#475569" stroke-width="4" stroke-dasharray="10 8" />
  <text x="1370" y="{y_rd + 12}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Cost of debt (r_d)</text>

  <!-- 2. WACC constant flat line -->
  <line x1="{x0}" y1="{y_wacc}" x2="1350" y2="{y_wacc}" stroke="#0284c7" stroke-width="6" />
  <text x="1370" y="{y_wacc + 12}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">WACC = r_0</text>

  <!-- 3. Cost of Equity (rE) rising linearly -->
  <line x1="{x0}" y1="{y_wacc}" x2="1300" y2="{y_re_end}" stroke="#0f172a" stroke-width="6" />
  <text x="1320" y="{y_re_end + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Cost of equity (r_e)</text>

  <!-- Formula Callout -->
  <rect x="360" y="160" width="580" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" rx="10" />
  <text x="650" y="218" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">r_e = r_0 + (D/E)(r_0 – r_d)</text>

  <!-- Pointer to rE line -->
  <line x1="650" y1="250" x2="720" y2="460" stroke="#0284c7" stroke-width="3" stroke-dasharray="6 6" />
  <circle cx="720" cy="460" r="7" fill="#0284c7" />

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/d28e321fce19050c46cc.png")
    print(f"Saved d28e321fce19050c46cc.png ({pix.width}x{pix.height})")


def render_a265():
    # Figure 25.3: MM Proposition II (With Corporate Taxes)
    # 1855 x 1140
    w, h = 1855, 1140
    
    x0, y0 = 180, 960
    x_max = 1600
    y_min = 160
    
    y_rd = 820
    y_wacc_start = 680
    y_re_end = 320

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="60" y="50" width="1735" height="1040" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <!-- Axis Labels -->
  <text x="{x0 - 25}" y="{y_min + 20}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Cost of</text>
  <text x="{x0 - 25}" y="{y_min + 65}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">capital</text>

  <text x="{x_max - 20}" y="{y0 + 75}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">D/E</text>

  <!-- 1. After-tax cost of debt dashed flat line -->
  <line x1="{x0}" y1="{y_rd}" x2="1350" y2="{y_rd}" stroke="#475569" stroke-width="4" stroke-dasharray="10 8" />
  <text x="1370" y="{y_rd + 12}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">After-tax cost of debt: r_d(1 – t)</text>

  <!-- 2. WACC curve sloping downward asymptotically toward rd(1-t) -->
  <path d="M {x0} {y_wacc_start} C 500 {y_wacc_start + 40}, 900 {y_rd - 25}, 1350 {y_rd - 10}" 
        fill="none" stroke="#0284c7" stroke-width="6" />
  <text x="1370" y="{y_rd - 10}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">WACC</text>

  <!-- 3. Cost of Equity (rE) rising linearly at reduced slope -->
  <line x1="{x0}" y1="{y_wacc_start}" x2="1350" y2="{y_re_end}" stroke="#0f172a" stroke-width="6" />
  <text x="1370" y="{y_re_end + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Cost of equity (r_e)</text>

  <!-- Formula Callout -->
  <rect x="340" y="150" width="670" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" rx="10" />
  <text x="675" y="208" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">r_e = r_0 + (D/E)(r_0 – r_d)(1 – t)</text>

  <!-- Pointer to rE line -->
  <line x1="675" y1="240" x2="750" y2="470" stroke="#0284c7" stroke-width="3" stroke-dasharray="6 6" />
  <circle cx="750" cy="470" r="7" fill="#0284c7" />

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/a265036044abb2af4c89.png")
    print(f"Saved a265036044abb2af4c89.png ({pix.width}x{pix.height})")


def render_59d8():
    # Figure 25.4: Static Tradeoff Theory Graph
    # 1792 x 1432
    w, h = 1792, 1432
    
    x0, y0 = 180, 1220
    x_max = 1600
    y_min = 160
    
    x_opt = 750
    y_wacc_opt = 880

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <rect x="60" y="50" width="1672" height="1332" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <!-- Axis Labels -->
  <text x="{x0 - 25}" y="{y_min + 20}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Cost of</text>
  <text x="{x0 - 25}" y="{y_min + 65}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">capital</text>

  <text x="{x_max - 20}" y="{y0 + 75}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">D/E</text>

  <!-- 1. Cost of Equity curve: starts at (180, 820) and bends upward -->
  <path d="M {x0} 820 C 500 800, 1000 650, 1450 360" fill="none" stroke="#0f172a" stroke-width="6" />
  <text x="1465" y="360" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Cost of equity</text>

  <!-- 2. After-tax cost of debt with financial distress: starts at (180, 1070) flat then rises sharply -->
  <path d="M {x0} 1070 C 600 1070, 950 1030, 1450 820" fill="none" stroke="#475569" stroke-width="5" stroke-dasharray="10 8" />
  <text x="1465" y="805" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">After-tax cost of debt</text>
  <text x="1465" y="845" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">with financial distress</text>

  <!-- 3. WACC U-shaped curve -->
  <!-- Starts at (180, 820), drops to min at (750, 880), climbs to (1450, 720) -->
  <path d="M {x0} 820 C 400 870, 600 {y_wacc_opt}, {x_opt} {y_wacc_opt} C 900 {y_wacc_opt}, 1200 820, 1450 720" 
        fill="none" stroke="#0284c7" stroke-width="7" />
  <text x="1465" y="720" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">WACC</text>

  <!-- Optimal Capital Structure Vertical Drop Line -->
  <line x1="{x_opt}" y1="{y_wacc_opt}" x2="{x_opt}" y2="{y0}" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <circle cx="{x_opt}" cy="{y_wacc_opt}" r="10" fill="#0284c7" stroke="#ffffff" stroke-width="3" />

  <text x="{x_opt}" y="{y0 + 55}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Optimal</text>
  <text x="{x_opt}" y="{y0 + 100}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">capital structure</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/59d8c89cd55cf0482eb1.png")
    print(f"Saved 59d8c89cd55cf0482eb1.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_b71b()
    render_3d8e()
    render_d28e()
    render_a265()
    render_59d8()
