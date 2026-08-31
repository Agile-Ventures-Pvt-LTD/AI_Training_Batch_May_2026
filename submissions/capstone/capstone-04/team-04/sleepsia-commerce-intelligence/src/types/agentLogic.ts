/**
 * Agent Logic, Formula, and Rule Types
 * Provides strongly-typed specifications for specialist agents, deterministic calculations,
 * anomaly thresholds, data lineage, and execution flows.
 */

import { AgentStructuredFinding, CalculatedKPIs, SleepsiaWorkbookData } from './commerce';
import { AgentId, AgentStatus } from './agents';

export interface DeterministicFormula {
  name: string;
  code: string;
  formula: string;
  description: string;
  mathExpression: string;
  unit: string;
  exampleCalculation?: string;
}

export type DeterministicFormulaSpec = DeterministicFormula;

export interface AnomalyThreshold {
  metric: string;
  healthyRange: string;
  warningThreshold: string;
  criticalThreshold: string;
  operator: '<' | '>' | '<=' | '>=' | 'range' | 'delta';
  severity: 'low' | 'medium' | 'high' | 'critical';
  triggerCondition: string;
  actionRequired: string;
}

export type AnomalyThresholdSpec = AnomalyThreshold;

export interface ExecutionStep {
  step: number;
  name: string;
  type: 'deterministic_calc' | 'data_reconciliation' | 'rule_evaluation' | 'llm_interpretation' | 'synthesis';
  description: string;
  input: string;
  output: string;
}

export interface SpecialistAgentSpec {
  id: AgentId;
  name: string;
  category: 'Validation' | 'Domain Intelligence' | 'Supply Chain' | 'External' | 'Synthesis' | 'Routing';
  role: string;
  purpose: string;
  primaryObjective: string;
  dataSourcesUsed: string[];
  metricsUsed: string[];
  deterministicFormulas: DeterministicFormula[];
  thresholds: AnomalyThreshold[];
  executionFlow: ExecutionStep[];
  systemPrompt: string;
  targetRoleStakeholders: string[];
}

export interface AgentExecutionContext {
  data: SleepsiaWorkbookData;
  selectedDate: string;
  kpis: CalculatedKPIs;
  previousDate?: string;
  previousKpis?: CalculatedKPIs;
  allFindings?: AgentStructuredFinding[];
}

export interface AgentExecutionResult {
  agentId: AgentId;
  agentName: string;
  status: AgentStatus;
  executionDurationMs: number;
  findings: AgentStructuredFinding[];
  computedMetrics: Record<string, any>;
  reasoningSummary: string;
  keyMetricObserved: string;
  topFinding?: string;
  topRecommendation?: string;
  skipReason?: string;
}

export interface MultiAgentPipelineStatus {
  pipelineId: string;
  date: string;
  startedAt: string;
  completedAt?: string;
  status: 'running' | 'completed' | 'error';
  totalFindings: number;
  agentsExecuted: number;
  results: AgentExecutionResult[];
  executiveReport?: any;
}

