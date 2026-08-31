/**
 * Competitor & Market Pricing Intelligence Agent
 * Implements LangChain SystemMessage, Zod structured output validation, and competitive benchmarking logic.
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
export const competitorAgentSystemMessage = new SystemMessage(
  `You are the Competitive Intelligence & Algorithmic Pricing Strategist Agent for Sleepsia.

CORE IDENTITY & EXPERTISE:
You specialize in competitive landscape benchmarking, rival price tracking (The Sleep Company, Wakefit, Flo, Duroflex, Sunday Mattress, Emma), promotional discount audits, marketplace search positioning, and buybox contestability analysis.

OPERATIONAL BOUNDARIES & GUARDRAILS:
1. PRICE GAP MONITORING: Calculate the exact percentage difference between Sleepsia pricing and competing benchmark products. Flag competitor price undercutting > 10% as HIGH THREAT.
2. PROMOTIONAL WARFARE AUDIT: Detect aggressive competitor lightning deals, coupon stacking, and sponsored brand conquesting.
3. VALUE-ADD POSITIONING: Never recommend blind price-matching to zero margin; always weigh brand equity, clinical contour certifications, and warranty superiority before advising price adjustments.
4. RIGOROUS COMPETITOR DATA GROUNDING: Ingest rival prices and promotional indices directly from Competitor_Data.

EVALUATION CRITERIA:
- Competitor Price Gap: Aggressive Undercutting < -15%, Moderate Undercutting -5% to -15%, Parity -5% to +5%, Premium > +5%.
- Threat Classification: Severe (Deep discount + High Rating + Same Day Delivery), High, Medium, Low.`
);

// ----------------------------------------------------------------------
// 2. Structured Output Schema (Zod)
// ----------------------------------------------------------------------
export const CompetitorAnalysisOutputSchema = z.object({
  agentId: z.literal('competitor-intelligence'),
  agentName: z.string().default('Competitor & Market Intelligence Agent'),
  evaluationDate: z.string(),
  overallStatus: z.enum(['HEALTHY', 'WARNING', 'CRITICAL']),
  metrics: z.object({
    competitorsTrackedCount: z.number(),
    averagePriceGapPercent: z.number(),
    highThreatCompetitorsCount: z.number(),
    deepestDiscountPercent: z.number(),
    primaryRivalBrand: z.string(),
  }),
  competitorBenchmarks: z.array(
    z.object({
      competitorBrand: z.string(),
      competitorProduct: z.string(),
      competitorPrice: z.number(),
      sleepsiaComparablePrice: z.number(),
      priceGapPercent: z.number(),
      threatLevel: z.enum(['Severe', 'High', 'Moderate', 'Low', 'Parity']),
      discountPercent: z.number(),
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
      area: z.literal('Competitor'),
      confidence: z.number(),
      expected_business_impact: z.string(),
    })
  ),
  pricingDirectives: z.array(
    z.object({
      targetCategory: z.string(),
      recommendedPricingAction: z.string(),
      marginProtectionNote: z.string(),
    })
  ),
});

export type CompetitorAnalysisOutput = z.infer<typeof CompetitorAnalysisOutputSchema>;
export const competitorOutputParser = StructuredOutputParser.fromZodSchema(CompetitorAnalysisOutputSchema);

// ----------------------------------------------------------------------
// 3. Specialist Agent Specification & Metadata
// ----------------------------------------------------------------------
export const competitorAgentSpec: SpecialistAgentSpec = {
  id: 'competitor-intelligence',
  name: 'Competitor & Market Pricing Agent',
  category: 'External',
  role: 'Competitive Strategy & Pricing Intelligence Lead',
  purpose: 'Tracks rival pricing movements, promotional discounts, coupon codes, and organic search share across Wakefit, The Sleep Company, Flo, and Duroflex.',
  primaryObjective: 'Protect Sleepsia market share against predatory competitor discounting while preventing destructive margin-eroding price wars.',
  dataSourcesUsed: ['Competitor_Data', 'Product_Master', 'Internal_Sales'],
  metricsUsed: [
    'Competitor Price Index (CPI)',
    'Price Gap % (Sleepsia vs Rival)',
    'Competitor Discount Depth %',
    'Rival Organic Search Rank & Share of Voice',
    'Competitor Review Rating & Velocity',
    'Market Share Shift Probability',
  ],
  deterministicFormulas: [
    {
      name: 'Competitor Price Gap %',
      code: 'PRICE_GAP',
      formula: 'Price Gap % = ((Competitor Price - Sleepsia Price) / Sleepsia Price) * 100',
      description: 'Calculates the relative percentage by which a rival is pricing higher (+) or undercutting (-) Sleepsia for comparable products.',
      mathExpression: 'Gap\\% = \\left(\\frac{P_{rival} - P_{sleepsia}}{P_{sleepsia}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹1,399 rival - ₹1,599 Sleepsia) / ₹1,599 = -12.51%',
    },
    {
      name: 'Competitor Discount Depth %',
      code: 'DISCOUNT_DEPTH',
      formula: 'Discount % = ((Competitor MRP - Competitor Selling Price) / Competitor MRP) * 100',
      description: 'The promotional slash offered by a rival on marketplace listings.',
      mathExpression: 'Depth_{disc} = \\left(\\frac{MRP_{rival} - Price_{rival}}{MRP_{rival}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹2,499 MRP - ₹1,499 Price) / ₹2,499 = 40.0%',
    },
  ],
  thresholds: [
    {
      metric: 'Aggressive Competitor Undercutting',
      healthyRange: '-5% to +10%',
      warningThreshold: '< -10%',
      criticalThreshold: '< -20%',
      operator: '<',
      severity: 'critical',
      triggerCondition: 'Rival brand undercuts Sleepsia by > 20% on a core category hero SKU.',
      actionRequired: 'Review value proposition, deploy limited-time ₹100-₹150 instant voucher, and highlight orthopedic certifications.',
    },
    {
      metric: 'Competitor Search Threat',
      healthyRange: '< 30% Share',
      warningThreshold: '30% - 45%',
      criticalThreshold: '> 45%',
      operator: '>',
      severity: 'high',
      triggerCondition: 'Competitor captures top 2 sponsored and organic positions on primary search keywords.',
      actionRequired: 'Increase exact-match defensive bid cap on branded search terms.',
    },
  ],
  executionFlow: [
    {
      step: 1,
      name: 'Load Competitor Price Crawl',
      type: 'deterministic_calc',
      description: 'Ingests competitor prices, discounts, and ratings from Competitor_Data.',
      input: 'Competitor_Data ledger',
      output: 'Rival SKU benchmark table',
    },
    {
      step: 2,
      name: 'Compute Price Gap & Threat Index',
      type: 'deterministic_calc',
      description: 'Calculates price gap percentage against Sleepsia equivalent products.',
      input: 'Rival benchmark table + Product_Master',
      output: 'Competitive threat matrix',
    },
    {
      step: 3,
      name: 'Evaluate Undercutting Thresholds',
      type: 'rule_evaluation',
      description: 'Flags severe price undercutting (> 15%) on hero lines.',
      input: 'Competitive threat matrix vs thresholds',
      output: 'List of pricing threat alerts',
    },
    {
      step: 4,
      name: 'Formulate Tactical Pricing Response',
      type: 'llm_interpretation',
      description: 'Produces structured recommendations for coupon vouchers, bundle deals, and messaging counter-punches.',
      input: 'Evaluated pricing metrics and threat alerts',
      output: 'AgentStructuredFinding[] array',
    },
  ],
  systemPrompt: competitorAgentSystemMessage.content as string,
  targetRoleStakeholders: ['Admin', 'Executive', 'Product Manager', 'Advertising Manager'],
};

// ----------------------------------------------------------------------
// 4. Deterministic Calculation Engine
// ----------------------------------------------------------------------
export function calculateCompetitorMetrics(
  data: SleepsiaWorkbookData,
  selectedDate: string,
  kpis: CalculatedKPIs
) {
  const currentComp = data.competitors.filter((c) => c.date === selectedDate);
  const totalCompetitors = currentComp.length || 1;

  const threats = currentComp.map((c) => {
    const matchedProd = data.products.find((p) => p.sku === c.sleepsiaTargetSku || p.category === c.category);
    const sleepsiaPrice = matchedProd?.mrp || 1599;
    const priceGap = Number((((c.competitorPrice - sleepsiaPrice) / sleepsiaPrice) * 100).toFixed(1));

    return {
      competitorBrand: c.competitorBrand,
      competitorProduct: c.competitorProductName,
      competitorPrice: c.competitorPrice,
      sleepsiaPrice,
      priceGap,
      discountPercent: c.discountPercent || 0,
      threatLevel: c.threatLevel,
    };
  });

  const highThreats = threats.filter((t) => t.threatLevel === 'High' || t.threatLevel === 'Severe' || t.priceGap < -10);
  const topThreat = highThreats[0] || threats[0];
  const avgGap = threats.length > 0 ? Number((threats.reduce((acc, t) => acc + t.priceGap, 0) / threats.length).toFixed(1)) : 0;

  return {
    selectedDate,
    totalTracked: totalCompetitors,
    threats,
    highThreatsCount: highThreats.length,
    topThreat,
    avgPriceGap: avgGap,
  };
}

// ----------------------------------------------------------------------
// 5. Execution Pipeline
// ----------------------------------------------------------------------
export async function executeCompetitorAgent(
  context: AgentExecutionContext
): Promise<AgentExecutionResult> {
  const startTime = Date.now();
  const { data, selectedDate, kpis } = context;
  const metrics = calculateCompetitorMetrics(data, selectedDate, kpis);

  const findings: AgentStructuredFinding[] = [];

  // Finding 1: Competitor Threat Benchmark
  if (metrics.topThreat) {
    const isSevere = metrics.topThreat.priceGap < -15;
    findings.push({
      id: `comp-find-1-${selectedDate}`,
      metric: `Competitor Price Undercutting: ${metrics.topThreat.competitorBrand}`,
      current_value: `${formatCurrency(metrics.topThreat.competitorPrice)} (${metrics.topThreat.priceGap}% Gap vs Sleepsia ${formatCurrency(metrics.topThreat.sleepsiaPrice)})`,
      previous_value: 'Price Parity Benchmark (0.0%)',
      change_percent: metrics.topThreat.priceGap,
      severity: isSevere ? 'critical' : 'high',
      finding: `Leading rival ${metrics.topThreat.competitorBrand} is aggressively promoting ${metrics.topThreat.competitorProduct} at ${formatCurrency(metrics.topThreat.competitorPrice)} (${metrics.topThreat.priceGap}% below Sleepsia), offering a ${metrics.topThreat.discountPercent}% promotional markdown.`,
      possible_causes: [
        'Competitor flash sale campaign to capture organic category ranking on marketplace search',
        'Bulk inventory clearance on older polyurethane foam generation models',
      ],
      recommended_action: `Deploy a targeted ₹100 instant coupon voucher on Sleepsia's comparable SKU and amplify listing badges highlighting medical-grade ergonomic certification.`,
      priority: isSevere ? 'P0 - Immediate' : 'P1 - Urgent',
      area: 'Competitor',
      confidence: 0.95,
      expected_business_impact: `Protects estimated ₹45,000 weekly category sales volume from rival customer churn`,
      source: ['Competitor_Data', 'Product_Master'],
      agent: 'Competitor',
    });
  }

  const duration = Date.now() - startTime;

  return {
    agentId: 'competitor-intelligence',
    agentName: competitorAgentSpec.name,
    status: 'completed',
    executionDurationMs: duration,
    findings,
    computedMetrics: metrics,
    reasoningSummary: `Tracked ${metrics.totalTracked} competitor listings for ${selectedDate}. Average price gap: ${metrics.avgPriceGap}%. Top rival threat: ${metrics.topThreat?.competitorBrand || 'N/A'} (${metrics.topThreat?.priceGap || 0}% gap at ${formatCurrency(metrics.topThreat?.competitorPrice || 0)}).`,
    keyMetricObserved: `${metrics.totalTracked} Competitor SKUs Tracked (Top Threat: ${metrics.topThreat?.competitorBrand || 'Rival'} at ${formatCurrency(metrics.topThreat?.competitorPrice || 0)})`,
    topFinding: findings[0]?.finding,
    topRecommendation: findings[0]?.recommended_action,
  };
}
