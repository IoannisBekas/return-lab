import fitz
import numpy as np
import math

def render_0abb():
    # Figure 3.2: 1280 x 2192 (Skewness comparison)
    w, h = 1280, 2192

    def phi(x):
        return (1.0 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)

    def Phi(x):
        # standard normal cdf using error function
        import math
        return 0.5 * (1.0 + special_erf(x / np.sqrt(2.0)))

    def special_erf(x):
        # erf approximation or math.erf
        import math
        if isinstance(x, np.ndarray):
            return np.vectorize(math.erf)(x)
        return math.erf(x)

    def skew_normal(cx, base_y, peak_h, sigma, alpha):
        z = np.linspace(-3.5, 3.5, 200)
        # pdf: 2 * phi(z) * Phi(alpha * z)
        pdf = 2.0 * phi(z) * 0.5 * (1.0 + special_erf((alpha * z) / np.sqrt(2.0)))
        pdf_max = np.max(pdf)
        ys = base_y - peak_h * (pdf / pdf_max)
        xs = cx + z * sigma
        
        # Calculate mode, median, mean
        # mode:
        idx_mode = np.argmax(pdf)
        x_mode = xs[idx_mode]
        y_mode = ys[idx_mode]
        
        # mean of skew normal: delta = alpha / sqrt(1 + alpha^2), mean_z = delta * sqrt(2/pi)
        delta = alpha / np.sqrt(1.0 + alpha**2)
        mean_z = delta * np.sqrt(2.0 / np.pi)
        x_mean = cx + mean_z * sigma
        y_mean = np.interp(x_mean, xs, ys)

        # median is approximately between mode and mean
        median_z = delta * np.sqrt(2.0 / np.pi) * 0.65
        x_med = cx + median_z * sigma
        y_med = np.interp(x_med, xs, ys)

        d = f"M {xs[0]:.1f} {base_y:.1f} " + " ".join(f"L {x:.1f} {y:.1f}" for x, y in zip(xs, ys)) + f" L {xs[-1]:.1f} {base_y:.1f}"
        return d, (x_mode, y_mode), (x_med, y_med), (x_mean, y_mean)

    sym_path, sym_mode, _, _ = skew_normal(640, 520, 360, 160, 0.0)
    pos_path, pos_mode, pos_med, pos_mean = skew_normal(580, 1200, 360, 160, 4.0)
    neg_path, neg_mode, neg_med, neg_mean = skew_normal(700, 1920, 360, 160, -4.0)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />

  <!-- PANEL 1: Symmetrical -->
  <text x="80" y="80" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">Symmetrical</text>
  <text x="80" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">(Mean = Median = Mode)</text>

  <path d="{sym_path}" fill="none" stroke="#0284c7" stroke-width="5" />
  <line x1="80" y1="520" x2="1200" y2="520" stroke="#334155" stroke-width="4" />
  <line x1="640" y1="{sym_mode[1]}" x2="640" y2="520" stroke="#334155" stroke-width="3" />
  
  <text x="640" y="565" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Mean</text>
  <text x="640" y="605" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Median</text>
  <text x="640" y="645" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Mode</text>

  <!-- PANEL 2: Positive Skew -->
  <line x1="80" y1="710" x2="1200" y2="710" stroke="#e2e8f0" stroke-width="3" />
  <text x="80" y="780" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">Positive (right) skew</text>
  <text x="80" y="830" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">(Mean &gt; Median &gt; Mode)</text>

  <path d="{pos_path}" fill="none" stroke="#0284c7" stroke-width="5" />
  <line x1="80" y1="1200" x2="1200" y2="1200" stroke="#334155" stroke-width="4" />
  
  <!-- Mode -->
  <line x1="{pos_mode[0]:.1f}" y1="{pos_mode[1]:.1f}" x2="{pos_mode[0]:.1f}" y2="1290" stroke="#334155" stroke-width="3" />
  <line x1="{pos_mode[0]:.1f}" y1="1290" x2="680" y2="1290" stroke="#334155" stroke-width="2" />
  <text x="700" y="1300" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Mode</text>

  <!-- Median -->
  <line x1="{pos_med[0]:.1f}" y1="{pos_med[1]:.1f}" x2="{pos_med[0]:.1f}" y2="1255" stroke="#334155" stroke-width="3" />
  <line x1="{pos_med[0]:.1f}" y1="1255" x2="680" y2="1255" stroke="#334155" stroke-width="2" />
  <text x="700" y="1265" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Median</text>

  <!-- Mean -->
  <line x1="{pos_mean[0]:.1f}" y1="{pos_mean[1]:.1f}" x2="{pos_mean[0]:.1f}" y2="1220" stroke="#334155" stroke-width="3" />
  <line x1="{pos_mean[0]:.1f}" y1="1220" x2="680" y2="1220" stroke="#334155" stroke-width="2" />
  <text x="700" y="1230" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Mean</text>

  <!-- PANEL 3: Negative Skew -->
  <line x1="80" y1="1380" x2="1200" y2="1380" stroke="#e2e8f0" stroke-width="3" />
  <text x="80" y="1450" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">Negative (left) skew</text>
  <text x="80" y="1500" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">(Mean &lt; Median &lt; Mode)</text>

  <path d="{neg_path}" fill="none" stroke="#0284c7" stroke-width="5" />
  <line x1="80" y1="1920" x2="1200" y2="1920" stroke="#334155" stroke-width="4" />

  <!-- Mean -->
  <line x1="{neg_mean[0]:.1f}" y1="{neg_mean[1]:.1f}" x2="{neg_mean[0]:.1f}" y2="1945" stroke="#334155" stroke-width="3" />
  <text x="{neg_mean[0]:.1f}" y="1985" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Mean</text>

  <!-- Median -->
  <line x1="{neg_med[0]:.1f}" y1="{neg_med[1]:.1f}" x2="{neg_med[0]:.1f}" y2="2020" stroke="#334155" stroke-width="3" />
  <text x="{neg_med[0]:.1f}" y="2060" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Median</text>

  <!-- Mode -->
  <line x1="{neg_mode[0]:.1f}" y1="{neg_mode[1]:.1f}" x2="{neg_mode[0]:.1f}" y2="2095" stroke="#334155" stroke-width="3" />
  <text x="{neg_mode[0]:.1f}" y="2135" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Mode</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/0abb7ae175098e266ea2.png")
    print(f"Saved 0abb7ae175098e266ea2.png ({pix.width}x{pix.height})")


