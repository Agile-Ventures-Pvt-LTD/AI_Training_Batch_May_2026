/**
 * Product & Merchandising Intelligence Agent
 * Implements LangChain SystemMessage, Zod structured output validation, and SKU catalog analytics.
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
export const productAgentSystemMessage = new SystemMessage(
  `You are the Chief Product & Merchandising Intelligence Officer Agent for Sleepsia.

CORE IDENTITY & EXPERTISE:
You are an authority on sleep ergonomics, cervical orthopedic catalog curation, memory foam density, and unit contribution economics. You audit SKU-level sales velocity, category revenue concentration, return rates by model, review ratings, and price band elasticity.

OPERATIONAL BOUNDARIES & GUARDRAILS:
1. SKU INTEGRITY: Every product SKU (e.g. SLP-CERV-01, SLP-MEM-02) must be reconciled with its exact Product Master specs (MRP, COGS, Category, Margin Target).
2. RETURN ANOMALY DETECTION: Flag any SKU with a return rate exceeding 10% for immediate quality control, sizing clarity, or packaging audit.
3. HERO SKU PROTECTION: Safeguard core revenue drivers from inventory starvation or margin erosion.
4. GROUNDED EVIDENCE: Base all product volume, revenue, and return figures on the active day's internal sales transactions.

EVALUATION CRITERIA:
- SKU Return Rate: Healthy ≤ 5%, Warning 6%-10%, Critical > 10%.
- Hero SKU Concentration: Healthy 25%-40%, Warning > 55% (vulnerability to single SKU shock).
- Unit Gross Contribution Margin: Healthy ≥ 55%, Critical < 40%.`
);

// ----------------------------------------------------------------------
// 2. Structured Output Schema (Zod)
// ----------------------------------------------------------------------
export const ProductAnalysisOutputSchema = z.object({
  agentId: z.literal('product-intelligence'),
  agentName: z.string().default('Product & Merchandising Intelligence Agent'),
  evaluationDate: z.string(),
  overallStatus: z.enum(['HEALTHY', 'WARNING', 'CRITICAL']),
  metrics: z.object({
    totalActiveSkus: z.number(),
    topSellingSku: z.string(),
    topSellingSkuRevenue: z.number(),
    topSellingSkuUnits: z.number(),
    topCategory: z.string(),
    topCategorySharePercent: z.number(),
    averageProductRating: z.number(),
    highReturnSkuCount: z.number(),
  }),
  skuPerformance: z.array(
    z.object({
      sku: z.string(),
      productName: z.string(),
      category: z.string(),
      revenue: z.number(),
      unitsSold: z.number(),
      returnRatePercent: z.number(),
      status: z.enum(['HERO_DRIVER', 'STEADY_PERFORMER', 'LOW_VELOCITY', 'RETURN_RISK']),
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
      area: z.literal('Inventory'),
      confidence: z.number(),
      expected_business_impact: z.string(),
    })
  ),
  merchandisingDirectives: z.array(z.string()),
});

export type ProductAnalysisOutput = z.infer<typeof ProductAnalysisOutputSchema>;
export const productOutputParser = StructuredOutputParser.fromZodSchema(ProductAnalysisOutputSchema);

// ----------------------------------------------------------------------
// 3. Specialist Agent Specification & Metadata
// ----------------------------------------------------------------------
export const productAgentSpec: SpecialistAgentSpec = {
  id: 'product-intelligence',
  name: 'Product & Merchandising Intelligence Agent',
  category: 'Domain Intelligence',
  role: 'Chief Product & Merchandising Officer',
  purpose: 'Analyzes SKU sales velocity, category revenue contribution, product return rates, review sentiment, and product catalog expansion opportunities.',
  primaryObjective: 'Identify hero products, eliminate high-return defective batches, and optimize product mix for maximum gross contribution margin.',
  dataSourcesUsed: ['Product_Master', 'Internal_Sales', 'Inventory_Data'],
  metricsUsed: [
    'SKU Sales Velocity (Units / Day)',
    'SKU Revenue Contribution (₹)',
    'Category Revenue Share %',
    'Product Return & Defect Rate %',
    'Product Rating & Review Count',
    'Gross Margin Contribution % per SKU',
  ],
  deterministicFormulas: [
    {
      name: 'SKU Sales Velocity',
      code: 'SKU_VELOCITY',
      formula: 'Velocity = Total Units Sold for SKU on Date',
      description: 'Calculates the daily order rate and unit consumption speed for a specific product.',
      mathExpression: 'V_{sku} = \\sum Units_{sku, date}',
      unit: 'units / day',
      exampleCalculation: '120 units sold on 2026-08-24',
    },
    {
      name: 'Product Return Rate %',
      code: 'PROD_RETURN_RATE',
      formula: 'Return % = (Returned Units for SKU / Total Units Sold for SKU) * 100',
      description: 'The percentage of customers returning or rejecting a specific product model.',
      mathExpression: 'Return\\% = \\left(\\frac{Units_{returned}}{Units_{sold}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(12 returned / 150 sold) * 100 = 8.0%',
    },
    {
      name: 'Category Revenue Contribution Share %',
      code: 'CAT_SHARE',
      formula: 'Category Share % = (Category Net Revenue / Total Net Revenue) * 100',
      description: 'The proportion of total brand sales driven by a specific product category.',
      mathExpression: 'Share_{cat} = \\left(\\frac{Rev_{cat}}{Rev_{total}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(₹3,20,000 / ₹5,50,000) * 100 = 58.18%',
    },
  ],
  thresholds: [
    {
      metric: 'Product Return Rate %',
      healthyRange: '< 6%',
      warningThreshold: '6% - 10%',
      criticalThreshold: '> 10%',
      operator: '>',
      severity: 'critical',
      triggerCondition: 'Any SKU exhibits a return rate > 10% with > 20 units sold.',
      actionRequired: 'Initiate warehouse quality batch inspection and update listing dimensions/firmness descriptions.',
    },
    {
      metric: 'Category Concentration %',
      healthyRange: '< 60%',
      warningThreshold: '60% - 75%',
      criticalThreshold: '> 75%',
      operator: '>',
      severity: 'high',
      triggerCondition: 'Single category represents > 75% of sales, creating single-market vulnerability.',
      actionRequired: 'Accelerate cross-merchandising in adjacent accessories and mattress protectors.',
    },
  ],
  executionFlow: [
    {
      step: 1,
      name: 'Reconcile SKU Ledger',
      type: 'deterministic_calc',
      description: 'Aggregates sales volume, revenue, and returns for each SKU on the reporting date.',
      input: 'Internal_Sales and Product_Master',
      output: 'SKU performance matrix',
    },
    {
      step: 2,
      name: 'Compute Category Mix & Return Rates',
      type: 'deterministic_calc',
      description: 'Calculates category revenue share % and returns percentage per SKU.',
      input: 'SKU performance matrix',
      output: 'Category breakdown and defect risk table',
    },
    {
      step: 3,
      name: 'Evaluate Product Quality & Concentration Thresholds',
      type: 'rule_evaluation',
      description: 'Flags SKUs exceeding 10% return rate or categories with dangerous concentration.',
      input: 'Computed metrics vs thresholds',
      output: 'List of product quality and merchandising alerts',
    },
    {
      step: 4,
      name: 'Generate Merchandising Recommendations',
      type: 'llm_interpretation',
      description: 'Produces structured findings for listing improvements, packaging updates, and catalog expansion.',
      input: 'Evaluated product metrics and anomaly triggers',
      output: 'AgentStructuredFinding[] array',
    },
  ],
  systemPrompt: productAgentSystemMessage.content as string,
  targetRoleStakeholders: ['Admin', 'Executive', 'Product Manager'],
};

// ----------------------------------------------------------------------
// 4. Deterministic Calculation Engine
// ----------------------------------------------------------------------
export function calculateProductMetrics(
  data: SleepsiaWorkbookData,
  selectedDate: string,
  kpis: CalculatedKPIs
) {
  const currentSales = data.sales.filter((s) => s.date === selectedDate);
  const totalNetRev = currentSales.reduce((acc, s) => acc + s.netRealizedRevenue, 0) || 1;

  // SKU Map
  const skuMap: Record<string, { sku: string; name: string; category: string; units: number; revenue: number; returns: number }> = {};
  currentSales.forEach((s) => {
    if (!skuMap[s.sku]) {
      const prod = data.products.find((p) => p.sku === s.sku);
      skuMap[s.sku] = {
        sku: s.sku,
        name: s.productName || prod?.productName || s.sku,
        category: prod?.category || 'Cervical Care',
        units: 0,
        revenue: 0,
        returns: 0,
      };
    }
    skuMap[s.sku].units += s.units;
    skuMap[s.sku].revenue += s.netRealizedRevenue;
    skuMap[s.sku].returns += s.returns;
  });

  const skuList = Object.values(skuMap).map((s) => {
    const returnRate = s.units > 0 ? Number(((s.returns / s.units) * 100).toFixed(1)) : 0;
    const share = Number(((s.revenue / totalNetRev) * 100).toFixed(1));
    return {
      ...s,
      returnRate,
      share,
    };
  }).sort((a, b) => b.revenue - a.revenue);

  // Category Map
  const catMap: Record<string, { revenue: number; units: number }> = {};
  skuList.forEach((s) => {
    if (!catMap[s.category]) {
      catMap[s.category] = { revenue: 0, units: 0 };
    }
    catMap[s.category].revenue += s.revenue;
    catMap[s.category].units += s.units;
  });

  const categoryBreakdown = Object.entries(catMap).map(([cat, m]) => ({
    category: cat,
    revenue: m.revenue,
    units: m.units,
    sharePercent: Number(((m.revenue / totalNetRev) * 100).toFixed(1)),
  })).sort((a, b) => b.revenue - a.revenue);

  const topSku = skuList[0];
  const topCategory = categoryBreakdown[0];
  const highReturnSkus = skuList.filter((s) => s.returnRate > 8 && s.units >= 10);

  return {
    selectedDate,
    totalSkusSold: skuList.length,
    skuList,
    topSku,
    categoryBreakdown,
    topCategory,
    highReturnSkus,
  };
}

// ----------------------------------------------------------------------
// 5. Execution Pipeline
// ----------------------------------------------------------------------
export async function executeProductAgent(
  context: AgentExecutionContext
): Promise<AgentExecutionResult> {
  const startTime = Date.now();
  const { data, selectedDate, kpis } = context;
  const metrics = calculateProductMetrics(data, selectedDate, kpis);

  const findings: AgentStructuredFinding[] = [];

  // Finding 1: Top Hero SKU Performance
  if (metrics.topSku) {
    findings.push({
      id: `prod-find-1-${selectedDate}`,
      metric: `Hero SKU: ${metrics.topSku.name}`,
      current_value: `${formatCurrency(metrics.topSku.revenue)} (${metrics.topSku.units} units, ${metrics.topSku.share}% share)`,
      previous_value: 'Hero SKU Baseline Tracked',
      change_percent: metrics.topSku.share,
      severity: 'low',
      finding: `Top revenue contributor is ${metrics.topSku.name} (${metrics.topSku.sku}), generating ${formatCurrency(metrics.topSku.revenue)} across ${metrics.topSku.units} units with a healthy return rate of ${metrics.topSku.returnRate}%.`,
      possible_causes: [
        'Consistently high organic search rank and positive verified reviews',
        'Strong clinical positioning for cervical neck and contour support',
      ],
      recommended_action: `Ensure continuous production batches and prevent warehouse stockouts at high-throughput fulfillment centers.`,
      priority: 'P3 - Medium',
      area: 'Inventory',
      confidence: 0.96,
      expected_business_impact: `Protects core ${metrics.topSku.share}% brand revenue engine`,
      source: ['Product_Master', 'Internal_Sales'],
      agent: 'Inventory & Shipping',
    });
  }

  // Finding 2: Return Rate Check
  if (metrics.highReturnSkus.length > 0) {
    const rSku = metrics.highReturnSkus[0];
    findings.push({
      id: `prod-find-2-${selectedDate}`,
      metric: `High Return Rate: ${rSku.name}`,
      current_value: `${rSku.returnRate}% Return Rate (${rSku.returns} units)`,
      previous_value: '5.0% Quality Standard',
      change_percent: Number((rSku.returnRate - 5.0).toFixed(1)),
      severity: rSku.returnRate > 12 ? 'critical' : 'high',
      finding: `SKU ${rSku.name} (${rSku.sku}) recorded an elevated return rate of ${rSku.returnRate}% (${rSku.returns} returns out of ${rSku.units} units sold).`,
      possible_causes: [
        'Potential customer expectation mismatch regarding pillow firmness or height',
        'Batch-specific foam density variation or packaging compression issues',
      ],
      recommended_action: `Conduct a quality audit on the active manufacturing lot, add an explicit height/firmness guide image to product listings, and inspect return reason codes.`,
      priority: 'P1 - Urgent',
      area: 'Inventory',
      confidence: 0.94,
      expected_business_impact: `Reduces return processing costs and protects customer ratings`,
      source: ['Internal_Sales', 'Product_Master'],
      agent: 'Inventory & Shipping',
    });
  }

  const duration = Date.now() - startTime;

  return {
    agentId: 'product-intelligence',
    agentName: productAgentSpec.name,
    status: 'completed',
    executionDurationMs: duration,
    findings,
    computedMetrics: metrics,
    reasoningSummary: `Evaluated ${metrics.totalSkusSold} active SKUs across ${metrics.categoryBreakdown.length} categories for ${selectedDate}. Hero product: ${metrics.topSku?.name || 'N/A'} (${metrics.topSku?.share || 0}% share). High return SKUs flagged: ${metrics.highReturnSkus.length}.`,
    keyMetricObserved: `${metrics.topSku?.name || 'Top SKU'}: ${formatCurrency(metrics.topSku?.revenue || 0)} (${metrics.topSku?.units || 0} Units, ${metrics.topSku?.share || 0}% Share)`,
    topFinding: findings[0]?.finding,
    topRecommendation: findings[0]?.recommended_action,
  };
}
