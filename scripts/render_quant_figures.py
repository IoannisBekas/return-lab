import fitz
import numpy as np

def render_2ccb():
    # Figure 8.3: Decision Grid (Type I & Type II Errors)
    # 2000 x 882
    w, h = 2000, 882
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="24" />
  
  <!-- Table Container -->
  <rect x="50" y="50" width="1900" height="782" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Headers -->
  <rect x="50" y="50" width="550" height="180" fill="#f1f5f9" rx="16" />
  <rect x="600" y="50" width="1350" height="90" fill="#0284c7" rx="8" />
  
  <text x="325" y="155" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Decision</text>
  <text x="1275" y="112" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">True Condition</text>
  
  <!-- Subheaders for True Condition -->
  <rect x="600" y="140" width="675" height="90" fill="#e0f2fe" />
  <rect x="1275" y="140" width="675" height="90" fill="#e0f2fe" rx="8" />
  
  <text x="937" y="200" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">H₀ is true</text>
  <text x="1612" y="200" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">H₀ is false</text>

  <!-- Horizontal divider under headers -->
  <line x1="50" y1="230" x2="1950" y2="230" stroke="#cbd5e1" stroke-width="3" />
  <!-- Vertical dividers -->
  <line x1="600" y1="50" x2="600" y2="832" stroke="#cbd5e1" stroke-width="3" />
  <line x1="1275" y1="140" x2="1275" y2="832" stroke="#cbd5e1" stroke-width="3" />
  <line x1="50" y1="530" x2="1950" y2="530" stroke="#cbd5e1" stroke-width="3" />

  <!-- ROW 1: Do not reject H0 -->
  <text x="325" y="390" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Do not reject H₀</text>

  <!-- Cell (Row 1, Col 1): Correct Decision (Green) -->
  <rect x="620" y="250" width="635" height="260" fill="#f0fdf4" rx="12" />
  <text x="937" y="390" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Correct decision</text>

  <!-- Cell (Row 1, Col 2): Type II Error (Orange/Red) -->
  <rect x="1295" y="250" width="635" height="260" fill="#fef2f2" rx="12" />
  <text x="1612" y="355" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="38" text-anchor="middle">Incorrect decision</text>
  <text x="1612" y="425" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Type II error</text>

  <!-- ROW 2: Reject H0 -->
  <text x="325" y="690" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Reject H₀</text>

  <!-- Cell (Row 2, Col 1): Type I Error (Red) -->
  <rect x="620" y="550" width="635" height="260" fill="#fef2f2" rx="12" />
  <text x="937" y="620" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="36" text-anchor="middle">Incorrect decision</text>
  <text x="937" y="680" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Type I error</text>
  <text x="937" y="740" fill="#7f1d1d" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="500" text-anchor="middle">Significance level, α = P(Type I error)</text>

  <!-- Cell (Row 2, Col 2): Power of the test (Green) -->
  <rect x="1295" y="550" width="635" height="260" fill="#f0fdf4" rx="12" />
  <text x="1612" y="625" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Correct decision</text>
  <text x="1612" y="685" fill="#15803d" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Power of the test</text>
  <text x="1612" y="745" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="500" text-anchor="middle">= 1 – P(Type II error)</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/2ccbecb6fc5317f7554b.png")
    print(f"Saved 2ccbecb6fc5317f7554b.png ({pix.width}x{pix.height})")


def render_ec08():
    # Figure 8.4: Chi-square test decision rule table
    # 2272 x 662
    w, h = 2272, 662
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="24" />
  
  <rect x="50" y="45" width="2172" height="572" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Header background: Probability in Right Tail -->
  <rect x="590" y="45" width="1632" height="85" fill="#0284c7" rx="8" />
  <text x="1406" y="103" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Probability in Right Tail</text>

  <!-- Degrees of Freedom Header -->
  <rect x="50" y="45" width="540" height="175" fill="#f1f5f9" rx="16" />
  <text x="320" y="150" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Degrees of Freedom</text>

  <!-- Probability columns subheaders -->
  <!-- Col widths: 272 each for 6 cols -->
