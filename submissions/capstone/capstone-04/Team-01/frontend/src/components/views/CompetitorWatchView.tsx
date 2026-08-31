import React from 'react';
import {
  Users,
  AlertTriangle,
  TrendingDown,
  Tag,
  Zap,
  ArrowRight,
  ShieldCheck,
  Clock
} from 'lucide-react';
import { CompetitorMove, MarketplaceId } from '../../types';
import { formatINR } from '../../data/mockData';
import { useData } from '../../context/DataContext';

interface CompetitorWatchViewProps {
  onNavigateActions: () => void;
}

export const CompetitorWatchView: React.FC<CompetitorWatchViewProps> = ({
  onNavigateActions
}) => {
  const { skus } = useData();

  const dynamicCompetitorMoves: CompetitorMove[] = skus.slice(0, 4).map((s, idx) => {
    const compNames = ['SleepyCat Ergonomics', 'The Sleep Company SmartGRID', 'Emma Ortho India', 'Wakefit Pro Support'];
    const compTypes: Array<'Price Drop' | 'Flash Sale' | 'Quick Commerce Promo' | 'New Launch'> = ['Price Drop', 'Flash Sale', 'Quick Commerce Promo', 'New Launch'];
    const threats: Array<'Critical' | 'High' | 'Medium'> = ['Critical', 'High', 'Medium'];
    const undercuts = [
      Math.round(s.sellingPrice * 0.85),
      Math.round(s.sellingPrice * 0.88),
      Math.round(s.sellingPrice * 0.90),
      Math.round(s.sellingPrice * 0.82)
    ];

    return {
      id: `COMP-MOVE-${s.sku}-${idx}`,
      competitorName: compNames[idx % compNames.length],
      matchedSku: `${s.sku} - ${s.name.slice(0, 24)}...`,
      type: compTypes[idx % compTypes.length],
      timeAgo: `${(idx + 1) * 8}m ago`,
      threatLevel: threats[idx % threats.length],
      description: `${compNames[idx % compNames.length]} dropped listing price to ₹${undercuts[idx].toLocaleString()} (undercutting ${s.sku} target MAP ₹${s.targetMap.toLocaleString()}).`,
      oldPrice: s.sellingPrice,
      newPrice: undercuts[idx],
      estimatedImpactInr: Math.round((s.grossSales30d || (s.sellingPrice * 100)) * 0.18),
      recommendedPlaybook: `Match quick commerce promotional coupon for ${s.sku} on Blinkit/Zepto while preserving target MAP on Amazon.`
    };
  });

  return (
    <div id="competitor-watch-view" className="space-y-6">
      {/* Header */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Competitor Watch & Threat Radar</h2>
            <span className="px-2 py-0.5 bg-rose-50 text-rose-700 border border-rose-200 text-[10px] font-bold rounded">
              {dynamicCompetitorMoves.length} Live Moves
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time monitoring of competitor price cuts, coupon badges, quick commerce promos, and new launches against your active SKUs
          </p>
        </div>

        <button
          onClick={onNavigateActions}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
        >
          <Zap className="w-3.5 h-3.5 text-amber-300" />
          <span>View Counter Playbooks</span>
        </button>
      </div>

      {/* Competitor Moves Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {dynamicCompetitorMoves.map((move) => {
          const isCritical = move.threatLevel === 'Critical';
          const isHigh = move.threatLevel === 'High';

          return (
            <div
              key={move.id}
              className={`p-5 bg-white rounded-xl border shadow-xs space-y-3.5 ${
                isCritical ? 'border-rose-300 ring-1 ring-rose-100' : isHigh ? 'border-amber-300' : 'border-slate-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-sm text-slate-900">{move.competitorName}</span>
                  <span className="text-[10px] bg-slate-100 text-slate-700 border border-slate-200 px-2 py-0.5 rounded font-semibold">
                    {move.type}
                  </span>
                </div>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${
                  isCritical ? 'bg-rose-100 text-rose-700 border-rose-200' : isHigh ? 'bg-amber-100 text-amber-800 border-amber-200' : 'bg-blue-100 text-blue-700 border-blue-200'
                }`}>
                  {move.threatLevel} Threat
                </span>
              </div>

              <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200">
                {move.description}
              </p>

              <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-100">
                <span className="text-slate-500">Target SKU: <strong className="text-slate-900">{move.matchedSku}</strong></span>
                <span className="text-rose-600 font-bold">Impact: ~{formatINR(move.estimatedImpactInr)}</span>
              </div>

              {/* Recommended Playbook */}
              <div className="p-3 bg-blue-50/70 border border-blue-200 rounded-lg text-xs space-y-1">
                <div className="font-bold text-blue-900 flex items-center space-x-1">
                  <Zap className="w-3.5 h-3.5 text-blue-600" />
                  <span>Autonomous Response:</span>
                </div>
                <p className="text-slate-700">{move.recommendedPlaybook}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
