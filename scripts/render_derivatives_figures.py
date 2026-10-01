import fitz
import numpy as np

def render_5cd0():
    # Figure 73.1: Call option moneyness diagram
    # 1385 x 1267
    w, h = 1385, 1267
    
    x0, y0 = 220, 980
    x_max = 1250
    y_min = 160
    x_strike = 620

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- Plot card -->
  <rect x="60" y="50" width="1265" height="1167" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <!-- Axis Labels -->
  <text x="{x0 - 25}" y="{y_min + 20}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Option</text>
  <text x="{x0 - 25}" y="{y_min + 65}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">value</text>

  <text x="{x_max - 20}" y="{y0 + 80}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Underlying</text>
  <text x="{x_max - 20}" y="{y0 + 125}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">value (S)</text>

  <!-- Zero baseline label -->
  <text x="{x0 - 25}" y="{y0 + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">0</text>

  <!-- Strike price vertical dashed line -->
  <line x1="{x_strike}" y1="{y0}" x2="{x_strike}" y2="{y_min + 30}" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />
  <text x="{x_strike}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Exercise</text>
  <text x="{x_strike}" y="{y0 + 105}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">price (X)</text>

  <!-- Call payoff line: flat at 0 until X, then 45 degree slope -->
  <!-- slope to (1200, 400) -->
  <line x1="{x0}" y1="{y0}" x2="{x_strike}" y2="{y0}" stroke="#0284c7" stroke-width="8" stroke-linecap="round" />
  <line x1="{x_strike}" y1="{y0}" x2="1200" y2="400" stroke="#0284c7" stroke-width="8" stroke-linecap="round" />

  <!-- Out of the money area -->
  <rect x="250" y="850" width="320" height="70" fill="#f1f5f9" rx="10" />
  <text x="410" y="897" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Out of the money</text>
  <text x="410" y="935" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">(S &lt; X)</text>

  <!-- In the money area -->
  <rect x="740" y="810" width="400" height="70" fill="#e0f2fe" rx="10" />
  <text x="940" y="857" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">In the money</text>
  <text x="940" y="895" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">(S &gt; X)</text>

  <!-- Double ended arrow under In the money -->
  <line x1="640" y1="940" x2="1200" y2="940" stroke="#0284c7" stroke-width="4" />
  <polygon points="640,940 655,932 655,948" fill="#0284c7" />
  <polygon points="1200,940 1185,932 1185,948" fill="#0284c7" />

  <!-- Point at X: At the money -->
  <circle cx="{x_strike}" cy="{y0}" r="10" fill="#0284c7" stroke="#ffffff" stroke-width="3" />
  <text x="{x_strike}" y="560" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">At the money</text>
  <text x="{x_strike}" y="600" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">(S = X)</text>
  <line x1="{x_strike}" y1="620" x2="{x_strike}" y2="{y0 - 20}" stroke="#0284c7" stroke-width="3" stroke-dasharray="4 4" />

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/5cd0c5a01fc33431d8a2.png")
    print(f"Saved 5cd0c5a01fc33431d8a2.png ({pix.width}x{pix.height})")


