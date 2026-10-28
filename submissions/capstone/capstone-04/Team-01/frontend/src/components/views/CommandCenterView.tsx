import React, { useState, useMemo } from 'react';
import {
  TrendingUp,
  DollarSign,
  Package,
  ShieldCheck,
  AlertTriangle,
  ArrowUpRight,
  Sparkles,
  Mail,
  Volume2,
  Filter,
  Search,
  Download,
  Building2,
  Calendar,
  Layers,
  ChevronRight,
  ShoppingBag,
  Zap
} from 'lucide-react';
import { useData } from '../../context/DataContext';
import { MarketplaceId, SKUListing, AlertAnomaly } from '../../types';
import { formatINR } from '../../data/mockData';

interface CommandCenterViewProps {
  onOpenEmailModal: (context?: any) => void;
  onOpenStockTransfer: (sku: string, hub: string, units?: number) => void;
  onSelectSku?: (skuId: string) => void;
  onNavigateToView?: (view: any) => void;
}

export const CommandCenterView: React.FC<CommandCenterViewProps> = ({
  onOpenEmailModal,
  onOpenStockTransfer,
  onSelectSku,
  onNavigateToView
}) => {
  const { skus, alerts, mapBreaches, darkStores, currentUser } = useData();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedChannel, setSelectedChannel] = useState<MarketplaceId | 'all'>('all');
  const [sortBy, setSortBy] = useState<'sales' | 'velocity' | 'margin' | 'stock'>('sales');

  // Dynamic calculations across active uploaded dataset
  const metrics = useMemo(() => {
    const total30dSales = skus.reduce((sum, s) => {
      const sales = s.grossSales30d || (s.sellingPrice * (s.dailyVelocity || 50) * 30);
      return sum + sales;
    }, 0);

    const totalUnitsSold = skus.reduce((sum, s) => sum + (s.unitsSold30d || (s.dailyVelocity || 50) * 30), 0);
    const avgSellingPrice = skus.length > 0
      ? Math.round(skus.reduce((sum, s) => sum + s.sellingPrice, 0) / skus.length)
      : 0;

    const totalMapBreaches = mapBreaches.length;
    const lowStockSkus = skus.filter(s => (s.darkStoreStock ?? 15) < 5 || s.stockStatus === 'Low Stock' || s.stockStatus === 'Out Of Stock');
    const totalRevenueAtRisk = alerts.reduce((sum, a) => sum + (a.revenueAtRiskInr || 0), 0);

    const validRoas = skus.filter(s => s.roas !== undefined && !isNaN(s.roas));
    const blendedRoas = validRoas.length > 0
      ? (validRoas.reduce((sum, s) => sum + (s.roas || 0), 0) / validRoas.length).toFixed(2)
      : '4.20';
    const avgAcos = skus.length > 0
      ? Math.round(skus.reduce((sum, s) => sum + (s.acos ?? 18.5), 0) / skus.length)
      : 18;
    const avgTacos = skus.length > 0
      ? Math.round(skus.reduce((sum, s) => sum + (s.tacos ?? 12.0), 0) / skus.length)
      : 12;
    const totalAdSpend = skus.reduce((sum, s) => sum + (s.adCost30d ?? Math.round((s.grossSales30d || (s.sellingPrice * (s.dailyVelocity || 50) * 30)) * 0.12)), 0);

    return {
      total30dSales,
      totalUnitsSold,
      avgSellingPrice,
      totalMapBreaches,
      lowStockCount: lowStockSkus.length,
      totalRevenueAtRisk,
      activeSkuCount: skus.length,
      blendedRoas,
      avgAcos,
      avgTacos,
      totalAdSpend
    };
  }, [skus, alerts, mapBreaches]);

  // Filtered & sorted SKU list
  const filteredSkus = useMemo(() => {
    return skus
      .filter((sku) => {
        const matchesSearch =
          sku.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          sku.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
          (sku.category && sku.category.toLowerCase().includes(searchQuery.toLowerCase()));

        const matchesCategory = selectedCategory === 'all' || sku.category === selectedCategory || sku.productType === selectedCategory;
        const matchesChannel = selectedChannel === 'all' || (sku.activeMarketplaces && sku.activeMarketplaces.includes(selectedChannel));

        return matchesSearch && matchesCategory && matchesChannel;
      })
      .sort((a, b) => {
        const aSales = a.grossSales30d || (a.sellingPrice * (a.dailyVelocity || 50) * 30);
        const bSales = b.grossSales30d || (b.sellingPrice * (b.dailyVelocity || 50) * 30);
        if (sortBy === 'sales') return bSales - aSales;
        if (sortBy === 'velocity') return (b.dailyVelocity || 0) - (a.dailyVelocity || 0);
        if (sortBy === 'margin') return (b.mrp - b.sellingPrice) - (a.mrp - a.sellingPrice);
        if (sortBy === 'stock') return (a.darkStoreStock ?? 0) - (b.darkStoreStock ?? 0);
        return 0;
      });
  }, [skus, searchQuery, selectedCategory, selectedChannel, sortBy]);

  const categories = useMemo(() => {
    const set = new Set<string>();
    skus.forEach((s) => {
      if (s.category) set.add(s.category);
      if (s.productType) set.add(s.productType);
    });
    return Array.from(set);
  }, [skus]);

  return (
    <div id="command-center-workspace" className="space-y-6">
      {currentUser?.role === 'Analyst' && (
        <div className="p-3.5 bg-amber-50 border border-amber-200 text-amber-900 rounded-xl text-xs font-medium flex items-center justify-between shadow-xs">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded border border-amber-300">Analyst View (Restricted)</span>
            <span>Financial revenue figures, ad spend metrics, email dispatch, and operational action triggers are restricted to Owner access.</span>
          </div>
          <span className="text-[10px] font-bold text-amber-700 bg-white px-2 py-1 rounded border border-amber-200 uppercase">Owner Only Security</span>
        </div>
      )}

      {/* 1. Header Banner */}
      <div className="p-6 bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 text-white rounded-2xl shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-5 border border-slate-700/50">
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 bg-blue-500/20 text-blue-300 border border-blue-400/30 text-[11px] font-bold rounded-md tracking-wider uppercase">
              Autonomous Control Tower
            </span>
            <span className="text-slate-400 text-xs">•</span>
            <span className="text-emerald-400 text-xs font-semibold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Live Dataset Connected ({metrics.activeSkuCount} SKUs)
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Command Center & Sales Intelligence
          </h1>
          <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
            Real-time unified executive dashboard monitoring 30-day velocity, revenue health, dark-store fulfillment, and automated MAP enforcement.
          </p>
        </div>

        {currentUser?.role !== 'Analyst' && (
          <div className="flex flex-wrap items-center gap-3">
            <button
              id="btn-trigger-briefing"
              onClick={() => onOpenEmailModal(undefined, undefined, 'live')}
              className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg shadow-sm flex items-center space-x-2 transition-all"
            >
              <Mail className="w-4 h-4" />
              <span>1-Click WBR Email</span>
            </button>

            {onNavigateToView && (
              <button
                onClick={() => onNavigateToView('dataset-sync')}
                className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200 text-xs font-semibold rounded-lg flex items-center space-x-1.5 transition-colors"
              >
                <Building2 className="w-4 h-4 text-slate-400" />
                <span>Dataset & Live Sync</span>
              </button>
            )}
          </div>
        )}
      </div>

      {/* 2. Executive KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">30D Gross Revenue</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className={`text-2xl font-black ${currentUser?.role === 'Analyst' ? 'text-slate-400 text-base font-semibold' : 'text-slate-900'}`}>
              {currentUser?.role === 'Analyst' ? '🔒 Restricted (Owner Only)' : formatINR(metrics.total30dSales, { abbreviate: true })}
            </span>
            {currentUser?.role !== 'Analyst' && (
              <span className="text-xs font-bold text-emerald-600 flex items-center">
                <ArrowUpRight className="w-3.5 h-3.5" /> +14.2%
              </span>
            )}
          </div>
          <p className="text-[11px] text-slate-500">Across {metrics.activeSkuCount} active SKU lines</p>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">30D Units Dispatched</span>
            <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Package className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-black text-slate-900">{metrics.totalUnitsSold.toLocaleString('en-IN')}</span>
            <span className="text-xs font-bold text-slate-500">units</span>
          </div>
          <p className="text-[11px] text-slate-500">Avg ASP: {formatINR(metrics.avgSellingPrice)}</p>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">MAP Compliance</span>
            <div className={`w-8 h-8 rounded-lg ${metrics.totalMapBreaches === 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'} flex items-center justify-center`}>
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-black text-slate-900">
              {metrics.totalMapBreaches === 0 ? '100%' : `${metrics.totalMapBreaches} Breaches`}
            </span>
          </div>
          <p className="text-[11px] text-slate-500">
            {metrics.totalMapBreaches > 0 ? 'Active unauthorized discounters detected' : 'Full price parity maintained'}
          </p>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Quick Commerce Stock</span>
            <div className={`w-8 h-8 rounded-lg ${metrics.lowStockCount === 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'} flex items-center justify-center`}>
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-black text-slate-900">
              {metrics.lowStockCount === 0 ? 'All Healthy' : `${metrics.lowStockCount} Starved`}
            </span>
          </div>
          <p className="text-[11px] text-slate-500">
            {formatINR(metrics.totalRevenueAtRisk, { abbreviate: true })} revenue protected via AI transfers
          </p>
        </div>
      </div>

      {/* Advertising & ROAS KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Blended 30D ROAS</span>
            <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-black text-indigo-700">{metrics.blendedRoas}x</span>
            <span className="text-xs font-bold text-emerald-600 flex items-center">
              <ArrowUpRight className="w-3.5 h-3.5" /> Target &gt;4.0x
            </span>
          </div>
          <p className="text-[11px] text-slate-500">Return on total ad spend across channels</p>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Average ACOS</span>
            <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Zap className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-black text-slate-900">{metrics.avgAcos}%</span>
          </div>
          <p className="text-[11px] text-slate-500">Ad cost of sales percentage</p>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Average TACOS</span>
            <div className="w-8 h-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
              <ShoppingBag className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-black text-slate-900">{metrics.avgTacos}%</span>
          </div>
          <p className="text-[11px] text-slate-500">Total ad cost of total revenue</p>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Ad Spend (30D)</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className={`text-2xl font-black ${currentUser?.role === 'Analyst' ? 'text-slate-400 text-base font-semibold' : 'text-slate-900'}`}>
              {currentUser?.role === 'Analyst' ? '🔒 Restricted (Owner Only)' : formatINR(metrics.totalAdSpend, { abbreviate: true })}
            </span>
          </div>
          <p className="text-[11px] text-slate-500">Synced from Sheet 1 AdCost column</p>
        </div>
      </div>

      {/* 3. Interactive Sales Intelligence & SKU Assortment Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        {/* Table Controls */}
        <div className="p-4 border-b border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-3 bg-slate-50/50">
          <div className="flex items-center space-x-2">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Active Assortment Performance</h2>
            <span className="px-2 py-0.5 bg-blue-100 text-blue-800 text-[10px] font-bold rounded">
              {filteredSkus.length} of {skus.length} SKUs
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            {/* Search Input */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search SKU or name..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 pr-3 py-1.5 bg-white border border-slate-200 text-xs rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 w-48 text-slate-800 placeholder-slate-400"
              />
            </div>

            {/* Category Filter */}
            {categories.length > 0 && (
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-2.5 py-1.5 bg-white border border-slate-200 text-xs rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 text-slate-700 font-medium"
              >
                <option value="all">All Categories</option>
                {categories.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            )}

            {/* Sort Options */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="px-2.5 py-1.5 bg-white border border-slate-200 text-xs rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 text-slate-700 font-medium"
            >
              <option value="sales">Sort: Highest Sales</option>
              <option value="velocity">Sort: Highest Velocity</option>
              <option value="stock">Sort: Lowest Stock (Risk)</option>
              <option value="margin">Sort: Highest Margin</option>
            </select>
          </div>
        </div>

        {/* Table View */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-100 text-slate-600 uppercase text-[10px] font-bold border-b border-slate-200 tracking-wider">
              <tr>
                <th className="py-3 px-4">SKU & Product</th>
                <th className="py-3 px-3">Category</th>
                <th className="py-3 px-3 text-right">Selling Price</th>
                <th className="py-3 px-3 text-right">Daily Velocity</th>
                <th className="py-3 px-3 text-right">30D Units</th>
                <th className="py-3 px-4 text-right">30D Gross Revenue</th>
                <th className="py-3 px-3 text-right">ROAS / ACOS</th>
                <th className="py-3 px-3 text-right">Ad Spend</th>
                <th className="py-3 px-3 text-center">Dark Store Stock</th>
                {currentUser?.role !== 'Analyst' && (
                  <th className="py-3 px-4 text-center">Action</th>
                )}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredSkus.map((s) => {
                const sales = s.grossSales30d || (s.sellingPrice * (s.dailyVelocity || 50) * 30);
                const units = s.unitsSold30d || (s.dailyVelocity || 50) * 30;
                const isLowStock = (s.darkStoreStock ?? 15) < 10;
                const isMapBreach = s.sellingPrice < s.targetMap;

                return (
                  <tr key={s.sku} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4">
                      <div>
                        <div className="font-bold text-slate-900">{s.name}</div>
                        <div className="flex items-center space-x-2 mt-0.5">
                          <span className="font-mono text-[10px] text-slate-500 font-semibold">{s.sku}</span>
                          {s.brand && (
                            <span className="text-[10px] text-blue-700 bg-blue-50 px-1 rounded border border-blue-100">
                              {s.brand}
                            </span>
                          )}
                          {isMapBreach && (
                            <span className="text-[10px] text-amber-700 bg-amber-50 px-1 rounded border border-amber-200 font-bold">
                              MAP Breach
                            </span>
                          )}
                        </div>
                      </div>
                    </td>

                    <td className="py-3 px-3 text-slate-600">
                      {s.productType || s.category || 'General Assortment'}
                    </td>

                    <td className="py-3 px-3 text-right font-mono font-semibold text-slate-900">
                      {formatINR(s.sellingPrice)}
                    </td>

                    <td className="py-3 px-3 text-right font-mono text-slate-700">
                      {s.dailyVelocity || 50} / day
                    </td>

                    <td className="py-3 px-3 text-right font-mono text-slate-700">
                      {units.toLocaleString('en-IN')}
                    </td>

                    <td className="py-3 px-4 text-right font-mono font-bold text-slate-900">
                      {currentUser?.role === 'Analyst' ? <span className="text-xs font-semibold text-slate-400">🔒 Restricted</span> : formatINR(sales, { abbreviate: true })}
                    </td>

                    <td className="py-3 px-3 text-right font-mono">
                      <div className="font-bold text-indigo-700">{s.roas !== undefined ? `${s.roas}x` : '4.20x'}</div>
                      <div className="text-[10px] text-slate-500">{s.acos !== undefined ? `ACOS: ${s.acos}%` : 'ACOS: 18%'}</div>
                    </td>

                    <td className="py-3 px-3 text-right font-mono font-semibold text-slate-900">
                      {currentUser?.role === 'Analyst' ? <span className="text-xs font-semibold text-slate-400">🔒 Restricted</span> : formatINR(s.adCost30d ?? Math.round(sales * 0.12))}
                    </td>

                    <td className="py-3 px-3 text-center">
                      {(() => {
                        const skuStores = darkStores.filter(d => d.sku?.toLowerCase() === s.sku.toLowerCase());
                        const lowStores = skuStores.filter(d => (d.availableStock ?? 15) < 10);
                        const isStockLow = (s.darkStoreStock ?? 15) < 10 || s.stockStatus === 'Low Stock' || lowStores.length > 0;
                        return (
                          <div className="flex flex-col items-center">
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                              isStockLow
                                ? 'bg-red-100 text-red-800 border-red-200 animate-pulse'
                                : 'bg-emerald-50 text-emerald-800 border-emerald-200'
                            }`}>
                              {(s.darkStoreStock ?? 15).toLocaleString('en-IN')} units
                            </span>
                            {isStockLow && (
                              <span className="text-[9px] text-rose-600 font-bold mt-0.5 max-w-[140px] truncate" title={lowStores.length > 0 ? `Low stock at: ${lowStores.map(ds => `${ds.storeName} (${ds.availableStock}u)`).join(', ')}` : `Low Total Stock`}>
                                {lowStores.length > 0 ? `Low: ${lowStores[0].storeName.replace(/Pod.*|Hub.*/g, '').trim()} (${lowStores[0].availableStock}u)` : `Low Total Stock (${s.darkStoreStock}u)`}
                                {lowStores.length > 1 ? ` +${lowStores.length - 1}` : ''}
                              </span>
                            )}
                          </div>
                        );
                      })()}
                    </td>

                    {currentUser?.role !== 'Analyst' && (
                      <td className="py-3 px-4 text-center">
                        <div className="flex items-center justify-center space-x-1.5">
                          <button
                            onClick={() => onOpenStockTransfer(s.sku, s.defaultMotherHub || 'Central Hub', s.transferUnitsSuggested || Math.max(20, Math.round((s.dailyVelocity || 30) * 2)))}
                            className="px-2 py-1 bg-amber-600 hover:bg-amber-700 text-white text-[11px] font-bold rounded shadow-2xs transition-colors flex items-center space-x-1"
                            title="Initiate Mother Hub Stock Transfer"
                          >
                            <Zap className="w-3 h-3" />
                            <span>Transfer</span>
                          </button>
                          <button
                            onClick={() => onOpenEmailModal(undefined, s, 'live')}
                            className="px-2 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold rounded border border-slate-200 transition-colors"
                            title="View Live Briefing & Email Dispatch"
                          >
                            Briefing
                          </button>
                        </div>
                      </td>
                    )}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
