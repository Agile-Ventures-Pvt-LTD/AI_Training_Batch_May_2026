import React, { useState, useEffect } from 'react';
import {
  Cpu,
  ShieldCheck,
  DollarSign,
  Layers,
  Zap,
  Package,
  Boxes,
  Truck,
  ShieldAlert,
  Sparkles,
  FileText,
  Activity,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Database,
  Search,
  Sliders,
  ChevronRight,
  Info,
  RefreshCw,
  Play,
  Check,
  Lock,
  Workflow,
  LayoutGrid,
  Network,
} from 'lucide-react';
import { SleepsiaWorkbookData, CalculatedKPIs } from '../types/commerce';
import { AgentExecutionState, RootCauseTrace, OrchestrationPipeline } from '../types/agents';
import { executeMultiAgentGraph } from '../services/agentGraphEngine';
import { getOrchestrationPipeline, getRootCauseTraces } from '../services/multiAgentSupervisor';
import { InteractivePipelineGraph } from './InteractivePipelineGraph';

interface MultiAgentOrchestratorProps {
  data: SleepsiaWorkbookData;
  kpis: CalculatedKPIs;
  selectedDate: string;
  onNavigateToTab?: (tab: string) => void;
  onOpenEmailModal?: () => void;
}

export const MultiAgentOrchestrator: React.FC<MultiAgentOrchestratorProps> = ({
  data,
  kpis,
  selectedDate,
  onNavigateToTab,
  onOpenEmailModal,
}) => {
  const [viewMode, setViewMode] = useState<'graph' | 'matrix'>('graph');
  const [pipeline, setPipeline] = useState<OrchestrationPipeline>(() =>
    getOrchestrationPipeline(data, selectedDate)
  );
  const [rootCauses, setRootCauses] = useState<RootCauseTrace[]>(() =>
    getRootCauseTraces(data, selectedDate)
  );
  const [selectedAgent, setSelectedAgent] = useState<AgentExecutionState | null>(null);
  const [selectedTrace, setSelectedTrace] = useState<RootCauseTrace | null>(null);
  const [activeFilter, setActiveFilter] = useState<
    'all' | 'Validation' | 'Domain Intelligence' | 'Supply Chain' | 'External' | 'Synthesis'
  >('all');
  const [isSimulatingRun, setIsSimulatingRun] = useState<boolean>(false);
  const [activeStepIndex, setActiveStepIndex] = useState<number>(4);

  // Update pipeline when data or date changes
  useEffect(() => {
    setPipeline(getOrchestrationPipeline(data, selectedDate));
    setRootCauses(getRootCauseTraces(data, selectedDate));
  }, [data, selectedDate]);

  const handleRunOrchestration = () => {
    setIsSimulatingRun(true);
    let step = 0;
    const interval = setInterval(() => {
      step += 1;
      setActiveStepIndex(step % 5);
      if (step >= 5) {
        clearInterval(interval);
        setIsSimulatingRun(false);
        setPipeline(getOrchestrationPipeline(data, selectedDate));
      }
    }, 600);
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

  const filteredAgents =
    activeFilter === 'all'
      ? pipeline.agents
      : pipeline.agents.filter((a) => a.category === activeFilter);

  // 5-Stage Orchestration Pipeline
  const pipelineStages = [
    {
      id: 'supervisor',
      name: 'Supervisor Agent',
      subtitle: 'Central Coordinator',
      status: 'Active',
      desc: 'Orchestrator decomposing queries & dispatching datasets',
    },
    {
      id: 'specialists',
      name: 'Specialist Agents',
      subtitle: '8 Domain Analysts',
      status: isSimulatingRun ? 'Processing' : 'Completed',
      desc: 'Sales, Ads, Logistics, Inventory, Competitor models',
    },
    {
      id: 'findings',
      name: 'Correlated Findings',
      subtitle: `${pipeline.totalFindings} Verified Signals`,
      status: 'Synthesized',
      desc: 'Isolating root causation from baseline correlation',
    },
    {
      id: 'recommendations',
      name: 'Recommendations',
      subtitle: 'P0 - P3 Action Directives',
      status: 'Prioritized',
      desc: 'Tactical operational playbooks & budget shifts',
    },
    {
      id: 'executive_summary',
      name: 'Executive Summary',
      subtitle: 'Daily Leadership Brief',
      status: 'Ready',
      desc: 'Executive briefing delivered via dashboard & email',
    },
  ];

  return (
    <div className="space-y-6">
      {/* 1. Supervisor Pipeline Architecture Header */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950 rounded-2xl p-6 text-white shadow-lg border border-slate-700/50">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-slate-700/60">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-xl bg-blue-600/30 border border-blue-400/40 flex items-center justify-center text-blue-400 shadow-inner">
              <Cpu className={`w-6 h-6 ${isSimulatingRun ? 'animate-spin' : 'animate-pulse'}`} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-black tracking-tight">AI Multi-Agent Commerce Operating System</h2>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-black uppercase tracking-wider flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
                  Supervisor Active
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-0.5">
                Autonomous orchestrator coordinating domain-specialist intelligence agents across all 14 commerce channels.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={handleRunOrchestration}
              disabled={isSimulatingRun}
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white px-3.5 py-2 rounded-xl text-xs font-bold transition-all shadow-md active:scale-95"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSimulatingRun ? 'animate-spin' : ''}`} />
              <span>{isSimulatingRun ? 'Running Pipeline...' : 'Re-Run Multi-Agent Cycle'}</span>
            </button>

            <div className="flex items-center gap-3 text-xs bg-slate-800/80 p-2.5 rounded-xl border border-slate-700">
              <div className="text-center px-3 border-r border-slate-700">
                <div className="text-slate-400 text-[10px] uppercase font-bold">Active Agents</div>
                <div className="text-base font-black text-emerald-400">{pipeline.activeAgentsCount} / 8</div>
              </div>
              <div className="text-center px-3 border-r border-slate-700">
                <div className="text-slate-400 text-[10px] uppercase font-bold">Total Findings</div>
                <div className="text-base font-black text-blue-400">{pipeline.totalFindings}</div>
              </div>
              <div className="text-center px-3">
                <div className="text-slate-400 text-[10px] uppercase font-bold">Confidence</div>
                <div className="text-base font-black text-purple-400">
                  {Math.round(pipeline.overallConfidence * 100)}%
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Visual Orchestration Flow: Supervisor -> Specialists -> Findings -> Recommendations -> Executive Summary */}
        <div className="pt-6">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-blue-400" />
              <span>Multi-Agent Orchestration Flow (End-to-End Pipeline)</span>
            </span>
            <span className="text-[10px] text-slate-400">Step {activeStepIndex + 1} of 5</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
            {pipelineStages.map((stage, idx) => {
              const isCurrent = activeStepIndex === idx;
              const isPassed = activeStepIndex > idx;
              return (
                <div
                  key={stage.id}
                  className={`rounded-xl p-3.5 border transition-all relative ${
                    isCurrent
                      ? 'bg-blue-900/60 border-blue-400 shadow-md ring-1 ring-blue-400/50'
                      : isPassed
                      ? 'bg-slate-800/80 border-slate-700 text-slate-300'
                      : 'bg-slate-800/40 border-slate-700/60 opacity-80'
                  }`}
                >
                  <div className="flex items-center justify-between text-[10px] mb-1 font-bold text-slate-400">
                    <span>STAGE {idx + 1}</span>
                    <span
                      className={`px-1.5 py-0.2 rounded text-[9px] font-bold uppercase ${
                        isCurrent
                          ? 'bg-blue-500 text-white'
                          : isPassed
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : 'bg-slate-700 text-slate-400'
                      }`}
                    >
                      {stage.status}
                    </span>
                  </div>
                  <div className="text-xs font-black text-white">{stage.name}</div>
                  <div className="text-[11px] font-semibold text-blue-300 mt-0.5">{stage.subtitle}</div>
                  <p className="text-[10px] text-slate-400 mt-1.5 leading-snug line-clamp-2">{stage.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* View Mode Switcher */}
      <div className="flex items-center justify-between bg-slate-900 p-2 rounded-2xl border border-slate-800 shadow-md">
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => setViewMode('graph')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-xs ${
              viewMode === 'graph'
                ? 'bg-blue-600 text-white shadow-blue-500/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-800'
            }`}
          >
            <Network className="w-4 h-4" />
            <span>Interactive Graphical Workflow Canvas</span>
            <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[9px] px-1.5 py-0.2 rounded-full uppercase font-black">
              Full Pipeline
            </span>
          </button>

          <button
            onClick={() => setViewMode('matrix')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              viewMode === 'matrix'
                ? 'bg-blue-600 text-white shadow-blue-500/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-800'
            }`}
          >
            <LayoutGrid className="w-4 h-4" />
            <span>Specialist Findings Matrix & Root-Cause Chains</span>
          </button>
        </div>

        <div className="hidden md:flex items-center gap-2 text-xs text-slate-400 pr-3">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>Full DAG Orchestration Ready</span>
        </div>
      </div>

      {/* RENDER SELECTED VIEW */}
      {viewMode === 'graph' ? (
        <InteractivePipelineGraph
          data={data}
          kpis={kpis}
          selectedDate={selectedDate}
          onNavigateToTab={onNavigateToTab}
          onOpenEmailModal={onOpenEmailModal}
          onRunLiveAnalysis={handleRunOrchestration}
        />
      ) : (
        <>
          {/* 2. Category Filter & Agents Grid */}
          <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-base font-bold text-slate-900">Domain Specialist Intelligence Agents</h3>
            <p className="text-xs text-slate-500">
              Specialized AI agents evaluating domain datasets, isolating causal drivers, and producing tactical recommendations.
            </p>
          </div>

          <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
            {(['all', 'Validation', 'Domain Intelligence', 'Supply Chain', 'External', 'Synthesis'] as const).map(
              (cat) => (
                <button
                  key={cat}
                  onClick={() => setActiveFilter(cat)}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                    activeFilter === cat
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  {cat === 'all' ? 'All Agents' : cat}
                </button>
              )
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredAgents.map((agent) => {
            const Icon = getAgentIcon(agent.id);
            const isSkipped = agent.status === 'skipped';
            const isCompleted = agent.status === 'completed';

            return (
              <div
                key={agent.id}
                onClick={() => setSelectedAgent(agent)}
                className={`bg-white rounded-xl border p-5 transition-all cursor-pointer flex flex-col justify-between shadow-xs hover:shadow-md ${
                  isSkipped
                    ? 'border-slate-200 bg-slate-50/50 opacity-80'
                    : 'border-slate-200 hover:border-blue-300'
                }`}
              >
                <div>
                  {/* Top Bar */}
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <div className="flex items-center gap-2.5">
                      <div
                        className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                          isSkipped
                            ? 'bg-slate-100 text-slate-400'
                            : 'bg-blue-50 text-blue-600 border border-blue-100'
                        }`}
                      >
                        <Icon className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-slate-900">{agent.name}</h4>
                        <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
                          {agent.category}
                        </span>
                      </div>
                    </div>

                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        isCompleted
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : isSkipped
                          ? 'bg-slate-100 text-slate-500 border border-slate-200'
                          : 'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}
                    >
                      {agent.status}
                    </span>
                  </div>

                  {/* Purpose Statement */}
                  {agent.purpose && (
                    <p className="text-xs text-slate-600 font-medium mb-3 leading-relaxed">
                      {agent.purpose}
                    </p>
                  )}

                  {/* Current Live Activity */}
                  {agent.currentActivity && !isSkipped && (
                    <div className="mb-3 p-2 bg-slate-50 rounded-lg border border-slate-200/80 text-[11px] text-slate-700 flex items-start gap-1.5">
                      <Activity className="w-3.5 h-3.5 text-blue-500 shrink-0 mt-0.5" />
                      <span>
                        <strong className="text-slate-900">Current Activity:</strong> {agent.currentActivity}
                      </span>
                    </div>
                  )}

                  {/* Datasets Used */}
                  <div className="flex flex-wrap gap-1 mb-2.5">
                    {agent.inputDatasets.map((ds) => (
                      <span
                        key={ds}
                        className="text-[9px] font-semibold bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded"
                      >
                        {ds}
                      </span>
                    ))}
                  </div>

                  {/* Key Metric or Reasoning */}
                  {isSkipped ? (
                    <p className="text-xs text-slate-500 italic bg-slate-100/80 p-2.5 rounded-lg border border-slate-200">
                      {agent.skipReason || 'Dataset unavailable. Agent execution skipped.'}
                    </p>
                  ) : (
                    <div className="space-y-2 text-xs">
                      {agent.keyMetricObserved && (
                        <div className="bg-blue-50/60 border border-blue-100 px-2.5 py-1.5 rounded-lg text-blue-900 font-bold">
                          {agent.keyMetricObserved}
                        </div>
                      )}
                      <p className="text-slate-600 line-clamp-2 leading-relaxed">
                        {agent.reasoningSummary}
                      </p>
                    </div>
                  )}
                </div>

                {/* Footer stats */}
                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                  {isSkipped ? (
                    <span className="text-slate-400">Execution Skipped</span>
                  ) : (
                    <>
                      <span>
                        Confidence: <strong className="text-slate-900">{Math.round(agent.confidence * 100)}%</strong>
                      </span>
                      <span>
                        Findings: <strong className="text-blue-600 font-bold">{agent.findingsCount}</strong>
                      </span>
                      <span className="text-blue-600 font-semibold flex items-center gap-0.5">
                        Inspect <ChevronRight className="w-3 h-3" />
                      </span>
                    </>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3. Root Cause Investigation Workspace */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-600" />
              <h3 className="text-base font-bold text-slate-900">Root-Cause Investigation Workspace</h3>
            </div>
            <p className="text-xs text-slate-500">
              Correlated multi-domain signals isolating verified causation from correlation.
            </p>
          </div>
          <span className="text-xs text-slate-400 font-medium">3 Active Causation Traces</span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {rootCauses.map((trace) => (
            <div
              key={trace.id}
              onClick={() => setSelectedTrace(trace)}
              className="bg-slate-50/70 border border-slate-200 rounded-xl p-4.5 hover:bg-white hover:border-purple-300 hover:shadow-xs transition-all cursor-pointer flex flex-col justify-between space-y-3"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                      trace.severity === 'critical'
                        ? 'bg-rose-50 text-rose-700 border border-rose-200'
                        : 'bg-amber-50 text-amber-700 border border-amber-200'
                    }`}
                  >
                    {trace.severity}
                  </span>
                  <span className="text-[10px] font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-100">
                    {trace.verdict.distinction}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-slate-900 leading-snug mb-1">{trace.title}</h4>
                <p className="text-xs text-slate-600 line-clamp-2">{trace.observedSymptom}</p>
              </div>

              <div className="pt-2.5 border-t border-slate-200/80 flex items-center justify-between text-xs">
                <span className="text-slate-500 text-[11px]">{trace.chainOfSignals.length} Signal Stages</span>
                <span className="text-purple-600 font-bold text-[11px] flex items-center gap-1">
                  Inspect Trace <ArrowRight className="w-3 h-3" />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Trace Deep Dive Modal / Drawer */}
      {selectedTrace && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col animate-in fade-in zoom-in-95 duration-200">
            <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-900 text-white">
              <div>
                <span className="text-[10px] font-bold text-purple-400 uppercase tracking-wider">
                  {selectedTrace.category} Investigation
                </span>
                <h3 className="text-sm font-bold text-white">{selectedTrace.title}</h3>
              </div>
              <button
                onClick={() => setSelectedTrace(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-5 flex-1">
              {/* Observed Symptom */}
              <div className="bg-rose-50 border border-rose-100 rounded-xl p-3.5 text-xs">
                <div className="font-bold text-rose-900 mb-0.5">Observed Symptom:</div>
                <div className="text-rose-800">{selectedTrace.observedSymptom}</div>
              </div>

              {/* Signal Chain */}
              <div className="space-y-2.5">
                <div className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Multi-Domain Signal Chain
                </div>
                {selectedTrace.chainOfSignals.map((sig, idx) => (
                  <div key={idx} className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-800">{sig.stage}</span>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          sig.classification === 'Observed Fact'
                            ? 'bg-blue-50 text-blue-700 border border-blue-200'
                            : sig.classification === 'Likely Driver'
                            ? 'bg-purple-50 text-purple-700 border border-purple-200'
                            : sig.classification === 'Excluded Factor'
                            ? 'bg-slate-100 text-slate-600 border border-slate-200'
                            : 'bg-amber-50 text-amber-700 border border-amber-200'
                        }`}
                      >
                        {sig.classification}
                      </span>
                    </div>
                    <p className="text-slate-700">{sig.signal}</p>
                    <div className="text-[10px] text-slate-500 font-mono bg-white p-1.5 rounded border border-slate-100">
                      Evidence: {sig.evidence}
                    </div>
                  </div>
                ))}
              </div>

              {/* Verdict */}
              <div className="bg-purple-50 border border-purple-200 rounded-xl p-4 text-xs space-y-1">
                <div className="flex items-center gap-1.5 text-purple-900 font-bold">
                  <CheckCircle2 className="w-4 h-4 text-purple-600" />
                  <span>Verdict: {selectedTrace.verdict.distinction}</span>
                </div>
                <p className="text-purple-800 leading-relaxed">{selectedTrace.verdict.explanation}</p>
              </div>

              {/* Recommendation */}
              <div className="bg-slate-900 text-white rounded-xl p-4 text-xs space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-400">
                    Action Recommendation ({selectedTrace.recommendedAction.priority})
                  </span>
                  <span className="text-[10px] text-slate-300">
                    Assigned: {selectedTrace.recommendedAction.assignedRole}
                  </span>
                </div>
                <p className="text-slate-200">{selectedTrace.recommendedAction.action}</p>
                <div className="text-[11px] text-emerald-300 pt-1 border-t border-slate-800">
                  Expected Impact: {selectedTrace.recommendedAction.expectedImpact}
                </div>
              </div>
            </div>

            <div className="px-6 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-end">
              <button
                onClick={() => setSelectedTrace(null)}
                className="px-4 py-2 bg-slate-900 text-white rounded-lg text-xs font-bold hover:bg-slate-800"
              >
                Close Trace
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Agent Detail Modal */}
      {selectedAgent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-xl max-h-[90vh] overflow-hidden flex flex-col animate-in fade-in zoom-in-95 duration-200">
            <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-900 text-white">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-blue-600/30 flex items-center justify-center text-blue-400">
                  <Cpu className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold">{selectedAgent.name}</h3>
                  <span className="text-[10px] text-slate-300 uppercase">{selectedAgent.category} Agent</span>
                </div>
              </div>
              <button
                onClick={() => setSelectedAgent(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-4 text-xs flex-1">
              {selectedAgent.purpose && (
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-slate-500 font-bold uppercase text-[10px] block">Agent Purpose &amp; Scope:</span>
                  <p className="text-slate-800 mt-1 leading-relaxed font-medium">{selectedAgent.purpose}</p>
                </div>
              )}

              {selectedAgent.currentActivity && (
                <div className="bg-blue-50/50 p-3 rounded-xl border border-blue-100 text-blue-900">
                  <span className="text-blue-700 font-bold uppercase text-[10px] block">Live Operational Activity:</span>
                  <p className="mt-0.5">{selectedAgent.currentActivity}</p>
                </div>
              )}

              <div>
                <span className="text-slate-400 font-bold uppercase text-[10px]">Reasoning Summary:</span>
                <p className="text-slate-800 mt-1 leading-relaxed">{selectedAgent.reasoningSummary}</p>
              </div>

              {selectedAgent.topFinding && (
                <div className="bg-blue-50 border border-blue-100 rounded-xl p-3.5">
                  <span className="text-blue-900 font-bold text-[11px]">Key Finding:</span>
                  <p className="text-blue-800 mt-0.5">{selectedAgent.topFinding}</p>
                </div>
              )}

              {selectedAgent.topRecommendation && (
                <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-3.5">
                  <span className="text-emerald-900 font-bold text-[11px]">Recommended Strategy:</span>
                  <p className="text-emerald-800 mt-0.5">{selectedAgent.topRecommendation}</p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-2 text-[11px] pt-2 border-t border-slate-100">
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <span className="text-slate-500">Confidence Score</span>
                  <div className="text-sm font-bold text-slate-900">{Math.round(selectedAgent.confidence * 100)}%</div>
                </div>
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <span className="text-slate-500">Execution Duration</span>
                  <div className="text-sm font-bold text-slate-900">{selectedAgent.executionDurationMs || 0} ms</div>
                </div>
              </div>
            </div>

            <div className="px-6 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-end">
              <button
                onClick={() => setSelectedAgent(null)}
                className="px-4 py-2 bg-slate-900 text-white rounded-lg text-xs font-bold hover:bg-slate-800"
              >
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}
        </>
      )}
    </div>
  );
};

export default MultiAgentOrchestrator;
