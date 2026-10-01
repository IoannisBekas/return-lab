import fitz
import numpy as np

def render_1e03():
    # Figure 12.5: Characteristics of Market Structures / Monopolistic Competition (2272 x 1050)
    w, h = 2272, 1050
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  
  <!-- Panel A: Short Run -->
  <rect x="40" y="40" width="1070" height="970" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  <text x="575" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Panel A: Short-Run Economic Profit</text>
  <text x="575" y="150" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Price exceeds ATC at MR = MC (P_SR &gt; ATC_SR)</text>
  
  <!-- Axes A -->
  <line x1="120" y1="880" x2="1030" y2="880" stroke="#0f172a" stroke-width="4" />
  <line x1="120" y1="880" x2="120" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="120" y="170" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Price, Cost ($)</text>
  <text x="1030" y="930" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">Quantity (Q)</text>
  
  <!-- Demand & MR curves -->
  <line x1="150" y1="280" x2="980" y2="760" stroke="#0284c7" stroke-width="5" />
  <text x="990" y="770" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">D_SR</text>
  
  <line x1="150" y1="280" x2="620" y2="860" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <text x="630" y="870" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">MR_SR</text>
  
  <!-- MC curve -->
  <path d="M 220 740 Q 400 820 500 580 T 780 240" fill="none" stroke="#e11d48" stroke-width="5" />
  <text x="790" y="240" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">MC</text>
  
  <!-- ATC curve -->
  <path d="M 250 560 Q 520 620 680 480 T 960 380" fill="none" stroke="#d97706" stroke-width="5" />
  <text x="970" y="380" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">ATC</text>
  
  <!-- Intersection MR = MC at Q_SR = 460 -->
  <!-- At Q=460: MR=MC at y=720 -->
  <!-- At Q=460: ATC is at y=570 -->
  <!-- At Q=460: Demand P is at y=460 -->
  <!-- Profit rectangle: x from 120 to 460, y from 460 to 570 -->
  <rect x="120" y="460" width="340" height="110" fill="#10b981" fill-opacity="0.25" stroke="#10b981" stroke-width="2" />
  <text x="290" y="525" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Economic Profit</text>
  
  <line x1="460" y1="880" x2="460" y2="460" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="120" y1="460" x2="460" y2="460" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="120" y1="570" x2="460" y2="570" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  
  <text x="460" y="920" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_SR</text>
  <text x="105" y="468" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">P_SR</text>
  <text x="105" y="578" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">ATC_SR</text>
  
  
  <!-- Panel B: Long Run -->
  <rect x="1160" y="40" width="1070" height="970" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  <text x="1695" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Panel B: Long-Run Equilibrium</text>
  <text x="1695" y="150" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Entry shifts Demand left until P_LR = ATC (Zero Economic Profit)</text>
  
  <!-- Axes B -->
  <line x1="1240" y1="880" x2="2150" y2="880" stroke="#0f172a" stroke-width="4" />
  <line x1="1240" y1="880" x2="1240" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="1240" y="170" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Price, Cost ($)</text>
  <text x="2150" y="930" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">Quantity (Q)</text>
  
  <!-- Tangent Demand & MR -->
  <line x1="1270" y1="360" x2="2060" y2="820" stroke="#0284c7" stroke-width="5" />
  <text x="2070" y="830" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">D_LR</text>
  
  <line x1="1270" y1="360" x2="1680" y2="860" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <text x="1690" y="870" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">MR_LR</text>
  
  <!-- MC curve -->
  <path d="M 1340 760 Q 1500 820 1570 600 T 1880 250" fill="none" stroke="#e11d48" stroke-width="5" />
  <text x="1890" y="250" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">MC</text>
  
  <!-- ATC curve tangent at (1540, 520) -->
  <path d="M 1340 620 Q 1540 520 1660 510 T 2050 420" fill="none" stroke="#d97706" stroke-width="5" />
  <text x="2060" y="420" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">ATC</text>
  
  <!-- Tangency point -->
  <circle cx="1540" cy="520" r="8" fill="#0284c7" />
  <line x1="1540" y1="880" x2="1540" y2="520" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="1240" y1="520" x2="1540" y2="520" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  
  <text x="1540" y="920" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_LR</text>
  <text x="1225" y="528" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">P_LR = ATC</text>
  
  <rect x="1400" y="950" width="600" height="45" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="8" />
  <text x="1700" y="982" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Long-Run Equilibrium: Normal Profit Only (P = ATC)</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/1e03e995e853f2a4c920.png")
    print(f"Saved 1e03e995e853f2a4c920.png ({pix.width}x{pix.height})")

def render_4015():
    # Figure 12.6: Monopolistic vs Perfect Competition (2150 x 960)
    w, h = 2150, 960
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  
  <!-- Left Panel: Monopolistic Competition -->
  <rect x="40" y="40" width="1010" height="880" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  <text x="545" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Monopolistic Competition (Excess Capacity)</text>
  <text x="545" y="150" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Downward-sloping demand; Output is below minimum efficient scale (Q_mc &lt; Q_eff)</text>
  
  <!-- Axes -->
  <line x1="120" y1="800" x2="980" y2="800" stroke="#0f172a" stroke-width="4" />
  <line x1="120" y1="800" x2="120" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="120" y="170" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Price, Cost</text>
  <text x="980" y="845" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">Quantity</text>
  
  <!-- Demand & ATC -->
  <line x1="160" y1="280" x2="900" y2="720" stroke="#0284c7" stroke-width="4" />
  <text x="910" y="730" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">D</text>
  
  <path d="M 220 620 Q 480 440 680 440 T 950 600" fill="none" stroke="#d97706" stroke-width="5" />
  <text x="960" y="600" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">ATC</text>
  
  <!-- Tangency at Q_mc = 480, y=440 -->
  <circle cx="480" cy="440" r="7" fill="#0284c7" />
  <line x1="480" y1="800" x2="480" y2="440" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <line x1="120" y1="440" x2="480" y2="440" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="480" y="835" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Q_mc</text>
  <text x="105" y="448" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="end">P_mc</text>
  
  <!-- Min ATC at Q_eff = 680, y=440 -->
  <circle cx="680" cy="440" r="7" fill="#d97706" />
  <line x1="680" y1="800" x2="680" y2="440" stroke="#d97706" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="680" y="835" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Q_eff</text>
  
  <!-- Excess Capacity bracket -->
  <line x1="480" y1="740" x2="680" y2="740" stroke="#ef4444" stroke-width="3" />
  <polygon points="480,740 495,733 495,747" fill="#ef4444" />
  <polygon points="680,740 665,733 665,747" fill="#ef4444" />
  <text x="580" y="720" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Excess Capacity</text>
  
  
  <!-- Right Panel: Perfect Competition -->
  <rect x="1100" y="40" width="1010" height="880" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  <text x="1605" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Perfect Competition (Minimum Efficient Scale)</text>
  <text x="1605" y="150" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Horizontal demand P = MR; Operates at the lowest point of the ATC curve</text>
  
  <!-- Axes -->
  <line x1="1180" y1="800" x2="2040" y2="800" stroke="#0f172a" stroke-width="4" />
  <line x1="1180" y1="800" x2="1180" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="1180" y="170" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Price, Cost</text>
  <text x="2040" y="845" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">Quantity</text>
  
  <!-- Horizontal Price / Demand -->
  <line x1="1180" y1="440" x2="2020" y2="440" stroke="#0284c7" stroke-width="5" />
  <text x="2030" y="448" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">P = MR = D</text>
  <text x="1165" y="448" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="end">P_pc</text>
  
  <!-- ATC curve -->
  <path d="M 1280 620 Q 1540 440 1740 440 T 2010 600" fill="none" stroke="#d97706" stroke-width="5" />
  <text x="2020" y="600" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">ATC</text>
  
  <!-- MC curve -->
  <path d="M 1350 720 Q 1500 780 1620 540 T 1880 230" fill="none" stroke="#e11d48" stroke-width="5" />
  <text x="1890" y="230" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">MC</text>
  
  <!-- Min point at Q_pc = 1620, y=440 -->
  <circle cx="1620" cy="440" r="8" fill="#059669" />
  <line x1="1620" y1="800" x2="1620" y2="440" stroke="#059669" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="1620" y="835" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Q_pc (Min ATC)</text>
  
  <rect x="1240" y="870" width="730" height="35" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1.5" rx="6" />
  <text x="1605" y="895" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Productive Efficiency: P = min ATC (No Excess Capacity)</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/4015f5270826986c79d6.png")
    print(f"Saved 4015f5270826986c79d6.png ({pix.width}x{pix.height})")

