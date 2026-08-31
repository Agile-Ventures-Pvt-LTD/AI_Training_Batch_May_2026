/**
 * Marketplace Channel Allocation & Quick Commerce Intelligence Agent
 * Implements LangChain SystemMessage, Zod structured output validation, and channel economics analysis.
 */

import { SystemMessage } from '@langchain/core/messages';
import { StructuredOutputParser } from '@langchain/core/output_parsers';
import { z } from 'zod';
import { AgentStructuredFinding, CalculatedKPIs, SleepsiaWorkbookData } from '../types/commerce';
import { SpecialistAgentSpec, AgentExecutionContext, AgentExecutionResult } from '../types/agentLogic';
import { formatCurrency, formatNumber } from '../utils/formatters';

// ----------------------------------------------------------------------
// 1. LangChain System Prompt & Persona
// ----------------------------------------------------------------------
export const marketplaceAgentSystemMessage = new SystemMessage(
  `You are the Head of Omnichannel & Marketplace Operations Agent for Sleepsia, overseeing 14+ enterprise commerce channels (Amazon India, Flipkart, Blinkit, Instamart, Zepto, Myntra, FirstCry, Nykaa, Meesho, JioMart, Pepperfry, Sleepbee, Tata 1mg, MyStore ONDC, and D2C Shopify).

CORE IDENTITY & EXPERTISE:
You are an expert in omnichannel channel allocation, marketplace fee structures, buybox dynamics, and the rapid evolution of Quick Commerce (10-20 minute hyperlocal delivery). You audit net margin retention after platform take-rates, commission tiers, and fulfillment charges.

OPERATIONAL BOUNDARIES & GUARDRAILS:
1. PLATFORM TAKE-RATE SCRUTINY: Monitor total marketplace fee drag (commissions + collection fees + platform logistics). Flag any channel where fee drag exceeds 25% of gross revenue.
2. CHANNEL CONCENTRATION RISK: Guard against over-reliance on a single marketplace (e.g. Amazon or Flipkart > 65% volume share).
3. QUICK COMMERCE EXPANSION: Track dark store replenishment velocity and 10-minute delivery penetration for high-impulse travel and ergonomic items.
4. STRICT GROUNDING: Every channel GMV, share percentage, and order count must match the exact Sleepsia workbook transaction rows.

EVALUATION CRITERIA:
- Single Channel Concentration Risk: Healthy < 50%, Warning 50%-65%, Critical > 65%.
- Channel Take-Rate / Fee Drag: Healthy < 18%, Warning 18%-24%, Critical > 25%.
- Quick Commerce Revenue Share: Target ≥ 12% of daily consumer volume.`
);

// ----------------------------------------------------------------------
// 2. Structured Output Schema (Zod)
// ----------------------------------------------------------------------
export const MarketplaceAnalysisOutputSchema = z.object({
  agentId: z.literal('marketplace-intelligence'),
  agentName: z.string().default('Marketplace Channel Intelligence Agent'),
  evaluationDate: z.string(),
  overallStatus: z.enum(['HEALTHY', 'WARNING', 'CRITICAL']),
  metrics: z.object({
    totalNetRevenue: z.number(),
    activeChannelsCount: z.number(),
    topChannelName: z.string(),
    topChannelSharePercent: z.number(),
    quickCommerceRevenue: z.number(),
    quickCommerceSharePercent: z.number(),
    averagePlatformCommissionPercent: z.number(),
  }),
  channelRankings: z.array(
    z.object({
      platform: z.string(),
      netRevenue: z.number(),
      grossRevenue: z.number(),
      sharePercent: z.number(),
      orders: z.number(),
      units: z.number(),
      returns: z.number(),
      commissionRatePercent: z.number(),
      riskFlag: z.string().optional(),
    })
  ),
  structuredFindings: z.array(
    z.object({
      id: z.string(),
      metric: z.string(),
      current_value: z.string(),
      previous_value: z.string(),
      change_percent: z.number(),
      severity: z.enum(['low', 'medium', 'high', 'critical']),
      finding: z.string(),
      possible_causes: z.array(z.string()),
      recommended_action: z.string(),
      priority: z.enum(['P0 - Immediate', 'P1 - Urgent', 'P2 - High', 'P3 - Medium']),
      area: z.literal('Sales'),
      confidence: z.number(),
      expected_business_impact: z.string(),
    })
  ),
  strategicAllocationDirectives: z.array(z.string()),
});

