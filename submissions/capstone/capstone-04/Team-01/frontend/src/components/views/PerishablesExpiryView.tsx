import React from 'react';
import {
  CalendarClock,
  AlertTriangle,
  CheckCircle,
  Tag,
  Building,
  Calendar,
  Clock,
  Zap,
  Filter,
  ShieldCheck
} from 'lucide-react';
import { BatchPerishableInfo } from '../../types';
import { formatINR } from '../../data/mockData';
import { useData } from '../../context/DataContext';

interface PerishablesExpiryViewProps {
  onOpenEmailModal: () => void;
  onOpenStockTransfer: (sku: string, hub: string) => void;
}

export const PerishablesExpiryView: React.FC<PerishablesExpiryViewProps> = ({
  onOpenEmailModal,
  onOpenStockTransfer
}) => {
  const { skus } = useData();
  const [statusFilter, setStatusFilter] = React.useState<'all' | 'Fresh' | 'Expiring Soon' | 'Critical'>('all');

  const dynamicBatches: BatchPerishableInfo[] = skus.map((s, idx) => {
    const isCritical = s.darkStoreStock < 5;
    const isExpiring = !isCritical && idx % 3 === 0;
    const status = isCritical ? 'Critical' : isExpiring ? 'Expiring Soon' : 'Fresh';
    const totalUnits = s.darkStoreStock + s.motherHubStock;
    const inventoryVal = totalUnits * s.sellingPrice;
    const daysRemaining = isCritical ? 24 : isExpiring ? 75 : 210;
    const healthPercent = isCritical ? 20 : isExpiring ? 50 : 88;

    return {
      batchNumber: `LOT-2026-${s.sku.replace(/[^0-9]/g, '') || String(idx + 1).padStart(2, '0')}`,
      skuId: s.sku,
      productName: s.name,
      manufacturerName: s.manufacturerName || 'Agile Life Sciences & Sleep Corp',
      manufacturerPlant: s.manufacturerPlant || 'Peenya Industrial Area, Bengaluru Plant-02',
      mfgDate: '2026-02-10',
      expiryDate: isCritical ? '2026-09-15' : '2027-02-15',
      daysRemaining,
      shelfLifeHealthPercent: healthPercent,
      inventoryUnits: totalUnits,
      inventoryValueInr: inventoryVal,
      status: status as 'Fresh' | 'Expiring Soon' | 'Critical',
      recommendedAction: isCritical
        ? `Execute immediate stock replenishment of ${s.sku} from Nelamangala Mother Hub to Blinkit HSR-04 Pod.`
        : isExpiring
        ? `Deploy 15% quick-commerce clearance promo on Zepto / Swiggy Instamart to clear inventory within 45 days.`
        : `Normal FEFO batch rotation compliant. Zero write-off risk.`
    };
  });

  const filteredBatches = dynamicBatches.filter((b) => {
    if (statusFilter !== 'all' && b.status !== statusFilter) return false;
    return true;
  });

  const criticalBatches = dynamicBatches.filter((b) => b.status === 'Critical');
  const expiringSoonBatches = dynamicBatches.filter((b) => b.status === 'Expiring Soon');
  const totalValue = dynamicBatches.reduce((sum, b) => sum + b.inventoryValueInr, 0);

  return (
    <div id="perishables-expiry-view" className="space-y-6">
      
      {/* Overview Banner */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Perishables & Batch Expiry Intelligence</h2>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold rounded">
              FEFO Enabled
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Batch-level manufacturing and expiry tracking to eliminate expired write-offs via automated quick commerce clearance
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-center">
            <span className="text-[10px] uppercase font-bold text-slate-500 block">Total Monitored Value</span>
            <span className="text-sm font-bold text-slate-900">{formatINR(totalValue, { abbreviate: true })}</span>
          </div>
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-center">
            <span className="text-[10px] uppercase font-bold text-rose-700 block">Critical Batches (&lt;30d)</span>
            <span className="text-sm font-bold text-rose-600">{criticalBatches.length} Batches</span>
          </div>
          <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg text-center">
            <span className="text-[10px] uppercase font-bold text-amber-800 block">Expiring Soon (&lt;90d)</span>
            <span className="text-sm font-bold text-amber-700">{expiringSoonBatches.length} Batches</span>
          </div>
        </div>
      </div>

      {/* Filter Chips */}
      <div className="flex items-center space-x-2 bg-white p-3.5 border border-slate-200 rounded-xl shadow-xs text-xs">
        <span className="font-semibold text-slate-600 flex items-center space-x-1">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <span>Filter Status:</span>
        </span>
        {(['all', 'Fresh', 'Expiring Soon', 'Critical'] as const).map((st) => (
          <button
            key={st}
            onClick={() => setStatusFilter(st)}
            className={`px-3 py-1 rounded-md font-medium transition-all ${
              statusFilter === st
                ? 'bg-blue-600 text-white shadow-2xs'
                : 'bg-slate-100 border border-slate-200 text-slate-700 hover:bg-slate-200'
            }`}
          >
            {st === 'all' ? 'All Batches' : st}
          </button>
        ))}
      </div>

      {/* Batch Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredBatches.map((batch) => {
          const isCritical = batch.status === 'Critical';
          const isExpiring = batch.status === 'Expiring Soon';

          return (
            <div
              key={batch.batchNumber}
              className={`p-5 bg-white rounded-xl border shadow-xs space-y-3.5 ${
                isCritical
                  ? 'border-rose-300 ring-1 ring-rose-100'
                  : isExpiring
                  ? 'border-amber-300'
                  : 'border-slate-200'
              }`}
            >
              {/* Batch Header */}
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-slate-800 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded">
                  {batch.batchNumber}
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${
                  isCritical
                    ? 'bg-rose-100 text-rose-700 border-rose-200 animate-pulse'
                    : isExpiring
                    ? 'bg-amber-100 text-amber-800 border-amber-200'
                    : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                }`}>
                  {batch.status}
                </span>
              </div>

              {/* Product Info */}
              <div>
                <h4 className="text-xs font-bold text-slate-900 leading-tight">{batch.productName}</h4>
                <p className="text-[10px] text-slate-500 font-mono mt-0.5">{batch.skuId}</p>
              </div>

              {/* Manufacturer & Plant */}
              <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-1">
                <div className="flex items-center space-x-1.5 text-slate-700 text-[11px]">
                  <Building className="w-3.5 h-3.5 text-slate-500" />
                  <span className="font-bold text-slate-900">{batch.manufacturerName}</span>
                </div>
                <p className="text-[10px] text-slate-500 pl-5">{batch.manufacturerPlant}</p>
              </div>

              {/* Dates & Shelf Life Progress */}
              <div className="space-y-2 text-xs">
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-500">Mfg: {batch.mfgDate}</span>
                  <span className="font-bold text-slate-800">Exp: {batch.expiryDate}</span>
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between text-[10px]">
                    <span className="text-slate-500">Shelf Life Remaining:</span>
                    <span className={`font-bold ${isCritical ? 'text-rose-600' : isExpiring ? 'text-amber-700' : 'text-emerald-700'}`}>
                      {batch.daysRemaining} Days ({batch.shelfLifeHealthPercent}%)
                    </span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        isCritical
                          ? 'bg-rose-500'
                          : isExpiring
                          ? 'bg-amber-500'
                          : 'bg-emerald-500'
                      }`}
                      style={{ width: `${batch.shelfLifeHealthPercent}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Value & Units */}
              <div className="flex justify-between text-xs pt-2 border-t border-slate-100">
                <div>
                  <span className="text-[10px] text-slate-500 block">Inventory Units:</span>
                  <span className="font-bold text-slate-800">{batch.inventoryUnits.toLocaleString()}</span>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-slate-500 block">Inventory Value:</span>
                  <span className="font-bold text-slate-900">{formatINR(batch.inventoryValueInr)}</span>
                </div>
              </div>

              {/* Recommended Action */}
              {batch.recommendedAction && (
                <div className="p-2.5 bg-blue-50/70 border border-blue-200 rounded-lg text-[11px] space-y-1 text-slate-700">
                  <div className="font-bold text-blue-900 flex items-center space-x-1">
                    <Zap className="w-3 h-3 text-blue-600" />
                    <span>Autonomous FEFO Playbook:</span>
                  </div>
                  <p className="leading-snug text-slate-700">{batch.recommendedAction}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