def render_4e75():
    # Figure 12.2: Total revenue and total cost curves breakeven & max profit (1497 x 1170)
    w, h = 1497, 1170
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1417" height="1090" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="748" y="115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 12.2: Breakeven Analysis (TR / TC Approach)</text>
  <text x="748" y="160" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Breakeven Points (TR = TC) and Profit Maximization (Max Vertical Distance)</text>
  
  <!-- Axes -->
  <line x1="140" y1="920" x2="1380" y2="920" stroke="#0f172a" stroke-width="4" />
  <line x1="140" y1="920" x2="140" y2="220" stroke="#0f172a" stroke-width="4" />
  <text x="140" y="195" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Total Revenue, Cost ($)</text>
  <text x="1380" y="965" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">Output Quantity (Q)</text>
  
  <!-- TR Curve (curving upwards or linear under price-taking) -->
  <line x1="140" y1="920" x2="1280" y2="280" stroke="#0284c7" stroke-width="5" />
  <text x="1290" y="280" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">TR</text>
  
  <!-- TC Curve: starts at fixed cost (140, 750), curves up, then flattens, then accelerates up -->
  <path d="M 140 750 C 350 750 480 650 680 580 C 880 500 1020 480 1250 220" fill="none" stroke="#e11d48" stroke-width="5" />
  <text x="1260" y="215" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">TC</text>
  
  <!-- Breakeven Point 1: intersection around x=420, y=760 -->
  <circle cx="420" cy="760" r="9" fill="#0f172a" />
  <line x1="420" y1="920" x2="420" y2="760" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="420" y="960" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_BE1</text>
  <text x="420" y="730" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Breakeven 1</text>
  
  <!-- Breakeven Point 2: intersection around x=1080, y=390 -->
  <circle cx="1080" cy="390" r="9" fill="#0f172a" />
  <line x1="1080" y1="920" x2="1080" y2="390" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="1080" y="960" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_BE2</text>
  <text x="1080" y="360" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Breakeven 2</text>
  
  <!-- Max Profit Point: around x=760 -->
  <!-- At x=760: TR is at y=570, TC is at y=540... let's adjust TR slope or points -->
  <line x1="750" y1="920" x2="750" y2="360" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  <text x="750" y="960" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_max (Max Profit)</text>
  
  <!-- Double-headed arrow between TR and TC at Q_max -->
  <line x1="750" y1="575" x2="750" y2="540" stroke="#059669" stroke-width="4" />
  <rect x="580" y="440" width="340" height="60" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="8" />
  <text x="750" y="480" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Max Profit (MR = MC)</text>
  
  <!-- Fixed Cost label at origin -->
  <text x="130" y="755" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="end">Total Fixed Cost (TFC)</text>
  
  <!-- Bottom summary banner -->
  <rect x="180" y="1020" width="1137" height="75" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="748" y="1067" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Economic Profit &gt; 0 between Q_BE1 and Q_BE2; Maximized where slopes of TR and TC are parallel (MR = MC).</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/4e752c6e7bf5691839bc.png")
    print(f"Saved 4e752c6e7bf5691839bc.png ({pix.width}x{pix.height})")

def render_519f():
    # Figure 12.7: Kinked demand curve model (1525 x 1085)
    w, h = 1525, 1085
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1445" height="1005" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="762" y="115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 12.7: Kinked Demand Curve Model of Oligopoly</text>
  <text x="762" y="160" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Price Rigidity: Rivals match price cuts (inelastic) but ignore price increases (elastic)</text>
  
  <!-- Axes -->
  <line x1="140" y1="880" x2="1400" y2="880" stroke="#0f172a" stroke-width="4" />
  <line x1="140" y1="880" x2="140" y2="220" stroke="#0f172a" stroke-width="4" />
  <text x="140" y="195" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Price ($)</text>
  <text x="1400" y="925" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">Quantity (Q)</text>
  
  <!-- Kink point at (680, 480) -->
  <!-- Above kink: flat/elastic demand from (200, 320) to (680, 480) -->
  <line x1="200" y1="320" x2="680" y2="480" stroke="#0284c7" stroke-width="6" />
  <text x="380" y="360" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Elastic Demand (Rivals Ignore Price Rise)</text>
  
  <!-- Below kink: steep/inelastic demand from (680, 480) to (1150, 850) -->
  <line x1="680" y1="480" x2="1150" y2="850" stroke="#0284c7" stroke-width="6" />
  <text x="960" y="700" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Inelastic Demand (Rivals Match Cuts)</text>
  <text x="1160" y="860" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">D</text>
  
  <!-- Kink Circle -->
  <circle cx="680" cy="480" r="10" fill="#e11d48" />
  <line x1="680" y1="880" x2="680" y2="480" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="140" y1="480" x2="680" y2="480" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <text x="680" y="925" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Q_K</text>
  <text x="120" y="488" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">P_K</text>
  
  <!-- MR Curve: Upper segment, vertical discontinuous gap, lower segment -->
  <line x1="200" y1="320" x2="680" y2="580" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <!-- Vertical gap at x=680 from y=580 to y=720 -->
  <line x1="680" y1="580" x2="680" y2="720" stroke="#ef4444" stroke-width="4" stroke-dasharray="4 4" />
  <line x1="680" y1="720" x2="880" y2="860" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <text x="890" y="870" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">MR</text>
  <text x="705" y="655" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">Discontinuous Gap in MR</text>
  
  <!-- Marginal Cost curves passing through the gap -->
  <path d="M 450 720 Q 600 680 680 640 T 950 480" fill="none" stroke="#d97706" stroke-width="4" />
  <text x="960" y="480" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">MC₁</text>
  
  <path d="M 450 680 Q 600 640 680 600 T 950 440" fill="none" stroke="#d97706" stroke-width="4" stroke-dasharray="6 4" />
  <text x="960" y="440" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">MC₂</text>
  
  <!-- Bottom explanation -->
  <rect x="180" y="955" width="1165" height="65" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="10" />
  <text x="762" y="997" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">As long as MC passes through the vertical MR gap, price P_K and quantity Q_K remain completely rigid.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/519ffb7b5d0e37f9640d.png")
    print(f"Saved 519ffb7b5d0e37f9640d.png ({pix.width}x{pix.height})")

