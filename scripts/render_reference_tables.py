import fitz, math, os, sys
import scipy.stats as st
sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = "public/content/figures"

def render_svg_to_png(svg_str, output_path, target_width, target_height):
    doc = fitz.open(stream=svg_str.encode('utf-8'), filetype="svg")
    page = doc[0]
    rect = page.rect
    zoom_x = target_width / rect.width
    zoom_y = target_height / rect.height
    mat = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(output_path)
    print(f"Saved {os.path.basename(output_path)} ({pix.width}x{pix.height})")

# 1. 236c50cbc08d6783fb2c.png (2042x3102) - Positive Z Normal Table (0.0 to 3.0)
def generate_svg_positive_z():
    width = 1000
    height = 1520
    
    # Table headers: z, 0.00, 0.01, ..., 0.09
    cols = ["z"] + [f"{c/100:.2f}" for c in range(10)]
    col_w = [70] + [85] * 10
    start_x = 35
    start_y = 230
    row_h = 37

    svg = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0284c7" />
    </marker>
  </defs>

  <rect x="15" y="15" width="{width-30}" height="{height-30}" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="35" y="35" width="{width-70}" height="{height-70}" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Normal Distribution Illustration -->
  <g transform="translate(360, 50)">
    <!-- Base line -->
    <line x1="0" y1="120" x2="280" y2="120" stroke="#334155" stroke-width="2" />
    <!-- Shaded area for P(Z <= z) where z > 0 (at x=190) -->
    <path d="M 10 120 C 60 120 100 20 140 20 C 160 20 175 40 190 60 L 190 120 Z" fill="#0284c7" fill-opacity="0.25" />
    <!-- Bell Curve -->
    <path d="M 10 120 C 60 120 100 20 140 20 C 180 20 220 120 270 120" fill="none" stroke="#0284c7" stroke-width="3" />
    <!-- Vertical dividing line at z -->
    <line x1="190" y1="60" x2="190" y2="120" stroke="#0f172a" stroke-width="2" />
    <text x="190" y="140" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">z</text>
    <!-- Label P(Z <= z) -->
    <line x1="90" y1="40" x2="135" y2="70" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow)" />
    <text x="85" y="35" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="end">P(Z ≤ z)</text>
  </g>

  <!-- Table Title Badge -->
  <rect x="50" y="55" width="280" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="65" y="78" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1">Standard Normal Table: P(Z ≤ z)</text>
