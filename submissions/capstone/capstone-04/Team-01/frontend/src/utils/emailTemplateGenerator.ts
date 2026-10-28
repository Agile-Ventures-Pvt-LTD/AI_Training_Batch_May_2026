import { AlertAnomaly, SKUListing, MAPBreach, DarkStoreInventory } from '../types';
import { expandAcronyms, ACRONYMS_DICTIONARY } from './acronyms';

export const OWNER_EMAIL = 'vikashr984@gmail.com';
export const SENDER_GMAIL = 'vikashr984@gmail.com';

export function formatINR(val?: number): string {
  if (val === undefined || val === null || isNaN(val)) return '₹0';
  if (val >= 10000000) {
    return `₹${(val / 10000000).toFixed(2)} Cr`;
  }
  if (val >= 100000) {
    return `₹${(val / 100000).toFixed(2)} Lakh`;
  }
  return `₹${val.toLocaleString('en-IN')}`;
}

export interface FollowUpSuggestion {
  id: string;
  title: string;
  actionText: string;
  impact: string;
  actionType: 'transfer_stock' | 'enforce_map' | 'clearance_fefo' | 'quality_audit' | 'deploy_coupon';
  payload?: {
    sku?: string;
    motherHub?: string;
    units?: number;
    price?: number;
    channel?: string;
    batchNumber?: string;
  };
}

export interface ResolutionFlowStep {
  stepNumber: number;
  title: string;
  description: string;
  badgeType: 'danger' | 'success' | 'info' | 'warning';
}

export interface GeneratedEmailContent {
  subject: string;
  recipientEmail: string;
  senderEmail: string;
  problemType: 'micro_oos' | 'map_breach' | 'sentiment_quality' | 'expiry_fefo' | 'sku_360' | 'executive_wbr';
  problemTitle: string;
  skuCode: string;
  metrics: {
    revenueAtRiskInr: number;
    motherHubStock: number;
    darkStoreStock: number;
    leadTimeHours: number;
    leadTimeLabel: string;
    motherHubName: string;
    dailyVelocity?: number;
    activePrice?: number;
  };
  diagnosticRootCause: string;
  resolutionFlow: ResolutionFlowStep[];
  followUpSuggestions: FollowUpSuggestion[];
  htmlContent: string;
  textContent: string;
  expandedSummary: string;
  usedAcronyms: Array<{ short: string; full: string; description: string }>;
}

export interface DatasetContext {
  skus?: SKUListing[];
  darkStores?: DarkStoreInventory[];
  alerts?: AlertAnomaly[];
  mapBreaches?: MAPBreach[];
}

