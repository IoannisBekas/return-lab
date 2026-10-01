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

# 1. 6b3f5a22c6fac9c014ac.png (2085x1647) - Figure 58.1: Convex Price-Yield Curve for an Option-Free Bond
def get_svg_6b3f():
    # viewBox="0 0 1000 790"
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 790" width="1000" height="790">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="970" height="760" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />

  <!-- Inner Plot Card -->
  <rect x="50" y="45" width="900" height="695" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Title Badge -->
  <rect x="80" y="70" width="680" height="38" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="95" y="95" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0369a1">Figure 58.1: Convex Price-Yield Curve for an Option-Free, 8%, 20-Year Bond</text>

  <!-- Explanatory note top-center -->
  <rect x="250" y="130" width="410" height="60" rx="8" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
  <text x="265" y="154" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">For an option-free bond, price-yield curve is</text>
  <text x="265" y="174" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">convex toward the origin (positive convexity)</text>

  <!-- Axes -->
  <!-- Origin at (160, 640) -->
  <line x1="160" y1="130" x2="160" y2="640" stroke="#334155" stroke-width="2.5" />
  <line x1="160" y1="640" x2="880" y2="640" stroke="#334155" stroke-width="2.5" />

  <!-- Axis Labels -->
  <text x="160" y="115" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">Price (% of Par)</text>
  <text x="895" y="645" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">YTM</text>

  <!-- Ticks & Gridlines -->
  <!-- Coordinates:
       Yields: 7% -> X=340, 8% -> X=510, 9% -> X=680
       Prices: 
       YTM 7%: Price=110.68 -> Y=280, Est_ -> Y=310
       YTM 8%: Price=100.00 -> Y=400 (tangent point)
       YTM 9%: Price=90.80  -> Y=495, Est+ -> Y=490
  -->
  <!-- Vertical dashed lines -->
  <line x1="340" y1="280" x2="340" y2="640" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />
  <line x1="510" y1="400" x2="510" y2="640" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />
  <line x1="680" y1="495" x2="680" y2="640" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />

  <!-- Horizontal dashed lines -->
  <line x1="160" y1="280" x2="340" y2="280" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />
  <line x1="160" y1="320" x2="340" y2="320" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />
  <line x1="160" y1="400" x2="510" y2="400" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />
  <line x1="160" y1="495" x2="680" y2="495" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />
  <line x1="160" y1="520" x2="680" y2="520" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,5" />

  <!-- X-Axis Tick Labels -->
  <text x="340" y="668" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#1e293b" text-anchor="middle">7%</text>
  <text x="510" y="668" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#1e293b" text-anchor="middle">8%</text>
  <text x="680" y="668" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#1e293b" text-anchor="middle">9%</text>

  <!-- Y-Axis Tick Labels -->
  <text x="145" y="285" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#1e293b" text-anchor="end">110.68</text>
  <text x="145" y="325" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#64748b" text-anchor="end">Est.₋</text>
  <text x="145" y="405" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#1e293b" text-anchor="end">100.00</text>
  <text x="145" y="500" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#1e293b" text-anchor="end">90.80</text>
  <text x="145" y="525" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#64748b" text-anchor="end">Est.₊</text>

  <!-- Curves:
       Linear Tangent Line: Passes through (510, 400), (340, 320), (680, 520)
       Actual Curve: Smooth bezier through (240, 200), (340, 280), (510, 400), (680, 495), (820, 550)
  -->
  <!-- Linear Duration Tangent line -->
  <line x1="200" y1="254" x2="800" y2="576" stroke="#475569" stroke-width="3" />

  <!-- Convex Actual Price Curve -->
  <path d="M 230 180 Q 350 310 510 400 T 830 550" fill="none" stroke="#0284c7" stroke-width="4" stroke-linecap="round" />

  <!-- Dots at key points -->
  <!-- On tangent line at 7% -->
  <circle cx="340" cy="320" r="5" fill="#1e293b" />
  <!-- On actual curve at 7% -->
  <circle cx="340" cy="280" r="5" fill="#0284c7" />

  <!-- Tangency point at 8% -->
  <circle cx="510" cy="400" r="6" fill="#0f172a" />

  <!-- On actual curve at 9% -->
  <circle cx="680" cy="495" r="5" fill="#0284c7" />
  <!-- On tangent line at 9% -->
  <circle cx="680" cy="520" r="5" fill="#1e293b" />

  <!-- Note on right -->
  <rect x="650" y="415" width="270" height="50" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1" />
  <text x="665" y="437" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#1e293b">Price falls at a decreasing</text>
  <text x="665" y="453" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#1e293b">rate as yields increase</text>
