import fitz
import numpy as np

def render_cae0():
    # Figure 47.1: Benchmark U.S. Treasury Yield Curve (2305 x 1380)
    w, h = 2305, 1380
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2205" height="1280" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1152" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 47.1: Benchmark U.S. Treasury Yield Curve</text>
  <text x="1152" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">On-the-run Treasury coupon yields plotted against term to maturity from 1 Month to 30 Years</text>
  
  <!-- Axes -->
  <line x1="200" y1="1080" x2="2050" y2="1080" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="1080" x2="200" y2="250" stroke="#0f172a" stroke-width="5" />
  <text x="200" y="220" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Yield to Maturity (%)</text>
  <text x="2050" y="1135" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">Maturity (Years)</text>
  
  <!-- Y-axis ticks: 0% to 6% -->
  <!-- 0% at 1080, 2% at 810, 4% at 540, 6% at 270 -->
  <line x1="190" y1="810" x2="200" y2="810" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="540" x2="200" y2="540" stroke="#0f172a" stroke-width="3" />
  <line x1="190" y1="270" x2="200" y2="270" stroke="#0f172a" stroke-width="3" />
  <text x="175" y="1090" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="end">0.0%</text>
  <text x="175" y="820" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="end">2.0%</text>
  <text x="175" y="550" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="end">4.0%</text>
  <text x="175" y="280" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="end">6.0%</text>
  
  <line x1="200" y1="810" x2="2050" y2="810" stroke="#f1f5f9" stroke-width="2" />
  <line x1="200" y1="540" x2="2050" y2="540" stroke="#f1f5f9" stroke-width="2" />
  <line x1="200" y1="270" x2="2050" y2="270" stroke="#f1f5f9" stroke-width="2" />
  
  <!-- Normal Yield Curve: starts steep at short end (bills), flattens at 10y-30y -->
  <path d="M 220 860 C 450 680 800 520 1200 480 C 1600 440 1850 420 2000 410" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Maturity Points and Labels -->
"""
    tenors = [
        ("1M", 240, 840, "1.8%"),
        ("3M", 340, 770, "2.3%"),
        ("6M", 460, 700, "2.8%"),
        ("1Y", 620, 630, "3.3%"),
        ("2Y", 800, 560, "3.8%"),
        ("3Y", 960, 520, "4.1%"),
        ("5Y", 1180, 480, "4.4%"),
        ("7Y", 1380, 460, "4.6%"),
        ("10Y", 1600, 440, "4.7%"),
        ("20Y", 1820, 420, "4.9%"),
        ("30Y", 2000, 410, "5.0%")
    ]
    for ten, xp, yp, yld in tenors:
        svg += f"""
  <circle cx="{xp}" cy="{yp}" r="9" fill="#0284c7" stroke="#ffffff" stroke-width="2" />
  <line x1="{xp}" y1="1080" x2="{xp}" y2="1095" stroke="#0f172a" stroke-width="2.5" />
  <text x="{xp}" y="1135" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{ten}</text>
  <text x="{xp}" y="{yp - 16}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">{yld}</text>
"""

    svg += """
  <!-- Callout Box -->
  <rect x="1350" y="550" width="650" height="130" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" rx="12" />
  <text x="1675" y="595" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Normal (Upward-Sloping) Term Structure</text>
  <text x="1675" y="630" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Longer maturities carry term premium for duration risk.</text>
  <text x="1675" y="658" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Serves as risk-free benchmark for all credit spreads.</text>
  
  <!-- Footer Note -->
  <rect x="200" y="1180" width="1850" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1125" y="1232" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Yield Curve Shapes: Normal (upward sloping: expansion), Inverted (downward sloping: recession warning), Flat (transition), Humped.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/cae0e11b0b300886d0c4.png")
    print(f"Saved cae0e11b0b300886d0c4.png ({pix.width}x{pix.height})")

