/**
 * Agent Logic & Analysis Specification View (Admin)
 * Dynamic transparency portal displaying deterministic formulas, anomaly thresholds, and execution graphs
 * directly sourced from the specialist agent specifications.
 */

import React, { useState, useMemo } from 'react';
import {
  Code2,
  Calculator,
  AlertTriangle,
  GitBranch,
  Shield,
  Layers,
  Search,
  Filter,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Database,
  Users,
  Sliders,
  Download,
  Copy,
  Check,
  Zap,
  TrendingUp,
  Boxes,
  Truck,
  DollarSign,
  Package,
  ShieldAlert,
  Sparkles,
  ExternalLink,
} from 'lucide-react';
import { ALL_SPECIALIST_SPECS } from '../specialistAgents/supervisorAgent';
import { SpecialistAgentSpec, DeterministicFormulaSpec, AnomalyThresholdSpec } from '../types/agentLogic';
import { SleepsiaWorkbookData, CalculatedKPIs } from '../types/commerce';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface AgentLogicAnalysisViewProps {
  dataset: SleepsiaWorkbookData;
  kpis: CalculatedKPIs;
  selectedDate: string;
}

const CATEGORY_ICONS: Record<string, any> = {
  'Domain Intelligence': TrendingUp,
  'Supply Chain': Boxes,
  'External': ShieldAlert,
  'Synthesis': Sparkles,
  'Validation': Shield,
  'Routing': GitBranch,
};

const AGENT_ICONS: Record<string, any> = {
  'sales-intelligence': DollarSign,
  'marketplace-channel': Layers,
  'advertising-intelligence': Zap,
  'product-intelligence': Package,
  'inventory-risk': Boxes,
  'logistics-fulfillment': Truck,
  'competitor-intelligence': ShieldAlert,
  'executive-reporting': Sparkles,
  'data-validation': Shield,
  'supervisor-orchestrator': GitBranch,
};

