import fitz, os, sys
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

# 1. 9d67ea1966abf6100143.png (2112x1557) - Fig 67.1: Long Call & Short Call Payoff / Profit
def get_svg_9d67():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 735" width="1000" height="735">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0f172a" />
    </marker>
  </defs>

  <rect x="15" y="15" width="970" height="705" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="45" y="40" width="910" height="655" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <rect x="75" y="60" width="460" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 67.1: Long Call and Short Call Profit / Loss</text>

  <!-- Axes: Origin at (120, 400) for zero profit. Total Y span: 120 (+$25) to 620 (-$25) -->
  <!-- Zero line -->
  <line x1="120" y1="400" x2="880" y2="400" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />
  <!-- Y Axis -->
  <line x1="120" y1="120" x2="120" y2="640" stroke="#334155" stroke-width="2.5" />
  <!-- X Axis -->
  <line x1="120" y1="640" x2="900" y2="640" stroke="#334155" stroke-width="2.5" />

  <text x="120" y="105" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">Profit / Loss ($)</text>
  <text x="915" y="645" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">Stock Price (ST)</text>

  <!-- Y Ticks: +$5 -> Y=330, 0 -> Y=400, -$5 -> Y=470 -->
  <line x1="110" y1="330" x2="120" y2="330" stroke="#334155" stroke-width="2" />
  <line x1="110" y1="400" x2="120" y2="400" stroke="#334155" stroke-width="2" />
  <line x1="110" y1="470" x2="120" y2="470" stroke="#334155" stroke-width="2" />
  <text x="100" y="335" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#16a34a" text-anchor="end">+$5</text>
  <text x="100" y="405" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#64748b" text-anchor="end">0</text>
  <text x="100" y="475" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#dc2626" text-anchor="end">−$5</text>

  <!-- X Points: X=$50 at X=460, X=$55 (Breakeven) at X=530 -->
  <line x1="460" y1="330" x2="460" y2="640" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="530" y1="330" x2="530" y2="640" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />

  <text x="460" y="668" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="middle">X = $50</text>
  <text x="530" y="668" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7" text-anchor="middle">$55</text>

  <!-- Long Call Line (Dark Slate / Charcoal): 
       From (120, 470) to (460, 470), then slope +1 upwards through (530, 400) to (760, 170)
  -->
  <polyline points="120,470 460,470 760,170" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
  <text x="770" y="165" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#1e293b">Long call</text>

  <!-- Short Call Line (Primary Blue): 
       From (120, 330) to (460, 330), then slope -1 downwards through (530, 400) to (760, 630)
  -->
  <polyline points="120,330 460,330 760,630" fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
  <text x="770" y="640" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">Short call</text>

  <!-- Dots at key transitions -->
  <circle cx="460" cy="470" r="5" fill="#1e293b" />
  <circle cx="460" cy="330" r="5" fill="#0284c7" />
  <circle cx="530" cy="400" r="6" fill="#0f172a" />

  <!-- Breakeven Arrow Callout -->
  <line x1="680" y1="400" x2="545" y2="400" stroke="#0f172a" stroke-width="2" marker-end="url(#arrow)" />
  <text x="695" y="405" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a">Breakeven (X + Premium = $55)</text>