def render_8f91():
    # Figure 12.10: Dominant firm oligopoly model (2370 x 1547)
    w, h = 2370, 1547
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2270" height="1447" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1185" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 12.10: The Dominant Firm Oligopoly Model</text>
  <text x="1185" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Dominant firm maximizes profit on residual demand (D_DF = D_market – S_CF); Competitive fringe takes P* as given</text>
  
  <!-- Axes -->
  <line x1="180" y1="1250" x2="2180" y2="1250" stroke="#0f172a" stroke-width="5" />
  <line x1="180" y1="1250" x2="180" y2="240" stroke="#0f172a" stroke-width="5" />
  <text x="180" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Price ($)</text>
  <text x="2180" y="1305" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">Quantity (Q)</text>
  
  <!-- Market Demand Curve -->
  <line x1="300" y1="320" x2="2050" y2="1200" stroke="#0f172a" stroke-width="5" />
  <text x="2060" y="1210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Market Demand (D_market)</text>
  
  <!-- Competitive Fringe Supply Curve (starts at y=800, slopes upward) -->
  <line x1="180" y1="950" x2="1500" y2="350" stroke="#64748b" stroke-width="5" />
  <text x="1510" y="340" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Fringe Supply (S_CF = ∑MC_CF)</text>
  
  <!-- Dominant Firm Residual Demand (D_DF) -->
  <line x1="1300" y1="440" x2="2050" y2="1200" stroke="#0284c7" stroke-width="5" />
  <text x="1350" y="420" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Dominant Firm Demand (D_DF)</text>
  
  <!-- Dominant Firm MR -->
  <line x1="1300" y1="440" x2="1680" y2="1220" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <text x="1690" y="1230" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">MR_DF</text>
  
  <!-- Dominant Firm MC (MC_DF) -->
  <path d="M 400 1150 Q 800 1180 1200 950 T 1750 480" fill="none" stroke="#e11d48" stroke-width="5" />
  <text x="1760" y="480" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">MC_DF</text>
  
  <!-- Intersection MR_DF = MC_DF at x=1480, y=800 -->
  <!-- Price P* on D_DF at x=1480: y=620 -->
  <circle cx="1480" cy="800" r="8" fill="#e11d48" />
  <line x1="180" y1="620" x2="1750" y2="620" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <text x="150" y="630" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">P*</text>
  
  <!-- Quantity projections at P*: -->
  <!-- Fringe supply at P*: x=840 -->
  <line x1="840" y1="1250" x2="840" y2="620" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <text x="840" y="1295" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Q_CF</text>
  
  <!-- Dominant Firm supply Q_DF: distance from 0 to Q_DF (projected at 640 or so) -->
  <!-- Total Market Quantity at P*: x=1480 -->
  <line x1="1480" y1="1250" x2="1480" y2="620" stroke="#0284c7" stroke-width="3" stroke-dasharray="6 6" />
  <text x="1480" y="1295" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Q_Total (Q_CF + Q_DF)</text>
  
  <!-- Callout summary -->
  <rect x="250" y="1340" width="1870" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="1185" y="1380" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Equilibrium: Dominant firm sets price P* where MR_DF = MC_DF. The competitive fringe takes P* and supplies Q_CF.</text>
  <text x="1185" y="1415" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">The dominant firm fills the remaining market demand: Q_DF = Q_Total – Q_CF.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/8f9111240bfabae88740.png")
    print(f"Saved 8f9111240bfabae88740.png ({pix.width}x{pix.height})")

def render_9bb5():
    # Figure 12.9: Prisoner's dilemma payoff matrix (1937 x 555)
    w, h = 1937, 555
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="30" y="30" width="1877" height="495" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="968" y="80" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">Figure 12.9: Prisoner's Dilemma Payoff Matrix for Two Oligopolists</text>
  
  <!-- Column Headers (Firm B) -->
  <text x="1250" y="135" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Firm B: Strategy</text>
  <text x="1000" y="180" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">High Price (Collude)</text>
  <text x="1500" y="180" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Low Price (Cheat)</text>
  
  <!-- Row Headers (Firm A) -->
  <text x="350" y="330" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Firm A: Strategy</text>
  <text x="620" y="270" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">High Price (Collude)</text>
  <text x="620" y="410" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">Low Price (Cheat)</text>
  
  <!-- Grid Box 1: (High, High) -->
  <rect x="750" y="200" width="500" height="140" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <text x="1000" y="255" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">A: $100M  |  B: $100M</text>
  <text x="1000" y="300" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Cooperative Outcome (Cartel)</text>
  
  <!-- Grid Box 2: (High, Low) -->
  <rect x="1250" y="200" width="500" height="140" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" />
  <text x="1500" y="255" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">A: $20M  |  B: $150M</text>
  <text x="1500" y="300" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Firm B captures market</text>
  
  <!-- Grid Box 3: (Low, High) -->
  <rect x="750" y="340" width="500" height="140" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" />
  <text x="1000" y="395" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">A: $150M  |  B: $20M</text>
  <text x="1000" y="440" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Firm A captures market</text>
  
  <!-- Grid Box 4: (Low, Low) - NASH EQUILIBRIUM -->
  <rect x="1250" y="340" width="500" height="140" fill="#fef2f2" stroke="#ef4444" stroke-width="4" />
  <text x="1500" y="395" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">A: $50M  |  B: $50M</text>
  <text x="1500" y="440" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">★ Nash Equilibrium ★</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/9bb58cab42a7d9df27ac.png")
    print(f"Saved 9bb58cab42a7d9df27ac.png ({pix.width}x{pix.height})")