export function AgentLogicAnalysisView({
  dataset,
  kpis,
  selectedDate,
}: AgentLogicAnalysisViewProps) {
  const [selectedAgentId, setSelectedAgentId] = useState<string>(ALL_SPECIALIST_SPECS[0].id);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [showPromptModal, setShowPromptModal] = useState<boolean>(false);

  const categories = useMemo(() => {
    const cats = Array.from(new Set(ALL_SPECIALIST_SPECS.map((s) => s.category)));
    return ['All', ...cats];
  }, []);

  const filteredAgents = useMemo(() => {
    return ALL_SPECIALIST_SPECS.filter((agent) => {
      const matchesCategory = selectedCategory === 'All' || agent.category === selectedCategory;
      const query = searchQuery.toLowerCase();
      const matchesSearch =
        agent.name.toLowerCase().includes(query) ||
        agent.role.toLowerCase().includes(query) ||
        agent.purpose.toLowerCase().includes(query) ||
        agent.metricsUsed.some((m) => m.toLowerCase().includes(query)) ||
        agent.deterministicFormulas.some((f) => f.name.toLowerCase().includes(query) || f.formula.toLowerCase().includes(query));

      return matchesCategory && matchesSearch;
    });
  }, [selectedCategory, searchQuery]);

  const activeAgent = useMemo(() => {
    return (
      ALL_SPECIALIST_SPECS.find((a) => a.id === selectedAgentId) ||
      filteredAgents[0] ||
      ALL_SPECIALIST_SPECS[0]
    );
  }, [selectedAgentId, filteredAgents]);

  const handleCopy = (text: string, code: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(code);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const handleExportSpecs = () => {
    const dataStr = JSON.stringify(ALL_SPECIALIST_SPECS, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `sleepsia-agent-logic-specs-${selectedDate}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner / Breadcrumb */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <Shield className="w-4 h-4" />
            <span>Admin Governance & Architecture Hub</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight">Agent Analysis Logic & Formulas</h1>
          <p className="text-sm text-slate-300 mt-1 max-w-2xl">
            Live technical specification of all {ALL_SPECIALIST_SPECS.length} autonomous specialist agents. Inspect deterministic formulas, anomaly thresholds, and execution graphs driving commercial decisions.
          </p>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <button
            onClick={handleExportSpecs}
            className="flex items-center gap-2 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold border border-slate-700 transition"
            title="Download JSON specifications"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Specs (JSON)</span>
          </button>
          <div className="px-3.5 py-2 bg-indigo-950/80 border border-indigo-500/30 rounded-xl text-xs font-semibold text-indigo-300 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-indigo-400" />
            <span>100% Deterministic Guardrails</span>
          </div>
        </div>
      </div>

      {/* Main Grid: Sidebar Navigator + Detail Specification Canvas */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Agent Selector Sidebar */}
        <div className="lg:col-span-4 space-y-4">
          {/* Search & Category Filter */}
          <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm space-y-3">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="Search formulas, metrics, agents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-indigo-500 outline-none"
              />
            </div>

            {/* Category Pills */}
            <div className="flex flex-wrap gap-1.5">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-2.5 py-1 rounded-lg text-xs font-medium transition ${
                    selectedCategory === cat
                      ? 'bg-indigo-600 text-white shadow-sm'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          {/* Specialist Agent List */}
          <div className="bg-white rounded-2xl p-2 border border-slate-200 shadow-sm space-y-1.5 max-h-[720px] overflow-y-auto">
            {filteredAgents.map((agent) => {
              const isSelected = agent.id === activeAgent.id;
              const AgentIcon = AGENT_ICONS[agent.id] || Zap;

              return (
                <button
                  key={agent.id}
                  onClick={() => setSelectedAgentId(agent.id)}
                  className={`w-full text-left p-3 rounded-xl transition flex items-start gap-3 border ${
                    isSelected
                      ? 'bg-indigo-50/70 border-indigo-200 text-indigo-950 shadow-sm'
                      : 'bg-white border-transparent hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5 ${
                      isSelected ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600'
                    }`}
                  >
                    <AgentIcon className="w-4 h-4" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-1">
                      <span className="text-xs font-bold truncate">{agent.name}</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-500 font-mono">
                        {agent.deterministicFormulas.length} formulas
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">{agent.role}</p>
                    <div className="flex items-center gap-2 mt-1.5">
                      <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-100 text-slate-600 font-medium">
                        {agent.category}
                      </span>
                      <span className="text-[10px] text-slate-400">
                        {agent.thresholds.length} threshold alerts
                      </span>
                    </div>
                  </div>
                </button>
              );
            })}

            {filteredAgents.length === 0 && (
              <div className="p-6 text-center text-xs text-slate-400">
                No agents match the current filter criteria.
              </div>
            )}
          </div>
        </div>

        {/* Right Active Agent Detail Specs */}
        <div className="lg:col-span-8 space-y-6">
          {activeAgent && (
            <>
              {/* Agent Overview Header */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
                  <div className="flex items-center gap-3">
                    <div className="w-11 h-11 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-md">
                      {React.createElement(AGENT_ICONS[activeAgent.id] || Zap, { className: 'w-6 h-6' })}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h2 className="text-lg font-bold text-slate-900">{activeAgent.name}</h2>
                        <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 font-medium">
                          {activeAgent.category}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 mt-0.5">{activeAgent.role}</p>
                    </div>
                  </div>

                  <button
                    onClick={() => setShowPromptModal(true)}
                    className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition"
                  >
                    <Code2 className="w-3.5 h-3.5" />
                    <span>View System Prompt</span>
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1">
                    <span className="font-semibold text-slate-700 flex items-center gap-1.5">
                      <TargetIcon className="w-3.5 h-3.5 text-indigo-600" />
                      Primary Objective
                    </span>
                    <p className="text-slate-600 text-[11px] leading-relaxed">{activeAgent.primaryObjective}</p>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1">
                    <span className="font-semibold text-slate-700 flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5 text-indigo-600" />
                      Target Stakeholders
                    </span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {activeAgent.targetRoleStakeholders.map((role) => (
                        <span key={role} className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-[10px] text-slate-600">
                          {role}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Data Sources & Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-2">
                  <div>
                    <span className="font-semibold text-slate-700 flex items-center gap-1.5 mb-2">
                      <Database className="w-3.5 h-3.5 text-indigo-600" />
                      Data Sources Ingested
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {activeAgent.dataSourcesUsed.map((ds) => (
                        <span key={ds} className="px-2 py-1 bg-indigo-50/70 border border-indigo-100 text-indigo-700 rounded-lg text-[11px] font-mono">
                          {ds}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <span className="font-semibold text-slate-700 flex items-center gap-1.5 mb-2">
                      <Sliders className="w-3.5 h-3.5 text-indigo-600" />
                      Key Core Metrics
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {activeAgent.metricsUsed.map((metric) => (
                        <span key={metric} className="px-2 py-1 bg-slate-100 border border-slate-200 text-slate-700 rounded-lg text-[11px]">
                          {metric}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Section 1: Deterministic Formulas */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <Calculator className="w-4 h-4 text-indigo-600" />
                    <h3 className="text-sm font-bold text-slate-900">Deterministic Mathematical Formulas</h3>
                  </div>
                  <span className="text-xs text-slate-400 font-mono">
                    {activeAgent.deterministicFormulas.length} formulas defined
                  </span>
                </div>

                <div className="space-y-4">
                  {activeAgent.deterministicFormulas.map((f) => (
                    <div key={f.code} className="p-4 bg-slate-50/80 rounded-xl border border-slate-200 space-y-3">
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-slate-900">{f.name}</span>
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-100 text-indigo-700 font-mono font-semibold">
                              {f.code}
                            </span>
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-200 text-slate-600 font-mono">
                              Unit: {f.unit}
                            </span>
                          </div>
                          <p className="text-xs text-slate-600 mt-1">{f.description}</p>
                        </div>

                        <button
                          onClick={() => handleCopy(f.formula, f.code)}
                          className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-200 rounded-lg transition"
                          title="Copy formula text"
                        >
                          {copiedCode === f.code ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                        </button>
                      </div>

                      {/* Formula Code Box */}
                      <div className="p-2.5 bg-slate-900 rounded-lg text-emerald-400 font-mono text-xs overflow-x-auto shadow-inner">
                        <code>{f.formula}</code>
                      </div>

                      {/* Math Expression & Example */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs pt-1">
                        {f.mathExpression && (
                          <div className="p-2 bg-white rounded-lg border border-slate-200">
                            <span className="text-[10px] text-slate-400 block font-mono">Math Notation:</span>
                            <span className="font-mono text-slate-800 text-[11px]">{f.mathExpression}</span>
                          </div>
                        )}
                        {f.exampleCalculation && (
                          <div className="p-2 bg-white rounded-lg border border-slate-200">
                            <span className="text-[10px] text-slate-400 block font-mono">Example Value:</span>
                            <span className="text-slate-700 text-[11px]">{f.exampleCalculation}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Section 2: Anomaly Thresholds & Trigger Rules */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    <h3 className="text-sm font-bold text-slate-900">Anomaly Detection Thresholds</h3>
                  </div>
                  <span className="text-xs text-slate-400 font-mono">
                    {activeAgent.thresholds.length} rules active
                  </span>
                </div>

                <div className="space-y-3">
                  {activeAgent.thresholds.map((t, idx) => (
                    <div key={idx} className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2.5">
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-slate-900">{t.metric}</span>
                          <span
                            className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                              t.severity === 'critical'
                                ? 'bg-red-100 text-red-700 border border-red-200'
                                : t.severity === 'high'
                                ? 'bg-amber-100 text-amber-700 border border-amber-200'
                                : 'bg-blue-100 text-blue-700 border border-blue-200'
                            }`}
                          >
                            {t.severity} Severity
                          </span>
                        </div>
                      </div>

                      {/* Threshold Tiers */}
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div className="p-2 bg-emerald-50 border border-emerald-200 rounded-lg">
                          <span className="text-[10px] text-emerald-600 block font-semibold">Healthy Range</span>
                          <span className="font-bold text-emerald-800 text-xs">{t.healthyRange}</span>
                        </div>
                        <div className="p-2 bg-amber-50 border border-amber-200 rounded-lg">
                          <span className="text-[10px] text-amber-600 block font-semibold">Warning Trigger</span>
                          <span className="font-bold text-amber-800 text-xs">{t.warningThreshold}</span>
                        </div>
                        <div className="p-2 bg-red-50 border border-red-200 rounded-lg">
                          <span className="text-[10px] text-red-600 block font-semibold">Critical Trigger</span>
                          <span className="font-bold text-red-800 text-xs">{t.criticalThreshold}</span>
                        </div>
                      </div>

                      {/* Condition & Action */}
                      <div className="text-xs space-y-1.5 pt-1">
                        <div className="flex items-start gap-1.5">
                          <span className="text-slate-500 font-semibold shrink-0">Trigger:</span>
                          <span className="text-slate-700">{t.triggerCondition}</span>
                        </div>
                        <div className="flex items-start gap-1.5">
                          <span className="text-indigo-600 font-semibold shrink-0">Required Action:</span>
                          <span className="text-slate-800">{t.actionRequired}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Section 3: 4-Step Execution Flow */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <GitBranch className="w-4 h-4 text-indigo-600" />
                    <h3 className="text-sm font-bold text-slate-900">4-Step Execution Graph</h3>
                  </div>
                  <span className="text-xs text-slate-400 font-mono">Sequential Node Lifecycle</span>
                </div>

                <div className="relative pl-6 space-y-6 before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-indigo-100">
                  {activeAgent.executionFlow.map((step) => (
                    <div key={step.step} className="relative">
                      <div className="absolute -left-6 top-1 w-6 h-6 rounded-full bg-indigo-600 text-white text-[11px] font-bold flex items-center justify-center shadow">
                        {step.step}
                      </div>

                      <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-xs font-bold text-slate-900">{step.name}</span>
                          <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 font-mono">
                            {step.type}
                          </span>
                        </div>
                        <p className="text-xs text-slate-600">{step.description}</p>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 text-[11px]">
                          <div className="p-1.5 bg-white rounded border border-slate-200">
                            <span className="text-[10px] text-slate-400 block font-mono">Input:</span>
                            <span className="text-slate-700">{step.input}</span>
                          </div>
                          <div className="p-1.5 bg-white rounded border border-slate-200">
                            <span className="text-[10px] text-slate-400 block font-mono">Output:</span>
                            <span className="text-slate-700">{step.output}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* System Prompt Modal */}
      {showPromptModal && activeAgent && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200">
            <div className="p-5 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Code2 className="w-5 h-5 text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900">{activeAgent.name} - System Prompt</h3>
              </div>
              <button
                onClick={() => setShowPromptModal(false)}
                className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition"
              >
                ✕
              </button>
            </div>

            <div className="p-5 overflow-y-auto font-mono text-xs bg-slate-900 text-emerald-400 whitespace-pre-wrap leading-relaxed">
              {activeAgent.systemPrompt}
            </div>

            <div className="p-4 border-t border-slate-100 flex justify-end">
              <button
                onClick={() => setShowPromptModal(false)}
                className="px-4 py-2 bg-slate-900 text-white rounded-xl text-xs font-semibold hover:bg-slate-800 transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function TargetIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg {...props} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <circle cx="12" cy="12" r="6" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  );
}