"""
    col_x = [590 + i * 272 for i in range(7)]
    prob_labels = ["0.975", "0.95", "0.90", "0.10", "0.05", "0.025"]
    for i, p in enumerate(prob_labels):
        cx = (col_x[i] + col_x[i+1]) / 2
        svg += f"""  <rect x="{col_x[i]}" y="130" width="272" height="90" fill="#e0f2fe" />
  <text x="{cx}" y="190" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">{p}</text>\n"""

    svg += """
  <line x1="50" y1="220" x2="2222" y2="220" stroke="#cbd5e1" stroke-width="3" />
  <line x1="590" y1="45" x2="590" y2="617" stroke="#cbd5e1" stroke-width="3" />
"""
    for x in col_x[1:-1]:
        svg += f"""  <line x1="{x}" y1="130" x2="{x}" y2="617" stroke="#e2e8f0" stroke-width="2" />\n"""

    rows = [
        ("9",  ["2.700", "3.325", "4.168", "14.684", "16.919", "19.023"]),
        ("10", ["3.247", "3.940", "4.865", "15.987", "18.307", "20.483"]),
        ("11", ["3.816", "4.575", "5.578", "17.275", "19.675", "21.920"]),
        ("30", ["16.791", "18.493", "20.599", "40.256", "43.773", "46.979"]),
    ]

    for r_idx, (df, vals) in enumerate(rows):
        y_top = 220 + r_idx * 99
        y_text = y_top + 62
        bg = "#ffffff" if r_idx % 2 == 0 else "#f8fafc"
        svg += f"""  <rect x="50" y="{y_top}" width="2172" height="99" fill="{bg}" />
  <text x="320" y="{y_text}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">{df}</text>\n"""
        for c_idx, val in enumerate(vals):
            cx = (col_x[c_idx] + col_x[c_idx+1]) / 2
            svg += f"""  <text x="{cx}" y="{y_text}" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="36" text-anchor="middle">{val}</text>\n"""
        if r_idx < len(rows) - 1:
            svg += f"""  <line x1="50" y1="{y_top + 99}" x2="2222" y2="{y_top + 99}" stroke="#e2e8f0" stroke-width="2" />\n"""

    svg += "</svg>"
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/ec0853b98c6f21d14c84.png")
    print(f"Saved ec0853b98c6f21d14c84.png ({pix.width}x{pix.height})")


def render_cdea():
    # Figure 9.1: Contingency table of observed frequencies
    # 1582 x 662
    w, h = 1582, 662
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="24" />
  
  <rect x="40" y="40" width="1502" height="582" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Header background: Dividend Yield -->
  <rect x="440" y="40" width="1102" height="75" fill="#0284c7" rx="8" />
  <text x="991" y="92" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Dividend Yield</text>

  <!-- Left Header: Earnings Growth -->
  <rect x="40" y="40" width="400" height="150" fill="#f1f5f9" rx="16" />
  <text x="240" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Earnings Growth</text>

  <!-- Subheaders for Dividend Yield -->
  <line x1="40" y1="190" x2="1542" y2="190" stroke="#cbd5e1" stroke-width="3" />
  <line x1="440" y1="40" x2="440" y2="622" stroke="#cbd5e1" stroke-width="3" />
"""
    col_x = [440, 715, 990, 1265, 1542]
    headers = ["Low", "Medium", "High", "Total"]
    for i, h_text in enumerate(headers):
        cx = (col_x[i] + col_x[i+1]) / 2
        bg = "#e0f2fe" if i < 3 else "#e2e8f0"
        txt_fill = "#0369a1" if i < 3 else "#0f172a"
        svg += f"""  <rect x="{col_x[i]}" y="115" width="{col_x[i+1]-col_x[i]}" height="75" fill="{bg}" />
  <text x="{cx}" y="165" fill="{txt_fill}" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">{h_text}</text>\n"""

    for x in col_x[1:-1]:
        svg += f"""  <line x1="{x}" y1="115" x2="{x}" y2="622" stroke="#e2e8f0" stroke-width="2" />\n"""

    rows = [
        ("Low",    ["28", "53", "42", "123"]),
        ("Medium", ["42", "32", "39", "113"]),
        ("High",   ["49", "25", "14", "88"]),
        ("Total",  ["119", "110", "95", "324"])
    ]

    for r_idx, (eg, vals) in enumerate(rows):
        y_top = 190 + r_idx * 108
        y_text = y_top + 68
        is_total = (r_idx == 3)
        bg = "#f1f5f9" if is_total else ("#ffffff" if r_idx % 2 == 0 else "#f8fafc")
        f_weight = "bold" if is_total else "normal"
        svg += f"""  <rect x="40" y="{y_top}" width="1502" height="108" fill="{bg}" />
  <text x="240" y="{y_text}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">{eg}</text>\n"""
        for c_idx, val in enumerate(vals):
            cx = (col_x[c_idx] + col_x[c_idx+1]) / 2
            cell_bold = "bold" if (is_total or c_idx == 3) else "normal"
            c_fill = "#0284c7" if (is_total and c_idx == 3) else "#0f172a" if cell_bold == "bold" else "#1e293b"
            svg += f"""  <text x="{cx}" y="{y_text}" fill="{c_fill}" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="{cell_bold}" text-anchor="middle">{val}</text>\n"""
        if r_idx < len(rows) - 1:
            div_color = "#cbd5e1" if is_total or r_idx == 2 else "#e2e8f0"
            div_w = 3 if r_idx == 2 else 2
            svg += f"""  <line x1="40" y1="{y_top + 108}" x2="1542" y2="{y_top + 108}" stroke="{div_color}" stroke-width="{div_w}" />\n"""

    svg += "</svg>"
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/cdeaad3ccf1b311495a8.png")
    print(f"Saved cdeaad3ccf1b311495a8.png ({pix.width}x{pix.height})")


