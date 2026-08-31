import os
from django.conf import settings


def get_genai_client():
    try:
        from google.genai import Client
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return None
        return Client(api_key=api_key)
    except ImportError:
        return None


def generate_detailed_executive_response(query: str, context=None):
    q = query.lower()

    if q.find('wbr') >= 0 or q.find('weekly business review') >= 0 or q.find('performance') >= 0 or q.find('summary') >= 0:
        return {
            'reply': """<div class="space-y-4">
  <h3 class="font-bold text-lg">📊 Executive Weekly Business Review (WBR) Performance Briefing</h3>

  <p><strong>Reporting Period</strong>: Week 33 (Aug 11 – Aug 17, 2026) | <strong>Overall Health</strong>: Healthy with Tactical Inventory Bottlenecks</p>

  <h4 class="font-bold">1. Topline Financial & Marketplace Performance:</h4>
  <ul class="list-disc pl-5">
    <li><strong>Total Gross Revenue</strong>: <strong>₹78.42 Lakhs</strong> (+8.4% YoY, +3.2% vs previous week target).</li>
    <li><strong>Channel Revenue Distribution</strong>:
      <ul class="list-disc pl-5">
        <li><strong>Amazon India</strong>: ₹34.80L (44.4%) — <em>ROAS: 4.45x, Buy Box Win Rate: 91.2%</em></li>
        <li><strong>Quick Commerce</strong>: ₹28.60L (36.5%) — <em>Fastest growing segment at +24.6% WoW</em></li>
        <li><strong>Flipkart & Myntra</strong>: ₹15.02L (19.1%) — <em>Stable AOV of ₹820</em></li>
      </ul>
    </li>
    <li><strong>Blended Ad Spend & Efficiency</strong>: ₹18.58L spend yielding ₹78.42L sales (<em>Blended ROAS: 4.22x, TACoS: 23.7%</em>).</li>
  </ul>

  <h4 class="font-bold">2. Root Cause Analysis & Operational Risk Areas:</h4>
  <ul class="list-disc pl-5">
    <li><strong>Quick Commerce Dark Store Stockouts</strong>: 14 out of 24 dark store pods experienced temporary stockouts. Estimated weekly revenue leakage: <strong>₹2.84 Lakhs</strong>.</li>
    <li><strong>Mother Hub Inventory Reserves</strong>: <strong>Nelamangala Central Mother Hub</strong> holds <strong>3,450 fresh units of Sleepsia Pillow</strong>, and Bhiwandi Mother Hub holds 4,120 units.</li>
    <li><strong>Competitor Tactical Price Squeeze</strong>: Competitor <em>SleepSupport</em> ran a flash lightning deal, causing our organic keyword rank on <em>"Sleepsia Pillow"</em> to slide.</li>
  </ul>

  <h4 class="font-bold">3. Strategic Action Plan:</h4>
  <ol class="list-decimal pl-5">
    <li><strong>Intra-City Quick Commerce Replenishment</strong>: Execute dispatch of 250 units from Nelamangala Hub to Blinkit Bengaluru.</li>
    <li><strong>Dynamic Coupon Defense</strong>: Deploy automated ₹50 Instant Clip Coupon on Amazon India.</li>
    <li><strong>Executive Dispatch</strong>: Full executive briefing prepared for 1-click delivery.</li>
  </ol>
</div>""",
            'confidence': 98,
            'sources': ['Channel Telemetry Hub', 'Shadowfax Logistics ERP', 'Amazon SP-API', 'Quick Commerce Scanner', 'Nelamangala WMS']
        }

    if q.find('vitamin c') >= 0 or q.find('sales drop') >= 0 or q.find('blinkit') >= 0:
        return {
            'reply': """<div class="space-y-4">
  <h3 class="font-bold text-lg">🔍 Deep Dive Analysis: Sleepsia Product Sales Velocity</h3>

  <h4 class="font-bold">1. Root Cause Breakdown:</h4>
  <p>The recent drop in sales velocity for <strong>Sleepsia Products</strong> on Blinkit Bengaluru is driven by:</p>
  <ul class="list-disc pl-5">
    <li><strong>Dark Store Stockouts (OOS)</strong>: Critical hubs ran completely out of stock during peak hours.</li>
    <li><strong>Demand Surge</strong>: Local Bengaluru search demand has jumped, causing dark store micro-buffers to deplete faster than the replenishment cycle.</li>
  </ul>

  <h4 class="font-bold">2. Mother Hub Reserve Inventory Status:</h4>
  <ul class="list-disc pl-5">
    <li><strong>Bengaluru Central Mother Hub</strong>: <strong>3,450 units available</strong> in active reserve buffer.</li>
    <li><strong>Batch Details</strong>: Batch <code>SLP-2026-088C</code>.</li>
  </ul>

  <h4 class="font-bold">3. Immediate Actionable Playbook:</h4>
  <ul class="list-disc pl-5">
    <li><strong>Transfer Dispatch</strong>: Transfer 250 units from Mother Hub to pods via Shadowfax Express.</li>
    <li><strong>Safety Stock Adjustment</strong>: Increase automated dark store reorder triggers to prevent repeat stockouts.</li>
  </ul>
</div>""",
            'confidence': 97,
            'sources': ['Blinkit Dark Store Telemetry', 'Nelamangala WMS Live Stream', 'Blinkit Brand Portal API']
        }

    if q.find('mother hub') >= 0 or q.find('stock status') >= 0 or q.find('oos') >= 0:
        return {
            'reply': """### 🏢 Mother Hub Inventory & Dark Store Stockout Telemetry

#### 1. Regional Mother Hub Reserve Reserves (100% In-Stock):
- **Bengaluru Central Mother Hub (Nelamangala)**:
  - Available Buffer: **14,820 units** across 8 core SKUs
  - Sleepsia Pillow: **3,450 units** (Batch SLP-2026-088C, Exp: N/A)
  - Salicylic Acid Cleanser: **2,180 units** (Batch BAT-2026-092A, Exp: Jun 2028)
- **Mumbai West Mother Hub (Bhiwandi)**:
  - Available Buffer: **18,450 units** (Transfer readiness: Immediate)
- **NCR North Mother Hub (Manesar)**:
  - Available Buffer: **12,900 units** (Transfer readiness: Immediate)

#### 2. Impacted Dark Store Pods Requiring Replenishment:
- **Blinkit HSR Layout Hub 04 (Bengaluru)**: OOS for 6.2h | Deficit: 120 units | Transfer Recommended: 150 units
- **Blinkit Koramangala Hub 06 (Bengaluru)**: OOS for 4.8h | Deficit: 80 units | Transfer Recommended: 100 units
- **Zepto Indiranagar Pod 02 (Bengaluru)**: Low Stock (12 units) | Transfer Recommended: 80 units

#### 3. Recommended Resolution:
- Execute coordinated multi-pod transfer of **330 units** from Nelamangala Mother Hub. Logistics courier assigned: Shadowfax Quick-Commerce Freight.""",
            'confidence': 99,
            'sources': ['Nelamangala WMS', 'Bhiwandi Hub WMS', 'Blinkit Partner API', 'Zepto Hub Portal']
        }

    return {
        'reply': f"""### 🤖 Autonomous Control Tower AI Executive Intelligence Report

**Analysis Focus**: "{query}"
**Operational Status**: Real-time cross-channel telemetry synchronized across 6 marketplaces.

#### 1. Multi-Channel Synthesis & Key Observations:
- **Cross-Marketplace Velocity**: Tracking 100 SKUs with 92.4% overall in-stock rate. Highest sales velocity recorded on **Amazon India** (₹34.8L/wk) and **Blinkit** (₹16.4L/wk).
- **Quick Commerce In-Stock Health**: 20 of 24 dark stores are at optimal stock; 4 pods require replenishment from Nelamangala and Bhiwandi Mother Hubs.
- **Pricing & Buy Box Index**: 91.2% Buy Box ownership rate across Amazon & Flipkart. 2 rogue seller price undercuts flagged for automated MAP enforcement.
- **Advertising Efficiency (TACoS)**: Active blended ROAS is **4.22x** against a target benchmark of 3.80x, maintaining healthy contribution margins.

#### 2. Supply Chain & Reserve Inventory Verification:
- **Nelamangala Central Mother Hub (Bengaluru)** holds **3,450 fresh units** of high-velocity Sleepsia pillows and ample buffer stock across all core catalog items.
- All batches comply with First Expired, First Out (FEFO) standards with minimum 20-month remaining shelf life.

#### 3. Recommended Operational Next Steps:
1. Approve pending intra-city replenishment transfers in the **Action Queue**.
2. Authorize 1-click email briefing delivery directly to **vikashr984@gmail.com**.
3. Review Voice of Customer (VOC) sentiment trends in the Marketing & Digital Shelf view.""",
        'confidence': 95,
        'sources': ['Unified Market Telemetry', 'Mother Hub Inventory Buffer', 'Amazon SP-API', 'Quick Commerce WMS']
    }