"""]

    # Table Header Row
    svg.append(f'<rect x="{start_x+10}" y="{start_y}" width="{sum(col_w)}" height="42" rx="6" fill="#0284c7" />')
    cur_x = start_x + 10
    for i, col in enumerate(cols):
        w = col_w[i]
        anchor = "center"
        tx = cur_x + w/2
        svg.append(f'<text x="{tx}" y="{start_y + 26}" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">{col}</text>')
        cur_x += w

    # Rows: z from 0.0 to 3.0 (31 rows)
    y = start_y + 46
    for r in range(31):
        z_val = r / 10.0
        row_bg = "#f8fafc" if r % 2 == 1 else "#ffffff"
        # subtle divider or grouping every 5 rows
        stroke_bottom = 'stroke="#cbd5e1" stroke-width="1.5"' if r % 5 == 4 else ""
        svg.append(f'<rect x="{start_x+10}" y="{y}" width="{sum(col_w)}" height="{row_h}" fill="{row_bg}" {stroke_bottom} />')
        
        # Col 0: z
        cur_x = start_x + 10
        svg.append(f'<text x="{cur_x + col_w[0]/2}" y="{y + 24}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">{z_val:.1f}</text>')
        cur_x += col_w[0]

        # Cols 1-10: P(Z <= z_val + col/100)
        for c in range(10):
            z_tot = z_val + c / 100.0
            prob = st.norm.cdf(z_tot)
            prob_str = f"{prob:.4f}"
            svg.append(f'<text x="{cur_x + col_w[c+1]/2}" y="{y + 24}" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#1e293b" text-anchor="middle">{prob_str}</text>')
            cur_x += col_w[c+1]

        y += row_h

    svg.append("</svg>")
    return "".join(svg)

# 2. d6ad52dc87eef482d15b.png (2034x2788) - Negative Z Normal Table (0.0 to -3.0)
def generate_svg_negative_z():
    width = 1000
    height = 1370
    
    cols = ["z"] + [f"{c/100:.2f}" for c in range(10)]
    col_w = [70] + [85] * 10
    start_x = 35
    start_y = 200
    row_h = 36

    svg = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0284c7" />
    </marker>
  </defs>

  <rect x="15" y="15" width="{width-30}" height="{height-30}" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="35" y="35" width="{width-70}" height="{height-70}" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Normal Distribution Illustration (Negative Tail) -->
  <g transform="translate(360, 45)">
    <line x1="0" y1="110" x2="280" y2="110" stroke="#334155" stroke-width="2" />
    <!-- Shaded area for P(Z <= -z) on left tail (up to x=90) -->
    <path d="M 10 110 C 50 110 75 80 90 60 L 90 110 Z" fill="#0284c7" fill-opacity="0.25" />
    <path d="M 10 110 C 60 110 100 20 140 20 C 180 20 220 110 270 110" fill="none" stroke="#0284c7" stroke-width="3" />
    <line x1="90" y1="60" x2="90" y2="110" stroke="#0f172a" stroke-width="2" />
    <text x="90" y="130" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">−z</text>
    <!-- Label P(Z <= z) -->
    <line x1="160" y1="40" x2="80" y2="75" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow)" />
    <text x="170" y="42" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">P(Z ≤ −z)</text>
  </g>

  <!-- Table Title Badge -->
  <rect x="50" y="55" width="280" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="65" y="78" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1">Standard Normal Table: P(Z ≤ −z)</text>
"""]

    # Table Header Row
    svg.append(f'<rect x="{start_x+10}" y="{start_y}" width="{sum(col_w)}" height="40" rx="6" fill="#0284c7" />')
    cur_x = start_x + 10
    for i, col in enumerate(cols):
        w = col_w[i]
        tx = cur_x + w/2
        svg.append(f'<text x="{tx}" y="{start_y + 25}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">{col}</text>')
        cur_x += w

    # Rows: -0.0 to -3.0 (31 rows)
    y = start_y + 44
    for r in range(31):
        z_abs = r / 10.0
        z_str = f"0.0" if r == 0 else f"−{z_abs:.1f}"
        row_bg = "#f8fafc" if r % 2 == 1 else "#ffffff"
        stroke_bottom = 'stroke="#cbd5e1" stroke-width="1.5"' if r % 5 == 4 else ""
        svg.append(f'<rect x="{start_x+10}" y="{y}" width="{sum(col_w)}" height="{row_h}" fill="{row_bg}" {stroke_bottom} />')
        
        cur_x = start_x + 10
        svg.append(f'<text x="{cur_x + col_w[0]/2}" y="{y + 23}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">{z_str}</text>')
        cur_x += col_w[0]

        for c in range(10):
            z_tot = - (z_abs + c / 100.0)
            prob = st.norm.cdf(z_tot)
            prob_str = f"{prob:.4f}"
            svg.append(f'<text x="{cur_x + col_w[c+1]/2}" y="{y + 23}" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#1e293b" text-anchor="middle">{prob_str}</text>')
            cur_x += col_w[c+1]

        y += row_h

    svg.append("</svg>")
    return "".join(svg)

