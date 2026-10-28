import React from 'react';
import {
  Percent,
  TrendingUp,
  DollarSign,
  Zap,
  Target,
  ArrowRight,
  Sparkles
} from 'lucide-react';
import { formatINR } from '../../data/mockData';
import { useData } from '../../context/DataContext';

interface AdCampaignItem {
  id: string;
  campaignName: string;
  marketplace: string;
  campaignType: string;
  spend30d: number;
  salesAttributed30d: number;
  roas: number;
  acos: number;
  dailyBudget: number;
  aiAction: string;
}

export const AdvertisingRoasView: React.FC = () => {
  const { skus } = useData();

  const dynamicCampaigns: AdCampaignItem[] = skus.slice(0, 6).map((s, idx) => {
    const rawSpend = Math.round((s.sellingPrice || 1000) * 12 + idx * 800);
    const roas = idx % 2 === 0 ? 4.8 : 3.6;
    const attributedSales = Math.round(rawSpend * roas);
    const acos = Math.round((1 / roas) * 100);
    const channel = (s.activeMarketplaces?.[0] || 'amazon') as any;

    return {
      id: `CAMP-${s.sku}`,
      campaignName: `${s.sku} - ${s.name.slice(0, 24)} [Auto-Target]`,
      marketplace: channel,
      campaignType: idx % 2 === 0 ? 'Sponsored Products' : 'Quick Commerce Search Boost',
      spend30d: rawSpend,
      salesAttributed30d: attributedSales,
      roas,
      acos,
      dailyBudget: Math.round(rawSpend / 30),
      aiAction: roas >= 4.5
        ? `Scale budget +20% during peak hours`
        : `Harvest negative keywords`
    };
  });

  const totalSpend = dynamicCampaigns.reduce((sum, c) => sum + c.spend30d, 0);
  const totalSales = dynamicCampaigns.reduce((sum, c) => sum + c.salesAttributed30d, 0);
  const blendedRoas = totalSpend > 0 ? (totalSales / totalSpend).toFixed(2) : '4.20';

  return (
    <div id="advertising-roas-view" className="space-y-6">
      {/* Header */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Advertising & Autonomous ROAS Optimizer</h2>
          <p className="text-xs text-slate-500 mt-1">
            Tracking Sponsored Products, Brands, and Quick Commerce banner performance with automated bidding recommendations
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="p-3 bg-indigo-50 border border-indigo-200 rounded-lg text-center">
            <span className="text-[10px] uppercase font-bold text-indigo-700 block">Blended 30D ROAS</span>
            <span className="text-base font-bold text-indigo-700">{blendedRoas}x</span>
          </div>
        </div>
      </div>

      {/* Campaigns Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Active Multi-Channel Campaigns ({dynamicCampaigns.length})</h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-[11px] uppercase font-bold">
                <th className="py-3 px-4">Campaign Name</th>
                <th className="py-3 px-4">Marketplace</th>
                <th className="py-3 px-4">Campaign Type</th>
                <th className="py-3 px-4">30D Spend</th>
                <th className="py-3 px-4">Attributed Sales</th>
                <th className="py-3 px-4">ROAS</th>
                <th className="py-3 px-4">ACOS</th>
                <th className="py-3 px-4">AI Budget Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {dynamicCampaigns.map((c) => (
                <tr key={c.id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-4">
                    <span className="font-bold text-slate-900">{c.campaignName}</span>
                    <div className="text-[10px] text-slate-500 font-mono">{c.id}</div>
                  </td>
                  <td className="py-3 px-4 font-bold uppercase text-[10px] text-slate-600">{c.marketplace}</td>
                  <td className="py-3 px-4 text-slate-700">{c.campaignType}</td>
                  <td className="py-3 px-4 font-bold text-slate-900">{formatINR(c.spend30d)}</td>
                  <td className="py-3 px-4 font-bold text-emerald-700">{formatINR(c.salesAttributed30d)}</td>
                  <td className="py-3 px-4 font-bold text-slate-900">{c.roas}x</td>
                  <td className="py-3 px-4 text-slate-500">{c.acos}%</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 rounded font-semibold text-[10px]">
                      {c.aiAction}
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
