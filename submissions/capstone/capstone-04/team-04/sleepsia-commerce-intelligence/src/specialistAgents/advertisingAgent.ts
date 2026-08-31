/**
 * Advertising & Performance Marketing Agent
 * Implements LangChain SystemMessage, Zod structured output validation, and PPC/TACoS optimization logic.
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
export const advertisingAgentSystemMessage = new SystemMessage(
  `You are the Principal Growth Marketer & PPC Strategy Lead Agent for Sleepsia.

CORE IDENTITY & EXPERTISE:
You specialize in omnichannel performance marketing, sponsored search bidding, ad attribution, and profit-first paid media management across Amazon Sponsored Products/Brands, Flipkart PLA/PCA, Google Ads (Search/PMax), and Meta Ads.

OPERATIONAL BOUNDARIES & GUARDRAILS:
1. MARGIN-PROTECTIVE PPC: Always analyze ad spend relative to gross margin. Never celebrate high ROAS if TACoS is eroding enterprise net profitability.
2. BLEEDING TARGET IDENTIFICATION: Detect low-converting broad search terms, negative ROI product targets, and out-of-control CPC spikes.
3. ORGANIC CANNIBALIZATION AUDIT: Differentiate between incremental ad conversions and defensive bidding on branded keywords that cannibalize organic sales.
4. STRICT MATHEMATICAL TRUTH: Compute exact ROAS (Attributed Revenue / Spend), ACoS (Spend / Attributed Revenue * 100), and TACoS (Spend / Total Net Revenue * 100) directly from dataset entries.

EVALUATION CRITERIA:
- Blended Portfolio ROAS: Healthy ≥ 3.50x, Warning < 3.00x, Critical < 2.20x.
- Campaign ACoS %: Healthy ≤ 28%, Warning > 35%, Critical > 45%.
- Total Brand TACoS %: Healthy ≤ 12%, Warning > 15%, Critical > 20%.`
);

// ----------------------------------------------------------------------
// 2. Structured Output Schema (Zod)
// ----------------------------------------------------------------------
export const AdvertisingAnalysisOutputSchema = z.object({
  agentId: z.literal('advertising-intelligence'),
  agentName: z.string().default('Advertising & Performance Marketing Agent'),
  evaluationDate: z.string(),
  overallStatus: z.enum(['HEALTHY', 'WARNING', 'CRITICAL']),
  metrics: z.object({
    totalAdSpend: z.number(),
    attributedAdRevenue: z.number(),
    blendedRoas: z.number(),
    blendedAcosPercent: z.number(),
    tacosPercent: z.number(),
    totalClicks: z.number(),
    averageCpc: z.number(),
    conversionRatePercent: z.number(),
    organicContributionPercent: z.number(),
  }),
  campaignPerformance: z.array(
    z.object({
      campaignName: z.string(),
      platform: z.string(),
      spend: z.number(),
      revenue: z.number(),
      roas: z.number(),
      acosPercent: z.number(),
      efficiency: z.enum(['HIGH_EFFICIENCY', 'ACCEPTABLE', 'BLEEDING']),
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
      area: z.literal('Advertising'),
      confidence: z.number(),
      expected_business_impact: z.string(),
    })
  ),
  bidDirectives: z.array(
    z.object({
      targetCampaign: z.string(),
      action: z.enum(['INCREASE_BUDGET', 'REDUCE_BID', 'PAUSE_TARGET', 'ADD_NEGATIVE_KEYWORD']),
      reason: z.string(),
    })
  ),
});

export type AdvertisingAnalysisOutput = z.infer<typeof AdvertisingAnalysisOutputSchema>;
export const advertisingOutputParser = StructuredOutputParser.fromZodSchema(AdvertisingAnalysisOutputSchema);

// ----------------------------------------------------------------------
// 3. Specialist Agent Specification & Metadata
// ----------------------------------------------------------------------
export const advertisingAgentSpec: SpecialistAgentSpec = {
  id: 'advertising-intelligence',
  name: 'Advertising & Performance Marketing Agent',
  category: 'Domain Intelligence',
  role: 'Principal Growth Marketer & PPC Strategy Lead',
  purpose: 'Monitors ad spend across Amazon PPC, Flipkart Ads, Meta, and Google Ads, evaluating Return on Ad Spend (ROAS), Advertising Cost of Sales (ACoS), Total ACoS (TACoS), and keyword efficiency.',
  primaryObjective: 'Maximize blended ROAS, curb wasteful broad-match keyword bidding, and optimize the ratio between paid acquisition and organic baseline sales.',
  dataSourcesUsed: ['Advertising_Data', 'Internal_Sales', 'Marketplace_Data'],
  metricsUsed: [
    'Blended Ad Spend',
    'Return on Ad Spend (ROAS)',
    'Advertising Cost of Sales (ACoS %)',
    'Total Advertising Cost of Sales (TACoS %)',
    'Paid vs Organic Revenue Contribution %',
    'Cost Per Click (CPC)',
    'Ad Conversion Rate (CVR %)',
  ],
  deterministicFormulas: [
    {
      name: 'Return on Ad Spend (ROAS)',
      code: 'ROAS',
      formula: 'ROAS = Attributed Ad Revenue / Total Ad Spend',
      description: 'Measures direct revenue generated for every Rupee invested in advertising campaigns.',
      mathExpression: 'ROAS = \\frac{R_{ad}}{Spend_{ad}}',
      unit: 'x (Multiplier)',
      exampleCalculation: '₹3,00,000 attributed revenue / ₹75,000 ad spend = 4.00x',
    },
    {
      name: 'Advertising Cost of Sales (ACoS %)',
      code: 'ACOS',
      formula: 'ACoS % = (Total Ad Spend / Attributed Ad Revenue) * 100',
      description: 'The direct advertising cost percentage required to generate ad-attributed sales.',
      mathExpression: 'ACoS = \\left(\\frac{Spend_{ad}}{R_{ad}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹75,000 / ₹3,00,000) * 100 = 25.0%',
    },
    {
      name: 'Total Advertising Cost of Sales (TACoS %)',
      code: 'TACOS',
      formula: 'TACoS % = (Total Ad Spend / Consolidated Net Realized Revenue) * 100',
      description: 'Measures total advertising burden against the entire brand revenue (both paid and organic).',
      mathExpression: 'TACoS = \\left(\\frac{Spend_{ad}}{R_{total}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹75,000 / ₹6,00,000) * 100 = 12.5%',
    },
    {
      name: 'Cost Per Click (CPC)',
      code: 'CPC',
      formula: 'CPC = Total Ad Spend / Total Ad Clicks',
      description: 'The average amount paid per shopper click on sponsored listings or ads.',
      mathExpression: 'CPC = \\frac{Spend_{ad}}{Clicks_{ad}}',
      unit: '₹ / click',
      exampleCalculation: '₹50,000 / 3,500 clicks = ₹14.28 / click',
    },
  ],
  thresholds: [
    {
      metric: 'Blended ROAS',
      healthyRange: '≥ 3.50x',
      warningThreshold: '< 3.00x',
      criticalThreshold: '< 2.20x',
      operator: '<',
      severity: 'critical',
      triggerCondition: 'ROAS falls below 2.20x on any major channel or overall brand portfolio.',
      actionRequired: 'Pause bleeding broad-match keywords, decrease top-of-search bid multipliers, and add negative keywords.',
    },
    {
      metric: 'ACoS %',
      healthyRange: '≤ 28%',
      warningThreshold: '> 35%',
      criticalThreshold: '> 45%',
      operator: '>',
      severity: 'high',
      triggerCondition: 'Campaign ACoS exceeds 45%, eroding SKU gross margin.',
      actionRequired: 'Recalibrate automated bid caps and shift budget to exact-match high-converting queries.',
    },
    {
      metric: 'TACoS %',
      healthyRange: '≤ 12%',
      warningThreshold: '> 15%',
      criticalThreshold: '> 20%',
      operator: '>',
      severity: 'high',
      triggerCondition: 'Brand TACoS exceeds 20% of net revenue, indicating over-reliance on paid traffic.',
      actionRequired: 'Optimize organic listing SEO, title keyword density, and review conversion funnels.',
    },
  ],
  executionFlow: [
    {
      step: 1,
      name: 'Aggregate Advertising Spend & Attributed Revenue',
      type: 'deterministic_calc',
      description: 'Filters Advertising_Data by reporting date and sums spend, clicks, impressions, and attributed sales.',
      input: 'Advertising_Data for selectedDate',
      output: 'Platform-level ad spend, clicks, and revenue ledger',
    },
    {
      step: 2,
      name: 'Compute ROAS, ACoS, TACoS & Paid vs Organic Mix',
      type: 'deterministic_calc',
      description: 'Reconciles ad revenue against total sales to determine ROAS, ACoS, TACoS, and paid contribution %.',
      input: 'Ad ledger + Internal_Sales net revenue',
      output: 'Efficiency metric matrix and campaign ranking',
    },
    {
      step: 3,
      name: 'Evaluate Campaign Inefficiencies',
      type: 'rule_evaluation',
      description: 'Identifies campaigns or channels breaching ACoS or TACoS threshold limits.',
      input: 'Computed ad metrics vs thresholds',
      output: 'List of ad inefficiency alerts with severity ratings',
    },
    {
      step: 4,
      name: 'Generate Performance Marketing Directives',
      type: 'llm_interpretation',
      description: 'Produces structured recommendations for bid adjustments, negative keyword additions, and budget reallocation.',
      input: 'Evaluated ad metrics and anomaly triggers',
      output: 'AgentStructuredFinding[] array',
    },
  ],
  systemPrompt: advertisingAgentSystemMessage.content as string,
  targetRoleStakeholders: ['Admin', 'Executive', 'Advertising Manager'],
};

// ----------------------------------------------------------------------
// 4. Deterministic Calculation Engine
// ----------------------------------------------------------------------
export function calculateAdvertisingMetrics(
  data: SleepsiaWorkbookData,
  selectedDate: string,
  kpis: CalculatedKPIs
) {
  const currentAds = data.advertising.filter((a) => a.date === selectedDate);
  const currentSales = data.sales.filter((s) => s.date === selectedDate);
  const totalNetRev = currentSales.reduce((acc, s) => acc + s.netRealizedRevenue, 0) || 1;

  const totalSpend = currentAds.reduce((acc, a) => acc + a.spend, 0);
  const totalAttrRev = currentAds.reduce((acc, a) => acc + a.attributedRevenue, 0);
  const totalClicks = currentAds.reduce((acc, a) => acc + a.clicks, 0);
  const totalImpressions = currentAds.reduce((acc, a) => acc + a.impressions, 0);
  const totalConversions = currentAds.reduce((acc, a) => acc + a.orders, 0);

  const blendedRoas = totalSpend > 0 ? Number((totalAttrRev / totalSpend).toFixed(2)) : 0;
  const blendedAcos = totalAttrRev > 0 ? Number(((totalSpend / totalAttrRev) * 100).toFixed(1)) : 0;
  const tacos = Number(((totalSpend / totalNetRev) * 100).toFixed(1));
  const avgCpc = totalClicks > 0 ? Number((totalSpend / totalClicks).toFixed(2)) : 0;
  const cvr = totalClicks > 0 ? Number(((totalConversions / totalClicks) * 100).toFixed(1)) : 0;

  const campaigns = currentAds.map((a) => ({
    name: a.campaignName,
    platform: a.platform,
    spend: a.spend,
    revenue: a.attributedRevenue,
    roas: a.spend > 0 ? Number((a.attributedRevenue / a.spend).toFixed(2)) : 0,
    acos: a.attributedRevenue > 0 ? Number(((a.spend / a.attributedRevenue) * 100).toFixed(1)) : 0,
    clicks: a.clicks,
    cpc: a.clicks > 0 ? Number((a.spend / a.clicks).toFixed(2)) : 0,
  }));

  const bestCampaign = [...campaigns].filter((c) => c.spend > 0).sort((a, b) => b.roas - a.roas)[0];
  const worstCampaign = [...campaigns].filter((c) => c.spend > 0).sort((a, b) => a.roas - b.roas)[0];

  return {
    selectedDate,
    totalSpend,
    totalAttrRev,
    blendedRoas,
    blendedAcos,
    tacos,
    avgCpc,
    cvr,
    totalClicks,
    totalImpressions,
    campaigns,
    bestCampaign,
    worstCampaign,
    organicSalesPercent: kpis.paidVsOrganic.organicContributionPercent,
  };
}

// ----------------------------------------------------------------------
// 5. Execution Pipeline
// ----------------------------------------------------------------------
export async function executeAdvertisingAgent(
  context: AgentExecutionContext
): Promise<AgentExecutionResult> {
  const startTime = Date.now();
  const { data, selectedDate, kpis } = context;
  const metrics = calculateAdvertisingMetrics(data, selectedDate, kpis);

  const findings: AgentStructuredFinding[] = [];

  // Finding 1: Blended ROAS & TACoS Efficiency
  const isRoasLow = metrics.blendedRoas < 3.0;
  const isTacosHigh = metrics.tacos > 15;

  findings.push({
    id: `ad-find-1-${selectedDate}`,
    metric: 'Blended ROAS & TACoS Efficiency',
    current_value: `${metrics.blendedRoas}x ROAS (TACoS: ${metrics.tacos}%)`,
    previous_value: '3.50x ROAS (TACoS: 12.0%) Target',
    change_percent: Number(((metrics.blendedRoas - 3.5) / 3.5 * 100).toFixed(1)),
    severity: metrics.blendedRoas < 2.2 ? 'critical' : isRoasLow || isTacosHigh ? 'high' : 'low',
    finding: `Sleepsia invested ${formatCurrency(metrics.totalSpend)} in paid advertising, delivering ${formatCurrency(metrics.totalAttrRev)} in attributed revenue at a blended ROAS of ${metrics.blendedRoas}x (TACoS: ${metrics.tacos}%, ACoS: ${metrics.blendedAcos}%). Organic sales account for ${metrics.organicSalesPercent}% of daily revenue.`,
    possible_causes: isRoasLow
      ? [
          'High keyword bid competition on generic category terms like "memory foam pillow"',
          'Bleeding auto/broad campaigns with low search term relevance',
          'Elevated CPCs in competitive marketplace auctions',
        ]
      : [
          'Strong conversion rate on brand defense and high-intent exact-match keywords',
          'Efficient retargeting audience pools driving repeat purchases',
        ],
    recommended_action: isRoasLow
      ? 'Add negative keywords to bleeding broad campaigns, reduce top-of-search bid modifiers by 15%, and reallocate budget to exact-match campaigns with ROAS > 4.0x.'
      : 'Maintain current bid structures and test incrementality scaling on top-converting SKU targets.',
    priority: metrics.blendedRoas < 2.2 ? 'P0 - Immediate' : isRoasLow ? 'P1 - Urgent' : 'P3 - Medium',
    area: 'Advertising',
    confidence: 0.96,
    expected_business_impact: isRoasLow
      ? `Saves estimated ${formatCurrency(metrics.totalSpend * 0.18)} in wasted ad spend while improving portfolio ROAS to 3.4x+`
      : 'Maintains optimal organic-to-paid flywheel and protects operating margin',
    source: ['Advertising_Data', 'Internal_Sales'],
    agent: 'Advertising',
  });

  // Finding 2: Bleeding Campaign Target
  if (metrics.worstCampaign && metrics.worstCampaign.roas < 2.5 && metrics.worstCampaign.spend > 0) {
    findings.push({
      id: `ad-find-2-${selectedDate}`,
      metric: `Bleeding Campaign: ${metrics.worstCampaign.name}`,
      current_value: `${metrics.worstCampaign.roas}x ROAS (ACoS: ${metrics.worstCampaign.acos}%)`,
      previous_value: '3.00x Target Minimum',
      change_percent: Number(((metrics.worstCampaign.roas - 3.0) / 3.0 * 100).toFixed(1)),
      severity: metrics.worstCampaign.roas < 1.8 ? 'critical' : 'high',
      finding: `Campaign "${metrics.worstCampaign.name}" on ${metrics.worstCampaign.platform} spent ${formatCurrency(metrics.worstCampaign.spend)} but returned only ${formatCurrency(metrics.worstCampaign.revenue)} (${metrics.worstCampaign.roas}x ROAS, ACoS ${metrics.worstCampaign.acos}%).`,
      possible_causes: [
        'Unconstrained broad keyword match types attracting irrelevant shopper queries',
        'Outdated landing page or uncompetitive pricing relative to adjacent sponsored rivals',
      ],
      recommended_action: `Pause underperforming ad groups in "${metrics.worstCampaign.name}", lower keyword bids by 25%, and add search terms with >₹500 spend and 0 orders to the negative exact list.`,
      priority: 'P1 - Urgent',
      area: 'Advertising',
      confidence: 0.94,
      expected_business_impact: `Recovers ${formatCurrency(metrics.worstCampaign.spend * 0.35)} in wasted daily budget`,
      source: ['Advertising_Data'],
      agent: 'Advertising',
    });
  }

  const duration = Date.now() - startTime;

  return {
    agentId: 'advertising-intelligence',
    agentName: advertisingAgentSpec.name,
    status: 'completed',
    executionDurationMs: duration,
    findings,
    computedMetrics: metrics,
    reasoningSummary: `Audited ${metrics.campaigns.length} campaigns across platforms for ${selectedDate}. Total ad spend: ${formatCurrency(metrics.totalSpend)}, Attributed revenue: ${formatCurrency(metrics.totalAttrRev)}. Blended ROAS: ${metrics.blendedRoas}x, TACoS: ${metrics.tacos}%. Best: ${metrics.bestCampaign?.name || 'N/A'} (${metrics.bestCampaign?.roas || 0}x).`,
    keyMetricObserved: `${metrics.blendedRoas}x Blended ROAS (${formatCurrency(metrics.totalSpend)} Spend, TACoS: ${metrics.tacos}%)`,
    topFinding: findings[0]?.finding,
    topRecommendation: findings[0]?.recommended_action,
  };
}