</svg>"""

# 2. a95bfe5b80056592daae.png (1855x1562) - Fig 67.2: Long Put & Short Put Payoff / Profit
def get_svg_a95b():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 840" width="1000" height="840">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0f172a" />
    </marker>
  </defs>

  <rect x="15" y="15" width="970" height="810" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="45" y="40" width="910" height="760" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <rect x="75" y="60" width="460" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 67.2: Long Put and Short Put Profit / Loss</text>

  <!-- Axes: Zero line at Y=440. Y span: 140 (+$45) to 740 (-$45) -->
  <line x1="130" y1="440" x2="880" y2="440" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />
  <line x1="130" y1="120" x2="130" y2="760" stroke="#334155" stroke-width="2.5" />
  <line x1="130" y1="760" x2="900" y2="760" stroke="#334155" stroke-width="2.5" />

  <text x="130" y="105" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">Profit / Loss ($)</text>
  <text x="915" y="765" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">Stock Price (ST)</text>

  <!-- Y Ticks: +$45 -> Y=160, +$5 -> Y=407, 0 -> Y=440, -$5 -> Y=473, -$45 -> Y=720 -->
  <line x1="120" y1="160" x2="130" y2="160" stroke="#334155" stroke-width="2" />
  <line x1="120" y1="407" x2="130" y2="407" stroke="#334155" stroke-width="2" />
  <line x1="120" y1="440" x2="130" y2="440" stroke="#334155" stroke-width="2" />
  <line x1="120" y1="473" x2="130" y2="473" stroke="#334155" stroke-width="2" />
  <line x1="120" y1="720" x2="130" y2="720" stroke="#334155" stroke-width="2" />

  <text x="110" y="165" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#16a34a" text-anchor="end">+$45</text>
  <text x="110" y="412" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#16a34a" text-anchor="end">+$5</text>
  <text x="110" y="445" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#64748b" text-anchor="end">0</text>
  <text x="110" y="478" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#dc2626" text-anchor="end">−$5</text>
  <text x="110" y="725" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#dc2626" text-anchor="end">−$45</text>

  <!-- X Ticks: Breakeven $45 at X=420, Strike $50 at X=480 -->
  <line x1="420" y1="160" x2="420" y2="760" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="480" y1="407" x2="480" y2="760" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />

  <text x="420" y="788" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7" text-anchor="middle">$45</text>
  <text x="480" y="788" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="middle">X = $50</text>

  <!-- Long Put Line (Dark Slate):
       Starts at (130, 160), slopes down through (420, 440) to (480, 473), then flat to (820, 473)
  -->
  <polyline points="130,160 480,473 820,473" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
  <text x="835" y="478" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#1e293b">Long put</text>

  <!-- Short Put Line (Primary Blue):
       Starts at (130, 720), slopes up through (420, 440) to (480, 407), then flat to (820, 407)
  -->
  <polyline points="130,720 480,407 820,407" fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
  <text x="835" y="412" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">Short put</text>

  <!-- Intersection Dot -->
  <circle cx="420" cy="440" r="6" fill="#0f172a" />
  <circle cx="480" cy="473" r="5" fill="#1e293b" />
  <circle cx="480" cy="407" r="5" fill="#0284c7" />

  <!-- Breakeven Arrow Callout -->
  <line x1="580" y1="440" x2="435" y2="440" stroke="#0f172a" stroke-width="2" marker-end="url(#arrow)" />
  <text x="595" y="445" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a">Breakeven (X − Premium = $45)</text>
</svg>"""

# 3. 6c280119591a1c902e62.png (2380x560) - Fig 70.1: Forward Contract Timeline
def get_svg_6c28():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 240" width="1000" height="240">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="10" y="10" width="980" height="220" rx="14" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />

  <!-- Timeline Horizontal Axis at Y=125 -->
  <!-- Ticks at Year 0: X=80, Year 1: X=230, Year 2: X=380, Year 3: X=530, Year 4: X=680 -->
  <line x1="80" y1="125" x2="710" y2="125" stroke="#334155" stroke-width="3" />

  <!-- Ticks -->
  <line x1="80" y1="110" x2="80" y2="140" stroke="#334155" stroke-width="3" />
  <line x1="230" y1="110" x2="230" y2="140" stroke="#334155" stroke-width="3" />
  <line x1="380" y1="110" x2="380" y2="140" stroke="#334155" stroke-width="3" />
  <line x1="530" y1="110" x2="530" y2="140" stroke="#334155" stroke-width="3" />
  <line x1="680" y1="110" x2="680" y2="140" stroke="#334155" stroke-width="3" />

  <!-- Year Labels -->
  <text x="80" y="165" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">Year 0</text>
  <text x="230" y="165" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">1</text>
  <text x="380" y="165" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">2</text>
  <text x="530" y="165" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">3</text>
  <text x="680" y="165" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">4</text>

  <!-- Upper Brace 1: F_{2,2} Spans Year 2 (380) to Year 4 (680) at Y=40 -->
  <path d="M 380 48 Q 380 40 400 40 L 515 40 Q 530 40 530 32 Q 530 40 545 40 L 660 40 Q 680 40 680 48" fill="none" stroke="#0284c7" stroke-width="2.2" />
  <text x="700" y="42" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">F<tspan font-size="11" dy="3">2,2</tspan><tspan font-size="14" dy="-3">: Two-year forward 2-year rate</tspan></text>

  <!-- Upper Brace 2: F_{1,3} Spans Year 1 (230) to Year 4 (680) at Y=85 -->
  <path d="M 230 92 Q 230 84 250 84 L 440 84 Q 455 84 455 76 Q 455 84 470 84 L 660 84 Q 680 84 680 92" fill="none" stroke="#0284c7" stroke-width="2.2" />
  <text x="700" y="87" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">F<tspan font-size="11" dy="3">1,3</tspan><tspan font-size="14" dy="-3">: One-year forward 3-year rate</tspan></text>

  <!-- Lower Brace 1: F_{1,2} Spans Year 1 (230) to Year 3 (530) at Y=180 -->
  <path d="M 230 178 Q 230 186 250 186 L 365 186 Q 380 186 380 194 Q 380 186 395 186 L 510 186 Q 530 186 530 178" fill="none" stroke="#0284c7" stroke-width="2.2" />
  <text x="550" y="193" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">F<tspan font-size="11" dy="3">1,2</tspan><tspan font-size="14" dy="-3">: One-year forward 2-year rate</tspan></text>

  <!-- Lower Brace 2: F_{3,1} Spans Year 3 (530) to Year 4 (680) at Y=210 -->
  <path d="M 530 205 Q 530 213 540 213 L 595 213 Q 605 213 605 221 Q 605 213 615 213 L 670 213 Q 680 213 680 205" fill="none" stroke="#0284c7" stroke-width="2.2" />
  <text x="700" y="219" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">F<tspan font-size="11" dy="3">3,1</tspan><tspan font-size="14" dy="-3">: Three-year forward 1-year rate</tspan></text>