</svg>"""

# 2. 540393c39595254c6f51.png (2387x1427) - Figure 58.2: Duration-Based Price Estimates vs. Actual Bond Prices
def get_svg_5403():
    # viewBox="0 0 1000 600"
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="1000" height="600">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b" />
    </marker>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="970" height="570" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <!-- Inner Plot Card -->
  <rect x="45" y="40" width="910" height="520" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="75" y="60" width="560" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 58.2: Duration-Based Price Estimates vs. Actual Bond Prices</text>

  <!-- Axes -->
  <line x1="140" y1="100" x2="140" y2="480" stroke="#334155" stroke-width="2.5" />
  <line x1="140" y1="480" x2="880" y2="480" stroke="#334155" stroke-width="2.5" />
  <text x="140" y="85" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">Price</text>
  <text x="895" y="485" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">YTM</text>

  <!-- Ticks: 
       X: 14.50% (X=330), 15.00% (X=480), 15.50% (X=630)
       Y: $88.127 (Y=175), $88.109 (Y=215), $86.591 (Y=305), $85.092 (Y=375), $85.074 (Y=415)
  -->
  <!-- Vertical dashed lines -->
  <line x1="330" y1="175" x2="330" y2="480" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="480" y1="305" x2="480" y2="480" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="630" y1="375" x2="630" y2="480" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Horizontal dashed lines -->
  <line x1="140" y1="175" x2="330" y2="175" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="140" y1="215" x2="330" y2="215" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="140" y1="305" x2="480" y2="305" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="140" y1="375" x2="630" y2="375" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="140" y1="415" x2="630" y2="415" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- X Labels -->
  <text x="330" y="508" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#1e293b" text-anchor="middle">14.50%</text>
  <text x="480" y="508" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#1e293b" text-anchor="middle">15.00%</text>
  <text x="630" y="508" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#1e293b" text-anchor="middle">15.50%</text>

  <!-- Y Labels -->
  <text x="130" y="180" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="end">$88.127</text>
  <text x="130" y="220" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#475569" text-anchor="end">$88.109</text>
  <text x="130" y="310" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="end">$86.591</text>
  <text x="130" y="380" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="end">$85.092</text>
  <text x="130" y="420" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#475569" text-anchor="end">$85.074</text>

  <!-- Tangent Line & Curved Line -->
  <!-- Tangent line passing through (480, 305), (330, 215), (630, 395) slope = 90/150 = 0.6 -->
  <line x1="220" y1="149" x2="700" y2="437" stroke="#475569" stroke-width="2.5" />
  <!-- Actual curve -->
  <path d="M 280 130 Q 380 230 480 305 T 750 420" fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" />

  <!-- Points -->
  <circle cx="330" cy="175" r="5" fill="#0284c7" />
  <circle cx="330" cy="215" r="5" fill="#1e293b" />
  <circle cx="480" cy="305" r="6" fill="#0f172a" />
  <circle cx="630" cy="375" r="5" fill="#0284c7" />
  <circle cx="630" cy="415" r="5" fill="#1e293b" />

  <!-- Error Brackets -->
  <path d="M 345 175 h 12 v 20 h 10 h -10 v 20 h -12" fill="none" stroke="#334155" stroke-width="1.5" />
  <path d="M 645 375 h 12 v 20 h 10 h -10 v 20 h -12" fill="none" stroke="#334155" stroke-width="1.5" />

  <!-- Arrow & Explanations -->
  <line x1="375" y1="195" x2="520" y2="195" stroke="#1e293b" stroke-width="1.5" marker-end="url(#arrow)" />
  <text x="535" y="190" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a">Prices based on duration are</text>
  <text x="535" y="210" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a">underestimates of actual prices</text>

  <!-- Curve Labels -->
  <text x="765" y="425" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">Actual price-yield curve</text>
  <text x="640" y="465" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#475569">Price estimates based on duration of 9.42</text>
</svg>"""

