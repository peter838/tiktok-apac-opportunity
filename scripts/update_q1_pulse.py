from pathlib import Path
import csv
import json
import re

ROOT = Path('/data/.openclaw/workspace-vibe-agent/dhl-singapore-opportunity')
ANALYSIS = Path('/data/.openclaw/workspace/assets/dhl-po-metrics/dhl_q1_2026_country_analysis.json')
CSV = Path('/data/.openclaw/workspace/assets/dhl-po-metrics/dhl_monthly_po_metrics_2023-01_to_2026-03.csv')

# Corrected Singapore data files (DHL Singapore family only)
SG_CORRECTED_ANALYSIS = Path('/data/.openclaw/workspace/assets/dhl-po-metrics/dhl_sg_only_corrected_analysis.json')
SG_CORRECTED_MONTHLY = Path('/data/.openclaw/workspace/assets/dhl-po-metrics/dhl_sg_only_corrected_monthly.json')

analysis = json.loads(ANALYSIS.read_text())
analysis_by_code = {c['country_code'].lower(): c for c in analysis['countries']}

# Load corrected Singapore analysis data if available
if SG_CORRECTED_ANALYSIS.exists():
    sg_corrected = json.loads(SG_CORRECTED_ANALYSIS.read_text())
    # Update Singapore data in analysis with corrected values
    if 'sg' in analysis_by_code:
        # Get Q1 2026 data from corrected analysis
        q1_2026 = sg_corrected.get('q1_comparisons', {}).get('2026', {})
        q1_2025 = sg_corrected.get('q1_comparisons', {}).get('2025', {})
        q1_2024 = sg_corrected.get('q1_comparisons', {}).get('2024', {})
        q1_2023 = sg_corrected.get('q1_comparisons', {}).get('2023', {})
        baseline = sg_corrected.get('q1_comparisons', {}).get('baseline_median_2023_2025', {})
        forecast = sg_corrected.get('forecast_2026', {})
        
        # Update the Singapore entry with corrected data
        sg_data = analysis_by_code['sg']
        sg_data['q1_2026'] = {
            'po_count': q1_2026.get('po_count', 51),
            'po_value': q1_2026.get('po_value', 25203.71)
        }
        sg_data['comparisons'] = {
            '2025': {
                'q1_po_count': q1_2025.get('q1_po_count', 68),
                'q1_po_value': q1_2025.get('q1_po_value', 185005.67),
                'po_count_delta': q1_2025.get('po_count_delta', -17),
                'po_value_delta': q1_2025.get('po_value_delta', -159801.96),
                'po_count_pct_change': q1_2025.get('po_count_pct_change', -25.0),
                'po_value_pct_change': q1_2025.get('po_value_pct_change', -86.4)
            },
            '2024': {
                'q1_po_count': q1_2024.get('q1_po_count', 84),
                'q1_po_value': q1_2024.get('q1_po_value', 51118.0),
                'po_count_delta': q1_2024.get('po_count_delta', -33),
                'po_value_delta': q1_2024.get('po_value_delta', -25914.29),
                'po_count_pct_change': q1_2024.get('po_count_pct_change', -39.3),
                'po_value_pct_change': q1_2024.get('po_value_pct_change', -50.7)
            },
            '2023': {
                'q1_po_count': q1_2023.get('q1_po_count', 122),
                'q1_po_value': q1_2023.get('q1_po_value', 112151.34),
                'po_count_delta': q1_2023.get('po_count_delta', -71),
                'po_value_delta': q1_2023.get('po_value_delta', -86947.63),
                'po_count_pct_change': q1_2023.get('po_count_pct_change', -58.2),
                'po_value_pct_change': q1_2023.get('po_value_pct_change', -77.5)
            }
        }
        sg_data['baseline'] = {
            'period': 'Q1 median 2023-2025',
            'po_count': baseline.get('po_count', 84),
            'po_value': baseline.get('po_value', 112151.34),
            'po_count_pct_change': -39.3,
            'po_value_pct_change': -77.5
        }
        sg_data['assessment'] = {
            'label': 'lower than normal',
            'summary': 'Q1 2026 is 39.3% below the Q1 median on count and 77.5% below on value.'
        }
        sg_data['forecast_2026'] = {
            'method': forecast.get('method', 'Annualize Q1 2026 using the average Q1 share of annual totals from 2023-2025 (same approach as prior analysis, but on SG-only DHL scope).'),
            'po_count': forecast.get('po_count', 249),
            'po_value': forecast.get('po_value', 89058.79),
            'po_count_vs_2025_pct': -8.9,
            'po_value_vs_2025_pct': -26.8
        }
        sg_data['bullets'] = [
            'Q1 2026 total: 51 POs and 25,203.71 SGD (DHL Singapore family only).',
            'Vs Q1 2025: -25.0% in count and -86.4% in value.',
            'Assessment: lower than normal. Q1 2026 is 39.3% below the Q1 median on count and 77.5% below on value.',
            '2026 forecast: about 249 POs and 89,058.79 SGD for the full year, using average Q1 share from 2023-2025.',
            'Scope: DHL Express (Singapore), DHL Global Forwarding (Singapore), DHL Supply Chain Singapore ONLY.'
        ]
        sg_data['scope_note'] = 'Corrected to DHL Singapore family only. Excludes non-DHL Singapore-region orders.'
        print('Loaded corrected Singapore data from', SG_CORRECTED_ANALYSIS)