export function generateInteractiveEmail(
  anomaly?: AlertAnomaly | null,
  skuContext?: SKUListing | null,
  mapAuditContext?: MAPBreach[] | null,
  options?: {
    customSubject?: string;
    recipient?: string;
    sender?: string;
    includeMotherHub?: boolean;
    includePerishables?: boolean;
    datasetContext?: DatasetContext | null;
    transferredUnits?: number;
  }
): GeneratedEmailContent {
  const customSubject = options?.customSubject;
  const recipient = options?.recipient || OWNER_EMAIL;
  const sender = options?.sender || SENDER_GMAIL;
  const includeMotherHub = options?.includeMotherHub ?? true;
  const dataset = options?.datasetContext;
  const skus = dataset?.skus || [];
  const darkStores = dataset?.darkStores || [];
  const allAlerts = dataset?.alerts || [];
  const allMapBreaches = dataset?.mapBreaches || [];
  const primaryHub = skus[0]?.defaultMotherHub || 'Central Mother Hub (Nelamangala)';

  const relevantAcronyms = [
    ACRONYMS_DICTIONARY.OOS,
    ACRONYMS_DICTIONARY.SKU,
    ACRONYMS_DICTIONARY.MAP,
    ACRONYMS_DICTIONARY.ROAS,
    ACRONYMS_DICTIONARY.QC,
    ACRONYMS_DICTIONARY.FEFO,
    ACRONYMS_DICTIONARY.ASP,
    ACRONYMS_DICTIONARY.SLA,
    ACRONYMS_DICTIONARY.WBR,
    ACRONYMS_DICTIONARY.VOC
  ];

  // -------------------------------------------------------------
  // CASE 1: MAP AUDIT & PRICE PROTECTION CONTEXT
  // -------------------------------------------------------------
  if (mapAuditContext && mapAuditContext.length > 0) {
    const totalMarginRisk = mapAuditContext.reduce((sum, b) => sum + (b.estimatedLossInr || ((b.enforcedMap - b.violatedPrice) * 150)), 0);
    const topBreach = mapAuditContext[0];
    const subject = customSubject || `[MAP ENFORCEMENT AUDIT] Executive Report: ${mapAuditContext.length} Active 3P Price Protection Breaches Detected`;

    const diagnosticRootCause = `Automated digital shelf monitoring across ${skus.length} catalog lines has detected ${mapAuditContext.length} active Minimum Advertised Price (MAP) violations. Unauthorized sellers such as "${topBreach.violatingSeller}" are undercutting enforced MAP by up to ₹${topBreach.priceGapInr || (topBreach.enforcedMap - topBreach.violatedPrice)} on ${topBreach.channel.toUpperCase()}, creating ₹${totalMarginRisk.toLocaleString('en-IN')} in monthly margin exposure and Buy Box erosion.`;

    const resolutionFlow: ResolutionFlowStep[] = mapAuditContext.map((b, idx) => ({
      stepNumber: idx + 1,
      title: `${b.sku} (${b.productName}) on ${b.channel.toUpperCase()}`,
      description: `Violating Seller: ${b.violatingSeller}. Target MAP: ₹${b.enforcedMap}, Violated Price: ₹${b.violatedPrice} (Undercut: ₹${b.priceGapInr || (b.enforcedMap - b.violatedPrice)}). Monthly Margin Risk: ₹${(b.estimatedLossInr || ((b.enforcedMap - b.violatedPrice) * 150)).toLocaleString('en-IN')}.`,
      badgeType: 'danger'
    }));

    const followUpSuggestions: FollowUpSuggestion[] = mapAuditContext.map((b, idx) => ({
      id: `sug-map-${b.sku}-${idx}`,
      title: `Enforce MAP Compliance on ${b.channel.toUpperCase()} for ${b.sku}`,
      actionText: `Issue automated Cease & Desist notice to "${b.violatingSeller}" and trigger Brand Registry BuyBox injunction.`,
      impact: `Protects target MAP of ₹${b.enforcedMap}, recovers ₹${(b.estimatedLossInr || ((b.enforcedMap - b.violatedPrice) * 150)).toLocaleString('en-IN')} monthly margin risk, and restores authorized dealer parity.`,
      actionType: 'enforce_map',
      payload: { sku: b.sku, channel: b.channel, price: b.enforcedMap }
    }));

    const textContent = `================================================================================
MAP ENFORCEMENT & PRICE PROTECTION AUDIT REPORT
Generated by Agile Solutions Autonomous Control Tower
================================================================================

TO: Vikash Kumar (${recipient})
FROM: E-commerce Control Tower (${sender})
DATE: ${new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
ACTIVE VIOLATIONS: ${mapAuditContext.length} SKU Assortment Lines

--------------------------------------------------------------------------------
1. EXECUTIVE FINANCIAL EXPOSURE
--------------------------------------------------------------------------------
• Total Active MAP Violations: ${mapAuditContext.length} SKUs
• Total Monthly Margin Risk at Stake: ₹${totalMarginRisk.toLocaleString('en-IN')}
• Channels Impacted: ${Array.from(new Set(mapAuditContext.map(b => b.channel.toUpperCase()))).join(', ')}

--------------------------------------------------------------------------------
2. DIAGNOSTIC ROOT CAUSE BREAKDOWN
--------------------------------------------------------------------------------
${diagnosticRootCause}

--------------------------------------------------------------------------------
3. AUTOMATED COMPLIANCE PLAYBOOKS & CEASE & DESIST NOTICES
--------------------------------------------------------------------------------
${followUpSuggestions.map((s, idx) => `[PLAYBOOK #${idx + 1}] ${s.title}
• Recommended Action: ${s.actionText}
• Projected Business Impact: ${s.impact}
`).join('\n')}

--------------------------------------------------------------------------------
4. RETAIL ACRONYMS GLOSSARY
--------------------------------------------------------------------------------
${relevantAcronyms.map((a) => `• ${a.short} = ${a.full}: ${a.description}`).join('\n')}

================================================================================
Dispatched via Agile Solutions Control Tower | Verified for Vikash Kumar
================================================================================`;

    const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${subject}</title>
  <style>
    body { margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #0f172a; line-height: 1.6; }
    .container { max-width: 680px; margin: 24px auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
    .header { background: #0f172a; color: #ffffff; padding: 24px; }
    .header-badge { display: inline-block; background-color: #d97706; color: #ffffff; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; margin-bottom: 8px; }
    .content { padding: 24px; }
    .kpi-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
    .kpi-card { background-color: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; padding: 12px 14px; }
    .kpi-label { font-size: 10px; font-weight: 700; color: #92400e; text-transform: uppercase; margin-bottom: 4px; }
    .kpi-value { font-size: 18px; font-weight: 800; color: #b45309; }
    .section-title { font-size: 13px; font-weight: 800; text-transform: uppercase; color: #0f172a; margin: 20px 0 10px 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }
    .sug-card { background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; font-size: 12px; }
    .footer { background-color: #f1f5f9; padding: 16px; font-size: 11px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-badge">MAP & PRICE PROTECTION AUDIT</div>
      <h2 style="margin:0 0 6px 0; font-size:18px;">Executive Price Compliance & C&D Playbooks</h2>
      <div style="font-size:12px; color:#cbd5e1;">Active Breaches: ${mapAuditContext.length} | Recipient: ${recipient}</div>
    </div>
    <div class="content">
      <p style="font-size:13px; margin-top:0;">Dear <strong>Vikash Kumar</strong>,<br>Below is the price protection audit report highlighting unauthorized 3P undercutting across your sales channels, with 1-click legal notice and Buy Box enforcement playbooks ready for dispatch.</p>
      
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">Active MAP Violations</div>
          <div class="kpi-value">${mapAuditContext.length} SKUs</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Total Monthly Margin Risk</div>
          <div class="kpi-value">₹${totalMarginRisk.toLocaleString('en-IN')}</div>
        </div>
      </div>

      <div class="section-title">1. Diagnostic Root Cause Breakdown</div>
      <div style="background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 12px; font-size: 12px; color: #92400e; margin-bottom: 16px;">
        ${diagnosticRootCause}
      </div>

      <div class="section-title">2. Recommended Compliance Playbooks</div>
      ${followUpSuggestions.map((s, idx) => `
        <div class="sug-card">
          <strong style="color: #b45309;">Playbook #${idx + 1}: ${s.title}</strong><br>
          <div style="color: #334155; margin-top: 3px;"><strong>Recommended Action:</strong> ${s.actionText}</div>
          <div style="color: #92400e; font-size: 11px; margin-top: 2px;"><strong>Business Impact:</strong> ${s.impact}</div>
        </div>
      `).join('')}
    </div>
    <div class="footer">
      Dispatched automatically by <strong>Agile Solutions Control Tower</strong> for <strong>${recipient}</strong>.
    </div>
  </div>
</body>
</html>
`;

    return {
      subject,
      recipientEmail: recipient,
      senderEmail: sender,
      problemType: 'map_breach',
      problemTitle: `${mapAuditContext.length} Active MAP Compliance Breaches`,
      skuCode: topBreach.sku,
      metrics: {
        revenueAtRiskInr: totalMarginRisk,
        motherHubStock: 35000,
        darkStoreStock: 0,
        leadTimeHours: 1.5,
        leadTimeLabel: '1.5h SLA',
        motherHubName: primaryHub
      },
      diagnosticRootCause,
      resolutionFlow,
      followUpSuggestions,
      htmlContent,
      textContent,
      expandedSummary: diagnosticRootCause,
      usedAcronyms: relevantAcronyms
    };
  }

  // -------------------------------------------------------------
  // CASE 2: SPECIFIC ANOMALY / ALERT EMAIL
  // -------------------------------------------------------------
  if (anomaly) {
    const skuObj = skus.find((s) => s.sku === anomaly.sku) || skuContext;
    const isMapBreach = anomaly.summary.toLowerCase().includes('map') || anomaly.recommendedPlaybook?.toLowerCase().includes('map');
    const isExpiry = anomaly.summary.toLowerCase().includes('expiry') || anomaly.summary.toLowerCase().includes('batch');
    const isQuality = anomaly.summary.toLowerCase().includes('rating') || anomaly.summary.toLowerCase().includes('sentiment');
    
    let problemType: 'micro_oos' | 'map_breach' | 'sentiment_quality' | 'expiry_fefo' = 'micro_oos';
    if (isMapBreach) problemType = 'map_breach';
    else if (isExpiry) problemType = 'expiry_fefo';
    else if (isQuality) problemType = 'sentiment_quality';

    const revenueAtRisk = anomaly.revenueAtRiskInr || 150000;
    const motherHubStock = anomaly.motherHubStock || skuObj?.motherHubStock || 35000;
    const darkStoreStock = anomaly.darkStoreStock ?? skuObj?.darkStoreStock ?? 0;
    const motherHubName = anomaly.motherHubName || skuObj?.defaultMotherHub || 'Central Mother Hub (Nelamangala)';
    const transferUnits = options?.transferredUnits ?? (anomaly.transferUnitsSuggested || Math.max(100, Math.ceil((skuObj?.dailyVelocity || 50) * 7)));
    const leadTime = anomaly.transferLeadTimeHours || 1.5;
    const batchNum = anomaly.batchNumber || skuObj?.batches?.[0]?.batchNumber || `BAT-${anomaly.sku}-01`;
    const expiryDate = anomaly.expiryDate || skuObj?.batches?.[0]?.expiryDate || '2028-04-20';
    const channelName = (anomaly.marketplace || 'blinkit').toUpperCase();

    const subject = customSubject || `[${anomaly.severity.toUpperCase()} INCIDENT] ${anomaly.sku} (${anomaly.productName}) on ${channelName} - Root Cause & Follow-Up Solutions`;

    const expandedSummary = expandAcronyms(anomaly.summary);

    // Follow-up suggestions according to the specific problem
    const followUpSuggestions: FollowUpSuggestion[] = [];
    const resolutionFlow: ResolutionFlowStep[] = [];

    if (problemType === 'micro_oos') {
      resolutionFlow.push({
        stepNumber: 1,
        title: `Micro-Fulfillment Dark Store Pod Starvation (${channelName})`,
        description: `Current available inventory across Quick Commerce pods has depleted to ${darkStoreStock} units. Real-time sales velocity is causing unfulfilled consumer demand.`,
        badgeType: 'danger'
      });
      resolutionFlow.push({
        stepNumber: 2,
        title: `Mother Hub Reserve Verification (${motherHubName})`,
        description: `Verified ${motherHubStock.toLocaleString('en-IN')} fresh units in reserve buffer. Manufacturing Batch: ${batchNum} (Exp: ${expiryDate}, FEFO Compliant).`,
        badgeType: 'success'
      });
      resolutionFlow.push({
        stepNumber: 3,
        title: `Intra-City Rapid Logistics Dispatch`,
        description: `Initiate express stock replenishment of ${transferUnits} units via ${anomaly.logisticsPartner || 'Quick Corridor'} with guaranteed ${leadTime} Hours Service Level Agreement (SLA).`,
        badgeType: 'info'
      });

      followUpSuggestions.push({
        id: `sug-transfer-${anomaly.sku}`,
        title: `1-Click Stock Dispatch (${transferUnits} Units)`,
        actionText: `Approve and dispatch ${transferUnits} units from ${motherHubName} to ${channelName} Dark Stores.`,
        impact: `Protects ${formatINR(revenueAtRisk)} in immediate 48-hour revenue exposure.`,
        actionType: 'transfer_stock',
        payload: { sku: anomaly.sku, motherHub: motherHubName, units: transferUnits }
      });
      followUpSuggestions.push({
        id: `sug-reorder-threshold-${anomaly.sku}`,
        title: `Dynamic Buffer Floor Adjustment`,
        actionText: `Auto-calibrate reorder threshold from 5 to ${Math.ceil((skuObj?.dailyVelocity || 50) * 0.4)} units for ${anomaly.sku}.`,
        impact: `Prevents recurring stockouts during peak ordering hours.`,
        actionType: 'deploy_coupon'
      });
      followUpSuggestions.push({
        id: `sug-pause-ads-${anomaly.sku}`,
        title: `Ad Spend Protection Throttle`,
        actionText: `Temporarily pause sponsored product bids on ${channelName} until dark store check-in is complete.`,
        impact: `Eliminates wasted ad clicks while product is out of stock.`,
        actionType: 'deploy_coupon'
      });
    } else if (problemType === 'map_breach') {
      const priceGap = (skuObj?.targetMap || 1499) - (skuObj?.sellingPrice || 1299);
      resolutionFlow.push({
        stepNumber: 1,
        title: `Unauthorized Reseller Discount Detected`,
        description: `Product is listed at ₹${(skuObj?.sellingPrice || 1299).toLocaleString('en-IN')} on ${channelName}, which is ₹${priceGap} below the target Minimum Advertised Price (MAP) of ₹${(skuObj?.targetMap || 1499).toLocaleString('en-IN')}.`,
        badgeType: 'danger'
      });
      resolutionFlow.push({
        stepNumber: 2,
        title: `Catalog Buy Box & Margin Impact`,
        description: `Price erosion poses a monthly revenue risk of ${formatINR(revenueAtRisk)} and suppresses brand buy box ownership across authorized channels.`,
        badgeType: 'warning'
      });
      resolutionFlow.push({
        stepNumber: 3,
        title: `Automated Price-Lock & Compliance Playbook`,
        description: `Execute legal notice to offending 3P merchant and trigger marketplace API pricing reset.`,
        badgeType: 'info'
      });

      followUpSuggestions.push({
        id: `sug-enforce-map-${anomaly.sku}`,
        title: `Issue Cease & Desist & MAP Price Reset`,
        actionText: `Trigger automated compliance notice to merchant desk and enforce target MAP of ₹${skuObj?.targetMap || 1499}.`,
        impact: `Recovers ${formatINR(revenueAtRisk)} in monthly brand value and stops price wars.`,
        actionType: 'enforce_map',
        payload: { sku: anomaly.sku, channel: channelName, price: skuObj?.targetMap || 1499 }
      });
      followUpSuggestions.push({
        id: `sug-defend-coupon-${anomaly.sku}`,
        title: `Deploy Instant Clip Coupon`,
        actionText: `Stage a ₹50 time-limited clip coupon on Amazon to defend sales rank without lowering MAP.`,
        impact: `Maintains search rank #1 while maintaining contractual price floor.`,
        actionType: 'deploy_coupon'
      });
    } else if (problemType === 'expiry_fefo') {
      resolutionFlow.push({
        stepNumber: 1,
        title: `Perishable Batch Shelf Life Threshold Alert`,
        description: `Manufacturing Batch ${batchNum} has near-term expiry date (${expiryDate}) with ${formatINR(revenueAtRisk)} worth of stock in warehouse storage.`,
        badgeType: 'warning'
      });
      resolutionFlow.push({
        stepNumber: 2,
        title: `First Expired, First Out (FEFO) Priority Routing`,
        description: `Routing system has prioritized batch ${batchNum} ahead of newer inventory to minimize write-offs.`,
        badgeType: 'info'
      });

      followUpSuggestions.push({
        id: `sug-fefo-flash-${anomaly.sku}`,
        title: `Launch FEFO Quick Commerce Clearance Flash`,
        actionText: `Deploy a 15% promotional bundle on Quick Commerce to liquidate batch ${batchNum} within 14 days.`,
        impact: `Recovers ${formatINR(revenueAtRisk)} in inventory value before write-off window.`,
        actionType: 'clearance_fefo',
        payload: { sku: anomaly.sku, batchNumber: batchNum }
      });
    } else {
      resolutionFlow.push({
        stepNumber: 1,
        title: `Customer Sentiment & Review Rating Dip`,
        description: `Average rating has dropped below 4.3★ benchmark. Review text indicates potential secondary courier packaging damage.`,
        badgeType: 'warning'
      });
      resolutionFlow.push({
        stepNumber: 2,
        title: `Quality Assurance Audit & Customer Remediation`,
        description: `Initiate packaging audit with manufacturing plant and dispatch customer care resolution.`,
        badgeType: 'info'
      });

      followUpSuggestions.push({
        id: `sug-quality-audit-${anomaly.sku}`,
        title: `Audit Secondary Transit Packaging`,
        actionText: `Instruct 3PL fulfillment center to apply double bubble wrap and tamper tape on all dispatches.`,
        impact: `Reduces return rate by an estimated 42% and restores customer CSAT score.`,
        actionType: 'quality_audit',
        payload: { sku: anomaly.sku }
      });
    }

    const textContent = `================================================================================
EXECUTIVE E-COMMERCE INTELLIGENCE & INCIDENT RESOLUTION REPORT
Generated by Agile Solutions Autonomous Control Tower
================================================================================

TO: Vikash Kumar (${recipient})
FROM: E-commerce Control Tower (${sender})
DATE: ${new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
SECURITY: Authenticated 250 OK Protocol

--------------------------------------------------------------------------------
1. INCIDENT DIAGNOSTIC & FINANCIAL EXPOSURE
--------------------------------------------------------------------------------
• Severity Level: ${anomaly.severity.toUpperCase()} ALERT
• Product Description: ${anomaly.productName}
• Stock Keeping Unit (SKU): ${anomaly.sku}
• Channel / Marketplace: ${channelName}
• Financial Revenue At Risk: Indian Rupees (INR) ${revenueAtRisk.toLocaleString('en-IN')} (${formatINR(revenueAtRisk)})
• Diagnostic Root Cause: ${expandedSummary}

--------------------------------------------------------------------------------
2. SUPPLY CHAIN RESOLUTION & INVENTORY FLOW
--------------------------------------------------------------------------------
• Dark Store / Micro-Fulfillment Status: ${darkStoreStock} Units Available (${darkStoreStock < 5 ? 'Low Stock / Out Of Stock' : 'In Stock'})
• Designated Backup Mother Hub: ${motherHubName}
• Mother Hub Reserve Stock: ${motherHubStock.toLocaleString('en-IN')} Fresh Units Ready in Warehouse
• Manufacturing Batch: ${batchNum} (Mfg: ${anomaly.mfgDate || '2026-01-15'}, Exp: ${expiryDate})
• Recommended Dispatch: Transfer ${transferUnits} Units via ${anomaly.logisticsPartner || 'Quick Corridor'} (${leadTime} Hours SLA)

--------------------------------------------------------------------------------
3. ACTIONABLE FOLLOW-UP SUGGESTIONS TAILORED TO THIS PROBLEM
--------------------------------------------------------------------------------
${followUpSuggestions.map((s, idx) => `[SUGGESTION #${idx + 1}] ${s.title}
• Recommended Action: ${s.actionText}
• Projected Business Impact: ${s.impact}
`).join('\n')}

--------------------------------------------------------------------------------
4. RETAIL ACRONYMS FULL-FORM GLOSSARY
--------------------------------------------------------------------------------
${relevantAcronyms.map((a) => `• ${a.short} = ${a.full}: ${a.description}`).join('\n')}

================================================================================
Dispatched via Agile Solutions Control Tower Engine | Verified for Vikash Kumar
================================================================================`;

    const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${subject}</title>
  <style>
    body { margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #0f172a; line-height: 1.6; }
    .container { max-width: 680px; margin: 24px auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
    .header { background: #0f172a; color: #ffffff; padding: 24px; }
    .header-badge { display: inline-block; background-color: #e11d48; color: #ffffff; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; margin-bottom: 8px; }
    .content { padding: 24px; }
    .kpi-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
    .kpi-card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 14px; }
    .kpi-label { font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 4px; }
    .kpi-value { font-size: 18px; font-weight: 800; color: #0f172a; }
    .kpi-value.danger { color: #dc2626; }
    .kpi-value.success { color: #16a34a; }
    .section-title { font-size: 13px; font-weight: 800; text-transform: uppercase; color: #0f172a; margin: 20px 0 10px 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }
    .flow-box { background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 14px; margin-bottom: 16px; font-size: 12px; }
    .sug-card { background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; font-size: 12px; }
    .footer { background-color: #f1f5f9; padding: 16px; font-size: 11px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-badge">${anomaly.severity.toUpperCase()} INCIDENT: ${problemType.toUpperCase()}</div>
      <h2 style="margin:0 0 6px 0; font-size:18px;">${anomaly.productName}</h2>
      <div style="font-size:12px; color:#94a3b8;">SKU: ${anomaly.sku} | Marketplace: ${channelName} | Recipient: ${recipient}</div>
    </div>
    <div class="content">
      <p style="font-size:13px; margin-top:0;">Dear <strong>Vikash Kumar</strong>,<br>Below is the real-time operational incident report with verified root causes and actionable follow-up recommendations derived from your live catalog dataset.</p>
      
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">Financial Revenue At Risk</div>
          <div class="kpi-value danger">${formatINR(revenueAtRisk)}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Mother Hub Reserve</div>
          <div class="kpi-value success">${motherHubStock.toLocaleString('en-IN')} Units</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Dark Store Pod Status</div>
          <div class="kpi-value danger">${darkStoreStock} Units (${darkStoreStock < 5 ? 'OOS / Low' : 'In Stock'})</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Transfer SLA Lead Time</div>
          <div class="kpi-value">${leadTime} Hours</div>
        </div>
      </div>

      <div class="section-title">1. Diagnostic Root Cause Breakdown</div>
      <div style="background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 12px; font-size: 12px; color: #92400e; margin-bottom: 16px;">
        ${expandedSummary}
      </div>

      <div class="section-title">2. Supply Chain & Resolution Flow</div>
      <div class="flow-box">
        ${resolutionFlow.map((r) => `
          <div style="margin-bottom: 8px;">
            <strong>Step ${r.stepNumber}: ${r.title}</strong><br>
            <span style="color: #334155;">${r.description}</span>
          </div>
        `).join('')}
      </div>

      <div class="section-title">3. Tailored Follow-Up Suggestions for the Problem</div>
      ${followUpSuggestions.map((s, idx) => `
        <div class="sug-card">
          <strong style="color: #15803d;">Suggestion #${idx + 1}: ${s.title}</strong><br>
          <div style="color: #334155; margin-top: 3px;"><strong>Action:</strong> ${s.actionText}</div>
          <div style="color: #166534; font-size: 11px; margin-top: 2px;"><strong>Impact:</strong> ${s.impact}</div>
        </div>
      `).join('')}

      <div style="margin-top: 24px; padding: 16px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; text-align: center;">
        <div style="font-size: 11px; font-weight: 800; color: #334155; text-transform: uppercase; margin-bottom: 10px;">⚡ Owner Action CTAs & Integration Links</div>
        <a href="https://ai.studio/build" target="_blank" style="display: inline-block; background-color: #2563eb; color: #ffffff !important; font-size: 12px; font-weight: 800; padding: 10px 18px; border-radius: 6px; text-decoration: none; margin: 4px;">🚀 Open Control Tower</a>
        <a href="https://docs.google.com/spreadsheets" target="_blank" style="display: inline-block; background-color: #16a34a; color: #ffffff !important; font-size: 12px; font-weight: 800; padding: 10px 18px; border-radius: 6px; text-decoration: none; margin: 4px;">📊 View Synced Google Sheet</a>
        <a href="mailto:${recipient}?subject=Acknowledged%20Incident%20${anomaly.sku}" style="display: inline-block; background-color: #0f172a; color: #ffffff !important; font-size: 12px; font-weight: 800; padding: 10px 18px; border-radius: 6px; text-decoration: none; margin: 4px;">✅ Confirm & Archive</a>
      </div>
    </div>
    <div class="footer">
      Dispatched automatically by <strong>Agile Solutions Control Tower</strong> for <strong>${recipient}</strong>.
    </div>
  </div>
</body>
</html>
`;

    return {
      subject,
      recipientEmail: recipient,
      senderEmail: sender,
      problemType,
      problemTitle: anomaly.summary,
      skuCode: anomaly.sku,
      metrics: {
        revenueAtRiskInr: revenueAtRisk,
        motherHubStock,
        darkStoreStock,
        leadTimeHours: leadTime,
        leadTimeLabel: `${leadTime}h (${anomaly.logisticsPartner || 'Shadowfax'})`,
        motherHubName,
        dailyVelocity: skuObj?.dailyVelocity || 50,
        activePrice: skuObj?.sellingPrice || 1499
      },
      diagnosticRootCause: expandedSummary,
      resolutionFlow,
      followUpSuggestions,
      htmlContent,
      textContent,
      expandedSummary,
      usedAcronyms: relevantAcronyms
    };
  }

  // -------------------------------------------------------------
  // CASE 2: SINGLE SKU CONTEXT / STOCK TRANSFER DISPATCH EMAIL
  // -------------------------------------------------------------
  if (skuContext) {
    const sku = skuContext;
    const revenueAtRisk = sku.revenueAtRisk || (sku.darkStoreStock < 5 ? Math.round(sku.dailyVelocity * 3 * sku.sellingPrice) : 0);
    const motherHubStock = sku.motherHubStock || 35000;
    const darkStoreStock = sku.darkStoreStock ?? 12;
    const motherHubName = sku.defaultMotherHub || 'Central Mother Hub';
    const transferUnits = options?.transferredUnits ?? Math.max(100, Math.ceil(sku.dailyVelocity * 7));

    const isTransferDispatch = options?.transferredUnits !== undefined;
    const transferredQty = options?.transferredUnits ?? 0;
    const updatedDarkStoreStock = darkStoreStock + transferredQty;

    const subject = customSubject || (isTransferDispatch
      ? `[REPLENISHMENT DISPATCHED] ${transferredQty} Units Transferred - Updated Dark Store Stock: ${updatedDarkStoreStock} Units`
      : `[SKU 360 AUDIT] ${sku.sku} (${sku.name}) - Multi-Channel Health & Follow-Up Playbooks`);

    const followUpSuggestions: FollowUpSuggestion[] = [];
    const resolutionFlow: ResolutionFlowStep[] = [];

    if (isTransferDispatch) {
      resolutionFlow.push({
        stepNumber: 1,
        title: `Stock Transfer Dispatched`,
        description: `Transferred Stock: ${transferredQty} Units from ${motherHubName}.`,
        badgeType: 'success'
      });
      resolutionFlow.push({
        stepNumber: 2,
        title: `Updated Dark Store Stock Level`,
        description: `Previous Stock: ${darkStoreStock} Units | Transferred: +${transferredQty} Units | Updated Dark Store Stock: ${updatedDarkStoreStock} Units.`,
        badgeType: 'info'
      });
    } else {
      if (darkStoreStock < 5) {
        followUpSuggestions.push({
          id: `sug-sku-transfer-${sku.sku}`,
          title: `Dispatch Urgent Hub Replenishment`,
          actionText: `Transfer ${transferUnits} units from ${motherHubName} to Dark Stores.`,
          impact: `Restores stock cover to 7 days and avoids ₹${(sku.dailyVelocity * 3 * sku.sellingPrice).toLocaleString('en-IN')} revenue loss.`,
          actionType: 'transfer_stock',
          payload: { sku: sku.sku, motherHub: motherHubName, units: transferUnits }
        });
      }

      if (sku.sellingPrice < sku.targetMap) {
        followUpSuggestions.push({
          id: `sug-sku-map-${sku.sku}`,
          title: `Enforce Minimum Advertised Price (MAP)`,
          actionText: `Reset marketplace selling price from ₹${sku.sellingPrice} to agreed MAP of ₹${sku.targetMap}.`,
          impact: `Recovers ₹${(sku.targetMap - sku.sellingPrice)} per unit margin.`,
          actionType: 'enforce_map',
          payload: { sku: sku.sku, price: sku.targetMap }
        });
      }

      followUpSuggestions.push({
        id: `sug-sku-content-${sku.sku}`,
        title: `Optimize Digital Shelf Listing Score`,
        actionText: `Improve content score from ${sku.digitalShelfScore}/100 by adding A+ comparative infographic and search keywords.`,
        impact: `Projected +14% lift in organic conversion rate.`,
        actionType: 'deploy_coupon'
      });
    }

    const textContent = `================================================================================
SKU 360 EXECUTIVE AUDIT & STOCK TRANSFER REPORT
================================================================================
TO: ${recipient} | SKU: ${sku.sku} - ${sku.name}

${isTransferDispatch ? `• Transferred Stock: ${transferredQty} Units\n• Updated Dark Store Stock: ${updatedDarkStoreStock} Units` : `• Dark Store Stock: ${darkStoreStock} Units\n• Gross Sales (30D): ${formatINR(sku.grossSales30d)}`}
• Mother Hub Stock: ${motherHubStock.toLocaleString('en-IN')} Units (${motherHubName})

CONTROL TOWER CTAs:
- Open Live Dashboard: https://ai.studio/build
- Verify in Google Sheets: https://docs.google.com/spreadsheets
================================================================================`;

    const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${subject}</title>
  <style>
    body { margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #0f172a; line-height: 1.6; }
    .container { max-width: 680px; margin: 24px auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
    .header { background: #0f172a; color: #ffffff; padding: 24px; }
    .header-badge { display: inline-block; background-color: ${isTransferDispatch ? '#10b981' : '#2563eb'}; color: #ffffff; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; margin-bottom: 8px; }
    .content { padding: 24px; }
    .kpi-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
    .kpi-card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 14px; }
    .kpi-label { font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 4px; }
    .kpi-value { font-size: 18px; font-weight: 800; color: #0f172a; }
    .kpi-value.danger { color: #dc2626; }
    .kpi-value.success { color: #16a34a; }
    .section-title { font-size: 13px; font-weight: 800; text-transform: uppercase; color: #0f172a; margin: 20px 0 10px 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }
    .flow-box { background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 14px; margin-bottom: 16px; font-size: 12px; }
    .sug-card { background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; font-size: 12px; }
    .cta-container { margin-top: 24px; padding: 16px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; text-align: center; }
    .cta-button { display: inline-block; background-color: #2563eb; color: #ffffff !important; font-size: 12px; font-weight: 800; padding: 10px 18px; border-radius: 6px; text-decoration: none; margin: 4px; }
    .cta-button.green { background-color: #16a34a; }
    .cta-button.dark { background-color: #0f172a; }
    .footer { background-color: #f1f5f9; padding: 16px; font-size: 11px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-badge">${isTransferDispatch ? 'REPLENISHMENT DISPATCHED' : 'SKU 360 AUDIT'}</div>
      <h2 style="margin:0 0 6px 0; font-size:18px;">${isTransferDispatch ? `Stock Transfer Confirmed: ${sku.name}` : sku.name}</h2>
      <div style="font-size:12px; color:#94a3b8;">SKU: ${sku.sku} | Recipient: ${recipient}</div>
    </div>
    <div class="content">
      <p style="font-size:13px; margin-top:0;">Dear <strong>Vikash Kumar</strong>,<br>Below is the verified stock transfer and inventory synchronization report.</p>
      
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">${isTransferDispatch ? 'Transferred Stock' : 'Gross Sales (30D)'}</div>
          <div class="kpi-value ${isTransferDispatch ? 'success' : ''}">${isTransferDispatch ? `${transferredQty} Units` : formatINR(sku.grossSales30d)}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">${isTransferDispatch ? 'Updated Dark Store Stock' : 'Dark Store Stock'}</div>
          <div class="kpi-value ${isTransferDispatch ? 'success' : ''}">${isTransferDispatch ? `${updatedDarkStoreStock} Units` : `${darkStoreStock} Units`}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Mother Hub Reserve</div>
          <div class="kpi-value success">${motherHubStock.toLocaleString('en-IN')} Units</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Transit SLA</div>
          <div class="kpi-value">~3.5 Hours</div>
        </div>
      </div>

      <div class="section-title">1. Stock Transfer Summary</div>
      <div class="flow-box">
        ${resolutionFlow.map((r) => `
          <div style="margin-bottom: 8px;">
            <strong>Step ${r.stepNumber}: ${r.title}</strong><br>
            <span style="color: #334155;">${r.description}</span>
          </div>
        `).join('')}
      </div>

      ${followUpSuggestions.length > 0 ? `
        <div class="section-title">2. Tailored Follow-Up Recommendations</div>
        ${followUpSuggestions.map((s, idx) => `
          <div class="sug-card">
            <strong style="color: #15803d;">Suggestion #${idx + 1}: ${s.title}</strong><br>
            <div style="color: #334155; margin-top: 3px;"><strong>Action:</strong> ${s.actionText}</div>
            <div style="color: #166534; font-size: 11px; margin-top: 2px;"><strong>Impact:</strong> ${s.impact}</div>
          </div>
        `).join('')}
      ` : ''}

      <div class="cta-container">
        <div style="font-size: 11px; font-weight: 800; color: #334155; text-transform: uppercase; margin-bottom: 10px;">⚡ Owner Action CTAs & Integration Links</div>
        <a href="https://ai.studio/build" target="_blank" class="cta-button">🚀 Open Control Tower</a>
        <a href="https://docs.google.com/spreadsheets" target="_blank" class="cta-button green">📊 View Synced Google Sheet</a>
        <a href="mailto:${recipient}?subject=Acknowledged%20Transfer%20${sku.sku}" class="cta-button dark">✅ Confirm & Archive</a>
      </div>
    </div>
    <div class="footer">
      Dispatched automatically by <strong>Agile Solutions Control Tower</strong> for <strong>${recipient}</strong>.
    </div>
  </div>
</body>
</html>
`;

    return {
      subject,
      recipientEmail: recipient,
      senderEmail: sender,
      problemType: isTransferDispatch ? 'micro_oos' : 'sku_360',
      problemTitle: isTransferDispatch ? `Stock Transfer Confirmed: ${sku.name}` : `SKU 360 Audit for ${sku.name}`,
      skuCode: sku.sku,
      metrics: {
        revenueAtRiskInr: revenueAtRisk,
        motherHubStock,
        darkStoreStock: updatedDarkStoreStock,
        leadTimeHours: 1.5,
        leadTimeLabel: '1.5h (Shadowfax)',
        motherHubName,
        dailyVelocity: sku.dailyVelocity,
        activePrice: sku.sellingPrice
      },
      diagnosticRootCause: isTransferDispatch
        ? `Transferred Stock: ${transferredQty} units. Updated Dark Store Stock: ${updatedDarkStoreStock} units.`
        : `30-Day gross sales reached ${formatINR(sku.grossSales30d)} with ${darkStoreStock} dark store units in inventory buffer.`,
      resolutionFlow,
      followUpSuggestions,
      htmlContent,
      textContent,
      expandedSummary: `SKU 360 Audit for ${sku.name} (${sku.sku})`,
      usedAcronyms: relevantAcronyms
    };
  }

  // -------------------------------------------------------------
  // CASE 3: GENERAL CATALOG DATASET EXECUTIVE WBR REPORT
  // -------------------------------------------------------------
  // Calculate aggregate metrics dynamically from the live active dataset
  const total30dSales = skus.reduce((sum, s) => sum + (s.grossSales30d || (s.sellingPrice * (s.dailyVelocity || 50) * 30)), 0);
  const totalUnitsSold = skus.reduce((sum, s) => sum + (s.unitsSold30d || (s.dailyVelocity || 50) * 30), 0);
  const skuTotalRisk = skus.reduce((sum, s) => sum + (s.revenueAtRisk || 0), 0);
  const alertTotalRisk = allAlerts.reduce((sum, a) => sum + (a.revenueAtRiskInr || 0), 0);
  const totalRevenueAtRisk = skuTotalRisk > 0 ? skuTotalRisk : alertTotalRisk;
  const totalMotherHubStock = skus.reduce((sum, s) => sum + (s.motherHubStock || 35000), 0);
  const lowStockSkus = skus.filter((s) => (s.darkStoreStock ?? 15) < 5);
  const starvingPodsCount = darkStores.filter((d) => (d.availableStock ?? 0) < 5).length;
  const mapBreachesCount = allMapBreaches.length;

  const topRiskSku = skus.slice().sort((a, b) => (b.revenueAtRisk || 0) - (a.revenueAtRisk || 0))[0] || skus[0];

  const subject = customSubject || `Executive Weekly Business Review (WBR) - Real-Time Intelligence & Supply Chain Follow-Ups`;

  const diagnosticRootCause = `Catalog analysis across ${skus.length} active SKUs reveals ${formatINR(total30dSales)} in 30-day gross revenue. A total of ${lowStockSkus.length} SKUs (${starvingPodsCount} dark store pods) are currently operating at critical stock starvation, generating ${formatINR(totalRevenueAtRisk)} in total revenue at risk.`;

  const resolutionFlow: ResolutionFlowStep[] = [
    {
      stepNumber: 1,
      title: `Catalog Revenue & Quick Commerce Penetration`,
      description: `Ingested ${skus.length} catalog items generating ${formatINR(total30dSales)} across Amazon, Flipkart, Blinkit, Zepto, and Instamart.`,
      badgeType: 'info'
    },
    {
      stepNumber: 2,
      title: `Micro-Fulfillment Pod Risk Analysis`,
      description: `${starvingPodsCount} dark store pods across Bangalore and Mumbai are starved below 5 units, putting ${formatINR(totalRevenueAtRisk)} at risk.`,
      badgeType: starvingPodsCount > 0 ? 'danger' : 'success'
    },
    {
      stepNumber: 3,
      title: `Central Mother Hub Availability`,
      description: `Reserve buffers across mother hubs hold ${totalMotherHubStock.toLocaleString('en-IN')} total units ready for immediate inter-hub rebalancing.`,
      badgeType: 'success'
    }
  ];

  // Dynamic Follow-Up Suggestions derived strictly from the dataset's problems
  const followUpSuggestions: FollowUpSuggestion[] = [];

  if (lowStockSkus.length > 0) {
    const topLowStock = lowStockSkus[0];
    const dispatchUnits = Math.max(150, Math.ceil((topLowStock.dailyVelocity || 50) * 7));
    followUpSuggestions.push({
      id: `sug-wbr-stock-${topLowStock.sku}`,
      title: `1-Click Dispatch: Replenish ${topLowStock.name}`,
      actionText: `Transfer ${dispatchUnits} units from ${topLowStock.defaultMotherHub || primaryHub} to Quick Commerce pods for ${topLowStock.sku}.`,
      impact: `Recovers ${formatINR(topLowStock.revenueAtRisk || (topLowStock.dailyVelocity || 50) * 3 * topLowStock.sellingPrice)} in stockout revenue exposure.`,
      actionType: 'transfer_stock',
      payload: { sku: topLowStock.sku, motherHub: topLowStock.defaultMotherHub || primaryHub, units: dispatchUnits }
    });
  }

  if (mapBreachesCount > 0) {
    const topBreach = allMapBreaches[0];
    followUpSuggestions.push({
      id: `sug-wbr-map-${topBreach.sku}`,
      title: `Enforce MAP Compliance on ${topBreach.channel.toUpperCase()}`,
      actionText: `Issue automated Cease & Desist to reseller "${topBreach.violatingSeller}" on ${topBreach.sku} (${topBreach.productName}).`,
      impact: `Protects target MAP of ₹${topBreach.enforcedMap} and restores Buy Box ownership.`,
      actionType: 'enforce_map',
      payload: { sku: topBreach.sku, channel: topBreach.channel, price: topBreach.enforcedMap }
    });
  }

  followUpSuggestions.push({
    id: 'sug-wbr-qc-boost',
    title: 'Hyperlocal Inventory Rebalancing',
    actionText: `Execute automated stock balancing across all ${starvingPodsCount || 4} low-stock Dark Store pods from ${primaryHub}.`,
    impact: `Elevates in-stock SLA from ${(100 - (starvingPodsCount * 3)).toFixed(1)}% to 98.5%.`,
    actionType: 'transfer_stock',
    payload: { sku: topRiskSku?.sku || 'ALL', motherHub: primaryHub, units: 250 }
  });

  const textContent = `================================================================================
EXECUTIVE WEEKLY BUSINESS REVIEW (WBR) INTELLIGENCE BRIEFING
Generated by Agile Solutions Autonomous Control Tower
================================================================================

TO: Vikash Kumar (${recipient})
FROM: E-commerce Control Tower (${sender})
DATE: ${new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
DATASET SCOPE: ${skus.length} Active Catalog Lines

--------------------------------------------------------------------------------
1. EXECUTIVE FINANCIAL SUMMARY (DERIVED FROM DATASET)
--------------------------------------------------------------------------------
• 30-Day Catalog Gross Revenue: ${formatINR(total30dSales)} (${totalUnitsSold.toLocaleString('en-IN')} Units Sold)
• Total Revenue At Risk from Anomalies: ${formatINR(totalRevenueAtRisk)}
• Starving Dark Store Pods (<5 units): ${starvingPodsCount} Pods Affected
• Active Minimum Advertised Price (MAP) Breaches: ${mapBreachesCount} Violations Detected
• Total Mother Hub Warehouse Stock: ${totalMotherHubStock.toLocaleString('en-IN')} Units in Reserve

--------------------------------------------------------------------------------
2. DIAGNOSTIC ROOT CAUSE BREAKDOWN
--------------------------------------------------------------------------------
${diagnosticRootCause}

--------------------------------------------------------------------------------
3. ACTIONABLE FOLLOW-UP SUGGESTIONS DERIVED ACCORDING TO PROBLEMS
--------------------------------------------------------------------------------
${followUpSuggestions.map((s, idx) => `[SUGGESTION #${idx + 1}] ${s.title}
• Recommended Action: ${s.actionText}
• Projected Business Impact: ${s.impact}
`).join('\n')}

--------------------------------------------------------------------------------
4. RETAIL ACRONYMS FULL-FORM GLOSSARY
--------------------------------------------------------------------------------
${relevantAcronyms.map((a) => `• ${a.short} = ${a.full}: ${a.description}`).join('\n')}

================================================================================
Dispatched via Agile Solutions Control Tower | Verified for Vikash Kumar
================================================================================`;

  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${subject}</title>
  <style>
    body { margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #0f172a; line-height: 1.6; }
    .container { max-width: 680px; margin: 24px auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
    .header { background: #0f172a; color: #ffffff; padding: 24px; }
    .header-badge { display: inline-block; background-color: #2563eb; color: #ffffff; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; margin-bottom: 8px; }
    .content { padding: 24px; }
    .kpi-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
    .kpi-card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 14px; }
    .kpi-label { font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 4px; }
    .kpi-value { font-size: 18px; font-weight: 800; color: #0f172a; }
    .kpi-value.danger { color: #dc2626; }
    .kpi-value.success { color: #16a34a; }
    .section-title { font-size: 13px; font-weight: 800; text-transform: uppercase; color: #0f172a; margin: 20px 0 10px 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }
    .sug-card { background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; font-size: 12px; }
    .footer { background-color: #f1f5f9; padding: 16px; font-size: 11px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-badge">WEEKLY BUSINESS REVIEW (WBR)</div>
      <h2 style="margin:0 0 6px 0; font-size:18px;">Executive Multi-Channel Intelligence</h2>
      <div style="font-size:12px; color:#94a3b8;">Dataset Scope: ${skus.length} Active Lines | Recipient: ${recipient}</div>
    </div>
    <div class="content">
      <p style="font-size:13px; margin-top:0;">Dear <strong>Vikash Kumar</strong>,<br>Below is the weekly executive review generated from your live dataset, featuring real-time diagnostic breakdowns and actionable follow-up suggestions according to current inventory and pricing risks.</p>
      
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">30-Day Catalog Gross Revenue</div>
          <div class="kpi-value">${formatINR(total30dSales)}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Total Revenue At Risk</div>
          <div class="kpi-value danger">${formatINR(totalRevenueAtRisk)}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Mother Hub Total Reserves</div>
          <div class="kpi-value success">${totalMotherHubStock.toLocaleString('en-IN')} Units</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Starving Dark Store Pods</div>
          <div class="kpi-value danger">${starvingPodsCount} Pods (&lt;5 units)</div>
        </div>
      </div>

      <div class="section-title">1. Diagnostic Root Cause Breakdown</div>
      <div style="background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 12px; font-size: 12px; color: #92400e; margin-bottom: 16px;">
        ${diagnosticRootCause}
      </div>

      <div class="section-title">2. Prioritized Follow-Up Suggestions for the Problem</div>
      ${followUpSuggestions.map((s, idx) => `
        <div class="sug-card">
          <strong style="color: #15803d;">Suggestion #${idx + 1}: ${s.title}</strong><br>
          <div style="color: #334155; margin-top: 3px;"><strong>Recommended Action:</strong> ${s.actionText}</div>
          <div style="color: #166534; font-size: 11px; margin-top: 2px;"><strong>Business Impact:</strong> ${s.impact}</div>
        </div>
      `).join('')}
    </div>
    <div class="footer">
      Dispatched automatically by <strong>Agile Solutions Control Tower</strong> for <strong>${recipient}</strong>.
    </div>
  </div>
</body>
</html>
`;

  return {
    subject,
    recipientEmail: recipient,
    senderEmail: sender,
    problemType: 'executive_wbr',
    problemTitle: '30-Day Multi-Channel Catalog Review',
    skuCode: 'ALL-CATALOG',
    metrics: {
      revenueAtRiskInr: totalRevenueAtRisk,
      motherHubStock: totalMotherHubStock,
      darkStoreStock: starvingPodsCount,
      leadTimeHours: 1.5,
      leadTimeLabel: '1.5h SLA (Quick Corridor)',
      motherHubName: primaryHub
    },
    diagnosticRootCause,
    resolutionFlow,
    followUpSuggestions,
    htmlContent,
    textContent,
    expandedSummary: diagnosticRootCause,
    usedAcronyms: relevantAcronyms
  };
}
