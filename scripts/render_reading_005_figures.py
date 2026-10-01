import fitz
import numpy as np

def render_745b():
    # Figure 5.1: 1647 x 460
    w, h = 1647, 460
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="20" />
  
  <!-- Header background -->
  <rect x="60" y="45" width="1527" height="75" fill="#0284c7" rx="8" />
  
  <!-- Header Text -->
  <text x="140" y="93" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Asset</text>
  <text x="490" y="93" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">A</text>
  <text x="910" y="93" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">B</text>
  <text x="1330" y="93" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle">C</text>

  <!-- Diagonal Highlights (Variances) -->
  <rect x="300" y="138" width="380" height="72" fill="#e0f2fe" rx="8" />
  <rect x="720" y="228" width="380" height="72" fill="#e0f2fe" rx="8" />
  <rect x="1140" y="318" width="380" height="72" fill="#e0f2fe" rx="8" />

  <!-- Row 1: Asset A -->
  <text x="140" y="185" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">A</text>
  <text x="490" y="184" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Cov(R_A, R_A) = Var(A)</text>
  <text x="910" y="184" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Cov(R_A, R_B)</text>
  <text x="1330" y="184" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Cov(R_A, R_C)</text>
  <line x1="60" y1="215" x2="1587" y2="215" stroke="#cbd5e1" stroke-width="2" />

  <!-- Row 2: Asset B -->
  <text x="140" y="275" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">B</text>
  <text x="490" y="274" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Cov(R_B, R_A)</text>
  <text x="910" y="274" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Cov(R_B, R_B) = Var(B)</text>
  <text x="1330" y="274" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Cov(R_B, R_C)</text>
  <line x1="60" y1="305" x2="1587" y2="305" stroke="#cbd5e1" stroke-width="2" />

  <!-- Row 3: Asset C -->
  <text x="140" y="365" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">C</text>
  <text x="490" y="364" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Cov(R_C, R_A)</text>
  <text x="910" y="364" fill="#1e293b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Cov(R_C, R_B)</text>
  <text x="1330" y="364" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Cov(R_C, R_C) = Var(C)</text>
  <line x1="60" y1="395" x2="1587" y2="395" stroke="#cbd5e1" stroke-width="2" />

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/745bc52701b2b9451cfc.png")
    print(f"Saved 745bc52701b2b9451cfc.png ({pix.width}x{pix.height})")