</svg>"""

# 4. 17e494178314731d85e6.png (1431x678) - Fig 70.2: Implied Forward Rate No-Arbitrage
def get_svg_17e4():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 480" width="1000" height="480">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="15" y="15" width="970" height="450" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="40" y="35" width="920" height="410" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="65" y="55" width="560" height="32" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="80" y="77" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1">Figure 70.2: No-Arbitrage Relation Between Spot and Forward Rates</text>

  <!-- Upper Level: Equation (1.02)(1.02)(1 + F_{2,1}) -->
  <text x="500" y="130" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" fill="#0284c7" text-anchor="middle">(1.02)(1.02)(1 + F<tspan font-size="14" dy="4">2,1</tspan><tspan font-size="20" dy="-4">)</tspan></text>

  <!-- Upper Braces: Year 0 (140) to Year 2 (580) and Year 2 (580) to Year 3 (800) -->
  <text x="95" y="172" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" fill="#0284c7">Z<tspan font-size="15" dy="5">2</tspan></text>
  <path d="M 140 178 Q 140 170 160 170 L 345 170 Q 360 170 360 160 Q 360 170 375 170 L 560 170 Q 580 170 580 178" fill="none" stroke="#0284c7" stroke-width="2.5" />

  <path d="M 590 178 Q 590 170 605 170 L 680 170 Q 695 170 695 160 Q 695 170 710 170 L 785 170 Q 800 170 800 178" fill="none" stroke="#1e293b" stroke-width="2.5" />
  <text x="825" y="172" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" fill="#1e293b">F<tspan font-size="15" dy="5">2,1</tspan></text>

  <!-- Lower Level: Equation (1.03)(1.03)(1.03) -->
  <text x="470" y="270" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" fill="#0284c7" text-anchor="middle">(1.03)(1.03)(1.03)</text>

  <!-- Lower Long Brace: Year 0 (140) to Year 3 (800) -->
  <text x="95" y="312" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" fill="#0284c7">Z<tspan font-size="15" dy="5">3</tspan></text>
  <path d="M 140 318 Q 140 310 160 310 L 455 310 Q 470 310 470 300 Q 470 310 485 310 L 780 310 Q 800 310 800 318" fill="none" stroke="#0284c7" stroke-width="2.5" />

  <!-- Timeline Axis at Y=340 -->
  <line x1="140" y1="340" x2="800" y2="340" stroke="#334155" stroke-width="3" />
  <line x1="140" y1="328" x2="140" y2="352" stroke="#334155" stroke-width="3" />
  <line x1="360" y1="328" x2="360" y2="352" stroke="#334155" stroke-width="3" />
  <line x1="580" y1="328" x2="580" y2="352" stroke="#334155" stroke-width="3" />
  <line x1="800" y1="328" x2="800" y2="352" stroke="#334155" stroke-width="3" />

  <text x="140" y="380" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a" text-anchor="middle">Year 0</text>
  <text x="360" y="380" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a" text-anchor="middle">1</text>
  <text x="580" y="380" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a" text-anchor="middle">2</text>
  <text x="800" y="380" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a" text-anchor="middle">3</text>
</svg>"""

