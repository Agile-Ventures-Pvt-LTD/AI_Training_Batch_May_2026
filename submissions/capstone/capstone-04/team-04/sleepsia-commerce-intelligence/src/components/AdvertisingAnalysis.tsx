import React, { useState } from 'react';
import {
  Zap,
  DollarSign,
  TrendingUp,
  Target,
  BarChart2,
  AlertCircle,
  HelpCircle,
  Percent,
  CheckCircle2,
} from 'lucide-react';
import { SleepsiaWorkbookData, CalculatedKPIs } from '../types/commerce';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface AdvertisingAnalysisProps {
  data: SleepsiaWorkbookData;
  kpis: CalculatedKPIs;
  selectedDate: string;
}

export const AdvertisingAnalysis: React.FC<AdvertisingAnalysisProps> = ({
  data,
  kpis,
  selectedDate,
}) => {
  const [platformFilter, setPlatformFilter] = useState<string>('All');
  const fmt = (n?: number | null) => formatCurrency(n);

  const adsForDate = data.advertising.filter((a) => a.date === selectedDate);
  const filteredCampaigns = platformFilter === 'All'
    ? adsForDate
    : adsForDate.filter((a) => a.platform === platformFilter);

  const availablePlatforms = Array.from(new Set(adsForDate.map((a) => a.platform)));

  return (
    <div className="space-y-6">
      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Ad Spend */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Ad Spend</span>
            <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center text-amber-600 border border-amber-100">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <h3 className="text-2xl font-black text-slate-900 mt-2">{fmt(kpis?.advertising?.totalSpend)}</h3>
          <p className="text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
            Across {availablePlatforms.length} active advertising channels
          </p>
        </div>

        {/* Blended ROAS & ACoS */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Blended ROAS (ACoS)</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center text-emerald-600 border border-emerald-100">
              <Target className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2 mt-2">
            <h3 className="text-2xl font-black text-emerald-700">{kpis?.advertising?.roas ?? 0}x</h3>
            <span className="text-xs font-bold text-slate-600 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">
              {kpis?.advertising?.acos ?? 0}% ACoS
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
            Attributed Rev: <strong className="text-slate-800">{fmt(kpis?.advertising?.attributedRevenue)}</strong>
          </p>
        </div>

        {/* Total ACoS (TACoS) */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">TACoS (Total ACoS)</span>
            <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100">
              <Percent className="w-4 h-4" />
            </div>
          </div>
          <h3 className="text-2xl font-black text-blue-700 mt-2">{kpis?.advertising?.tacos ?? 0}%</h3>
          <p className="text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
            Ad Spend as % of Total Net Revenue (Benchmark: &lt; 15%)
          </p>
        </div>

        {/* CTR & CPC */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Engagement (CTR / CPC)</span>
            <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600 border border-indigo-100">
              <Zap className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2 mt-2">
            <h3 className="text-2xl font-black text-indigo-700">{kpis?.advertising?.ctr ?? 0}% CTR</h3>
            <span className="text-xs font-bold text-slate-600 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">
              CPC: {formatCurrency(kpis?.advertising?.cpc)}
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
            Impressions: {formatNumber(kpis?.advertising?.impressions)} | Clicks: {formatNumber(kpis?.advertising?.clicks)}
          </p>
        </div>
      </div>

      {/* Critical Paid vs Organic Intelligence Section */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-amber-600" />
              Paid vs. Organic Incremental Intelligence Model
            </h3>
            <p className="text-xs text-slate-500">
              Decomposing true baseline velocity from paid advertising dependency
            </p>
          </div>
          <span className="text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200 px-2.5 py-1 rounded-full">
            Incremental Confidence: High
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
          {/* Visual Breakdown Bar */}
          <div className="space-y-3">
            <div className="flex justify-between text-xs font-bold">
              <span className="text-amber-700">Paid Ad-Attributed: {kpis.paidVsOrganic.paidContributionPercent}%</span>
              <span className="text-emerald-700">Organic Non-Attributed: {kpis.paidVsOrganic.organicContributionPercent}%</span>
            </div>
            <div className="h-5 w-full bg-slate-100 rounded-lg overflow-hidden flex border border-slate-200">
              <div
                style={{ width: `${kpis.paidVsOrganic.paidContributionPercent}%` }}
                className="bg-amber-500 flex items-center justify-center text-[10px] font-black text-white"
              >
                {kpis.paidVsOrganic.paidContributionPercent}%
              </div>
              <div
                style={{ width: `${kpis.paidVsOrganic.organicContributionPercent}%` }}
                className="bg-emerald-500 flex items-center justify-center text-[10px] font-black text-white"
              >
                {kpis.paidVsOrganic.organicContributionPercent}%
              </div>
            </div>
            <div className="flex justify-between text-xs text-slate-500 font-medium">
              <span>{fmt(kpis.paidVsOrganic.adAttributedSales)} (Attributed GMV)</span>
              <span>{fmt(kpis.paidVsOrganic.organicSales)} (Pure Organic)</span>
            </div>
          </div>

          {/* Business Interpretation Guidelines */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2 text-xs text-slate-700">
            <div className="flex items-center gap-1.5 text-blue-700 font-bold">
              <HelpCircle className="w-3.5 h-3.5" />
              <span>Attribution vs. Incremental Lift Guardrail:</span>
            </div>
            <p className="leading-relaxed text-slate-600">
              {kpis.paidVsOrganic.notes}
            </p>
            <div className="text-[11px] text-slate-600 pt-1 border-t border-slate-200 flex items-center gap-2">
              <CheckCircle2 className="w-3 h-3 text-emerald-600" />
              <span>Organic discovery is highest on D2C Website and Tata 1mg Orthopedic collections.</span>
            </div>
          </div>
        </div>
      </div>

      {/* Campaign Performance Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-xs">
        <div className="p-4 bg-slate-50/80 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Advertising Campaigns Breakdown</h3>
            <p className="text-xs text-slate-500">Detailed campaign-level metrics for {selectedDate}</p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 font-medium">Filter Channel:</span>
            <select
              value={platformFilter}
              onChange={(e) => setPlatformFilter(e.target.value)}
              className="bg-white border border-slate-200 text-slate-900 text-xs rounded-md px-2.5 py-1.5 outline-none shadow-xs focus:ring-1 focus:ring-blue-500 font-medium"
            >
              <option value="All">All Channels</option>
              {availablePlatforms.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                <th className="py-3 px-4">Campaign Name / SKU</th>
                <th className="py-3 px-4">Platform</th>
                <th className="py-3 px-4">Type</th>
                <th className="py-3 px-4 text-right">Spend</th>
                <th className="py-3 px-4 text-right">Attributed Rev</th>
                <th className="py-3 px-4 text-right">ROAS</th>
                <th className="py-3 px-4 text-right">ACoS %</th>
                <th className="py-3 px-4 text-right">Clicks / Orders</th>
                <th className="py-3 px-4 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-800">
              {filteredCampaigns.map((camp) => (
                <tr key={camp.campaignId + camp.platform} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3 px-4">
                    <div className="font-bold text-slate-900">{camp.campaignName}</div>
                    <div className="text-[10px] text-slate-400 font-mono">{camp.sku} • {camp.campaignId}</div>
                  </td>
                  <td className="py-3 px-4 font-semibold text-slate-800">{camp.platform}</td>
                  <td className="py-3 px-4 text-slate-600">{camp.campaignType}</td>
                  <td className="py-3 px-4 text-right font-black text-amber-700">{fmt(camp.spend)}</td>
                  <td className="py-3 px-4 text-right font-bold text-slate-900">{fmt(camp.attributedRevenue)}</td>
                  <td className="py-3 px-4 text-right">
                    <span className={`font-bold ${
                      camp.roas >= 4.0 ? 'text-emerald-700' : camp.roas >= 2.8 ? 'text-blue-700' : 'text-rose-700'
                    }`}>
                      {camp.roas}x
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right font-semibold text-slate-700">{camp.acos}%</td>
                  <td className="py-3 px-4 text-right text-slate-600">
                    {camp.clicks} clk / <strong className="text-slate-800">{camp.orders} ord</strong>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      {camp.status}
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