def render_abde():
    # Figure 12.3: Long-run average total cost (LRATC) curve displaying economies of scale (2375 x 1275)
    w, h = 2375, 1275
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2275" height="1175" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1187" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 12.3: Economies and Diseconomies of Scale (LRATC)</text>
  <text x="1187" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">The Long-Run Average Total Cost curve envelopes short-run curves across plant capacities</text>
  
  <!-- Axes -->
  <line x1="160" y1="1020" x2="2180" y2="1020" stroke="#0f172a" stroke-width="5" />
  <line x1="160" y1="1020" x2="160" y2="240" stroke="#0f172a" stroke-width="5" />
  <text x="160" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Average Total Cost ($)</text>
  <text x="2180" y="1075" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">Output (Q)</text>
  
  <!-- SRATC curves -->
  <path d="M 220 720 Q 380 500 540 680" fill="none" stroke="#94a3b8" stroke-width="3" />
  <text x="380" y="480" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">SRATC₁</text>
  
  <path d="M 520 620 Q 720 420 920 600" fill="none" stroke="#94a3b8" stroke-width="3" />
  <text x="720" y="400" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">SRATC₂</text>
  
  <path d="M 940 540 Q 1187 360 1440 540" fill="none" stroke="#94a3b8" stroke-width="3" />
  <text x="1187" y="340" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">SRATC₃</text>
  
  <path d="M 1460 580 Q 1680 440 1900 660" fill="none" stroke="#94a3b8" stroke-width="3" />
  <text x="1680" y="420" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">SRATC₄</text>
  
  <!-- Broad U-shaped LRATC curve -->
  <path d="M 200 780 C 500 480 850 380 1187 380 C 1500 380 1850 480 2150 780" fill="none" stroke="#0284c7" stroke-width="7" />
  <text x="2160" y="790" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">LRATC</text>
  
  <!-- Vertical regions dividing lines -->
  <line x1="850" y1="1020" x2="850" y2="380" stroke="#cbd5e1" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="1520" y1="1020" x2="1520" y2="380" stroke="#cbd5e1" stroke-width="3" stroke-dasharray="6 6" />
  
  <!-- Region 1: Economies of Scale -->
  <rect x="250" y="850" width="500" height="90" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="12" />
  <text x="500" y="890" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Economies of Scale</text>
  <text x="500" y="920" fill="#047857" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Falling LRATC as output expands</text>
  
  <!-- Region 2: Constant Returns to Scale -->
  <rect x="910" y="850" width="550" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" rx="12" />
  <text x="1185" y="890" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Constant Returns to Scale</text>
  <text x="1185" y="920" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Flat bottom of LRATC</text>
  
  <!-- Region 3: Diseconomies of Scale -->
  <rect x="1600" y="850" width="500" height="90" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="12" />
  <text x="1850" y="890" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Diseconomies of Scale</text>
  <text x="1850" y="920" fill="#b91c1c" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Rising LRATC due to coordination costs</text>
  
  <!-- Minimum Efficient Scale (MES) Point -->
  <circle cx="850" cy="390" r="9" fill="#059669" />
  <text x="850" y="340" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Minimum Efficient Scale (MES)</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/abde5c4cb1ee91e8bb8f.png")
    print(f"Saved abde5c4cb1ee91e8bb8f.png ({pix.width}x{pix.height})")

def render_b75d():
    # Figure 12.11: Collusion vs. Perfect Competition (2360 x 1552)
    w, h = 2360, 1552
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2260" height="1452" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1180" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 12.11: Collusion vs. Perfect Competition</text>
  <text x="1180" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Cartels maximize joint profits by restricting output to Q_collusion and raising price to P_collusion</text>
  
  <!-- Axes -->
  <line x1="180" y1="1250" x2="2150" y2="1250" stroke="#0f172a" stroke-width="5" />
  <line x1="180" y1="1250" x2="180" y2="240" stroke="#0f172a" stroke-width="5" />
  <text x="180" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Price, Cost ($)</text>
  <text x="2150" y="1305" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">Quantity (Q)</text>
  
  <!-- Demand Line -->
  <line x1="250" y1="320" x2="2000" y2="1200" stroke="#0284c7" stroke-width="6" />
  <text x="2010" y="1210" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Demand (P)</text>
  
  <!-- MR Line -->
  <line x1="250" y1="320" x2="1125" y2="1200" stroke="#0284c7" stroke-width="4" stroke-dasharray="8 6" />
  <text x="1135" y="1210" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">MR</text>
  
  <!-- MC = Supply Line (upward sloping or horizontal) -->
  <line x1="180" y1="1050" x2="1900" y2="550" stroke="#e11d48" stroke-width="5" />
  <text x="1910" y="550" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">MC = ∑MC</text>
  
  <!-- Perfect Competition Outcome: P = MC at intersection of Demand & MC -->
  <!-- Intersection of (250,320)-(2000,1200) and (180,1050)-(1900,550): approx x=1350, y=870 -->
  <circle cx="1350" cy="870" r="10" fill="#059669" />
  <line x1="1350" y1="1250" x2="1350" y2="870" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="180" y1="870" x2="1350" y2="870" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  <text x="1350" y="1295" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Q_competition</text>
  <text x="150" y="878" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">P_competition</text>
  
  <!-- Collusion/Monopoly Outcome: MR = MC at approx x=800, y=870 -->
  <!-- At x=800, Demand price is at y=600 -->
  <circle cx="800" cy="870" r="10" fill="#e11d48" />
  <circle cx="800" cy="600" r="10" fill="#0f172a" />
  <line x1="800" y1="1250" x2="800" y2="600" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="180" y1="600" x2="800" y2="600" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <text x="800" y="1295" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Q_collusion</text>
  <text x="150" y="608" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">P_collusion</text>
  
  <!-- Deadweight Loss Triangle between x=800 and x=1350 -->
  <polygon points="800,600 1350,870 800,870" fill="#ef4444" fill-opacity="0.25" stroke="#ef4444" stroke-width="3" />
  <text x="980" y="780" fill="#b91c1c" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Deadweight Loss (DWL)</text>
  
  <!-- Summary Box -->
  <rect x="250" y="1340" width="1860" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="1180" y="1380" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Collusion results in monopoly price and quantity, creating a deadweight loss of consumer surplus.</text>
  <text x="1180" y="1415" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">Cheating incentive: If one firm secretly expands output, it can earn higher individual profits, often causing cartels to collapse.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b75d144111f7833fae2c.png")
    print(f"Saved b75d144111f7833fae2c.png ({pix.width}x{pix.height})")