# 5. 166332d92fa56b78f1dd.png (2387x1230) - Fig 70.3: FRA Timeline & Settlement
def get_svg_1663():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 520" width="1000" height="520">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow-up" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 10 L 5 0 L 10 10 z" fill="#0284c7" />
    </marker>
    <marker id="arrow-slate-up" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 10 L 5 0 L 10 10 z" fill="#334155" />
    </marker>
  </defs>

  <rect x="15" y="15" width="970" height="490" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="40" y="35" width="920" height="450" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="65" y="50" width="450" height="30" rx="6" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="80" y="70" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0369a1">Figure 70.3: Timeline &amp; Cash Flows for a 3 × 9 FRA</text>

  <!-- Braces above timeline: 3 months (X=100 to 380), 6 months (X=380 to 880) -->
  <text x="240" y="88" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">3 months</text>
  <path d="M 100 108 Q 100 98 120 98 L 225 98 Q 240 98 240 90 Q 240 98 255 98 L 360 98 Q 380 98 380 108" fill="none" stroke="#0284c7" stroke-width="2" />

  <text x="630" y="88" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">6 months</text>
  <path d="M 380 108 Q 380 98 400 98 L 615 98 Q 630 98 630 90 Q 630 98 645 98 L 860 98 Q 880 98 880 108" fill="none" stroke="#0284c7" stroke-width="2" />

  <!-- Timeline Axis at Y=130 -->
  <line x1="100" y1="130" x2="880" y2="130" stroke="#334155" stroke-width="3" />
  <line x1="100" y1="118" x2="100" y2="142" stroke="#334155" stroke-width="3" />
  <line x1="380" y1="118" x2="380" y2="142" stroke="#334155" stroke-width="3" />
  <line x1="880" y1="118" x2="880" y2="142" stroke="#334155" stroke-width="3" />

  <!-- T labels above ticks -->
  <text x="90" y="85" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a">T<tspan font-size="13" dy="4">0</tspan></text>
  <text x="370" y="85" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a">T<tspan font-size="13" dy="4">3</tspan></text>
  <text x="870" y="85" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a">T<tspan font-size="13" dy="4">9</tspan></text>

  <!-- Events at T0 -->
  <line x1="100" y1="185" x2="100" y2="148" stroke="#334155" stroke-width="2" marker-end="url(#arrow-slate-up)" />
  <text x="100" y="205" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Fixed Rate</text>
  <text x="100" y="225" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#475569" text-anchor="middle">(Forward Rate)</text>
  <text x="100" y="245" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="middle">Determined = 1%</text>

  <!-- Events at T3 -->
  <line x1="380" y1="185" x2="380" y2="148" stroke="#334155" stroke-width="2" marker-end="url(#arrow-slate-up)" />
  <text x="380" y="205" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Start of borrowing/lending</text>
  <text x="380" y="228" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0284c7" text-anchor="middle">FRA Expires</text>
  <text x="380" y="248" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#475569" text-anchor="middle">6-month MRR discovered</text>
  <rect x="330" y="265" width="100" height="26" rx="6" fill="#e0f2fe" />
  <text x="380" y="283" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1" text-anchor="middle">Settled</text>

  <!-- Events at T9 -->
  <line x1="880" y1="185" x2="880" y2="148" stroke="#334155" stroke-width="2" marker-end="url(#arrow-slate-up)" />
  <text x="880" y="205" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">End of borrowing/lending</text>
  <text x="880" y="235" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Payoffs computed</text>
  <text x="880" y="270" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="middle">Long = (MRR − 1%) × (180 / 360) × $1M</text>

  <!-- Discounting / Settlement path from T9 back to T3 -->
  <path d="M 880 320 v 80 H 380 v -60" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-dasharray="8,5" marker-end="url(#arrow-up)" />
  <rect x="420" y="375" width="420" height="48" rx="8" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5" />
  <text x="630" y="396" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0369a1" text-anchor="middle">Present value of payoff at MRR is settled</text>
  <text x="630" y="414" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0369a1" text-anchor="middle">in cash at expiration of FRA (T3)</text>
