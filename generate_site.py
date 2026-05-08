from pathlib import Path
import json

ROOT = Path('/data/.openclaw/workspace-vibe-agent/dhl-singapore-opportunity')

countries = {
    'sg': {
        'flag': '🇸🇬', 'name': 'Singapore', 'code': 'SG',
        'observed_total': 175.0,
        'observed_label': '~SGD 175K',
        'observed_note': 'Approximate, aligned to the Jan-Dec 2025 dashboard screenshot for (SG) (DHL). Exact chart-reading may vary slightly.',
        'potential_total': 900.0,
        'story': 'Singapore appears meaningfully under-captured relative to the operating complexity of a premium-cost market handling customer service, office operations, facility upkeep, and day-to-day consumables.',
        'categories': [
            ('IT Accessories & Equipment', 42),
            ('MRO', 28),
            ('Events (Food)', 24),
            ('Office & Pantry Supplies', 20),
            ('MRO Services', 16),
            ('Customized Events', 12),
            ('Gifts/Promotions (Vouchers)', 10),
            ('Others', 9),
            ('Uniforms', 7),
            ('Medical Supplies', 4),
            ('Creative Services', 3),
        ],
        'products': [
            {'icon':'🎧','title':'Jabra headsets for customer support teams','category':'IT Accessories & Equipment','estimate':'SGD 35K-55K','logic':'150-220 agents × 1 headset every 24-30 months × SGD 220-320 per unit','note':'A concrete DHL-relevant subcategory that often sits behind generic IT accessories spend.'},
            {'icon':'👞','title':'Safety shoes for warehouse and ramp staff','category':'Uniforms / Safety','estimate':'SGD 18K-30K','logic':'180-250 frontline staff × 1-1.5 pairs per year × SGD 80-120 per pair','note':'Observed uniforms spend alone rarely reflects the broader PPE/safety footwear need.'},
            {'icon':'📄','title':'Office paper and copy paper','category':'Office & Pantry Supplies','estimate':'SGD 10K-18K','logic':'30-50 cartons per month × SGD 28-32 × 12 months','note':'Still relevant in logistics environments with manifests, labels, admin printing, and dispatch paperwork.'},
            {'icon':'🖨️','title':'Printer toner cartridges','category':'Office / IT Print','estimate':'SGD 12K-24K','logic':'20-40 devices × 3-5 cartridge sets per year × SGD 180-260 per set','note':'Useful proof-point for how print spend hides inside office and IT categories.'},
            {'icon':'🧰','title':'Hand tools, tapes, adhesives, facility consumables','category':'MRO','estimate':'SGD 40K-70K','logic':'Multiple facilities × monthly replenishment for engineering and operations teams','note':'Often fragmented across many low-ticket purchases, making under-capture easy.'},
            {'icon':'🥪','title':'Shift meals, meetings, and training catering','category':'Events (Food)','estimate':'SGD 35K-60K','logic':'8-15 events or training sessions per month × SGD 300-450 average ticket × 12 months','note':'Food tends to be more recurring than one-off event budgets suggest.'},
        ]
    },
    'cn': {
        'flag': '🇨🇳', 'name': 'China', 'code': 'CN',
        'observed_total': 1013.6363, 'observed_label': 'SGD 1.01M',
        'observed_note': 'Observed actual based on transcribed Jan-Dec 2025 dashboard values provided by the user.',
        'potential_total': 4500.0,
        'story': 'China already shows the largest observed spend base in the set, but the mix still suggests substantial untapped share in operational categories that should scale with a national logistics footprint.',
        'categories': [
            ('Office & Pantry Supplies', 281.45637), ('IT Accessories & Equipment', 192.26047), ('Events (Food)', 152.78482),
            ('MRO', 146.87045), ('MRO Services', 87.84059), ('Medical Supplies', 53.2), ('Gifts/Promotions (Vouchers)', 52.97961),
            ('Others', 29.57943), ('Customized Events', 13.86584), ('Creative Services', 2.30476), ('Uniforms', 0.49396),
        ],
        'products': [
            {'icon':'🧻','title':'Janitorial paper, pantry restock, washroom consumables','category':'Office & Pantry Supplies','estimate':'SGD 250K-400K','logic':'Large multi-site footprint × recurring monthly consumables × high-frequency replenishment','note':'China’s observed office/pantry base is already large, suggesting this is a real procurement lane with room to widen share.'},
            {'icon':'💻','title':'Monitors, docking stations, keyboards, mice','category':'IT Accessories & Equipment','estimate':'SGD 180K-320K','logic':'1,500-2,500 office and support users × staggered refresh cycles × accessory bundles','note':'Observed spend is meaningful, but hardware accessories still look under-represented for national scale.'},
            {'icon':'🎫','title':'Meal support, town halls, employee event catering','category':'Events (Food)','estimate':'SGD 200K-350K','logic':'Distributed site events + team engagement + training sessions across the year','note':'Food spend often expands with frequency of ops-led gatherings more than with event size alone.'},
            {'icon':'🔧','title':'Warehouse maintenance consumables and repair parts','category':'MRO','estimate':'SGD 350K-550K','logic':'Conveyors, dock equipment, packaging lines, facility consumables, electrical items','note':'Operational environments typically generate a broader long-tail than observed dashboards show.'},
            {'icon':'🥾','title':'Safety shoes and PPE','category':'Uniforms / Safety','estimate':'SGD 60K-120K','logic':'500-900 frontline staff × 1-2 replacements per year × SGD 90-130 per set','note':'Uniforms are nearly absent in the observed file, which is likely a routing or taxonomy issue rather than true lack of demand.'},
            {'icon':'🎁','title':'Employee recognition and campaign gift sets','category':'Gifts/Promotions','estimate':'SGD 90K-160K','logic':'Seasonal campaigns + milestone awards + corporate gifting across major sites','note':'Observed voucher spend indicates a live budget that can broaden into physical gift and promo packs.'},
        ]
    },
    'jp': {
        'flag': '🇯🇵', 'name': 'Japan', 'code': 'JP',
        'observed_total': 603.92809, 'observed_label': 'SGD 604K',
        'observed_note': 'Observed actual based on transcribed dashboard values provided by the user.',
        'potential_total': 3500.0,
        'story': 'Japan shows a credible observed base in office, IT, and MRO, but still looks light once mapped against a high-cost, service-intensive market where replacement standards and service quality are typically higher.',
        'categories': [
            ('Office & Pantry Supplies', 167.12977), ('IT Accessories & Equipment', 158.43220), ('MRO', 113.79490), ('Events (Food)', 78.30217),
            ('MRO Services', 26.35061), ('Medical Supplies', 23.79394), ('Gifts/Promotions (Vouchers)', 20.15136), ('Others', 10.38057),
            ('Customized Events', 3.70661), ('Creative Services', 1.88245), ('Uniforms', 0.00351),
        ],
        'products': [
            {'icon':'🖥️','title':'Business monitors and docking setups','category':'IT Accessories & Equipment','estimate':'SGD 140K-240K','logic':'600-900 desks × 20-25% annual refresh equivalent × SGD 900-1,100 bundles','note':'Japan’s IT spend is already visible, but peripherals often scale faster than core devices.'},
            {'icon':'🖨️','title':'Printer toner and managed print consumables','category':'Office / IT Print','estimate':'SGD 30K-55K','logic':'30-50 network printers × regular cartridge rotation × premium market pricing','note':'A concrete subcategory that helps explain office + IT overlap.'},
            {'icon':'🧰','title':'Engineering consumables and replacement parts','category':'MRO','estimate':'SGD 220K-360K','logic':'Service level expectations + preventive maintenance + high-cost vendor environment','note':'Japan’s higher service standards often support a bigger MRO wallet than observed alone suggests.'},
            {'icon':'🥪','title':'Training and internal event catering','category':'Events (Food)','estimate':'SGD 90K-140K','logic':'Monthly management, training, and engagement events × higher local unit costs','note':'The observed food category is real, but likely not fully representative.'},
            {'icon':'👞','title':'Frontline safety footwear and PPE refresh','category':'Uniforms / Safety','estimate':'SGD 25K-45K','logic':'200-300 eligible staff × annual refresh × SGD 110-150 set values','note':'Observed uniforms are near zero, which looks more like untracked scope than zero demand.'},
        ]
    },
    'au': {
        'flag': '🇦🇺', 'name': 'Australia', 'code': 'AU',
        'observed_total': 486.00406, 'observed_label': 'SGD 486K',
        'observed_note': 'Observed actual based on transcribed dashboard values provided by the user.',
        'potential_total': 2200.0,
        'story': 'Australia carries a broad-based spend pattern across MRO, office supplies, food, and IT, but the absolute level still looks modest relative to the cost base and operational breadth of the market.',
        'categories': [
            ('MRO', 113.61211), ('Office & Pantry Supplies', 90.93139), ('MRO Services', 79.65948), ('Events (Food)', 61.50028),
            ('IT Accessories & Equipment', 48.68950), ('Gifts/Promotions (Vouchers)', 40.27695), ('Customized Events', 26.13848), ('Others', 22.29510),
            ('Medical Supplies', 1.92529), ('Creative Services', 0.83499), ('Uniforms', 0.14049),
        ],
        'products': [
            {'icon':'🔩','title':'Maintenance parts, sealants, tapes, fasteners','category':'MRO','estimate':'SGD 180K-300K','logic':'Facility intensity × high local labor and material costs × recurring replenishment','note':'Australia’s observed MRO base already signals a real lane worth deepening.'},
            {'icon':'🛠️','title':'Preventive maintenance call-outs and on-site services','category':'MRO Services','estimate':'SGD 120K-220K','logic':'Scheduled service contracts + reactive repairs across multiple sites','note':'Service-led categories often widen once procurement consolidates vendors.'},
            {'icon':'☕','title':'Pantry beverages, cleaning consumables, washroom supplies','category':'Office & Pantry Supplies','estimate':'SGD 130K-220K','logic':'Mid-size workforce × monthly recurring restock × premium market prices','note':'A dependable category for share expansion because consumption is non-discretionary.'},
            {'icon':'🎧','title':'Headsets and collaboration accessories','category':'IT Accessories & Equipment','estimate':'SGD 45K-80K','logic':'150-250 support users × 2-3 year refresh × SGD 220-320 per kit','note':'Useful wedge into the broader IT accessories wallet.'},
            {'icon':'👷','title':'Safety footwear and high-visibility PPE','category':'Uniforms / Safety','estimate':'SGD 22K-40K','logic':'120-180 frontline staff × annual issue/replacement × SGD 120-170','note':'Observed uniforms are too low to represent true operational need.'},
        ]
    },
    'my': {
        'flag': '🇲🇾', 'name': 'Malaysia', 'code': 'MY',
        'observed_total': 358.71611, 'observed_label': 'SGD 359K',
        'observed_note': 'Observed actual based on transcribed dashboard values provided by the user.',
        'potential_total': 1800.0,
        'story': 'Malaysia shows healthy activity in food, gifts, office supplies, and events, but the total still points to under-penetration in core operational categories for a national logistics operation.',
        'categories': [
            ('Events (Food)', 79.76274), ('Office & Pantry Supplies', 65.46879), ('Gifts/Promotions (Vouchers)', 57.01040), ('IT Accessories & Equipment', 46.18292),
            ('Customized Events', 44.06136), ('MRO Services', 26.63053), ('Creative Services', 14.36284), ('Others', 14.09649), ('MRO', 11.01801), ('Medical Supplies', 0.12203),
        ],
        'products': [
            {'icon':'🥤','title':'Pantry drinks, paper goods, and washroom consumables','category':'Office & Pantry Supplies','estimate':'SGD 90K-150K','logic':'300-500 staff supported across offices and operations sites × monthly recurring restock','note':'A practical category where share expansion can happen quickly.'},
            {'icon':'🍱','title':'Training meals, town halls, and festive event catering','category':'Events (Food)','estimate':'SGD 110K-180K','logic':'Regular internal events + cultural calendar peaks + distributed site activity','note':'Malaysia’s observed food base suggests this category already has momentum.'},
            {'icon':'🎁','title':'Festive gift packs and employee reward kits','category':'Gifts/Promotions','estimate':'SGD 70K-120K','logic':'Hari Raya, year-end, recognition campaigns, customer gifts','note':'Voucher-heavy observed spend can often widen into curated physical merchandise programs.'},
            {'icon':'🎧','title':'Customer service headsets and desk accessories','category':'IT Accessories & Equipment','estimate':'SGD 30K-55K','logic':'120-180 users × 24-30 month cycle × SGD 220-300 per kit','note':'A strong concrete example that makes the IT category feel operationally real.'},
            {'icon':'👞','title':'Safety shoes and essential PPE','category':'Uniforms / Safety','estimate':'SGD 20K-35K','logic':'150-220 eligible staff × annual replacement × SGD 80-110','note':'This need is operationally plausible even if not clearly visible in observed dashboard categories.'},
        ]
    },
    'id': {
        'flag': '🇮🇩', 'name': 'Indonesia', 'code': 'ID',
        'observed_total': 197.11206, 'observed_label': 'SGD 197K',
        'observed_note': 'Observed actual based on transcribed dashboard values provided by the user.',
        'potential_total': 1300.0,
        'story': 'Indonesia shows meaningful spend in pantry, food, MRO, and MRO services, but still appears far below the likely total category wallet for a dispersed, labor-intensive logistics market.',
        'categories': [
            ('Office & Pantry Supplies', 60.54677), ('Events (Food)', 52.15426), ('MRO', 25.35760), ('MRO Services', 18.75608), ('Medical Supplies', 11.49421),
            ('IT Accessories & Equipment', 9.59627), ('Customized Events', 8.92008), ('Gifts/Promotions (Vouchers)', 7.25253), ('Others', 2.97216), ('Creative Services', 0.06210),
        ],
        'products': [
            {'icon':'📦','title':'Packing station consumables and facility sundries','category':'MRO / Operations','estimate':'SGD 80K-140K','logic':'High-volume operations × recurring line-side consumables × many small purchase events','note':'Indonesia often hides spend in fragmented operational buying.'},
            {'icon':'☕','title':'Pantry and janitorial restock','category':'Office & Pantry Supplies','estimate':'SGD 85K-140K','logic':'Multiple operating sites × monthly recurring consumption','note':'Observed pantry spend is already one of the clearest proof points.'},
            {'icon':'🍛','title':'Team meals and training catering','category':'Events (Food)','estimate':'SGD 70K-120K','logic':'Frequent shift, training, and engagement moments across the year','note':'Recurring food spend can be larger than event-budget framing suggests.'},
            {'icon':'🩹','title':'First-aid refills and occupational health consumables','category':'Medical Supplies','estimate':'SGD 18K-35K','logic':'Site safety compliance + cabinet refills + incident readiness','note':'Medical is already visible, suggesting a solid opening for a structured offer.'},
            {'icon':'👞','title':'Safety shoes for frontline personnel','category':'Uniforms / Safety','estimate':'SGD 18K-32K','logic':'200-320 staff × 1 pair per year × SGD 75-100','note':'Useful modeled example even though uniforms are not explicitly broken out in the observed set.'},
        ]
    },
    'in': {
        'flag': '🇮🇳', 'name': 'India', 'code': 'IN',
        'observed_total': 186.63606, 'observed_label': 'SGD 187K',
        'observed_note': 'Observed actual based on transcribed dashboard values provided by the user.',
        'potential_total': 1800.0,
        'story': 'India’s observed spend is dominated by vouchers, which makes the current view feel unusually narrow. For a large and distributed market, the non-voucher categories look notably underrepresented.',
        'categories': [
            ('Gifts/Promotions (Vouchers)', 135.61368), ('Events (Food)', 12.01778), ('Others', 11.92197), ('Office & Pantry Supplies', 9.45165), ('MRO', 9.35868),
            ('IT Accessories & Equipment', 6.97287), ('MRO Services', 0.72824), ('Customized Events', 0.49609), ('Medical Supplies', 0.04042), ('Uniforms', 0.03468),
        ],
        'products': [
            {'icon':'🎁','title':'Voucher programs and recognition packs','category':'Gifts/Promotions','estimate':'SGD 160K-260K','logic':'Observed voucher base plus seasonal peaks and wider employee campaign coverage','note':'This is the one lane already strongly visible in the observed data.'},
            {'icon':'🎧','title':'Contact center headsets and desk accessories','category':'IT Accessories & Equipment','estimate':'SGD 55K-90K','logic':'250-400 support users × 24-30 month cycle × SGD 180-260 kits','note':'India’s IT accessories line looks disproportionately small for likely support headcount.'},
            {'icon':'🧰','title':'Facility consumables and warehouse maintenance items','category':'MRO','estimate':'SGD 110K-190K','logic':'Multi-site ops footprint × monthly replenishment × fragmented local buying','note':'A likely blind spot if procurement is decentralized.'},
            {'icon':'📄','title':'Copy paper, stationery, and admin consumables','category':'Office Supplies','estimate':'SGD 45K-75K','logic':'Corporate/admin support + recurring print and paper demand','note':'Even digitized environments retain meaningful office supply consumption.'},
            {'icon':'👞','title':'Safety shoes and basic PPE','category':'Uniforms / Safety','estimate':'SGD 25K-45K','logic':'250-350 frontline staff × annual issue/replacement × SGD 70-100','note':'Observed uniforms are effectively zero, which is unlikely to reflect actual need.'},
        ]
    },
    'th': {
        'flag': '🇹🇭', 'name': 'Thailand', 'code': 'TH',
        'observed_total': 12.31278, 'observed_label': 'SGD 12K',
        'observed_note': 'Observed actual based on transcribed dashboard values provided by the user.',
        'potential_total': 500.0,
        'story': 'Thailand is the starkest under-capture case in the set. The observed file is so small that it likely reflects partial visibility rather than true category demand.',
        'categories': [
            ('MRO', 3.59576), ('Office & Pantry Supplies', 2.83969), ('Customized Events', 2.56372), ('IT Accessories & Equipment', 1.51308), ('Events (Food)', 0.89705), ('Gifts/Promotions (Vouchers)', 0.69589), ('Others', 0.18201), ('Medical Supplies', 0.02558),
        ],
        'products': [
            {'icon':'🔧','title':'Basic facility maintenance consumables','category':'MRO','estimate':'SGD 50K-90K','logic':'Even a modest logistics operation requires steady MRO replenishment','note':'The current observed base is too small to represent true operational demand.'},
            {'icon':'🧻','title':'Pantry, paper, and washroom consumables','category':'Office & Pantry Supplies','estimate':'SGD 45K-80K','logic':'Monthly restock across office and operations sites','note':'A reliable, recurring category that almost certainly exists beyond the dashboard view.'},
            {'icon':'🎧','title':'Headsets and desktop accessories','category':'IT Accessories & Equipment','estimate':'SGD 20K-35K','logic':'60-120 users × 2-3 year refresh × SGD 220-300 kits','note':'Useful concrete drilldown for a category that otherwise sounds abstract.'},
            {'icon':'🥪','title':'Training and event catering','category':'Events (Food)','estimate':'SGD 18K-35K','logic':'Monthly internal events, management meetings, and training sessions','note':'Food is usually more recurring than the observed figure suggests.'},
            {'icon':'👞','title':'Safety shoes and protective basics','category':'Uniforms / Safety','estimate':'SGD 12K-20K','logic':'80-140 eligible staff × annual refresh × SGD 80-100','note':'Modeled example to make the opportunity tangible.'},
        ]
    }
}

