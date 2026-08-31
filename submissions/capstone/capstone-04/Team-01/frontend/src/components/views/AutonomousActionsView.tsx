import React from 'react';
import {
  Zap,
  CheckCircle2,
  XCircle,
  Clock,
  RotateCcw,
  ShieldCheck,
  Building2,
  Truck,
  ArrowRight
} from 'lucide-react';
import { AutonomousAction } from '../../types';
import { formatINR } from '../../data/mockData';
import { useData } from '../../context/DataContext';
import confetti from 'canvas-confetti';

interface AutonomousActionsViewProps {
  onOpenStockTransfer: (sku: string, hub: string, units?: number) => void;
}

export const AutonomousActionsView: React.FC<AutonomousActionsViewProps> = ({
  onOpenStockTransfer
}) => {
  const { autonomousActions, approveAction, rejectAction } = useData();

  const handleApprove = async (actionId: string) => {
    await approveAction(actionId);
    confetti({
      particleCount: 60,
      spread: 50,
      origin: { y: 0.6 }
    });
  };

  const handleReject = (actionId: string) => {
    rejectAction(actionId);
  };

  const stagedCount = autonomousActions.filter((a) => a.status === 'Pending Approval').length;
  const executedCount = autonomousActions.filter((a) => a.status === 'Executed').length;

  return (
    <div id="autonomous-actions-view" className="space-y-6">
      {/* Header */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Autonomous Action Approvals & Playbooks</h2>
            <span className="px-2 py-0.5 bg-amber-50 text-amber-800 border border-amber-200 text-[10px] font-bold rounded">
              {stagedCount} Staged For Approval
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Supervised AI operations with automated policy guardrails, one-click execution, and instant rollback safety
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-center">
            <span className="text-[10px] uppercase font-bold text-emerald-800 block">Executed Playbooks</span>
            <span className="text-base font-bold text-emerald-700">{executedCount} Live</span>
          </div>
        </div>
      </div>

      {/* Action Cards */}
      <div className="space-y-4">
        {autonomousActions.map((act) => {
          const isPending = act.status === 'Pending Approval';
          const isExecuted = act.status === 'Executed';

          return (
            <div
              key={act.id}
              className={`p-5 bg-white rounded-xl border shadow-xs space-y-3.5 transition-all ${
                isPending ? 'border-amber-300 ring-1 ring-amber-100' : 'border-slate-200'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                <div className="flex items-center space-x-2.5">
                  <span className="font-mono text-xs font-bold text-slate-800 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded">
                    {act.id}
                  </span>
                  <span className="text-xs font-bold text-blue-700">{act.category}</span>
                  <span className="text-slate-300">&bull;</span>
                  <span className="text-xs text-slate-500 font-mono">{act.targetSku}</span>
                  <span className="text-slate-300">&bull;</span>
                  <span className="text-xs font-bold text-slate-700 uppercase">{act.marketplace}</span>
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

              <div className="space-y-1">
                <h3 className="text-sm font-bold text-slate-900">{act.title}</h3>
                <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200">
                  {act.description}
                </p>
              </div>

              {/* Guardrails & Value Impact */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs pt-1 border-t border-slate-100">
                <div className="flex items-center space-x-2 text-slate-600">
                  <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Safety Guardrail: <strong className="text-slate-900">{act.guardrailsCheck}</strong></span>
                </div>

                <div className="flex items-center space-x-2 font-bold text-emerald-700">
                  <span>Estimated Value Recovered:</span>
                  <span className="text-sm font-bold text-emerald-700">{formatINR(act.estimatedValueRecoveredInr)}</span>
                </div>
              </div>

              {/* Action Buttons */}
              {isPending && (
                <div className="flex items-center justify-end space-x-2.5 pt-2">
                  <button
                    onClick={() => handleReject(act.id)}
                    className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-700 text-xs font-semibold rounded-md transition-colors"
                  >
                    Reject
                  </button>
                  <button
                    id={`approve-action-${act.id}`}
                    onClick={() => handleApprove(act.id)}
                    className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-md flex items-center space-x-1.5 shadow-2xs transition-colors"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>1-Click Approve & Execute</span>
                  </button>
                </div>
              )}

              {isExecuted && (
                <div className="p-2.5 bg-emerald-50 border border-emerald-200 rounded-lg text-xs font-medium text-emerald-800 flex items-center justify-between">
                  <span>Playbook executed successfully live on connected marketplace API.</span>
                  <span className="font-mono text-[10px] text-emerald-700 font-bold">Audit ID: #TX-9481</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