def render_b944():
    # Figure 12.1: Shutdown and Breakeven (1675 x 925)
    w, h = 1675, 925
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1595" height="845" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="837" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 12.1: Shutdown and Breakeven Cost Conditions</text>
  <text x="837" y="155" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Marginal Cost (MC), Average Total Cost (ATC), and Average Variable Cost (AVC)</text>
  
  <!-- Axes -->
  <line x1="140" y1="760" x2="1520" y2="760" stroke="#0f172a" stroke-width="4" />
  <line x1="140" y1="760" x2="140" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="140" y="175" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Price, Cost ($)</text>
  <text x="1520" y="805" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">Quantity (Q)</text>
  
  <!-- AVC curve -->
  <path d="M 250 560 Q 650 640 950 560 T 1400 480" fill="none" stroke="#64748b" stroke-width="4" />
  <text x="1410" y="480" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">AVC</text>
  
  <!-- ATC curve -->
  <path d="M 250 420 Q 750 480 1100 420 T 1450 360" fill="none" stroke="#d97706" stroke-width="4" />
  <text x="1460" y="360" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">ATC</text>
  
  <!-- MC curve cuts through min AVC and min ATC -->
  <path d="M 320 680 Q 550 720 750 590 T 1200 220" fill="none" stroke="#e11d48" stroke-width="5" />
  <text x="1210" y="220" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">MC</text>
  
  <!-- Shutdown Point: min AVC at (750, 590) -->
  <circle cx="750" cy="590" r="8" fill="#e11d48" />
  <line x1="140" y1="590" x2="750" y2="590" stroke="#e11d48" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="120" y="598" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="end">P_SD = min AVC</text>
  
  <!-- Breakeven Point: min ATC at (980, 440) -->
  <circle cx="980" cy="440" r="8" fill="#059669" />
  <line x1="140" y1="440" x2="980" y2="440" stroke="#059669" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="120" y="448" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="end">P_BE = min ATC</text>
  
  <!-- Decision Labels -->
  <rect x="250" y="270" width="380" height="50" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" rx="8" />
  <text x="440" y="303" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">P &gt; ATC: Positive Economic Profit</text>
  
  <rect x="250" y="500" width="450" height="50" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.5" rx="8" />
  <text x="475" y="533" fill="#92400e" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">AVC &lt; P &lt; ATC: Operate in Short Run</text>
  
  <rect x="250" y="640" width="380" height="50" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5" rx="8" />
  <text x="440" y="673" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">P &lt; AVC: Shut Down Immediately</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b944e55e4e9c6c186e17.png")
    print(f"Saved b944e55e4e9c6c186e17.png ({pix.width}x{pix.height})")

def render_3f76():
    # Figure 13.2: Leading, Coincident, and Lagging Indicators Table (2064 x 2188)
    w, h = 2064, 2188
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1964" height="2088" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1032" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 13.2: Business Cycle Economic Indicators</text>
  <text x="1032" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Classification of Principal Macroeconomic Series (The Conference Board)</text>
  
  <!-- SECTION 1: LEADING INDICATORS -->
  <rect x="80" y="230" width="1904" height="60" fill="#0284c7" rx="12" />
  <text x="1032" y="272" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">LEADING INDICATORS (Turn Before the Business Cycle)</text>
"""
    leading = [
        ("1. Average weekly hours in manufacturing", "Employers adjust hours before hiring or firing permanent workers."),
        ("2. Initial weekly claims for unemployment insurance", "Sensitive, timely metric of changes in layoffs and labor market slack."),
        ("3. Manufacturers' new orders for consumer goods & materials", "Direct signal of future production activity and inventory replenishment."),
        ("4. Manufacturers' new orders for nondefense capital goods", "Measures corporate willingness to commit capital to long-term expansion."),
        ("5. ISM® New Orders Index (PMI sub-index)", "Purchasing managers' forward-looking assessment of incoming customer orders."),
        ("6. Building permits for new private housing units", "Housing construction represents a major leading driver of economic activity."),
        ("7. S&P 500 Stock Price Index", "Equity markets reflect forward expectations of corporate earnings and discount rates."),
        ("8. Leading Credit Index™ (LCI)", "Synthesizes credit market conditions, yield spreads, and banking liquidity."),
        ("9. Interest rate spread: 10-year Treasury minus Fed Funds", "Yield curve slope; inverted spread historically precedes recessions by 12–18 mo."),
        ("10. Average consumer expectations for business conditions", "Consumer sentiment drives ~70% of U.S. GDP through discretionary consumption.")
    ]
    y_curr = 300
    for i, (title, desc) in enumerate(leading):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="80" y="{y_curr}" width="1904" height="55" fill="{bg}" />
  <text x="110" y="{y_curr + 37}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">{title}</text>
  <text x="850" y="{y_curr + 37}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22">{desc}</text>
  <line x1="80" y1="{y_curr + 55}" x2="1984" y2="{y_curr + 55}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_curr += 55

    # SECTION 2: COINCIDENT INDICATORS
    y_curr += 30
    svg += f"""
  <rect x="80" y="{y_curr}" width="1904" height="60" fill="#059669" rx="12" />
  <text x="1032" y="{y_curr + 42}" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">COINCIDENT INDICATORS (Move Concurrently with Aggregate Economy)</text>
"""
    y_curr += 70
    coincident = [
        ("1. Employees on nonagricultural payrolls", "Comprehensive benchmark measure of current economy-wide employment levels."),
        ("2. Personal income less transfer payments", "Real disposable income generated by current economic production and labor."),
        ("3. Industrial Production Index", "Monthly output measure of manufacturing, mining, and electric/gas utilities."),
        ("4. Manufacturing and trade sales", "Actual real sales volume flowing through wholesale and retail distribution channels.")
    ]
    for i, (title, desc) in enumerate(coincident):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="80" y="{y_curr}" width="1904" height="55" fill="{bg}" />
  <text x="110" y="{y_curr + 37}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">{title}</text>
  <text x="850" y="{y_curr + 37}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22">{desc}</text>
  <line x1="80" y1="{y_curr + 55}" x2="1984" y2="{y_curr + 55}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_curr += 55

    # SECTION 3: LAGGING INDICATORS
    y_curr += 30
    svg += f"""
  <rect x="80" y="{y_curr}" width="1904" height="60" fill="#d97706" rx="12" />
  <text x="1032" y="{y_curr + 42}" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">LAGGING INDICATORS (Change Direction After the Cycle Has Turned)</text>
"""
    y_curr += 70
    lagging = [
        ("1. Average duration of unemployment (weeks)", "Takes time after a recovery begins for long-term unemployed to find work."),
        ("2. Inventories-to-sales ratio (manufacturing & trade)", "Inventories accumulate unintentionally during downturns before being liquidated."),
        ("3. Change in labor cost per unit of output", "Wage adjustments and compensation renegotiations lag productivity shifts."),
        ("4. Average prime rate charged by banks", "Commercial lending rates adjust slowly after central bank policy changes."),
        ("5. Commercial and industrial loans outstanding", "Borrowing often peaks late in expansion to finance involuntary inventory build."),
        ("6. Ratio of consumer installment credit to personal income", "Consumers reduce debt burdens only well after an economic downturn begins."),
        ("7. Change in Consumer Price Index for services", "Services inflation is sticky and continues rising late into the business cycle.")
    ]
    for i, (title, desc) in enumerate(lagging):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="80" y="{y_curr}" width="1904" height="55" fill="{bg}" />
  <text x="110" y="{y_curr + 37}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">{title}</text>
  <text x="850" y="{y_curr + 37}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22">{desc}</text>
  <line x1="80" y1="{y_curr + 55}" x2="1984" y2="{y_curr + 55}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_curr += 55

    svg += """
  <!-- Footer Note -->
  <rect x="80" y="2020" width="1904" height="80" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1032" y="2068" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Analytical Utility: Leading indicators forecast turning points; Coincident indicators identify current status; Lagging indicators confirm cycle phases.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/3f76889fe539950edf3b.png")
    print(f"Saved 3f76889fe539950edf3b.png ({pix.width}x{pix.height})")

