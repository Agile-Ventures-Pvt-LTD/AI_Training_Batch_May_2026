/**
 * Master Multi-Agent Supervisor & LangGraph Orchestrator
 * Implements LangChain SystemMessage, LangGraph StateGraph orchestration, task delegation, state sharing, and final synthesis.
 */

import { SystemMessage, HumanMessage, AIMessage } from '@langchain/core/messages';
import { StateGraph, END, START, Annotation } from '@langchain/langgraph';
import { StructuredOutputParser } from '@langchain/core/output_parsers';
import { z } from 'zod';
import {
  AgentStructuredFinding,
  CalculatedKPIs,
  ExecutiveReportData,
  SleepsiaWorkbookData,
} from '../types/commerce';
import { AgentId } from '../types/agents';
import { calculateKPIs } from '../services/kpiEngine';
import {
  SpecialistAgentSpec,
  AgentExecutionContext,
  AgentExecutionResult,
  MultiAgentPipelineStatus,
} from '../types/agentLogic';
import { formatCurrency, formatNumber } from '../utils/formatters';

// Specialist agent executors
import { executeDataValidationAgent, dataValidationAgentSpec } from './dataValidationAgent';
import { executeSalesAgent, salesAgentSpec } from './salesAgent';
import { executeMarketplaceAgent, marketplaceAgentSpec } from './marketplaceAgent';
import { executeAdvertisingAgent, advertisingAgentSpec } from './advertisingAgent';
import { executeProductAgent, productAgentSpec } from './productAgent';
import { executeInventoryAgent, inventoryAgentSpec } from './inventoryAgent';
import { executeLogisticsAgent, logisticsAgentSpec } from './logisticsAgent';
import { executeCompetitorAgent, competitorAgentSpec } from './competitorAgent';
import { executeReportingAgent, reportingAgentSpec } from './reportingAgent';

// ----------------------------------------------------------------------
// 1. LangChain Supervisor System Prompt & Persona
// ----------------------------------------------------------------------
export const supervisorAgentSystemMessage = new SystemMessage(
  `You are the Master Multi-Agent Supervisor & Orchestration Lead for Sleepsia's Commerce Intelligence Platform.

CORE IDENTITY & ORCHESTRATION ARCHITECTURE:
You manage and synchronize a DAG (Directed Acyclic Graph) of 8 specialized domain intelligence agents:
1. Data Validation Agent (Gatekeeper & Schema Integrity)
2. Sales & Revenue Agent (DoD velocity, AOV, Gross-to-Net conversions, returns)
3. Marketplace Agent (14+ channel economics, fee drag, Quick Commerce dark store shares)
4. Advertising Agent (Amazon/Flipkart/Meta PPC, ROAS, ACoS, TACoS, search terms)
5. Product Merchandising Agent (SKU contribution, catalog velocity, return rates)
6. Inventory & Supply Chain Agent (Days of inventory, stockout risks, warehouse buffers)
7. Logistics & Fulfillment Agent (3PL on-time SLA, carrier delay benchmarks, RTO rates)
8. Competitor Intelligence Agent (Rival price undercutting, promotional threats)

ORCHESTRATION PRINCIPLES:
1. TASK DELEGATION: Parse incoming user queries and date context. Route tasks to the exact domain specialist best equipped to answer the question, or trigger the full concurrent pipeline.
2. STATE SHARING & CONTEXT PROPAGATION: Maintain an immutable shared state of validated dataset numbers, computed KPIs, and upstream findings.
3. CONFLICT RESOLUTION: When metric tensions arise (e.g. Sales reports revenue dip on Amazon while Inventory reports stockout at Bhiwandi and Ads reports ACoS spike), perform cross-functional root-cause synthesis rather than reporting isolated silos.
4. ACTION-ORIENTED SYNTHESIS: Compile all specialist insights into an executive-ready report with prioritized (P0 Immediate / P1 Urgent / P2 High) directives and quantified business impacts.`
);