</svg>"""

# 6. 489b2d67b13bcdea028c.png (2497x1457) - Fig 79.1: Real Estate Investment Quadrant
def get_svg_489b():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 580" width="1000" height="580">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="15" y="15" width="970" height="550" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="40" y="35" width="920" height="510" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="65" y="50" width="420" height="30" rx="6" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="80" y="70" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0369a1">Figure 79.1: Real Estate Investment Quadrants</text>

  <!-- Quadrant Matrix Axes -->
  <!-- Top Headers: Debt (X=350) and Equity (X=720) -->
  <rect x="180" y="90" width="340" height="36" rx="8" fill="#e0f2fe" />
  <text x="350" y="114" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0369a1" text-anchor="middle">Debt</text>

  <rect x="550" y="90" width="370" height="36" rx="8" fill="#e0f2fe" />
  <text x="735" y="114" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0369a1" text-anchor="middle">Equity</text>

  <!-- Left Row Headers: Private (Y=210) and Public (Y=380) -->
  <rect x="55" y="140" width="105" height="150" rx="8" fill="#f1f5f9" />
  <text x="107" y="222" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#1e293b" text-anchor="middle">Private</text>

  <rect x="55" y="310" width="105" height="150" rx="8" fill="#f1f5f9" />
  <text x="107" y="392" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#1e293b" text-anchor="middle">Public</text>

  <!-- Quadrant 1: Private Debt (Top Left) -->
  <rect x="180" y="140" width="340" height="150" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
  <g font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#1e293b" text-anchor="middle">
    <text x="350" y="180" font-weight="bold">• Mortgage debt</text>
    <text x="350" y="215" font-weight="bold">• Construction loans</text>
    <text x="350" y="250" font-weight="bold">• Mezzanine debt</text>
  </g>

  <!-- Quadrant 2: Private Equity (Top Right) -->
  <rect x="550" y="140" width="370" height="150" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
  <g font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#1e293b">
    <text x="575" y="165" font-weight="bold" fill="#0284c7">Direct ownership:</text>
    <text x="590" y="188">• Sole ownership, Joint ventures, Limited partnerships</text>
    <text x="575" y="225" font-weight="bold" fill="#0284c7">Indirect ownership:</text>
    <text x="590" y="248">• Real estate private equity funds, Private REITs</text>
  </g>

  <!-- Quadrant 3: Public Debt (Bottom Left) -->
  <rect x="180" y="310" width="340" height="150" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
  <g font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#1e293b" text-anchor="middle">
    <text x="350" y="348" font-weight="bold">• MBS / CMBS / CMOs</text>
    <text x="350" y="378" font-weight="bold">• Covered bonds</text>
    <text x="350" y="408" font-weight="bold">• Mortgage REITs</text>
    <text x="350" y="438" font-weight="bold">• Mortgage ETFs</text>
  </g>

  <!-- Quadrant 4: Public Equity (Bottom Right) -->
  <rect x="550" y="310" width="370" height="150" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
  <g font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#1e293b">
    <text x="575" y="340" font-weight="bold" fill="#0284c7">Publicly traded shares:</text>
    <text x="590" y="365">• Real estate operating companies (REOCs)</text>
    <text x="590" y="390">• Equity REITs (publicly traded)</text>
    <text x="590" y="415">• Real estate mutual funds and ETFs</text>
    <text x="590" y="440">• UCITS real estate funds</text>
  </g>

  <!-- Divider lines -->
  <line x1="535" y1="135" x2="535" y2="465" stroke="#94a3b8" stroke-width="2" />
  <line x1="170" y1="300" x2="930" y2="300" stroke="#94a3b8" stroke-width="2" />

  <!-- Footnote -->
  <text x="65" y="500" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#64748b">CFA Program Curriculum Level I: Real Estate and Infrastructure Categories.</text>
</svg>"""

# 7. 7d4f3ed23815cd023232.png (2220x1332) - Fig 83.3: Capital Allocation Line (CAL)
def get_svg_7d4f():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="1000" height="600">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="15" y="15" width="970" height="570" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="45" y="40" width="910" height="520" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <rect x="75" y="60" width="380" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 83.3: Capital Allocation Line (CAL)</text>

  <!-- Axes: Origin at (140, 480) -->
  <line x1="140" y1="100" x2="140" y2="480" stroke="#334155" stroke-width="2.5" />
  <line x1="140" y1="480" x2="880" y2="480" stroke="#334155" stroke-width="2.5" />

  <text x="140" y="85" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">E(R)</text>
  <text x="895" y="485" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">σ</text>

  <!-- Points on Line:
       CAL starts at Rf at (140, 400).
       Point X at (400, 310) -> (sigma_p, E(R_p))
       Risky portfolio at (740, 190) -> (sigma_risky, E(R_risky))
       Line extends to (840, 155)
  -->
  <!-- Projection lines for Point X -->
  <line x1="140" y1="310" x2="400" y2="310" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="400" y1="310" x2="400" y2="480" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Projection lines for Risky Portfolio -->
  <line x1="140" y1="190" x2="740" y2="190" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="740" y1="190" x2="740" y2="480" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Y Tick Labels -->
  <text x="125" y="405" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">Rf</text>
  <text x="125" y="315" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">E(Rp)</text>
  <text x="125" y="195" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">E(R<tspan font-size="12" dy="3">risky portfolio</tspan><tspan font-size="16" dy="-3">)</tspan></text>

  <!-- X Tick Labels -->
  <text x="400" y="508" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">σp</text>
  <text x="740" y="508" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">σ<tspan font-size="12" dy="3">risky portfolio</tspan></text>

  <!-- CAL Line -->
  <line x1="140" y1="400" x2="840" y2="155" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" />

  <!-- Dots at key points -->
  <circle cx="140" cy="400" r="5" fill="#0284c7" />
  <circle cx="400" cy="310" r="6" fill="#0284c7" />
  <text x="415" y="325" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a">X</text>

  <circle cx="740" cy="190" r="6" fill="#0284c7" />

  <!-- Line Label -->
  <text x="820" y="180" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">Capital</text>
  <text x="820" y="202" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">Allocation</text>
  <text x="820" y="224" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">Line</text>
