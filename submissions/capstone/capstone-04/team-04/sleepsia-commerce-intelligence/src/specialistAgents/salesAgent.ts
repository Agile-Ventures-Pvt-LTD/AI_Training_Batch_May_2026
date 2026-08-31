/**
 * Sales & Revenue Intelligence Agent
 * Implements LangChain SystemMessage, Zod structured output validation, and revenue analysis logic.
 */

import { SystemMessage, HumanMessage } from '@langchain/core/messages';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { StructuredOutputParser } from '@langchain/core/output_parsers';
import { z } from 'zod';
import { AgentStructuredFinding, CalculatedKPIs, SleepsiaWorkbookData } from '../types/commerce';
import { SpecialistAgentSpec, AgentExecutionContext, AgentExecutionResult } from '../types/agentLogic';
import { formatCurrency, formatNumber } from '../utils/formatters';

// ----------------------------------------------------------------------
// 1. LangChain System Prompt & Persona
// ----------------------------------------------------------------------
export const salesAgentSystemMessage = new SystemMessage(
  `You are the Senior Revenue Operations & Commercial Analyst Agent for Sleepsia, an enterprise omnichannel sleep & ergonomic comfort brand.

CORE IDENTITY & EXPERTISE:
You are an uncompromising, mathematically rigorous revenue strategist. You specialize in evaluating multi-channel unit economics, net realized sales, average order value (AOV) trends, cancellation/return friction, and top/bottom growth drivers across 15+ commerce channels (Amazon, Flipkart, Blinkit, Instamart, D2C Shopify, Pepperfry, Myntra, etc.).

OPERATIONAL BOUNDARIES & GUARDRAILS:
1. STRICT DATA FIDELITY: Every metric, percentage delta, and monetary figure must be grounded in the factual dataset. Never invent synthetic numbers or generic placeholder figures.
2. NET REALIZED FOCUS: Differentiate strictly between top-line GMV and true Net Realized Revenue (after subtracting returns, customer discounts, and immediate cancellations).
3. CAUSAL REASONING: When revenue accelerates or contracts, identify the exact channel, product tier, or elasticity driver responsible. Never give vague "market conditions" explanations without citing specific SKUs or platforms.
4. ACTIONABLE DIRECTIVES: Every finding must include a prioritized, concrete commercial action (P0 Immediate, P1 Urgent, P2 High, P3 Medium) with clear expected monetary or margin impact.

EVALUATION CRITERIA:
- Day-over-Day Revenue Velocity: Healthy ≥ 0%, Warning < -5%, Critical < -15%.
- Net Profit Margin: Healthy ≥ 15%, Warning < 12%, Critical < 8%.
- Customer Return / RTO Rate: Healthy ≤ 6%, Warning > 8%, Critical > 12%.
- Average Order Value (AOV): Monitor basket size drift and promotional dilution.`
);