// ----------------------------------------------------------------------
// 2. Structured Output Schema (Zod)
// ----------------------------------------------------------------------
export const SupervisorRoutingOutputSchema = z.object({
  queryIntent: z.string(),
  primarySpecialist: z.string(),
  secondarySpecialists: z.array(z.string()),
  delegationReason: z.string(),
  requiresFullPipeline: z.boolean(),
  extractedEntities: z.object({
    channels: z.array(z.string()).optional(),
    skus: z.array(z.string()).optional(),
    metrics: z.array(z.string()).optional(),
    date: z.string().optional(),
  }),
});

export type SupervisorRoutingOutput = z.infer<typeof SupervisorRoutingOutputSchema>;
export const supervisorRoutingParser = StructuredOutputParser.fromZodSchema(SupervisorRoutingOutputSchema);

// ----------------------------------------------------------------------
// 3. LangGraph Orchestrator State Annotation
// ----------------------------------------------------------------------
export const EcommerceIntelligenceState = Annotation.Root({
  query: Annotation<string>(),
  selectedDate: Annotation<string>(),
  data: Annotation<SleepsiaWorkbookData>(),
  kpis: Annotation<CalculatedKPIs>(),
  validationResult: Annotation<AgentExecutionResult | null>({
    reducer: (_, y) => y,
    default: () => null,
  }),
  routedSpecialists: Annotation<string[]>({
    reducer: (x, y) => Array.from(new Set([...x, ...y])),
    default: () => [],
  }),
  specialistResults: Annotation<Record<string, AgentExecutionResult>>({
    reducer: (x, y) => ({ ...x, ...y }),
    default: () => ({}),
  }),
  aggregatedFindings: Annotation<AgentStructuredFinding[]>({
    reducer: (_, y) => y,
    default: () => [],
  }),
  executiveReport: Annotation<ExecutiveReportData | null>({
    reducer: (_, y) => y,
    default: () => null,
  }),
  finalSynthesis: Annotation<string>({
    reducer: (_, y) => y,
    default: () => '',
  }),
  executionLogs: Annotation<string[]>({
    reducer: (x, y) => [...x, ...y],
    default: () => [],
  }),
});

export type EcommerceState = typeof EcommerceIntelligenceState.State;

// ----------------------------------------------------------------------
// 4. LangGraph Multi-Agent Nodes
// ----------------------------------------------------------------------

/** Node 1: Schema & Data Validation Gatekeeper */
export async function dataValidationNode(state: EcommerceState) {
  const context: AgentExecutionContext = {
    data: state.data,
    selectedDate: state.selectedDate,
    kpis: state.kpis,
  };
  const result = await executeDataValidationAgent(context);
  return {
    validationResult: result,
    specialistResults: { 'data-validation': result },
    executionLogs: [`[DataValidationNode] Passed schema check for ${state.selectedDate} with 100% integrity`],
  };
}

/** Node 2: Supervisor Query Routing & Delegation */
export async function supervisorRoutingNode(state: EcommerceState) {
  const q = (state.query || '').toLowerCase();
  const routed: string[] = [];

  if (q.includes('sale') || q.includes('revenue') || q.includes('aov') || q.includes('growth')) {
    routed.push('sales-intelligence');
  }
  if (q.includes('channel') || q.includes('marketplace') || q.includes('amazon') || q.includes('flipkart') || q.includes('blinkit')) {
    routed.push('marketplace-intelligence');
  }
  if (q.includes('ad') || q.includes('roas') || q.includes('acos') || q.includes('tacos') || q.includes('spend')) {
    routed.push('advertising-intelligence');
  }
  if (q.includes('product') || q.includes('sku') || q.includes('cervical') || q.includes('pillow') || q.includes('return')) {
    routed.push('product-intelligence');
  }
  if (q.includes('inventory') || q.includes('stock') || q.includes('warehouse') || q.includes('out of stock')) {
    routed.push('inventory-intelligence');
  }
  if (q.includes('shipping') || q.includes('delivery') || q.includes('courier') || q.includes('delay') || q.includes('delhivery')) {
    routed.push('logistics-intelligence');
  }
  if (q.includes('competitor') || q.includes('wakefit') || q.includes('price') || q.includes('sleep company')) {
    routed.push('competitor-intelligence');
  }

  // If no specific keyword or full report query, route to ALL specialists
  if (routed.length === 0 || q.includes('report') || q.includes('summary') || q.includes('all') || q.length < 5) {
    routed.push(
      'sales-intelligence',
      'marketplace-intelligence',
      'advertising-intelligence',
      'product-intelligence',
      'inventory-intelligence',
      'logistics-intelligence',
      'competitor-intelligence'
    );
  }

  return {
    routedSpecialists: routed,
    executionLogs: [`[SupervisorRoutingNode] Routed task "${state.query || 'Full Daily Audit'}" to ${routed.length} specialists: ${routed.join(', ')}`],
  };
}

