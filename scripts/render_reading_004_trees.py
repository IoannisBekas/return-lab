import fitz
import math

def render_0f8b():
    # 0f8b04065cedff265396.png: 2160 x 1087
    w, h = 2160, 1087
    
    root_x, root_y = 120, 543
    n1_x, n1_y = 820, 290
    n2_x, n2_y = 820, 796
    
    # Sub branch end points
    o1_x, o1_y = 1250, 140
    o2_x, o2_y = 1250, 440
    o3_x, o3_y = 1250, 646
    o4_x, o4_y = 1250, 946

    # Angles
    ang1 = math.degrees(math.atan2(n1_y - root_y, n1_x - root_x))
    ang_o1 = math.degrees(math.atan2(o1_y - n1_y, o1_x - n1_x))
    ang_o2 = math.degrees(math.atan2(o2_y - n1_y, o1_x - n1_x))
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <!-- Card Background -->
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- Branches -->
  <line x1="{root_x}" y1="{root_y}" x2="{n1_x}" y2="{n1_y}" stroke="#1e293b" stroke-width="8" stroke-linecap="round" />
  <line x1="{root_x}" y1="{root_y}" x2="{n2_x}" y2="{n2_y}" stroke="#1e293b" stroke-width="8" stroke-linecap="round" />

  <line x1="{n1_x}" y1="{n1_y}" x2="{o1_x}" y2="{o1_y}" stroke="#0284c7" stroke-width="7" stroke-linecap="round" />
  <line x1="{n1_x}" y1="{n1_y}" x2="{o2_x}" y2="{o2_y}" stroke="#0284c7" stroke-width="7" stroke-linecap="round" />

  <line x1="{n2_x}" y1="{n2_y}" x2="{o3_x}" y2="{o3_y}" stroke="#0284c7" stroke-width="7" stroke-linecap="round" />
  <line x1="{n2_x}" y1="{n2_y}" x2="{o4_x}" y2="{o4_y}" stroke="#0284c7" stroke-width="7" stroke-linecap="round" />

  <!-- Nodes -->
  <circle cx="{root_x}" cy="{root_y}" r="15" fill="#1e293b" />
  <circle cx="{n1_x}" cy="{n1_y}" r="15" fill="#1e293b" />
  <circle cx="{n2_x}" cy="{n2_y}" r="15" fill="#1e293b" />
  <circle cx="{o1_x}" cy="{o1_y}" r="13" fill="#0284c7" />
  <circle cx="{o2_x}" cy="{o2_y}" r="13" fill="#0284c7" />
  <circle cx="{o3_x}" cy="{o3_y}" r="13" fill="#0284c7" />
  <circle cx="{o4_x}" cy="{o4_y}" r="13" fill="#0284c7" />

  <!-- Stage 1 Labels (Parallel to branch lines) -->
  <g transform="translate(470, 416) rotate({ang1})">
    <text x="0" y="-30" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">60% outperform</text>
  </g>

  <g transform="translate(470, 670) rotate({-ang1})">
    <text x="0" y="55" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">40% underperform</text>
  </g>

  <!-- Stage 2 Labels (Parallel) -->
  <g transform="translate(1035, 215) rotate({ang_o1})">
    <text x="0" y="-25" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">70% up</text>
  </g>

  <g transform="translate(1035, 365) rotate({ang_o2})">
    <text x="0" y="45" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">30% dn</text>
  </g>

  <g transform="translate(1035, 721) rotate({ang_o1})">
    <text x="0" y="-25" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">20% up</text>
  </g>

  <g transform="translate(1035, 871) rotate({ang_o2})">
    <text x="0" y="45" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">80% dn</text>
  </g>

  <!-- Terminal outcome text -->
  <text x="{o1_x + 40}" y="{o1_y + 14}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">42% <tspan font-weight="500" fill="#334155">(outperform + gains)</tspan></text>
  <text x="{o2_x + 40}" y="{o2_y + 14}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">18% <tspan font-weight="500" fill="#334155">(outperform + no gains)</tspan></text>
  <text x="{o3_x + 40}" y="{o3_y + 14}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">8% <tspan font-weight="500" fill="#334155">(underperform + gains)</tspan></text>
  <text x="{o4_x + 40}" y="{o4_y + 14}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">32% <tspan font-weight="500" fill="#334155">(underperform + no gains)</tspan></text>

