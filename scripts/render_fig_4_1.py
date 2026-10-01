import fitz
import math

def generate_figure_4_1():
    w, h = 1004, 562
    
    # Coordinates
    root_x, root_y = 270, 281
    n1_x, n1_y = 505, 145
    n2_x, n2_y = 505, 417
    
    # Outcomes
    out_x = 735
    o1_y = 70
    o2_y = 220
    o3_y = 342
    o4_y = 492
    
    # Angles
    ang_stage1 = math.degrees(math.atan2(n1_y - root_y, n1_x - root_x)) # ~ -30.0 deg
    ang_stage2_up = math.degrees(math.atan2(o1_y - n1_y, out_x - n1_x)) # ~ -18.0 deg
    ang_stage2_dn = math.degrees(math.atan2(o2_y - n1_y, out_x - n1_x)) # ~ +18.0 deg

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <!-- Background -->
  <rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff" />

  <!-- Root box (left) -->
  <rect x="24" y="171" width="246" height="220" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5" rx="8" />
  <text x="38" y="203" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">Expected EPS = $1.51</text>
  <line x1="38" y1="213" x2="256" y2="213" stroke="#bae6fd" stroke-width="1.5" />
  
  <text x="38" y="239" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold">Calculation:</text>
  <text x="38" y="263" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="14">(18% × $1.80) +</text>
  <text x="38" y="287" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="14">(42% × $1.70) +</text>
  <text x="38" y="311" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="14">(24% × $1.30) +</text>
  <text x="38" y="335" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="14">(16% × $1.00)</text>
  <text x="38" y="369" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">= $1.51</text>

  <!-- Stage 1 Branch lines -->
  <line x1="{root_x}" y1="{root_y}" x2="{n1_x}" y2="{n1_y}" stroke="#1e293b" stroke-width="3" stroke-linecap="round" />
  <line x1="{root_x}" y1="{root_y}" x2="{n2_x}" y2="{n2_y}" stroke="#1e293b" stroke-width="3" stroke-linecap="round" />

  <!-- Stage 1 Nodes -->
  <circle cx="{n1_x}" cy="{n1_y}" r="5.5" fill="#1e293b" />
  <circle cx="{n2_x}" cy="{n2_y}" r="5.5" fill="#1e293b" />

  <!-- Stage 1 Labels (Parallel to branch lines) -->
  <!-- Upper: Good economy (parallel above line) -->
  <!-- Midpoint is ~ (387, 213). Shift perpendicular by ~14px up-left -->
  <g transform="translate(380, 203) rotate({ang_stage1})">
    <text x="0" y="-18" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold">Prob. of good economy</text>
    <text x="0" y="-2" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold">= 60%</text>
  </g>

  <!-- Lower: Poor economy (parallel below line) -->
  <!-- Midpoint is ~ (387, 349). Shift perpendicular by ~14px down-left -->
  <g transform="translate(380, 359) rotate({-ang_stage1})">
    <text x="0" y="16" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold">Prob. of poor economy</text>
    <text x="0" y="32" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold">= 40%</text>
  </g>

  <!-- Stage 2 Branch lines from Good economy -->
  <line x1="{n1_x}" y1="{n1_y}" x2="{out_x}" y2="{o1_y}" stroke="#1e293b" stroke-width="3" stroke-linecap="round" />
  <line x1="{n1_x}" y1="{n1_y}" x2="{out_x}" y2="{o2_y}" stroke="#1e293b" stroke-width="3" stroke-linecap="round" />

  <!-- Stage 2 Labels (Good Economy) -->
  <!-- Upper: Good results (parallel above line) -->
  <!-- Midpoint is ~ (620, 107) -->
  <g transform="translate(615, 99) rotate({ang_stage2_up})">
    <text x="0" y="-17" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold">Prob. of good results</text>
    <text x="0" y="-1" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold">= 30%</text>
  </g>

  <!-- Lower: Poor results (parallel below line) -->
  <!-- Midpoint is ~ (620, 182) -->
  <g transform="translate(615, 191) rotate({ang_stage2_dn})">
    <text x="0" y="15" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold">Prob. of poor results</text>
    <text x="0" y="31" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold">= 70%</text>
  </g>

  <!-- Stage 2 Branch lines from Poor economy -->
  <line x1="{n2_x}" y1="{n2_y}" x2="{out_x}" y2="{o3_y}" stroke="#1e293b" stroke-width="3" stroke-linecap="round" />
  <line x1="{n2_x}" y1="{n2_y}" x2="{out_x}" y2="{o4_y}" stroke="#1e293b" stroke-width="3" stroke-linecap="round" />

  <!-- Stage 2 Labels (Poor Economy) -->
  <!-- Upper: Good results (parallel above line) -->
  <!-- Midpoint is ~ (620, 379) -->
  <g transform="translate(615, 371) rotate({ang_stage2_up})">
    <text x="0" y="-17" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold">Prob. of good results</text>
    <text x="0" y="-1" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold">= 60%</text>
  </g>

  <!-- Lower: Poor results (parallel below line) -->
  <!-- Midpoint is ~ (620, 454) -->
  <g transform="translate(615, 463) rotate({ang_stage2_dn})">
    <text x="0" y="15" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold">Prob. of poor results</text>
    <text x="0" y="31" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold">= 40%</text>
  </g>

  <!-- OUTCOME BOX 1: EPS $1.80, Prob 18% -->
  <rect x="{out_x}" y="25" width="245" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5" rx="8" />
  <text x="{out_x + 18}" y="52" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">EPS = $1.80</text>
  <text x="{out_x + 18}" y="76" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="14">Prob = (60% × 30%)</text>
  <text x="{out_x + 18}" y="100" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">= 18%</text>

  <!-- OUTCOME BOX 2: EPS $1.70, Prob 42% -->
  <rect x="{out_x}" y="175" width="245" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5" rx="8" />
  <text x="{out_x + 18}" y="202" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">EPS = $1.70</text>
  <text x="{out_x + 18}" y="226" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="14">Prob = (60% × 70%)</text>
  <text x="{out_x + 18}" y="250" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">= 42%</text>

  <!-- OUTCOME BOX 3: EPS $1.30, Prob 24% -->
  <rect x="{out_x}" y="297" width="245" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5" rx="8" />
  <text x="{out_x + 18}" y="324" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">EPS = $1.30</text>
  <text x="{out_x + 18}" y="348" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="14">Prob = (40% × 60%)</text>
  <text x="{out_x + 18}" y="372" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">= 24%</text>

  <!-- OUTCOME BOX 4: EPS $1.00, Prob 16% -->
  <rect x="{out_x}" y="447" width="245" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="2.5" rx="8" />
  <text x="{out_x + 18}" y="474" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">EPS = $1.00</text>
  <text x="{out_x + 18}" y="498" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="14">Prob = (40% × 40%)</text>
  <text x="{out_x + 18}" y="522" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold">= 16%</text>

</svg>"""

    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    page = doc[0]
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save("public/content/figures/dbce15c32e7f233b9acd.png")
    print(f"Saved dbce15c32e7f233b9acd.png with size {pix.width}x{pix.height}")

if __name__ == "__main__":
    generate_figure_4_1()