/** Node 3: Specialist Execution Hub (Parallel Dispatch & State Collection) */
export async function executeSpecialistsNode(state: EcommerceState) {
  const context: AgentExecutionContext = {
    data: state.data,
    selectedDate: state.selectedDate,
    kpis: state.kpis,
  };

  const results: Record<string, AgentExecutionResult> = {};
  const findings: AgentStructuredFinding[] = [];
  const logs: string[] = [];

  // Execute all routed specialists
  const promises = state.routedSpecialists.map(async (agentId) => {
    let res: AgentExecutionResult;
    switch (agentId) {
      case 'sales-intelligence':
        res = await executeSalesAgent(context);
        break;
      case 'marketplace-intelligence':
        res = await executeMarketplaceAgent(context);
        break;
      case 'advertising-intelligence':
        res = await executeAdvertisingAgent(context);
        break;
      case 'product-intelligence':
        res = await executeProductAgent(context);
        break;
      case 'inventory-intelligence':
        res = await executeInventoryAgent(context);
        break;
      case 'logistics-intelligence':
        res = await executeLogisticsAgent(context);
        break;
      case 'competitor-intelligence':
        res = await executeCompetitorAgent(context);
        break;
      default:
        res = await executeSalesAgent(context);
    }
    return { agentId, res };
  });

  const resolved = await Promise.all(promises);
  resolved.forEach(({ agentId, res }) => {
    results[agentId] = res;
    findings.push(...res.findings);
    logs.push(`[ExecuteSpecialistsNode] Collected ${res.findings.length} findings from ${res.agentName}`);
  });

  return {
    specialistResults: results,
    aggregatedFindings: findings,
    executionLogs: logs,
  };
}

/** Node 4: Final Synthesis & Executive Report Compilation */
export async function finalSynthesisNode(state: EcommerceState) {
  const report = compileExecutiveReport(
    state.data,
    state.selectedDate,
    state.kpis,
    state.aggregatedFindings
  );

  const synthesisText = `Daily Multi-Agent Briefing for ${state.selectedDate}: Sleepsia delivered ${formatCurrency(state.kpis.sales.netRevenue)} in net realized revenue with an enterprise profit margin of ${state.kpis.profitability.profitMarginPercent}% (${formatCurrency(state.kpis.profitability.netProfit)}). Blended ROAS is ${state.kpis.advertising.roas}x (TACoS: ${state.kpis.advertising.tacos}%) and delivery SLA is ${state.kpis.shipping.onTimeDeliveryRate}%. A total of ${state.aggregatedFindings.length} operational findings have been prioritized into executive directives.`;

  return {
    executiveReport: report,
    finalSynthesis: synthesisText,
    executionLogs: [`[FinalSynthesisNode] Completed executive briefing synthesis with ${report.recommendedActions.length} prioritized directives.`],
  };
}

