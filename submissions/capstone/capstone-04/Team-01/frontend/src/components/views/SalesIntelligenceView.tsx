import React from 'react';
import {
  TrendingUp,
  DollarSign,
  ShoppingCart,
  Percent,
  ArrowUpRight,
  ArrowDownRight,
  Filter,
  Download
} from 'lucide-react';
import { MarketplaceId } from '../../types';
import { formatINR, formatPercent } from '../../data/mockData';
import { useData } from '../../context/DataContext';

interface SalesIntelligenceViewProps {
  selectedChannel: MarketplaceId | 'all';
  onSelectSku: (skuId: string) => void;
}

export const SalesIntelligenceView: React.FC<SalesIntelligenceViewProps> = ({
  selectedChannel,
  onSelectSku
}) => {
  const { skus } = useData();
  const [selectedCategory, setSelectedCategory] = React.useState<string>('all');

  const categories = ['all', ...Array.from(new Set(skus.map((s) => s.category || s.productType || 'Sleep Support').filter(Boolean)))];

  const filteredSkus = skus.filter((s) => {
    if (selectedChannel !== 'all' && !s.activeMarketplaces?.includes(selectedChannel)) return false;
    const cat = s.category || s.productType || 'Sleep Support';
    if (selectedCategory !== 'all' && cat !== selectedCategory) return false;
    return true;
  });

  const totalGross = filteredSkus.reduce((sum, s) => sum + (s.grossSales30d || (s.sellingPrice * (s.unitsSold30d || 100))), 0);
  const totalUnits = filteredSkus.reduce((sum, s) => sum + (s.unitsSold30d || 100), 0);
  const avgAsp = totalUnits > 0 ? Math.round(totalGross / totalUnits) : 0;

  return (
    <div id="sales-intelligence-view" className="space-y-6">
      
      {/* Header Summary */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Sales Intelligence & Unit Economics</h2>
          <p className="text-xs text-slate-500 mt-1">
            Comprehensive revenue attribution, sales velocity, organic vs paid contribution, and ASP trends
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-right">
            <span className="text-[10px] uppercase font-bold text-blue-700 block">Catalog 30D Revenue</span>
            <span className="text-base font-bold text-blue-700">{formatINR(totalGross, { abbreviate: true })}</span>
          </div>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs space-y-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Gross Sales (30D)</span>
          <p className="text-lg font-bold text-slate-900">{formatINR(totalGross, { abbreviate: true })}</p>
          <span className="text-xs font-semibold text-emerald-600 flex items-center">
            <TrendingUp className="w-3 h-3 mr-0.5" /> +8.4% YoY
          </span>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs space-y-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Units Sold</span>
          <p className="text-lg font-bold text-slate-900">{totalUnits.toLocaleString()} Units</p>
          <span className="text-xs font-semibold text-emerald-600 flex items-center">
            <TrendingUp className="w-3 h-3 mr-0.5" /> +11.2% MoM
          </span>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs space-y-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Effective ASP</span>
          <p className="text-lg font-bold text-slate-900">{formatINR(avgAsp)}</p>
          <span className="text-xs text-slate-500">Target MAP Average</span>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs space-y-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Quick Commerce Velocity</span>
          <p className="text-lg font-bold text-amber-700">36.5% Share</p>
          <span className="text-xs text-slate-500">10-15 Min Delivery SLA</span>
        </div>
      </div>

      {/* Category Filter Chips */}
      {categories.length > 2 && (
        <div className="flex flex-wrap items-center gap-2 bg-white p-3.5 border border-slate-200 rounded-xl shadow-xs text-xs">
          <span className="font-semibold text-slate-600 flex items-center space-x-1">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span>Category:</span>
          </span>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                selectedCategory === cat
                  ? 'bg-blue-600 text-white shadow-2xs'
                  : 'bg-slate-100 border border-slate-200 text-slate-700 hover:bg-slate-200'
              }`}
            >
              {cat === 'all' ? 'All Categories' : cat}
            </button>
          ))}
        </div>
      )}

      {/* Detailed SKU Sales Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Active SKU Revenue Breakdown</h3>
            <p className="text-xs text-slate-500">Showing {filteredSkus.length} active assortment lines from dataset</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-[11px] uppercase font-bold">
                <th className="py-3 px-4">SKU & Product</th>
                <th className="py-3 px-4">Category / Type</th>
                <th className="py-3 px-4">Effective Price</th>
                <th className="py-3 px-4">30D Gross Sales</th>
                <th className="py-3 px-4">Units Sold</th>
                <th className="py-3 px-4">Daily Velocity</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredSkus.map((sku) => (
                <tr key={sku.id || sku.sku} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-4">
                    <button
                      onClick={() => onSelectSku(sku.sku || sku.id)}
                      className="font-bold text-slate-900 hover:text-blue-600 text-left"
                    >
                      {sku.name}
                    </button>
                    <div className="text-[10px] text-slate-500 font-mono">{sku.sku}</div>
                  </td>
                  <td className="py-3 px-4 text-slate-700">{sku.productType || sku.category || 'Ergonomic Support'}</td>
                  <td className="py-3 px-4 font-semibold text-slate-800">{formatINR(sku.sellingPrice)}</td>
                  <td className="py-3 px-4 font-bold text-slate-900">
                    {formatINR(sku.grossSales30d || (sku.sellingPrice * (sku.unitsSold30d || 100)), { abbreviate: true })}
                  </td>
                  <td className="py-3 px-4 text-slate-700">{(sku.unitsSold30d || 100).toLocaleString()}</td>
                  <td className="py-3 px-4 font-semibold text-slate-800">{sku.dailyVelocity || 12} / day</td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => onSelectSku(sku.sku || sku.id)}
                      className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 rounded text-xs font-semibold"
                    >
                      Inspect
                    </button>
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