# 3. 7a435d62f34d9005f653.png (2192x1330) - Figure 59.1: Price-Yield Function of Callable vs Option-Free
def get_svg_7a43():
    # viewBox="0 0 1000 600"
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="1000" height="600">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
    </marker>
    <marker id="arrow-slate" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#334155" />
    </marker>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="970" height="570" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <!-- Inner Plot Card -->
  <rect x="45" y="40" width="910" height="520" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="75" y="60" width="620" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="83" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 59.1: Price-Yield Function of Callable vs. Option-Free Bond</text>

  <!-- Axes -->
  <line x1="120" y1="100" x2="120" y2="480" stroke="#334155" stroke-width="2.5" />
  <line x1="120" y1="480" x2="880" y2="480" stroke="#334155" stroke-width="2.5" />
  <text x="120" y="85" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7" text-anchor="middle">Price (% of Par)</text>
  <text x="895" y="485" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0284c7">Yield</text>

  <!-- Call Price 102 line -->
  <line x1="120" y1="280" x2="850" y2="280" stroke="#64748b" stroke-width="1.8" stroke-dasharray="6,5" />
  <text x="105" y="285" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="end">102 (Call Price)</text>

  <!-- Yield threshold y' line -->
  <line x1="480" y1="180" x2="480" y2="480" stroke="#64748b" stroke-width="1.8" stroke-dasharray="6,5" />
  <text x="480" y="510" font-family="Arial, Helvetica, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">y'</text>

  <!-- Regions below axis -->
  <text x="300" y="510" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#dc2626" text-anchor="middle">Negative Convexity</text>
  <text x="680" y="510" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#16a34a" text-anchor="middle">Positive Convexity</text>

  <!-- Option-Free Bond Curve (Solid Blue) -->
  <path d="M 220 140 Q 340 260 480 340 T 850 455" fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" />
  <text x="260" y="165" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">Option-Free Bond</text>
  <line x1="310" y1="172" x2="310" y2="200" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow)" />

  <!-- Callable Bond Curve (Dashed Dark Slate / Flattening at 102) -->
  <path d="M 150 288 C 240 292 360 320 480 350 T 850 460" fill="none" stroke="#0369a1" stroke-width="2.8" stroke-dasharray="6,4" stroke-linecap="round" />
  <text x="200" y="380" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1">Callable Bond</text>
  <line x1="240" y1="365" x2="240" y2="330" stroke="#0369a1" stroke-width="1.5" marker-end="url(#arrow)" />

  <!-- Call option value bracket/double arrow -->
  <line x1="290" y1="210" x2="290" y2="300" stroke="#334155" stroke-width="2" marker-start="url(#arrow-slate)" marker-end="url(#arrow-slate)" />
  <text x="280" y="245" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#334155" text-anchor="end">Call Option</text>
  <text x="280" y="262" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#334155" text-anchor="end">Value</text>
</svg>"""

# 4. d1e38ef8eea046d0f3c7.png (2417x1235) - Figure 59.2: Option-Free and Putable Bonds
def get_svg_d1e3():
    # viewBox="0 0 1000 510"
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 510" width="1000" height="510">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <marker id="arrow-slate" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#334155" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
    </marker>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="970" height="480" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <!-- Inner Plot Card -->
  <rect x="45" y="35" width="910" height="440" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Badge Header -->
  <rect x="75" y="55" width="560" height="32" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="77" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1">Figure 59.2: Comparing Price-Yield Curves for Option-Free and Putable Bonds</text>

  <!-- Axes -->
  <line x1="120" y1="85" x2="120" y2="420" stroke="#334155" stroke-width="2.5" />
  <line x1="120" y1="420" x2="880" y2="420" stroke="#334155" stroke-width="2.5" />
  <text x="120" y="70" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7" text-anchor="middle">Price</text>
  <text x="895" y="425" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7">Yield</text>

  <!-- Option-Free Bond Curve (Solid Blue) -->
  <path d="M 160 105 Q 320 230 480 300 T 820 375" fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" />
  <text x="440" y="380" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="middle">Option-Free Bond</text>
  <line x1="440" y1="362" x2="475" y2="310" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow-blue)" />

  <!-- Putable Bond Curve (Dashed Dark Slate, floor at high yields) -->
  <path d="M 165 95 Q 340 215 520 275 C 620 295 720 305 820 305" fill="none" stroke="#334155" stroke-width="2.8" stroke-dasharray="6,4" stroke-linecap="round" />
  <text x="640" y="260" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#1e293b" text-anchor="middle">Putable Bond</text>
  <line x1="640" y1="268" x2="648" y2="285" stroke="#334155" stroke-width="1.5" marker-end="url(#arrow-slate)" />

  <!-- Double arrow: Value of the Put Option -->
  <line x1="720" y1="315" x2="720" y2="355" stroke="#0f172a" stroke-width="2" marker-start="url(#arrow-slate)" marker-end="url(#arrow-slate)" />
  <text x="735" y="340" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Value of the Put Option</text>
</svg>"""