monthly = {}

# Load corrected Singapore monthly data if available
if SG_CORRECTED_MONTHLY.exists():
    sg_monthly = json.loads(SG_CORRECTED_MONTHLY.read_text())
    sg_rows = sg_monthly.get('monthly', [])
    monthly['sg'] = [
        {
            'month': row['month'],
            'po_count': row['po_count'],
            'po_value': row['po_value'],
            'currency': row.get('currency', 'SGD')
        }
        for row in sg_rows
    ]
    print('Loaded corrected Singapore monthly data from', SG_CORRECTED_MONTHLY)

with CSV.open(newline='') as f:
    for row in csv.DictReader(f):
        code = row['country_code'].lower()
        # Skip Singapore - already loaded from corrected file
        if code == 'sg':
            continue
        monthly.setdefault(code, []).append({
            'month': row['month'],
            'po_count': int(float(row['po_count'])),
            'po_value': float(row['po_value']),
        })
for code in monthly:
    monthly[code].sort(key=lambda r: r['month'])

annual = {}
for code, rows in monthly.items():
    annual_totals = {
        year: sum(row['po_value'] for row in rows if row['month'].startswith(f'{year}-'))
        for year in ['2023', '2024', '2025']
    }
    q1_totals = {
        year: sum(row['po_value'] for row in rows if row['month'].startswith(f'{year}-0') and int(row['month'][5:7]) <= 3)
        for year in ['2023', '2024', '2025']
    }
    q1_2026_value = sum(row['po_value'] for row in rows if row['month'].startswith('2026-') and int(row['month'][5:7]) <= 3)
    q1_shares = [q1_totals[year] / annual_totals[year] for year in ['2023', '2024', '2025'] if annual_totals[year]]
    avg_q1_share = sum(q1_shares) / len(q1_shares) if q1_shares else 0
    forecast_2026_value = q1_2026_value / avg_q1_share if avg_q1_share else 0
    annual[code] = {
        'currency': analysis_by_code.get(code, {}).get('currency', rows[0].get('currency', '') if rows else ''),
        'totals': annual_totals,
        'q1_totals': q1_totals,
        'q1_2026_value': q1_2026_value,
        'forecast_2026_value': forecast_2026_value,
        'avg_q1_share': avg_q1_share,
    }
analysis_by_code = {c['country_code'].lower(): c for c in analysis['countries']}


def fmt_count(v):
    return f"{int(round(v)):,}"


def fmt_value(v):
    return f"{v:,.2f}"


def compact_currency(v, currency):
    if v >= 1_000_000:
        return f"{currency} {v/1_000_000:.1f}M".replace('.0M', 'M')
    if v >= 1_000:
        return f"{currency} {v/1_000:.1f}K".replace('.0K', 'K')
    return f"{currency} {v:,.0f}"


def sign_pct(v):
    return f"{'+' if v > 0 else ''}{v:.1f}%"


def delta_class(v):
    return 'delta-pos' if v > 0 else 'delta-neg' if v < 0 else 'delta-flat'


def chip_class(label):
    return 'q1-chip-positive' if label == 'higher than normal' else 'q1-chip-negative' if label == 'lower than normal' else 'q1-chip-neutral'


