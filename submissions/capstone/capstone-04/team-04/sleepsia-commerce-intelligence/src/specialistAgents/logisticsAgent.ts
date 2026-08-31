/**
 * Logistics & Fulfillment SLA Agent
 * Implements LangChain SystemMessage, Zod structured output validation, and 3PL delivery performance auditing.
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
export const logisticsAgentSystemMessage = new SystemMessage(
  `You are the Fleet Operations & Fulfillment SLA Auditor Agent for Sleepsia.

CORE IDENTITY & EXPERTISE:
You are an expert in middle-mile and last-mile logistics, 3PL carrier benchmarking (Delhivery, BlueDart, Bluedart Surface, Xpressbees, Shadowfax, Amazon ATS), warehouse dispatch SLA, Return to Origin (RTO) non-delivery analysis, and transit zone latency.

OPERATIONAL BOUNDARIES & GUARDRAILS:
1. ON-TIME DELIVERY AUDIT: Scrutinize carrier on-time delivery rates against the 92% enterprise contractual SLA threshold.
2. DELAY ROOT-CAUSE: Differentiate between warehouse dispatch bottlenecks (pick & pack delays) and in-transit carrier exceptions (NDR / fake delivery attempts).
3. RTO NON-DELIVERY SUPPRESSION: Flag carriers with RTO rate > 8% for COD verification audits.
4. RIGOROUS CARRIER PERFORMANCE METRICS: Compute exact on-time rates, average delay days, and failed delivery counts strictly from Shipping_Data.

EVALUATION CRITERIA:
- Carrier On-Time Delivery Rate: Healthy ≥ 92%, Warning 85%-91%, Critical < 85%.
- Average Delivery Delay: Healthy ≤ 0.5 days, Warning 0.6-1.5 days, Critical > 1.5 days.
- RTO / NDR Rate: Healthy ≤ 5%, Warning 6%-9%, Critical > 9%.`
);

// ----------------------------------------------------------------------
// 2. Structured Output Schema (Zod)
// ----------------------------------------------------------------------
export const LogisticsAnalysisOutputSchema = z.object({
  agentId: z.literal('logistics-intelligence'),
  agentName: z.string().default('Logistics & Fulfillment Agent'),
  evaluationDate: z.string(),
  overallStatus: z.enum(['HEALTHY', 'WARNING', 'CRITICAL']),
  metrics: z.object({
    totalShipments: z.number(),
    onTimeDeliveryPercent: z.number(),
    averageDelayDays: z.number(),
    delayedOrdersCount: z.number(),
    failedShipmentsCount: z.number(),
    worstPerformingCarrier: z.string(),
    worstCarrierOnTimeRate: z.number(),
  }),
  carrierPerformance: z.array(
    z.object({
      carrier: z.string(),
      shipmentCount: z.number(),
      onTimeRatePercent: z.number(),
      averageDelayDays: z.number(),
      status: z.enum(['MEETS_SLA', 'AT_RISK', 'BREACHING_SLA']),
    })
  ),
  thresholdViolations: z.array(
    z.object({
      metric: z.string(),
      carrier: z.string(),
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
      area: z.literal('Shipping'),
      confidence: z.number(),
      expected_business_impact: z.string(),
    })
  ),
  carrierReallocationPlan: z.array(
    z.object({
      fromCarrier: z.string(),
      toCarrier: z.string(),
      volumePercentage: z.number(),
      reason: z.string(),
    })
  ),
});

export type LogisticsAnalysisOutput = z.infer<typeof LogisticsAnalysisOutputSchema>;
export const logisticsOutputParser = StructuredOutputParser.fromZodSchema(LogisticsAnalysisOutputSchema);

// ----------------------------------------------------------------------
// 3. Specialist Agent Specification & Metadata
// ----------------------------------------------------------------------
export const logisticsAgentSpec: SpecialistAgentSpec = {
  id: 'logistics-intelligence',
  name: 'Logistics & Fulfillment SLA Agent',
  category: 'Supply Chain',
  role: 'Logistics & Fleet Operations Auditor',
  purpose: 'Audits on-time delivery rates, courier partner SLA compliance, regional transit delays, and Return to Origin (RTO) non-delivery risks across Delhivery, BlueDart, Xpressbees, and Shadowfax.',
  primaryObjective: 'Ensure customer delivery promises are met (> 92% SLA), minimize transit damages, and dynamically reroute shipments away from lagging couriers.',
  dataSourcesUsed: ['Shipping_Data', 'Internal_Sales', 'Inventory_Data'],
  metricsUsed: [
    'On-Time Delivery Rate %',
    'Average Transit Time (Days)',
    'Delayed Orders & Breach Count',
    'Return to Origin (RTO) Non-Delivery %',
    'Courier SLA Breach Penalties (₹)',
    'Warehouse Dispatch Latency (Hours)',
  ],
  deterministicFormulas: [
    {
      name: 'On-Time Delivery Rate %',
      code: 'OTD_RATE',
      formula: 'OTD % = (Shipments Delivered On or Before Promised Date / Total Delivered Shipments) * 100',
      description: 'Calculates the proportion of shipments delivered within promised delivery windows.',
      mathExpression: 'OTD = \\left(\\frac{N_{ontime}}{N_{total}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(450 on-time / 500 total) * 100 = 90.0%',
    },
    {
      name: 'Average Delay in Days',
      code: 'AVG_DELAY',
      formula: 'Average Delay = Total Delay Days across Delayed Orders / Count of Delayed Orders',
      description: 'The average number of extra days taken beyond promised ETA for late shipments.',
      mathExpression: '\\bar{D}_{delay} = \\frac{\\sum D_{late}}{N_{delayed}}',
      unit: 'days',
      exampleCalculation: '75 total late days / 50 late orders = 1.50 days',
    },
    {
      name: 'Carrier Defect Rate %',
      code: 'CARRIER_DEFECT',
      formula: 'Defect % = ((Delayed Orders + Damaged Shipments + Lost Shipments) / Total Dispatches) * 100',
      description: 'Comprehensive failure metric for evaluation of 3PL logistics contract penalties.',
      mathExpression: 'Rate_{defect} = \\left(\\frac{Orders_{failed}}{Orders_{total}}\\right) \\times 100',
      unit: '%',
      exampleCalculation: '(35 defects / 500 dispatches) * 100 = 7.0%',
    },
  ],
  thresholds: [
    {
      metric: 'Carrier On-Time Delivery Rate',
      healthyRange: '≥ 92%',
      warningThreshold: '< 90%',
      criticalThreshold: '< 85%',
      operator: '<',
      severity: 'critical',
      triggerCondition: 'Any carrier drops below 85% on-time delivery on > 30 daily dispatches.',
      actionRequired: 'Cap carrier allocation cap by 50% and route traffic to secondary SLA-compliant partners.',
    },
    {
      metric: 'Return to Origin (RTO) Rate',
      healthyRange: '< 5%',
      warningThreshold: '5% - 8%',
      criticalThreshold: '> 8%',
      operator: '>',
      severity: 'high',
      triggerCondition: 'RTO rate exceeds 8% in any geographic delivery circle.',
      actionRequired: 'Enforce WhatsApp COD confirmation and OTP pre-dispatch verification.',
    },
  ],
  executionFlow: [
    {
      step: 1,
      name: 'Ingest Shipping & Tracking Logs',
      type: 'deterministic_calc',
      description: 'Filters Shipping_Data records for the reporting date and cross-references carrier names.',
      input: 'Shipping_Data ledger',
      output: 'Dispatched orders tracking matrix',
    },
    {
      step: 2,
      name: 'Compute Carrier SLA & Delay Metrics',
      type: 'deterministic_calc',
      description: 'Calculates on-time delivery rate %, average delay days, and RTO counts per carrier.',
      input: 'Dispatched tracking matrix',
      output: 'Carrier performance comparison table',
    },
    {
      step: 3,
      name: 'Evaluate SLA Threshold Violations',
      type: 'rule_evaluation',
      description: 'Flags courier partners violating the 92% on-time delivery threshold.',
      input: 'Carrier comparison table vs thresholds',
      output: 'List of courier SLA breach alerts',
    },
    {
      step: 4,
      name: 'Generate Logistics Routing Directives',
      type: 'llm_interpretation',
      description: 'Produces structured recommendations for carrier volume throttling and fulfillment re-routing.',
      input: 'Evaluated logistics metrics and breach alerts',
      output: 'AgentStructuredFinding[] array',
    },
  ],
  systemPrompt: logisticsAgentSystemMessage.content as string,
  targetRoleStakeholders: ['Admin', 'Executive', 'Logistics Manager'],
};

// ----------------------------------------------------------------------
// 4. Deterministic Calculation Engine
// ----------------------------------------------------------------------
export function calculateLogisticsMetrics(
  data: SleepsiaWorkbookData,
  selectedDate: string,
  kpis: CalculatedKPIs
) {
  const currentShipping = data.shipping.filter((s) => s.date === selectedDate);
  const totalShipments = currentShipping.length || 1;

  const onTimeCount = currentShipping.filter((s) => s.deliveryStatus === 'On-Time' || (s.delayDays || 0) <= 0).length;
  const delayedOrders = currentShipping.filter((s) => (s.delayDays || 0) > 0 || s.deliveryStatus === 'Delayed');
  const failedShipments = currentShipping.filter((s) => s.shipmentStatus === 'Lost' || s.deliveryStatus === 'Failed');

  const onTimeRate = Number(((onTimeCount / totalShipments) * 100).toFixed(1));
  const totalDelayDays = delayedOrders.reduce((acc, s) => acc + (s.delayDays || 0), 0);
  const avgDelay = delayedOrders.length > 0 ? Number((totalDelayDays / delayedOrders.length).toFixed(1)) : 0;

  // Carrier performance breakdown
  const carrierMap: Record<string, { total: number; onTime: number; delayed: number; totalDelay: number }> = {};
  currentShipping.forEach((s) => {
    if (!carrierMap[s.carrier]) {
      carrierMap[s.carrier] = { total: 0, onTime: 0, delayed: 0, totalDelay: 0 };
    }
    carrierMap[s.carrier].total += 1;
    if ((s.delayDays || 0) <= 0) {
      carrierMap[s.carrier].onTime += 1;
    } else {
      carrierMap[s.carrier].delayed += 1;
      carrierMap[s.carrier].totalDelay += (s.delayDays || 0);
    }
  });

  const carrierStats = Object.entries(carrierMap).map(([carrier, c]) => {
    const rate = c.total > 0 ? Number(((c.onTime / c.total) * 100).toFixed(1)) : 100;
    const delay = c.delayed > 0 ? Number((c.totalDelay / c.delayed).toFixed(1)) : 0;
    return {
      carrier,
      total: c.total,
      onTime: c.onTime,
      delayed: c.delayed,
      onTimeRate: rate,
      avgDelay: delay,
    };
  }).sort((a, b) => a.onTimeRate - b.onTimeRate);

  const worstCarrier = carrierStats[0];
  const bestCarrier = carrierStats[carrierStats.length - 1];

  return {
    selectedDate,
    totalShipments,
    onTimeRate: kpis.shipping.onTimeDeliveryRate || onTimeRate,
    avgDelay: kpis.shipping.averageDelayDays || avgDelay,
    delayedOrdersCount: delayedOrders.length,
    failedShipmentsCount: failedShipments.length,
    carrierStats,
    worstCarrier,
    bestCarrier,
  };
}

// ----------------------------------------------------------------------
// 5. Execution Pipeline
// ----------------------------------------------------------------------
export async function executeLogisticsAgent(
  context: AgentExecutionContext
): Promise<AgentExecutionResult> {
  const startTime = Date.now();
  const { data, selectedDate, kpis } = context;
  const metrics = calculateLogisticsMetrics(data, selectedDate, kpis);

  const findings: AgentStructuredFinding[] = [];

  // Finding 1: Fleet On-Time Delivery SLA
  const isSlaBreach = metrics.onTimeRate < 90;
  findings.push({
    id: `log-find-1-${selectedDate}`,
    metric: 'Fleet On-Time Delivery SLA',
    current_value: `${metrics.onTimeRate}% (${metrics.delayedOrdersCount} delayed orders)`,
    previous_value: '92.0% Contractual SLA Target',
    change_percent: Number((metrics.onTimeRate - 92.0).toFixed(1)),
    severity: metrics.onTimeRate < 85 ? 'critical' : isSlaBreach ? 'high' : 'low',
    finding: `Sleepsia fulfillment logistics achieved a ${metrics.onTimeRate}% on-time delivery rate across ${metrics.totalShipments} dispatches, with an average delay of ${metrics.avgDelay} days on delayed orders.`,
    possible_causes: isSlaBreach
      ? [
          `Carrier service level dips on regional routes handled by ${metrics.worstCarrier?.carrier || '3PL couriers'}`,
          'Heavy monsoon transit exceptions and localized hub backlogs',
          'Warehouse late pickup dispatch on peak volume slots',
        ]
      : [
          'High operational SLA compliance by premier air and surface carriers',
          'Efficient same-day dispatch from primary regional warehouses',
        ],
    recommended_action: isSlaBreach
      ? `Reallocate 30% of dispatch volume away from ${metrics.worstCarrier?.carrier || 'underperforming couriers'} to ${metrics.bestCarrier?.carrier || 'top SLA carriers'} and enforce dispatch penalty clauses.`
      : 'Maintain current carrier volume routing ratios and monitor weekend transit buffers.',
    priority: metrics.onTimeRate < 85 ? 'P0 - Immediate' : isSlaBreach ? 'P1 - Urgent' : 'P3 - Medium',
    area: 'Shipping',
    confidence: 0.95,
    expected_business_impact: isSlaBreach
      ? 'Restores fulfillment SLA to > 92% and avoids marketplace late delivery penalties'
      : 'Maintains high customer satisfaction ratings and repeat purchase velocity',
    source: ['Shipping_Data', 'Internal_Sales'],
    agent: 'Inventory & Shipping',
  });

  // Finding 2: Worst Carrier Outlier
  if (metrics.worstCarrier && metrics.worstCarrier.onTimeRate < 88 && metrics.worstCarrier.total >= 5) {
    findings.push({
      id: `log-find-2-${selectedDate}`,
      metric: `Carrier SLA Breach: ${metrics.worstCarrier.carrier}`,
      current_value: `${metrics.worstCarrier.onTimeRate}% On-Time (${metrics.worstCarrier.delayed} delays)`,
      previous_value: '92.0% SLA Threshold',
      change_percent: Number((metrics.worstCarrier.onTimeRate - 92.0).toFixed(1)),
      severity: metrics.worstCarrier.onTimeRate < 82 ? 'critical' : 'high',
      finding: `${metrics.worstCarrier.carrier} breached delivery standards with an on-time rate of ${metrics.worstCarrier.onTimeRate}% (${metrics.worstCarrier.delayed} late deliveries averaging ${metrics.worstCarrier.avgDelay} days delay).`,
      possible_causes: [
        'Hub sorting congestion at destination delivery centers',
        'Repeated non-delivery report (NDR) exceptions on COD shipments',
      ],
      recommended_action: `Impose a temporary daily dispatch volume cap on ${metrics.worstCarrier.carrier} and mandate pre-delivery customer OTP verification.`,
      priority: 'P1 - Urgent',
      area: 'Shipping',
      confidence: 0.94,
      expected_business_impact: `Eliminates ~${metrics.worstCarrier.delayed} delayed customer deliveries per day`,
      source: ['Shipping_Data'],
      agent: 'Inventory & Shipping',
    });
  }

  const duration = Date.now() - startTime;

  return {
    agentId: 'logistics-intelligence',
    agentName: logisticsAgentSpec.name,
    status: 'completed',
    executionDurationMs: duration,
    findings,
    computedMetrics: metrics,
    reasoningSummary: `Audited ${metrics.totalShipments} dispatches across ${metrics.carrierStats.length} carrier partners for ${selectedDate}. Overall OTD SLA: ${metrics.onTimeRate}%, Average delay: ${metrics.avgDelay} days. Lowest carrier: ${metrics.worstCarrier?.carrier || 'N/A'} (${metrics.worstCarrier?.onTimeRate || 0}%).`,
    keyMetricObserved: `${metrics.onTimeRate}% On-Time Delivery (${metrics.delayedOrdersCount} Delays, ${metrics.carrierStats.length} Carriers)`,
    topFinding: findings[0]?.finding,
    topRecommendation: findings[0]?.recommended_action,
  };
}