# 5. 37d4ab5a7d5be7fee01d.png (2068x1504) - Figure 60.1: Credit Rating Agency Classification Scale
def get_svg_37d4():
    # viewBox="0 0 1000 730"
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 730" width="1000" height="730">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="970" height="700" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <!-- Inner Card -->
  <rect x="45" y="40" width="910" height="650" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Header Badge -->
  <rect x="75" y="55" width="460" height="34" rx="8" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="90" y="78" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0369a1">Figure 60.1: Credit Rating Agency Scale Mapping</text>

  <!-- Panel A: Investment Grade Ratings -->
  <g transform="translate(65, 105)">
    <rect x="0" y="0" width="410" height="520" rx="10" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" />
    <rect x="0" y="0" width="410" height="42" rx="10" fill="#dcfce7" />
    <text x="205" y="27" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#166534" text-anchor="middle">(a) Investment Grade Ratings</text>

    <!-- Column Headers -->
    <rect x="10" y="48" width="190" height="30" rx="6" fill="#ffffff" stroke="#bbf7d0" />
    <text x="105" y="68" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#14532d" text-anchor="middle">Moody's</text>

    <rect x="210" y="48" width="190" height="30" rx="6" fill="#ffffff" stroke="#bbf7d0" />
    <text x="305" y="68" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#14532d" text-anchor="middle">S&amp;P, Fitch</text>

    <!-- Rows: Aaa/AAA down to Baa3/BBB- -->
    <!-- Y start at 105, spacing 40 -->
    <g font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">
      <text x="105" y="112" fill="#1e293b">Aaa</text><text x="305" y="112" fill="#0284c7">AAA</text>
      <line x1="20" y1="124" x2="390" y2="124" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="152" fill="#1e293b">Aa1</text><text x="305" y="152" fill="#0284c7">AA+</text>
      <line x1="20" y1="164" x2="390" y2="164" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="192" fill="#1e293b">Aa2</text><text x="305" y="192" fill="#0284c7">AA</text>
      <line x1="20" y1="204" x2="390" y2="204" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="232" fill="#1e293b">Aa3</text><text x="305" y="232" fill="#0284c7">AA−</text>
      <line x1="20" y1="244" x2="390" y2="244" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="272" fill="#1e293b">A1</text><text x="305" y="272" fill="#0284c7">A+</text>
      <line x1="20" y1="284" x2="390" y2="284" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="312" fill="#1e293b">A2</text><text x="305" y="312" fill="#0284c7">A</text>
      <line x1="20" y1="324" x2="390" y2="324" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="352" fill="#1e293b">A3</text><text x="305" y="352" fill="#0284c7">A−</text>
      <line x1="20" y1="364" x2="390" y2="364" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="392" fill="#1e293b">Baa1</text><text x="305" y="392" fill="#0284c7">BBB+</text>
      <line x1="20" y1="404" x2="390" y2="404" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="432" fill="#1e293b">Baa2</text><text x="305" y="432" fill="#0284c7">BBB</text>
      <line x1="20" y1="444" x2="390" y2="444" stroke="#dcfce7" stroke-width="1" />
      <text x="105" y="472" fill="#1e293b">Baa3</text><text x="305" y="472" fill="#0284c7">BBB−</text>
    </g>
  </g>

  <!-- Panel B: Non-Investment Grade Ratings -->
  <g transform="translate(525, 105)">
    <rect x="0" y="0" width="410" height="520" rx="10" fill="#fff7ed" stroke="#fdba74" stroke-width="1.5" />
    <rect x="0" y="0" width="410" height="42" rx="10" fill="#ffedd5" />
    <text x="205" y="27" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#9a3412" text-anchor="middle">(b) Non-Investment Grade (High Yield)</text>

    <!-- Column Headers -->
    <rect x="10" y="48" width="190" height="30" rx="6" fill="#ffffff" stroke="#fed7aa" />
    <text x="105" y="68" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#7c2d12" text-anchor="middle">Moody's</text>

    <rect x="210" y="48" width="190" height="30" rx="6" fill="#ffffff" stroke="#fed7aa" />
    <text x="305" y="68" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="#7c2d12" text-anchor="middle">S&amp;P, Fitch*</text>

    <!-- Rows: Ba1/BB+ down to C/D -->
    <g font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" text-anchor="middle">
      <text x="105" y="108" fill="#1e293b">Ba1</text><text x="305" y="108" fill="#ea580c">BB+</text>
      <line x1="20" y1="117" x2="390" y2="117" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="138" fill="#1e293b">Ba2</text><text x="305" y="138" fill="#ea580c">BB</text>
      <line x1="20" y1="147" x2="390" y2="147" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="168" fill="#1e293b">Ba3</text><text x="305" y="168" fill="#ea580c">BB−</text>
      <line x1="20" y1="177" x2="390" y2="177" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="198" fill="#1e293b">B1</text><text x="305" y="198" fill="#ea580c">B+</text>
      <line x1="20" y1="207" x2="390" y2="207" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="228" fill="#1e293b">B2</text><text x="305" y="228" fill="#ea580c">B</text>
      <line x1="20" y1="237" x2="390" y2="237" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="258" fill="#1e293b">B3</text><text x="305" y="258" fill="#ea580c">B−</text>
      <line x1="20" y1="267" x2="390" y2="267" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="288" fill="#1e293b">Caa1</text><text x="305" y="288" fill="#ea580c">CCC+</text>
      <line x1="20" y1="297" x2="390" y2="297" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="318" fill="#1e293b">Caa2</text><text x="305" y="318" fill="#ea580c">CCC</text>
      <line x1="20" y1="327" x2="390" y2="327" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="348" fill="#1e293b">Caa3</text><text x="305" y="348" fill="#ea580c">CCC−</text>
      <line x1="20" y1="357" x2="390" y2="357" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="378" fill="#1e293b">Ca</text><text x="305" y="378" fill="#ea580c">CC</text>
      <line x1="20" y1="387" x2="390" y2="387" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="408" fill="#1e293b">C</text><text x="305" y="408" fill="#ea580c">C</text>
      <line x1="20" y1="417" x2="390" y2="417" stroke="#ffedd5" stroke-width="1" />
      <text x="105" y="438" fill="#dc2626">C (Default)</text><text x="305" y="438" fill="#dc2626">D (Default)</text>
    </g>
  </g>

  <!-- Footnote -->
  <text x="65" y="658" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#64748b">* Fitch omits the use of +/− symbols for the CCC rating.</text>