def render_dd14():
    # Figure 49.1: Fixed-income credit and maturity spectrum matrix (2038 x 1624)
    w, h = 2038, 1624
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1938" height="1524" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1019" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 49.1: Fixed-Income Credit &amp; Maturity Spectrum</text>
  <text x="1019" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Mapping bond asset classes across credit risk quality and duration maturity buckets</text>
  
  <!-- Column Headers (Maturity) -->
  <rect x="420" y="240" width="460" height="70" fill="#0284c7" rx="12" />
  <text x="650" y="283" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Short-Term (&lt; 3 Years)</text>
  
  <rect x="910" y="240" width="460" height="70" fill="#0284c7" rx="12" />
  <text x="1140" y="283" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Intermediate (3–10 Years)</text>
  
  <rect x="1400" y="240" width="460" height="70" fill="#0284c7" rx="12" />
  <text x="1630" y="283" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Long-Term (&gt; 10 Years)</text>
  
  <!-- Row 1: Sovereign / Supernational -->
  <rect x="100" y="340" width="280" height="340" fill="#f0fdf4" stroke="#10b981" stroke-width="3" rx="14" />
  <text x="240" y="500" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Sovereign / Agency</text>
  <text x="240" y="540" fill="#047857" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Highest Credit Quality (AAA/AA)</text>
  
  <!-- Cells Row 1 -->
  <rect x="420" y="340" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="650" y="420" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Treasury Bills / Commercial Paper</text>
  <text x="650" y="470" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Cash equivalents / Near-zero duration</text>
  <text x="650" y="510" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• High liquidity, minimal spread</text>
  <text x="650" y="550" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Money market instruments</text>
  
  <rect x="910" y="340" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1140" y="420" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Treasury Notes / Sovereign Bonds</text>
  <text x="1140" y="470" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Moderate duration sensitivity</text>
  <text x="1140" y="510" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Benchmark reference rates</text>
  <text x="1140" y="550" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Core reserve holdings for central banks</text>
  
  <rect x="1400" y="340" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1630" y="420" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">30-Year Treasury / Gilt / Bund</text>
  <text x="1630" y="470" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• High duration risk, zero default risk</text>
  <text x="1630" y="510" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Asset-liability matching for pensions</text>
  <text x="1630" y="550" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Pure interest rate exposure</text>
  
  <!-- Row 2: Investment-Grade Corporate -->
  <rect x="100" y="710" width="280" height="340" fill="#eff6ff" stroke="#0284c7" stroke-width="3" rx="14" />
  <text x="240" y="870" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Investment Grade</text>
  <text x="240" y="910" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Corporate (AAA to BBB–)</text>
  
  <rect x="420" y="710" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="650" y="790" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Short-Term IG Corporate</text>
  <text x="650" y="840" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Modest credit spread over Treasuries</text>
  <text x="650" y="880" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Low volatility cash management</text>
  <text x="650" y="920" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Popular for corporate treasurers</text>
  
  <rect x="910" y="710" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1140" y="790" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Intermediate IG Corporate</text>
  <text x="1140" y="840" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Core fixed-income allocation</text>
  <text x="1140" y="880" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Blends credit spread + duration yield</text>
  <text x="1140" y="920" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Liquid institutional market</text>
  
  <rect x="1400" y="710" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1630" y="790" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Long-Term IG Corporate</text>
  <text x="1630" y="840" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• High sensitivity to interest rates</text>
  <text x="1630" y="880" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Significant duration &amp; spread duration</text>
  <text x="1630" y="920" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Life insurers and pension liability match</text>
  
  <!-- Row 3: High Yield -->
  <rect x="100" y="1080" width="280" height="340" fill="#fef2f2" stroke="#ef4444" stroke-width="3" rx="14" />
  <text x="240" y="1240" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">High Yield / Junk</text>
  <text x="240" y="1280" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Sub-Investment Grade (&lt; BBB–)</text>
  
  <rect x="420" y="1080" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="650" y="1160" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Short-Duration High Yield</text>
  <text x="650" y="1210" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Focuses strictly on default/credit risk</text>
  <text x="650" y="1250" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Low rate sensitivity, high income yield</text>
  <text x="650" y="1290" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Attractive in rising rate environments</text>
  
  <rect x="910" y="1080" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1140" y="1160" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Broad High Yield Market</text>
  <text x="1140" y="1210" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• High correlation with equity cycles</text>
  <text x="1140" y="1250" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Covenants, call features, and liquidity risk</text>
  <text x="1140" y="1290" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Substantial default loss potential</text>
  
  <rect x="1400" y="1080" width="460" height="340" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1630" y="1160" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Distressed Debt / Mezzanine</text>
  <text x="1630" y="1210" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Extremely rare for high yield to issue &gt; 10y</text>
  <text x="1630" y="1250" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• Restructuring, bankruptcy claims, workout</text>
  <text x="1630" y="1290" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">• High risk, private debt / hedge fund focus</text>
  
  <!-- Footer Note -->
  <rect x="100" y="1450" width="1760" height="80" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="980" y="1498" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Investor Takeaway: The two primary risks in bond portfolio construction are Duration Risk (horizontal axis) and Credit/Default Risk (vertical axis).</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/dd14baf42741ba494d49.png")
    print(f"Saved dd14baf42741ba494d49.png ({pix.width}x{pix.height})")

