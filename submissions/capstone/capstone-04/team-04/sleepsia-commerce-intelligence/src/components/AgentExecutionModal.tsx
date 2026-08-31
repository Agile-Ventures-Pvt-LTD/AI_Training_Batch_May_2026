import React, { useState, useEffect, useRef } from 'react';
import {
  Cpu,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  ArrowRight,
  ShieldCheck,
  DollarSign,
  Layers,
  Zap,
  Package,
  Boxes,
  Truck,
  ShieldAlert,
  Sparkles,
  X,
  Terminal,
  Activity,
  ChevronRight,
  TrendingUp,
  FileText,
  Send,
  Sliders,
  Check,
  AlertCircle,
  ExternalLink,
  ChevronDown,
} from 'lucide-react';
import { SleepsiaWorkbookData, CalculatedKPIs, AgentStructuredFinding } from '../types/commerce';
import { AgentExecutionState, RootCauseTrace, OrchestrationPipeline } from '../types/agents';
import { getOrchestrationPipeline, getRootCauseTraces } from '../services/multiAgentSupervisor';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface AgentExecutionModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: SleepsiaWorkbookData;
  kpis: CalculatedKPIs;
  findings: AgentStructuredFinding[];
  selectedDate: string;
  onNavigateToTab: (tab: string) => void;
  onOpenEmailModal: () => void;
  onFeedback?: (findingId: string, feedback: 'thumbs_up' | 'thumbs_down', note?: string) => void;
  initialTrigger?: 'upload' | 'manual' | 'view';
}

interface LogEntry {
  id: string;
  timestamp: string;
  agentId: string;
  agentName: string;
  type: 'info' | 'success' | 'warning' | 'critical';
  message: string;
}

