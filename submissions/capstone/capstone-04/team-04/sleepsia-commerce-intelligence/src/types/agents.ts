/**
 * Multi-Agent Orchestration Architecture Type Definitions
 */

export type AgentId =
  | 'supervisor'
  | 'supervisor-orchestrator'
  | 'data-validation'
  | 'sales-intelligence'
  | 'marketplace-intelligence'
  | 'advertising-intelligence'
  | 'product-intelligence'
  | 'inventory-intelligence'
  | 'inventory-risk'
  | 'logistics-intelligence'
  | 'logistics-fulfillment'
  | 'competitor-intelligence'
  | 'reporting-synthesis'
  | 'executive-reporting';

export type AgentStatus = 'idle' | 'running' | 'completed' | 'skipped' | 'warning' | 'error';

export interface AgentExecutionState {
  id: AgentId;
  name: string;
  category: 'Validation' | 'Domain Intelligence' | 'Supply Chain' | 'External' | 'Synthesis';
  icon: string;
  purpose?: string;
  currentActivity?: string;
  status: AgentStatus;
  executionOrder: number;
  inputDatasets: string[];
  reasoningSummary: string;
  findingsCount: number;
  confidence: number; // 0 - 1
  keyMetricObserved?: string;
  topFinding?: string;
  topRecommendation?: string;
  skipReason?: string;
  completedAt?: string;
  executionDurationMs?: number;
}

export interface OrchestrationPipeline {
  runId: string;
  startedAt: string;
  completedAt?: string;
  supervisorStatus: 'orchestrating' | 'completed' | 'analyzing';
  activeAgentsCount: number;
  skippedAgentsCount: number;
  totalFindings: number;
  overallConfidence: number;
  datasetsEvaluated: {
    dataset: string;
    status: 'Valid' | 'Partial' | 'Unavailable';
    rowCount: number;
  }[];
  agents: AgentExecutionState[];
}

export interface RootCauseTrace {
  id: string;
  title: string;
  observedSymptom: string;
  severity: 'critical' | 'high' | 'medium';
  category: string;
  chainOfSignals: {
    stage: string;
    signal: string;
    classification: 'Observed Fact' | 'Likely Driver' | 'Root Cause' | 'Secondary Effect' | 'Excluded Factor';
    evidence: string;
    confidence: number;
  }[];
  verdict: {
    distinction: 'Causation Verified' | 'Correlation Only' | 'Inconclusive';
    explanation: string;
  };
  recommendedAction: {
    priority: 'P0 - Immediate' | 'P1 - Urgent' | 'P2 - High' | 'P3 - Medium';
    action: string;
    expectedImpact: string;
    assignedRole: string;
  };
}