def render_c011():
    # Figure 13.1: Stylized business cycle wave diagram (1822 x 1062)
    w, h = 1822, 1062
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1742" height="982" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="911" y="115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Figure 13.1: Four Phases of the Business Cycle</text>
  <text x="911" y="160" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Real GDP fluctuations around long-term potential GDP growth trend</text>
  
  <!-- Axes -->
  <line x1="140" y1="840" x2="1680" y2="840" stroke="#0f172a" stroke-width="4" />
  <line x1="140" y1="840" x2="140" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="140" y="175" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Real GDP</text>
  <text x="1680" y="885" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">Time</text>
  
  <!-- Long-term Trend Line (Potential GDP) -->
  <line x1="140" y1="720" x2="1650" y2="300" stroke="#94a3b8" stroke-width="4" stroke-dasharray="8 6" />
  <text x="1660" y="300" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Long-Term Growth Trend (Potential GDP)</text>
  
  <!-- Wave Curve: Trough 1, Expansion, Peak, Contraction (Recession), Trough 2, Expansion -->
  <path d="M 180 750 C 350 780 450 500 680 320 C 850 180 980 450 1150 720 C 1300 900 1450 620 1620 400" fill="none" stroke="#0284c7" stroke-width="6" />
  
  <!-- Markers & Labels -->
  <!-- Trough 1 at x=280, y=760 -->
  <circle cx="280" cy="760" r="9" fill="#ef4444" />
  <text x="280" y="805" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Trough</text>
  
  <!-- Peak at x=680, y=320 -->
  <circle cx="680" cy="320" r="9" fill="#059669" />
  <text x="680" y="280" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Peak</text>
  
  <!-- Trough 2 at x=1220, y=780 -->
  <circle cx="1220" cy="780" r="9" fill="#ef4444" />
  <text x="1220" y="825" fill="#ef4444" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Trough</text>
  
  <!-- Phase 1: Expansion -->
  <rect x="380" y="520" width="220" height="55" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="8" />
  <text x="490" y="555" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Expansion ↗</text>
  
  <!-- Phase 2: Contraction (Recession) -->
  <rect x="850" y="480" width="240" height="55" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="8" />
  <text x="970" y="515" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Contraction ↘</text>
  
  <!-- Phase 3: Recovery / Expansion -->
  <rect x="1350" y="560" width="220" height="55" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="8" />
  <text x="1460" y="595" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Expansion ↗</text>
  
  <!-- Bottom summary banner -->
  <rect x="140" y="910" width="1542" height="75" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="10" />
  <text x="911" y="955" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Four Phases: Expansion (increasing real GDP) → Peak (top of cycle) → Contraction (declining real GDP) → Trough (bottom).</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/c0118ae379453a3e067b.png")
    print(f"Saved c0118ae379453a3e067b.png ({pix.width}x{pix.height})")

def render_b7b0():
    # Figure 16.1: Four-quadrant matrix diagram illustrating archetypes of globalization (2445 x 1535)
    w, h = 2445, 1535
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2345" height="1435" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1222" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 16.1: Archetypes of Globalization and Cooperation</text>
  <text x="1222" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Framework mapping international cooperation versus national autarky</text>
  
  <!-- Axis Cross centered at (1222, 780) -->
  <line x1="250" y1="780" x2="2194" y2="780" stroke="#0f172a" stroke-width="5" />
  <line x1="1222" y1="1300" x2="1222" y2="260" stroke="#0f172a" stroke-width="5" />
  
  <!-- Axis Labels -->
  <text x="2194" y="830" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">High Globalization / Cooperation →</text>
  <text x="250" y="830" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">← Low Globalization / Cooperation</text>
  
  <text x="1222" y="240" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">↑ High Multilateralism / Shared Sovereignty</text>
  <text x="1222" y="1350" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">↓ National Autarky / Unilateralism</text>
  
  <!-- Quadrant 1 (Top-Right): Multilateralism / Global Integration -->
  <rect x="1280" y="300" width="850" height="420" fill="#f0f9ff" stroke="#0284c7" stroke-width="3" rx="16" />
  <text x="1705" y="360" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Global Integration (Multilateralism)</text>
  <text x="1705" y="420" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Rule-based global trade bodies (WTO, IMF, World Bank)</text>
  <text x="1705" y="465" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Deep cross-border capital flows and global supply chains</text>
  <text x="1705" y="510" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Harmonized international regulatory &amp; ESG standards</text>
  <text x="1705" y="555" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Maximum economic efficiency and specialization</text>
  
  <!-- Quadrant 2 (Top-Left): Regionalism -->
  <rect x="314" y="300" width="850" height="420" fill="#f8fafc" stroke="#64748b" stroke-width="3" rx="16" />
  <text x="739" y="360" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Regional Blocs (Regionalism)</text>
  <text x="739" y="420" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Preferential trade agreements (EU, USMCA, CPTPP)</text>
  <text x="739" y="465" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Nearshoring and friendshoring within geographic spheres</text>
  <text x="739" y="510" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Common external barriers to non-member nations</text>
  <text x="739" y="555" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Semi-integrated regional regulatory alignment</text>
  
  <!-- Quadrant 3 (Bottom-Left): Autarky / Extreme Nationalism -->
  <rect x="314" y="840" width="850" height="420" fill="#fef2f2" stroke="#ef4444" stroke-width="3" rx="16" />
  <text x="739" y="900" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Autarky (National Protectionism)</text>
  <text x="739" y="960" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• High protective tariffs, import quotas, and embargoes</text>
  <text x="739" y="1005" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Severe capital controls and restrictions on FDI</text>
  <text x="739" y="1050" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Domestic self-reliance prioritizing national security</text>
  <text x="739" y="1095" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Suboptimal resource allocation and high domestic costs</text>
  
  <!-- Quadrant 4 (Bottom-Right): Bilateralism / Transactionalism -->
  <rect x="1280" y="840" width="850" height="420" fill="#fffbeb" stroke="#f59e0b" stroke-width="3" rx="16" />
  <text x="1705" y="900" fill="#92400e" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Bilateral Deals (Transactionalism)</text>
  <text x="1705" y="960" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Country-to-country direct trade pacts</text>
  <text x="1705" y="1005" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Strategic resource partnerships (oil, critical minerals)</text>
  <text x="1705" y="1050" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Opportunistic trade without multilateral constraints</text>
  <text x="1705" y="1095" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">• Higher geopolitical friction and shifting alliances</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b7b0a9e49d16445162d8.png")
    print(f"Saved b7b0a9e49d16445162d8.png ({pix.width}x{pix.height})")