def line_chart_svg(series, metric, currency=None):
    width, height = 1020, 300
    pad_l, pad_r, pad_t, pad_b = 62, 24, 24, 48
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    values = [s[metric] for s in series]
    ymax = max(values) * 1.08 if max(values) else 1

    def x(i):
        return pad_l + (plot_w * i / (len(series) - 1 if len(series) > 1 else 1))

    def y(v):
        return pad_t + plot_h - (v / ymax) * plot_h

    pts = [(x(i), y(v)) for i, v in enumerate(values)]

    def path(points):
        return ' '.join([('M' if i == 0 else 'L') + f'{px:.2f},{py:.2f}' for i, (px, py) in enumerate(points)])

    area = path([(pts[0][0], pad_t + plot_h)] + pts + [(pts[-1][0], pad_t + plot_h)])
    line = path(pts)

    grid = []
    for frac in [0, 0.25, 0.5, 0.75, 1.0]:
        gy = pad_t + plot_h - frac * plot_h
        val = ymax * frac
        label = fmt_count(val) if metric == 'po_count' else compact_currency(val, currency)
        grid.append(f'<line x1="{pad_l}" y1="{gy:.2f}" x2="{width-pad_r}" y2="{gy:.2f}" class="q1-gridline" />')
        grid.append(f'<text x="{pad_l-10}" y="{gy+4:.2f}" class="q1-axis-label q1-axis-y" text-anchor="end">{label}</text>')

    month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i, row in enumerate(series):
        if i % 3 == 0:
            year = row['month'][:4]
            month = int(row['month'][5:7])
            label = f"{month_labels[month-1]} {year[-2:]}"
            grid.append(f'<text x="{x(i):.2f}" y="{height-16}" class="q1-axis-label" text-anchor="middle">{label}</text>')
        if row['month'].endswith('-01') and i != 0:
            gx = x(i)
            grid.append(f'<line x1="{gx:.2f}" y1="{pad_t}" x2="{gx:.2f}" y2="{pad_t+plot_h}" class="q1-year-marker" />')
            grid.append(f'<text x="{gx+4:.2f}" y="{pad_t+12}" class="q1-year-tag">{row["month"][:4]}</text>')

    dots = []
    for i, (px, py) in enumerate(pts):
        cls = 'q1-point q1-point-emphasis' if i >= len(pts) - 3 else 'q1-point'
        r = 4.8 if i >= len(pts) - 3 else 3.1
        row = series[i]
        tooltip_currency = currency or ''
        tooltip_value = f"{tooltip_currency} {fmt_value(row['po_value'])}".strip()
        month_label = f"{row['month'][:4]}-{row['month'][5:7]}"
        dots.append(
            f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r}" class="{cls}" '
            f'data-month="{month_label}" data-count="{row["po_count"]}" data-value="{row["po_value"]:.2f}" '
            f'data-currency="{tooltip_currency}" data-count-label="{fmt_count(row["po_count"])}" '
            f'data-value-label="{tooltip_value}" data-metric="{metric}" />'
        )

    last = pts[-1]
    last_v = values[-1]
    label_text = fmt_count(last_v) if metric == 'po_count' else f"{currency} {fmt_value(last_v)}"
    label_x = min(last[0] + 12, width - 30)
    label_y = max(last[1] - 12, 36)
    accent = 'teal' if metric == 'po_count' else 'amber'
    stroke = 'var(--teal)' if metric == 'po_count' else 'var(--amber)'
    return f'''
<svg viewBox="0 0 {width} {height}" class="q1-chart-svg" role="img" aria-label="Monthly {metric.replace('_',' ')} chart">
  <defs>
    <linearGradient id="{metric}-fill" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="{stroke}" stop-opacity="0.28" />
      <stop offset="100%" stop-color="{stroke}" stop-opacity="0.02" />
    </linearGradient>
  </defs>
  <g>{''.join(grid)}</g>
  <path d="{area}" fill="url(#{metric}-fill)" />
  <path d="{line}" fill="none" stroke="{stroke}" stroke-width="2.75" stroke-linecap="round" stroke-linejoin="round" />
  <g>{''.join(dots)}</g>
  <g>
    <circle cx="{last[0]:.2f}" cy="{last[1]:.2f}" r="7" class="q1-point-final q1-point-final-{accent}" />
    <text x="{label_x:.2f}" y="{label_y:.2f}" class="q1-last-label">{label_text}</text>
  </g>
</svg>'''