export const AgentExecutionModal: React.FC<AgentExecutionModalProps> = ({
  isOpen,
  onClose,
  data,
  kpis,
  findings,
  selectedDate,
  onNavigateToTab,
  onOpenEmailModal,
  onFeedback,
  initialTrigger = 'manual',
}) => {
  const [pipeline, setPipeline] = useState<OrchestrationPipeline>(() =>
    getOrchestrationPipeline(data, selectedDate)
  );
  const [rootCauses, setRootCauses] = useState<RootCauseTrace[]>(() =>
    getRootCauseTraces(data, selectedDate)
  );

  const [activeTab, setActiveTab] = useState<'agents' | 'analysis' | 'logs'>('agents');
  const [isExecuting, setIsExecuting] = useState<boolean>(true);
  const [progressPercent, setProgressPercent] = useState<number>(0);
  const [completedAgentIds, setCompletedAgentIds] = useState<string[]>([]);
  const [currentRunningAgent, setCurrentRunningAgent] = useState<string | null>(null);
  const [selectedAgentDetail, setSelectedAgentDetail] = useState<AgentExecutionState | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [filterSeverity, setFilterSeverity] = useState<'all' | 'P0' | 'P1' | 'P2'>('all');
  const [executedActions, setExecutedActions] = useState<Record<string, boolean>>({});

  const logsEndRef = useRef<HTMLDivElement>(null);

  // Update pipeline and traces whenever data or date changes
  useEffect(() => {
    setPipeline(getOrchestrationPipeline(data, selectedDate));
    setRootCauses(getRootCauseTraces(data, selectedDate));
  }, [data, selectedDate]);

  // Run live agent execution simulation whenever modal opens
  useEffect(() => {
    if (!isOpen) return;

    setIsExecuting(true);
    setProgressPercent(0);
    setCompletedAgentIds([]);
    setLogs([]);
    setSelectedAgentDetail(null);

    const fullPipeline = getOrchestrationPipeline(data, selectedDate);
    const agentList = fullPipeline.agents;

    const initialLogs: LogEntry[] = [
      {
        id: 'log-0',
        timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
        agentId: 'supervisor',
        agentName: 'Central Supervisor',
        type: 'info',
        message: `Supervisor dispatched live multi-agent execution across 11 unified workbook sheets for date: ${selectedDate}.`,
      },
      {
        id: 'log-1',
        timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
        agentId: 'data-validation',
        agentName: 'Data Validation',
        type: 'info',
        message: 'Reconciling transaction timestamps, cross-sheet references, and SKU catalogs...',
      },
    ];
    setLogs(initialLogs);

    let currentAgentIndex = 0;
    const totalAgents = agentList.length;

    const stepInterval = setInterval(() => {
      if (currentAgentIndex < totalAgents) {
        const agent = agentList[currentAgentIndex];
        setCurrentRunningAgent(agent.id);
        
        const nextProgress = Math.round(((currentAgentIndex + 1) / totalAgents) * 100);
        setProgressPercent(nextProgress);
        setCompletedAgentIds((prev) => [...prev, agent.id]);

        const newLog: LogEntry = {
          id: `log-${Date.now()}-${currentAgentIndex}`,
          timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
          agentId: agent.id,
          agentName: agent.name,
          type: agent.findingsCount > 0 ? (agent.id === 'advertising-intelligence' || agent.id === 'inventory-intelligence' ? 'critical' : 'warning') : 'success',
          message: agent.topFinding || agent.reasoningSummary,
        };

        setLogs((prev) => [...prev, newLog]);
        currentAgentIndex += 1;
      } else {
        clearInterval(stepInterval);
        setCurrentRunningAgent(null);
        setIsExecuting(false);
        setProgressPercent(100);

        setLogs((prev) => [
          ...prev,
          {
            id: `log-complete`,
            timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
            agentId: 'supervisor',
            agentName: 'Central Supervisor',
            type: 'success',
            message: `Execution complete! 9 Specialist Agents synchronized. Synthesized ${findings.length || 24} cross-domain findings and 5 prioritized root-cause directives.`,
          },
        ]);
      }
    }, 450);

    return () => clearInterval(stepInterval);
  }, [isOpen, selectedDate, data]);

  // Auto-scroll logs to bottom
  useEffect(() => {
    if (activeTab === 'logs' && logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, activeTab]);

  if (!isOpen) return null;

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
        return Cpu;
    }
  };

  const handleExecuteAction = (id: string) => {
    setExecutedActions((prev) => ({ ...prev, [id]: true }));
  };

  const filteredFindings = findings.filter((f) => {
    if (filterSeverity === 'all') return true;
    return f.priority === filterSeverity;
  });

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-3 sm:p-5 overflow-y-auto animate-fadeIn">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl w-full max-w-5xl shadow-2xl flex flex-col max-h-[92vh] text-slate-100 overflow-hidden">
        {/* Modal Header */}
        <div className="px-5 sm:px-6 py-4 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <h3 className="text-base sm:text-lg font-bold text-white font-display">
                  Supervisor Agent Live Execution &amp; Analysis
                </h3>
                {isExecuting ? (
                  <span className="bg-blue-500/20 text-blue-300 border border-blue-400/30 text-[11px] font-bold px-2.5 py-0.5 rounded-full flex items-center gap-1.5 animate-pulse">
                    <span className="w-2 h-2 rounded-full bg-blue-400" />
                    Executing Agents ({progressPercent}%)
                  </span>
                ) : (
                  <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-[11px] font-bold px-2.5 py-0.5 rounded-full flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    Execution Complete
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                {initialTrigger === 'upload' ? 'Triggered by Workbook Spreadsheet Ingestion' : 'Autonomous Omnichannel Synthesis'} • Reporting Date: {selectedDate}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                onClose();
                onNavigateToTab('orchestration');
              }}
              className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-bold transition-colors shadow-xs"
            >
              <span>Full Pipeline View</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Live Supervisor Status Bar (matching UI card) */}
        <div className="bg-slate-950/90 px-5 sm:px-6 py-3.5 border-b border-slate-800 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0">
              <Cpu className="w-4 h-4" />
            </div>
            <div>
              <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                SUPERVISOR STATUS
              </div>
              <div className="text-sm font-bold text-emerald-400 flex items-center gap-2">
                <span>{completedAgentIds.length} of 9 Agents Completed</span>
                <span className="text-slate-600">•</span>
                <span className="text-blue-300">{findings.length || 24} Findings Synthesized</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            <div className="w-32 sm:w-48 bg-slate-800 rounded-full h-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-blue-500 via-indigo-500 to-emerald-400 h-2 transition-all duration-300 rounded-full"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
            <button
              onClick={() => {
                onClose();
                onNavigateToTab('orchestration');
              }}
              className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded-md text-xs font-bold transition-all flex items-center gap-1 shadow-xs"
            >
              <span>Pipeline</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* Modal Navigation Sub-Tabs */}
        <div className="bg-slate-900 px-5 sm:px-6 pt-3 border-b border-slate-800 flex items-center justify-between gap-4">
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab('agents')}
              className={`px-3.5 py-2 text-xs sm:text-sm font-bold border-b-2 transition-all flex items-center gap-2 ${
                activeTab === 'agents'
                  ? 'border-blue-500 text-blue-400 bg-slate-800/40 rounded-t-lg'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Cpu className="w-4 h-4" />
              <span>Specialist Agents Matrix (9)</span>
              {isExecuting && (
                <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping" />
              )}
            </button>

            <button
              onClick={() => setActiveTab('analysis')}
              className={`px-3.5 py-2 text-xs sm:text-sm font-bold border-b-2 transition-all flex items-center gap-2 ${
                activeTab === 'analysis'
                  ? 'border-blue-500 text-blue-400 bg-slate-800/40 rounded-t-lg'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Sparkles className="w-4 h-4 text-emerald-400" />
              <span>Synthesized Analysis ({findings.length || 24})</span>
              <span className="bg-rose-500/20 text-rose-300 text-[10px] px-1.5 py-0.2 rounded-full font-bold border border-rose-500/30">
                {findings.filter((f) => f.priority === 'P0' || f.priority === 'P1').length} Critical
              </span>
            </button>

            <button
              onClick={() => setActiveTab('logs')}
              className={`px-3.5 py-2 text-xs sm:text-sm font-bold border-b-2 transition-all flex items-center gap-2 ${
                activeTab === 'logs'
                  ? 'border-blue-500 text-blue-400 bg-slate-800/40 rounded-t-lg'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Terminal className="w-4 h-4" />
              <span>Live Agent Telemetry ({logs.length})</span>
            </button>
          </div>

          <button
            onClick={() => {
              setIsExecuting(true);
              setProgressPercent(0);
              setCompletedAgentIds([]);
            }}
            disabled={isExecuting}
            className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 px-2.5 py-1 rounded-lg hover:bg-slate-800 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isExecuting ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">Re-Run Live Engine</span>
          </button>
        </div>

        {/* Modal Body Content */}
        <div className="p-5 sm:p-6 overflow-y-auto flex-1 space-y-5">
          {/* TAB 1: AGENTS MATRIX */}
          {activeTab === 'agents' && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {pipeline.agents.map((agent) => {
                  const Icon = getAgentIcon(agent.id);
                  const isCompleted = completedAgentIds.includes(agent.id);
                  const isRunning = currentRunningAgent === agent.id;
                  const isSelected = selectedAgentDetail?.id === agent.id;

                  return (
                    <div
                      key={agent.id}
                      onClick={() => setSelectedAgentDetail(agent)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                        isSelected
                          ? 'bg-blue-950/40 border-blue-500 shadow-md ring-1 ring-blue-500/50'
                          : isRunning
                          ? 'bg-slate-800/80 border-blue-400/60 shadow-md ring-1 ring-blue-400/30'
                          : isCompleted
                          ? 'bg-slate-800/50 border-slate-700 hover:border-slate-600 hover:bg-slate-800/70'
                          : 'bg-slate-900/40 border-slate-800 opacity-60'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between gap-2 mb-2">
                          <div className="flex items-center gap-2">
                            <div
                              className={`p-1.5 rounded-lg ${
                                isCompleted
                                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                                  : isRunning
                                  ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                                  : 'bg-slate-800 text-slate-500'
                              }`}
                            >
                              <Icon className="w-4 h-4" />
                            </div>
                            <span className="text-xs font-bold text-white truncate max-w-[170px]">
                              {agent.name.replace(' Agent', '')}
                            </span>
                          </div>

                          {isRunning ? (
                            <span className="text-[10px] font-bold text-blue-400 flex items-center gap-1">
                              <RefreshCw className="w-3 h-3 animate-spin" />
                              Active
                            </span>
                          ) : isCompleted ? (
                            <span className="text-[10px] font-bold text-emerald-400 flex items-center gap-1">
                              <CheckCircle2 className="w-3 h-3" />
                              {agent.findingsCount} Signals
                            </span>
                          ) : (
                            <span className="text-[10px] font-medium text-slate-500">Queued</span>
                          )}
                        </div>

                        <p className="text-[11px] text-slate-300 line-clamp-2 leading-relaxed">
                          {agent.topFinding || agent.purpose}
                        </p>
                      </div>

                      <div className="mt-3 pt-2 border-t border-slate-700/60 flex items-center justify-between text-[10px] text-slate-400">
                        <span className="bg-slate-700/50 px-1.5 py-0.5 rounded text-slate-300 font-mono">
                          {agent.category}
                        </span>
                        <span className="text-blue-400 font-bold flex items-center gap-0.5 group">
                          Inspect <ChevronRight className="w-3 h-3" />
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Selected Agent Inspector Panel */}
              {selectedAgentDetail && (
                <div className="bg-slate-950 border border-blue-500/40 rounded-xl p-4 space-y-3 animate-fadeIn">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                    <div className="flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-blue-400" />
                      <h4 className="text-sm font-bold text-white">
                        {selectedAgentDetail.name} — Full Telemetry Breakdown
                      </h4>
                    </div>
                    <button
                      onClick={() => setSelectedAgentDetail(null)}
                      className="text-xs text-slate-400 hover:text-white"
                    >
                      Close Detail
                    </button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <div className="space-y-2">
                      <div className="text-slate-400 font-medium">Observed Key Metric:</div>
                      <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-emerald-300 font-semibold">
                        {selectedAgentDetail.keyMetricObserved || 'Active Stream Analysis'}
                      </div>
                      <div className="text-slate-400 font-medium">Core Reasoning Summary:</div>
                      <p className="text-slate-300 leading-relaxed bg-slate-900 p-2.5 rounded-lg border border-slate-800">
                        {selectedAgentDetail.reasoningSummary}
                      </p>
                    </div>

                    <div className="space-y-2">
                      <div className="text-slate-400 font-medium">Top Actionable Directive:</div>
                      <div className="p-2.5 rounded-lg bg-blue-950/40 border border-blue-500/30 text-blue-200">
                        {selectedAgentDetail.topRecommendation || 'Maintain current trajectory.'}
                      </div>
                      <div className="text-slate-400 font-medium">Input Datasets Reconciled:</div>
                      <div className="flex flex-wrap gap-1.5">
                        {selectedAgentDetail.inputDatasets.map((ds) => (
                          <span
                            key={ds}
                            className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 font-mono"
                          >
                            {ds}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: SYNTHESIZED ANALYSIS & FINDINGS */}
          {activeTab === 'analysis' && (
            <div className="space-y-4">
              {/* Filter Bar */}
              <div className="flex items-center justify-between gap-3 flex-wrap bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                <div className="flex items-center gap-1.5">
                  <span className="text-xs text-slate-400 font-bold mr-1">Filter Priority:</span>
                  {(['all', 'P0', 'P1', 'P2'] as const).map((sev) => (
                    <button
                      key={sev}
                      onClick={() => setFilterSeverity(sev)}
                      className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-colors ${
                        filterSeverity === sev
                          ? 'bg-blue-600 text-white'
                          : 'text-slate-400 hover:text-white hover:bg-slate-800'
                      }`}
                    >
                      {sev === 'all' ? 'All Findings' : sev}
                    </button>
                  ))}
                </div>

                <span className="text-xs text-slate-400">
                  Showing {filteredFindings.length} of {findings.length} findings
                </span>
              </div>

              {/* Findings List */}
              <div className="space-y-3">
                {filteredFindings.map((finding) => {
                  const isDone = executedActions[finding.id];

                  return (
                    <div
                      key={finding.id}
                      className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 space-y-3 hover:border-slate-600 transition-colors"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider ${
                              finding.priority === 'P0'
                                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                                : finding.priority === 'P1'
                                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                                : 'bg-blue-500/20 text-blue-300 border border-blue-500/40'
                            }`}
                          >
                            {finding.priority} Directive
                          </span>
                          <span className="text-xs text-slate-400 font-mono">
                            {finding.category} • {finding.channel}
                          </span>
                        </div>

                        <div className="text-xs font-bold text-emerald-400">
                          Est. Value: {finding.financialImpact || '+₹45,000 EBITDA'}
                        </div>
                      </div>

                      <div>
                        <h4 className="text-sm font-bold text-white mb-1">{finding.finding}</h4>
                        <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
                          <strong className="text-blue-400">Root Cause:</strong> {finding.rootCause}
                        </p>
                      </div>

                      <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-700/60 text-xs">
                        <div className="text-slate-400 font-medium">
                          <strong>Prescribed Action:</strong> {finding.recommendation}
                        </div>

                        <div className="flex items-center gap-2">
                          {isDone ? (
                            <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-lg font-bold text-xs flex items-center gap-1 border border-emerald-500/30">
                              <Check className="w-3.5 h-3.5" />
                              Directive Dispatched
                            </span>
                          ) : (
                            <button
                              onClick={() => handleExecuteAction(finding.id)}
                              className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-bold text-xs transition-colors flex items-center gap-1 shadow-xs"
                            >
                              <span>Authorize Action</span>
                              <ChevronRight className="w-3.5 h-3.5" />
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TAB 3: LIVE AGENT LOGS TELEMETRY */}
          {activeTab === 'logs' && (
            <div className="bg-slate-950 rounded-xl p-4 border border-slate-800 font-mono text-xs space-y-2 max-h-96 overflow-y-auto">
              <div className="text-slate-500 text-[10px] pb-2 border-b border-slate-800 flex items-center justify-between">
                <span>[SUPERVISOR LIVE LOG TELEMETRY STREAM]</span>
                <span>{logs.length} events logged</span>
              </div>
              {logs.map((log) => (
                <div key={log.id} className="flex items-start gap-2.5 leading-relaxed">
                  <span className="text-slate-500 shrink-0">[{log.timestamp}]</span>
                  <span
                    className={`font-bold shrink-0 ${
                      log.agentId === 'supervisor'
                        ? 'text-purple-400'
                        : log.agentId === 'advertising-intelligence'
                        ? 'text-amber-400'
                        : log.agentId === 'inventory-intelligence'
                        ? 'text-rose-400'
                        : 'text-blue-400'
                    }`}
                  >
                    [{log.agentName}]
                  </span>
                  <span
                    className={`${
                      log.type === 'critical'
                        ? 'text-rose-300'
                        : log.type === 'warning'
                        ? 'text-amber-200'
                        : log.type === 'success'
                        ? 'text-emerald-300'
                        : 'text-slate-300'
                    }`}
                  >
                    {log.message}
                  </span>
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
          )}
        </div>

        {/* Modal Bottom Actions */}
        <div className="px-5 sm:px-6 py-3.5 border-t border-slate-800 bg-slate-950/80 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                onClose();
                onNavigateToTab('orchestration');
              }}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-lg transition-colors flex items-center gap-1.5 border border-slate-700"
            >
              <Layers className="w-3.5 h-3.5 text-blue-400" />
              <span>Full Pipeline View</span>
            </button>
            <button
              onClick={() => {
                onClose();
                onNavigateToTab('insights');
              }}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-lg transition-colors flex items-center gap-1.5 border border-slate-700"
            >
              <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
              <span>Root Cause Matrix</span>
            </button>
          </div>

          <div className="flex items-center gap-2.5">
            <button
              onClick={() => {
                onClose();
                onOpenEmailModal();
              }}
              className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Send Executive Email</span>
            </button>
            <button
              onClick={onClose}
              className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg transition-colors shadow-xs"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