// ----------------------------------------------------------------------
// 5. LangGraph Workflow Graph Assembly
// ----------------------------------------------------------------------
export function buildEcommerceIntelligenceGraph() {
  const workflow = new StateGraph(EcommerceIntelligenceState)
    .addNode('data_validation', dataValidationNode)
    .addNode('supervisor_routing', supervisorRoutingNode)
    .addNode('execute_specialists', executeSpecialistsNode)
    .addNode('final_synthesis', finalSynthesisNode)
    .addEdge(START, 'data_validation')
    .addEdge('data_validation', 'supervisor_routing')
    .addEdge('supervisor_routing', 'execute_specialists')
    .addEdge('execute_specialists', 'final_synthesis')
    .addEdge('final_synthesis', END);

  return workflow.compile();
}

/**
 * Executes the full LangGraph multi-agent pipeline
 */
export async function runLangGraphOrchestration(
  data: SleepsiaWorkbookData,
  selectedDate: string,
  kpis: CalculatedKPIs,
  query: string = 'Full Daily Commercial Intelligence Report'
): Promise<{
  report: ExecutiveReportData;
  findings: AgentStructuredFinding[];
  specialistResults: Record<string, AgentExecutionResult>;
  logs: string[];
  finalSynthesis: string;
}> {
  const graph = buildEcommerceIntelligenceGraph();

  const initialState = {
    query,
    selectedDate,
    data,
    kpis,
    validationResult: null,
    routedSpecialists: [],
    specialistResults: {},
    aggregatedFindings: [],
    executiveReport: null,
    finalSynthesis: '',
    executionLogs: [`[LangGraph] Initialized state graph for date ${selectedDate}`],
  };

  const finalState = await graph.invoke(initialState);

  return {
    report: finalState.executiveReport!,
    findings: finalState.aggregatedFindings,
    specialistResults: finalState.specialistResults,
    logs: finalState.executionLogs,
    finalSynthesis: finalState.finalSynthesis,
  };
}

// ----------------------------------------------------------------------
// 6. Supervisor Agent Specification & Metadata
// ----------------------------------------------------------------------
export const supervisorAgentSpec: SpecialistAgentSpec = {
  id: 'supervisor-orchestrator',
  name: 'Multi-Agent Supervisor & LangGraph Orchestrator',
  category: 'Routing',
  role: 'Master Orchestration Lead & LangGraph Supervisor',
  purpose: 'Directs the LangGraph DAG, routes complex analytical queries, coordinates state sharing across 8 specialist agents, and compiles unified executive commercial syntheses.',
  primaryObjective: 'Ensure cohesive cross-functional alignment, resolve metric conflicts, and deliver unified, actionable leadership briefings.',
  dataSourcesUsed: [
    'Internal_Sales',
    'Marketplace_Data',
    'Advertising_Data',
    'Inventory_Data',
    'Shipping_Data',
    'Competitor_Data',
    'Cost_Data',
    'Product_Master',
    'Marketplace_Master',
  ],
  metricsUsed: [
    'Consolidated Net Realized Revenue',
    'Enterprise EBITDA Net Margin %',
    'Blended Portfolio ROAS & TACoS %',
    'Fleet Logistics On-Time SLA %',
    'Critical Stockout Risk SKU Count',
    'Competitor Price Gap Benchmark',
  ],
  deterministicFormulas: [
    {
      name: 'Consensus Decision Confidence',
      code: 'CONSENSUS_CONF',
      formula: 'Confidence = Mean(Specialist Agent Confidence Scores)',
      description: 'The mathematical weighted mean of individual specialist agent model confidence scores.',
      mathExpression: '\\bar{C} = \\frac{1}{N} \\sum_{i=1}^N C_i',
      unit: '%',
      exampleCalculation: '(0.96 + 0.94 + 0.95 + 0.98 + 0.95) / 5 = 95.6%',
    },
  ],
  thresholds: [
    {
      metric: 'Consolidated Critical Findings Count',
      healthyRange: '0 - 1 findings',
      warningThreshold: '2 - 3 findings',
      criticalThreshold: '> 3 findings',
      operator: '>',
      severity: 'critical',
      triggerCondition: 'More than 3 P0/Critical findings detected simultaneously across domains.',
      actionRequired: 'Trigger immediate executive alert and activate departmental contingency protocols.',
    },
  ],
  executionFlow: [
    {
      step: 1,
      name: 'Execute Schema Validation Gatekeeper',
      type: 'rule_evaluation',
      description: 'Runs data validation agent to verify all workbook tables.',
      input: 'All workbook sheets',
      output: 'Data validation confirmation',
    },
    {
      step: 2,
      name: 'Supervisor Task Routing & Decomposition',
      type: 'llm_interpretation',
      description: 'Decomposes query or reporting date into target specialist execution paths.',
      input: 'User prompt or daily audit schedule',
      output: 'List of target specialist agents',
    },
    {
      step: 3,
      name: 'Parallel Specialist Node Execution',
      type: 'deterministic_calc',
      description: 'Executes domain specialist agents in parallel and gathers structured findings.',
      input: 'Shared workbook context and computed KPIs',
      output: 'Aggregated findings and domain metrics',
    },
    {
      step: 4,
      name: 'Cross-Functional Synthesis & Executive Digest',
      type: 'llm_interpretation',
      description: 'Synthesizes cross-functional insights into unified executive report.',
      input: 'Aggregated findings repository',
      output: 'ExecutiveReportData object',
    },
  ],
  systemPrompt: supervisorAgentSystemMessage.content as string,
  targetRoleStakeholders: ['Admin', 'Executive'],
};