</svg>"""

# 8. 853ba8e8cc02b4cd6a13.png (2365x1552) - Fig 84.4: Capital Market Line (CML) Lending & Borrowing
def get_svg_853b():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 660" width="1000" height="660">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect x="15" y="15" width="970" height="630" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="45" y="40" width="910" height="580" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <rect x="75" y="60" width="460" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 84.4: Capital Market Line (Lending &amp; Borrowing)</text>

  <!-- Axes: Origin at (140, 540) -->
  <line x1="140" y1="100" x2="140" y2="540" stroke="#334155" stroke-width="2.5" />
  <line x1="140" y1="540" x2="880" y2="540" stroke="#334155" stroke-width="2.5" />

  <text x="140" y="85" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">E(R)</text>
  <text x="895" y="545" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">σ</text>

  <!-- Key points:
       Rf at (140, 440)
       W_M = 25% at (250, 400)
       W_M = 75% at (470, 320)
       Market M at (580, 280)
       W_M = 125% at (690, 240)
       CML ends at (860, 180)
  -->
  <!-- Projection lines -->
  <line x1="140" y1="400" x2="250" y2="400" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="250" y1="400" x2="250" y2="540" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <line x1="140" y1="320" x2="470" y2="320" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="470" y1="320" x2="470" y2="540" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <line x1="140" y1="280" x2="580" y2="280" stroke="#334155" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="580" y1="280" x2="580" y2="540" stroke="#334155" stroke-width="2" />

  <line x1="140" y1="240" x2="690" y2="240" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="690" y1="240" x2="690" y2="540" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Y labels -->
  <text x="125" y="445" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">Rf</text>
  <text x="125" y="285" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">E(RM)</text>

  <!-- X labels -->
  <text x="580" y="568" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">σM</text>

  <!-- CML Line -->
  <line x1="140" y1="440" x2="860" y2="180" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round" />

  <!-- Dots on CML -->
  <circle cx="250" cy="400" r="5" fill="#0f172a" />
  <text x="265" y="420" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7">WM = 25%</text>

  <circle cx="470" cy="320" r="5" fill="#0f172a" />
  <text x="485" y="340" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7">WM = 75%</text>

  <circle cx="580" cy="280" r="7" fill="#0284c7" />
  <text x="595" y="295" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a">M</text>

  <circle cx="690" cy="240" r="5" fill="#0f172a" />
  <text x="705" y="258" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7">WM = 125%</text>

  <!-- Lending Portfolios Brace & Label (along line from Rf to M) -->
  <rect x="200" y="325" width="180" height="32" rx="6" fill="#f0f9ff" stroke="#bae6fd" />
  <text x="290" y="346" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1" text-anchor="middle">Lending Portfolios</text>

  <!-- Borrowing Portfolios Brace & Label (along line above M) -->
  <rect x="620" y="165" width="190" height="32" rx="6" fill="#f0f9ff" stroke="#bae6fd" />
  <text x="715" y="186" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1" text-anchor="middle">Borrowing Portfolios</text>
</svg>"""

# 9. d51ed93c1b0872cc3b93.png (1647x1150) - Fig 84.7: SML vs Covariance
def get_svg_d51e():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700" width="1000" height="700">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0f172a" />
    </marker>
  </defs>

  <rect x="15" y="15" width="970" height="670" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="45" y="40" width="910" height="620" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <rect x="75" y="60" width="460" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 84.7: Security Market Line (Covariance Form)</text>

  <!-- Axes: Origin at (140, 580) -->
  <line x1="140" y1="120" x2="140" y2="580" stroke="#334155" stroke-width="2.5" />
  <line x1="140" y1="580" x2="880" y2="580" stroke="#334155" stroke-width="2.5" />

  <text x="140" y="105" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#0284c7" text-anchor="middle">E(Ri)</text>
  <text x="760" y="618" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">Systematic Risk (Covi,mkt)</text>

  <!-- Rf at Y=490. Market point at (420, 370). Line extends to (800, 160) -->
  <line x1="140" y1="370" x2="420" y2="370" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="420" y1="370" x2="420" y2="580" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Y Tick Labels -->
  <text x="125" y="495" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#0f172a" text-anchor="end">Rf</text>
  <text x="125" y="375" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#0f172a" text-anchor="end">E(Rmkt)</text>

  <!-- X Tick Labels -->
  <text x="420" y="618" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">Covmkt,mkt = σ²mkt</text>

  <!-- SML Line -->
  <line x1="140" y1="490" x2="820" y2="150" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" />

  <!-- Market Portfolio Point -->
  <circle cx="420" cy="370" r="7" fill="#0284c7" />

  <!-- Arrow pointing to Market Portfolio -->
  <line x1="620" y1="370" x2="445" y2="370" stroke="#0f172a" stroke-width="2" marker-end="url(#arrow)" />
  <text x="635" y="375" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a">Market Portfolio</text>

  <!-- SML Label Top Right -->
  <text x="680" y="145" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">Security Market Line</text>
  <text x="680" y="170" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">(SML)</text>