export type MarketplaceAnalysisOutput = z.infer<typeof MarketplaceAnalysisOutputSchema>;
export const marketplaceOutputParser = StructuredOutputParser.fromZodSchema(MarketplaceAnalysisOutputSchema);

// ----------------------------------------------------------------------
// 3. Specialist Agent Specification & Metadata
// ----------------------------------------------------------------------
export const marketplaceAgentSpec: SpecialistAgentSpec = {
  id: 'marketplace-intelligence',
  name: 'Marketplace Channel Intelligence Agent',
  category: 'Domain Intelligence',
  role: 'Head of Omnichannel & Marketplace Operations',
  purpose: 'Monitors channel-by-channel sales volume, net margin retention, commission fee structures, and quick commerce velocity across Amazon, Flipkart, Blinkit, Instamart, Myntra, FirstCry, Nykaa, Meesho, JioMart, Pepperfry, Sleepbee, Tata 1mg, MyStore / ONDC, and D2C.',
  primaryObjective: 'Optimize channel mix, maximize net payout percentage, expand quick-commerce availability, and detect channel cannibalization.',
  dataSourcesUsed: ['Marketplace_Data', 'Marketplace_Master', 'Internal_Sales', 'Finance_Data'],
  metricsUsed: [
    'Channel GMV & Net Revenue (₹)',
    'Channel Volume Share %',
    'Platform Take-Rate / Fee Drag %',
    'Quick Commerce Revenue Contribution %',
    'Marketplace Product Rating & Search Position',
    'Channel Payout Settlement Timeline (Days)',
  ],
  deterministicFormulas: [
    {
      name: 'Channel Revenue Contribution Share %',
      code: 'CHAN_SHARE',
      formula: 'Channel Share % = (Channel Net Revenue / Total Enterprise Net Revenue) * 100',
      description: 'Calculates the proportion of total enterprise realized revenue driven by an individual marketplace.',
      mathExpression: 'Share_{channel} = \\left(\\frac{Rev_{channel}}{Rev_{total}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹2,50,000 / ₹5,75,000) * 100 = 43.48%',
    },
    {
      name: 'Channel Net Fee Drag %',
      code: 'FEE_DRAG',
      formula: 'Fee Drag % = (Marketplace Fees + Commission / Channel Gross Revenue) * 100',
      description: 'The effective percentage of top-line revenue consumed by platform take-rates, commissions, and fulfillment charges.',
      mathExpression: 'Drag_{fee} = \\left(\\frac{Fees_{platform} + Comm_{platform}}{GMV_{channel}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹30,000 / ₹1,50,000) * 100 = 20.0%',
    },
    {
      name: 'Quick Commerce Growth Share %',
      code: 'QCOMM_SHARE',
      formula: 'Q-Comm Share % = ((Blinkit + Instamart + Zepto) Net Revenue / Total Net Revenue) * 100',
      description: 'Tracks ultra-fast 10-20 minute delivery channel penetration across dark store networks.',
      mathExpression: 'Share_{qcomm} = \\left(\\frac{Rev_{blinkit} + Rev_{instamart} + Rev_{zepto}}{Rev_{total}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹85,000 / ₹5,75,000) * 100 = 14.78%',
    },
  ],
  thresholds: [
    {
      metric: 'Single Channel Concentration Risk',
      healthyRange: '< 50%',
      warningThreshold: '50% - 65%',
      criticalThreshold: '> 65%',
      operator: '>',
      severity: 'high',
      triggerCondition: 'A single marketplace contributes > 65% of total enterprise sales volume.',
      actionRequired: 'Diversify ad spend into Quick Commerce and D2C to reduce platform dependency.',
    },
    {
      metric: 'Channel Marketplace Fee Drag %',
      healthyRange: '< 18%',
      warningThreshold: '18% - 24%',
      criticalThreshold: '> 25%',
      operator: '>',
      severity: 'critical',
      triggerCondition: 'Platform take-rate and commissions exceed 25% of channel GMV.',
      actionRequired: 'Audit tier-based commission fee categories and re-negotiate logistic service tiers.',
    },
  ],
  executionFlow: [
    {
      step: 1,
      name: 'Segment Marketplace Sales Records',
      type: 'deterministic_calc',
      description: 'Aggregates sales, orders, units, and fees per platform for the reporting date.',
      input: 'Marketplace_Data and Internal_Sales tables',
      output: 'Channel performance ledger table',
    },
    {
      step: 2,
      name: 'Calculate Channel Mix & Margin Drag',
      type: 'deterministic_calc',
      description: 'Computes channel share %, take-rate %, and quick commerce growth contribution.',
      input: 'Channel ledger table',
      output: 'Channel efficiency matrix',
    },
    {
      step: 3,
      name: 'Evaluate Channel Risk Thresholds',
      type: 'rule_evaluation',
      description: 'Checks for excessive channel concentration (> 65%) or negative margin channels.',
      input: 'Channel efficiency matrix vs thresholds',
      output: 'List of marketplace channel anomaly triggers',
    },
    {
      step: 4,
      name: 'Generate Channel Allocation Strategy',
      type: 'llm_interpretation',
      description: 'Synthesizes channel rebalancing advice, fee negotiation points, and stock priority.',
      input: 'Evaluated channel metrics and anomalies',
      output: 'AgentStructuredFinding[] array',
    },
  ],
  systemPrompt: marketplaceAgentSystemMessage.content as string,
  targetRoleStakeholders: ['Admin', 'Executive', 'Marketplace Manager'],
};