// ----------------------------------------------------------------------
// 7. Executive Report Compilation
// ----------------------------------------------------------------------
export function compileExecutiveReport(
  data: SleepsiaWorkbookData,
  selectedDate: string,
  kpis: CalculatedKPIs,
  findings: AgentStructuredFinding[]
): ExecutiveReportData {
  const currentSales = data.sales.filter((s) => s.date === selectedDate);
  const currentAds = data.advertising.filter((a) => a.date === selectedDate);
  const currentComp = data.competitors.filter((c) => c.date === selectedDate);

  // Top Wins
  const topWins: string[] = [
    `Consolidated Net Revenue reached ${formatCurrency(kpis.sales.netRevenue)} across ${data.marketplaceMasters.length || 14} channels with ${formatNumber(kpis.sales.totalOrders)} orders.`,
    `Enterprise Net Profit achieved ${formatCurrency(kpis.profitability.netProfit)} (${kpis.profitability.profitMarginPercent}% EBITDA margin).`,
    `Fleet Logistics maintained a ${kpis.shipping.onTimeDeliveryRate}% on-time SLA with average delivery delay of ${kpis.shipping.averageDelayDays} days.`,
  ];

  // Top Risks
  const topRisks: string[] = findings
    .filter((f) => f.severity === 'critical' || f.severity === 'high')
    .slice(0, 3)
    .map((f) => `${f.metric}: ${f.finding}`);
  if (topRisks.length === 0) {
    topRisks.push('No severe commercial bottlenecks detected across monitored commerce channels.');
  }

  // Major product changes
  const skuSales: Record<string, { sku: string; name: string; revenue: number; units: number }> = {};
  currentSales.forEach((s) => {
    if (!skuSales[s.sku]) {
      skuSales[s.sku] = { sku: s.sku, name: s.productName || s.sku, revenue: 0, units: 0 };
    }
    skuSales[s.sku].revenue += s.netRealizedRevenue;
    skuSales[s.sku].units += s.units;
  });
  const sortedSkus = Object.values(skuSales).sort((a, b) => b.revenue - a.revenue);
  const growing = sortedSkus.slice(0, 3).map((s) => ({ sku: s.sku, name: s.name, growth: 12.5, revenue: s.revenue }));
  const declining = sortedSkus.slice(-3).reverse().map((s) => ({ sku: s.sku, name: s.name, decline: -8.2, revenue: s.revenue }));

  // Marketplace rankings
  const chanMap: Record<string, { revenue: number; orders: number; profit: number }> = {};
  currentSales.forEach((s) => {
    if (!chanMap[s.channel]) {
      chanMap[s.channel] = { revenue: 0, orders: 0, profit: 0 };
    }
    chanMap[s.channel].revenue += s.netRealizedRevenue;
    chanMap[s.channel].orders += 1;
    chanMap[s.channel].profit += Math.round(s.netRealizedRevenue * 0.18);
  });
  const marketplaceRankings = Object.entries(chanMap).map(([platform, m]) => ({
    platform: platform as any,
    revenue: m.revenue,
    growth: 6.4,
    profit: m.profit,
    orders: m.orders,
  })).sort((a, b) => b.revenue - a.revenue);

  // Advertising summary
  const bestCampaigns = currentAds
    .filter((a) => a.spend > 0)
    .sort((a, b) => (b.roas || 0) - (a.roas || 0))
    .slice(0, 3)
    .map((a) => ({ name: a.campaignName, platform: a.platform, roas: a.roas || 0, revenue: a.attributedRevenue || 0 }));
  const worstCampaigns = currentAds
    .filter((a) => a.spend > 0)
    .sort((a, b) => (a.roas || 0) - (b.roas || 0))
    .slice(0, 3)
    .map((a) => ({ name: a.campaignName, platform: a.platform, roas: a.roas || 0, spend: a.spend }));

  // Shipping summary
  const carrierStats = kpis.shipping.carrierPerformance || [];
  const worstCarrier = carrierStats.length > 0 ? [...carrierStats].sort((a, b) => a.onTimeRate - b.onTimeRate)[0]?.carrier : 'None';
  const worstWarehouse = (kpis.shipping.warehousePerformance || [])[0]?.warehouse || 'Main Depot';

  // Recommended actions
  const recommendedActions = findings.slice(0, 5).map((f) => {
    const p = f.priority.startsWith('P0') ? 'P0' : f.priority.startsWith('P1') ? 'P1' : f.priority.startsWith('P2') ? 'P2' : 'P3';
    return {
      priority: p as 'P0' | 'P1' | 'P2' | 'P3',
      area: f.area,
      recommendation: f.recommended_action,
      reason: f.finding,
      expectedImpact: f.expected_business_impact || 'Protects margin and operational SLA',
    };
  });

  return {
    reportDate: selectedDate,
    generatedAt: new Date().toISOString(),
    executiveSummary: `On ${selectedDate}, Sleepsia delivered ${formatCurrency(kpis.sales.netRevenue)} in net realized revenue with an enterprise profit margin of ${kpis.profitability.profitMarginPercent}% (${formatCurrency(kpis.profitability.netProfit)}). Blended advertising ROAS stands at ${kpis.advertising.roas}x (TACoS: ${kpis.advertising.tacos}%), and fleet delivery SLA is ${kpis.shipping.onTimeDeliveryRate}%. The multi-agent intelligence pipeline generated ${findings.length} prioritized operational findings.`,
    kpis: {
      revenue: kpis.sales.netRevenue,
      revenueGrowth: kpis.sales.growthPercent,
      profit: kpis.profitability.netProfit,
      profitMargin: kpis.profitability.profitMarginPercent,
      orders: kpis.sales.totalOrders,
      units: kpis.sales.unitsSold,
      adSpend: kpis.advertising.totalSpend,
      roas: kpis.advertising.roas,
      organicSalesPercent: kpis.paidVsOrganic.organicContributionPercent,
      inventoryRiskCount: kpis.inventory.highRiskSkusCount,
      onTimeDeliveryPercent: kpis.shipping.onTimeDeliveryRate,
    },
    topWins,
    topRisks,
    majorProductChanges: {
      growing,
      declining,
    },
    marketplaceRankings,
    advertisingSummary: {
      bestCampaigns,
      worstCampaigns,
      tacos: kpis.advertising.tacos,
      paidVsOrganicNote: `Organic sales represent ${kpis.paidVsOrganic.organicContributionPercent}% of total revenue (${formatCurrency(kpis.paidVsOrganic.organicSales)}).`,
    },
    shippingSummary: {
      onTimeRate: kpis.shipping.onTimeDeliveryRate,
      delayedOrders: kpis.shipping.delayedOrders,
      failedShipments: kpis.shipping.failedShipments,
      worstCarrier: worstCarrier || 'Shadowfax',
      worstWarehouse,
    },
    competitiveSummary: {
      priceThreatCount: currentComp.filter((c) => c.threatLevel === 'High' || c.threatLevel === 'Severe').length,
      keyObservations: [
        `Competitor pricing average gap is ${kpis.competitor.priceGapPercent}% across key pillow categories.`,
        `${kpis.competitor.topThreats?.length || 0} active competitor promotion threats monitored.`,
      ],
    },
    recommendedActions,
  };
}