def render_eb44():
    # Figure 17.1: Domestic supply and demand graph illustrating the welfare effects of import tariffs (1855 x 1417)
    w, h = 1855, 1417
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1755" height="1317" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="927" y="125" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 17.1: Welfare Effects of Tariffs and Quotas</text>
  <text x="927" y="175" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Consumer Surplus loss = a + b + c + d | Producer gain = a | Tariff revenue = c | Deadweight loss = b + d</text>
  
  <!-- Axes -->
  <line x1="180" y1="1100" x2="1680" y2="1100" stroke="#0f172a" stroke-width="5" />
  <line x1="180" y1="1100" x2="180" y2="240" stroke="#0f172a" stroke-width="5" />
  <text x="180" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Price ($)</text>
  <text x="1680" y="1150" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">Quantity (Q)</text>
  
  <!-- Domestic Supply and Demand Lines -->
  <!-- S_dom: from (240, 1020) to (1550, 320) -->
  <line x1="240" y1="1020" x2="1550" y2="320" stroke="#e11d48" stroke-width="5" />
  <text x="1560" y="320" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">S_domestic</text>
  
  <!-- D_dom: from (240, 320) to (1550, 1020) -->
  <line x1="240" y1="320" x2="1550" y2="1020" stroke="#0284c7" stroke-width="5" />
  <text x="1560" y="1020" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">D_domestic</text>
  
  <!-- World Price P_W = 850 -->
  <line x1="180" y1="850" x2="1600" y2="850" stroke="#64748b" stroke-width="4" stroke-dasharray="6 6" />
  <text x="150" y="858" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">P_World</text>
  
  <!-- Tariff Price P_Tariff = 650 -->
  <line x1="180" y1="650" x2="1600" y2="650" stroke="#0f172a" stroke-width="4" stroke-dasharray="6 6" />
  <text x="150" y="658" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">P_Tariff (P_W + t)</text>
  
  <!-- Coordinates: -->
  <!-- At P_W=850: S_dom is at x=560 (Q_S1), D_dom is at x=1230 (Q_D1) -->
  <!-- At P_Tariff=650: S_dom is at x=930 (Q_S2), D_dom is at x=860... let's calibrate: -->
  <!-- Let Supply line be: x = 180 + (1100 - y)*1.3 -->
  <!-- At y=850 (P_W): x_S1 = 505. At y=650 (P_T): x_S2 = 765 -->
  <!-- Let Demand line be: x = 180 + (y - 240)*1.3 + offset... let's set exact corners: -->
  <!-- Region A (trapezoid): (180,650) to (765,650) to (505,850) to (180,850) -->
  <polygon points="180,650 765,650 505,850 180,850" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
  <text x="400" y="750" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">a</text>
  
  <!-- Region B (DWL production triangle): (505,850) to (765,650) to (765,850) -->
  <polygon points="505,850 765,650 765,850" fill="#fef2f2" stroke="#ef4444" stroke-width="2" />
  <text x="680" y="780" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">b</text>
  
  <!-- Region C (Tariff revenue rect): (765,650) to (1180,650) to (1180,850) to (765,850) -->
  <polygon points="765,650 1180,650 1180,850 765,850" fill="#eff6ff" stroke="#0284c7" stroke-width="2" />
  <text x="972" y="750" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">c</text>
  
  <!-- Region D (DWL consumption triangle): (1180,650) to (1440,850) to (1180,850) -->
  <polygon points="1180,650 1440,850 1180,850" fill="#fef2f2" stroke="#ef4444" stroke-width="2" />
  <text x="1270" y="780" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">d</text>
  
  <!-- Vertical quantity dashed lines -->
  <line x1="505" y1="1100" x2="505" y2="850" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <line x1="765" y1="1100" x2="765" y2="650" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <line x1="1180" y1="1100" x2="1180" y2="650" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <line x1="1440" y1="1100" x2="1440" y2="850" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  
  <text x="505" y="1145" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_S1</text>
  <text x="765" y="1145" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_S2</text>
  <text x="1180" y="1145" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_D2</text>
  <text x="1440" y="1145" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Q_D1</text>
  
  <!-- Legend / Explanation Banner -->
  <rect x="180" y="1200" width="1495" height="130" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="927" y="1245" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Welfare Breakdown: Consumer Surplus falls by –(a + b + c + d).</text>
  <text x="927" y="1285" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Area a = Transferred to domestic producers | Area c = Tariff revenue collected by domestic government</text>
  <text x="927" y="1318" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Deadweight Loss to Society = b (production inefficiency) + d (consumption distortion)</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/eb4467953a10883923f2.png")
    print(f"Saved eb4467953a10883923f2.png ({pix.width}x{pix.height})")


def render_ee24():
    # Figure 12.4: Comparison matrix of market structures (2064 x 970)
    w, h = 2064, 970
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1984" height="890" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1032" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 12.4: Key Characteristics of Four Market Structures</text>
  
  <!-- Table Header -->
  <rect x="70" y="150" width="1924" height="70" fill="#0284c7" rx="12" />
  <text x="220" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Characteristic</text>
  <text x="560" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Perfect Competition</text>
  <text x="960" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Monopolistic Competition</text>
  <text x="1360" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Oligopoly</text>
  <text x="1760" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Monopoly</text>
"""
    rows = [
        ("Number of Sellers", "Many (fragmented)", "Many", "Few dominant firms", "Single seller"),
        ("Barriers to Entry / Exit", "None (free entry/exit)", "Low / Free", "High (scale, capital, patents)", "Very High / Insurmountable"),
        ("Nature of Product", "Homogeneous (identical)", "Differentiated", "Homogeneous or differentiated", "Unique (no close substitutes)"),
        ("Pricing Power", "None (Price Taker, P = MR)", "Some (downward sloping)", "Substantial (interdependent)", "Considerable (Price Searcher)"),
        ("Demand Elasticity Faced", "Perfectly elastic (horizontal)", "Highly elastic", "Elastic above kink, inelastic below", "Market demand curve"),
        ("Non-Price Competition", "None", "Extensive (advertising, brand)", "Extensive (product quality, ads)", "Public relations / Goodwill"),
        ("Long-Run Economic Profit", "Zero (Normal profit only)", "Zero (Normal profit only)", "Positive (economies of scale)", "Positive (protected by barriers)")
    ]
    y_row = 230
    for i, (char, pc, mc, oli, mono) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="70" y="{y_row}" width="1924" height="85" fill="{bg}" />
  <text x="100" y="{y_row + 52}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">{char}</text>
  <text x="560" y="{y_row + 52}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{pc}</text>
  <text x="960" y="{y_row + 52}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{mc}</text>
  <text x="1360" y="{y_row + 52}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{oli}</text>
  <text x="1760" y="{y_row + 52}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{mono}</text>
  <line x1="70" y1="{y_row + 85}" x2="1994" y2="{y_row + 85}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 85

    svg += """
  <!-- Footer Note -->
  <text x="1032" y="885" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Summary: As market structure shifts from perfect competition to monopoly, pricing power and barriers to entry increase.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/ee24809342f1814b5faa.png")
    print(f"Saved ee24809342f1814b5faa.png ({pix.width}x{pix.height})")

def render_fc4b():
    # Figure 12.12: Comparative taxonomy table of market structures (2060 x 974)
    w, h = 2060, 974
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1980" height="894" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1030" y="110" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" text-anchor="middle">Figure 12.12: Long-Run Equilibrium Across Market Structures</text>
  
  <!-- Table Header -->
  <rect x="70" y="150" width="1920" height="70" fill="#0284c7" rx="12" />
  <text x="220" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Economic Dimension</text>
  <text x="560" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Perfect Competition</text>
  <text x="960" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Monopolistic Competition</text>
  <text x="1360" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Oligopoly</text>
  <text x="1760" y="195" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Monopoly</text>