def render_5136():
    # Figure 49.2: Institutional investor positioning chart (2042 x 1524)
    w, h = 2042, 1524
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="1942" height="1424" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1021" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 49.2: Institutional Investor Positioning</text>
  <text x="1021" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Mapping major institutional asset managers across Liability Duration and Risk/Return Profiles</text>
  
  <!-- Header Table -->
  <rect x="80" y="240" width="1882" height="65" fill="#0284c7" rx="12" />
  <text x="250" y="283" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">Institutional Investor</text>
  <text x="650" y="283" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Liability Horizon</text>
  <text x="1050" y="283" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Liquidity Requirement</text>
  <text x="1450" y="283" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Target Fixed-Income Sector</text>
  <text x="1800" y="283" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Tax Status</text>
"""
    investors = [
        ("Commercial Banks", "Short-term (Deposits are demand liabilities)", "Very High (Reserve requirements & withdrawals)", "Short-dated Treasuries, Agencies, ABS, High-grade floating notes", "Fully Taxable"),
        ("Life Insurance Companies", "Long-term (Predictable mortality claims over decades)", "Low (Predictable payout schedules)", "Long-term IG Corporates, Infrastructure debt, Commercial mortgages", "Fully Taxable"),
        ("Property & Casualty (P&C) Insurers", "Short to Intermediate (Unpredictable claim events / storms)", "High (Contingency reserves for sudden catastrophe losses)", "High-quality short/intermediate municipal bonds, Treasuries, IG debt", "Fully Taxable"),
        ("Defined Benefit Pension Plans", "Very Long-term (Decades of contractual retiree pension obligations)", "Low to Moderate (Regular benefit disbursement matching)", "Long-term Government and Corporate bonds, STRIPS (ALM matching)", "Tax-Exempt"),
        ("Foundations & Endowments", "Perpetual (Maintain real purchasing power forever while spending ~5%)", "Low (Predictable annual spending policy rate)", "Diversified core fixed-income, inflation-protected bonds (TIPS), private debt", "Tax-Exempt"),
        ("Sovereign Wealth Funds (SWFs)", "Long-term / Intergenerational wealth transfer", "Low (Excluding sudden commodity revenue shock stabilization)", "Global government benchmarks, high-grade sovereigns, diversified debt", "Tax-Exempt / Varies"),
        ("Central Banks", "Open Market Operations / Foreign Exchange Reserves", "Maximum (Immediate intervention and monetary transmission)", "Ultra-liquid short and medium sovereign paper, gold, IMF SDRs", "Non-Taxable")
    ]
    y_row = 320
    for i, (inv, horiz, liq, sect, tax) in enumerate(investors):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="80" y="{y_row}" width="1882" height="135" fill="{bg}" />
  <text x="110" y="{y_row + 45}" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold">{inv}</text>
  <text x="110" y="{y_row + 85}" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20">Investment Objective</text>
  <text x="650" y="{y_row + 55}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">{horiz}</text>
  <text x="1050" y="{y_row + 55}" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{liq}</text>
  <foreignObject x="1220" y="{y_row + 15}" width="460" height="110">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 20px; color: #334155; line-height: 1.3; text-align: center;">
      {sect}
    </div>
  </foreignObject>
  <text x="1800" y="{y_row + 55}" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{tax}</text>
  <line x1="80" y1="{y_row + 135}" x2="1962" y2="{y_row + 135}" stroke="#e2e8f0" stroke-width="1.5" />
"""
        y_row += 140

    svg += """
  <!-- Footer Note -->
  <rect x="80" y="1330" width="1882" height="85" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1021" y="1382" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Asset-Liability Management (ALM): Institutional bond portfolios are shaped primarily by the duration, cash flow timing, and predictability of their liabilities.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/5136fa555016721788f2.png")
    print(f"Saved 5136fa555016721788f2.png ({pix.width}x{pix.height})")

def render_f022():
    # Figure 50.1: Repurchase agreement (repo) transaction structure (2402 x 1322)
    w, h = 2402, 1322
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2302" height="1222" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1201" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 50.1: Repurchase Agreement (Repo) Transaction Structure</text>
  <text x="1201" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Secured short-term financing mechanism between Borrower (Seller) and Lender (Buyer)</text>
  
  <!-- PHASE 1: INCEPTION (START OF REPO) -->
  <rect x="100" y="240" width="2202" height="420" fill="#f8fafc" stroke="#0284c7" stroke-width="3" rx="16" />
  <rect x="100" y="240" width="2202" height="60" fill="#0284c7" rx="16" />
  <rect x="100" y="280" width="2202" height="20" fill="#0284c7" />
  <text x="1201" y="282" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Phase 1: Inception of Repo (Today / Time 0)</text>
  
  <!-- Inception Left Entity -->
  <rect x="200" y="340" width="550" height="270" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="475" y="400" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Borrower / Dealer</text>
  <text x="475" y="440" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">(Repo Seller / Cash Borrower)</text>
  <text x="475" y="500" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Holds Treasury collateral; Needs short-term liquidity</text>
  <text x="475" y="535" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Agrees to buy back securities later</text>
  
  <!-- Inception Right Entity -->
  <rect x="1650" y="340" width="550" height="270" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="1925" y="400" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Lender / Investor</text>
  <text x="1925" y="440" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">(Reverse Repo Buyer / Cash Lender)</text>
  <text x="1925" y="500" fill="#334155" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Has excess cash; Requires secured yield</text>
  <text x="1925" y="535" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">Takes delivery of Treasury collateral</text>
  
  <!-- Flow Arrows Phase 1 -->
  <!-- Top Arrow: Collateral delivered from Borrower to Lender -->
  <line x1="770" y1="410" x2="1630" y2="410" stroke="#0284c7" stroke-width="5" />
  <polygon points="1630,410 1614,400 1614,420" fill="#0284c7" />
  <rect x="980" y="370" width="440" height="45" fill="#eff6ff" stroke="#0284c7" stroke-width="2" rx="8" />
  <text x="1200" y="400" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">1. Delivers High-Quality Collateral (Treasuries) →</text>
  
  <!-- Bottom Arrow: Cash Loan delivered from Lender to Borrower -->
  <line x1="1630" y1="510" x2="770" y2="510" stroke="#059669" stroke-width="5" />
  <polygon points="770,510 786,500 786,520" fill="#059669" />
  <rect x="980" y="490" width="440" height="45" fill="#ecfdf5" stroke="#059669" stroke-width="2" rx="8" />
  <text x="1200" y="520" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">← 2. Disburses Cash Loan ($10,000,000 minus Haircut)</text>
  
  
  <!-- PHASE 2: MATURITY (END OF REPO) -->
  <rect x="100" y="700" width="2202" height="420" fill="#f8fafc" stroke="#059669" stroke-width="3" rx="16" />
  <rect x="100" y="700" width="2202" height="60" fill="#059669" rx="16" />
  <rect x="100" y="740" width="2202" height="20" fill="#059669" />
  <text x="1201" y="742" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Phase 2: Maturity / Unwind (Overnight or Term Date)</text>
  
  <!-- Maturity Left Entity -->
  <rect x="200" y="800" width="550" height="270" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="475" y="860" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Borrower / Dealer</text>
  <text x="475" y="900" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Repays principal + repo interest</text>
  <text x="475" y="955" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Receives collateral back</text>
  
  <!-- Maturity Right Entity -->
  <rect x="1650" y="800" width="550" height="270" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" rx="14" />
  <text x="1925" y="860" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">Lender / Investor</text>
  <text x="1925" y="900" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Receives cash + repo interest yield</text>
  <text x="1925" y="955" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Returns Treasury collateral</text>
  
  <!-- Flow Arrows Phase 2 -->
  <!-- Top Arrow: Repurchase Cash delivered from Borrower to Lender -->
  <line x1="770" y1="870" x2="1630" y2="870" stroke="#059669" stroke-width="5" />
  <polygon points="1630,870 1614,860 1614,880" fill="#059669" />
  <rect x="940" y="830" width="520" height="45" fill="#ecfdf5" stroke="#059669" stroke-width="2" rx="8" />
  <text x="1200" y="860" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">1. Repays Cash Principal + Repo Interest →</text>
  
  <!-- Bottom Arrow: Collateral Returned from Lender to Borrower -->
  <line x1="1630" y1="970" x2="770" y2="970" stroke="#0284c7" stroke-width="5" />
  <polygon points="770,970 786,960 786,980" fill="#0284c7" />
  <rect x="940" y="950" width="520" height="45" fill="#eff6ff" stroke="#0284c7" stroke-width="2" rx="8" />
  <text x="1200" y="980" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">← 2. Returns Treasury Collateral to Borrower</text>
  
  <!-- Summary Box -->
  <rect x="100" y="1150" width="2202" height="90" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1201" y="1195" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Key Terms: Repo Rate = (Repurchase Price – Sale Price) / Sale Price × (360 / Days) | Haircut (Margin) protects lender against collateral price fluctuations.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/f02266fc1f325393b01c.png")
    print(f"Saved f02266fc1f325393b01c.png ({pix.width}x{pix.height})")

def render_8adc():
    # Figure 52.1: Market Yield vs Bond Value for an 8% Coupon Bond (2122 x 1212)
    w, h = 2122, 1212
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2022" height="1112" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1061" y="125" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="bold" text-anchor="middle">Figure 52.1: Inverse Price-Yield Relationship and Convexity</text>
  <text x="1061" y="175" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">8% Coupon, 20-Year Option-Free Bond demonstrating asymmetric price responsiveness</text>
  
  <!-- Axes -->
  <line x1="200" y1="950" x2="1950" y2="950" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="950" x2="200" y2="220" stroke="#0f172a" stroke-width="5" />
  <text x="200" y="190" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">Bond Price ($)</text>
  <text x="1950" y="1005" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" text-anchor="end">Market Yield / YTM (%)</text>
  
  <!-- Convex Price-Yield Curve -->
  <path d="M 280 260 C 500 480 800 680 1060 680 C 1350 680 1650 820 1880 890" fill="none" stroke="#0284c7" stroke-width="7" />
  
  <!-- Par Point: YTM = 8%, Price = $1,000 (at x=1060, y=680) -->
  <circle cx="1060" cy="680" r="11" fill="#059669" />
  <line x1="1060" y1="950" x2="1060" y2="680" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="200" y1="680" x2="1060" y2="680" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  <text x="1060" y="995" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">8.0% (Coupon Rate)</text>
  <text x="175" y="688" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">$1,000 (Par)</text>
  
  <!-- Premium Region: YTM = 6%, Price = $1,231 (x=660, y=470) -->
  <circle cx="660" cy="470" r="10" fill="#0284c7" />
  <line x1="660" y1="950" x2="660" y2="470" stroke="#64748b" stroke-width="2.5" stroke-dasharray="6 6" />
  <line x1="200" y1="470" x2="660" y2="470" stroke="#64748b" stroke-width="2.5" stroke-dasharray="6 6" />
  <text x="660" y="995" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">6.0%</text>
  <text x="175" y="478" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">$1,231</text>
  
  <!-- Discount Region: YTM = 10%, Price = $830 (x=1460, y=810) -->
  <circle cx="1460" cy="810" r="10" fill="#e11d48" />
  <line x1="1460" y1="950" x2="1460" y2="810" stroke="#64748b" stroke-width="2.5" stroke-dasharray="6 6" />
  <line x1="200" y1="810" x2="1460" y2="810" stroke="#64748b" stroke-width="2.5" stroke-dasharray="6 6" />
  <text x="1460" y="995" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">10.0%</text>
  <text x="175" y="818" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">$830</text>
  
  <!-- Asymmetry Bracket Comparison: -->
  <!-- Yield drops 2% (8% -> 6%): Price rises +$231 -->
  <!-- Yield rises 2% (8% -> 10%): Price falls -$170 -->
  <rect x="400" y="300" width="520" height="90" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="10" />
  <text x="660" y="340" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Yield Drops 200 bps (8% → 6%):</text>
  <text x="660" y="375" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Price Rises +$231 (+23.1%) ↗</text>
  
  <rect x="1350" y="650" width="520" height="90" fill="#fef2f2" stroke="#ef4444" stroke-width="2" rx="10" />
  <text x="1610" y="690" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Yield Rises 200 bps (8% → 10%):</text>
  <text x="1610" y="725" fill="#dc2626" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Price Falls –$170 (–17.0%) ↘</text>
  
  <!-- Footer Note -->
  <rect x="200" y="1040" width="1750" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1075" y="1080" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Convexity Effect: For an option-free bond, price gain from a yield decrease exceeds price loss from an equal yield increase.</text>
  <text x="1075" y="1115" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Because the curve is convex, a tangent duration line always underestimates bond prices.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/8adc7ab21674bb09ec87.png")
    print(f"Saved 8adc7ab21674bb09ec87.png ({pix.width}x{pix.height})")

def render_484a():
    # Figure 52.2: Bond price convergence paths over time / Pull to Par (1942 x 965)
    w, h = 1942, 965
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="40" y="40" width="1862" height="885" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="971" y="115" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle">Figure 52.2: Constant-Yield Price Trajectories ("Pull to Par")</text>
  <text x="971" y="160" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="26" text-anchor="middle">Assuming market discount rate remains constant over time until maturity</text>
  
  <!-- Axes -->
  <line x1="180" y1="780" x2="1750" y2="780" stroke="#0f172a" stroke-width="4" />
  <line x1="180" y1="780" x2="180" y2="200" stroke="#0f172a" stroke-width="4" />
  <text x="180" y="175" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Bond Price ($)</text>
  <text x="1750" y="825" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">Time to Maturity</text>
  
  <!-- Par Value line ($1,000) at y=480 -->
  <line x1="180" y1="480" x2="1650" y2="480" stroke="#059669" stroke-width="5" />
  <circle cx="1650" cy="480" r="10" fill="#059669" />
  <text x="160" y="488" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="end">$1,000 (Par)</text>
  <text x="800" y="460" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Par Bond (Coupon = YTM)</text>
  
  <!-- Premium Bond Path: starts at y=250 ($1,250), pulls down to (1650, 480) -->
  <path d="M 180 250 Q 900 290 1650 480" fill="none" stroke="#0284c7" stroke-width="6" />
  <text x="160" y="258" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">Premium ($1,250)</text>
  <text x="600" y="270" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Premium Bond (Coupon &gt; YTM) → Amortizes Down to Par</text>
  
  <!-- Discount Bond Path: starts at y=710 ($750), pulls up to (1650, 480) -->
  <path d="M 180 710 Q 900 670 1650 480" fill="none" stroke="#e11d48" stroke-width="6" />
  <text x="160" y="718" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="end">Discount ($750)</text>
  <text x="600" y="710" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold">Discount Bond (Coupon &lt; YTM) → Accretes Up to Par</text>
  
  <!-- Maturity Point Label -->
  <line x1="1650" y1="780" x2="1650" y2="480" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="1650" y="825" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Maturity Date (Price = Par)</text>
  <text x="180" y="825" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Issue Date</text>
  
  <!-- Bottom summary banner -->
  <rect x="180" y="855" width="1570" height="55" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" rx="8" />
  <text x="965" y="890" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Pull to Par Effect: If the market discount rate remains unchanged, capital gains/losses amortize cleanly to zero at maturity.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/484a28cf39e95750e504.png")
    print(f"Saved 484a28cf39e95750e504.png ({pix.width}x{pix.height})")

def render_eb35():
    # Figure 52.3: Premium, Par, and Discount Bonds (2492 x 1365)
    w, h = 2492, 1365
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2392" height="1265" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1246" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 52.3: Relationships Among Coupon Rate, Current Yield, and YTM</text>
  <text x="1246" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Comparative analysis of pricing conditions for fixed-rate bonds</text>
  
  <!-- Header -->
  <rect x="80" y="240" width="2332" height="70" fill="#0284c7" rx="12" />
  <text x="300" y="285" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold">Bond Condition</text>
  <text x="800" y="285" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Price vs. Par Value</text>
  <text x="1400" y="285" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Yield Metric Relationship</text>
  <text x="2000" y="285" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">Capital Gain / Loss over Holding Period</text>
"""
    rows = [
        ("Discount Bond", "Price &lt; Par Value", "Coupon Rate &lt; Current Yield &lt; Yield to Maturity (YTM)", "Capital gain required over time to pull price up to par value.", "#e11d48"),
        ("Par Bond", "Price = Par Value", "Coupon Rate = Current Yield = Yield to Maturity (YTM)", "Zero capital gain or loss; total return equals coupon income.", "#059669"),
        ("Premium Bond", "Price &gt; Par Value", "Coupon Rate &gt; Current Yield &gt; Yield to Maturity (YTM)", "Capital loss amortizes over time to pull price down to par value.", "#0284c7")
    ]
    y_row = 330
    for i, (cond, pr, yld, cap, col) in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        svg += f"""
  <rect x="80" y="{y_row}" width="2332" height="160" fill="{bg}" />
  <text x="120" y="{y_row + 65}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold">{cond}</text>
  <text x="800" y="{y_row + 65}" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">{pr}</text>
  <text x="1400" y="{y_row + 65}" fill="{col}" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">{yld}</text>
  <foreignObject x="1750" y="{y_row + 20}" width="550" height="120">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 22px; color: #475569; line-height: 1.4;">
      {cap}
    </div>
  </foreignObject>
  <line x1="80" y1="{y_row + 160}" x2="2412" y2="{y_row + 160}" stroke="#e2e8f0" stroke-width="2" />
"""
        y_row += 165

    # 3 Example Cards Below
    svg += """
  <rect x="80" y="850" width="730" height="320" fill="#fef2f2" stroke="#ef4444" stroke-width="2.5" rx="14" />
  <text x="445" y="905" fill="#991b1b" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Discount Example (6% Coupon, 8% YTM)</text>
  <text x="445" y="960" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Price: $803.64 | Current Yield: 7.47%</text>
  <text x="445" y="1010" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">6.00% &lt; 7.47% &lt; 8.00%</text>
  <text x="445" y="1060" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Current yield understates total return (YTM)</text>
  
  <rect x="881" y="850" width="730" height="320" fill="#f0fdf4" stroke="#10b981" stroke-width="2.5" rx="14" />
  <text x="1246" y="905" fill="#065f46" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Par Example (8% Coupon, 8% YTM)</text>
  <text x="1246" y="960" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Price: $1,000.00 | Current Yield: 8.00%</text>
  <text x="1246" y="1010" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">8.00% = 8.00% = 8.00%</text>
  <text x="1246" y="1060" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Current yield perfectly equals YTM</text>
  
  <rect x="1682" y="850" width="730" height="320" fill="#eff6ff" stroke="#0284c7" stroke-width="2.5" rx="14" />
  <text x="2047" y="905" fill="#0369a1" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Premium Example (10% Coupon, 8% YTM)</text>
  <text x="2047" y="960" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">Price: $1,196.36 | Current Yield: 8.36%</text>
  <text x="2047" y="1010" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">10.00% &gt; 8.36% &gt; 8.00%</text>
  <text x="2047" y="1060" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">Current yield overstates total return (YTM)</text>
  
  <!-- Footer Note -->
  <rect x="80" y="1200" width="2332" height="75" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1246" y="1248" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Definition: Current Yield = Annual Cash Coupon / Flat Market Bond Price. Because it ignores capital gains/losses, it is always between Coupon and YTM.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/eb35c23d463125aa873b.png")
    print(f"Saved eb35c23d463125aa873b.png ({pix.width}x{pix.height})")

def render_cd0a():
    # Figure 57.1: Graphic representation of approximate modified duration tangent line (2230 x 1515)
    w, h = 2230, 1515
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#f8fafc" rx="28" />
  <rect x="50" y="50" width="2130" height="1415" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" rx="20" />
  
  <text x="1115" y="130" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" text-anchor="middle">Figure 57.1: Modified Duration as the Tangent Line to Price-Yield Curve</text>
  <text x="1115" y="180" fill="#64748b" font-family="Arial, Helvetica, sans-serif" font-size="28" text-anchor="middle">Linear approximation of bond price sensitivity: %ΔPrice ≈ –ModDur × ΔYield</text>
  
  <!-- Axes -->
  <line x1="200" y1="1200" x2="2000" y2="1200" stroke="#0f172a" stroke-width="5" />
  <line x1="200" y1="1200" x2="200" y2="250" stroke="#0f172a" stroke-width="5" />
  <text x="200" y="220" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold">Bond Price (P)</text>
  <text x="2000" y="1255" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="end">Yield to Maturity (y)</text>
  
  <!-- Convex Price-Yield Curve -->
  <path d="M 280 320 C 550 580 850 780 1100 780 C 1400 780 1700 950 1950 1020" fill="none" stroke="#0284c7" stroke-width="7" />
  <text x="1960" y="1030" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Actual Price-Yield Curve</text>
  
  <!-- Tangent Line at Point (y0, P0) = (1100, 780) -->
  <!-- slope of curve at (1100, 780): ~ -0.45 -->
  <!-- tangent line from (500, 510) to (1700, 1050) -->
  <line x1="450" y1="488" x2="1750" y2="1073" stroke="#e11d48" stroke-width="5" stroke-dasharray="10 8" />
  <text x="1760" y="1080" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold">Tangent Line (Duration Estimate)</text>
  
  <!-- Center Point (y0, P0) -->
  <circle cx="1100" cy="780" r="12" fill="#059669" />
  <line x1="1100" y1="1200" x2="1100" y2="780" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  <line x1="200" y1="780" x2="1100" y2="780" stroke="#059669" stroke-width="3" stroke-dasharray="6 6" />
  <text x="1100" y="1245" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle">y₀ (Current Yield)</text>
  <text x="175" y="788" fill="#059669" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="end">P₀</text>
  
  <!-- Yield Drop Δy-: x=750 -->
  <!-- Actual price on curve at x=750: y=680 -->
  <!-- Tangent estimate at x=750: y=623 -->
  <line x1="750" y1="1200" x2="750" y2="600" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5 5" />
  <text x="750" y="1245" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">y₀ – Δy</text>
  
  <!-- Duration Error Gap on Left -->
  <line x1="750" y1="623" x2="750" y2="720" stroke="#e11d48" stroke-width="4" />
  <text x="730" y="670" fill="#e11d48" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" text-anchor="end">Duration Error Gap</text>
  
  <!-- Approx ModDur Formula Callout Box -->
  <rect x="350" y="270" width="700" height="150" fill="#f8fafc" stroke="#0284c7" stroke-width="2.5" rx="14" />
  <text x="700" y="315" fill="#0284c7" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">Approximate Modified Duration Formula:</text>
  <text x="700" y="360" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">ApproxModDur = (P_– – P_+) / (2 · P₀ · Δy)</text>
  <text x="700" y="398" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">P_– = Price if yield falls by Δy | P_+ = Price if yield rises by Δy</text>
  
  <!-- Footer Note -->
  <rect x="200" y="1290" width="1800" height="95" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" rx="12" />
  <text x="1100" y="1335" fill="#0f172a" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">Convexity Implication: The linear duration tangent line always sits BELOW the actual price-yield curve.</text>
  <text x="1100" y="1368" fill="#475569" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">For large yield changes, the second-order Convexity adjustment must be added to eliminate duration error.</text>
</svg>"""
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(alpha=False)
    pix.save("public/content/figures/cd0af4b7234dbcce56b4.png")
    print(f"Saved cd0af4b7234dbcce56b4.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    render_cae0()
    render_dd14()
    render_5136()
    render_f022()
    render_8adc()
    render_484a()
    render_eb35()
    render_cd0a()