def render_4a6b():
    # Figure 73.2: Put option moneyness diagram
    # 1410 x 1265
    w, h = 1410, 1265
    
    x0, y0 = 220, 980
    x_max = 1270
    y_min = 160
    x_strike = 840

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- Plot card -->
  <rect x="60" y="50" width="1290" height="1165" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y_min}" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y0}" x2="{x_max}" y2="{y0}" stroke="#0f172a" stroke-width="4" />

  <!-- Axis Labels -->
  <text x="{x0 - 25}" y="{y_min + 20}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Option</text>
  <text x="{x0 - 25}" y="{y_min + 65}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">value</text>

  <text x="{x_max - 20}" y="{y0 + 80}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">Underlying</text>
  <text x="{x_max - 20}" y="{y0 + 125}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">value (S)</text>

  <!-- Zero baseline label -->
  <text x="{x0 - 25}" y="{y0 + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">0</text>

  <!-- Strike price vertical dashed line -->
  <line x1="{x_strike}" y1="{y0}" x2="{x_strike}" y2="{y_min + 30}" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8" />
  <text x="{x_strike}" y="{y0 + 60}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">Exercise</text>
  <text x="{x_strike}" y="{y0 + 105}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">price (X)</text>

  <!-- Put payoff line: sloping down from (220, 360) to (840, 980), then flat at 0 -->
  <line x1="{x0}" y1="360" x2="{x_strike}" y2="{y0}" stroke="#0284c7" stroke-width="8" stroke-linecap="round" />
  <line x1="{x_strike}" y1="{y0}" x2="{x_max - 40}" y2="{y0}" stroke="#0284c7" stroke-width="8" stroke-linecap="round" />

  <!-- In the money area -->
  <rect x="340" y="810" width="380" height="70" fill="#e0f2fe" rx="10" />
  <text x="530" y="857" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">In the money</text>
  <text x="530" y="895" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">(S &lt; X)</text>

  <!-- Out of the money area -->
  <rect x="910" y="810" width="320" height="70" fill="#f1f5f9" rx="10" />
  <text x="1070" y="857" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="middle">Out of the money</text>
  <text x="1070" y="895" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">(S &gt; X)</text>

  <!-- Arrow pointing right for OTM -->
  <line x1="1170" y1="940" x2="1260" y2="940" stroke="#64748b" stroke-width="4" />
  <polygon points="1260,940 1245,932 1245,948" fill="#64748b" />

  <!-- Point at X: At the money -->
  <circle cx="{x_strike}" cy="{y0}" r="10" fill="#0284c7" stroke="#ffffff" stroke-width="3" />
  <text x="{x_strike}" y="560" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">At the money</text>
  <text x="{x_strike}" y="600" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">(S = X)</text>
  <line x1="{x_strike}" y1="620" x2="{x_strike}" y2="{y0 - 20}" stroke="#0284c7" stroke-width="3" stroke-dasharray="4 4" />

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/4a6b87d49267dda413df.png")
    print(f"Saved 4a6b87d49267dda413df.png ({pix.width}x{pix.height})")


def render_0ddb():
    # Figure 82.1: Digital Asset Taxonomy
    # 2267 x 852
    w, h = 2267, 852
    
    col_w = 1040
    card_y = 60
    card_h = 732

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- LEFT COLUMN: Cryptocurrencies -->
  <rect x="65" y="{card_y}" width="{col_w}" height="{card_h}" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <rect x="65" y="{card_y}" width="{col_w}" height="100" fill="#0284c7" rx="16" />
  <text x="585" y="{card_y + 65}" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Cryptocurrencies</text>

  <!-- Items in Left Column -->
  <!-- Bitcoin -->
  <rect x="110" y="200" width="32" height="32" fill="#0284c7" rx="6" />
  <text x="170" y="228" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Bitcoin</text>

  <!-- Altcoins -->
  <rect x="110" y="280" width="32" height="32" fill="#0284c7" rx="6" />
  <text x="170" y="308" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Altcoins</text>

  <!-- Altcoins subitems -->
  <line x1="200" y1="375" x2="230" y2="375" stroke="#64748b" stroke-width="4" stroke-linecap="round" />
  <text x="250" y="386" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="34">Other cryptocurrencies (e.g., Ether)</text>

  <line x1="200" y1="445" x2="230" y2="445" stroke="#64748b" stroke-width="4" stroke-linecap="round" />
  <text x="250" y="456" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="34">Stablecoins (e.g., Tether)</text>

  <line x1="200" y1="515" x2="230" y2="515" stroke="#64748b" stroke-width="4" stroke-linecap="round" />
  <text x="250" y="526" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="34">Meme coins (e.g., Dogecoin)</text>

  <!-- CBDCs -->
  <rect x="110" y="590" width="32" height="32" fill="#0284c7" rx="6" />
  <text x="170" y="618" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Central bank digital currencies (CBDCs)</text>


  <!-- RIGHT COLUMN: Tokens -->
  <rect x="1162" y="{card_y}" width="{col_w}" height="{card_h}" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <rect x="1162" y="{card_y}" width="{col_w}" height="100" fill="#0f172a" rx="16" />
  <text x="1682" y="{card_y + 65}" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Tokens</text>

  <!-- Items in Right Column -->
  <!-- NFTs -->
  <rect x="1207" y="200" width="32" height="32" fill="#0f172a" rx="6" />
  <text x="1267" y="228" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Nonfungible tokens (NFTs)</text>

  <!-- Security tokens -->
  <rect x="1207" y="280" width="32" height="32" fill="#0f172a" rx="6" />
  <text x="1267" y="308" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Security tokens</text>

  <!-- Subitem -->
  <line x1="1297" y1="375" x2="1327" y2="375" stroke="#64748b" stroke-width="4" stroke-linecap="round" />
  <text x="1347" y="386" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="34">Initial coin offerings (ICOs)</text>

  <!-- Utility tokens -->
  <rect x="1207" y="450" width="32" height="32" fill="#0f172a" rx="6" />
  <text x="1267" y="478" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Utility tokens</text>

  <!-- Governance tokens -->
  <rect x="1207" y="530" width="32" height="32" fill="#0f172a" rx="6" />
  <text x="1267" y="558" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Governance tokens</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/0ddb58387ccd4dc3e182.png")
    print(f"Saved 0ddb58387ccd4dc3e182.png ({pix.width}x{pix.height})")