def q1_section(code, c):
    series = monthly[code]
    q1 = c['q1_2026']
    comps = c['comparisons']
    baseline = c['baseline']
    assessment = c['assessment']
    forecast = c['forecast_2026']
    currency = c['currency']
    chart_count = line_chart_svg(series, 'po_count', currency=currency)
    chart_value = line_chart_svg(series, 'po_value', currency=currency)

    compare_cards = []
    for year in ['2025', '2024', '2023']:
        comp = comps[year]
        compare_cards.append(f'''
          <article class="q1-compare-card">
            <div class="q1-compare-label">Vs Q1 {year}</div>
            <div class="q1-compare-value">{fmt_count(comp['q1_po_count'])} POs</div>
            <div class="q1-compare-sub">{currency} {fmt_value(comp['q1_po_value'])}</div>
            <div class="q1-compare-delta"><span class="{delta_class(comp['po_count_pct_change'])}">{sign_pct(comp['po_count_pct_change'])}</span> count <span class="q1-dot">•</span> <span class="{delta_class(comp['po_value_pct_change'])}">{sign_pct(comp['po_value_pct_change'])}</span> value</div>
          </article>''')
    compare_cards.append(f'''
          <article class="q1-compare-card q1-compare-forecast">
            <div class="q1-compare-label">2026 forecast</div>
            <div class="q1-compare-value">{fmt_count(forecast['po_count'])} POs</div>
            <div class="q1-compare-sub">{currency} {fmt_value(forecast['po_value'])}</div>
            <div class="q1-compare-delta"><span class="q1-forecast-method">{forecast['method']}</span></div>
            <div class="q1-compare-delta"><span class="{delta_class(forecast['po_count_vs_2025_pct'])}">{sign_pct(forecast['po_count_vs_2025_pct'])}</span> vs 2025 count <span class="q1-dot">•</span> <span class="{delta_class(forecast['po_value_vs_2025_pct'])}">{sign_pct(forecast['po_value_vs_2025_pct'])}</span> vs 2025 value</div>
          </article>''')

    return f'''
  <!-- Q1-2026-PULSE-START -->
  <section class="section q1-section" style="background:var(--bg-primary);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">Q1 2026 pulse</div>
      <h2 class="section-title reveal reveal-delay-1">Monthly PO count + value, with Jan–Mar comparisons</h2>
      <p class="section-subtitle reveal reveal-delay-2">Native currency only, not FX-normalized. Counts and values use completed / valid POs only; rejected and PO-cancelled entries are excluded. The view below combines the full monthly series from Jan 2023 to Mar 2026 with the Q1 2026 comparison set and a directional full-year forecast.</p>

      <div class="q1-shell reveal reveal-delay-3">
        <div class="q1-summary-panel">
          <div class="q1-summary-top">
            <div>
              <div class="q1-eyebrow">Current readout</div>
              <div class="q1-status-badge {chip_class(assessment['label'])}">{assessment['label']}</div>
            </div>
            <div class="q1-baseline-chip">
              <span class="q1-baseline-label">Q1 median 2023–2025</span>
              <strong>{fmt_count(baseline['po_count'])} POs</strong>
              <span>{currency} {fmt_value(baseline['po_value'])}</span>
            </div>
          </div>
          <div class="q1-summary-copy">{assessment['summary']}</div>
          <div class="q1-metric-strip">
            <div class="q1-metric"><span>Q1 2026 POs</span><strong>{fmt_count(q1['po_count'])}</strong></div>
            <div class="q1-metric"><span>Q1 2026 value</span><strong>{currency} {fmt_value(q1['po_value'])}</strong></div>
            <div class="q1-metric"><span>vs Q1 2025</span><strong class="{delta_class(comps['2025']['po_count_pct_change'])}">{sign_pct(comps['2025']['po_count_pct_change'])} count</strong><small class="{delta_class(comps['2025']['po_value_pct_change'])}">{sign_pct(comps['2025']['po_value_pct_change'])} value</small></div>
          </div>
        </div>

        <div class="q1-chart-grid">
          <article class="q1-chart-card">
            <div class="q1-chart-header">
              <div>
                <div class="q1-chart-title">Monthly PO count</div>
                <div class="q1-chart-subtitle">Jan 2023 → Mar 2026</div>
              </div>
              <div class="q1-chart-pill">Q1 2026: {fmt_count(q1['po_count'])} POs</div>
            </div>
            {chart_count}
          </article>
          <article class="q1-chart-card">
            <div class="q1-chart-header">
              <div>
                <div class="q1-chart-title">Monthly PO value</div>
                <div class="q1-chart-subtitle">Jan 2023 → Mar 2026</div>
              </div>
              <div class="q1-chart-pill">Q1 2026: {currency} {fmt_value(q1['po_value'])}</div>
            </div>
            {chart_value}
          </article>
        </div>

        <div class="q1-compare-grid">
          {''.join(compare_cards)}
        </div>

        <div class="q1-caveat"><strong>Caveat:</strong> values are native-market currency only and are not FX-normalized. The monthly series and comparisons exclude rejected and PO-cancelled entries. The 2026 forecast annualizes Q1 2026 using the average Q1 share of annual totals from 2023-2025, so treat it as directional planning input rather than a promise.</div>
      </div>
    </div>
  </section>
  <!-- Q1-2026-PULSE-END -->
'''


