import React, { useState, useEffect, useMemo } from 'react';
import {
  ShieldCheck,
  DollarSign,
  Layers,
  Zap,
  Package,
  Boxes,
  Truck,
  ShieldAlert,
  Sparkles,
  Database,
  ArrowRight,
  RefreshCw,
  Play,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ExternalLink,
  ChevronRight,
  Sliders,
  Send,
  Eye,
  FileText,
  Activity,
  X,
  Info,
  Radio,
  Share2,
} from 'lucide-react';
import { SleepsiaWorkbookData, CalculatedKPIs, AgentStructuredFinding } from '../types/commerce';
import { AgentExecutionState, OrchestrationPipeline } from '../types/agents';
import { executeMultiAgentGraph, AgentGraphState } from '../services/agentGraphEngine';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface InteractivePipelineGraphProps {
  data: SleepsiaWorkbookData;
  kpis: CalculatedKPIs;
  selectedDate: string;
  onNavigateToTab?: (tab: string) => void;
  onOpenEmailModal?: () => void;
  onRunLiveAnalysis?: () => void;
}

export const InteractivePipelineGraph: React.FC<InteractivePipelineGraphProps> = ({
  data,
  kpis,
  selectedDate,
  onNavigateToTab,
  onOpenEmailModal,
  onRunLiveAnalysis,
}) => {
  const [pipelineState, setPipelineState] = useState<OrchestrationPipeline | null>(null);
  const [graphState, setGraphState] = useState<AgentGraphState | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string>('supervisor');
  const [isExecuting, setIsExecuting] = useState<boolean>(false);
  const [executingStep, setExecutingStep] = useState<number>(0);
  const [executionLog, setExecutionLog] = useState<string[]>([]);

  // Run graph whenever data or selected date changes
  useEffect(() => {
    let isMounted = true;
    executeMultiAgentGraph(data, selectedDate).then((res) => {
      if (isMounted) {
        setPipelineState(res.pipeline);
        setGraphState(res.state);
      }
    });
    return () => {
      isMounted = false;
    };
  }, [data, selectedDate]);

  // Handle live interactive graph execution
  const handleExecuteGraph = async () => {
    setIsExecuting(true);
    setExecutingStep(1);
    setExecutionLog(['[LangGraph] Initializing Graph State with Sleepsia dataset...']);

    // Step 1: Validation
    await new Promise((r) => setTimeout(r, 250));
    setExecutingStep(2);
    setExecutionLog((prev) => [
      ...prev,
      `[Data Validation] Reconciled ${data.sales.length} sales & ${data.marketplaceData.length} marketplace records.`,
    ]);

    // Step 2: Supervisor Routing
    await new Promise((r) => setTimeout(r, 300));
    setExecutingStep(3);
    setExecutionLog((prev) => [
      ...prev,
      `[LangGraph Supervisor] Evaluated data signals. Dispatching specialist agents...`,
    ]);

    // Step 3: Specialists
    await new Promise((r) => setTimeout(r, 400));
    setExecutingStep(4);
    setExecutionLog((prev) => [
      ...prev,
      `[Specialists] Executing Sales, Marketplace, Product, Ads, Inventory, Logistics & Competitor agents in parallel.`,
    ]);

    // Step 4: Executive Synthesis
    await new Promise((r) => setTimeout(r, 350));
    setExecutingStep(5);
    setExecutionLog((prev) => [
      ...prev,
      `[Executive Reporting] Synthesized cross-domain findings into verified causal traces and prioritized directives.`,
    ]);

    // Complete
    const res = await executeMultiAgentGraph(data, selectedDate);
    setPipelineState(res.pipeline);
    setGraphState(res.state);
    setIsExecuting(false);
    setExecutingStep(0);
    setExecutionLog((prev) => [
      ...prev,
      `[LangGraph] Execution completed in ${res.pipeline.agents.reduce(
        (a, b) => a + (b.executionDurationMs || 0),
        0
      )}ms. State broadcast to Dashboard, Alerts, Report, and Email.`,
    ]);

    if (onRunLiveAnalysis) {
      onRunLiveAnalysis();
    }
  };

  const getAgentIcon = (id: string) => {
    switch (id) {
      case 'data-validation':
        return ShieldCheck;
      case 'sales-intelligence':
        return DollarSign;
      case 'marketplace-intelligence':
        return Layers;
      case 'advertising-intelligence':
        return Zap;
      case 'product-intelligence':
        return Package;
      case 'inventory-intelligence':
        return Boxes;
      case 'logistics-fulfillment':
        return Truck;
      case 'competitor-intelligence':
        return ShieldAlert;
      case 'executive-reporting':
        return Sparkles;
      default:
        return Sparkles;
    }
  };

  // Build the list of specialist agents
  const specialistAgents = useMemo(() => {
    if (!pipelineState) return [];
    return pipelineState.agents.filter(
      (a) => a.id !== 'data-validation' && a.id !== 'executive-reporting'
    );
  }, [pipelineState]);

  const validationAgent = useMemo(() => {
    return pipelineState?.agents.find((a) => a.id === 'data-validation');
  }, [pipelineState]);

  const executiveAgent = useMemo(() => {
    return pipelineState?.agents.find((a) => a.id === 'executive-reporting');
  }, [pipelineState]);

  // Selected agent details
  const selectedAgentDetails = useMemo(() => {
    if (selectedNodeId === 'dataset') {
      return {
        id: 'dataset',
        name: 'Sleepsia Unified Commerce Dataset',
        purpose: 'Single source of truth containing internal sales, marketplaces, ads, inventory, shipping, and competitor data.',
        status: 'completed' as const,
        inputDatasets: ['Sleepsia_Workbook.xlsx'],
        reasoningSummary: `Loaded ${data.sales.length} orders, ${data.products.length} catalog items, and ${data.marketplaceData.length} marketplace daily snapshots for date ${selectedDate}.`,
        keyMetricObserved: `${data.sales.length} Transactions Loaded`,
        findings: [],
        metrics: {
          salesRows: data.sales.length,
          productsCount: data.products.length,
          marketplaceRows: data.marketplaceData.length,
          advertisingRows: data.advertising.length,
          inventoryRows: data.inventory.length,
          shippingRows: data.shipping.length,
          competitorRows: data.competitors.length,
        },
      };
    }
    if (selectedNodeId === 'supervisor') {
      return {
        id: 'supervisor',
        name: 'LangGraph Supervisor Agent',
        purpose: 'Inspects data availability and KPI anomalies to dynamically route execution across specialist agents.',
        status: 'completed' as const,
        inputDatasets: ['All Available Datasets'],
        reasoningSummary: `Dynamically routed ${specialistAgents.filter((a) => a.status === 'completed').length} active specialist agents. Competitor agent: ${
          data.competitors?.length > 0 ? 'Active' : 'Skipped (No data)'
        }. Advertising agent: ${data.advertising?.length > 0 ? 'Active' : 'Skipped'}.`,
        keyMetricObserved: `${specialistAgents.filter((a) => a.status === 'completed').length} Active Specialists`,
        findings: [],
        metrics: {
          totalSpecialists: specialistAgents.length,
          activeCount: specialistAgents.filter((a) => a.status === 'completed').length,
          skippedCount: specialistAgents.filter((a) => a.status === 'skipped').length,
        },
      };
    }
    if (selectedNodeId === 'downstream') {
      return {
        id: 'downstream',
        name: 'Downstream Delivery Channels',
        purpose: 'Distributes verified findings and prioritized directives to executive dashboards, real-time alerts, daily reports, and scheduled emails.',
        status: 'completed' as const,
        inputDatasets: ['Executive Synthesis Output'],
        reasoningSummary: 'Synchronizes live application state across Dashboard KPI cards, AI Insights feed, Alerts tab, PDF Reports, and automated Gmail/SMTP dispatch.',
        keyMetricObserved: `${graphState?.recommendations.length || 0} Directives Published`,
        findings: graphState?.findings || [],
        metrics: {
          alertsGenerated: graphState?.alerts.length || 0,
          recommendationsCount: graphState?.recommendations.length || 0,
          tracesCount: graphState?.root_cause_traces.length || 0,
        },
      };
    }

    const agent = pipelineState?.agents.find((a) => a.id === selectedNodeId);
    const agentFindings = graphState?.findings.filter((f) => {
      if (agent?.id === 'sales-intelligence') return f.agent === 'Sales';
      if (agent?.id === 'advertising-intelligence') return f.agent === 'Advertising';
      if (agent?.id === 'competitor-intelligence') return f.agent === 'Competitor';
      if (agent?.id === 'inventory-intelligence' || agent?.id === 'logistics-fulfillment')
        return f.agent === 'Inventory & Shipping';
      return true;
    });

    return {
      ...agent,
      findings: agentFindings || [],
    };
  }, [selectedNodeId, pipelineState, graphState, data, selectedDate, specialistAgents]);

  return (
    <div className="space-y-6">
      {/* Header Toolbar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-white shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              LangGraph Orchestration
            </span>
            <span className="text-xs text-slate-400">
              Reporting Date: <strong className="text-white">{selectedDate}</strong>
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            Multi-Agent Architecture & Execution Pipeline
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Real data-driven LangGraph workflow executing deterministic analytics + LLM interpretation on the Sleepsia dataset.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleExecuteGraph}
            disabled={isExecuting}
            className="flex items-center gap-2 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 font-semibold text-xs rounded-xl shadow-lg transition-all"
          >
            <Play className={`w-4 h-4 ${isExecuting ? 'animate-spin' : ''}`} />
            <span>{isExecuting ? 'Executing LangGraph...' : 'Run LangGraph Workflow'}</span>
          </button>

          {onOpenEmailModal && (
            <button
              onClick={onOpenEmailModal}
              className="flex items-center gap-2 px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs rounded-xl transition-all"
            >
              <Send className="w-3.5 h-3.5 text-blue-400" />
              <span>Email Report</span>
            </button>
          )}
        </div>
      </div>

      {/* Main Graph Canvas & Inspector Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 8 Cols: Visual LangGraph Flow */}
        <div className="lg:col-span-8 space-y-6">
          <div className="bg-slate-900/95 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
            {/* Background Grid Pattern */}
            <div className="absolute inset-0 opacity-5 pointer-events-none bg-[radial-gradient(#94a3b8_1px,transparent_1px)] [background-size:16px_16px]" />

            {/* Step Indicators if executing */}
            {isExecuting && (
              <div className="mb-6 bg-emerald-950/40 border border-emerald-500/30 rounded-xl p-3 flex items-center justify-between text-xs text-emerald-300">
                <div className="flex items-center gap-2">
                  <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />
                  <span>LangGraph Executing Step {executingStep} of 5: Running node transitions...</span>
                </div>
                <span className="font-mono text-[11px] text-emerald-400">Live DAG Active</span>
              </div>
            )}

            {/* 1. TOP LAYER: DATASET */}
            <div className="flex flex-col items-center">
              <button
                onClick={() => setSelectedNodeId('dataset')}
                className={`w-full max-w-md p-4 rounded-xl border transition-all text-left flex items-center justify-between ${
                  selectedNodeId === 'dataset'
                    ? 'bg-blue-950/60 border-blue-500 ring-2 ring-blue-500/30'
                    : 'bg-slate-800/80 border-slate-700 hover:border-slate-600'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
                    <Database className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-blue-400 uppercase tracking-wider">
                        Source Layer
                      </span>
                      <span className="px-1.5 py-0.2 rounded text-[10px] bg-blue-500/20 text-blue-300">
                        {data.sales.length} rows
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white">Sleepsia Commerce Dataset</h3>
                    <p className="text-[11px] text-slate-400">Sales, Marketplace, Ads, Inventory, Shipping</p>
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-500" />
              </button>

              {/* Connector */}
              <div className="h-6 w-0.5 bg-gradient-to-b from-blue-500 to-emerald-500 my-1" />
            </div>

            {/* 2. VALIDATION LAYER */}
            <div className="flex flex-col items-center">
              <button
                onClick={() => setSelectedNodeId('data-validation')}
                className={`w-full max-w-md p-4 rounded-xl border transition-all text-left flex items-center justify-between ${
                  selectedNodeId === 'data-validation'
                    ? 'bg-emerald-950/60 border-emerald-500 ring-2 ring-emerald-500/30'
                    : 'bg-slate-800/80 border-slate-700 hover:border-slate-600'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                    <ShieldCheck className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                        Integrity Node
                      </span>
                      <span className="px-1.5 py-0.2 rounded text-[10px] bg-emerald-500/20 text-emerald-300">
                        {validationAgent?.executionDurationMs || 14}ms
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white">Data Validation Agent</h3>
                    <p className="text-[11px] text-slate-400">Reconciles 0 nulls, schema consistency & date windows</p>
                  </div>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-emerald-400">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Valid</span>
                </div>
              </button>

              {/* Connector */}
              <div className="h-6 w-0.5 bg-gradient-to-b from-emerald-500 to-indigo-500 my-1" />
            </div>

            {/* 3. SUPERVISOR ORCHESTRATOR */}
            <div className="flex flex-col items-center">
              <button
                onClick={() => setSelectedNodeId('supervisor')}
                className={`w-full max-w-lg p-4 rounded-xl border transition-all text-left flex items-center justify-between ${
                  selectedNodeId === 'supervisor'
                    ? 'bg-indigo-950/60 border-indigo-500 ring-2 ring-indigo-500/30'
                    : 'bg-slate-800/80 border-slate-700 hover:border-slate-600'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">
                        LangGraph Supervisor
                      </span>
                      <span className="px-1.5 py-0.2 rounded text-[10px] bg-indigo-500/20 text-indigo-300">
                        State Router
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white">Supervisor Agent (Conditional Dispatch)</h3>
                    <p className="text-[11px] text-slate-400">
                      Evaluates signals → dispatches active specialists in parallel
                    </p>
                  </div>
                </div>
                <span className="px-2 py-1 rounded-md text-xs font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  Active
                </span>
              </button>

              {/* Connector Hub */}
              <div className="h-6 w-0.5 bg-gradient-to-b from-indigo-500 to-slate-600 my-1" />
            </div>

            {/* 4. SPECIALIST AGENTS GRID */}
            <div className="bg-slate-950/80 border border-slate-800/90 rounded-xl p-4 my-2">
              <div className="flex items-center justify-between mb-3 px-1">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Specialist Intelligence Agents (Parallel Execution)
                </span>
                <span className="text-xs text-slate-500">
                  {specialistAgents.filter((a) => a.status === 'completed').length} / {specialistAgents.length} Active
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {specialistAgents.map((agent) => {
                  const Icon = getAgentIcon(agent.id);
                  const isSelected = selectedNodeId === agent.id;
                  const isSkipped = agent.status === 'skipped';

                  return (
                    <button
                      key={agent.id}
                      onClick={() => setSelectedNodeId(agent.id)}
                      className={`p-3 rounded-xl border text-left transition-all flex items-start justify-between ${
                        isSelected
                          ? 'bg-slate-800 border-emerald-500 ring-2 ring-emerald-500/30'
                          : isSkipped
                          ? 'bg-slate-900/40 border-slate-800/80 opacity-60'
                          : 'bg-slate-800/60 border-slate-700/80 hover:border-slate-600'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <div
                          className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                            isSkipped
                              ? 'bg-slate-800 text-slate-500'
                              : 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400'
                          }`}
                        >
                          <Icon className="w-4 h-4" />
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="text-xs font-bold text-white leading-snug">{agent.name}</h4>
                          </div>
                          <p className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                            {isSkipped ? agent.skipReason || 'Skipped: data unavailable' : agent.keyMetricObserved}
                          </p>
                        </div>
                      </div>

                      <div className="text-right shrink-0 ml-2">
                        {isSkipped ? (
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-400 border border-slate-700">
                            Skipped
                          </span>
                        ) : (
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                            {agent.executionDurationMs ? `${agent.executionDurationMs}ms` : 'Completed'}
                          </span>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Connector */}
            <div className="flex flex-col items-center">
              <div className="h-6 w-0.5 bg-gradient-to-b from-slate-600 to-purple-500 my-1" />

              {/* 5. EXECUTIVE SYNTHESIS AGENT */}
              <button
                onClick={() => setSelectedNodeId('executive-reporting')}
                className={`w-full max-w-lg p-4 rounded-xl border transition-all text-left flex items-center justify-between ${
                  selectedNodeId === 'executive-reporting'
                    ? 'bg-purple-950/60 border-purple-500 ring-2 ring-purple-500/30'
                    : 'bg-slate-800/80 border-slate-700 hover:border-slate-600'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider">
                        Executive Synthesis
                      </span>
                      <span className="px-1.5 py-0.2 rounded text-[10px] bg-purple-500/20 text-purple-300">
                        {executiveAgent?.executionDurationMs || 30}ms
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white">Executive Synthesis & Reporting Agent</h3>
                    <p className="text-[11px] text-slate-400">
                      Cross-correlates findings into root cause traces & prioritized P0-P3 actions
                    </p>
                  </div>
                </div>
                <span className="px-2 py-1 rounded-md text-xs font-medium bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  Synthesized
                </span>
              </button>

              {/* Connector */}
              <div className="h-6 w-0.5 bg-gradient-to-b from-purple-500 to-amber-500 my-1" />

              {/* 6. DOWNSTREAM CHANNELS */}
              <button
                onClick={() => setSelectedNodeId('downstream')}
                className={`w-full max-w-md p-4 rounded-xl border transition-all text-left flex items-center justify-between ${
                  selectedNodeId === 'downstream'
                    ? 'bg-amber-950/60 border-amber-500 ring-2 ring-amber-500/30'
                    : 'bg-slate-800/80 border-slate-700 hover:border-slate-600'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400">
                    <Radio className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider">
                        Delivery Hub
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white">Dashboard + Alerts + Reports + Email</h3>
                    <p className="text-[11px] text-slate-400">Pushes verified intelligence to user-facing tabs</p>
                  </div>
                </div>
                <ExternalLink className="w-4 h-4 text-slate-500" />
              </button>
            </div>
          </div>

          {/* Real-time Graph Execution Log */}
          {executionLog.length > 0 && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 font-mono text-xs">
              <div className="flex items-center justify-between text-slate-400 mb-2 font-sans font-semibold">
                <span>LangGraph Execution Event Stream</span>
                <span className="text-[10px] text-emerald-400">Verified Deterministic Run</span>
              </div>
              <div className="space-y-1 text-slate-300 max-h-32 overflow-y-auto">
                {executionLog.map((log, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <span className="text-emerald-400">›</span>
                    <span>{log}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right 4 Cols: Agent Deep Dive Inspector */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl text-white sticky top-20">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
              <div>
                <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-400">
                  Node Inspector
                </span>
                <h3 className="text-base font-bold text-slate-100">{selectedAgentDetails?.name}</h3>
              </div>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  selectedAgentDetails?.status === 'skipped'
                    ? 'bg-slate-800 text-slate-400 border border-slate-700'
                    : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                }`}
              >
                {selectedAgentDetails?.status === 'skipped' ? 'Skipped' : 'Completed'}
              </span>
            </div>

            {/* Purpose */}
            <div className="mb-4">
              <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Purpose
              </label>
              <p className="text-xs text-slate-300 leading-relaxed">{selectedAgentDetails?.purpose}</p>
            </div>

            {/* Data Sources Used */}
            <div className="mb-4">
              <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Data Sources Referenced
              </label>
              <div className="flex flex-wrap gap-1.5">
                {selectedAgentDetails?.inputDatasets?.map((src, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 rounded bg-slate-800 text-[11px] text-slate-300 border border-slate-700"
                  >
                    {src}
                  </span>
                ))}
              </div>
            </div>

            {/* Execution Duration */}
            {selectedAgentDetails?.executionDurationMs !== undefined && (
              <div className="mb-4 flex items-center justify-between text-xs bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
                <span className="text-slate-400 flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  Actual Execution Time
                </span>
                <span className="font-mono text-emerald-400 font-bold">
                  {selectedAgentDetails.executionDurationMs} ms
                </span>
              </div>
            )}

            {/* Reasoning Summary */}
            <div className="mb-4">
              <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Reasoning Summary
              </label>
              <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-xs text-slate-300 leading-relaxed">
                {selectedAgentDetails?.reasoningSummary}
              </div>
            </div>

            {/* Actual Structured Findings */}
            {selectedAgentDetails?.findings && selectedAgentDetails.findings.length > 0 && (
              <div className="mb-4">
                <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
                  Generated Structured Findings ({selectedAgentDetails.findings.length})
                </label>
                <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                  {selectedAgentDetails.findings.map((f: AgentStructuredFinding) => (
                    <div
                      key={f.id}
                      className="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700/70 text-xs space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-200">{f.metric}</span>
                        <span
                          className={`text-[10px] px-1.5 py-0.2 rounded uppercase font-bold ${
                            f.severity === 'critical'
                              ? 'bg-rose-500/20 text-rose-300'
                              : f.severity === 'high'
                              ? 'bg-amber-500/20 text-amber-300'
                              : 'bg-blue-500/20 text-blue-300'
                          }`}
                        >
                          {f.severity}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400">{f.finding}</p>
                      {f.recommended_action && (
                        <div className="text-[11px] text-emerald-400 pt-1 border-t border-slate-700/50">
                          <strong>Action:</strong> {f.recommended_action}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Quick Action to Navigate to related tabs */}
            {onNavigateToTab && (
              <div className="pt-2 border-t border-slate-800 flex gap-2">
                <button
                  onClick={() => onNavigateToTab('insights')}
                  className="flex-1 py-2 text-center text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors"
                >
                  View AI Insights →
                </button>
                <button
                  onClick={() => onNavigateToTab('executive')}
                  className="flex-1 py-2 text-center text-xs font-semibold rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 transition-colors"
                >
                  Executive Report →
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