category_multiplier = {
    'IT Accessories & Equipment': 5.0,
    'MRO': 4.5,
    'MRO Services': 4.0,
    'Office & Pantry Supplies': 3.2,
    'Events (Food)': 2.8,
    'Customized Events': 4.0,
    'Gifts/Promotions (Vouchers)': 2.5,
    'Others': 2.8,
    'Uniforms': 10.0,
    'Medical Supplies': 3.0,
    'Creative Services': 3.5,
}

for code, c in countries.items():
    cats = []
    for name, observed in c['categories']:
        potential = max(observed * category_multiplier.get(name, 3.0), observed * 1.25)
        cats.append({'name': name, 'observed': observed, 'potential': potential})
    scale = c['potential_total'] / sum(x['potential'] for x in cats)
    for x in cats:
        x['potential'] = round(x['potential'] * scale, 1)
    cats = sorted(cats, key=lambda x: x['potential'] - x['observed'], reverse=True)
    gap_total = round(sum(x['potential'] - x['observed'] for x in cats), 1)
    capture = round(c['observed_total'] / c['potential_total'] * 100)
    c['cats_processed'] = cats
    c['gap_total'] = gap_total
    c['capture'] = capture


def fmt_k(v):
    if v >= 1000:
        s = f"{v/1000:.1f}".rstrip('0').rstrip('.')
        return f"SGD {s}M"
    if abs(v - round(v)) < 0.05:
        return f"SGD {round(v)}K"
    return f"SGD {v:.1f}K"