def render_b779():
    # Figure 5.4: 2385 x 1862 (Roy's safety-first)
    w, h = 2385, 1862
    
    def bell_path(cx, base_y, peak_h, sigma_px):
        # Clip tightly to base_y
        xs = np.linspace(cx - 3.0 * sigma_px, cx + 3.0 * sigma_px, 150)
        ys = np.minimum(base_y, base_y - peak_h * np.exp(-0.5 * ((xs - cx) / sigma_px) ** 2))
        d = f"M {xs[0]:.1f} {base_y:.1f} " + " ".join(f"L {x:.1f} {y:.1f}" for x, y in zip(xs, ys)) + f" L {xs[-1]:.1f} {base_y:.1f}"
        return d, xs[0], xs[-1]

    def shaded_tail_path(cx, base_y, peak_h, sigma_px, cutoff_x):
        start_x = cx - 3.0 * sigma_px
        xs = np.linspace(start_x, cutoff_x, 80)
        ys = np.minimum(base_y, base_y - peak_h * np.exp(-0.5 * ((xs - cx) / sigma_px) ** 2))
        d = f"M {start_x:.1f} {base_y:.1f} " + " ".join(f"L {x:.1f} {y:.1f}" for x, y in zip(xs, ys)) + f" L {cutoff_x:.1f} {base_y:.1f} Z"
        return d

    # Panel A curves
    curve_a_d, a_x0, a_x1 = bell_path(600, 700, 360, 180)
    tail_a_d = shaded_tail_path(600, 700, 360, 180, 380)

    curve_b_d, b_x0, b_x1 = bell_path(1750, 700, 420, 150)
    tail_b_d = shaded_tail_path(1750, 700, 420, 150, 1500)

    # Panel B curves
    curve_std_a_d, _, _ = bell_path(600, 1600, 380, 160)
    tail_std_a_d = shaded_tail_path(600, 1600, 380, 160, 493)

    curve_std_b_d, _, _ = bell_path(1750, 1600, 380, 160)
    tail_std_b_d = shaded_tail_path(1750, 1600, 380, 160, 1617)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- SECTION A -->
  <text x="80" y="90" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold">A. Normally Distributed Returns</text>

  <!-- Curve A -->
  <text x="600" y="160" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">Portfolio A: E(R) = 12%, σ_A = 18%</text>
  <text x="360" y="240" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Probability of returns &lt; 0%</text>
  <text x="360" y="280" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">– i.e., shortfall risk</text>
  
  <!-- Shaded Tail A -->
  <path d="{tail_a_d}" fill="#0284c7" fill-opacity="0.85" />
  <!-- Curve A stroke -->
  <path d="{curve_a_d}" fill="none" stroke="#0284c7" stroke-width="5" />
  <!-- Baseline A -->
  <line x1="40" y1="700" x2="1160" y2="700" stroke="#334155" stroke-width="4" />
  <!-- Vertical mean line -->
  <line x1="600" y1="340" x2="600" y2="700" stroke="#334155" stroke-width="3" />
  <!-- Labels -->
  <line x1="380" y1="700" x2="380" y2="715" stroke="#334155" stroke-width="3" />
  <text x="380" y="755" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">0%</text>
  <line x1="600" y1="700" x2="600" y2="715" stroke="#334155" stroke-width="3" />
  <text x="600" y="755" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">12%</text>
  
  <!-- SFR Formula A -->
  <g transform="translate(600, 850)">
    <text x="-160" y="0" text-anchor="end" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">SFR_A =</text>
    <text x="-50" y="-18" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">12 – 0</text>
    <line x1="-130" y1="-7" x2="30" y2="-7" stroke="#0f172a" stroke-width="3" />
    <text x="-50" y="32" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">18</text>
    <text x="60" y="0" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">= 0.667</text>
  </g>

  <!-- Curve B -->
  <text x="1750" y="160" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">Portfolio B: E(R) = 10%, σ_B = 12%</text>
  
  <!-- Shaded Tail B -->
  <path d="{tail_b_d}" fill="#0284c7" fill-opacity="0.85" />
  <!-- Curve B stroke -->
  <path d="{curve_b_d}" fill="none" stroke="#0284c7" stroke-width="5" />
  <!-- Baseline B -->
  <line x1="1200" y1="700" x2="2320" y2="700" stroke="#334155" stroke-width="4" />
  <!-- Vertical mean line -->
  <line x1="1750" y1="280" x2="1750" y2="700" stroke="#334155" stroke-width="3" />
  <!-- Labels -->
  <line x1="1500" y1="700" x2="1500" y2="715" stroke="#334155" stroke-width="3" />
  <text x="1500" y="755" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">0%</text>
  <line x1="1750" y1="700" x2="1750" y2="715" stroke="#334155" stroke-width="3" />
  <text x="1750" y="755" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">10%</text>
  
  <!-- SFR Formula B -->
  <g transform="translate(1750, 850)">
    <text x="-160" y="0" text-anchor="end" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">SFR_B =</text>
    <text x="-50" y="-18" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">10 – 0</text>
    <line x1="-130" y1="-7" x2="30" y2="-7" stroke="#0f172a" stroke-width="3" />
    <text x="-50" y="32" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">12</text>
    <text x="60" y="0" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">= 0.833</text>
  </g>

  <!-- SECTION B -->
  <line x1="80" y1="960" x2="2305" y2="960" stroke="#e2e8f0" stroke-width="3" />
  <text x="80" y="1030" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold">B. Standard Normal (Z-Distribution)</text>

  <!-- Std Normal Left -->
  <path d="{tail_std_a_d}" fill="#0284c7" fill-opacity="0.85" />
  <path d="{curve_std_a_d}" fill="none" stroke="#0284c7" stroke-width="5" />
  <line x1="40" y1="1600" x2="1160" y2="1600" stroke="#334155" stroke-width="4" />
  <line x1="600" y1="1220" x2="600" y2="1600" stroke="#334155" stroke-width="3" />
  <text x="493" y="1655" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">– 0.67</text>
  <text x="600" y="1655" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">0</text>
  
  <text x="350" y="1420" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">25.14%</text>

  <!-- Std Normal Right -->
  <path d="{tail_std_b_d}" fill="#0284c7" fill-opacity="0.85" />
  <path d="{curve_std_b_d}" fill="none" stroke="#0284c7" stroke-width="5" />
  <line x1="1200" y1="1600" x2="2320" y2="1600" stroke="#334155" stroke-width="4" />
  <line x1="1750" y1="1220" x2="1750" y2="1600" stroke="#334155" stroke-width="3" />
  <text x="1617" y="1655" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">– 0.833</text>
  <text x="1750" y="1655" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">0</text>

  <text x="1450" y="1420" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">20.33%</text>

  <!-- Conclusion Banner -->
  <rect x="580" y="1730" width="1225" height="85" fill="#e0f2fe" rx="12" />
  <text x="1192" y="1785" text-anchor="middle" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Recommendation: Portfolio B is preferred (higher SFR of 0.833, lower shortfall probability of 20.33%)</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/b77962b177f73d87f044.png")
    print(f"Saved b77962b177f73d87f044.png ({pix.width}x{pix.height})")

if __name__ == "__main__":
    render_745b()
    render_b779()