</svg>"""

# 10. 73de09a9a85d8de3ae53.png (1600x1145) - Fig 84.8: SML vs Beta
def get_svg_73de():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 715" width="1000" height="715">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0f172a" />
    </marker>
  </defs>

  <rect x="15" y="15" width="970" height="685" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="45" y="40" width="910" height="635" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <rect x="75" y="60" width="460" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 84.8: Security Market Line (Beta Form)</text>

  <!-- Axes: Origin at (140, 580) -->
  <line x1="140" y1="120" x2="140" y2="580" stroke="#334155" stroke-width="2.5" />
  <line x1="140" y1="580" x2="880" y2="580" stroke="#334155" stroke-width="2.5" />

  <text x="140" y="105" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#0284c7" text-anchor="middle">E(Ri)</text>
  <text x="760" y="618" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">Systematic Risk (βi)</text>

  <!-- Rf at Y=490. Market point at (420, 370). Line extends to (820, 150) -->
  <line x1="140" y1="370" x2="420" y2="370" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="420" y1="370" x2="420" y2="580" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Y Tick Labels -->
  <text x="125" y="495" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#0f172a" text-anchor="end">Rf</text>
  <text x="125" y="375" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#0f172a" text-anchor="end">E(Rmkt)</text>

  <!-- X Tick Labels -->
  <text x="420" y="618" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">βmkt = 1.0</text>

  <!-- SML Line -->
  <line x1="140" y1="490" x2="820" y2="150" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" />

  <!-- Market Portfolio Point -->
  <circle cx="420" cy="370" r="7" fill="#0284c7" />

  <!-- Arrow pointing to Market Portfolio -->
  <line x1="620" y1="370" x2="445" y2="370" stroke="#0f172a" stroke-width="2" marker-end="url(#arrow)" />
  <text x="635" y="375" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a">Market Portfolio</text>

  <!-- SML Label Top Right -->
  <text x="680" y="145" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">Security Market Line</text>
  <text x="680" y="170" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">(SML)</text>
</svg>"""

# 11. e5d02d0e339378b8eb6b.png (1937x972) - Fig 84.11: Modigliani-Modigliani (M-squared) Measure
def get_svg_e5d0():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" width="1000" height="500">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0f172a" />
    </marker>
  </defs>

  <rect x="15" y="15" width="970" height="470" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="40" y="35" width="920" height="430" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="65" y="50" width="460" height="30" rx="6" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="80" y="70" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#0369a1">Figure 84.11: Modigliani–Modigliani (M²) Measure</text>

  <!-- Axes: Origin at (340, 420) -->
  <line x1="340" y1="90" x2="340" y2="420" stroke="#334155" stroke-width="2.5" />
  <line x1="340" y1="420" x2="920" y2="420" stroke="#334155" stroke-width="2.5" />

  <text x="340" y="75" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">E(R)</text>
  <text x="935" y="425" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">σ</text>

  <!-- Efficient Frontier Hyperbola (Black) -->
  <path d="M 680 370 C 510 360 480 290 560 230 C 650 170 780 150 890 140" fill="none" stroke="#334155" stroke-width="2.2" />

  <!-- Key points:
       Rf at (340, 360)
       sigma_P at X=420, sigma_M at X=570
       Market M at (570, 230)
       Portfolio P at (420, 290)
       Levered P* at (570, 120)
  -->
  <!-- Projection lines -->
  <line x1="340" y1="120" x2="570" y2="120" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="340" y1="230" x2="570" y2="230" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="340" y1="290" x2="420" y2="290" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <line x1="420" y1="290" x2="420" y2="420" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="570" y1="120" x2="570" y2="420" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Y labels on left -->
  <text x="325" y="365" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="end">Rf</text>
  <text x="325" y="295" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="end">RP</text>
  <text x="325" y="235" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="end">RM</text>
  <!-- M^2 formula label at Y=120 -->
  <text x="325" y="125" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="end">M² = (σM / σP)(RP − Rf) + Rf</text>

  <!-- X labels -->
  <text x="420" y="445" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="middle">σP</text>
  <text x="570" y="445" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="middle">σM</text>

  <!-- CML Line (tangent at M) from (340, 360) through (570, 230) to (820, 90) -->
  <line x1="340" y1="360" x2="820" y2="90" stroke="#0ea5e9" stroke-width="2.5" />

  <!-- CAL of Portfolio P from (340, 360) through (420, 290) and (570, 120) to (610, 75) -->
  <line x1="340" y1="360" x2="610" y2="75" stroke="#0284c7" stroke-width="3" stroke-linecap="round" />

  <!-- Points -->
  <circle cx="420" cy="290" r="5" fill="#0284c7" />
  <text x="435" y="295" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7">P</text>

  <circle cx="570" cy="230" r="6" fill="#0f172a" />
  <text x="585" y="245" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a">M</text>

  <circle cx="570" cy="120" r="6" fill="#0284c7" />
  <text x="585" y="125" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">P*</text>

  <!-- M^2 Alpha bracket / arrow between M and P* -->
  <line x1="630" y1="175" x2="578" y2="175" stroke="#0f172a" stroke-width="2" marker-end="url(#arrow)" />
  <text x="645" y="180" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a">M² Alpha</text>