</svg>"""

    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/0f8b04065cedff265396.png")
    print(f"Saved 0f8b04065cedff265396.png ({pix.width}x{pix.height})")


def render_dc31():
    # dc31279e9262d8e1f0de.png: 2195 x 972
    w, h = 2195, 972
    
    root_x, root_y = 110, 486
    n1_x, n1_y = 750, 240
    n2_x, n2_y = 750, 732
    
    o1_x, o1_y = 1200, 95
    o2_x, o2_y = 1200, 385
    o3_x, o3_y = 1200, 587
    o4_x, o4_y = 1200, 877

    ang1 = math.degrees(math.atan2(n1_y - root_y, n1_x - root_x))
    ang_o1 = math.degrees(math.atan2(o1_y - n1_y, o1_x - n1_x))
    ang_o2 = math.degrees(math.atan2(o2_y - n1_y, o1_x - n1_x))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <!-- Card Background -->
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- Branches -->
  <line x1="{root_x}" y1="{root_y}" x2="{n1_x}" y2="{n1_y}" stroke="#1e293b" stroke-width="7" stroke-linecap="round" />
  <line x1="{root_x}" y1="{root_y}" x2="{n2_x}" y2="{n2_y}" stroke="#1e293b" stroke-width="7" stroke-linecap="round" />

  <line x1="{n1_x}" y1="{n1_y}" x2="{o1_x}" y2="{o1_y}" stroke="#0284c7" stroke-width="6" stroke-linecap="round" />
  <line x1="{n1_x}" y1="{n1_y}" x2="{o2_x}" y2="{o2_y}" stroke="#0284c7" stroke-width="6" stroke-linecap="round" />

  <line x1="{n2_x}" y1="{n2_y}" x2="{o3_x}" y2="{o3_y}" stroke="#0284c7" stroke-width="6" stroke-linecap="round" />
  <line x1="{n2_x}" y1="{n2_y}" x2="{o4_x}" y2="{o4_y}" stroke="#0284c7" stroke-width="6" stroke-linecap="round" />

  <!-- Nodes -->
  <circle cx="{root_x}" cy="{root_y}" r="14" fill="#1e293b" />
  <circle cx="{n1_x}" cy="{n1_y}" r="14" fill="#1e293b" />
  <circle cx="{n2_x}" cy="{n2_y}" r="14" fill="#1e293b" />
  <circle cx="{o1_x}" cy="{o1_y}" r="12" fill="#0284c7" />
  <circle cx="{o2_x}" cy="{o2_y}" r="12" fill="#0284c7" />
  <circle cx="{o3_x}" cy="{o3_y}" r="12" fill="#0284c7" />
  <circle cx="{o4_x}" cy="{o4_y}" r="12" fill="#0284c7" />

  <!-- Stage 1 Labels -->
  <g transform="translate(430, 363) rotate({ang1})">
    <text x="0" y="-28" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">40% EPS &gt; $2</text>
  </g>

  <g transform="translate(430, 609) rotate({-ang1})">
    <text x="0" y="50" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">60% EPS &lt; $2</text>
  </g>

  <!-- Stage 2 Labels -->
  <g transform="translate(975, 167) rotate({ang_o1})">
    <text x="0" y="-22" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">70% upgrade</text>
  </g>

  <g transform="translate(975, 312) rotate({ang_o2})">
    <text x="0" y="40" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">30% no upgrade</text>
  </g>

  <g transform="translate(975, 660) rotate({ang_o1})">
    <text x="0" y="-22" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">20% upgrade</text>
  </g>

  <g transform="translate(975, 804) rotate({ang_o2})">
    <text x="0" y="40" text-anchor="middle" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">80% no upgrade</text>
  </g>

  <!-- Outcomes -->
  <text x="{o1_x + 36}" y="{o1_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">28% <tspan font-weight="500" fill="#334155">upgrade and EPS &gt; $2</tspan></text>
  <text x="{o2_x + 36}" y="{o2_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">12% <tspan font-weight="500" fill="#334155">no upgrade and EPS &gt; $2</tspan></text>
  <text x="{o3_x + 36}" y="{o3_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">12% <tspan font-weight="500" fill="#334155">upgrade and EPS &lt; $2</tspan></text>
  <text x="{o4_x + 36}" y="{o4_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">48% <tspan font-weight="500" fill="#334155">no upgrade and EPS &lt; $2</tspan></text>

</svg>"""

    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/dc31279e9262d8e1f0de.png")
    print(f"Saved dc31279e9262d8e1f0de.png ({pix.width}x{pix.height})")

if __name__ == "__main__":
    render_0f8b()
    render_dc31()
