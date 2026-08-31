import React, { useState } from 'react';
import {
  ShieldAlert,
  TrendingDown,
  Star,
  Tag,
  AlertTriangle,
  Award,
  Search,
  ExternalLink,
} from 'lucide-react';
import { SleepsiaWorkbookData, CalculatedKPIs } from '../types/commerce';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface CompetitorIntelligenceProps {
  data: SleepsiaWorkbookData;
  kpis: CalculatedKPIs;
  selectedDate: string;
}

export const CompetitorIntelligence: React.FC<CompetitorIntelligenceProps> = ({
  data,
  kpis,
  selectedDate,
}) => {
  const [selectedBrand, setSelectedBrand] = useState<string>('All');
  const fmt = (n?: number | null) => formatCurrency(n);

  const competitorsForDate = data.competitors.filter((c) => c.date === selectedDate);
  const brands = Array.from(new Set(competitorsForDate.map((c) => c.competitorBrand)));

  const filteredCompetitors = selectedBrand === 'All'
    ? competitorsForDate
    : competitorsForDate.filter((c) => c.competitorBrand === selectedBrand);

  return (
    <div className="space-y-6">
      {/* Top Benchmark Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg Competitor Price</span>
          <h3 className="text-2xl font-black text-slate-900 mt-2">{fmt(kpis.competitor.avgCompetitorPrice)}</h3>
          <p className="text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
            Sleepsia Benchmark: <strong className="text-slate-800">{fmt(kpis.competitor.sleepsiaAvgPrice)}</strong>
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Price Gap Variance</span>
          <div className="flex items-baseline gap-2 mt-2">
            <h3 className={`text-2xl font-black ${kpis.competitor.priceGapPercent > 0 ? 'text-amber-700' : 'text-emerald-700'}`}>
              {kpis.competitor.priceGapPercent > 0 ? `+${kpis.competitor.priceGapPercent}%` : `${kpis.competitor.priceGapPercent}%`}
            </h3>
            <span className="text-xs font-medium text-slate-500">Premium vs Rivals</span>
          </div>
          <p className="text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
            Sleepsia positioned as premium ergonomic brand
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg Competitor Discount</span>
          <h3 className="text-2xl font-black text-rose-700 mt-2">{kpis.competitor.avgCompetitorDiscount}% Off</h3>
          <p className="text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
            Sleepsia Discount: <strong className="text-slate-800">32% Off</strong>
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Sleepsia Quality Advantage</span>
          <div className="flex items-baseline gap-2 mt-2">
            <h3 className="text-2xl font-black text-emerald-700">+0.3★</h3>
            <span className="text-xs font-medium text-slate-500">Rating Lead</span>
          </div>
          <p className="text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
            Sleepsia (4.6★) vs Competitors (4.3★ avg)
          </p>
        </div>
      </div>

      {/* Critical Competitor Threat Alert */}
      <div className="bg-gradient-to-r from-rose-50/70 via-white to-white border border-rose-200 rounded-xl p-5 shadow-xs">
        <div className="flex items-center gap-2 mb-2">
          <ShieldAlert className="w-5 h-5 text-rose-600" />
          <h3 className="text-sm font-bold text-slate-900">Live Competitor Action Spotlight (Wakefit Flash Sale)</h3>
        </div>
        <p className="text-xs text-slate-700 leading-relaxed">
          Competitor <strong className="text-slate-900">Wakefit</strong> launched a 45% discount campaign with instant ₹150 Amazon coupon on Memory Foam Contour Pillows. This correlated directly with an increase in Wakefit's sponsored search ranking to <strong className="text-slate-900">#1</strong> on primary category keywords and contributed to an 13.04% decline in Sleepsia Amazon sales.
        </p>
        <div className="mt-3 text-xs bg-blue-50/80 p-3 rounded-lg border border-blue-200 text-blue-900 font-medium">
          <strong className="text-blue-950">AI Counter-Strategy:</strong> Counter with a value-bundle promotion (Pillow + Bamboo Protector) rather than participating in a direct margin-eroding price war.
        </div>
      </div>

      {/* Competitor Catalog Comparison Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-xs">
        <div className="p-4 bg-slate-50/80 flex flex-wrap items-center justify-between gap-3 border-b border-slate-200">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Competitor Price, Rating &amp; Visibility Matrix</h3>
            <p className="text-xs text-slate-500">Tracked across Amazon, Flipkart and Quick Commerce</p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 font-medium">Filter Brand:</span>
            <select
              value={selectedBrand}
              onChange={(e) => setSelectedBrand(e.target.value)}
              className="bg-white border border-slate-200 text-slate-900 text-xs rounded-md px-2.5 py-1.5 outline-none shadow-xs focus:ring-1 focus:ring-blue-500 font-medium"
            >
              <option value="All">All Competitor Brands</option>
              {brands.map((b) => (
                <option key={b} value={b}>
                  {b}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                <th className="py-3 px-4">Competitor &amp; Product Name</th>
                <th className="py-3 px-4">Targeted Category</th>
                <th className="py-3 px-4 text-right">Competitor Price</th>
                <th className="py-3 px-4 text-center">Discount %</th>
                <th className="py-3 px-4 text-center">Rating / Reviews</th>
                <th className="py-3 px-4 text-center">Search Rank</th>
                <th className="py-3 px-4">Active Promotion</th>
                <th className="py-3 px-4 text-center">Threat Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-800">
              {filteredCompetitors.map((c, i) => (
                <tr key={i} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-slate-900">{c.competitorBrand}</div>
                    <div className="text-[11px] text-slate-500">{c.competitorProductName}</div>
                  </td>
                  <td className="py-3.5 px-4 text-slate-600 font-medium">{c.category}</td>
                  <td className="py-3.5 px-4 text-right font-bold text-slate-900">{fmt(c.competitorPrice)}</td>
                  <td className="py-3.5 px-4 text-center">
                    <span className="px-2 py-0.5 rounded font-bold text-rose-700 bg-rose-50 border border-rose-200 text-[11px]">
                      {c.discountPercent}% OFF
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <span className="font-bold text-amber-600 flex items-center justify-center gap-1">
                      <Star className="w-3 h-3 fill-amber-500 text-amber-500" /> {c.rating.toFixed(1)}
                    </span>
                    <span className="text-[10px] text-slate-500 block">{c.reviewCount} revs</span>
                  </td>
                  <td className="py-3.5 px-4 text-center font-bold text-slate-800">
                    #{c.searchPosition}
                  </td>
                  <td className="py-3.5 px-4 text-slate-700">
                    <span className="flex items-center gap-1 text-[11px]">
                      <Tag className="w-3 h-3 text-amber-600" />
                      {c.activePromotion}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${
                      c.threatLevel === 'Severe'
                        ? 'bg-rose-50 text-rose-700 border-rose-200'
                        : c.threatLevel === 'High'
                        ? 'bg-amber-50 text-amber-700 border-amber-200'
                        : 'bg-slate-100 text-slate-600 border-slate-200'
                    }`}>
                      {c.threatLevel}
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