</svg>"""

# 6. 456f381c3049da9ce338.png (2068x760) - Figure 62.1: Key credit ratios summary table
def get_svg_456f():
    # viewBox="0 0 1000 370"
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 370" width="1000" height="370">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="970" height="340" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <!-- Inner Table Card -->
  <rect x="40" y="35" width="920" height="300" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)" />

  <!-- Table Header Bar -->
  <rect x="55" y="55" width="890" height="42" rx="8" fill="#0284c7" />
  <text x="80" y="81" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">Ratio Type</text>
  <text x="210" y="81" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">Ratio Name</text>
  <text x="430" y="81" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">Calculation</text>
  <text x="730" y="81" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">Indication of Higher Credit Quality</text>

  <!-- Row 1: Profitability -->
  <rect x="55" y="105" width="890" height="48" rx="6" fill="#f8fafc" />
  <text x="80" y="135" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Profitability</text>
  <text x="210" y="135" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#1e293b">EBIT margin</text>
  <text x="430" y="135" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#0284c7" font-weight="bold">EBIT / revenue</text>
  <text x="730" y="135" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#16a34a">Higher ratio</text>

  <!-- Row 2: Coverage -->
  <rect x="55" y="159" width="890" height="48" rx="6" fill="#ffffff" />
  <text x="80" y="189" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Coverage</text>
  <text x="210" y="189" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#1e293b">EBIT to interest expense</text>
  <text x="430" y="189" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#0284c7" font-weight="bold">EBIT / interest expense</text>
  <text x="730" y="189" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#16a34a">Higher ratio</text>

  <!-- Row 3: Leverage (Debt to EBITDA) -->
  <rect x="55" y="213" width="890" height="48" rx="6" fill="#f8fafc" />
  <text x="80" y="243" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Leverage</text>
  <text x="210" y="243" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#1e293b">Debt to EBITDA</text>
  <text x="430" y="243" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#0284c7" font-weight="bold">Debt / EBITDA</text>
  <text x="730" y="243" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#dc2626">Lower ratio</text>

  <!-- Row 4: Leverage (RCF to net debt) -->
  <rect x="55" y="267" width="890" height="52" rx="6" fill="#ffffff" />
  <text x="80" y="299" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Leverage</text>
  <text x="210" y="299" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#1e293b">RCF to net debt</text>
  <text x="430" y="299" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#0284c7" font-weight="bold">RCF / (debt − cash and marketable securities)</text>
  <text x="730" y="299" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#16a34a">Higher ratio</text>
</svg>"""

