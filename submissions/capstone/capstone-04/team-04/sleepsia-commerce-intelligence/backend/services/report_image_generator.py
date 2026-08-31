"""
Server-side Report & Dashboard Image Generator in Python.
Deterministically generates high-contrast, executive-grade SVG dashboard visuals.
"""

import html
from typing import Dict, Any, List

def escape_xml(unsafe: Any) -> str:
    if unsafe is None:
        return ''
    return html.escape(str(unsafe), quote=True)

def truncate_and_escape(s: Any, max_len: int) -> str:
    if not s:
        return ''
    text = str(s)
    if len(text) > max_len:
        text = text[:max_len - 3] + '...'
    return escape_xml(text)

def wrap_text(text: str, max_chars_per_line: int, max_lines: int = 2) -> List[str]:
    if not text:
        return []
    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        if len((current_line + ' ' + word).strip()) <= max_chars_per_line:
            current_line = (current_line + ' ' + word).strip()
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
            if len(lines) >= max_lines - 1:
                break
    if current_line and len(lines) < max_lines:
        lines.append(current_line)
    if len(lines) == max_lines and len(words) > len(' '.join(lines).split()):
        lines[-1] = lines[-1].rstrip('.') + '...'
    return lines

def generate_dashboard_svg(report: Dict[str, Any]) -> str:
    report_date = report.get('reportDate', '2026-08-07')
    kpis = report.get('kpis', {})
    top_wins = report.get('topWins', [])
    top_risks = report.get('topRisks', [])
    marketplace_rankings = report.get('marketplaceRankings', [])
    actions = report.get('actionPlan', [])
    summary = report.get('executiveSummary', 'Executive briefing unavailable.')

    width = 1200
    height = 900

    def fmt(n: Any) -> str:
        try:
            return f"₹{round(float(n)):,}"
        except Exception:
            return f"₹{n}"

    top_mkt = marketplace_rankings[:5]
    summary_lines = wrap_text(summary, 130, 2)

    net_rev = kpis.get('netRevenue', 0)
    net_profit = kpis.get('netProfit', 0)
    margin = kpis.get('profitMarginPercent', 0)
    orders = kpis.get('totalOrders', 0)
    units = kpis.get('unitsSold', 0)
    ad_spend = kpis.get('adSpend', 0)
    roas = kpis.get('blendedRoas', 0)
    on_time = kpis.get('onTimeDeliveryRate', 92.0)
    stockouts = kpis.get('stockoutRiskCount', 0)

    # Build SVG content
    svg_parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} ${height}" xmlns="http://www.w3.org/2000/svg" style="background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif;">',
        '  <defs>',
        '    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#1e293b"/>',
        '      <stop offset="100%" stop-color="#0f172a"/>',
        '    </linearGradient>',
        '    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#1e293b"/>',
        '      <stop offset="100%" stop-color="#111827"/>',
        '    </linearGradient>',
        '  </defs>',
        f'  <!-- Background -->',
        f'  <rect width="{width}" height="{height}" fill="#0b0f19"/>',
        f'  <!-- Top Brand Banner -->',
        f'  <rect x="0" y="0" width="{width}" height="90" fill="url(#headerGrad)"/>',
        f'  <line x1="0" y1="90" x2="{width}" y2="90" stroke="#334155" stroke-width="1"/>',
        f'  <!-- Sleepsia Brand Logo & Badge -->',
        f'  <rect x="40" y="24" width="42" height="42" rx="10" fill="#3b82f6"/>',
        f'  <text x="61" y="52" font-size="22" font-weight="900" fill="#ffffff" text-anchor="middle">S</text>',
        f'  <text x="96" y="44" font-size="20" font-weight="800" fill="#f8fafc">Sleepsia</text>',
        f'  <text x="96" y="62" font-size="12" font-weight="600" fill="#94a3b8" letter-spacing="1">COMMERCE INTELLIGENCE PLATFORM</text>',
        f'  <!-- Report Date Badge -->',
        f'  <rect x="880" y="28" width="280" height="34" rx="8" fill="#1e293b" stroke="#334155"/>',
        f'  <circle cx="900" cy="45" r="5" fill="#10b981"/>',
        f'  <text x="915" y="49" font-size="13" font-weight="600" fill="#e2e8f0">Report Date: {escape_xml(report_date)}</text>',
        f'  <!-- ROW 1: 4 Main KPI Cards -->',
        f'  <g transform="translate(40, 115)">',
        f'    <rect width="260" height="110" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1"/>',
        f'    <rect x="0" y="0" width="6" height="110" rx="3" fill="#3b82f6"/>',
        f'    <text x="24" y="32" font-size="12" font-weight="700" fill="#94a3b8">NET REALIZED REVENUE</text>',
        f'    <text x="24" y="68" font-size="26" font-weight="800" fill="#f8fafc">{escape_xml(fmt(net_rev))}</text>',
        f'    <text x="24" y="94" font-size="12" font-weight="600" fill="#10b981">Orders: {orders:,} | Units: {units:,}</text>',
        f'  </g>',
        f'  <g transform="translate(325, 115)">',
        f'    <rect width="260" height="110" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1"/>',
        f'    <rect x="0" y="0" width="6" height="110" rx="3" fill="#10b981"/>',
        f'    <text x="24" y="32" font-size="12" font-weight="700" fill="#94a3b8">NET PROFIT (MARGIN)</text>',
        f'    <text x="24" y="68" font-size="26" font-weight="800" fill="#10b981">{escape_xml(fmt(net_profit))}</text>',
        f'    <text x="24" y="94" font-size="12" font-weight="600" fill="#e2e8f0">Margin: {margin}%</text>',
        f'  </g>',
        f'  <g transform="translate(610, 115)">',
        f'    <rect width="260" height="110" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1"/>',
        f'    <rect x="0" y="0" width="6" height="110" rx="3" fill="#f59e0b"/>',
        f'    <text x="24" y="32" font-size="12" font-weight="700" fill="#94a3b8">AD SPEND &amp; ROAS</text>',
        f'    <text x="24" y="68" font-size="26" font-weight="800" fill="#f59e0b">{escape_xml(fmt(ad_spend))}</text>',
        f'    <text x="24" y="94" font-size="12" font-weight="600" fill="#94a3b8">ROAS: {roas}x</text>',
        f'  </g>',
        f'  <g transform="translate(895, 115)">',
        f'    <rect width="265" height="110" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1"/>',
        f'    <rect x="0" y="0" width="6" height="110" rx="3" fill="#8b5cf6"/>',
        f'    <text x="24" y="32" font-size="12" font-weight="700" fill="#94a3b8">LOGISTICS SLA &amp; STOCK</text>',
        f'    <text x="24" y="68" font-size="26" font-weight="800" fill="#8b5cf6">{on_time}% SLA</text>',
        f'    <text x="24" y="94" font-size="12" font-weight="600" fill="#ef4444">Stockout Alerts: {stockouts} SKUs</text>',
        f'  </g>',
        f'  <!-- ROW 2: Executive Summary Box -->',
        f'  <g transform="translate(40, 245)">',
        f'    <rect width="1120" height="90" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1"/>',
        f'    <text x="24" y="30" font-size="13" font-weight="800" fill="#38bdf8">AI SUPERVISOR EXECUTIVE BRIEFING</text>',
    ]

    for idx, line in enumerate(summary_lines):
        svg_parts.append(f'    <text x="24" y="{52 + idx * 18}" font-size="12" font-weight="500" fill="#cbd5e1">{escape_xml(line)}</text>')

    svg_parts.extend([
        '  </g>',
        '  <!-- ROW 3 LEFT: Top Marketplace Leaderboard -->',
        '  <g transform="translate(40, 355)">',
        '    <rect width="545" height="255" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1"/>',
        '    <text x="24" y="34" font-size="14" font-weight="800" fill="#f8fafc">MARKETPLACE REVENUE LEADERBOARD</text>',
        '    <line x1="24" y1="48" x2="521" y2="48" stroke="#334155" stroke-width="1"/>',
    ])

    max_rev = max([m.get('netRevenue', 1) for m in top_mkt] or [1])
    for i, mp in enumerate(top_mkt):
        y = 74 + i * 36
        rev_val = mp.get('netRevenue', 0)
        bar_w = max(30, round((rev_val / max_rev) * 230))
        plat_name = mp.get('platform', 'Unknown')
        svg_parts.append(f'    <text x="24" y="{y + 14}" font-size="12" font-weight="700" fill="#e2e8f0">{truncate_and_escape(plat_name, 22)}</text>')
        svg_parts.append(f'    <rect x="180" y="{y}" width="{bar_w}" height="18" rx="4" fill="#3b82f6" opacity="0.85"/>')
        svg_parts.append(f'    <text x="{190 + bar_w}" y="{y + 14}" font-size="12" font-weight="700" fill="#f8fafc">{escape_xml(fmt(rev_val))}</text>')

    svg_parts.extend([
        '  </g>',
        '  <!-- ROW 3 RIGHT: Top Wins & Strategic Risks -->',
        '  <g transform="translate(615, 355)">',
        '    <rect width="545" height="255" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1"/>',
        '    <text x="24" y="34" font-size="14" font-weight="800" fill="#10b981">TOP WINS &amp; CATALYSTS</text>',
        '    <line x1="24" y1="48" x2="521" y2="48" stroke="#334155" stroke-width="1"/>',
    ])

    for i, w in enumerate(top_wins[:2]):
        lines = wrap_text(w, 65, 2)
        start_y = 70 + i * 42
        svg_parts.append(f'    <circle cx="32" cy="{start_y + 4}" r="4" fill="#10b981"/>')
        for li, l in enumerate(lines):
            svg_parts.append(f'    <text x="46" y="{start_y + li * 15}" font-size="11.5" font-weight="500" fill="#cbd5e1">{escape_xml(l)}</text>')

    svg_parts.extend([
        '    <text x="24" y="165" font-size="14" font-weight="800" fill="#ef4444">CRITICAL BUSINESS RISKS</text>',
        '    <line x1="24" y1="178" x2="521" y2="178" stroke="#334155" stroke-width="1"/>',
    ])

    for i, r in enumerate(top_risks[:2]):
        lines = wrap_text(r, 65, 2)
        start_y = 200 + i * 40
        svg_parts.append(f'    <circle cx="32" cy="{start_y + 4}" r="4" fill="#ef4444"/>')
        for li, l in enumerate(lines):
            svg_parts.append(f'    <text x="46" y="{start_y + li * 15}" font-size="11.5" font-weight="500" fill="#cbd5e1">{escape_xml(l)}</text>')

    svg_parts.extend([
        '  </g>',
        '  <!-- ROW 4: Action Plan Matrix -->',
        '  <g transform="translate(40, 630)">',
        '    <rect width="1120" height="230" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1"/>',
        '    <text x="24" y="34" font-size="14" font-weight="800" fill="#f8fafc">PRIORITIZED OPERATIONAL ACTION PLAN</text>',
        '    <line x1="24" y1="48" x2="1096" y2="48" stroke="#334155" stroke-width="1"/>',
    ])

    for i, act in enumerate(actions[:3]):
        y = 62 + i * 54
        p_str = act.get('priority', 'P2')
        p_color = '#ef4444' if 'P0' in p_str else ('#f59e0b' if 'P1' in p_str else '#3b82f6')
        p_short = 'P0' if 'P0' in p_str else ('P1' if 'P1' in p_str else 'P2')
        owner = act.get('owner', 'Operations')
        action_text = act.get('action', '')
        impact_text = act.get('expectedImpact', '')

        svg_parts.append(f'    <rect x="24" y="{y}" width="42" height="24" rx="6" fill="{p_color}" opacity="0.2" stroke="{p_color}"/>')
        svg_parts.append(f'    <text x="45" y="{y + 16}" font-size="11" font-weight="800" fill="{p_color}" text-anchor="middle">{escape_xml(p_short)}</text>')
        svg_parts.append(f'    <rect x="74" y="{y}" width="95" height="24" rx="6" fill="#334155"/>')
        svg_parts.append(f'    <text x="121" y="{y + 16}" font-size="11" font-weight="700" fill="#94a3b8" text-anchor="middle">{truncate_and_escape(owner, 12)}</text>')
        svg_parts.append(f'    <text x="180" y="{y + 16}" font-size="12" font-weight="700" fill="#f8fafc">{truncate_and_escape(action_text, 85)}</text>')
        svg_parts.append(f'    <text x="180" y="{y + 36}" font-size="11" font-weight="500" fill="#64748b">Impact: {truncate_and_escape(impact_text, 95)}</text>')

    svg_parts.extend([
        '  </g>',
        f'  <!-- Footer -->',
        f'  <text x="40" y="880" font-size="11" font-weight="500" fill="#64748b">Sleepsia Commerce Intelligence • Generated automatically via Python Django Multi-Agent Engine</text>',
        f'  <text x="1160" y="880" font-size="11" font-weight="600" fill="#94a3b8" text-anchor="end">CONFIDENTIAL • FOR SLEEPSIA MANAGEMENT ONLY</text>',
        '</svg>',
    ])

    return '\n'.join(svg_parts)