def rel_prefix(code):
    return '..' if code else '.'


def make_country_page(code, c):
    top3 = c['cats_processed'][:3]
    product_cards = '\n'.join([
        f'''<div class="product-card reveal reveal-delay-{(i%5)+1}">\n  <div class="product-card-header">\n    <div class="product-card-icon">{p['icon']}</div>\n    <div>\n      <div class="product-card-title">{p['title']}</div>\n      <div class="product-card-cat">{p['category']}</div>\n    </div>\n  </div>\n  <div class="product-card-body">\n    <div class="product-card-estimate">{p['estimate']}</div>\n    <p style="font-size:14px;color:var(--text-secondary);line-height:1.6;">{p['note']}</p>\n    <div class="product-card-logic"><span class="logic-label">Directional spend logic</span>{p['logic']}</div>\n  </div>\n</div>'''
        for i, p in enumerate(c['products'])
    ])
    cat_rows = '\n'.join([
        f"<tr><td style='color:var(--text-muted);font-family:var(--font-mono);font-size:12px;'>{i+1}</td><td class='cat-name'>{x['name']}</td><td class='cat-observed' style='text-align:right'>{fmt_k(x['observed'])}</td><td class='cat-potential' style='text-align:right'>{fmt_k(x['potential'])}</td><td class='cat-gap' style='text-align:right'>{fmt_k(round(x['potential']-x['observed'],1))}</td><td class='cat-capture {'capture-high' if x['observed']/x['potential']>0.5 else 'capture-med' if x['observed']/x['potential']>0.3 else 'capture-low'}' style='text-align:right'>{(x['observed']/x['potential']*100):.1f}%</td></tr>"
        for i, x in enumerate(c['cats_processed'])
    ])
    categories_json = json.dumps(c['cats_processed'])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Missed Opportunities — DHL {c['name']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300..700&family=Playfair+Display:wght@400..900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <nav class="nav" id="nav">
    <div class="nav-inner">
      <a href="../index.html" class="nav-brand">
        <div class="nav-brand-icon">SS</div>
        <span>SourceSage — Opportunity Intelligence</span>
      </a>
      <div style="display:flex;align-items:center;gap:16px;">
        <a href="../index.html" class="nav-back">← All countries</a>
        <div class="nav-tag">DHL {c['name']}</div>
      </div>
    </div>
  </nav>

  <section class="hero">
    <div class="hero-grid"></div>
    <div class="container hero-content">
      <div class="hero-eyebrow reveal">Country Analysis — DHL {c['name']}</div>
      <h1 class="hero-title reveal reveal-delay-1">Missed <em>Opportunities</em><br>with DHL {c['name']}</h1>
      <p class="hero-description reveal reveal-delay-2">{c['story']}</p>
      <div class="hero-stats reveal reveal-delay-3">
        <div class="hero-stat"><div class="hero-stat-value">{len(c['categories'])}</div><div class="hero-stat-label">Categories Analyzed</div></div>
        <div class="hero-stat"><div class="hero-stat-value teal">{c['observed_label']}</div><div class="hero-stat-label">Observed Spend</div></div>
        <div class="hero-stat"><div class="hero-stat-value amber">{fmt_k(c['potential_total'])}</div><div class="hero-stat-label">Directional Potential</div></div>
        <div class="hero-stat"><div class="hero-stat-value red">{c['capture']}%</div><div class="hero-stat-label">Estimated Capture</div></div>
      </div>
      <div class="disclaimer-banner reveal reveal-delay-4" style="max-width:900px;margin-top:24px;">
        <div class="icon">⚠️</div>
        <p><strong>Observed vs modeled.</strong> {c['observed_note']} Potential and gap figures are directional assumptions, not factual audited totals.</p>
      </div>
    </div>
    <div class="scroll-indicator"><span>Scroll</span><div class="scroll-arrow"></div></div>
  </section>

  <section class="section story">
    <div class="container">
      <div class="story-content">
        <div class="story-text reveal">
          <div class="section-label">Executive Read</div>
          <h2 class="section-title">What the observed mix suggests</h2>
          <p>The dashboard shows <strong>{c['observed_label']}</strong> of visible spend across {len(c['categories'])} tracked categories for DHL {c['name']}.</p>
          <p>That is useful as an anchor, but not as the full wallet. The more important question is whether the current category mix looks complete for a DHL operation in this market. In our view, it does not.</p>
          <p>The biggest white space tends to sit not only at category level, but one layer deeper: <strong>specific product families</strong> like headsets, safety shoes, paper, toner, pantry consumables, and facility maintenance items.</p>
        </div>
        <div class="reveal reveal-delay-2">
          <div class="story-highlight">
            <div class="story-highlight-number">{fmt_k(c['gap_total']).replace('SGD ','')}</div>
            <div class="story-highlight-text">Estimated annual gap between observed spend and a directional modeled wallet for DHL {c['name']}. This should be treated as <strong>commercial framing</strong>, not audited fact.</div>
          </div>
          <div class="disclaimer-banner" style="margin-top:20px;">
            <div class="icon">🧭</div>
            <p><strong>Directional assumptions.</strong> Country potential is modeled from category mix, market cost levels, and plausible operational scope. Where site-level actuals are unavailable, we do not present fabricated site splits.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section" style="background:var(--bg-primary);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">Key Metrics</div>
      <h2 class="section-title reveal reveal-delay-1">The spend gap at a glance</h2>
      <p class="section-subtitle reveal reveal-delay-2">Observed values come from the dashboard transcription. Potential values are directional and explicitly modeled.</p>
      <div class="insights-grid">
        <div class="insight-card observed reveal reveal-delay-1"><div class="insight-icon teal">📊</div><div class="insight-label">Observed Spend</div><div class="insight-value teal">{c['observed_label']}</div><div class="insight-note">Dashboard-aligned visible spend in the provided 2025 scope.</div></div>
        <div class="insight-card potential reveal reveal-delay-2"><div class="insight-icon amber">🎯</div><div class="insight-label">Directional Potential</div><div class="insight-value amber">{fmt_k(c['potential_total'])}</div><div class="insight-note">Modeled estimate of what the category wallet could plausibly look like.</div></div>
        <div class="insight-card gap reveal reveal-delay-3"><div class="insight-icon red">📉</div><div class="insight-label">Modeled Gap</div><div class="insight-value red">{fmt_k(c['gap_total'])}</div><div class="insight-note">White space between observed and modeled demand, intended for prioritization.</div></div>
      </div>
    </div>
  </section>

  <section class="section categories">
    <div class="container">
      <div class="section-label reveal">Category Breakdown</div>
      <h2 class="section-title reveal reveal-delay-1">Observed vs. directional potential by category</h2>
      <p class="section-subtitle reveal reveal-delay-2">Teal bars are observed dashboard values. Amber bars are directional modeled opportunity estimates to make the commercial discussion more concrete.</p>
      <div class="category-list reveal reveal-delay-3" id="categoryList"></div>
      <div class="bar-legend reveal reveal-delay-4"><div class="bar-legend-item"><div class="bar-legend-dot teal"></div><span>Observed</span></div><div class="bar-legend-item"><div class="bar-legend-dot amber"></div><span>Modeled potential</span></div></div>
    </div>
  </section>

  <section class="section top-opps">
    <div class="container">
      <div class="section-label reveal">What sits inside each category</div>
      <h2 class="section-title reveal reveal-delay-1">Product-level drilldowns that make the story real</h2>
      <p class="section-subtitle reveal reveal-delay-2">These examples show how abstract categories translate into concrete DHL-relevant buying needs.</p>
      <div class="product-grid">{product_cards}</div>
    </div>
  </section>

  <section class="section heatmap">
    <div class="container">
      <div class="section-label reveal">Detailed View</div>
      <h2 class="section-title reveal reveal-delay-1">Category opportunity table</h2>
      <p class="section-subtitle reveal reveal-delay-2">A ranked view of observed actuals against directional modeled potential.</p>
      <div style="overflow-x:auto;">
        <table class="heatmap-table reveal reveal-delay-3">
          <thead><tr><th style="width:24px">#</th><th>Category</th><th style="text-align:right">Observed</th><th style="text-align:right">Potential</th><th style="text-align:right">Gap</th><th style="text-align:right">Capture Rate</th></tr></thead>
          <tbody>{cat_rows}</tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="section assumptions">
    <div class="container">
      <div class="section-label reveal">Transparency</div>
      <h2 class="section-title reveal reveal-delay-1">Assumptions and limits</h2>
      <p class="section-subtitle reveal reveal-delay-2">This page deliberately separates what is observed from what is modeled.</p>
      <div class="assumptions-grid">
        <div class="assumption-item reveal reveal-delay-1"><h4>Observed data source <span class="assumption-badge">Actual</span></h4><p>Observed values are taken from the user-provided transcription of dashboard screenshots for DHL {c['name']}. Singapore uses an explicitly approximate observed anchor because the latest chart was described as slightly below SGD 180K rather than machine-readable exact.</p></div>
        <div class="assumption-item reveal reveal-delay-2"><h4>Modeled opportunity <span class="assumption-badge">Directional</span></h4><p>Potential values are estimated using category multipliers, local cost expectations, and operational logic. They are not claimed as factual DHL procurement totals.</p></div>
        <div class="assumption-item reveal reveal-delay-3"><h4>Product examples <span class="assumption-badge">Illustrative</span></h4><p>Highlighted examples such as Jabra headsets, safety shoes, office paper, and toner cartridges are used to make demand more concrete. They are examples of plausible subcategory demand, not confirmed DHL line items.</p></div>
        <div class="assumption-item reveal reveal-delay-4"><h4>No fabricated site actuals <span class="assumption-badge">Guardrail</span></h4><p>Where site-level actual data is not available from the source dashboards, this page avoids presenting site-level facts. Any future site split should be clearly labeled as modeled or illustrative unless sourced from DHL data.</p></div>
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="container">
      <div class="reveal">
        <div class="section-label" style="justify-content:center;">Bottom Line</div>
        <h2 class="cta-title">DHL {c['name']} looks <em>under-captured</em>.</h2>
        <p class="cta-text">The most credible next step is to use the observed dashboard categories as a wedge, then expand the discussion into concrete product families and replacement-cycle logic.</p>
        <div class="cta-amount">{fmt_k(c['gap_total'])}</div>
        <div class="cta-amount-label">Directional annual opportunity gap</div>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <div class="footer-text">SourceSage Opportunity Intelligence · DHL {c['name']} Analysis</div>
      <div class="footer-divider"></div>
      <div class="footer-text" style="font-size:11px;">Confidential — Internal discussion draft only. Observed values are dashboard-based; potential values are directional modeling.</div>
    </div>
  </footer>

  <script src="../shared.js"></script>
  <script>
    const categories = {categories_json};
    renderCategoryBars(categories, 'categoryList');
    initAll();
  </script>
</body>
</html>'''


def make_landing_page():
    total_obs = sum(c['observed_total'] for c in countries.values())
    total_pot = sum(c['potential_total'] for c in countries.values())
    cards = []
    order = ['cn','jp','au','my','id','in','sg','th']
    for code in order:
        c = countries[code]
        top = ', '.join([x[0] for x in sorted(c['categories'], key=lambda y: y[1], reverse=True)[:3]])
        width = round(c['observed_total']/c['potential_total']*100)
        cards.append(f'''<a href="{code}/index.html" class="country-card reveal">
          <div class="country-flag">{c['flag']}</div>
          <div class="country-card-name">{c['name']}</div>
          <div class="country-card-code">{c['code']}</div>
          <div class="country-card-stats">
            <div><div class="country-card-stat-value" style="color:var(--teal)">{c['observed_label']}</div><div class="country-card-stat-label">Observed</div></div>
            <div><div class="country-card-stat-value" style="color:var(--amber)">{fmt_k(c['potential_total'])}</div><div class="country-card-stat-label">Potential</div></div>
          </div>
          <div class="country-card-bar"><div class="country-card-bar-fill" style="width:{width}%"></div></div>
          <div class="country-card-categories">{len(c['categories'])} categories • Top observed: {top}</div>
        </a>''')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DHL APAC Opportunity Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300..700&family=Playfair+Display:wght@400..900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav class="nav" id="nav">
    <div class="nav-inner">
      <a href="index.html" class="nav-brand"><div class="nav-brand-icon">SS</div><span>SourceSage — Opportunity Intelligence</span></a>
      <div class="nav-tag">DHL APAC</div>
    </div>
  </nav>

  <section class="hero">
    <div class="hero-grid"></div>
    <div class="container hero-content">
      <div class="hero-eyebrow reveal">Regional Overview — DHL Asia-Pacific</div>
      <h1 class="hero-title reveal reveal-delay-1">Missed <em>Opportunities</em><br>Across DHL APAC</h1>
      <p class="hero-description reveal reveal-delay-2">A regional opportunity narrative built from user-provided 2025 dashboard transcriptions. Each country page starts with observed dashboard spend, then drills into concrete product families and directional opportunity logic.</p>
      <div class="agg-stats reveal reveal-delay-3">
        <div class="agg-stat"><div class="agg-stat-value" style="color:var(--amber)">{len(countries)}</div><div class="agg-stat-label">Countries analyzed</div></div>
        <div class="agg-stat"><div class="agg-stat-value" style="color:var(--teal)">{fmt_k(total_obs)}</div><div class="agg-stat-label">Observed spend</div></div>
        <div class="agg-stat"><div class="agg-stat-value" style="color:var(--amber)">{fmt_k(total_pot)}</div><div class="agg-stat-label">Directional potential</div></div>
        <div class="agg-stat"><div class="agg-stat-value" style="color:var(--red-soft)">{round((1-total_obs/total_pot)*100)}%</div><div class="agg-stat-label">Modeled gap</div></div>
      </div>
      <div class="disclaimer-banner reveal reveal-delay-4" style="max-width:920px;margin-top:24px;"><div class="icon">⚠️</div><p><strong>Transparency first.</strong> Observed values come from dashboard screenshots transcribed by the user. Potential values are directional modeling only. We avoid claiming site-level facts where the source data does not provide them.</p></div>
    </div>
    <div class="scroll-indicator"><span>Scroll</span><div class="scroll-arrow"></div></div>
  </section>

  <section class="section" style="background:var(--bg-primary);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">Country Pages</div>
      <h2 class="section-title reveal reveal-delay-1">Pick a DHL market</h2>
      <p class="section-subtitle reveal reveal-delay-2">Every page uses the same executive storytelling structure: observed dashboard actuals, category white space, concrete product examples, and clearly labeled directional assumptions.</p>
      <div class="country-grid">{''.join(cards)}</div>
    </div>
  </section>

  <section class="section story">
    <div class="container">
      <div class="story-content">
        <div class="story-text reveal">
          <div class="section-label">What changes in this version</div>
          <h2 class="section-title">From categories to believable product demand</h2>
          <p>The first-pass story was mostly category-level. This second pass goes one layer deeper: what actually sits inside each category.</p>
          <p>That means turning generic buckets into concrete buying logic: <strong>Jabra headsets for support staff, safety shoes for frontline teams, office paper, printer toner cartridges, pantry consumables, and facility maintenance items.</strong></p>
          <p>This makes the opportunity narrative more credible because it mirrors how procurement conversations actually happen.</p>
        </div>
        <div class="reveal reveal-delay-2">
          <div class="story-highlight">
            <div class="story-highlight-number">8</div>
            <div class="story-highlight-text">country pages built around the same executive structure, each adapted to its observed spend mix and each separating <strong>dashboard actuals</strong> from <strong>directional modeled upside</strong>.</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <div class="footer-text">SourceSage Opportunity Intelligence · DHL APAC</div>
      <div class="footer-divider"></div>
      <div class="footer-text" style="font-size:11px;">Confidential — Internal discussion only. Not for external circulation without validation.</div>
    </div>
  </footer>

  <script src="shared.js"></script>
  <script>initAll();</script>
</body>
</html>'''

ROOT.joinpath('index.html').write_text(make_landing_page())
for code, c in countries.items():
    d = ROOT / code
    d.mkdir(exist_ok=True)
    d.joinpath('index.html').write_text(make_country_page(code, c))

summary = {k: {'observed_total_k': v['observed_total'], 'potential_total_k': v['potential_total'], 'gap_total_k': v['gap_total']} for k, v in countries.items()}
ROOT.joinpath('site-data.json').write_text(json.dumps(summary, indent=2))
print('generated', len(countries), 'country pages')