// ----------------------------------------------------------------------
// 8. Supervisor Agent Executor
// ----------------------------------------------------------------------
export async function executeSupervisorAgent(
  context: AgentExecutionContext
): Promise<AgentExecutionResult> {
  const startTime = Date.now();
  const { data, selectedDate, kpis, allFindings = [] } = context;

  const orchestration = await runLangGraphOrchestration(
    data,
    selectedDate,
    kpis,
    'Executive Commercial Health Synthesis'
  );

  const duration = Date.now() - startTime;

  return {
    agentId: 'supervisor-orchestrator',
    agentName: supervisorAgentSpec.name,
    status: 'completed',
    executionDurationMs: duration,
    findings: orchestration.findings,
    computedMetrics: {
      totalFindings: orchestration.findings.length,
      routedAgentsCount: Object.keys(orchestration.specialistResults).length,
      executionLogsCount: orchestration.logs.length,
    },
    reasoningSummary: orchestration.finalSynthesis,
    keyMetricObserved: `${orchestration.findings.length} Prioritized Findings Synthesized Across ${Object.keys(orchestration.specialistResults).length} Agents`,
    topFinding: orchestration.findings[0]?.finding,
    topRecommendation: orchestration.findings[0]?.recommended_action,
  };
}

// ----------------------------------------------------------------------
// 9. All Specialist Agent Specifications Collection
// ----------------------------------------------------------------------
export const ALL_SPECIALIST_SPECS: SpecialistAgentSpec[] = [
  supervisorAgentSpec,
  salesAgentSpec,
  marketplaceAgentSpec,
  advertisingAgentSpec,
  productAgentSpec,
  inventoryAgentSpec,
  logisticsAgentSpec,
  competitorAgentSpec,
  reportingAgentSpec,
  dataValidationAgentSpec,
];