"""
    rows = [
        ("Short-Run Output Rule", "MR = MC (P = MC)", "MR = MC (P &gt; MC)", "MR = MC (P &gt; MC)", "MR = MC (P &gt; MC)"),
        ("Long-Run Output Rule", "P = MR = MC = min ATC", "P = ATC &gt; MC = MR", "P &gt; MC = MR", "P &gt; MC = MR"),
        ("Long-Run Economic Profit", "Zero (P = min ATC)", "Zero (P = ATC, tangency)", "Positive (can be sustained)", "Positive (sustainable)"),
        ("Allocative Efficiency (P = MC)", "Yes (Welfare maximized)", "No (Deadweight loss)", "No (Deadweight loss)", "No (Maximum deadweight loss)"),
        ("Productive Efficiency (min ATC)", "Yes (Min efficient scale)", "No (Excess capacity)", "No (Output restricted)", "No (Output restricted)"),
        ("Strategy / Interaction", "Independent price-taking", "Independent pricing/ads", "Strategic interdependence", "Independent price setting"),
        ("Government Regulation", "Typically minimal", "Truth-in-advertising laws", "Antitrust / Collusion rules", "Public utility / Price caps")
    ]
    y_row = 230
    for i, (char, pc, mc, oli, mono) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="70" y="{y_row}" width="1920" height="85" fill="{bg}" />
  <text x="100" y="{y_row + 52}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold">{char}</text>
  <text x="560" y="{y_row + 52}" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{pc}</text>
  <text x="960" y="{y_row + 52}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{mc}</text>
  <text x="1360" y="{y_row + 52}" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="21" text-anchor="middle">{oli}</text>
  <text x="1760" y="{y_row + 52}" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{mono}</text>
  <line x1="70" y1="{y_row + 85}" x2="1990" y2="{y_row + 85}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 85

    svg += """
  <!-- Footer Note -->
  <text x="1030" y="885" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Efficiency Takeaway: Only perfect competition achieves both allocative efficiency (P = MC) and productive efficiency (P = min ATC).</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/fc4be2a57f8069b508ea.png")
    print(f"Saved fc4be2a57f8069b508ea.png ({pix.width}x{pix.height})")


def render_75fa():
    # Figure 12.8: Marginal Revenue With Kinked Demand Curve (2487 x 1540)
    w, h = 2487, 1540
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2387" height="1440" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1243" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 12.8: Marginal Revenue Discontinuity in Kinked Demand</text>
  <text x="1243" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="30" text-anchor="middle">Derivation of the vertical gap in MR: MR has twice the slope of each demand segment</text>
  
  <!-- Axes -->
  <line x1="200" y1="1250" x2="2250" y2="1250" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="1250" x2="200" y2="240" stroke="#0f172a" stroke-width="5" />
  <text x="200" y="210" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Price, Cost, MR ($)</text>
  <text x="2250" y="1305" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">Quantity (Q)</text>
  
  <!-- Kink Point at (1050, 680) -->
  <!-- Upper Segment: flatter demand D1 from (200, 420) to (1050, 680) -->
  <line x1="200" y1="420" x2="1050" y2="680" stroke="#0284c7" stroke-width="6" />
  <!-- Extension dashed -->
  <line x1="1050" y1="680" x2="1950" y2="955" stroke="#0284c7" stroke-width="3" stroke-dasharray="6 6" opacity="0.4" />
  <text x="450" y="480" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">D₁ (Elastic: Rivals do not match price increase)</text>
  
  <!-- Lower Segment: steeper demand D2 from (1050, 680) to (1650, 1200) -->
  <line x1="1050" y1="680" x2="1650" y2="1200" stroke="#0284c7" stroke-width="6" />
  <!-- Backward extension dashed -->
  <line x1="550" y1="247" x2="1050" y2="680" stroke="#0284c7" stroke-width="3" stroke-dasharray="6 6" opacity="0.4" />
  <text x="1450" y="980" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">D₂ (Inelastic: Rivals match price cut)</text>
  <text x="1660" y="1210" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">D</text>
  
  <!-- Kink Point -->
  <circle cx="1050" cy="680" r="10" fill="#e11d48" />
  <line x1="1050" y1="1250" x2="1050" y2="680" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="200" y1="680" x2="1050" y2="680" stroke="#64748b" stroke-width="3" stroke-dasharray="6 6" />
  <text x="1050" y="1295" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Q_K</text>
  <text x="170" y="688" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">P_K</text>
  
  <!-- MR1 (twice slope of D1): starts at (200, 420), reaches (1050, 840) -->
  <line x1="200" y1="420" x2="1050" y2="840" stroke="#0369a1" stroke-width="5" stroke-dasharray="10 8" />
  <text x="600" y="700" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">MR₁</text>
  
  <!-- MR2 (twice slope of D2): from (1050, 1060) to (1250, 1220) -->
  <line x1="1050" y1="1060" x2="1250" y2="1220" stroke="#0369a1" stroke-width="5" stroke-dasharray="10 8" />
  <text x="1270" y="1230" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">MR₂</text>
  
  <!-- Vertical Discontinuous Gap between MR1 (y=840) and MR2 (y=1060) at x=1050 -->
  <line x1="1050" y1="840" x2="1050" y2="1060" stroke="#ef4444" stroke-width="6" stroke-dasharray="6 6" />
  <circle cx="1050" cy="840" r="7" fill="#ef4444" />
  <circle cx="1050" cy="1060" r="7" fill="#ef4444" />
  
  <rect x="1100" y="900" width="460" height="90" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="10" />
  <text x="1330" y="940" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Discontinuity (Vertical Gap in MR)</text>
  <text x="1330" y="970" fill="#b91c1c" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Length of gap = P_K · (1/ε₂ – 1/ε₁)</text>
  
  <!-- MC shifting within the gap -->
  <path d="M 700 1000 Q 950 970 1050 930 T 1400 700" fill="none" stroke="#d97706" stroke-width="5" />
  <text x="1410" y="700" fill="#d97706" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">MC (Shifts within gap)</text>
  
  <!-- Summary Box -->
  <rect x="250" y="1340" width="1987" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="1243" y="1380" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Key Insight: Marginal cost can fluctuate anywhere within the vertical dashed gap without causing a change in P_K or Q_K.</text>
  <text x="1243" y="1415" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">This mathematical discontinuity provides formal microeconomic justification for observed oligopolistic price stickiness.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/75fa5c08f42a1f1146e8.png")
    print(f"Saved 75fa5c08f42a1f1146e8.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_1e03()
    render_4015()
    render_4e75()
    render_519f()
    render_8f91()
    render_9bb5()
    render_abde()
    render_b75d()
    render_b944()
    render_3f76()
    render_c011()
    render_b7b0()
    render_eb44()
    render_ee24()
    render_fc4b()
    render_75fa()