def render_bcb8():
    # Figure 9.2: Expected frequencies table
    # 1770 x 555
    w, h = 1770, 555
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="24" />
  
  <rect x="40" y="40" width="1690" height="475" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Header background: Dividend Yield -->
  <rect x="490" y="40" width="1240" height="75" fill="#0284c7" rx="8" />
  <text x="1110" y="92" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Dividend Yield</text>

  <!-- Left Header: Earnings Growth -->
  <rect x="40" y="40" width="450" height="150" fill="#f1f5f9" rx="16" />
  <text x="265" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Earnings Growth</text>

  <!-- Subheaders for Dividend Yield -->
  <line x1="40" y1="190" x2="1730" y2="190" stroke="#cbd5e1" stroke-width="3" />
  <line x1="490" y1="40" x2="490" y2="515" stroke="#cbd5e1" stroke-width="3" />
"""
    col_x = [490, 903, 1316, 1730]
    headers = ["Low", "Medium", "High"]
    for i, h_text in enumerate(headers):
        cx = (col_x[i] + col_x[i+1]) / 2
        svg += f"""  <rect x="{col_x[i]}" y="115" width="{col_x[i+1]-col_x[i]}" height="75" fill="#e0f2fe" />
  <text x="{cx}" y="165" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">{h_text}</text>\n"""

    for x in col_x[1:-1]:
        svg += f"""  <line x1="{x}" y1="115" x2="{x}" y2="515" stroke="#e2e8f0" stroke-width="2" />\n"""

    rows = [
        ("Low",    ["45.2", "41.8", "36.1"]),
        ("Medium", ["41.5", "38.4", "33.1"]),
        ("High",   ["32.3", "29.9", "25.8"])
    ]

    for r_idx, (eg, vals) in enumerate(rows):
        y_top = 190 + r_idx * 108
        y_text = y_top + 68
        bg = "#ffffff" if r_idx % 2 == 0 else "#f8fafc"
        svg += f"""  <rect x="40" y="{y_top}" width="1690" height="108" fill="{bg}" />
  <text x="265" y="{y_text}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">{eg}</text>\n"""
        for c_idx, val in enumerate(vals):
            cx = (col_x[c_idx] + col_x[c_idx+1]) / 2
            svg += f"""  <text x="{cx}" y="{y_text}" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="34" text-anchor="middle">{val}</text>\n"""
        if r_idx < len(rows) - 1:
            svg += f"""  <line x1="40" y1="{y_top + 108}" x2="1730" y2="{y_top + 108}" stroke="#e2e8f0" stroke-width="2" />\n"""

    svg += "</svg>"
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/bcb83a7a80c17a1f4534.png")
    print(f"Saved bcb83a7a80c17a1f4534.png ({pix.width}x{pix.height})")


def render_b0c8():
    # Figure 9.3: Grid displaying calculated squared differences for Chi-square
    # 1892 x 680
    w, h = 1892, 680
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="24" />
  
  <rect x="40" y="40" width="1812" height="600" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="16" />

  <!-- Header background: Dividend Yield -->
  <rect x="520" y="40" width="1332" height="75" fill="#0284c7" rx="8" />
  <text x="1186" y="92" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Dividend Yield</text>

  <!-- Left Header: Earnings Growth -->
  <rect x="40" y="40" width="480" height="150" fill="#f1f5f9" rx="16" />
  <text x="280" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Earnings Growth</text>

  <!-- Subheaders for Dividend Yield -->
  <line x1="40" y1="190" x2="1852" y2="190" stroke="#cbd5e1" stroke-width="3" />
  <line x1="520" y1="40" x2="520" y2="540" stroke="#cbd5e1" stroke-width="3" />
