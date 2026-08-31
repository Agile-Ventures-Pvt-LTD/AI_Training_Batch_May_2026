import React from 'react';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  ShoppingCart,
  Percent,
  AlertTriangle,
  Zap,
  Building2,
  Truck,
  Mail,
  ArrowRight,
  ShieldAlert,
  Sparkles,
  BarChart3,
  Calendar,
  CheckCircle2
} from 'lucide-react';
import { MarketplaceId, UserRole, AlertAnomaly } from '../../types';
import {
  formatINR,
  formatPercent,
  HISTORICAL_CHART_DATA,
  MARKETPLACE_CONFIGS,
  OWNER_EMAIL
} from '../../data/mockData';
import { useData } from '../../context/DataContext';

interface ExecutiveTowerViewProps {
  selectedChannel: MarketplaceId | 'all';
  onNavigateView: (viewId: any) => void;
  onOpenEmailModal: (anomaly?: any) => void;
  onOpenStockTransfer: (sku: string, hub: string) => void;
  onSelectSku: (skuId: string) => void;
}

export const ExecutiveTowerView: React.FC<ExecutiveTowerViewProps> = ({
  selectedChannel,
  onNavigateView,
  onOpenEmailModal,
  onOpenStockTransfer,
  onSelectSku
}) => {
  const { skus, alerts, mapBreaches, darkStores } = useData();

  // Aggregate Metrics derived dynamically from dataset
  const grossSalesTotal = skus.reduce((sum, s) => sum + (s.grossSales30d || (s.sellingPrice * (s.unitsSold30d || 50))), 0) || 0;
  const netSalesTotal = Math.round(grossSalesTotal * 0.92);
  const totalAdSpend = Math.round(grossSalesTotal * 0.072);
  const blendedRoas = totalAdSpend > 0 ? (grossSalesTotal / totalAdSpend).toFixed(2) : '0.00';
  const quickCommercePenetration = 36.5;
  const revenueAtRisk = alerts.reduce((acc, a) => acc + (a.revenueAtRiskInr || 0), 0);
  const recoveredRevenue = Math.round(grossSalesTotal * 0.2);
  const oosSkusCount = skus.filter((s) => s.stockStatus === 'Out Of Stock' || s.darkStoreStock === 0).length;
  const darkStoreOosRate = skus.length > 0 ? Number(((oosSkusCount / skus.length) * 100).toFixed(1)) : 0;
  const activeMapBreaches = mapBreaches.length;

  // Primary Urgent Anomaly Alert from real dynamic state
  const primaryAnomaly: AlertAnomaly | undefined = alerts.find(a => a.severity === 'Critical') || alerts[0];
  const primarySku = primaryAnomaly ? skus.find(s => s.sku === primaryAnomaly.sku) : skus[0];

  return (
    <div id="executive-tower-container" className="space-y-6">
      
      {/* Top Banner: Urgent Anomaly Alert with Supply Chain Solution */}
      {primaryAnomaly ? (
        <div className="p-5 bg-white text-slate-900 rounded-xl border border-red-200 shadow-xs flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
          <div className="flex items-start space-x-3.5">
            <div className="w-10 h-10 rounded-lg bg-red-100 text-red-600 border border-red-200 flex items-center justify-center shrink-0 mt-0.5 shadow-2xs animate-pulse">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <div className="space-y-1">
              <div className="flex items-center space-x-2">
                <span className="px-2 py-0.5 bg-red-600 text-white text-[10px] font-bold rounded uppercase tracking-wider">
                  {primaryAnomaly.severity} Anomaly Triggered
                </span>
                <span className="text-xs font-semibold text-blue-700">
                  {primaryAnomaly.productName} ({primaryAnomaly.sku}) on {primaryAnomaly.marketplace.toUpperCase()}
                </span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed max-w-3xl">
                {primaryAnomaly.summary}
                {primaryAnomaly.motherHubName && (
                  <span className="ml-1">
                    <strong className="text-emerald-700 font-bold">Follow-Up Solution:</strong> {primaryAnomaly.motherHubName} holds <strong className="text-slate-900 font-bold">{(primaryAnomaly.motherHubStock || 1500).toLocaleString()} fresh units</strong>.
                  </span>
                )}
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center space-x-2.5 shrink-0 self-end lg:self-center">
            <button
              id="tower-topology-btn"
              onClick={() => onNavigateView('dark-stores-supply-chain')}
              className="px-3 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 text-xs font-bold rounded-lg flex items-center space-x-1.5 transition-colors"
            >
              <Building2 className="w-3.5 h-3.5" />
              <span>Interactive Topology Flow</span>
            </button>
            <button
              id="tower-transfer-btn"
              onClick={() => onOpenStockTransfer(primaryAnomaly.sku, primaryAnomaly.motherHubName || (primarySku?.defaultMotherHub || 'Mother Hub'))}
              className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-sm transition-colors"
            >
              <Truck className="w-3.5 h-3.5" />
              <span>Transfer {primaryAnomaly.transferUnitsSuggested || 250} Units from Hub</span>
            </button>
            <button
              id="tower-email-btn"
              onClick={() => onOpenEmailModal(primaryAnomaly)}
              className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
            >
              <Mail className="w-3.5 h-3.5" />
              <span>1-Click Auto-Send Email</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="p-4 bg-emerald-50 text-slate-900 rounded-xl border border-emerald-200 shadow-xs flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <CheckCircle2 className="w-4 h-4" />
            </div>
            <div>
              <p className="text-xs font-bold text-emerald-900">All Operations Synchronized & Healthy</p>
              <p className="text-[11px] text-emerald-700">Catalog of {skus.length} active SKUs running within safety stock thresholds.</p>
            </div>
          </div>
          <button
            onClick={() => onNavigateView('digital-shelf')}
            className="px-3 py-1.5 bg-emerald-600 text-white text-xs font-bold rounded-lg hover:bg-emerald-700 transition-colors"
          >
            Inspect Catalog &rarr;
          </button>
        </div>
      )}

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Gross Sales */}
        <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-2">
          <div className="flex items-center justify-between text-slate-500 text-xs">
            <span className="font-bold uppercase tracking-widest text-[10px]">30D Gross Brand Sales</span>
            <div className="p-1.5 bg-blue-50 text-blue-700 rounded-lg border border-blue-100">
              <DollarSign className="w-3.5 h-3.5" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-bold text-slate-900 tracking-tight">
              {formatINR(grossSalesTotal, { abbreviate: true })}
            </span>
            <span className="text-xs font-bold text-emerald-600 flex items-center">
              <TrendingUp className="w-3 h-3 mr-0.5" />
              +8.4% YoY
            </span>
          </div>
          <div className="text-[10px] text-slate-500 flex justify-between pt-2 border-t border-slate-100">
            <span>Net: {formatINR(netSalesTotal, { abbreviate: true })}</span>
            <span className="text-slate-600 font-medium">Target: ₹3.50Cr</span>
          </div>
        </div>

        {/* Quick Commerce Share */}
        <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-2">
          <div className="flex items-center justify-between text-slate-500 text-xs">
            <span className="font-bold uppercase tracking-widest text-[10px]">Quick Commerce Share</span>
            <div className="p-1.5 bg-amber-50 text-amber-700 rounded-lg border border-amber-100">
              <ShoppingCart className="w-3.5 h-3.5" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-bold text-slate-900 tracking-tight">
              {quickCommercePenetration}%
            </span>
            <span className="text-xs font-bold text-emerald-600 flex items-center">
              <TrendingUp className="w-3 h-3 mr-0.5" />
              +14.2% MoM
            </span>
          </div>
          <div className="text-[10px] text-slate-500 flex justify-between pt-2 border-t border-slate-100">
            <span>Blinkit + Zepto + Instamart</span>
            <span className="text-red-600 font-semibold">OOS: {darkStoreOosRate}%</span>
          </div>
        </div>

        {/* Blended ROAS */}
        <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-2">
          <div className="flex items-center justify-between text-slate-500 text-xs">
            <span className="font-bold uppercase tracking-widest text-[10px]">Blended ROAS / TACOS</span>
            <div className="p-1.5 bg-indigo-50 text-indigo-700 rounded-lg border border-indigo-100">
              <Percent className="w-3.5 h-3.5" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-bold text-slate-900 tracking-tight">
              {blendedRoas}x
            </span>
            <span className="text-xs font-medium text-slate-500">
              (TACOS 7.2%)
            </span>
          </div>
          <div className="text-[10px] text-slate-500 flex justify-between pt-2 border-t border-slate-100">
            <span>Spend: {formatINR(totalAdSpend, { abbreviate: true })}</span>
            <span className="text-emerald-700 font-semibold">QC ROAS: 7.05x</span>
          </div>
        </div>

        {/* Revenue at Risk vs Recovered */}
        <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-2 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-500 text-xs">
            <span className="font-bold uppercase tracking-widest text-[10px] text-slate-600">Revenue at Risk</span>
            <div className="p-1.5 bg-red-50 text-red-700 rounded-lg border border-red-100">
              <ShieldAlert className="w-3.5 h-3.5" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-bold text-red-600 tracking-tight">
              {formatINR(revenueAtRisk, { abbreviate: true })}
            </span>
            <span className="text-xs font-medium text-slate-500">
              Rec: {formatINR(recoveredRevenue, { abbreviate: true })}
            </span>
          </div>
          <div className="text-[10px] text-slate-500 flex justify-between pt-2 border-t border-slate-100">
            <span>4 Active Playbooks</span>
            <button
              onClick={() => onNavigateView('autonomous-actions')}
              className="text-blue-600 hover:underline font-semibold"
            >
              Review Actions &rarr;
            </button>
          </div>
          <div className="absolute bottom-0 left-0 h-1 bg-red-500 w-1/3"></div>
        </div>
      </div>

      {/* Main Charts & Pareto Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: 30-Day Multi-Channel Sales Trend */}
        <div className="lg:col-span-2 p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">30-Day Multi-Channel Revenue & Ad Velocity</h3>
              <p className="text-xs text-slate-500 mt-0.5">Daily gross sales vs ad spend across all 6 connected marketplaces</p>
            </div>
            <div className="flex items-center space-x-3 text-xs">
              <div className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-600" />
                <span className="text-slate-600 text-xs font-medium">Gross Sales</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                <span className="text-slate-600 text-xs font-medium">Ad Spend</span>
              </div>
            </div>
          </div>

          {/* SVG Bar / Area Visualizer */}
          <div className="h-56 w-full pt-4 flex items-end justify-between gap-1 border-b border-slate-100">
            {HISTORICAL_CHART_DATA.slice(-20).map((d, i) => {
              const maxSales = 1600000;
              const salesHeight = Math.min(100, Math.max(15, (d.grossSales / maxSales) * 100));
              const adHeight = Math.min(60, Math.max(8, (d.adSpend / 150000) * 100));

              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1 group relative h-full justify-end">
                  {/* Tooltip on hover */}
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity absolute bottom-full mb-2 bg-slate-900 border border-slate-800 text-white text-[10px] p-2.5 rounded-lg shadow-xl pointer-events-none z-20 whitespace-nowrap">
                    <p className="font-bold">{d.fullDate}</p>
                    <p>Gross: {formatINR(d.grossSales)}</p>
                    <p>Ad Spend: {formatINR(d.adSpend)}</p>
                    <p>ROAS: {d.roas}x</p>
                  </div>

                  <div className="w-full flex items-end justify-center gap-0.5 h-full">
                    {/* Gross Sales Bar */}
                    <div
                      className="w-1/2 bg-blue-600 group-hover:bg-blue-700 rounded-t-xs transition-all"
                      style={{ height: `${salesHeight}%` }}
                    />
                    {/* Ad Spend Bar */}
                    <div
                      className="w-1/2 bg-amber-500 group-hover:bg-amber-600 rounded-t-xs transition-all"
                      style={{ height: `${adHeight}%` }}
                    />
                  </div>
                  <span className="text-[9px] text-slate-400 font-mono rotate-45 origin-left mt-1">
                    {d.date}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Summary Row */}
          <div className="grid grid-cols-3 gap-3 pt-2 text-center text-xs">
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
              <span className="text-slate-500 block text-[10px]">Average Daily Revenue</span>
              <span className="font-bold text-slate-900">{formatINR(1222266)}</span>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
              <span className="text-slate-500 block text-[10px]">Avg Quick Commerce ROAS</span>
              <span className="font-bold text-emerald-700">7.05x</span>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
              <span className="text-slate-500 block text-[10px]">Share of Search in Category</span>
              <span className="font-bold text-blue-700">24.8%</span>
            </div>
          </div>
        </div>

        {/* Right 1 Col: Marketplace Performance Pareto */}
        <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-4 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Channel Revenue Pareto</h3>
                <p className="text-xs text-slate-500">Live share across 6 channels</p>
              </div>
              <span className="text-[10px] font-mono bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full border border-emerald-200 font-bold">
                Live Feed
              </span>
            </div>

            <div className="space-y-3">
              {MARKETPLACE_CONFIGS.map((m) => {
                const shares: Record<string, { pct: number; rev: number }> = {
                  amazon: { pct: 38.2, rev: 14007000 },
                  flipkart: { pct: 25.3, rev: 9277000 },
                  blinkit: { pct: 18.5, rev: 6783500 },
                  zepto: { pct: 11.2, rev: 4106800 },
                  myntra: { pct: 4.8, rev: 1760000 },
                  instamart: { pct: 2.0, rev: 733700 }
                };
                const item = shares[m.id] || { pct: 1.0, rev: 366000 };

                return (
                  <div key={m.id} className="space-y-1">
                    <div className="flex justify-between text-xs">
                      <div className="flex items-center space-x-1.5">
                        <span className="w-2 h-2 rounded-full" style={{ backgroundColor: m.color }} />
                        <span className="font-semibold text-slate-800">{m.name}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="font-bold text-slate-900">{formatINR(item.rev, { abbreviate: true })}</span>
                        <span className="text-[10px] text-slate-500">({item.pct}%)</span>
                      </div>
                    </div>
                    <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{ width: `${item.pct}%`, backgroundColor: m.color }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100">
            <button
              onClick={() => onNavigateView('sales-intelligence')}
              className="w-full py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 text-xs font-semibold rounded-lg flex items-center justify-center space-x-1.5 transition-colors"
            >
              <span>Deep-Dive Channel Unit Economics</span>
              <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
            </button>
          </div>
        </div>
      </div>

      {/* Hero SKUs & Top Revenue at Risk Table */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Live Catalog Health & Supply Chain Status</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Real-time monitoring of velocity, digital shelf score, dark store stock, and mother hub reserves
            </p>
          </div>
          <button
            onClick={() => onNavigateView('digital-shelf')}
            className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center space-x-1"
          >
            <span>View Full Catalog ({skus.length} SKUs)</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 text-slate-500 text-[10px] uppercase tracking-wider font-bold">
                <th className="py-3 px-3">SKU & Product Name</th>
                <th className="py-3 px-3">Target MAP / Price</th>
                <th className="py-3 px-3">30D Gross Sales</th>
                <th className="py-3 px-3">Digital Shelf Score</th>
                <th className="py-3 px-3">Dark Stores Stock</th>
                <th className="py-3 px-3">Mother Hub Reserves</th>
                <th className="py-3 px-3 text-right">Autonomous Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {skus.slice(0, 8).map((sku) => {
                const isOos = sku.darkStoreStock === 0 || sku.stockStatus === 'Out Of Stock';
                const isLow = !isOos && (sku.darkStoreStock < 5 || sku.stockStatus === 'Low Stock');

                return (
                  <tr key={sku.id || sku.sku} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-3">
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => onSelectSku(sku.sku || sku.id)}
                          className="font-bold text-slate-900 hover:text-blue-600 text-left"
                        >
                          {sku.name}
                        </button>
                      </div>
                      <div className="flex items-center space-x-2 text-[10px] text-slate-500 mt-0.5">
                        <span className="font-mono text-slate-600 font-bold">{sku.sku}</span>
                        <span>&bull;</span>
                        <span>{sku.category || 'Standard'}</span>
                        {sku.manufacturerName && (
                          <>
                            <span>&bull;</span>
                            <span>{sku.manufacturerName}</span>
                          </>
                        )}
                      </div>
                    </td>
                    <td className="py-3.5 px-3">
                      <div className="font-bold text-slate-900">{formatINR(sku.sellingPrice)}</div>
                      <div className="text-[10px] text-slate-500">MAP: {formatINR(sku.targetMap || sku.sellingPrice)}</div>
                    </td>
                    <td className="py-3.5 px-3">
                      <div className="font-bold text-slate-900">{formatINR(sku.grossSales30d || (sku.sellingPrice * (sku.unitsSold30d || 50)), { abbreviate: true })}</div>
                      <div className="text-[10px] text-slate-500">{sku.dailyVelocity || Math.round((sku.unitsSold30d || 50) / 30)} units/day</div>
                    </td>
                    <td className="py-3.5 px-3">
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          (sku.digitalShelfScore || 85) >= 85
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : (sku.digitalShelfScore || 85) >= 70
                            ? 'bg-blue-50 text-blue-700 border border-blue-200'
                            : 'bg-amber-50 text-amber-700 border border-amber-200'
                        }`}>
                          {sku.digitalShelfScore || 88}/100
                        </span>
                      </div>
                    </td>
                    <td className="py-3.5 px-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        isOos
                          ? 'bg-red-50 text-red-700 border border-red-200'
                          : isLow
                          ? 'bg-amber-50 text-amber-800 border border-amber-200'
                          : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                      }`}>
                        {isOos ? '0 Units (OOS)' : `${(sku.darkStoreStock ?? 10).toLocaleString()} Units`}
                      </span>
                    </td>
                    <td className="py-3.5 px-3">
                      <div className="font-bold text-slate-900">
                        {(sku.motherHubStock ?? 5000).toLocaleString()} Units
                      </div>
                      <div className="text-[10px] text-slate-500 truncate max-w-[160px]">
                        {sku.defaultMotherHub || 'Mother Hub'}
                      </div>
                    </td>
                    <td className="py-3.5 px-3 text-right">
                      {isOos || isLow ? (
                        <button
                          onClick={() => onOpenStockTransfer(sku.sku, sku.defaultMotherHub || 'Mother Hub')}
                          className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-[11px] font-semibold transition-colors shadow-2xs"
                        >
                          Transfer Units
                        </button>
                      ) : (
                        <button
                          onClick={() => onSelectSku(sku.sku || sku.id)}
                          className="px-3 py-1 bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 rounded-md text-[11px] font-medium transition-colors"
                        >
                          Inspect 360
                        </button>
                      )}
                    </td>
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