// ----------------------------------------------------------------------
// 4. Deterministic Calculation Engine
// ----------------------------------------------------------------------
export function calculateMarketplaceMetrics(
  data: SleepsiaWorkbookData,
  selectedDate: string,
  kpis: CalculatedKPIs
) {
  const currentSales = data.sales.filter((s) => s.date === selectedDate);
  const totalNetRev = currentSales.reduce((acc, s) => acc + s.netRealizedRevenue, 0) || 1;

  const channelMap: Record<string, { orders: number; units: number; netRev: number; grossRev: number; returns: number }> = {};
  currentSales.forEach((s) => {
    if (!channelMap[s.channel]) {
      channelMap[s.channel] = { orders: 0, units: 0, netRev: 0, grossRev: 0, returns: 0 };
    }
    channelMap[s.channel].orders += 1;
    channelMap[s.channel].units += s.units;
    channelMap[s.channel].netRev += s.netRealizedRevenue;
    channelMap[s.channel].grossRev += s.grossSales;
    channelMap[s.channel].returns += s.returns;
  });

  const channelBreakdown = Object.entries(channelMap).map(([platform, m]) => {
    const sharePercent = Number(((m.netRev / totalNetRev) * 100).toFixed(1));
    const mktMaster = data.marketplaceMasters.find((mm) => mm.platform === platform);
    const commRatePercent = mktMaster ? Number((mktMaster.commissionRate * 100).toFixed(1)) : 15.0;

    return {
      platform,
      orders: m.orders,
      units: m.units,
      netRev: m.netRev,
      grossRev: m.grossRev,
      returns: m.returns,
      sharePercent,
      commRatePercent,
    };
  }).sort((a, b) => b.netRev - a.netRev);

  // Quick commerce aggregation
  const qcommChannels = ['Blinkit', 'Instamart', 'Zepto'];
  const qcommRev = channelBreakdown
    .filter((c) => qcommChannels.some((qc) => c.platform.toLowerCase().includes(qc.toLowerCase())))
    .reduce((acc, c) => acc + c.netRev, 0);
  const qcommSharePercent = Number(((qcommRev / totalNetRev) * 100).toFixed(1));

  const topChannel = channelBreakdown[0];
  const activeChannelsCount = channelBreakdown.length;

  return {
    selectedDate,
    totalNetRev,
    activeChannelsCount,
    channelBreakdown,
    topChannel,
    qcommRev,
    qcommSharePercent,
  };
}