def render_97e9():
    w, h = 2497, 1475
    def y_pos(val):
        return 1375 - val * 12.75

    box_left = 700
    box_right = 1800
    cx = (box_left + box_right) / 2

    q1_y = y_pos(20)
    q3_y = y_pos(54)
    med_y = y_pos(38.5)
    mean_y = y_pos(41.5)
    max_y = y_pos(98)
    min_y = y_pos(2)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
"""
    for val in range(0, 101, 10):
        y = y_pos(val)
        svg += f"""  <line x1="200" y1="{y}" x2="2350" y2="{y}" stroke="#cbd5e1" stroke-width="2" />
  <text x="160" y="{y + 12}" text-anchor="end" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">{val}</text>\n"""

    svg += f"""
  <!-- Whiskers -->
  <line x1="{cx}" y1="{q3_y}" x2="{cx}" y2="{max_y}" stroke="#0284c7" stroke-width="6" />
  <line x1="{cx - 150}" y1="{max_y}" x2="{cx + 150}" y2="{max_y}" stroke="#0284c7" stroke-width="6" />
  <text x="{cx + 180}" y="{max_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Largest observation (98)</text>

  <line x1="{cx}" y1="{q1_y}" x2="{cx}" y2="{min_y}" stroke="#0284c7" stroke-width="6" />
  <line x1="{cx - 150}" y1="{min_y}" x2="{cx + 150}" y2="{min_y}" stroke="#0284c7" stroke-width="6" />
  <text x="{cx + 180}" y="{min_y + 12}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold">Smallest observation (2)</text>

  <!-- The Box: Q1 to Q3 -->
  <rect x="{box_left}" y="{q3_y}" width="{box_right - box_left}" height="{q1_y - q3_y}" fill="#ffffff" stroke="#0284c7" stroke-width="6" />

  <!-- Median Line -->
  <line x1="{box_left}" y1="{med_y}" x2="{box_right}" y2="{med_y}" stroke="#0284c7" stroke-width="6" />
  <text x="{box_right + 30}" y="{med_y + 12}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold">Median (38.5)</text>

  <!-- Mean marker 'x' -->
  <line x1="{cx - 14}" y1="{mean_y - 14}" x2="{cx + 14}" y2="{mean_y + 14}" stroke="#0284c7" stroke-width="6" />
  <line x1="{cx - 14}" y1="{mean_y + 14}" x2="{cx + 14}" y2="{mean_y - 14}" stroke="#0284c7" stroke-width="6" />
  
  <text x="{cx}" y="{mean_y - 35}" text-anchor="middle" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold">Mean (41.5)</text>
  <line x1="{cx}" y1="{mean_y - 28}" x2="{cx}" y2="{mean_y - 14}" stroke="#0f172a" stroke-width="3" />

  <!-- Box annotations -->
  <text x="{box_left - 30}" y="{q3_y + 12}" text-anchor="end" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Q3 (75th percentile) = 54</text>
  <text x="{box_left - 30}" y="{q1_y + 12}" text-anchor="end" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Q1 (25th percentile) = 20</text>
  <text x="{box_left - 30}" y="{(q1_y + q3_y)/2 + 12}" text-anchor="end" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">IQR = Q3 – Q1 = 34</text>

</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/97e98af8fc5291307d5c.png")
    print(f"Saved 97e98af8fc5291307d5c.png ({pix.width}x{pix.height})")

if __name__ == "__main__":
    render_0abb()
    render_97e9()