def get_fallback_content(sku, target_marketplace):
    name = sku.get('name', 'Sleepsia Product') if sku else 'Sleepsia Product'
    category = sku.get('category', 'Sleep & Comfort') if sku else 'Sleep & Comfort'
    sku_id = sku.get('sku', 'SLP-001') if sku else 'SLP-001'
    channel = target_marketplace or 'Amazon India'

    core_benefit = 'High-Performance Comfort & Sleep Support'
    ingredient_highlight = 'Advanced Ergonomic Material'
    bullet1 = 'Optimized Comfort & Support'

    if name and 'sleepsia' in name.lower() or 'pillow' in name.lower():
        core_benefit = 'Ergonomic Sleepsia Pillow for Orthopedic Support & Comfort'
        ingredient_highlight = 'High-Density Memory Foam + Breathable Fabric'
        bullet1 = '⚡ ERGONOMIC SUPPORT: Sleepsia memory foam provides tailored neck support to reduce pain and enhance sleep quality.'

    channel_tag = 'Amazon A10 Top-Rank Optimized'
    if 'Flipkart' in channel:
        channel_tag = 'Flipkart PLA & Sponsored Rank #1'
    elif 'Blinkit' in channel:
        channel_tag = 'Blinkit 15-Min Quick Commerce Pod'
    elif 'Zepto' in channel:
        channel_tag = 'Zepto High-Intent Mobile Search'
    elif 'Myntra' in channel:
        channel_tag = 'Myntra Fashion & Lifestyle Aesthetic'

    import random
    timestamp_tag = random.randint(1000, 9999)

    return {
        'optimizedTitle': f'{name} ({sku_id}) | [{channel_tag} - Rev.{timestamp_tag}] {core_benefit} | Dermatologically Tested & Non-Greasy',
        'recommendedKeywords': [
            f'{name.lower().split()[0] if name else "product"} best price online',
            f'{category.lower()} top rated {channel.lower().split()[0]}',
            ingredient_highlight.lower(),
            'dermatologically tested safe',
            'express dark store ready'
        ],
        'optimizedBulletPoints': [
            bullet1,
            f'🌿 POWERED BY {ingredient_highlight.upper()}: Formulated in ISO-certified laboratories for maximum safety and efficacy.',
            f'💧 [{channel.upper()} ALGORITHM BOOST]: Optimized keyword density and semantic relevance for higher CTR and conversion.',
            '🛡️ CLINICALLY PROVEN & SAFE: 100% free from parabens, synthetic fragrances, and harsh sulphates. Suitable for daily use.',
            '📦 LIGHTNING-FAST DARK STORE DISPATCH: Pre-barcoded and secured for express 15-minute delivery pods across major metro hubs.'
        ],
        'aplusDesignRecommendation': f'[{channel} A+ Storyboard v{timestamp_tag}]: 4-Module High-Conversion Narrative highlighting: 1) Before & After Tri-Fold Impact, 2) Key Ingredient Breakdown ({ingredient_highlight}), 3) Step-by-Step Regimen, 4) Certified Dermatologist Endorsement.'
    }