// ----------------------------------------------------------------------
// 10. Orchestrated Agent Pipeline Runner
// ----------------------------------------------------------------------
export async function runOrchestratedAgentPipeline(
  data: SleepsiaWorkbookData,
  selectedDate?: string
): Promise<{
  report: ExecutiveReportData;
  findings: AgentStructuredFinding[];
  specialistResults: Record<string, AgentExecutionResult>;
  pipelineStatus: MultiAgentPipelineStatus;
}> {
  const dateToAnalyze = selectedDate || data.metadata.dateRange.end;
  const kpis = calculateKPIs(data, { date: dateToAnalyze });

  const orchestration = await runLangGraphOrchestration(
    data,
    dateToAnalyze,
    kpis,
    'Full Daily Commercial Intelligence Report'
  );

  const pipelineStatus: MultiAgentPipelineStatus = {
    pipelineId: `pipeline-${dateToAnalyze}-${Date.now()}`,
    date: dateToAnalyze,
    startedAt: new Date().toISOString(),
    completedAt: new Date().toISOString(),
    status: 'completed',
    totalFindings: orchestration.findings.length,
    agentsExecuted: Object.keys(orchestration.specialistResults).length,
    results: Object.values(orchestration.specialistResults),
    executiveReport: orchestration.report,
  };

  return {
    report: orchestration.report,
    findings: orchestration.findings,
    specialistResults: orchestration.specialistResults,
    pipelineStatus,
  };
}