def render_07e7():
    # Figure 77.1: Private Equity Fund Lifecycle J-Curve
    # 2055 x 1085
    w, h = 2055, 1085
    
    x0 = 260
    x_end = 1800
    y_zero = 520
    
    # Time points: 0, 5, 10 years
    # x(0) = 260, x(5) = 1030, x(10) = 1800
    # IRR scale: 20% -> y=200, 0% -> y=520, -20% -> y=840
    # 10% = 160px
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- Plot Card -->
  <rect x="80" y="50" width="1895" height="985" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />

  <!-- Axes -->
  <line x1="{x0}" y1="120" x2="{x0}" y2="920" stroke="#0f172a" stroke-width="4" />
  <line x1="{x0}" y1="{y_zero}" x2="{x_end}" y2="{y_zero}" stroke="#0f172a" stroke-width="4" />

  <!-- Y-Axis labels (IRR) -->
  <text x="{x0 - 25}" y="100" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" text-anchor="end">IRR</text>
  
  <text x="{x0 - 25}" y="212" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">20%</text>
  <line x1="{x0 - 10}" y1="200" x2="{x0}" y2="200" stroke="#0f172a" stroke-width="3" />

  <text x="{x0 - 25}" y="372" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">10%</text>
  <line x1="{x0 - 10}" y1="360" x2="{x0}" y2="360" stroke="#0f172a" stroke-width="3" />

  <text x="{x0 - 25}" y="532" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="end">0%</text>

  <text x="{x0 - 25}" y="692" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">-10%</text>
  <line x1="{x0 - 10}" y1="680" x2="{x0}" y2="680" stroke="#0f172a" stroke-width="3" />

  <text x="{x0 - 25}" y="852" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">-20%</text>
  <line x1="{x0 - 10}" y1="840" x2="{x0}" y2="840" stroke="#0f172a" stroke-width="3" />

  <!-- X-Axis ticks and labels -->
  <!-- 5 years -->
  <line x1="1030" y1="{y_zero - 15}" x2="1030" y2="{y_zero + 40}" stroke="#0f172a" stroke-width="3" />
  <text x="1030" y="{y_zero + 90}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">5</text>

  <!-- 10 years -->
  <line x1="{x_end}" y1="{y_zero - 40}" x2="{x_end}" y2="{y_zero + 40}" stroke="#0f172a" stroke-width="3" />
  <text x="{x_end}" y="{y_zero + 90}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">10</text>
  
  <text x="{x_end + 30}" y="{y_zero - 20}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Time</text>
  <text x="{x_end + 30}" y="{y_zero + 25}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28">(Years)</text>

  <!-- J-Curve Path: starts (260, 520), bottoms around (650, 840), crosses (1030, 520), reaches (1750, 170) -->
  <!-- We can use cubic beziers: C cp1x cp1y, cp2x cp2y, x y -->
  <path d="M 260 520 C 420 620, 550 840, 700 840 C 850 840, 950 640, 1030 520 C 1130 360, 1300 170, 1750 170" 
        fill="none" stroke="#0284c7" stroke-width="7" stroke-linecap="round" />

  <!-- Shaded Regions -->
  <!-- Negative Phase (Downside / Investment) -->
  <path d="M 260 520 C 420 620, 550 840, 700 840 C 850 840, 950 640, 1030 520 Z" fill="#fee2e2" opacity="0.45" />
  <text x="640" y="650" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Capital Drawdowns &amp; Fees</text>
  <text x="640" y="690" fill="#b91c1c" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">(Early Negative Returns)</text>

  <!-- Positive Phase (Harvest / Realization) -->
  <path d="M 1030 520 C 1130 360, 1300 170, 1750 170 L 1750 520 Z" fill="#dcfce7" opacity="0.45" />
  <text x="1420" y="380" fill="#166534" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Portfolio Realizations &amp; Exits</text>
  <text x="1420" y="420" fill="#15803d" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle">(Substantial Value Creation)</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/07e7ceaae7b1462c4c0f.png")
    print(f"Saved 07e7ceaae7b1462c4c0f.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_5cd0()
    render_4a6b()
    render_0ddb()
    render_07e7()
