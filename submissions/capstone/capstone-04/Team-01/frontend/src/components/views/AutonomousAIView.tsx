import React, { useState } from 'react';
import {
  Zap,
  AlertTriangle,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  RotateCcw,
  Sparkles,
  ArrowRight,
  Send,
  Building2,
  Lock,
  RefreshCw
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { useData } from '../../context/DataContext';
import { AutonomousAction, AlertAnomaly } from '../../types';
import { formatINR } from '../../data/mockData';

interface AutonomousAIViewProps {
  onOpenStockTransfer: (sku: string, hub: string, units?: number) => void;
  onOpenEmailModal: (anomaly?: AlertAnomaly) => void;
}

export const AutonomousAIView: React.FC<AutonomousAIViewProps> = ({
  onOpenStockTransfer,
  onOpenEmailModal
}) => {
  const { alerts, skus, autonomousActions: contextActions } = useData();

  // Actions state to allow interactive approve / reject
  const [actions, setActions] = useState<AutonomousAction[]>([]);
  const [activeTab, setActiveTab] = useState<'pending_actions' | 'live_anomalies' | 'rules_engine'>('pending_actions');

  React.useEffect(() => {
    if (contextActions && contextActions.length > 0) {
      setActions(contextActions);
    } else {
      // Generate from alerts if contextActions is empty
      const generated: AutonomousAction[] = alerts.map((a, idx) => ({
        id: `ACT-${a.sku}-${idx + 1}`,
        actionCode: `PLAYBOOK-${a.sku}`,
        title: a.recommendedPlaybook || `Auto-Remediation for ${a.sku}`,
        description: a.summary,
        channel: a.marketplace,
        marketplace: a.marketplace,
        category: 'Autonomous Decision Engine',
        agentName: 'Operations AI Agent',
        targetSku: a.sku,
        sku: a.sku,
        status: idx === 0 || idx === 1 ? 'Pending Approval' : 'Executed',
        confidencePercent: 96 - idx * 2,
        confidenceScore: 96 - idx * 2,
        projectedRoiInr: a.revenueAtRiskInr || 150000,
        estimatedValueRecoveredInr: a.revenueAtRiskInr || 150000,
        approvalRequired: true,
        safetyGuardrail: 'Autonomous policy threshold limits rate of change and validates Mother Hub stock reserves prior to execution.',
        guardrailsCheck: 'Passed (Risk verified against policy)',
        playbookType: a.recommendedPlaybook || 'Auto-Playbook',
        triggerAlertId: a.id
      }));
      setActions(generated);
    }
  }, [alerts, contextActions]);

  const handleApprove = (actionId: string) => {
    setActions((prev) =>
      prev.map((a) =>
        a.id === actionId
          ? { ...a, status: 'Executed', executionStatus: 'Completed via API' }
          : a
      )
    );

    confetti({
      particleCount: 50,
      spread: 60,
      origin: { y: 0.6 }
    });
  };

  const handleReject = (actionId: string) => {
    setActions((prev) =>
      prev.map((a) => (a.id === actionId ? { ...a, status: 'Rejected' } : a))
    );
  };

  const pendingCount = actions.filter((a) => a.status === 'Pending Approval').length;
  const executedCount = actions.filter((a) => a.status === 'Executed').length;

  return (
    <div id="autonomous-ai-workspace" className="space-y-6">
      {/* 1. Header */}
      <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-2xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 bg-amber-50 text-amber-800 border border-amber-200 text-[11px] font-bold rounded-md uppercase tracking-wider">
              Autonomous AI Decision Engine
            </span>
            <span className="text-slate-400 text-xs">•</span>
            <span className="text-xs text-slate-500 font-medium">
              Human-in-the-Loop Supervised Execution
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-1">
            Anomalies, Playbooks & Action Approvals
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time rule-based anomaly detection evaluating stock starvation, pricing breaches, and automated remediation playbooks.
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-right">
            <span className="text-[10px] font-bold text-amber-800 uppercase block">Pending Approval</span>
            <span className="text-base font-black text-amber-700">{pendingCount} Staged</span>
          </div>

          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-right">
            <span className="text-[10px] font-bold text-emerald-800 uppercase block">Executed Live</span>
            <span className="text-base font-black text-emerald-700">{executedCount} Live</span>
          </div>
        </div>
      </div>

      {/* 2. Workspace Navigation Tabs */}
      <div className="flex border-b border-slate-200 gap-6 text-xs font-bold">
        <button
          onClick={() => setActiveTab('pending_actions')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all ${
            activeTab === 'pending_actions'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <Zap className="w-4 h-4" />
          <span>Action Approvals Queue ({pendingCount})</span>
        </button>

        <button
          onClick={() => setActiveTab('live_anomalies')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all ${
            activeTab === 'live_anomalies'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <AlertTriangle className="w-4 h-4" />
          <span>Rule-Detected Anomalies ({alerts.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('rules_engine')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all ${
            activeTab === 'rules_engine'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          <span>Operational Rules & Guardrails</span>
        </button>
      </div>

      {/* 3. Tab Content */}
      {activeTab === 'pending_actions' && (
        <div className="space-y-4">
          {actions.map((act) => {
            const isPending = act.status === 'Pending Approval';
            const isExecuted = act.status === 'Executed';

            return (
              <div
                key={act.id}
                className={`p-5 bg-white rounded-xl border shadow-2xs space-y-3.5 transition-all ${
                  isPending ? 'border-amber-300 ring-1 ring-amber-100' : 'border-slate-200'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-bold text-slate-900 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded">
                      {act.id}
                    </span>
                    <span className="text-xs font-bold text-blue-700">{act.category}</span>
                    <span className="text-slate-300">•</span>
                    <span className="text-xs font-mono text-slate-600 font-bold">{act.targetSku || act.sku}</span>
                    <span className="text-slate-300">•</span>
                    <span className="text-xs uppercase font-bold text-slate-700">{act.marketplace || act.channel}</span>
                  </div>

                  <span className={`px-2.5 py-0.5 rounded text-xs font-bold border ${
                    isPending
                      ? 'bg-amber-100 text-amber-800 border-amber-200 animate-pulse'
                      : isExecuted
                      ? 'bg-emerald-100 text-emerald-800 border-emerald-200'
                      : 'bg-slate-100 border border-slate-200 text-slate-600'
                  }`}>
                    {act.status}
                  </span>
                </div>

                <div className="space-y-1.5">
                  <h3 className="text-sm font-bold text-slate-900">{act.title}</h3>
                  <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200">
                    {act.description}
                  </p>
                </div>

                {/* Guardrails and Projected ROI */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs pt-1 border-t border-slate-100">
                  <div className="flex items-center space-x-2 text-slate-600">
                    <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                    <span>Guardrail: <strong className="text-slate-900">{act.guardrailsCheck || act.safetyGuardrail}</strong></span>
                  </div>

                  <div className="flex items-center space-x-2 font-bold text-emerald-700">
                    <span>Projected ROI:</span>
                    <span className="text-sm font-bold text-emerald-700">
                      {formatINR(act.projectedRoiInr || act.estimatedValueRecoveredInr)}
                    </span>
                  </div>
                </div>

                {/* Actions */}
                {isPending && (
                  <div className="flex items-center justify-end space-x-2.5 pt-2">
                    <button
                      onClick={() => handleReject(act.id)}
                      className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-700 text-xs font-semibold rounded-md transition-colors"
                    >
                      Reject
                    </button>
                    <button
                      onClick={() => handleApprove(act.id)}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-md flex items-center space-x-1.5 shadow-2xs transition-colors"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>1-Click Approve & Auto-Execute</span>
                    </button>
                  </div>
                )}

                {isExecuted && (
                  <div className="p-2.5 bg-emerald-50 border border-emerald-200 rounded-lg text-xs font-medium text-emerald-800 flex items-center justify-between">
                    <span>Playbook executed successfully live on connected channel API.</span>
                    <span className="font-mono text-[10px] text-emerald-700 font-bold">Audit ID: #TX-LIVE</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {activeTab === 'live_anomalies' && (
        <div className="space-y-3">
          {alerts.map((a) => (
            <div
              key={a.id}
              className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-3"
            >
              <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-0.5 text-[10px] font-bold rounded uppercase ${
                    a.severity === 'Critical'
                      ? 'bg-red-100 text-red-800 border border-red-200'
                      : 'bg-amber-100 text-amber-800 border border-amber-200'
                  }`}>
                    {a.severity}
                  </span>
                  <span className="font-bold text-xs text-slate-900">{a.summary}</span>
                </div>
                <span className="text-[10px] text-slate-400 font-medium">{a.timeDisplay || 'Just now'}</span>
              </div>

              <p className="text-xs text-slate-700 bg-slate-50 p-3 rounded-lg border border-slate-100">
                {a.summary}
              </p>

              <div className="flex items-center justify-between pt-1">
                <div className="text-xs text-slate-600">
                  Revenue at risk: <strong className="text-red-600 font-mono">{formatINR(a.revenueAtRiskInr)}</strong>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onOpenEmailModal(a)}
                    className="px-3 py-1.5 bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 text-xs font-semibold rounded-md"
                  >
                    Dispatch Notice
                  </button>
                  {a.transferUnitsSuggested && a.transferUnitsSuggested > 0 && (
                    <button
                      onClick={() => onOpenStockTransfer(a.sku, a.motherHubName || 'Central Hub', a.transferUnitsSuggested)}
                      className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-md"
                    >
                      Stock Transfer
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'rules_engine' && (
        <div className="p-6 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-4">
          <h3 className="text-sm font-bold text-slate-900">Operational E-Commerce Business Rules</h3>
          <div className="space-y-3 text-xs text-slate-700">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
              <strong className="text-slate-900 block font-bold">Rule 1: Quick Commerce Micro-OOS</strong>
              <p className="text-slate-600">If dark store inventory runway is under 48 hours (<code className="bg-slate-200 px-1 rounded">darkStoreStock &lt; dailyVelocity * 2</code>), an automated stock replenishment transfer order is staged from the Mother Hub.</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
              <strong className="text-slate-900 block font-bold">Rule 2: Minimum Advertised Price (MAP) Protection</strong>
              <p className="text-slate-600">If active marketplace selling price is below target MAP (<code className="bg-slate-200 px-1 rounded">sellingPrice &lt; targetMap</code>), triggers an automated cease-and-desist notice and price parity lock.</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
              <strong className="text-slate-900 block font-bold">Rule 3: Batch Expiry & FEFO Liquidation</strong>
              <p className="text-slate-600">If batch shelf life drops below 180 days, an automated First-Expiry-First-Out flash promotion is scheduled on connected quick commerce channels.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