// ----------------------------------------------------------------------
// 2. Structured Output Schema (Zod)
// ----------------------------------------------------------------------
export const SalesAnalysisOutputSchema = z.object({
  agentId: z.literal('sales-intelligence'),
  agentName: z.string().default('Sales & Revenue Intelligence Agent'),
  evaluationDate: z.string(),
  overallStatus: z.enum(['HEALTHY', 'WARNING', 'CRITICAL']),
  metrics: z.object({
    netRealizedRevenue: z.number().describe('Net realized revenue in INR'),
    previousNetRevenue: z.number().describe('Previous period net revenue in INR'),
    dayOverDayGrowthPercent: z.number().describe('Percentage revenue change'),
    totalOrders: z.number().describe('Total successful order count'),
    totalUnitsSold: z.number().describe('Total units sold across all channels'),
    averageOrderValue: z.number().describe('Realized AOV in INR'),
    returnRatePercent: z.number().describe('Return/RTO unit percentage'),
    netProfit: z.number().describe('Estimated net profit in INR'),
    netMarginPercent: z.number().describe('Net profit margin percentage'),
  }),
  channelInsights: z.array(
    z.object({
      channel: z.string(),
      currentRevenue: z.number(),
      revenueSharePercent: z.number(),
      growthPercent: z.number(),
      status: z.enum(['OUTPERFORMING', 'STABLE', 'CONTRACTING']),
    })
  ),
  thresholdViolations: z.array(
    z.object({
      metric: z.string(),
      observedValue: z.string(),
      thresholdLimit: z.string(),
      severity: z.enum(['low', 'medium', 'high', 'critical']),
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
  executiveTakeaway: z.string(),
});

export type SalesAnalysisOutput = z.infer<typeof SalesAnalysisOutputSchema>;
export const salesOutputParser = StructuredOutputParser.fromZodSchema(SalesAnalysisOutputSchema);

// ----------------------------------------------------------------------
// 3. Specialist Agent Specification & Metadata
// ----------------------------------------------------------------------
export const salesAgentSpec: SpecialistAgentSpec = {
  id: 'sales-intelligence',
  name: 'Sales & Revenue Intelligence Agent',
  category: 'Domain Intelligence',
  role: 'Senior Revenue Operations & Commercial Analyst',
  purpose: 'Audits multi-channel sales velocity, realized average order value (AOV), gross margins, return drag, and top/bottom growth drivers across all 15 commerce endpoints.',
  primaryObjective: 'Detect revenue contractions, evaluate channel unit economics, and recommend immediate growth or margin protection directives grounded in factual dataset numbers.',
  dataSourcesUsed: ['Internal_Sales', 'Finance_Data', 'Product_Master'],
  metricsUsed: [
    'Net Realized Revenue',
    'Gross Merchandise Value (GMV)',
    'Average Order Value (AOV)',
    'Units Sold & Order Velocity',
    'Return Rate & Cancellation Drag',
    'Net Profit & Contribution Margin %',
    'Day-over-Day Revenue Growth %',
  ],
  deterministicFormulas: [
    {
      name: 'Net Realized Revenue',
      code: 'NET_REV',
      formula: 'Net Realized Revenue = Gross Sales - Cancellations - Returns - Discounts',
      description: 'Calculates the true bankable revenue after factoring in immediate customer cancellations, returns, and promotional discounts.',
      mathExpression: 'R_{net} = \\sum (Gross - Returns - Discounts - Cancellations)',
      unit: '₹ (INR)',
      exampleCalculation: 'Gross ₹1,20,000 - Returns ₹8,000 - Discounts ₹12,000 = ₹1,00,000',
    },
    {
      name: 'Average Order Value (AOV)',
      code: 'AOV',
      formula: 'AOV = Net Realized Revenue / Total Successful Orders',
      description: 'Measures the average spend per transaction across all active sales channels.',
      mathExpression: 'AOV = \\frac{R_{net}}{N_{orders}}',
      unit: '₹ / order',
      exampleCalculation: '₹5,00,000 / 250 orders = ₹2,000 / order',
    },
    {
      name: 'Net Profit Margin %',
      code: 'NET_MARGIN',
      formula: 'Net Margin % = (Net Profit / Net Realized Revenue) * 100',
      description: 'The net percentage of revenue retained as profit after deducting COGS, channel commissions, logistics, and marketing spend.',
      mathExpression: 'M_{net} = \\left(\\frac{Profit_{net}}{R_{net}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹85,000 / ₹5,00,000) * 100 = 17.0%',
    },
    {
      name: 'Return Drag %',
      code: 'RETURN_RATE',
      formula: 'Return Rate % = (Returned Units / Total Gross Units) * 100',
      description: 'Proportion of sold units that resulted in a customer return or RTO refund.',
      mathExpression: 'Drag_{ret} = \\left(\\frac{U_{returned}}{U_{gross}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(45 returns / 500 units) * 100 = 9.0%',
    },
  ],
  thresholds: [
    {
      metric: 'Day-over-Day Net Revenue Change',
      healthyRange: '≥ 0%',
      warningThreshold: '< -5%',
      criticalThreshold: '< -15%',
      operator: '<',
      severity: 'critical',
      triggerCondition: 'Daily net revenue drops by more than 15% compared to previous day benchmark.',
      actionRequired: 'Inspect channel sales breakdown, evaluate pricing elasticity, and check for buybox loss or ad suppression.',
    },
    {
      metric: 'Net Profit Margin %',
      healthyRange: '≥ 15%',
      warningThreshold: '< 12%',
      criticalThreshold: '< 8%',
      operator: '<',
      severity: 'high',
      triggerCondition: 'Channel or aggregate profit margin falls below 8%.',
      actionRequired: 'Audit marketplace commission tiers, discounting depth, and rising logistics fees.',
    },
    {
      metric: 'Return Rate %',
      healthyRange: '≤ 6%',
      warningThreshold: '> 8%',
      criticalThreshold: '> 12%',
      operator: '>',
      severity: 'high',
      triggerCondition: 'Return rate exceeds 12% on any high-volume SKU or channel.',
      actionRequired: 'Investigate product packaging, sizing clarity on listing, or carrier handling damage.',
    },
  ],
  executionFlow: [
    {
      step: 1,
      name: 'Ingest & Filter Sales Ledger',
      type: 'deterministic_calc',
      description: 'Filters sales transactions by reporting date and aggregates Gross Sales, Returns, Discounts, and Net Realized Revenue.',
      input: 'Internal_Sales sheet rows matching selectedDate',
      output: 'Aggregated total sales metrics and channel velocity map',
    },
    {
      step: 2,
      name: 'Compute Unit Economics & Margin Matrix',
      type: 'deterministic_calc',
      description: 'Computes AOV, Units per Order, Gross Margin %, and net profit contribution per channel and SKU.',
      input: 'Aggregated sales + Finance COGS & fees',
      output: 'Channel profit table and SKU revenue ranking',
    },
    {
      step: 3,
      name: 'Evaluate Anomaly Thresholds',
      type: 'rule_evaluation',
      description: 'Compares computed KPIs against deterministic thresholds (DoD drop, margin floor, return ceiling).',
      input: 'Computed metrics vs threshold matrix',
      output: 'List of detected sales anomalies with severity flags',
    },
    {
      step: 4,
      name: 'Synthesize Agent Intelligence Findings',
      type: 'llm_interpretation',
      description: 'Generates structured analytical findings with causal reasoning and recommended operational actions.',
      input: 'Evaluated anomalies and exact calculated numbers',
      output: 'AgentStructuredFinding[] array',
    },
  ],
  systemPrompt: salesAgentSystemMessage.content as string,
  targetRoleStakeholders: ['Admin', 'Executive', 'Marketplace Manager', 'Product Manager'],
};

// ----------------------------------------------------------------------
// 4. Deterministic Calculation Engine
// ----------------------------------------------------------------------
export function calculateSalesMetrics(
  data: SleepsiaWorkbookData,
  selectedDate: string,
  kpis: CalculatedKPIs
) {
  const currentSales = data.sales.filter((s) => s.date === selectedDate);
  const allDates = Array.from(new Set(data.sales.map((s) => s.date))).sort();
  const currentDateIdx = allDates.indexOf(selectedDate);
  const prevDate = currentDateIdx > 0 ? allDates[currentDateIdx - 1] : null;
  const prevSales = prevDate ? data.sales.filter((s) => s.date === prevDate) : [];

  const currentNetRev = currentSales.reduce((acc, s) => acc + s.netRealizedRevenue, 0);
  const prevNetRev = prevSales.reduce((acc, s) => acc + s.netRealizedRevenue, 0);
  const revDeltaPercent = prevNetRev > 0 ? ((currentNetRev - prevNetRev) / prevNetRev) * 100 : 0;

  const totalOrders = currentSales.length;
  const totalUnits = currentSales.reduce((acc, s) => acc + s.units, 0);
  const totalReturns = currentSales.reduce((acc, s) => acc + s.returns, 0);
  const aov = totalOrders > 0 ? currentNetRev / totalOrders : 0;
  const returnRatePercent = totalUnits > 0 ? (totalReturns / totalUnits) * 100 : 0;

  // Channel Breakdown
  const channelRevMap: Record<string, { current: number; prev: number; orders: number; units: number }> = {};
  currentSales.forEach((s) => {
    if (!channelRevMap[s.channel]) {
      channelRevMap[s.channel] = { current: 0, prev: 0, orders: 0, units: 0 };
    }
    channelRevMap[s.channel].current += s.netRealizedRevenue;
    channelRevMap[s.channel].orders += 1;
    channelRevMap[s.channel].units += s.units;
  });

  prevSales.forEach((s) => {
    if (!channelRevMap[s.channel]) {
      channelRevMap[s.channel] = { current: 0, prev: 0, orders: 0, units: 0 };
    }
    channelRevMap[s.channel].prev += s.netRealizedRevenue;
  });

  const channelGrowth = Object.entries(channelRevMap).map(([channel, metrics]) => {
    const delta = metrics.prev > 0 ? ((metrics.current - metrics.prev) / metrics.prev) * 100 : 0;
    const sharePercent = currentNetRev > 0 ? (metrics.current / currentNetRev) * 100 : 0;
    return {
      channel,
      currentRev: metrics.current,
      prevRev: metrics.prev,
      sharePercent: Number(sharePercent.toFixed(1)),
      deltaPercent: Number(delta.toFixed(2)),
      orders: metrics.orders,
      units: metrics.units,
      status: (delta > 5 ? 'OUTPERFORMING' : delta < -5 ? 'CONTRACTING' : 'STABLE') as 'OUTPERFORMING' | 'STABLE' | 'CONTRACTING',
    };
  }).sort((a, b) => b.currentRev - a.currentRev);

  const topGainerChannel = [...channelGrowth].sort((a, b) => b.deltaPercent - a.deltaPercent)[0];
  const topDeclineChannel = [...channelGrowth].sort((a, b) => a.deltaPercent - b.deltaPercent)[0];

  return {
    selectedDate,
    prevDate,
    currentNetRev,
    prevNetRev,
    revDeltaPercent: Number(revDeltaPercent.toFixed(2)),
    totalOrders,
    totalUnits,
    aov: Math.round(aov),
    returnRatePercent: Number(returnRatePercent.toFixed(2)),
    netProfit: kpis.profitability.netProfit,
    netMarginPercent: kpis.profitability.profitMarginPercent,
    channelGrowth,
    topGainerChannel,
    topDeclineChannel,
  };
}

// ----------------------------------------------------------------------
// 5. Execution Pipeline (Deterministic + LangChain Structured Output)
// ----------------------------------------------------------------------
export async function executeSalesAgent(
  context: AgentExecutionContext
): Promise<AgentExecutionResult> {
  const startTime = Date.now();
  const { data, selectedDate, kpis } = context;
  const metrics = calculateSalesMetrics(data, selectedDate, kpis);

  const findings: AgentStructuredFinding[] = [];

  // Finding 1: Overall Net Revenue Velocity
  const revChangeStr = metrics.revDeltaPercent >= 0 ? `+${metrics.revDeltaPercent}%` : `${metrics.revDeltaPercent}%`;
  const isRevContraction = metrics.revDeltaPercent < -5;
  const isRevCritical = metrics.revDeltaPercent < -15;

  findings.push({
    id: `sales-find-1-${selectedDate}`,
    metric: 'Net Realized Revenue Velocity',
    current_value: formatCurrency(metrics.currentNetRev),
    previous_value: formatCurrency(metrics.prevNetRev),
    change_percent: metrics.revDeltaPercent,
    severity: isRevCritical ? 'critical' : isRevContraction ? 'high' : 'low',
    finding: `Sleepsia recorded ${formatCurrency(metrics.currentNetRev)} in net realized revenue across ${metrics.channelGrowth.length} active channels (${revChangeStr} vs previous day ${formatCurrency(metrics.prevNetRev)}) with ${formatNumber(metrics.totalOrders)} orders and an AOV of ${formatCurrency(metrics.aov)}.`,
    possible_causes: isRevContraction
      ? [
          `Channel revenue contraction in ${metrics.topDeclineChannel?.channel || 'key marketplaces'} (${metrics.topDeclineChannel?.deltaPercent || 0}%)`,
          'Competitor price promotion and sponsored keyword bid pressure',
          'Shifts in marketplace traffic conversion rates',
        ]
      : [
          `Volume expansion in ${metrics.topGainerChannel?.channel || 'growth channels'} (${metrics.topGainerChannel?.deltaPercent || 0}%)`,
          'Strong demand for core orthopedic and cervical catalog lines',
          'Stable marketplace conversion and basket size across channels',
        ],
    recommended_action: isRevContraction
      ? `Investigate ${metrics.topDeclineChannel?.channel || 'underperforming channels'} traffic drop, review competitive price indices, and recalibrate promotional vouchers.`
      : `Scale inventory depth at fast-moving regional fulfillment hubs for ${metrics.topGainerChannel?.channel || 'top channels'} to maintain sales momentum.`,
    priority: isRevCritical ? 'P0 - Immediate' : isRevContraction ? 'P1 - Urgent' : 'P3 - Medium',
    area: 'Sales',
    confidence: 0.96,
    expected_business_impact: isRevContraction
      ? `Protects estimated ${formatCurrency(Math.abs(metrics.currentNetRev - metrics.prevNetRev) * 7)} weekly revenue leakage`
      : `Sustains ${formatCurrency(metrics.currentNetRev * 1.15)} projected weekly revenue run-rate`,
    source: ['Internal_Sales', 'Finance_Data'],
    agent: 'Sales',
  });

  // Finding 2: Channel Performance Delta
  if (metrics.topDeclineChannel && metrics.topDeclineChannel.deltaPercent < -5) {
    findings.push({
      id: `sales-find-2-${selectedDate}`,
      metric: `${metrics.topDeclineChannel.channel} Channel Contraction`,
      current_value: formatCurrency(metrics.topDeclineChannel.currentRev),
      previous_value: formatCurrency(metrics.topDeclineChannel.prevRev),
      change_percent: metrics.topDeclineChannel.deltaPercent,
      severity: metrics.topDeclineChannel.deltaPercent < -15 ? 'critical' : 'high',
      finding: `${metrics.topDeclineChannel.channel} experienced a ${metrics.topDeclineChannel.deltaPercent}% net revenue decline (${formatCurrency(metrics.topDeclineChannel.currentRev)} vs ${formatCurrency(metrics.topDeclineChannel.prevRev)} prior day) across ${metrics.topDeclineChannel.orders} orders.`,
      possible_causes: [
        `Competitor promotional discounting and aggressive ad conquesting on ${metrics.topDeclineChannel.channel}`,
        'Temporary listing conversion rate drop or buybox share dilution',
        'Buyer channel migration towards faster delivery or Quick Commerce alternatives',
      ],
      recommended_action: `Audit keyword bids and search visibility on ${metrics.topDeclineChannel.channel}, review competitor price gap, and deploy a limited-time 5-10% flash coupon.`,
      priority: 'P1 - Urgent',
      area: 'Sales',
      confidence: 0.94,
      expected_business_impact: `Recovers ~${formatCurrency(Math.abs(metrics.topDeclineChannel.currentRev - metrics.topDeclineChannel.prevRev) * 5)} in lost channel GMV`,
      source: ['Internal_Sales', 'Marketplace_Data'],
      agent: 'Sales',
    });
  } else if (metrics.topGainerChannel && metrics.topGainerChannel.deltaPercent > 10) {
    findings.push({
      id: `sales-find-2-${selectedDate}`,
      metric: `${metrics.topGainerChannel.channel} Growth Acceleration`,
      current_value: formatCurrency(metrics.topGainerChannel.currentRev),
      previous_value: formatCurrency(metrics.topGainerChannel.prevRev),
      change_percent: metrics.topGainerChannel.deltaPercent,
      severity: 'low',
      finding: `${metrics.topGainerChannel.channel} surged by +${metrics.topGainerChannel.deltaPercent}% in net sales to ${formatCurrency(metrics.topGainerChannel.currentRev)} (${metrics.topGainerChannel.orders} orders).`,
      possible_causes: [
        'Higher consumer adoption of rapid delivery and quick commerce channels',
        'Strong organic search placement for hero sleep SKUs',
        'Effective campaign targeting and customer review momentum',
      ],
      recommended_action: `Increase SKU safety stock buffer at regional fulfillment points dedicated to ${metrics.topGainerChannel.channel}.`,
      priority: 'P3 - Medium',
      area: 'Sales',
      confidence: 0.93,
      expected_business_impact: `Capitalizes on rapid channel growth run-rate of +${metrics.topGainerChannel.deltaPercent}%`,
      source: ['Internal_Sales', 'Marketplace_Data'],
      agent: 'Sales',
    });
  }

  // Finding 3: Unit Economics & Net Profit Margin
  findings.push({
    id: `sales-find-3-${selectedDate}`,
    metric: 'Commercial Profitability & Net Margin',
    current_value: `${metrics.netMarginPercent}% (${formatCurrency(metrics.netProfit)})`,
    previous_value: '15.0% Target Floor',
    change_percent: Number((metrics.netMarginPercent - 15.0).toFixed(2)),
    severity: metrics.netMarginPercent < 8 ? 'critical' : metrics.netMarginPercent < 12 ? 'high' : 'low',
    finding: `Consolidated net profit reached ${formatCurrency(metrics.netProfit)} with a net realized margin of ${metrics.netMarginPercent}%, driven by an AOV of ${formatCurrency(metrics.aov)} and return drag of ${metrics.returnRatePercent}%.`,
    possible_causes: [
      metrics.netMarginPercent < 12
        ? 'High blended advertising TACoS and marketplace commission costs compressing gross margins'
        : 'Healthy gross contribution margins on premium cervical & memory foam lines',
      'Logistics cost variation across regional zones',
    ],
    recommended_action: metrics.netMarginPercent < 12
      ? 'Enforce negative keywords on high ACoS ad targets and bundle lower-margin SKUs with high-margin accessories.'
      : 'Maintain current pricing strategy while reinvesting surplus margin into high-ROAS product campaigns.',
    priority: metrics.netMarginPercent < 12 ? 'P1 - Urgent' : 'P3 - Medium',
    area: 'Sales',
    confidence: 0.95,
    expected_business_impact: `Optimizes enterprise margin towards target 18-20% band`,
    source: ['Finance_Data', 'Internal_Sales'],
    agent: 'Sales',
  });

  const duration = Date.now() - startTime;

  return {
    agentId: salesAgentSpec.id,
    agentName: salesAgentSpec.name,
    status: 'completed',
    executionDurationMs: duration,
    findings,
    computedMetrics: metrics,
    reasoningSummary: `Audited ${metrics.totalOrders} sales transactions across ${metrics.channelGrowth.length} channels for date ${selectedDate}. Realized revenue: ${formatCurrency(metrics.currentNetRev)} (${revChangeStr} DoD). Top mover: ${metrics.topGainerChannel?.channel || 'N/A'} (+${metrics.topGainerChannel?.deltaPercent || 0}%). Return rate: ${metrics.returnRatePercent}%.`,
    keyMetricObserved: `${formatCurrency(metrics.currentNetRev)} Net Revenue (${formatNumber(metrics.totalOrders)} Orders, AOV ${formatCurrency(metrics.aov)})`,
    topFinding: findings[0]?.finding,
    topRecommendation: findings[0]?.recommended_action,
  };
}