</svg>"""

# 12. a6f9f340aa67b6b629a0.png (1930x1150) - Fig 84.12: Treynor Ratio and Jensen's Alpha
def get_svg_a6f9():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="1000" height="600">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0f172a" />
    </marker>
  </defs>

  <rect x="15" y="15" width="970" height="570" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <rect x="45" y="40" width="910" height="520" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <rect x="75" y="60" width="460" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 84.12: Treynor Measure &amp; Jensen's Alpha</text>

  <!-- Axes: Origin at (140, 500) -->
  <line x1="140" y1="100" x2="140" y2="500" stroke="#334155" stroke-width="2.5" />
  <line x1="140" y1="500" x2="880" y2="500" stroke="#334155" stroke-width="2.5" />

  <text x="140" y="85" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">E(R)</text>
  <text x="895" y="505" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">β</text>

  <!-- Rf at (140, 440)
       Beta_P at X=280, Beta_M = 1.0 at X=420
       Point M at (420, 320)
       SML line from (140, 440) through (420, 320) to (760, 175)
       SML expected return at Beta_P is at (280, 380)
       Portfolio P return is at (280, 260)
       Portfolio ray from (140, 440) through (280, 260) to (500, 75)
  -->
  <!-- Projection lines -->
  <line x1="140" y1="260" x2="280" y2="260" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="140" y1="320" x2="420" y2="320" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="280" y1="260" x2="280" y2="500" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="420" y1="320" x2="420" y2="500" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Y labels -->
  <text x="125" y="445" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">Rf</text>
  <text x="125" y="325" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">RM</text>
  <text x="125" y="265" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">RP</text>

  <!-- X labels -->
  <text x="280" y="528" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">βP</text>
  <text x="420" y="528" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">1.0</text>

  <!-- SML Line -->
  <line x1="140" y1="440" x2="760" y2="175" stroke="#0ea5e9" stroke-width="3" />
  <text x="775" y="175" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0ea5e9">SML</text>

  <!-- Portfolio Ray (Treynor Slope) -->
  <line x1="140" y1="440" x2="520" y2="70" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" />
  <text x="535" y="65" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">slope = Treynor measure for Portfolio P</text>

  <!-- Points -->
  <circle cx="420" cy="320" r="6" fill="#0f172a" />
  <text x="420" y="300" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">M</text>

  <circle cx="280" cy="260" r="6" fill="#0284c7" />
  <text x="270" y="245" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">P</text>

  <circle cx="280" cy="380" r="5" fill="#0ea5e9" />

  <!-- Jensen's Alpha Bracket at Beta_P between Y=260 and Y=380 -->
  <path d="M 295 260 h 12 v 60 h 10 h -10 v 60 h -12" fill="none" stroke="#334155" stroke-width="2" />
  <line x1="550" y1="410" x2="330" y2="330" stroke="#0f172a" stroke-width="2" marker-end="url(#arrow)" />
  <text x="565" y="420" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0284c7">Jensen's alpha (αP)</text>
</svg>"""

def main():
    items = [
        ("9d67ea1966abf6100143.png", get_svg_9d67(), 2112, 1557),
        ("a95bfe5b80056592daae.png", get_svg_a95b(), 1855, 1562),
        ("6c280119591a1c902e62.png", get_svg_6c28(), 2380, 560),
        ("17e494178314731d85e6.png", get_svg_17e4(), 1431, 678),
        ("166332d92fa56b78f1dd.png", get_svg_1663(), 2387, 1230),
        ("489b2d67b13bcdea028c.png", get_svg_489b(), 2497, 1457),
        ("7d4f3ed23815cd023232.png", get_svg_7d4f(), 2220, 1332),
        ("853ba8e8cc02b4cd6a13.png", get_svg_853b(), 2365, 1552),
        ("d51ed93c1b0872cc3b93.png", get_svg_d51e(), 1647, 1150),
        ("73de09a9a85d8de3ae53.png", get_svg_73de(), 1600, 1145),
        ("e5d02d0e339378b8eb6b.png", get_svg_e5d0(), 1937, 972),
        ("a6f9f340aa67b6b629a0.png", get_svg_a6f9(), 1930, 1150),
    ]

    for fname, svg_str, w, h in items:
        out_path = os.path.join(OUTPUT_DIR, fname)
        render_svg_to_png(svg_str, out_path, w, h)

if __name__ == "__main__":
    main()
