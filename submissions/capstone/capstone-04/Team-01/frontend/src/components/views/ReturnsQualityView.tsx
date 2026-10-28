import React from 'react';
import {
  RotateCcw,
  AlertTriangle,
  Building,
  CheckCircle2,
  Calendar,
  Layers
} from 'lucide-react';
import { formatINR } from '../../data/mockData';
import { useData } from '../../context/DataContext';

export const ReturnsQualityView: React.FC = () => {
  const { skus } = useData();

  const dynamicReturns = skus.slice(0, 6).map((s, idx) => {
    const reasons = [
      'Outer polybag puncture during quick delivery transit',
      'Customer expected firmer memory foam contour density',
      'Incorrect size variant selected on mobile app',
      'Box seal damaged at dark-store sorting hub',
      'Transit box crush by courier 3PL van delivery'
    ];
    const solutions = [
      'Upgrade to 90 GSM double-layer polybag packaging',
      'Publish video firmness guide in A+ Brand Story',
      'Add dimension selector visual on Quick Commerce PDP',
      'Enforce rigid outer corrugated box packing at Mother Hub',
      'Inspect return batch and claim 3PL courier transit indemnity'
    ];
    const returnRate = (3.2 + (idx % 4) * 1.6).toFixed(1);

    return {
      id: `RET-${s.sku}`,
      sku: `${s.sku} - ${s.name}`,
      channel: (s.activeMarketplaces?.[0] || 'amazon') as string,
      returnRate,
      batchCorrelated: `LOT-2026-${s.sku.replace(/[^0-9]/g, '') || String(idx + 1).padStart(2, '0')}`,
      topReason: reasons[idx % reasons.length],
      actionableSolution: solutions[idx % solutions.length]
    };
  });

  const avgReturn = dynamicReturns.length > 0
    ? (dynamicReturns.reduce((sum, r) => sum + parseFloat(r.returnRate), 0) / dynamicReturns.length).toFixed(1)
    : '5.2';

  return (
    <div id="returns-quality-view" className="space-y-6">
      {/* Header */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Returns & Batch Quality Forensics</h2>
          <p className="text-xs text-slate-500 mt-1">
            Tracking return reasons, defect root cause analysis, warehouse handling correlation, and packaging audits for active SKUs
          </p>
        </div>

        <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-center">
          <span className="text-[10px] uppercase font-bold text-rose-700 block">Catalog Avg Return Rate</span>
          <span className="text-base font-bold text-rose-600">{avgReturn}%</span>
        </div>
      </div>

      {/* Returns Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Root Cause Return Audit by SKU & Batch ({dynamicReturns.length})</h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-[11px] uppercase font-bold">
                <th className="py-3 px-4">SKU & Product</th>
                <th className="py-3 px-4">Channel</th>
                <th className="py-3 px-4">Return Rate</th>
                <th className="py-3 px-4">Correlated Batch</th>
                <th className="py-3 px-4">Top Return Reason</th>
                <th className="py-3 px-4">Quality Playbook Solution</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {dynamicReturns.map((r) => (
                <tr key={r.id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-4 font-bold text-slate-900">{r.sku}</td>
                  <td className="py-3 px-4 uppercase font-bold text-[10px] text-slate-600">{r.channel}</td>
                  <td className="py-3 px-4 font-bold text-rose-600">{r.returnRate}%</td>
                  <td className="py-3 px-4 font-mono font-bold text-slate-800">{r.batchCorrelated}</td>
                  <td className="py-3 px-4 text-slate-700 font-medium">{r.topReason}</td>
                  <td className="py-3 px-4">
                    <span className="px-2.5 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded-md text-[11px] font-semibold">
                      {r.actionableSolution}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
