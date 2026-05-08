#!/usr/bin/env python3
"""DHL APAC Opportunity Intelligence — v3 generator
Adds: Hong Kong market, site-by-site opportunity model (archetype framework).
Regenerates all pages."""

from pathlib import Path
import json, html as H

ROOT = Path('/data/.openclaw/workspace-vibe-agent/dhl-singapore-opportunity')

# ────────────────────────────────────────────────────────────
# SITE ARCHETYPE MODEL  (modeled framework — NOT actual site spend)
# ────────────────────────────────────────────────────────────
site_archetypes = [
    {
        'id': 'hq',
        'icon': '🏢',
        'name': 'Country HQ / Office',
        'desc': 'Corporate headquarters, regional offices, back-office administration. Typically 50–300 desk-based staff.',
        'products': [
            {'icon': '🎧', 'family': 'IT Accessories', 'examples': 'Jabra headsets, monitors, docking stations, keyboards, mice, webcams', 'intensity': 'high'},
            {'icon': '📄', 'family': 'Office Supplies', 'examples': 'Copy paper, toner cartridges, stationery, binders, envelopes', 'intensity': 'high'},
            {'icon': '🩹', 'family': 'Medical / First Aid', 'examples': 'Office first-aid kits, AED pads, masks', 'intensity': 'low'},
            {'icon': '🔧', 'family': 'MRO / Facilities', 'examples': 'Lighting, HVAC filters, cleaning supplies, janitorial', 'intensity': 'med'},
            {'icon': '👞', 'family': 'Safety / Uniforms', 'examples': 'Minimal — front-desk staff, building access PPE', 'intensity': 'low'},
        ]
    },
    {
        'id': 'cs',
        'icon': '🎧',
        'name': 'Customer Service / Control Tower',
        'desc': 'Contact centres, shipment monitoring, operations control rooms. High headset density, shift-based staffing.',
        'products': [
            {'icon': '🎧', 'family': 'IT Accessories', 'examples': 'Jabra/Poly headsets (core tool), monitors, docks, keyboards, mouse pads', 'intensity': 'high'},
            {'icon': '📄', 'family': 'Office Supplies', 'examples': 'Paper, toner, stationery for admin and print queues', 'intensity': 'med'},
            {'icon': '🩹', 'family': 'Medical / First Aid', 'examples': 'First-aid kits, ergonomic aids', 'intensity': 'low'},
            {'icon': '🔧', 'family': 'MRO / Facilities', 'examples': 'Office-grade HVAC, electrical, UPS maintenance', 'intensity': 'low'},
            {'icon': '👞', 'family': 'Safety / Uniforms', 'examples': 'Corporate uniforms/ID lanyards only', 'intensity': 'low'},
        ]
    },
    {
        'id': 'wh',
        'icon': '🏭',
        'name': 'Warehouse / Distribution Centre',
        'desc': 'Fulfilment centres, cross-dock facilities, bonded warehouses. Large frontline workforce, heavy equipment, compliance-driven.',
        'products': [
            {'icon': '📦', 'family': 'Warehouse Consumables', 'examples': 'Pallet wrap, labels, tape, cartons, barcode scanners, thermal ribbons', 'intensity': 'high'},
            {'icon': '👞', 'family': 'Safety / Uniforms', 'examples': 'Safety shoes, gloves, hi-vis vests, uniforms, hard hats, PPE', 'intensity': 'high'},
            {'icon': '🔧', 'family': 'MRO / Facilities', 'examples': 'Tools, lubricants, conveyor parts, janitorial, electrical consumables, forklift servicing', 'intensity': 'high'},
            {'icon': '🩹', 'family': 'Medical / First Aid', 'examples': 'First-aid kits, disposable gloves, masks, AED consumables, eyewash stations', 'intensity': 'med'},
            {'icon': '🎧', 'family': 'IT Accessories', 'examples': 'Rugged tablets, barcode scanners, a few office desks', 'intensity': 'low'},
            {'icon': '📄', 'family': 'Office Supplies', 'examples': 'Shipping labels, manifest paper, some admin stationery', 'intensity': 'low'},
        ]
    },
    {
        'id': 'gw',
        'icon': '✈️',
        'name': 'Gateway / Hub / Station',
        'desc': 'Airport gateways, sorting hubs, last-mile stations. Equipment-intensive, 24/7 operations, vehicle fleets.',
        'products': [
            {'icon': '🔧', 'family': 'MRO / Facilities', 'examples': 'Vehicle maintenance, ground equipment, HVAC servicing, electrical, dock repairs', 'intensity': 'high'},
            {'icon': '👞', 'family': 'Safety / Uniforms', 'examples': 'Safety shoes, hi-vis, gloves, ear protection, PPE for ramp/ground ops', 'intensity': 'high'},
            {'icon': '📦', 'family': 'Warehouse Consumables', 'examples': 'Labels, tape, packaging materials, ULD nets, strapping', 'intensity': 'med'},
            {'icon': '🩹', 'family': 'Medical / First Aid', 'examples': 'Compliance kits, AED consumables, occupational health supplies', 'intensity': 'med'},
            {'icon': '🎧', 'family': 'IT Accessories', 'examples': 'Ops desk IT, handheld scanners, some monitors', 'intensity': 'med'},
            {'icon': '📄', 'family': 'Office Supplies', 'examples': 'Minimal admin paper, manifest printing', 'intensity': 'low'},
        ]
    },
]

# Archetype × product family matrix for the landing page summary
archetype_matrix = {
    'families': ['IT Accessories', 'Office Supplies', 'Safety / Uniforms', 'Warehouse Consumables', 'MRO / Facilities', 'Medical / First Aid'],
    'archetypes': {
        'Country HQ / Office':             ['high', 'high', 'low',  'none', 'med',  'low'],
        'Customer Service / Control Tower': ['high', 'med',  'low',  'none', 'low',  'low'],
        'Warehouse / Distribution Centre':  ['low',  'low',  'high', 'high', 'high', 'med'],
        'Gateway / Hub / Station':          ['med',  'low',  'high', 'med',  'high', 'med'],
    }
}

# Approximate site counts per country (modeled, for illustrative purposes)
country_sites = {
    'sg': {'hq': 1, 'cs': 1, 'wh': 3, 'gw': 1, 'note': 'Compact city-state; concentrated footprint.'},
    'cn': {'hq': 1, 'cs': 2, 'wh': 15, 'gw': 8, 'note': 'Largest APAC network; multi-region distribution.'},
    'jp': {'hq': 1, 'cs': 1, 'wh': 8, 'gw': 5, 'note': 'Premium market; high service standard per site.'},
    'au': {'hq': 1, 'cs': 1, 'wh': 6, 'gw': 4, 'note': 'Geographically dispersed; high per-site cost base.'},
    'my': {'hq': 1, 'cs': 1, 'wh': 5, 'gw': 3, 'note': 'Growing hub between SG and broader SEA.'},
    'id': {'hq': 1, 'cs': 1, 'wh': 6, 'gw': 4, 'note': 'Archipelago logistics; many small stations.'},
    'in': {'hq': 1, 'cs': 2, 'wh': 10, 'gw': 6, 'note': 'Large, dispersed footprint; labor-intensive.'},
    'th': {'hq': 1, 'cs': 1, 'wh': 3, 'gw': 2, 'note': 'Moderate-scale Thai network.'},
    'hk': {'hq': 1, 'cs': 1, 'wh': 1, 'gw': 1, 'note': 'Small territory; DHL Asia-Pacific regional HQ functions.'},
}