"""
    col_x = [520, 964, 1408, 1852]
    headers = ["Low", "Medium", "High"]
    for i, h_text in enumerate(headers):
        cx = (col_x[i] + col_x[i+1]) / 2
        svg += f"""  <rect x="{col_x[i]}" y="115" width="{col_x[i+1]-col_x[i]}" height="75" fill="#e0f2fe" />
  <text x="{cx}" y="165" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">{h_text}</text>\n"""

    for x in col_x[1:-1]:
        svg += f"""  <line x1="{x}" y1="115" x2="{x}" y2="540" stroke="#e2e8f0" stroke-width="2" />\n"""

    rows = [
        ("Low",    ["6.5451", "3.0010", "0.9643"]),
        ("Medium", ["0.0060", "1.0667", "1.0517"]),
        ("High",   ["8.6344", "0.8030", "5.3969"])
    ]

    for r_idx, (eg, vals) in enumerate(rows):
        y_top = 190 + r_idx * 116
        y_text = y_top + 72
        bg = "#ffffff" if r_idx % 2 == 0 else "#f8fafc"
        svg += f"""  <rect x="40" y="{y_top}" width="1812" height="116" fill="{bg}" />
  <text x="280" y="{y_text}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">{eg}</text>\n"""
        for c_idx, val in enumerate(vals):
            cx = (col_x[c_idx] + col_x[c_idx+1]) / 2
            svg += f"""  <text x="{cx}" y="{y_text}" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="34" text-anchor="middle">{val}</text>\n"""
        svg += f"""  <line x1="40" y1="{y_top + 116}" x2="1852" y2="{y_top + 116}" stroke="#cbd5e1" stroke-width="2" />\n"""

    # Bottom Sum Box
    svg += f"""  <rect x="520" y="540" width="1332" height="100" fill="#f0f9ff" rx="8" />
  <text x="1186" y="605" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">Sum = 27.4691</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b0c855a8963d32275a89.png")
    print(f"Saved b0c855a8963d32275a89.png ({pix.width}x{pix.height})")


def render_507b():
    # Figure 10.8: Residual plot exhibiting parabolic pattern
    # 1947 x 1547
    w, h = 1947, 1547
    
    # Coordinates of plot area
    x_left = 220
    x_right = 1860
    y_top = 100
    y_bottom = 1380

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- Plot Card Area -->
  <rect x="{x_left}" y="{y_top}" width="{x_right - x_left}" height="{y_bottom - y_top}" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="12" />

  <!-- Grid lines and Y labels: 0.00 to 20.00 (step 2.00) -->
"""
    for val in range(0, 21, 2):
        y = y_bottom - (val / 20.0) * (y_bottom - y_top)
        svg += f"""  <line x1="{x_left}" y1="{y}" x2="{x_right}" y2="{y}" stroke="#f1f5f9" stroke-width="2" stroke-dasharray="6 6" />
  <text x="{x_left - 25}" y="{y + 12}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">{val:.2f}</text>\n"""

    # X-axis ticks: 0, 5, 10, 15, 20, 25
    for val in [0, 5, 10, 15, 20, 25]:
        x = x_left + (val / 25.0) * (x_right - x_left)
        svg += f"""  <line x1="{x}" y1="{y_top}" x2="{x}" y2="{y_bottom}" stroke="#f1f5f9" stroke-width="2" stroke-dasharray="6 6" />
  <text x="{x}" y="{y_bottom + 60}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">{val}</text>\n"""

    # Data points from x=1 to x=25 with quadratic growth
    xs = np.arange(1, 26)
    # Fit y values to match scan: at x=1 y~1.6, at x=25 y=20.0
    ys = 1.5 + 0.0296 * (xs ** 2)

    for x_val, y_val in zip(xs, ys):
        cx = x_left + (x_val / 25.0) * (x_right - x_left)
        cy = y_bottom - (y_val / 20.0) * (y_bottom - y_top)
        svg += f"""  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="15" fill="#0284c7" stroke="#ffffff" stroke-width="3" />\n"""

    svg += "</svg>"
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/507b49cf9328de958f2e.png")
    print(f"Saved 507b49cf9328de958f2e.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_2ccb()
    render_ec08()
    render_cdea()
    render_bcb8()
    render_b0c8()
    render_507b()