# 3. 5463b8f4d7dbe4792cb4.png (1986x2914) - Student's t Table
def generate_svg_t_table():
    width = 1000
    height = 1460

    # One-tailed alphas: 0.100, 0.050, 0.025, 0.010, 0.005, 0.0005
    # Two-tailed alphas: 0.20, 0.10, 0.05, 0.02, 0.01, 0.001
    alphas_1 = [0.100, 0.050, 0.025, 0.010, 0.005, 0.0005]
    alphas_2 = [0.20, 0.10, 0.05, 0.02, 0.01, 0.001]
    df_rows = list(range(1, 31)) + [40, 60, 120, 999999] # 999999 represents infinity

    col_w = [110] + [135] * 6
    start_x = 40
    start_y = 60
    row_h = 36

    svg = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="15" y="15" width="{width-30}" height="{height-30}" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="35" y="35" width="{width-70}" height="{height-70}" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Double Header for One-Tailed and Two-Tailed -->
  <!-- Top Bar: One-Tailed -->
  <rect x="{start_x+10}" y="{start_y}" width="{sum(col_w)}" height="32" rx="6" fill="#0284c7" />
  <text x="{start_x + 10 + sum(col_w)/2}" y="{start_y + 22}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">Level of Significance for One-Tailed Test</text>

  <!-- One-tailed values row -->
  <rect x="{start_x+10}" y="{start_y + 34}" width="{sum(col_w)}" height="32" fill="#e0f2fe" />
  <text x="{start_x + 10 + col_w[0]/2}" y="{start_y + 55}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1" text-anchor="middle">df</text>
"""]

    cur_x = start_x + 10 + col_w[0]
    for a1 in alphas_1:
        svg.append(f'<text x="{cur_x + 135/2}" y="{start_y + 55}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1" text-anchor="middle">{a1}</text>')
        cur_x += 135

    # Second Bar: Two-Tailed
    y_h2 = start_y + 70
    svg.append(f'<rect x="{start_x+10}" y="{y_h2}" width="{sum(col_w)}" height="32" rx="6" fill="#0369a1" />')
    svg.append(f'<text x="{start_x + 10 + sum(col_w)/2}" y="{y_h2 + 22}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">Level of Significance for Two-Tailed Test</text>')

    # Two-tailed values row
    svg.append(f'<rect x="{start_x+10}" y="{y_h2 + 34}" width="{sum(col_w)}" height="32" fill="#bae6fd" />')
    svg.append(f'<text x="{start_x + 10 + col_w[0]/2}" y="{y_h2 + 55}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0c4a6e" text-anchor="middle">df</text>')

    cur_x = start_x + 10 + col_w[0]
    for a2 in alphas_2:
        svg.append(f'<text x="{cur_x + 135/2}" y="{y_h2 + 55}" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0c4a6e" text-anchor="middle">{a2}</text>')
        cur_x += 135

    # Data Rows
    y = y_h2 + 70
    for idx, df in enumerate(df_rows):
        row_bg = "#f8fafc" if idx % 2 == 1 else "#ffffff"
        stroke_bottom = 'stroke="#cbd5e1" stroke-width="1.5"' if (idx in [4, 9, 14, 19, 24, 29, 33]) else ""
        svg.append(f'<rect x="{start_x+10}" y="{y}" width="{sum(col_w)}" height="{row_h}" fill="{row_bg}" {stroke_bottom} />')
        
        df_label = "∞" if df == 999999 else str(df)
        cur_x = start_x + 10
        svg.append(f'<text x="{cur_x + col_w[0]/2}" y="{y + 24}" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="middle">{df_label}</text>')
        cur_x += col_w[0]

        for a1 in alphas_1:
            if df == 999999:
                val = st.norm.ppf(1 - a1)
            else:
                val = st.t.ppf(1 - a1, df)
            val_str = f"{val:.3f}" if val < 100 else f"{val:.1f}"
            svg.append(f'<text x="{cur_x + 135/2}" y="{y + 24}" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#1e293b" text-anchor="middle">{val_str}</text>')
            cur_x += 135

        y += row_h

    svg.append("</svg>")
    return "".join(svg)

# 4. 4c03d785ccda6e4dbc55.png (2252x2342) - F-Distribution 5% Table
def generate_svg_f_table_5pct():
    width = 1100
    height = 1140

    df1_cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 24, 30, 40]
    df2_rows = list(range(1, 26)) + [30, 40, 60, 120, 999999]

    col_w = [60] + [62] * 16
    start_x = 25
    start_y = 60
    row_h = 32

    svg = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="15" y="15" width="{width-30}" height="{height-30}" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="30" y="30" width="{width-60}" height="{height-60}" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="50" y="45" width="460" height="30" rx="6" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="65" y="65" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0369a1">F-Distribution Critical Values (α = 0.05 in right tail)</text>
"""]

    # Table Header Row: df1 at Y=90
    y_header = 90
    svg.append(f'<rect x="{start_x}" y="{y_header}" width="{sum(col_w)}" height="34" rx="6" fill="#0284c7" />')
    svg.append(f'<text x="{start_x + col_w[0]/2}" y="{y_header + 22}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">df2\\df1</text>')

    cur_x = start_x + col_w[0]
    for df1 in df1_cols:
        svg.append(f'<text x="{cur_x + 62/2}" y="{y_header + 22}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">{df1}</text>')
        cur_x += 62

    # Data Rows
    y = y_header + 38
    for idx, df2 in enumerate(df2_rows):
        row_bg = "#f8fafc" if idx % 2 == 1 else "#ffffff"
        stroke_bottom = 'stroke="#cbd5e1" stroke-width="1.5"' if (idx in [4, 9, 14, 19, 24]) else ""
        svg.append(f'<rect x="{start_x}" y="{y}" width="{sum(col_w)}" height="{row_h}" fill="{row_bg}" {stroke_bottom} />')

        df2_label = "∞" if df2 == 999999 else str(df2)
        cur_x = start_x
        svg.append(f'<text x="{cur_x + col_w[0]/2}" y="{y + 21}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0f172a" text-anchor="middle">{df2_label}</text>')
        cur_x += col_w[0]

        for df1 in df1_cols:
            if df2 == 999999:
                val = st.chi2.ppf(0.95, df1) / df1
            else:
                val = st.f.ppf(0.95, df1, df2)
            
            if val >= 100:
                val_str = f"{val:.0f}"
            elif val >= 10:
                val_str = f"{val:.1f}"
            else:
                val_str = f"{val:.2f}"
            svg.append(f'<text x="{cur_x + 62/2}" y="{y + 21}" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#1e293b" text-anchor="middle">{val_str}</text>')
            cur_x += 62

        y += row_h

    svg.append("</svg>")
    return "".join(svg)

