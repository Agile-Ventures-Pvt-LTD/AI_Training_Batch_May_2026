import React, { useState } from 'react';
import {
  Package,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Zap,
  DollarSign,
  ShieldCheck,
  Search,
} from 'lucide-react';
import { SleepsiaWorkbookData, CalculatedKPIs } from '../types/commerce';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface ProductIntelligenceProps {
  data: SleepsiaWorkbookData;
  kpis: CalculatedKPIs;
  selectedDate: string;
}

export const ProductIntelligence: React.FC<ProductIntelligenceProps> = ({
  data,
  kpis,
  selectedDate,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const fmt = (n?: number | null) => formatCurrency(n);

  // Build product performance list
  const productStats = data.products.map((p) => {
    const productSales = data.sales.filter((s) => s.date === selectedDate && s.sku === p.sku);
    const productAds = data.advertising.filter((a) => a.date === selectedDate && a.sku === p.sku);
    const productInv = data.inventory.filter((i) => i.date === selectedDate && i.sku === p.sku);

    const units = productSales.reduce((acc, s) => acc + s.units, 0);
    const netRevenue = productSales.reduce((acc, s) => acc + s.netRealizedRevenue, 0);
    const cogs = p.standardCost * units;
    const adSpend = productAds.reduce((acc, a) => acc + a.spend, 0);
    const adRev = productAds.reduce((acc, a) => acc + a.attributedRevenue, 0);
    const profit = netRevenue - cogs - adSpend - Math.round(netRevenue * 0.15);
    const margin = netRevenue > 0 ? Number(((profit / netRevenue) * 100).toFixed(1)) : 0;

    const adDependency = netRevenue > 0 ? Number(((adRev / netRevenue) * 100).toFixed(1)) : 0;
    const daysLeft = productInv.length > 0 ? Math.min(...productInv.map((i) => i.daysOfInventory)) : 14;
    const isStockoutRisk = daysLeft <= 4;

    return {
      sku: p.sku,
      name: p.productName,
      category: p.category,
      mrp: p.mrp,
      cost: p.standardCost,
      units,
      netRevenue,
      profit,
      margin,
      adSpend,
      adRev,
      adDependency,
      daysLeft,
      isStockoutRisk,
      lifecycle: p.productLifecycle,
    };
  });

  const filteredProducts = productStats.filter(
    (p) =>
      p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Top Header Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Package className="w-5 h-5 text-blue-600" />
              Product Catalog Intelligence &amp; Profitability Matrix
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              SKU-level margins, advertising dependency, and warehouse stockout risk for {selectedDate}
            </p>
          </div>

          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search product or SKU..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-white border border-slate-200 text-slate-900 text-xs rounded-lg pl-8 pr-3 py-2 outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 w-64 shadow-xs"
            />
          </div>
        </div>
      </div>

      {/* Main Product Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                <th className="py-3 px-4">Product Name &amp; SKU</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4 text-right">MRP / Unit Cost</th>
                <th className="py-3 px-4 text-right">Units Sold</th>
                <th className="py-3 px-4 text-right">Net Revenue</th>
                <th className="py-3 px-4 text-right">Net Profit (Margin)</th>
                <th className="py-3 px-4 text-center">Ad Dependency</th>
                <th className="py-3 px-4 text-center">Stock Buffer</th>
                <th className="py-3 px-4 text-center">Lifecycle</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-800">
              {filteredProducts.map((p) => (
                <tr key={p.sku} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-slate-900">{p.name}</div>
                    <div className="text-[10px] text-slate-400 font-mono">{p.sku}</div>
                  </td>
                  <td className="py-3.5 px-4 text-slate-600 font-medium">{p.category}</td>
                  <td className="py-3.5 px-4 text-right">
                    <span className="font-semibold text-slate-900">{fmt(p.mrp)}</span>
                    <span className="text-[10px] text-slate-500 block font-mono">Cost: {fmt(p.cost)}</span>
                  </td>
                  <td className="py-3.5 px-4 text-right font-bold text-slate-800">{p.units}</td>
                  <td className="py-3.5 px-4 text-right font-black text-slate-900">{fmt(p.netRevenue)}</td>
                  <td className="py-3.5 px-4 text-right">
                    <span className={`font-bold ${p.profit > 0 ? 'text-emerald-700' : 'text-rose-700'}`}>
                      {fmt(p.profit)}
                    </span>
                    <span className="text-[10px] text-slate-500 block font-medium">({p.margin}% margin)</span>
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${
                      p.adDependency > 65
                        ? 'bg-amber-50 text-amber-700 border-amber-200'
                        : 'bg-slate-100 text-slate-700 border-slate-200'
                    }`}>
                      {p.adDependency}% Paid
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-bold border ${
                      p.isStockoutRisk
                        ? 'bg-rose-50 text-rose-700 border-rose-200'
                        : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    }`}>
                      {p.daysLeft} days
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <span className="text-[11px] font-medium text-slate-700 px-2 py-0.5 bg-slate-100 rounded border border-slate-200">
                      {p.lifecycle}
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