# 7. 297803755043c81bcb67.png (1685x1197) - Figure 63.1: Structure of Fred Motor Company Asset Securitization
def get_svg_2978():
    # viewBox="0 0 850 600"
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 600" width="850" height="600">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.06" />
    </filter>
    <marker id="arrow-down" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0284c7" />
    </marker>
    <marker id="arrow-up" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 10 0 L 0 5 L 10 10 z" fill="#16a34a" />
    </marker>
    <marker id="arrow-both" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="820" height="570" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />

  <!-- Box 1: Customers Buy Cars (Y=50) -->
  <rect x="230" y="50" width="390" height="65" rx="10" fill="#ffffff" stroke="#94a3b8" stroke-width="2" filter="url(#shadow)" />
  <text x="425" y="88" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a" text-anchor="middle">Customers Buy Cars</text>

  <!-- Connector 1-2: Double-headed arrow -->
  <line x1="425" y1="120" x2="425" y2="160" stroke="#475569" stroke-width="2" marker-start="url(#arrow-both)" marker-end="url(#arrow-both)" />
  <text x="445" y="145" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7">$1 billion in car loans</text>

  <!-- Box 2: Fred Motor Company (Y=170) -->
  <rect x="230" y="170" width="390" height="75" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#shadow)" />
  <text x="425" y="202" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a" text-anchor="middle">Fred Motor Company</text>
  <text x="425" y="228" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7" text-anchor="middle">(Seller and Servicer)</text>

  <!-- Connectors 2-3 (Y=245 to 305) -->
  <!-- Left: Down arrow (Loans) -->
  <line x1="330" y1="250" x2="330" y2="300" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-down)" />
  <text x="315" y="280" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="end">$1 billion in car loans</text>

  <!-- Right: Up arrow (Cash) -->
  <line x1="520" y1="300" x2="520" y2="250" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-up)" />
  <text x="535" y="280" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#16a34a" text-anchor="start">$1 billion cash</text>

  <!-- Box 3: Auto Owner Trust (SPE) (Y=310) -->
  <rect x="230" y="310" width="390" height="75" rx="10" fill="#ffffff" stroke="#0ea5e9" stroke-width="2" filter="url(#shadow)" />
  <text x="425" y="342" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a" text-anchor="middle">Auto Owner Trust (SPE)</text>
  <text x="425" y="368" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0284c7" text-anchor="middle">(Issuer / Trust)</text>

  <!-- Connectors 3-4 (Y=385 to 445) -->
  <!-- Left: Down arrow (ABS) -->
  <line x1="330" y1="390" x2="330" y2="440" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-down)" />
  <text x="315" y="420" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="end">$1 billion in ABS</text>

  <!-- Right: Up arrow (Cash) -->
  <line x1="520" y1="440" x2="520" y2="390" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-up)" />
  <text x="535" y="420" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#16a34a" text-anchor="start">$1 billion cash</text>

  <!-- Box 4: Investors (Y=450) -->
  <rect x="230" y="450" width="390" height="65" rx="10" fill="#ffffff" stroke="#94a3b8" stroke-width="2" filter="url(#shadow)" />
  <text x="425" y="490" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" fill="#0f172a" text-anchor="middle">Investors</text>

  <!-- Bankruptcy remote pill badge on the side -->
  <rect x="645" y="325" width="165" height="44" rx="8" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" />
  <text x="727" y="344" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="#166534" text-anchor="middle">Bankruptcy-Remote</text>
  <text x="727" y="359" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="#166534" text-anchor="middle">from Originator</text>