# 5. a5cbb7719f7458f34a22.png (2538x2342) - F-Distribution 2.5% Table
def generate_svg_f_table_2_5pct():
    width = 1100
    height = 1140

    df1_cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 24, 30, 40]
    df2_rows = list(range(1, 26)) + [30, 40, 60, 120, 999999]

    col_w = [60] + [62] * 16
    start_x = 25
    row_h = 32

    svg = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="15" y="15" width="{width-30}" height="{height-30}" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="30" y="30" width="{width-60}" height="{height-60}" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="50" y="45" width="460" height="30" rx="6" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="65" y="65" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0369a1">F-Distribution Critical Values (α = 0.025 in right tail)</text>
"""]

    y_header = 90
    svg.append(f'<rect x="{start_x}" y="{y_header}" width="{sum(col_w)}" height="34" rx="6" fill="#0284c7" />')
    svg.append(f'<text x="{start_x + col_w[0]/2}" y="{y_header + 22}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">df2\\df1</text>')

    cur_x = start_x + col_w[0]
    for df1 in df1_cols:
        svg.append(f'<text x="{cur_x + 62/2}" y="{y_header + 22}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">{df1}</text>')
        cur_x += 62

    y = y_header + 38
    for idx, df2 in enumerate(df2_rows):
        row_bg = "#f8fafc" if idx % 2 == 1 else "#ffffff"
        stroke_bottom = 'stroke="#cbd5e1" stroke-width="1.5"' if (idx in [4, 9, 14, 19, 24]) else ""
        svg.append(f'<rect x="{start_x}" y="{y}" width="{sum(col_w)}" height="{row_h}" fill="{row_bg}" {stroke_bottom} />')

        df2_label = "∞" if df2 == 999999 else str(df2)
        cur_x = start_x
        svg.append(f'<text x="{cur_x + col_w[0]/2}" y="{y + 21}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0f172a" text-anchor="middle">{df2_label}</text>')
        cur_x += col_w[0]

        for df1 in df1_cols:
            if df2 == 999999:
                val = st.chi2.ppf(0.975, df1) / df1
            else:
                val = st.f.ppf(0.975, df1, df2)
            
            if val >= 100:
                val_str = f"{val:.0f}"
            elif val >= 10:
                val_str = f"{val:.2f}"
            else:
                val_str = f"{val:.2f}"
            svg.append(f'<text x="{cur_x + 62/2}" y="{y + 21}" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#1e293b" text-anchor="middle">{val_str}</text>')
            cur_x += 62

        y += row_h

    svg.append("</svg>")
    return "".join(svg)

# 6. fd7cdf02d96a2690be89.png (2226x2590) - Chi-Squared Table
def generate_svg_chi2_table():
    width = 1000
    height = 1270

    p_cols = [0.99, 0.975, 0.95, 0.90, 0.10, 0.05, 0.025, 0.01, 0.005]
    df_rows = list(range(1, 26)) + list(range(26, 31)) + [50, 60, 80, 100]

    col_w = [140] + [90] * 9
    start_x = 25
    row_h = 32

    svg = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="15" y="15" width="{width-30}" height="{height-30}" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="30" y="30" width="{width-60}" height="{height-60}" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="45" y="45" width="460" height="30" rx="6" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="60" y="65" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0369a1">Chi-Squared (χ²) Distribution Right-Tail Critical Values</text>
"""]

    y_header = 90
    svg.append(f'<rect x="{start_x}" y="{y_header}" width="{sum(col_w)}" height="34" rx="6" fill="#0284c7" />')
    svg.append(f'<text x="{start_x + col_w[0]/2}" y="{y_header + 22}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">Degrees of Freedom</text>')

    cur_x = start_x + col_w[0]
    for p in p_cols:
        svg.append(f'<text x="{cur_x + 90/2}" y="{y_header + 22}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">{p}</text>')
        cur_x += 90

    y = y_header + 38
    for idx, df in enumerate(df_rows):
        row_bg = "#f8fafc" if idx % 2 == 1 else "#ffffff"
        stroke_bottom = 'stroke="#cbd5e1" stroke-width="1.5"' if (idx in [4, 9, 14, 19, 24, 29]) else ""
        svg.append(f'<rect x="{start_x}" y="{y}" width="{sum(col_w)}" height="{row_h}" fill="{row_bg}" {stroke_bottom} />')

        cur_x = start_x
        svg.append(f'<text x="{cur_x + col_w[0]/2}" y="{y + 21}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0f172a" text-anchor="middle">{df}</text>')
        cur_x += col_w[0]

        for p in p_cols:
            val = st.chi2.ppf(1 - p, df)
            if val < 0.001:
                val_str = f"{val:.6f}"
            elif val < 0.01:
                val_str = f"{val:.5f}"
            elif val < 1.0:
                val_str = f"{val:.4f}"
            elif val < 10.0:
                val_str = f"{val:.3f}"
            elif val < 100.0:
                val_str = f"{val:.3f}"
            else:
                val_str = f"{val:.3f}"
            svg.append(f'<text x="{cur_x + 90/2}" y="{y + 21}" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#1e293b" text-anchor="middle">{val_str}</text>')
            cur_x += 90

        y += row_h

    svg.append("</svg>")
    return "".join(svg)

def main():
    items = [
        ("236c50cbc08d6783fb2c.png", generate_svg_positive_z(), 2042, 3102),
        ("d6ad52dc87eef482d15b.png", generate_svg_negative_z(), 2034, 2788),
        ("5463b8f4d7dbe4792cb4.png", generate_svg_t_table(), 1986, 2914),
        ("4c03d785ccda6e4dbc55.png", generate_svg_f_table_5pct(), 2252, 2342),
        ("a5cbb7719f7458f34a22.png", generate_svg_f_table_2_5pct(), 2538, 2342),
        ("fd7cdf02d96a2690be89.png", generate_svg_chi2_table(), 2226, 2590),
    ]

    for fname, svg_str, w, h in items:
        out_path = os.path.join(OUTPUT_DIR, fname)
        render_svg_to_png(svg_str, out_path, w, h)

if __name__ == "__main__":
    main()