// ----------------------------------------------------------------------
// 5. Execution Pipeline
// ----------------------------------------------------------------------
export async function executeMarketplaceAgent(
  context: AgentExecutionContext
): Promise<AgentExecutionResult> {
  const startTime = Date.now();
  const { data, selectedDate, kpis } = context;
  const metrics = calculateMarketplaceMetrics(data, selectedDate, kpis);

  const findings: AgentStructuredFinding[] = [];

  // Finding 1: Top Channel Concentration & Share
  if (metrics.topChannel) {
    const isConcentrationHigh = metrics.topChannel.sharePercent > 55;
    findings.push({
      id: `mkt-find-1-${selectedDate}`,
      metric: `${metrics.topChannel.platform} Channel Share & Performance`,
      current_value: `${metrics.topChannel.sharePercent}% Share (${formatCurrency(metrics.topChannel.netRev)})`,
      previous_value: '45.0% Baseline Target Share',
      change_percent: Number((metrics.topChannel.sharePercent - 45.0).toFixed(1)),
      severity: isConcentrationHigh ? 'high' : 'low',
      finding: `${metrics.topChannel.platform} is the top revenue channel generating ${formatCurrency(metrics.topChannel.netRev)} (${metrics.topChannel.sharePercent}% of total sales) across ${metrics.topChannel.orders} orders.`,
      possible_causes: [
        `High marketplace search visibility and brand store traffic on ${metrics.topChannel.platform}`,
        'Concentrated promotional focus and listing optimization',
      ],
      recommended_action: isConcentrationHigh
        ? `Scale inventory allocation to Quick Commerce (Blinkit / Instamart) and D2C to balance channel concentration below 50%.`
        : `Maintain strong listing content scores and prime fulfillment speed on ${metrics.topChannel.platform}.`,
      priority: isConcentrationHigh ? 'P2 - High' : 'P3 - Medium',
      area: 'Sales',
      confidence: 0.95,
      expected_business_impact: `Optimizes channel contribution and mitigates single-marketplace platform risk`,
      source: ['Marketplace_Data', 'Internal_Sales'],
      agent: 'Sales',
    });
  }

  // Finding 2: Quick Commerce Penetration
  if (metrics.qcommRev > 0) {
    findings.push({
      id: `mkt-find-2-${selectedDate}`,
      metric: 'Quick Commerce Growth Velocity',
      current_value: `${metrics.qcommSharePercent}% Share (${formatCurrency(metrics.qcommRev)})`,
      previous_value: '10.0% Q-Comm Target Share',
      change_percent: Number((metrics.qcommSharePercent - 10.0).toFixed(1)),
      severity: metrics.qcommSharePercent >= 10 ? 'low' : 'medium',
      finding: `Quick Commerce channels (Blinkit & Instamart) generated ${formatCurrency(metrics.qcommRev)} representing ${metrics.qcommSharePercent}% of daily sales volume.`,
      possible_causes: [
        'Surge in localized 10-minute delivery demand for travel neck pillows and eye masks',
        'Expanding dark store presence in Tier-1 metropolitan hubs',
      ],
      recommended_action: 'Increase dedicated dark store replenishment frequency to 48-hour cycles to prevent stockouts in high-velocity micro-fulfillment centers.',
      priority: 'P2 - High',
      area: 'Sales',
      confidence: 0.93,
      expected_business_impact: `Unlocks estimated +₹40,000 additional weekly GMV from quick commerce impulsive purchases`,
      source: ['Marketplace_Data', 'Internal_Sales'],
      agent: 'Sales',
    });
  }

  const duration = Date.now() - startTime;

  return {
    agentId: 'marketplace-intelligence',
    agentName: marketplaceAgentSpec.name,
    status: 'completed',
    executionDurationMs: duration,
    findings,
    computedMetrics: metrics,
    reasoningSummary: `Evaluated ${metrics.activeChannelsCount} active commerce channels for date ${selectedDate}. Top channel: ${metrics.topChannel?.platform || 'N/A'} (${metrics.topChannel?.sharePercent || 0}% share). Quick commerce contribution: ${metrics.qcommSharePercent}% (${formatCurrency(metrics.qcommRev)}).`,
    keyMetricObserved: `${metrics.activeChannelsCount} Active Channels (${metrics.topChannel?.platform || 'Amazon'}: ${metrics.topChannel?.sharePercent || 0}%, Q-Comm: ${metrics.qcommSharePercent}%)`,
    topFinding: findings[0]?.finding,
    topRecommendation: findings[0]?.recommended_action,
  };
}
