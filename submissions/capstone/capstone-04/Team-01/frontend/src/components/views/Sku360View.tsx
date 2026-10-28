import React from 'react';
import {
  Box,
  Building,
  Calendar,
  DollarSign,
  TrendingUp,
  Store,
  Truck,
  Mail,
  Search,
  Star,
  ShieldCheck,
  AlertTriangle,
  Sparkles,
  ArrowRight,
  Clock,
  Layers,
  Database
} from 'lucide-react';
import { SKUListing, MarketplaceId } from '../../types';
import { formatINR, formatPercent, MOTHER_HUBS, OWNER_EMAIL } from '../../data/mockData';
import { useData } from '../../context/DataContext';

interface Sku360ViewProps {
  selectedSkuId: string;
  onSelectSkuId: (id: string) => void;
  onOpenStockTransfer: (sku: string, hub: string, units?: number) => void;
  onOpenEmailModal: (sku: SKUListing) => void;
}

export const Sku360View: React.FC<Sku360ViewProps> = ({
  selectedSkuId,
  onSelectSkuId,
  onOpenStockTransfer,
  onOpenEmailModal
}) => {
  const { skus } = useData();
  const [activeTab, setActiveTab] = React.useState<'overview' | 'supply_chain' | 'pricing' | 'search' | 'reviews'>('overview');

  if (!skus || skus.length === 0) {
    return (
      <div className="p-8 bg-white border border-slate-200 rounded-xl text-center space-y-3">
        <Database className="w-8 h-8 text-slate-400 mx-auto" />
        <h3 className="font-bold text-slate-800 text-sm">No SKUs Loaded in Catalog</h3>
        <p className="text-xs text-slate-500">Connect your Google Sheet or upload an Excel file from the top bar to inspect 360-degree SKU intelligence.</p>
      </div>
    );
  }

  // Find in dynamic dataset
  const currentSku = skus.find((s) => s.sku === selectedSkuId || s.id === selectedSkuId) || skus[0];

  // Dynamic marketplace prices fallback
  const marketplaceEntries = currentSku.marketplacePrices
    ? Object.entries(currentSku.marketplacePrices)
    : [
        ['amazon', { price: currentSku.sellingPrice, inStock: (currentSku.darkStoreStock ?? 10) > 0, shareOfSearch: currentSku.shareOfSearchPercent || 42, revenue30d: Math.round((currentSku.grossSales30d || (currentSku.sellingPrice * 50)) * 0.45) }],
        ['blinkit', { price: currentSku.sellingPrice, inStock: (currentSku.darkStoreStock ?? 10) > 0, shareOfSearch: currentSku.shareOfSearchPercent || 38, revenue30d: Math.round((currentSku.grossSales30d || (currentSku.sellingPrice * 50)) * 0.25) }],
        ['zepto', { price: currentSku.sellingPrice, inStock: (currentSku.darkStoreStock ?? 10) > 0, shareOfSearch: 35, revenue30d: Math.round((currentSku.grossSales30d || (currentSku.sellingPrice * 50)) * 0.18) }],
        ['flipkart', { price: currentSku.sellingPrice, inStock: true, shareOfSearch: 30, revenue30d: Math.round((currentSku.grossSales30d || (currentSku.sellingPrice * 50)) * 0.12) }]
      ];

  const batches = currentSku.batches && currentSku.batches.length > 0
    ? currentSku.batches
    : [
        {
          batchNumber: `LOT-${currentSku.sku.replace(/[^a-zA-Z0-9]/g, '')}-2026A`,
          skuId: currentSku.sku,
          productName: currentSku.name,
          manufacturerName: currentSku.manufacturerName || 'Production Facility',
          manufacturerPlant: currentSku.manufacturerPlant || 'Central Unit',
          mfgDate: '2026-02-15',
          expiryDate: '2028-02-15',
          daysRemaining: 720,
          shelfLifeHealthPercent: 95,
          inventoryUnits: (currentSku.darkStoreStock || 0) + (currentSku.motherHubStock || 5000),
          inventoryValueInr: ((currentSku.darkStoreStock || 0) + (currentSku.motherHubStock || 5000)) * currentSku.sellingPrice,
          status: 'Fresh' as const
        }
      ];

  return (
    <div id="sku-360-view" className="space-y-6">
      
      {/* Top SKU Selector & Quick Search */}
      <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3 w-full md:w-auto">
          <div className="w-10 h-10 rounded-lg bg-blue-50 border border-blue-200 text-blue-700 flex items-center justify-center font-bold">
            <Box className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold text-slate-500 block">Active SKU 360 Inspection</span>
            <select
              id="sku-selector-dropdown"
              value={currentSku.sku}
              onChange={(e) => onSelectSkuId(e.target.value)}
              className="font-bold text-sm text-slate-900 bg-slate-50 border border-slate-300 rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer max-w-sm"
            >
              {skus.map((s) => (
                <option key={s.sku} value={s.sku} className="text-slate-900">
                  {s.sku} - {s.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center space-x-2.5 w-full md:w-auto justify-end">
          <button
            onClick={() => onOpenStockTransfer(currentSku.sku, currentSku.defaultMotherHub, Math.max(20, Math.round((currentSku.dailyVelocity || 40) * 2)))}
            className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
          >
            <Truck className="w-3.5 h-3.5" />
            <span>Transfer from Mother Hub</span>
          </button>
          <button
            onClick={() => onOpenEmailModal(currentSku)}
            className="px-3.5 py-2 bg-slate-50 hover:bg-slate-100 border border-slate-300 text-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1.5 transition-colors"
          >
            <Mail className="w-3.5 h-3.5 text-emerald-600" />
            <span>Email SKU Dossier</span>
          </button>
        </div>
      </div>

      {/* Main SKU Summary Header Card */}
      <div className="p-6 bg-white border border-slate-200 rounded-xl shadow-xs space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 font-mono text-xs font-bold rounded">
                {currentSku.sku}
              </span>
              <span className="px-2 py-0.5 bg-slate-100 text-slate-700 border border-slate-200 text-xs font-medium rounded">
                {currentSku.category}
              </span>
              <span className={`px-2 py-0.5 text-xs font-bold rounded border ${
                currentSku.stockStatus === 'Active'
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  : 'bg-rose-50 text-rose-700 border border-rose-200'
              }`}>
                {currentSku.stockStatus}
              </span>
            </div>
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">{currentSku.name}</h2>
            <p className="text-xs text-slate-500">
              Brand: <strong className="text-slate-800">{currentSku.brand}</strong> &bull; Subcategory: {currentSku.subcategory}
            </p>
          </div>

          <div className="flex items-center space-x-6">
            <div>
              <span className="text-[10px] text-slate-500 uppercase font-bold block">Selling Price</span>
              <span className="text-base font-bold text-slate-900">{formatINR(currentSku.sellingPrice)}</span>
              <span className="text-[10px] text-slate-500 block">MRP: {formatINR(currentSku.mrp)}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-500 uppercase font-bold block">30D Gross Sales</span>
              <span className="text-base font-bold text-blue-700">{formatINR(currentSku.grossSales30d, { abbreviate: true })}</span>
              <span className="text-[10px] text-slate-500 block">{currentSku.unitsSold30d} units sold</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-500 uppercase font-bold block">Shelf Health</span>
              <span className="text-base font-bold text-emerald-700">{currentSku.digitalShelfScore}/100</span>
              <span className="text-[10px] text-slate-500 block">★ {currentSku.rating} ({currentSku.reviewCount})</span>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center space-x-2 border-b border-slate-100 overflow-x-auto">
          {[
            { id: 'overview' as const, label: 'Cross-Channel Overview' },
            { id: 'supply_chain' as const, label: 'Supply Chain, Hubs & Batches' },
            { id: 'pricing' as const, label: 'Price & MAP Breaches' },
            { id: 'search' as const, label: 'Search Rank & Visibility' },
            { id: 'reviews' as const, label: 'Customer VOC & Defects' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2.5 text-xs font-bold transition-all border-b-2 -mb-px whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-blue-600 text-blue-700'
                  : 'border-transparent text-slate-500 hover:text-slate-900'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab 1: Overview */}
        {activeTab === 'overview' && (
          <div className="space-y-4 pt-2">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Marketplace Presence & Buy Box Status
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {marketplaceEntries.map(([channel, data]: [string, any]) => (
                <div key={channel} className="p-3.5 bg-slate-50 border border-slate-200 rounded-lg space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900 uppercase">{channel}</span>
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold border ${
                      data.inStock ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'
                    }`}>
                      {data.inStock ? 'In Stock' : 'OOS'}
                    </span>
                  </div>
                  <div className="flex justify-between items-baseline">
                    <span className="text-slate-500">Live Price:</span>
                    <span className="font-bold text-slate-900">{formatINR(data.price)}</span>
                  </div>
                  <div className="flex justify-between items-baseline">
                    <span className="text-slate-500">30D Revenue:</span>
                    <span className="font-bold text-blue-700">{formatINR(data.revenue30d, { abbreviate: true })}</span>
                  </div>
                  <div className="flex justify-between items-baseline">
                    <span className="text-slate-500">Share of Search:</span>
                    <span className="font-semibold text-slate-700">{data.shareOfSearch}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 2: Supply Chain & Perishables */}
        {activeTab === 'supply_chain' && (
          <div className="space-y-4 pt-2">
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="space-y-2">
                <h4 className="font-bold text-slate-900 flex items-center space-x-1.5">
                  <Building className="w-4 h-4 text-slate-500" />
                  <span>Manufacturing Facility</span>
                </h4>
                <div className="p-3 bg-white border border-slate-200 rounded-md space-y-1">
                  <p className="font-bold text-slate-900">{currentSku.manufacturerName || 'Certified Production Facility'}</p>
                  <p className="text-slate-500 text-[11px]">{currentSku.manufacturerPlant || 'Central Industrial Area'}</p>
                </div>
              </div>

              <div className="space-y-2">
                <h4 className="font-bold text-slate-900 flex items-center space-x-1.5">
                  <Truck className="w-4 h-4 text-emerald-600" />
                  <span>Primary Mother Hub Reserves</span>
                </h4>
                <div className="p-3 bg-white border border-slate-200 rounded-md space-y-1">
                  <p className="font-bold text-slate-900">{currentSku.defaultMotherHub || 'Central Mother Hub'}</p>
                  <p className="text-emerald-700 font-bold text-xs">
                    {(currentSku.motherHubStock || 0).toLocaleString()} Available Reserve Units
                  </p>
                </div>
              </div>
            </div>

            {/* Batches Table */}
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                Manufacturing Batches & Expiry Health
              </h4>
              <div className="border border-slate-200 rounded-lg overflow-hidden">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 text-[11px] uppercase font-bold">
                    <tr>
                      <th className="py-2.5 px-3">Batch Number</th>
                      <th className="py-2.5 px-3">Mfg Date</th>
                      <th className="py-2.5 px-3">Expiry Date</th>
                      <th className="py-2.5 px-3">Days Remaining</th>
                      <th className="py-2.5 px-3">Units in Batch</th>
                      <th className="py-2.5 px-3">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {batches.map((b) => (
                      <tr key={b.batchNumber} className="hover:bg-slate-50 transition-colors">
                        <td className="py-2.5 px-3 font-mono font-bold text-slate-800">{b.batchNumber}</td>
                        <td className="py-2.5 px-3 text-slate-500">{b.mfgDate}</td>
                        <td className="py-2.5 px-3 text-slate-800 font-medium">{b.expiryDate}</td>
                        <td className="py-2.5 px-3 font-bold text-slate-900">{b.daysRemaining} days</td>
                        <td className="py-2.5 px-3 text-slate-700">{b.inventoryUnits.toLocaleString()}</td>
                        <td className="py-2.5 px-3">
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                            {b.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Pricing & MAP Breaches */}
        {activeTab === 'pricing' && (
          <div className="space-y-4 pt-2 text-xs">
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg flex items-center justify-between">
              <div>
                <span className="text-slate-500 uppercase font-bold text-[10px]">MAP Guardrail</span>
                <p className="text-base font-bold text-slate-900">{formatINR(currentSku.targetMap)}</p>
                <p className="text-[11px] text-slate-500">Minimum Advertised Price enforcement across all authorized 3P sellers</p>
              </div>
              <span className="px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold rounded">
                Compliant on 5 / 6 Channels
              </span>
            </div>
          </div>
        )}

        {/* Tab 4: Search Rank */}
        {activeTab === 'search' && (
          <div className="space-y-4 pt-2 text-xs">
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg flex items-center justify-between">
              <div>
                <span className="text-blue-700 uppercase font-bold text-[10px]">Category Share of Search</span>
                <p className="text-base font-bold text-blue-900">{currentSku.shareOfSearchPercent}%</p>
                <p className="text-[11px] text-slate-600">Ranked #1 on "mineral sunscreen" and #3 on "vitamin c serum"</p>
              </div>
            </div>
          </div>
        )}

        {/* Tab 5: Reviews */}
        {activeTab === 'reviews' && (
          <div className="space-y-4 pt-2 text-xs">
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg flex items-center justify-between">
              <div>
                <span className="text-slate-500 uppercase font-bold text-[10px]">Customer Sentiment Index</span>
                <p className="text-base font-bold text-emerald-700">88% Positive</p>
                <p className="text-[11px] text-slate-600">Top positive topic: Fast Absorption. Top defect topic: Dropper cap courier leakage.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