</svg>"""

# 8. cc025233ef36a3f56ecd.png (1680x640) - Figure 65.1: Mortgage Pass-Through Cash Flow
def get_svg_cc02():
    # viewBox="0 0 1000 380"
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" width="1000" height="380">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.06" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0284c7" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#16a34a" />
    </marker>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="970" height="350" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />

  <!-- Badge Header -->
  <rect x="45" y="35" width="460" height="30" rx="6" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1" />
  <text x="60" y="55" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0369a1">Figure 65.1: Mortgage Pass-Through Cash Flow Structure</text>

  <!-- Mortgages on Left -->
  <g font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="end">
    <text x="180" y="105">Mortgage 1</text>
    <text x="180" y="145">Mortgage 2</text>
    <text x="180" y="185">· · ·</text>
    <text x="180" y="225">Mortgage N</text>
  </g>

  <!-- Arrows from Mortgages to Pool -->
  <line x1="195" y1="100" x2="385" y2="155" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)" />
  <line x1="195" y1="140" x2="380" y2="165" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)" />
  <line x1="195" y1="180" x2="380" y2="175" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)" />
  <line x1="195" y1="220" x2="385" y2="185" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)" />

  <!-- Central Mortgage Pool Oval -->
  <ellipse cx="480" cy="170" rx="95" ry="50" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" filter="url(#shadow)" />
  <text x="480" y="176" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" fill="#0284c7" text-anchor="middle">Pool</text>

  <!-- Aperture / Pass-Through Filter -->
  <ellipse cx="650" cy="170" rx="16" ry="60" fill="#ffffff" stroke="#334155" stroke-width="2" filter="url(#shadow)" />

  <!-- Line connecting Pool to Aperture -->
  <line x1="575" y1="170" x2="634" y2="170" stroke="#334155" stroke-width="2.5" />

  <!-- Arrows from Aperture to Investors -->
  <line x1="666" y1="140" x2="775" y2="95" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green)" />
  <line x1="666" y1="155" x2="775" y2="135" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green)" />
  <line x1="666" y1="175" x2="775" y2="175" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green)" />
  <line x1="666" y1="195" x2="775" y2="215" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green)" />

  <!-- Investors on Right -->
  <g font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="start">
    <text x="790" y="100">Investor 1</text>
    <text x="790" y="140">Investor 2</text>
    <text x="790" y="180">· · ·</text>
    <text x="790" y="220">Investor N</text>
  </g>

  <!-- Lower Callout Box -->
  <rect x="290" y="275" width="460" height="55" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#shadow)" />
  <text x="520" y="298" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="middle">Pass-through securities backed by</text>
  <text x="520" y="318" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="bold" fill="#0284c7" text-anchor="middle">the pool are issued to investors</text>
  <!-- Connector arrow from box to aperture -->
  <line x1="590" y1="275" x2="640" y2="235" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arrow)" />
</svg>"""

def main():
    items = [
        ("6b3f5a22c6fac9c014ac.png", get_svg_6b3f(), 2085, 1647),
        ("540393c39595254c6f51.png", get_svg_5403(), 2387, 1427),
        ("7a435d62f34d9005f653.png", get_svg_7a43(), 2192, 1330),
        ("d1e38ef8eea046d0f3c7.png", get_svg_d1e3(), 2417, 1235),
        ("37d4ab5a7d5be7fee01d.png", get_svg_37d4(), 2068, 1504),
        ("456f381c3049da9ce338.png", get_svg_456f(), 2068, 760),
        ("297803755043c81bcb67.png", get_svg_2978(), 1685, 1197),
        ("cc025233ef36a3f56ecd.png", get_svg_cc02(), 1680, 640),
    ]

    for fname, svg_str, w, h in items:
        out_path = os.path.join(OUTPUT_DIR, fname)
        render_svg_to_png(svg_str, out_path, w, h)

if __name__ == "__main__":
    main()