def annual_section(code, c):
    currency = c['currency']
    totals = c['totals']
    forecast_2026 = c['forecast_2026_value']
    values = [totals['2023'], totals['2024'], totals['2025'], forecast_2026]
    max_value = max(values) if values else 1
    year_cards = []
    card_specs = [
        ('2023', 'Base year', totals['2023'], None, False),
        ('2024', f"vs 2023: {sign_pct((totals['2024'] / totals['2023'] - 1) * 100) if totals['2023'] else '—'}", totals['2024'], (totals['2024'] / totals['2023'] - 1) * 100 if totals['2023'] else 0, False),
        ('2025', f"vs 2024: {sign_pct((totals['2025'] / totals['2024'] - 1) * 100) if totals['2024'] else '—'}", totals['2025'], (totals['2025'] / totals['2024'] - 1) * 100 if totals['2024'] else 0, False),
        ('Forecast 2026', f"Annualized from Q1 2026 • vs 2025: {sign_pct((forecast_2026 / totals['2025'] - 1) * 100) if totals['2025'] else '—'}", forecast_2026, (forecast_2026 / totals['2025'] - 1) * 100 if totals['2025'] else 0, True),
    ]
    for label, sub, value, delta, is_forecast in card_specs:
        pct_width = max(4, round((value / max_value) * 100)) if max_value else 4
        delta_html = '<span class="q1-forecast-method">Annualized from Q1 2026 using the average Q1 share of annual totals from 2023-2025.</span>' if is_forecast else (
            '<span class="delta-flat">Base year</span>' if delta is None else f'<span class="{delta_class(delta)}">{sign_pct(delta)}</span> vs prior year'
        )
        year_cards.append(f'''
          <article class="q1-compare-card {'q1-compare-forecast' if is_forecast else ''}">
            <div class="q1-compare-label">{label}</div>
            <div class="q1-compare-value">{compact_currency(value, currency)}</div>
            <div class="q1-compare-sub">{sub}</div>
            <div class="annual-bar"><span style="width:{pct_width}%"></span></div>
            <div class="q1-compare-delta">{delta_html}</div>
          </article>''')

    return f'''
  <section class="section annual-section" style="background:var(--bg-deep);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">Annual PO value comparison</div>
      <h2 class="section-title reveal reveal-delay-1">2023 vs 2024 vs 2025 vs Forecast 2026</h2>
      <p class="section-subtitle reveal reveal-delay-2">Native currency only, not FX-normalized. Annual totals use the same completed / valid PO baseline, excluding rejected and PO-cancelled entries. 2026 is projected by annualizing Q1 2026 using the average Q1 share of annual totals from 2023-2025.</p>
      <div class="q1-compare-grid reveal reveal-delay-3">
        {''.join(year_cards)}
      </div>
      <div class="q1-caveat reveal reveal-delay-4"><strong>Method:</strong> annual totals come from the full Jan-Dec monthly series for 2023-2025 using the cleaned completed-PO baseline. Forecast 2026 uses the same Q1-share annualization logic as the Q1 pulse, but applied to annual value only.</div>
    </div>
  </section>'''

for code, c in analysis_by_code.items():
    page = ROOT / code / 'index.html'
    text = page.read_text()
    new_block = q1_section(code, c) + '\n' + annual_section(code, annual[code])
    if '<!-- Q1-2026-PULSE-START -->' in text:
        text = re.sub(r'\n  <!-- Q1-2026-PULSE-START -->.*?<!-- Q1-2026-PULSE-END -->\n', '\n' + new_block + '\n', text, flags=re.S)
    else:
        marker = '\n  <section class="section story">'
        if marker not in text:
            raise SystemExit(f'Could not find insertion marker in {page}')
        text = text.replace(marker, '\n' + new_block + marker, 1)
    page.write_text(text)
    print('updated', page)