# ────────────────────────────────────────────────────────────
# TREND DATA
# ────────────────────────────────────────────────────────────
trends = {
    'jp': {
        'trend_label': 'Rebound / expansion market',
        'trend_emoji': '📈',
        'trend_color': 'var(--green-soft)',
        'trend_summary': 'Japan surged in 2025 across IT, MRO, Events (Food), and Medical after a weak 2024. This looks like a reactivation story — momentum is live and worth reinforcing.',
        'trend_cats': {
            'IT Accessories & Equipment': (None, None, 158.4),
            'MRO': (None, None, 113.8),
            'Events (Food)': (None, None, 78.3),
            'Medical Supplies': (None, None, 23.8),
        }
    },
    'id': {
        'trend_label': 'IT reactivation opportunity',
        'trend_emoji': '🔄',
        'trend_color': 'var(--amber)',
        'trend_summary': 'IT Accessories collapsed from SGD 58K (2023) to 9.6K (2025). MRO partially recovered. Events (Food) grew to 52K. The IT lane is the clearest reactivation target.',
        'trend_cats': {
            'IT Accessories & Equipment': (58.0, 24.0, 9.6),
            'MRO': (49.0, 9.6, 25.4),
            'Events (Food)': (None, None, 52.2),
        }
    },
    'th': {
        'trend_label': 'Turnaround market — small scale',
        'trend_emoji': '⚠️',
        'trend_color': 'var(--red-soft)',
        'trend_summary': 'Thailand saw major collapses: Events (Food) fell from 54.8K to under 1K; Gifts from 9.3K to 0.7K. IT peaked in 2024 then dropped to 1.5K. A turnaround market, but total scale remains very small.',
        'trend_cats': {
            'Events (Food)': (29.1, 54.8, 0.9),
            'Gifts/Promotions (Vouchers)': (9.3, 1.9, 0.7),
            'IT Accessories & Equipment': (None, None, 1.5),
        }
    },
    'cn': {
        'trend_label': 'Major expansion market',
        'trend_emoji': '🚀',
        'trend_color': 'var(--green-soft)',
        'trend_summary': 'China is the strongest multi-year growth story in the portfolio. IT ramped 35K → 167K → 192K. Events (Food) went from zero to 153K. MRO from 1K to 147K. Medical from 3K to 53K. Every major lane is expanding.',
        'trend_cats': {
            'IT Accessories & Equipment': (34.9, 166.8, 192.3),
            'Events (Food)': (0, 39.4, 152.8),
            'MRO': (1.0, 96.8, 146.9),
            'Medical Supplies': (2.8, 13.3, 53.2),
        }
    },
    'in': {
        'trend_label': 'Voucher-led market — cross-sell potential',
        'trend_emoji': '🎁',
        'trend_color': 'var(--amber)',
        'trend_summary': 'India exploded from near-zero to SGD 136K in Gifts/Vouchers alone. Events (Food) and MRO are growing but still small. The opportunity is to cross-sell operational categories off the voucher relationship.',
        'trend_cats': {
            'Gifts/Promotions (Vouchers)': (0, 3.9, 135.6),
            'Events (Food)': (None, None, 12.0),
            'MRO': (None, None, 9.4),
        }
    },
    'au': {
        'trend_label': 'Large but volatile wallet',
        'trend_emoji': '📊',
        'trend_color': 'var(--amber)',
        'trend_summary': 'Australia\'s MRO spiked from 103K to 679K in 2024, then corrected to 114K in 2025. The wallet is large across Events (Food) 62K, Gifts 40K, and IT 49K — but MRO volatility suggests project-based spending patterns.',
        'trend_cats': {
            'MRO': (103.0, 678.6, 113.6),
            'Events (Food)': (None, None, 61.5),
            'Gifts/Promotions (Vouchers)': (None, None, 40.3),
            'IT Accessories & Equipment': (None, None, 48.7),
        }
    },
    'my': {
        'trend_label': 'Mixed recovery — operational base growing',
        'trend_emoji': '🔀',
        'trend_color': 'var(--amber)',
        'trend_summary': 'Malaysia is strong in Events (Food) 80K, Gifts 57K, and IT 46K. MRO dropped from 47K to 11K. Customized Events rebounded from a 7.4K dip to 44K. A mixed pattern with growing operational engagement.',
        'trend_cats': {
            'Events (Food)': (None, None, 79.8),
            'Gifts/Promotions (Vouchers)': (None, None, 57.0),
            'IT Accessories & Equipment': (None, None, 46.2),
            'MRO': (46.9, None, 11.0),
            'Customized Events': (45.6, 7.4, 44.1),
        }
    },
    'sg': {
        'trend_label': 'Anchor market — needs baseline growth',
        'trend_emoji': '🏠',
        'trend_color': 'var(--teal)',
        'trend_summary': 'Singapore is the home market but observed spend is modest at ~SGD 175K. Multi-year trend detail is limited from the provided screenshots. The opportunity is about baseline category expansion.',
        'trend_cats': {}
    },
    'hk': {
        'trend_label': 'Micro-base market — early stage',
        'trend_emoji': '🔬',
        'trend_color': 'var(--text-muted)',
        'trend_summary': 'Hong Kong\'s observed spend totals just SGD 3.4K in 2025 — effectively a rounding error against regional peers. Medical Supplies collapsed from 4K (2024) to near-zero. Office & Pantry is the only lane showing consistent small growth. This is not currently a meaningful revenue market.',
        'trend_cats': {
            'Medical Supplies': (1.080, 4.025, 0.025),
            'Office & Pantry Supplies': (0.146, 1.385, 1.449),
            'IT Accessories & Equipment': (0, 0, 1.741),
        }
    },
}

# ────────────────────────────────────────────────────────────
# LOWEST-HANGING FRUIT
# ────────────────────────────────────────────────────────────
fruit_items = [
    {'icon': '☕', 'title': 'Office & Pantry Supplies', 'why': 'Non-discretionary, monthly recurring, high purchase frequency. Every site buys paper, pantry stock, and washroom consumables regardless of budget cycles.', 'signal': 'Already top-3 observed in CN, JP, AU, MY, ID. Easy to expand share.', 'tag': 'Recurring'},
    {'icon': '🎧', 'title': 'IT Accessories & Equipment', 'why': 'Headsets, monitors, keyboards have predictable refresh cycles (24-36 months). Demand scales with headcount.', 'signal': 'Strong growth in CN (35K→192K). Collapse in ID (58K→10K) = reactivation target.', 'tag': 'Refresh cycle'},
    {'icon': '🖨️', 'title': 'Printer consumables (toner, cartridges)', 'why': 'Sits inside Office or IT budgets but is a distinct, recurring purchase. Logistics environments still print heavily (manifests, labels, invoices).', 'signal': 'Hidden inside Office & Pantry line; usually under-counted.', 'tag': 'Hidden demand'},
    {'icon': '👞', 'title': 'Safety shoes, PPE & Uniforms', 'why': 'Compliance-driven, annual replacement cycle for frontline staff. Not optional — regulated in logistics.', 'signal': 'Observed uniforms spend is near-zero in most markets. Likely routed elsewhere or unsupplied.', 'tag': 'Compliance'},
    {'icon': '🔧', 'title': 'MRO consumables & services', 'why': 'Conveyor belts, dock equipment, facility maintenance. Operational necessity with fragmented buying patterns.', 'signal': 'AU spiked to 679K (2024); CN ramped 1K→147K. Real demand exists.', 'tag': 'Operational'},
]

# ────────────────────────────────────────────────────────────
# COUNTRY BASE DATA
# ────────────────────────────────────────────────────────────
countries = {
    'sg': {
        'flag': '🇸🇬', 'name': 'Singapore', 'code': 'SG',
        'observed_total': 112.5, 'observed_label': 'SGD 113K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 112,500 across all DHL entities. Note: SG data is API-driven on /sg page — this static value is fallback only.',
        'potential_total': 900.0,
        'story': 'Singapore appears meaningfully under-captured relative to the operating complexity of a premium-cost market handling customer service, office operations, facility upkeep, and day-to-day consumables.',
        'categories': [
            ('IT Accessories & Equipment', 42), ('MRO', 28), ('Events (Food)', 24), ('Office & Pantry Supplies', 20),
            ('MRO Services', 16), ('Customized Events', 12), ('Gifts/Promotions (Vouchers)', 10), ('Others', 9),
            ('Uniforms', 7), ('Medical Supplies', 4), ('Creative Services', 3),
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
        'observed_total': 597.6, 'observed_label': 'SGD 598K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 597,600 across all DHL entities.',
        'potential_total': 4500.0,
        'story': 'China already shows the largest observed spend base in the set, but the mix still suggests substantial untapped share in operational categories that should scale with a national logistics footprint.',
        'categories': [
            ('Office & Pantry Supplies', 281.456), ('IT Accessories & Equipment', 192.260), ('Events (Food)', 152.785),
            ('MRO', 146.870), ('MRO Services', 87.841), ('Medical Supplies', 53.2), ('Gifts/Promotions (Vouchers)', 52.980),
            ('Others', 29.579), ('Customized Events', 13.866), ('Creative Services', 2.305), ('Uniforms', 0.494),
        ],
        'products': [
            {'icon':'🧻','title':'Janitorial paper, pantry restock, washroom consumables','category':'Office & Pantry Supplies','estimate':'SGD 250K-400K','logic':'Large multi-site footprint × recurring monthly consumables × high-frequency replenishment','note':'China\'s observed office/pantry base is already large, suggesting this is a real procurement lane with room to widen share.'},
            {'icon':'💻','title':'Monitors, docking stations, keyboards, mice','category':'IT Accessories & Equipment','estimate':'SGD 180K-320K','logic':'1,500-2,500 office and support users × staggered refresh cycles × accessory bundles','note':'Observed spend is meaningful, but hardware accessories still look under-represented for national scale.'},
            {'icon':'🎫','title':'Meal support, town halls, employee event catering','category':'Events (Food)','estimate':'SGD 200K-350K','logic':'Distributed site events + team engagement + training sessions across the year','note':'Food spend often expands with frequency of ops-led gatherings more than with event size alone.'},
            {'icon':'🔧','title':'Warehouse maintenance consumables and repair parts','category':'MRO','estimate':'SGD 350K-550K','logic':'Conveyors, dock equipment, packaging lines, facility consumables, electrical items','note':'Operational environments typically generate a broader long-tail than observed dashboards show.'},
            {'icon':'🥾','title':'Safety shoes and PPE','category':'Uniforms / Safety','estimate':'SGD 60K-120K','logic':'500-900 frontline staff × 1-2 replacements per year × SGD 90-130 per set','note':'Uniforms are nearly absent in the observed file, which is likely a routing or taxonomy issue rather than true lack of demand.'},
            {'icon':'🎁','title':'Employee recognition and campaign gift sets','category':'Gifts/Promotions','estimate':'SGD 90K-160K','logic':'Seasonal campaigns + milestone awards + corporate gifting across major sites','note':'Observed voucher spend indicates a live budget that can broaden into physical gift and promo packs.'},
        ]
    },
    'jp': {
        'flag': '🇯🇵', 'name': 'Japan', 'code': 'JP',
        'observed_total': 475.7, 'observed_label': 'SGD 476K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 475,700 across all DHL entities.',
        'potential_total': 3500.0,
        'story': 'Japan shows a credible observed base in office, IT, and MRO, but still looks light once mapped against a high-cost, service-intensive market where replacement standards and service quality are typically higher.',
        'categories': [
            ('Office & Pantry Supplies', 167.130), ('IT Accessories & Equipment', 158.432), ('MRO', 113.795), ('Events (Food)', 78.302),
            ('MRO Services', 26.351), ('Medical Supplies', 23.794), ('Gifts/Promotions (Vouchers)', 20.151), ('Others', 10.381),
            ('Customized Events', 3.707), ('Creative Services', 1.882), ('Uniforms', 0.004),
        ],
        'products': [
            {'icon':'🖥️','title':'Business monitors and docking setups','category':'IT Accessories & Equipment','estimate':'SGD 140K-240K','logic':'600-900 desks × 20-25% annual refresh equivalent × SGD 900-1,100 bundles','note':'Japan\'s IT spend is already visible, but peripherals often scale faster than core devices.'},
            {'icon':'🖨️','title':'Printer toner and managed print consumables','category':'Office / IT Print','estimate':'SGD 30K-55K','logic':'30-50 network printers × regular cartridge rotation × premium market pricing','note':'A concrete subcategory that helps explain office + IT overlap.'},
            {'icon':'🧰','title':'Engineering consumables and replacement parts','category':'MRO','estimate':'SGD 220K-360K','logic':'Service level expectations + preventive maintenance + high-cost vendor environment','note':'Japan\'s higher service standards often support a bigger MRO wallet than observed alone suggests.'},
            {'icon':'🥪','title':'Training and internal event catering','category':'Events (Food)','estimate':'SGD 90K-140K','logic':'Monthly management, training, and engagement events × higher local unit costs','note':'The observed food category is real, but likely not fully representative.'},
            {'icon':'👞','title':'Frontline safety footwear and PPE refresh','category':'Uniforms / Safety','estimate':'SGD 25K-45K','logic':'200-300 eligible staff × annual refresh × SGD 110-150 set values','note':'Observed uniforms are near zero, which looks more like untracked scope than zero demand.'},
        ]
    },
    'au': {
        'flag': '🇦🇺', 'name': 'Australia', 'code': 'AU',
        'observed_total': 317.3, 'observed_label': 'SGD 317K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 317,300 across all DHL entities.',
        'potential_total': 2200.0,
        'story': 'Australia carries a broad-based spend pattern across MRO, office supplies, food, and IT, but the absolute level still looks modest relative to the cost base and operational breadth of the market.',
        'categories': [
            ('MRO', 113.612), ('Office & Pantry Supplies', 90.931), ('MRO Services', 79.660), ('Events (Food)', 61.500),
            ('IT Accessories & Equipment', 48.690), ('Gifts/Promotions (Vouchers)', 40.277), ('Customized Events', 26.138), ('Others', 22.295),
            ('Medical Supplies', 1.925), ('Creative Services', 0.835), ('Uniforms', 0.140),
        ],
        'products': [
            {'icon':'🔩','title':'Maintenance parts, sealants, tapes, fasteners','category':'MRO','estimate':'SGD 180K-300K','logic':'Facility intensity × high local labor and material costs × recurring replenishment','note':'Australia\'s observed MRO base already signals a real lane worth deepening.'},
            {'icon':'🛠️','title':'Preventive maintenance call-outs and on-site services','category':'MRO Services','estimate':'SGD 120K-220K','logic':'Scheduled service contracts + reactive repairs across multiple sites','note':'Service-led categories often widen once procurement consolidates vendors.'},
            {'icon':'☕','title':'Pantry beverages, cleaning consumables, washroom supplies','category':'Office & Pantry Supplies','estimate':'SGD 130K-220K','logic':'Mid-size workforce × monthly recurring restock × premium market prices','note':'A dependable category for share expansion because consumption is non-discretionary.'},
            {'icon':'🎧','title':'Headsets and collaboration accessories','category':'IT Accessories & Equipment','estimate':'SGD 45K-80K','logic':'150-250 support users × 2-3 year refresh × SGD 220-320 per kit','note':'Useful wedge into the broader IT accessories wallet.'},
            {'icon':'👷','title':'Safety footwear and high-visibility PPE','category':'Uniforms / Safety','estimate':'SGD 22K-40K','logic':'120-180 frontline staff × annual issue/replacement × SGD 120-170','note':'Observed uniforms are too low to represent true operational need.'},
        ]
    },
    'my': {
        'flag': '🇲🇾', 'name': 'Malaysia', 'code': 'MY',
        'observed_total': 341.7, 'observed_label': 'SGD 342K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 341,700 across all DHL entities.',
        'potential_total': 1800.0,
        'story': 'Malaysia shows healthy activity in food, gifts, office supplies, and events, but the total still points to under-penetration in core operational categories for a national logistics operation.',
        'categories': [
            ('Events (Food)', 79.763), ('Office & Pantry Supplies', 65.469), ('Gifts/Promotions (Vouchers)', 57.010), ('IT Accessories & Equipment', 46.183),
            ('Customized Events', 44.061), ('MRO Services', 26.631), ('Creative Services', 14.363), ('Others', 14.096), ('MRO', 11.018), ('Medical Supplies', 0.122),
        ],
        'products': [
            {'icon':'🥤','title':'Pantry drinks, paper goods, and washroom consumables','category':'Office & Pantry Supplies','estimate':'SGD 90K-150K','logic':'300-500 staff supported across offices and operations sites × monthly recurring restock','note':'A practical category where share expansion can happen quickly.'},
            {'icon':'🍱','title':'Training meals, town halls, and festive event catering','category':'Events (Food)','estimate':'SGD 110K-180K','logic':'Regular internal events + cultural calendar peaks + distributed site activity','note':'Malaysia\'s observed food base suggests this category already has momentum.'},
            {'icon':'🎁','title':'Festive gift packs and employee reward kits','category':'Gifts/Promotions','estimate':'SGD 70K-120K','logic':'Hari Raya, year-end, recognition campaigns, customer gifts','note':'Voucher-heavy observed spend can often widen into curated physical merchandise programs.'},
            {'icon':'🎧','title':'Customer service headsets and desk accessories','category':'IT Accessories & Equipment','estimate':'SGD 30K-55K','logic':'120-180 users × 24-30 month cycle × SGD 220-300 per kit','note':'A strong concrete example that makes the IT category feel operationally real.'},
            {'icon':'👞','title':'Safety shoes and essential PPE','category':'Uniforms / Safety','estimate':'SGD 20K-35K','logic':'150-220 eligible staff × annual replacement × SGD 80-110','note':'This need is operationally plausible even if not clearly visible in observed dashboard categories.'},
        ]
    },
    'id': {
        'flag': '🇮🇩', 'name': 'Indonesia', 'code': 'ID',
        'observed_total': 152.9, 'observed_label': 'SGD 153K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 152,900 across all DHL entities.',
        'potential_total': 1300.0,
        'story': 'Indonesia shows meaningful spend in pantry, food, MRO, and MRO services, but still appears far below the likely total category wallet for a dispersed, labor-intensive logistics market.',
        'categories': [
            ('Office & Pantry Supplies', 60.547), ('Events (Food)', 52.154), ('MRO', 25.358), ('MRO Services', 18.756), ('Medical Supplies', 11.494),
            ('IT Accessories & Equipment', 9.596), ('Customized Events', 8.920), ('Gifts/Promotions (Vouchers)', 7.253), ('Others', 2.972), ('Creative Services', 0.062),
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
        'observed_total': 142.4, 'observed_label': 'SGD 142K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 142,400 across all DHL entities.',
        'potential_total': 1800.0,
        'story': 'India\'s observed spend is dominated by vouchers, which makes the current view feel unusually narrow. For a large and distributed market, the non-voucher categories look notably underrepresented.',
        'categories': [
            ('Gifts/Promotions (Vouchers)', 135.614), ('Events (Food)', 12.018), ('Others', 11.922), ('Office & Pantry Supplies', 9.452), ('MRO', 9.359),
            ('IT Accessories & Equipment', 6.973), ('MRO Services', 0.728), ('Customized Events', 0.496), ('Medical Supplies', 0.040), ('Uniforms', 0.035),
        ],
        'products': [
            {'icon':'🎁','title':'Voucher programs and recognition packs','category':'Gifts/Promotions','estimate':'SGD 160K-260K','logic':'Observed voucher base plus seasonal peaks and wider employee campaign coverage','note':'This is the one lane already strongly visible in the observed data.'},
            {'icon':'🎧','title':'Contact center headsets and desk accessories','category':'IT Accessories & Equipment','estimate':'SGD 55K-90K','logic':'250-400 support users × 24-30 month cycle × SGD 180-260 kits','note':'India\'s IT accessories line looks disproportionately small for likely support headcount.'},
            {'icon':'🧰','title':'Facility consumables and warehouse maintenance items','category':'MRO','estimate':'SGD 110K-190K','logic':'Multi-site ops footprint × monthly replenishment × fragmented local buying','note':'A likely blind spot if procurement is decentralized.'},
            {'icon':'📄','title':'Copy paper, stationery, and admin consumables','category':'Office Supplies','estimate':'SGD 45K-75K','logic':'Corporate/admin support + recurring print and paper demand','note':'Even digitized environments retain meaningful office supply consumption.'},
            {'icon':'👞','title':'Safety shoes and basic PPE','category':'Uniforms / Safety','estimate':'SGD 25K-45K','logic':'250-350 frontline staff × annual issue/replacement × SGD 70-100','note':'Observed uniforms are effectively zero, which is unlikely to reflect actual need.'},
        ]
    },
    'th': {
        'flag': '🇹🇭', 'name': 'Thailand', 'code': 'TH',
        'observed_total': 4.1, 'observed_label': 'SGD 4.1K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 4,100 across all DHL entities.',
        'potential_total': 500.0,
        'story': 'Thailand is the starkest under-capture case in the set. The observed file is so small that it likely reflects partial visibility rather than true category demand.',
        'categories': [
            ('MRO', 3.596), ('Office & Pantry Supplies', 2.840), ('Customized Events', 2.564), ('IT Accessories & Equipment', 1.513), ('Events (Food)', 0.897), ('Gifts/Promotions (Vouchers)', 0.696), ('Others', 0.182), ('Medical Supplies', 0.026),
        ],
        'products': [
            {'icon':'🔧','title':'Basic facility maintenance consumables','category':'MRO','estimate':'SGD 50K-90K','logic':'Even a modest logistics operation requires steady MRO replenishment','note':'The current observed base is too small to represent true operational demand.'},
            {'icon':'🧻','title':'Pantry, paper, and washroom consumables','category':'Office & Pantry Supplies','estimate':'SGD 45K-80K','logic':'Monthly restock across office and operations sites','note':'A reliable, recurring category that almost certainly exists beyond the dashboard view.'},
            {'icon':'🎧','title':'Headsets and desktop accessories','category':'IT Accessories & Equipment','estimate':'SGD 20K-35K','logic':'60-120 users × 2-3 year refresh × SGD 220-300 kits','note':'Useful concrete drilldown for a category that otherwise sounds abstract.'},
            {'icon':'🥪','title':'Training and event catering','category':'Events (Food)','estimate':'SGD 18K-35K','logic':'Monthly internal events, management meetings, and training sessions','note':'Food is usually more recurring than the observed figure suggests.'},
            {'icon':'👞','title':'Safety shoes and protective basics','category':'Uniforms / Safety','estimate':'SGD 12K-20K','logic':'80-140 eligible staff × annual refresh × SGD 80-100','note':'Modeled example to make the opportunity tangible.'},
        ]
    },
    # ── HONG KONG (NEW) ──────────────────────────────────────
    'hk': {
        'flag': '🇭🇰', 'name': 'Hong Kong', 'code': 'HK',
        'observed_total': 1.9, 'observed_label': 'SGD 1.9K',
        'observed_note': 'Observed actual spend from SA data (Jan-Dec 2025). Total SGD 1,900 across all DHL entities — an extremely small base, likely reflecting limited platform adoption rather than zero purchasing activity.',
        'potential_total': 150.0,
        'story': 'Hong Kong\'s observed spend is effectively negligible at SGD 3.4K — far below any operational plausibility for a DHL market that hosts Asia-Pacific regional functions. The data most likely reflects minimal SourceSage platform adoption rather than absence of purchasing. This is a visibility gap, not a demand gap. The modeled potential is kept deliberately conservative.',
        'categories': [
            ('IT Accessories & Equipment', 1.741),
            ('Office & Pantry Supplies', 1.449),
            ('MRO', 0.197),
            ('Customized Events', 0.016),
            ('Medical Supplies', 0.025),
            ('Others', 0.0),
        ],
        'products': [
            {'icon':'🎧','title':'IT peripherals for office and regional HQ staff','category':'IT Accessories & Equipment','estimate':'SGD 15K-30K','logic':'50-120 desk-based staff × staggered refresh × SGD 300-500 per bundle','note':'HK hosts DHL APAC regional functions. Even a modest office generates real IT accessory demand. The SGD 1.7K observed is implausibly low.'},
            {'icon':'☕','title':'Office pantry, washroom, and paper supplies','category':'Office & Pantry Supplies','estimate':'SGD 8K-15K','logic':'Monthly recurring restock for office(s) × local premium pricing','note':'The observed SGD 1.4K could represent a single month or partial quarter, not full-year demand.'},
            {'icon':'🔧','title':'Office and facility maintenance consumables','category':'MRO / Facilities','estimate':'SGD 5K-12K','logic':'HVAC filters, lighting, cleaning, minor repairs for leased office space','note':'Even premium office environments generate recurring maintenance consumption.'},
            {'icon':'🩹','title':'First-aid kits and compliance consumables','category':'Medical Supplies','estimate':'SGD 2K-5K','logic':'Regulatory first-aid cabinets + annual refills across office(s)','note':'The collapse from SGD 4K (2024) to near-zero in 2025 suggests a procurement gap, not eliminated need.'},
        ]
    },
}

# ────────────────────────────────────────────────────────────
# HELPERS
# ────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────
# EXACT OBSERVED VALUES (from 2025 dashboard screenshots)
# Values are in actual SGD (not thousands)
# ────────────────────────────────────────────────────────────
observed_exact_values = {
    'cn': {
        'Creative Services': 2304.76,
        'Customized Events': 13865.84,
        'Events (Food)': 152784.82,
        'Gifts/Promotions (Vouchers)': 52979.61,
        'IT Accessories & Equipment': 192260.47,
        'Medical Supplies': 53200.00,
        'MRO': 146870.45,
        'MRO Services': 87840.59,
        'Office & Pantry Supplies': 281456.37,
        'Others': 29579.43,
        'Uniforms': 493.96,
    },
    'in': {
        'Customized Events': 496.09,
        'Events (Food)': 12017.78,
        'Gifts/Promotions (Vouchers)': 135613.68,
        'IT Accessories & Equipment': 6972.87,
        'Medical Supplies': 40.42,
        'MRO': 9358.68,
        'MRO Services': 728.24,
        'Office & Pantry Supplies': 9451.65,
        'Others': 11921.97,
        'Uniforms': 34.68,
    },
    'th': {
        'Customized Events': 2563.72,
        'Events (Food)': 897.05,
        'Gifts/Promotions (Vouchers)': 695.89,
        'IT Accessories & Equipment': 1513.08,
        'Medical Supplies': 25.58,
        'MRO': 3595.76,
        'Office & Pantry Supplies': 2839.69,
        'Others': 182.01,
    },
    'au': {
        'Creative Services': 834.99,
        'Customized Events': 26138.48,
        'Events (Food)': 61500.28,
        'Gifts/Promotions (Vouchers)': 40276.95,
        'IT Accessories & Equipment': 48689.50,
        'Medical Supplies': 1925.29,
        'MRO': 113612.11,
        'MRO Services': 79659.48,
        'Office & Pantry Supplies': 90931.39,
        'Others': 22295.10,
        'Uniforms': 140.49,
    },
    'my': {
        'Creative Services': 14362.84,
        'Customized Events': 44061.36,
        'Events (Food)': 79762.74,
        'Gifts/Promotions (Vouchers)': 57010.40,
        'IT Accessories & Equipment': 46182.92,
        'Medical Supplies': 122.03,
        'MRO': 11018.01,
        'MRO Services': 26630.53,
        'Office & Pantry Supplies': 65468.79,
        'Others': 14096.49,
    },
    'jp': {
        'Creative Services': 1882.45,
        'Customized Events': 3706.61,
        'Events (Food)': 78302.17,
        'Gifts/Promotions (Vouchers)': 20151.36,
        'IT Accessories & Equipment': 158432.20,
        'Medical Supplies': 23793.94,
        'MRO': 113794.90,
        'MRO Services': 26350.61,
        'Office & Pantry Supplies': 167129.77,
        'Others': 10380.57,
        'Uniforms': 3.51,
    },
    'id': {
        'Creative Services': 62.10,
        'Customized Events': 8920.08,
        'Events (Food)': 52154.26,
        'Gifts/Promotions (Vouchers)': 7252.53,
        'IT Accessories & Equipment': 9596.27,
        'Medical Supplies': 11494.21,
        'MRO': 25357.60,
        'MRO Services': 18756.08,
        'Office & Pantry Supplies': 60546.77,
        'Others': 2972.16,
    },
    'hk': {
        'Customized Events': 15.96,
        'IT Accessories & Equipment': 1741.38,
        'Medical Supplies': 24.88,
        'MRO': 197.14,
        'Office & Pantry Supplies': 1449.23,
        'Others': 0.00,
    },
    # SG: no exact category values available — keep approximate
}

category_multiplier = {
    'IT Accessories & Equipment': 5.0, 'MRO': 4.5, 'MRO Services': 4.0,
    'Office & Pantry Supplies': 3.2, 'Events (Food)': 2.8, 'Customized Events': 4.0,
    'Gifts/Promotions (Vouchers)': 2.5, 'Others': 2.8, 'Uniforms': 10.0,
    'Medical Supplies': 3.0, 'Creative Services': 3.5,
}

for code, c in countries.items():
    cats = []
    is_approx = code == 'sg'
    exact_map = observed_exact_values.get(code, {})
    for name, observed in c['categories']:
        potential = max(observed * category_multiplier.get(name, 3.0), observed * 1.25)
        exact_val = exact_map.get(name)
        cats.append({'name': name, 'observed': observed, 'potential': potential, 'observedExact': exact_val, 'isApproximate': is_approx})
    scale = c['potential_total'] / max(sum(x['potential'] for x in cats), 1)
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


def fmt_exact(v):
    """Format exact dollar value as SGD X,XXX.XX"""
    if v is None:
        return None
    return f"SGD {v:,.2f}"


# ────────────────────────────────────────────────────────────
# HTML BUILDERS
# ────────────────────────────────────────────────────────────

def build_trend_sparkline_html(cat_name, vals):
    y23, y24, y25 = vals
    points = []
    labels = []
    available = [(i, v) for i, v in enumerate([y23, y24, y25]) if v is not None]
    if len(available) < 2:
        return ''
    mx = max(v for _, v in available)
    if mx == 0:
        mx = 1
    for idx, val in available:
        x = idx * 40
        y = 36 - (val / mx * 30)
        points.append(f"{x},{y:.0f}")
        labels.append((x, y, val, ['2023','2024','2025'][idx]))
    pts = ' '.join(points)
    dots = ''.join(f'<circle cx="{x}" cy="{y:.0f}" r="2.5" fill="var(--amber)"/>' for x, y, _, _ in labels)
    txt = ''.join(f'<text x="{x}" y="48" fill="var(--text-muted)" font-size="8" text-anchor="middle">{yr}</text>' for x, _, _, yr in labels)
    val_txt = ''.join(f'<text x="{x}" y="{max(y-6,8):.0f}" fill="var(--text-secondary)" font-size="7.5" text-anchor="middle" font-family="var(--font-mono)">{v:.1f}K</text>' for x, y, v, _ in labels)
    return f'<svg viewBox="-4 -2 88 54" width="88" height="54" style="flex-shrink:0"><polyline points="{pts}" fill="none" stroke="var(--amber)" stroke-width="1.5" stroke-linejoin="round"/>{dots}{txt}{val_txt}</svg>'


def build_trend_section_country(code, t):
    if not t:
        return ''
    rows = ''
    for cat, vals in t['trend_cats'].items():
        spark = build_trend_sparkline_html(cat, vals)
        y23, y24, y25 = vals
        available = [v for v in [y23, y24, y25] if v is not None]
        if len(available) >= 2:
            if available[-1] > available[-2] * 1.15:
                arrow = '<span style="color:var(--green-soft);font-weight:600">↑ Rising</span>'
            elif available[-1] < available[-2] * 0.7:
                arrow = '<span style="color:var(--red-soft);font-weight:600">↓ Declining</span>'
            else:
                arrow = '<span style="color:var(--amber);font-weight:600">→ Flat/mixed</span>'
        else:
            arrow = '<span style="color:var(--text-muted)">—</span>'
        vals_str = ' → '.join([f"{'—' if v is None else f'{v:.1f}K'}" for v in [y23, y24, y25]])
        rows += f'''<div style="display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid var(--border);">
          {spark}
          <div style="flex:1;min-width:0;">
            <div style="font-size:14px;font-weight:500;color:var(--text-primary);">{H.escape(cat)}</div>
            <div style="font-family:var(--font-mono);font-size:12px;color:var(--text-secondary);margin-top:2px;">{vals_str}</div>
          </div>
          <div style="text-align:right;font-size:13px;">{arrow}</div>
        </div>'''

    return f'''
  <section class="section" style="background:var(--bg-primary);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">Multi-Year Trend</div>
      <h2 class="section-title reveal reveal-delay-1">2023 → 2024 → 2025 Trajectory</h2>
      <p class="section-subtitle reveal reveal-delay-2">Key category movements based on user-provided dashboard screenshots. The original rising / declining / flat category signals are preserved row by row, rather than being rewritten into a different storyline.</p>
      <div class="reveal reveal-delay-3" style="background:var(--bg-card);border:1px solid var(--border);border-radius:16px;padding:28px 32px;margin-top:36px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
          <span style="font-size:24px;">{t['trend_emoji']}</span>
          <div>
            <div style="font-size:16px;font-weight:600;color:{t['trend_color']}">{H.escape(t['trend_label'])}</div>
            <div style="font-size:14px;color:var(--text-secondary);line-height:1.6;margin-top:4px;">{H.escape(t['trend_summary'])}</div>
          </div>
        </div>
        <div>{rows}</div>
      </div>
      <div class="disclaimer-banner reveal reveal-delay-4" style="margin-top:20px;">
        <div class="icon">📋</div>
        <p><strong>Partial extraction.</strong> Trend values are drawn from key visible categories in the user-provided screenshots. Not every category had multi-year data available. Treat as directional signals, not audited time series.</p>
      </div>
    </div>
  </section>'''


def build_fruit_section():
    cards = ''
    for i, f in enumerate(fruit_items):
        cards += f'''<div class="product-card reveal reveal-delay-{(i%5)+1}">
          <div class="product-card-header">
            <div class="product-card-icon">{f['icon']}</div>
            <div>
              <div class="product-card-title">{H.escape(f['title'])}</div>
              <div class="product-card-cat">{H.escape(f['tag'])}</div>
            </div>
          </div>
          <div class="product-card-body">
            <p style="font-size:14px;color:var(--text-secondary);line-height:1.6;">{H.escape(f['why'])}</p>
            <div class="product-card-logic"><span class="logic-label">Market signal</span>{H.escape(f['signal'])}</div>
          </div>
        </div>'''
    return f'''
  <section class="section" style="background:var(--bg-deep);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">Lowest-Hanging Fruit</div>
      <h2 class="section-title reveal reveal-delay-1">Where to start: recurring, easy-conversion categories</h2>
      <p class="section-subtitle reveal reveal-delay-2">These five product families combine non-discretionary demand, predictable replacement cycles, and proven purchase patterns across the APAC portfolio. They convert faster than project-based or event-driven categories.</p>
      <div class="product-grid">{cards}</div>
    </div>
  </section>'''


def build_regional_trend_section():
    rows = ''
    order = [('cn','🚀','Major expansion','var(--green-soft)'),
             ('jp','📈','Rebound market','var(--green-soft)'),
             ('au','📊','Large but volatile','var(--amber)'),
             ('my','🔀','Mixed recovery','var(--amber)'),
             ('in','🎁','Voucher-led','var(--amber)'),
             ('id','🔄','IT reactivation','var(--amber)'),
             ('sg','🏠','Needs baseline growth','var(--teal)'),
             ('hk','🔬','Micro-base — early stage','var(--text-muted)'),
             ('th','⚠️','Turnaround — small scale','var(--red-soft)')]
    for code, emoji, label, color in order:
        c = countries[code]
        t = trends.get(code, {})
        summary = t.get('trend_summary', 'Limited multi-year data available.')
        cats_html = ''
        tc = t.get('trend_cats', {})
        highlights = []
        for cat, vals in list(tc.items())[:3]:
            avail = [v for v in vals if v is not None]
            if len(avail) >= 2:
                if avail[-1] > avail[0] * 1.5:
                    highlights.append(f'<span style="color:var(--green-soft)">↑</span> {H.escape(cat)}')
                elif avail[-1] < avail[0] * 0.5:
                    highlights.append(f'<span style="color:var(--red-soft)">↓</span> {H.escape(cat)}')
                else:
                    highlights.append(f'<span style="color:var(--amber)">→</span> {H.escape(cat)}')
            elif avail:
                highlights.append(f'{H.escape(cat)}')
        if highlights:
            cats_html = '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;">' + ''.join(f'<span style="font-size:12px;padding:3px 10px;background:var(--bg-subtle);border-radius:6px;color:var(--text-secondary)">{h}</span>' for h in highlights) + '</div>'

        rows += f'''<a href="{code}/index.html" class="reveal" style="display:block;background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:20px 24px;text-decoration:none;color:inherit;transition:border-color 0.3s,transform 0.3s;">
          <div style="display:flex;align-items:flex-start;gap:14px;">
            <span style="font-size:28px;">{countries[code]['flag']}</span>
            <div style="flex:1;min-width:0;">
              <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                <span style="font-size:16px;font-weight:600;color:var(--text-primary)">{countries[code]['name']}</span>
                <span style="font-family:var(--font-mono);font-size:10px;padding:2px 8px;border-radius:4px;background:rgba(245,158,11,0.08);color:{color}">{emoji} {H.escape(label)}</span>
                <span style="font-family:var(--font-mono);font-size:12px;color:var(--teal);margin-left:auto;">{c['observed_label']}</span>
              </div>
              <p style="font-size:13px;color:var(--text-secondary);line-height:1.5;margin-top:6px;">{H.escape(summary[:180])}</p>
              {cats_html}
            </div>
          </div>
        </a>'''
    return f'''
  <section class="section" style="background:var(--bg-deep);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">2023 → 2024 → 2025 Trends</div>
      <h2 class="section-title reveal reveal-delay-1">Multi-year trajectory by market</h2>
      <p class="section-subtitle reveal reveal-delay-2">Each market shows a distinct spending pattern. The original direction signals — rising, declining, or mixed — are kept intact from the dashboard extraction.</p>
      <div style="display:flex;flex-direction:column;gap:12px;margin-top:40px;">{rows}</div>
      <div class="disclaimer-banner reveal" style="margin-top:24px;"><div class="icon">📋</div><p><strong>Partial extraction.</strong> Multi-year data is drawn from selected high-signal categories across 2023, 2024, and 2025 dashboard screenshots. Not every category or year was available for every market.</p></div>
    </div>
  </section>'''


# ────────────────────────────────────────────────────────────
# SITE ARCHETYPE SECTION BUILDERS
# ────────────────────────────────────────────────────────────

def build_archetype_section_landing():
    """Build the site archetype overview for the landing page — matrix + card summary."""
    # Matrix table
    fams = archetype_matrix['families']
    header_cells = ''.join(f'<th style="text-align:center;min-width:80px;">{H.escape(f.split("/")[0].strip())}</th>' for f in fams)
    matrix_rows = ''
    dot_map = {'high': ('dot-high', '●'), 'med': ('dot-med', '●'), 'low': ('dot-low', '●'), 'none': ('dot-none', '○')}
    label_map = {'high': 'High', 'med': 'Medium', 'low': 'Low', 'none': '—'}
    for arch_name, intensities in archetype_matrix['archetypes'].items():
        cells = ''
        for intensity in intensities:
            cls, sym = dot_map[intensity]
            lbl = label_map[intensity]
            cells += f'<td style="text-align:center;"><span class="dot {cls}"></span><span style="font-size:11px;color:var(--text-muted)">{lbl}</span></td>'
        matrix_rows += f'<tr><td>{H.escape(arch_name)}</td>{cells}</tr>'

    # Archetype cards
    cards = ''
    for i, arch in enumerate(site_archetypes):
        prods_html = ''
        for p in arch['products'][:4]:
            int_cls = f'intensity-{p["intensity"]}'
            int_lbl = {'high': 'High', 'med': 'Medium', 'low': 'Low'}[p['intensity']]
            prods_html += f'''<div class="archetype-product-row">
              <div class="archetype-product-icon">{p['icon']}</div>
              <div class="archetype-product-info">
                <div class="archetype-product-name">{H.escape(p['family'])}</div>
                <div class="archetype-product-examples">{H.escape(p['examples'][:80])}</div>
              </div>
              <span class="archetype-intensity {int_cls}">{int_lbl}</span>
            </div>'''
        cards += f'''<div class="archetype-card reveal reveal-delay-{(i%4)+1}">
          <div class="archetype-card-header">
            <div class="archetype-icon {arch['id']}">{arch['icon']}</div>
            <div>
              <div class="archetype-name">{H.escape(arch['name'])}</div>
              <div class="archetype-desc">{H.escape(arch['desc'])}</div>
            </div>
          </div>
          <div class="archetype-products">{prods_html}</div>
        </div>'''

    return f'''
  <section class="section archetype-section" style="background:var(--bg-primary);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">Site-by-Site Opportunity Model</div>
      <h2 class="section-title reveal reveal-delay-1">What each DHL site type should be buying</h2>
      <p class="section-subtitle reveal reveal-delay-2">A modeled framework mapping product families to DHL site archetypes. This is not actual site-level spend data — it is a buying-propensity model based on operational logic.</p>
      <div class="disclaimer-banner reveal reveal-delay-3" style="margin-top:24px;margin-bottom:8px;">
        <div class="icon">🏗️</div>
        <p><strong>Modeled framework.</strong> The site counts and buying intensities below are illustrative archetypes, not sourced from DHL facility lists or actual site-level procurement records. Use this as a conversation tool for what <em>should</em> exist, not what currently does.</p>
      </div>

      <div style="overflow-x:auto;margin-top:36px;">
        <table class="archetype-matrix reveal reveal-delay-3">
          <thead><tr><th style="min-width:200px;">Site Archetype</th>{header_cells}</tr></thead>
          <tbody>{matrix_rows}</tbody>
        </table>
      </div>
      <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:16px;padding:12px 0;">
        <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-muted)"><span class="dot dot-high" style="display:inline-block;width:8px;height:8px;border-radius:50%;"></span> High — core buying need</div>
        <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-muted)"><span class="dot dot-med" style="display:inline-block;width:8px;height:8px;border-radius:50%;"></span> Medium — regular but secondary</div>
        <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-muted)"><span class="dot dot-low" style="display:inline-block;width:8px;height:8px;border-radius:50%;"></span> Low — occasional or minimal</div>
      </div>

      <div class="archetype-grid" style="margin-top:48px;">{cards}</div>
    </div>
  </section>'''


def build_archetype_section_country(code):
    """Build the site archetype section for a country page — contextualized site counts + product mapping."""
    c = countries[code]
    sites = country_sites.get(code, {})
    if not sites:
        return ''

    total_sites = sites.get('hq', 0) + sites.get('cs', 0) + sites.get('wh', 0) + sites.get('gw', 0)
    note = sites.get('note', '')

    # Site count summary
    site_pills = ''
    archetype_labels = {
        'hq': ('🏢', 'HQ / Office'),
        'cs': ('🎧', 'Customer Svc'),
        'wh': ('🏭', 'Warehouse / DC'),
        'gw': ('✈️', 'Gateway / Hub'),
    }
    for key, (icon, label) in archetype_labels.items():
        count = sites.get(key, 0)
        if count > 0:
            site_pills += f'''<div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:20px 24px;text-align:center;min-width:140px;">
              <div style="font-size:24px;margin-bottom:8px;">{icon}</div>
              <div style="font-family:var(--font-display);font-size:28px;font-weight:600;color:var(--amber);">~{count}</div>
              <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-top:4px;">{label}</div>
            </div>'''

    # Product family rows for each archetype relevant to this country
    archetype_details = ''
    for arch in site_archetypes:
        count = sites.get(arch['id'], 0)
        if count == 0:
            continue
        prods_html = ''
        for p in arch['products']:
            int_cls = f'intensity-{p["intensity"]}'
            int_lbl = {'high': 'High', 'med': 'Medium', 'low': 'Low'}[p['intensity']]
            prods_html += f'''<div class="archetype-product-row">
              <div class="archetype-product-icon">{p['icon']}</div>
              <div class="archetype-product-info">
                <div class="archetype-product-name">{H.escape(p['family'])}</div>
                <div class="archetype-product-examples">{H.escape(p['examples'])}</div>
              </div>
              <span class="archetype-intensity {int_cls}">{int_lbl}</span>
            </div>'''
        archetype_details += f'''<div class="archetype-card reveal">
          <div class="archetype-card-header">
            <div class="archetype-icon {arch['id']}">{arch['icon']}</div>
            <div>
              <div class="archetype-name">{H.escape(arch['name'])} <span style="font-family:var(--font-mono);font-size:13px;color:var(--amber);font-weight:400;">×~{count}</span></div>
              <div class="archetype-desc">{H.escape(arch['desc'])}</div>
            </div>
          </div>
          <div class="archetype-products">{prods_html}</div>
        </div>'''

    return f'''
  <section class="section archetype-section" style="background:var(--bg-primary);border-top:1px solid var(--border);">
    <div class="container">
      <div class="section-label reveal">Site-by-Site Opportunity Model</div>
      <h2 class="section-title reveal reveal-delay-1">Modeled site buying profile — {H.escape(c['name'])}</h2>
      <p class="section-subtitle reveal reveal-delay-2">An illustrative framework of what DHL sites in {H.escape(c['name'])} could plausibly be purchasing, mapped by site type. {H.escape(note)}</p>
      <div class="disclaimer-banner reveal reveal-delay-3" style="margin-top:24px;">
        <div class="icon">🏗️</div>
        <p><strong>This is a modeled framework, not actual site-level spend.</strong> Site counts are approximate. Product-family intensities are based on operational logic for each site type. No site-level procurement data from DHL was used to construct this view.</p>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:40px;justify-content:center;" class="reveal reveal-delay-3">
        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:20px 24px;text-align:center;min-width:140px;">
          <div style="font-size:24px;margin-bottom:8px;">📍</div>
          <div style="font-family:var(--font-display);font-size:28px;font-weight:600;color:var(--teal);">~{total_sites}</div>
          <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-top:4px;">Est. Total Sites</div>
        </div>
        {site_pills}
      </div>

      <div class="archetype-grid" style="margin-top:48px;">{archetype_details}</div>
    </div>
  </section>'''


# ────────────────────────────────────────────────────────────
# PAGE GENERATORS
# ────────────────────────────────────────────────────────────

def make_country_page(code, c):
    t = trends.get(code, {})
    product_cards = '\n'.join([
        f'''<div class="product-card reveal reveal-delay-{(i%5)+1}">
  <div class="product-card-header"><div class="product-card-icon">{p['icon']}</div><div><div class="product-card-title">{H.escape(p['title'])}</div><div class="product-card-cat">{H.escape(p['category'])}</div></div></div>
  <div class="product-card-body"><div class="product-card-estimate">{p['estimate']}</div><p style="font-size:14px;color:var(--text-secondary);line-height:1.6;">{H.escape(p['note'])}</p><div class="product-card-logic"><span class="logic-label">Directional spend logic</span>{H.escape(p['logic'])}</div></div>
</div>''' for i, p in enumerate(c['products'])
    ])
    def _obs_cell(x):
        ex = x.get('observedExact')
        if ex is not None:
            return f"<span class='exact-val'>{fmt_exact(ex)}</span>"
        elif x.get('isApproximate'):
            return f"<span class='approx-val'>~{fmt_k(x['observed'])}</span>"
        else:
            return fmt_k(x['observed'])
    cat_rows = '\n'.join([
        f"<tr><td style='color:var(--text-muted);font-family:var(--font-mono);font-size:12px;'>{i+1}</td><td class='cat-name'>{H.escape(x['name'])}</td><td class='cat-observed' style='text-align:right'>{_obs_cell(x)}</td><td class='cat-potential' style='text-align:right'>{fmt_k(x['potential'])}</td><td class='cat-gap' style='text-align:right'>{fmt_k(round(x['potential']-x['observed'],1))}</td><td class='cat-capture {'capture-high' if x['observed']/max(x['potential'],0.01)>0.5 else 'capture-med' if x['observed']/max(x['potential'],0.01)>0.3 else 'capture-low'}' style='text-align:right'>{(x['observed']/max(x['potential'],0.01)*100):.1f}%</td></tr>"
        for i, x in enumerate(c['cats_processed'])
    ])
    categories_json = json.dumps(c['cats_processed'])
    trend_section = build_trend_section_country(code, t)
    fruit_section = build_fruit_section()
    archetype_section = build_archetype_section_country(code)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Missed Opportunities — DHL {H.escape(c['name'])}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300..700&family=Playfair+Display:wght@400..900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <nav class="nav" id="nav"><div class="nav-inner"><a href="../index.html" class="nav-brand"><div class="nav-brand-icon">SS</div><span>SourceSage — Opportunity Intelligence</span></a><div style="display:flex;align-items:center;gap:16px;"><a href="../index.html" class="nav-back">← All countries</a><div class="nav-tag">DHL {H.escape(c['name'])}</div></div></div></nav>

  <section class="hero"><div class="hero-grid"></div><div class="container hero-content">
    <div class="hero-eyebrow reveal">Country Analysis — DHL {H.escape(c['name'])}</div>
    <h1 class="hero-title reveal reveal-delay-1">Missed <em>Opportunities</em><br>with DHL {H.escape(c['name'])}</h1>
    <p class="hero-description reveal reveal-delay-2">{H.escape(c['story'])}</p>
    <div class="hero-stats reveal reveal-delay-3">
      <div class="hero-stat"><div class="hero-stat-value">{len(c['categories'])}</div><div class="hero-stat-label">Categories Analyzed</div></div>
      <div class="hero-stat"><div class="hero-stat-value teal">{c['observed_label']}</div><div class="hero-stat-label">Observed Spend</div></div>
      <div class="hero-stat"><div class="hero-stat-value amber">{fmt_k(c['potential_total'])}</div><div class="hero-stat-label">Directional Potential</div></div>
      <div class="hero-stat"><div class="hero-stat-value red">{c['capture']}%</div><div class="hero-stat-label">Estimated Capture</div></div>
    </div>
    <div class="disclaimer-banner reveal reveal-delay-4" style="max-width:900px;margin-top:24px;"><div class="icon">⚠️</div><p><strong>Observed vs modeled.</strong> {H.escape(c['observed_note'])} Potential and gap figures are directional assumptions, not factual audited totals.</p></div>
  </div><div class="scroll-indicator"><span>Scroll</span><div class="scroll-arrow"></div></div></section>

  {trend_section}

  <section class="section story"><div class="container"><div class="story-content">
    <div class="story-text reveal">
      <div class="section-label">Executive Read</div>
      <h2 class="section-title">What the observed mix suggests</h2>
      <p>The dashboard shows <strong>{c['observed_label']}</strong> of visible spend across {len(c['categories'])} tracked categories for DHL {H.escape(c['name'])}.</p>
      <p>That is useful as an anchor, but not as the full wallet. The more important question is whether the current category mix looks complete for a DHL operation in this market. In our view, it does not.</p>
      <p>The biggest white space tends to sit not only at category level, but one layer deeper: <strong>specific product families</strong> like headsets, safety shoes, paper, toner, pantry consumables, and facility maintenance items.</p>
    </div>
    <div class="reveal reveal-delay-2">
      <div class="story-highlight"><div class="story-highlight-number">{fmt_k(c['gap_total']).replace('SGD ','')}</div><div class="story-highlight-text">Estimated annual gap between observed spend and a directional modeled wallet for DHL {H.escape(c['name'])}. This should be treated as <strong>commercial framing</strong>, not audited fact.</div></div>
      <div class="disclaimer-banner" style="margin-top:20px;"><div class="icon">🧭</div><p><strong>Directional assumptions.</strong> Country potential is modeled from category mix, market cost levels, and plausible operational scope. Where site-level actuals are unavailable, we do not present fabricated site splits.</p></div>
    </div>
  </div></div></section>

  <section class="section" style="background:var(--bg-primary);border-top:1px solid var(--border);"><div class="container">
    <div class="section-label reveal">Key Metrics</div>
    <h2 class="section-title reveal reveal-delay-1">The spend gap at a glance</h2>
    <p class="section-subtitle reveal reveal-delay-2">Observed values come from the dashboard transcription. Potential values are directional and explicitly modeled.</p>
    <div class="insights-grid">
      <div class="insight-card observed reveal reveal-delay-1"><div class="insight-icon teal">📊</div><div class="insight-label">Observed Spend</div><div class="insight-value teal">{c['observed_label']}</div><div class="insight-note">Dashboard-aligned visible spend in the provided 2025 scope.</div></div>
      <div class="insight-card potential reveal reveal-delay-2"><div class="insight-icon amber">🎯</div><div class="insight-label">Directional Potential</div><div class="insight-value amber">{fmt_k(c['potential_total'])}</div><div class="insight-note">Modeled estimate of what the category wallet could plausibly look like.</div></div>
      <div class="insight-card gap reveal reveal-delay-3"><div class="insight-icon red">📉</div><div class="insight-label">Modeled Gap</div><div class="insight-value red">{fmt_k(c['gap_total'])}</div><div class="insight-note">White space between observed and modeled demand, intended for prioritization.</div></div>
    </div>
  </div></section>

  <section class="section categories"><div class="container">
    <div class="section-label reveal">Category Breakdown</div>
    <h2 class="section-title reveal reveal-delay-1">Observed vs. directional potential by category</h2>
    <p class="section-subtitle reveal reveal-delay-2">Teal bars are observed dashboard values. Amber bars are directional modeled opportunity estimates.</p>
    <div class="category-list reveal reveal-delay-3" id="categoryList"></div>
    <div class="bar-legend reveal reveal-delay-4"><div class="bar-legend-item"><div class="bar-legend-dot teal"></div><span>Observed</span></div><div class="bar-legend-item"><div class="bar-legend-dot amber"></div><span>Modeled potential</span></div></div>
  </div></section>

  <section class="section top-opps"><div class="container">
    <div class="section-label reveal">What sits inside each category</div>
    <h2 class="section-title reveal reveal-delay-1">Product-level drilldowns</h2>
    <p class="section-subtitle reveal reveal-delay-2">Concrete product families that make the category narrative operationally real.</p>
    <div class="product-grid">{product_cards}</div>
  </div></section>

  {archetype_section}

  {fruit_section}

  <section class="section heatmap"><div class="container">
    <div class="section-label reveal">Detailed View</div>
    <h2 class="section-title reveal reveal-delay-1">Category opportunity table</h2>
    <div style="overflow-x:auto;"><table class="heatmap-table reveal reveal-delay-3"><thead><tr><th style="width:24px">#</th><th>Category</th><th style="text-align:right">Observed</th><th style="text-align:right">Potential</th><th style="text-align:right">Gap</th><th style="text-align:right">Capture Rate</th></tr></thead><tbody>{cat_rows}</tbody></table></div>
  </div></section>

  <section class="section assumptions"><div class="container">
    <div class="section-label reveal">Transparency</div>
    <h2 class="section-title reveal reveal-delay-1">Assumptions and limits</h2>
    <div class="assumptions-grid">
      <div class="assumption-item reveal reveal-delay-1"><h4>Observed data source <span class="assumption-badge">Actual</span></h4><p>Observed values from user-provided dashboard transcriptions for DHL {H.escape(c['name'])}.</p></div>
      <div class="assumption-item reveal reveal-delay-2"><h4>Modeled opportunity <span class="assumption-badge">Directional</span></h4><p>Potential values estimated using category multipliers, local cost expectations, and operational logic.</p></div>
      <div class="assumption-item reveal reveal-delay-3"><h4>Site archetype model <span class="assumption-badge">Framework</span></h4><p>Site types and product-family intensities are modeled archetypes — not sourced from actual DHL site-level procurement data.</p></div>
      <div class="assumption-item reveal reveal-delay-4"><h4>No fabricated site actuals <span class="assumption-badge">Guardrail</span></h4><p>Where site-level actual data is unavailable, this page uses a framework model instead of presenting fabricated site-level facts.</p></div>
    </div>
  </div></section>

  <section class="cta"><div class="container"><div class="reveal">
    <div class="section-label" style="justify-content:center;">Bottom Line</div>
    <h2 class="cta-title">DHL {H.escape(c['name'])} looks <em>under-captured</em>.</h2>
    <p class="cta-text">The most credible next step is to use the observed dashboard categories as a wedge, then expand the discussion into concrete product families and replacement-cycle logic.</p>
    <div class="cta-amount">{fmt_k(c['gap_total'])}</div>
    <div class="cta-amount-label">Directional annual opportunity gap</div>
  </div></div></section>

  <footer class="footer"><div class="container">
    <div class="footer-text">SourceSage Opportunity Intelligence · DHL {H.escape(c['name'])} Analysis</div>
    <div class="footer-divider"></div>
    <div class="footer-text" style="font-size:11px;">Confidential — Internal discussion draft only. Observed values are dashboard-based; potential values are directional modeling. Site archetype model is illustrative, not sourced from DHL facility data.</div>
  </div></footer>
  <script src="../shared.js"></script>
  <script>
    const categories = {categories_json};
    renderCategoryBars(categories, 'categoryList');
    initAll();
  </script>
</body></html>'''


def make_landing_page():
    total_obs = sum(c['observed_total'] for c in countries.values())
    total_pot = sum(c['potential_total'] for c in countries.values())
    cards = []
    order = ['cn','jp','au','my','id','in','sg','hk','th']
    for code in order:
        c = countries[code]
        t = trends.get(code, {})
        top = ', '.join([x[0] for x in sorted(c['categories'], key=lambda y: y[1], reverse=True)[:3]])
        width = round(c['observed_total']/c['potential_total']*100)
        trend_badge = ''
        if t:
            trend_badge = f'<span style="font-family:var(--font-mono);font-size:10px;padding:2px 8px;border-radius:4px;background:rgba(245,158,11,0.08);color:{t.get("trend_color","var(--amber)")}">{t.get("trend_emoji","")} {H.escape(t.get("trend_label",""))}</span>'
        cards.append(f'''<a href="{code}/index.html" class="country-card reveal">
          <div class="country-flag">{c['flag']}</div>
          <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;"><div class="country-card-name">{H.escape(c['name'])}</div>{trend_badge}</div>
          <div class="country-card-code">{c['code']}</div>
          <div class="country-card-stats">
            <div><div class="country-card-stat-value" style="color:var(--teal)">{c['observed_label']}</div><div class="country-card-stat-label">Observed</div></div>
            <div><div class="country-card-stat-value" style="color:var(--amber)">{fmt_k(c['potential_total'])}</div><div class="country-card-stat-label">Potential</div></div>
          </div>
          <div class="country-card-bar"><div class="country-card-bar-fill" style="width:{width}%"></div></div>
          <div class="country-card-categories">{len(c['categories'])} categories • Top: {H.escape(top)}</div>
        </a>''')

    regional_trend = build_regional_trend_section()
    fruit_section = build_fruit_section()
    archetype_section = build_archetype_section_landing()

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DHL APAC Opportunity Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300..700&family=Playfair+Display:wght@400..900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav class="nav" id="nav"><div class="nav-inner"><a href="index.html" class="nav-brand"><div class="nav-brand-icon">SS</div><span>SourceSage — Opportunity Intelligence</span></a><div class="nav-tag">DHL APAC</div></div></nav>

  <section class="hero"><div class="hero-grid"></div><div class="container hero-content">
    <div class="hero-eyebrow reveal">Regional Overview — DHL Asia-Pacific</div>
    <h1 class="hero-title reveal reveal-delay-1">Missed <em>Opportunities</em><br>Across DHL APAC</h1>
    <p class="hero-description reveal reveal-delay-2">A regional opportunity narrative built from 2025 dashboard transcriptions with 2023–2025 trend overlay, now including a site-by-site buying model. Each country page drills into product families and directional opportunity logic.</p>
    <div class="agg-stats reveal reveal-delay-3">
      <div class="agg-stat"><div class="agg-stat-value" style="color:var(--amber)">{len(countries)}</div><div class="agg-stat-label">Markets analyzed</div></div>
      <div class="agg-stat"><div class="agg-stat-value" style="color:var(--teal)">{fmt_k(total_obs)}</div><div class="agg-stat-label">Observed spend</div></div>
      <div class="agg-stat"><div class="agg-stat-value" style="color:var(--amber)">{fmt_k(total_pot)}</div><div class="agg-stat-label">Directional potential</div></div>
      <div class="agg-stat"><div class="agg-stat-value" style="color:var(--red-soft)">{round((1-total_obs/total_pot)*100)}%</div><div class="agg-stat-label">Modeled gap</div></div>
    </div>
    <div class="disclaimer-banner reveal reveal-delay-4" style="max-width:920px;margin-top:24px;"><div class="icon">⚠️</div><p><strong>Transparency first.</strong> Observed values from 2025 dashboard screenshots. Potential values are directional modeling. Multi-year trends are partial extraction from key visible categories. Site archetype model is an illustrative framework, not actual DHL site procurement data.</p></div>
  </div><div class="scroll-indicator"><span>Scroll</span><div class="scroll-arrow"></div></div></section>

  <section class="section" style="background:var(--bg-primary);border-top:1px solid var(--border);"><div class="container">
    <div class="section-label reveal">Country Pages</div>
    <h2 class="section-title reveal reveal-delay-1">Pick a DHL market</h2>
    <p class="section-subtitle reveal reveal-delay-2">Every page uses the same structure: observed actuals, multi-year trends, product drilldowns, site archetype model, lowest-hanging fruit, and clearly labeled directional assumptions.</p>
    <div class="country-grid">{''.join(cards)}</div>
  </div></section>

  {regional_trend}
  {archetype_section}
  {fruit_section}

  <section class="cta"><div class="container"><div class="reveal">
    <div class="section-label" style="justify-content:center;">The Opportunity</div>
    <h2 class="cta-title">~{fmt_k(total_pot - total_obs).replace('SGD ','')} in <em>missed opportunity</em></h2>
    <p class="cta-text">The gap between observed and realistic spend across all {len(countries)} DHL APAC entities, anchored in dashboard actuals, layered with multi-year momentum signals and a site-by-site buying framework.</p>
    <div class="cta-amount">{fmt_k(total_pot - total_obs)}</div>
    <div class="cta-amount-label">Total directional annual gap</div>
  </div></div></section>

  <footer class="footer"><div class="container">
    <div class="footer-text">SourceSage Opportunity Intelligence · DHL APAC</div>
    <div class="footer-divider"></div>
    <div class="footer-text" style="font-size:11px;">Confidential — Internal discussion only. Not for external circulation without validation. Multi-year trends are partial category extraction. Site archetype model is illustrative.</div>
  </div></footer>
  <script src="shared.js"></script>
  <script>initAll();</script>
</body></html>'''


# ────────────────────────────────────────────────────────────
# BUILD
# ────────────────────────────────────────────────────────────
# Update site-data.json
site_data = {}
for code, c in countries.items():
    site_data[code] = {
        'observed_total_k': round(c['observed_total'], 4),
        'potential_total_k': c['potential_total'],
        'gap_total_k': c['gap_total'],
    }
ROOT.joinpath('site-data.json').write_text(json.dumps(site_data, indent=2))

# Generate pages
ROOT.joinpath('index.html').write_text(make_landing_page())
for code, c in countries.items():
    d = ROOT / code
    d.mkdir(exist_ok=True)
    d.joinpath('index.html').write_text(make_country_page(code, c))

print(f'✅ v3 generated — {len(countries)} markets (incl. Hong Kong) + site archetype model on all pages')
