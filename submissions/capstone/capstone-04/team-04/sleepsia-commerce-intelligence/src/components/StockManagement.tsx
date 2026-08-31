import React, { useState, useMemo } from 'react';
import {
  Boxes,
  AlertTriangle,
  CheckCircle2,
  TrendingDown,
  ArrowRight,
  RefreshCw,
  Search,
  Sliders,
  Building2,
  Truck,
  Package,
  Layers,
  ArrowUpDown,
  ShieldAlert,
  Zap,
  Check,
  X,
  Filter,
  Plus,
  Send,
} from 'lucide-react';
import { SleepsiaWorkbookData, InventoryRecord } from '../types/commerce';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface StockManagementProps {
  data: SleepsiaWorkbookData;
  selectedDate: string;
  onNavigateToTab?: (tab: string) => void;
  onUpdateInventory?: (updatedInventory: InventoryRecord[]) => void;
}

export const StockManagement: React.FC<StockManagementProps> = ({
  data,
  selectedDate,
  onNavigateToTab,
  onUpdateInventory,
}) => {
  // Alert Threshold State (default 30 units, user configurable)
  const [stockThreshold, setStockThreshold] = useState<number>(30);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedWarehouseFilter, setSelectedWarehouseFilter] = useState<string>('All');
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState<string>('All');
  const [statusFilter, setStatusFilter] = useState<'All' | 'Critical' | 'Warning' | 'Healthy'>('All');
  const [sortBy, setSortBy] = useState<'stock_asc' | 'stock_desc' | 'doi_asc' | 'sku'>('stock_asc');

  // Local inventory state for interactive transfers
  const [inventoryList, setInventoryList] = useState<InventoryRecord[]>(() => data.inventory);

  // Transfer Modal State
  const [isTransferModalOpen, setIsTransferModalOpen] = useState<boolean>(false);
  const [transferSource, setTransferSource] = useState<string>('Noida Mother DC');
  const [transferTarget, setTransferTarget] = useState<string>('');
  const [transferSku, setTransferSku] = useState<string>('');
  const [transferUnits, setTransferUnits] = useState<number>(50);
  const [transferSuccessMessage, setTransferSuccessMessage] = useState<string | null>(null);

  // Map product names & categories
  const productMap = useMemo(() => {
    const map = new Map<string, { name: string; category: string; mrp: number; cost: number }>();
    data.products.forEach((p) => {
      map.set(p.sku, { name: p.productName, category: p.category, mrp: p.mrp, cost: p.standardCost });
    });
    return map;
  }, [data.products]);

  // Extract unique darkstores and warehouses
  const allLocations = useMemo(() => {
    const locSet = new Set<string>();
    inventoryList.forEach((inv) => {
      if (inv.warehouse) locSet.add(inv.warehouse);
    });
    // Ensure standard darkstores if dataset has sparse names
    if (locSet.size < 4) {
      locSet.add('Blinkit Koramangala Hub (BLK-BGL-01)');
      locSet.add('Instamart Andheri West (INSTA-MUM-01)');
      locSet.add('Zepto Gurgaon Hub (ZEP-GGN-02)');
      locSet.add('Blinkit Indirapuram (BLK-NCR-03)');
      locSet.add('Noida Mother DC');
      locSet.add('Mumbai Mother DC');
    }
    return Array.from(locSet);
  }, [inventoryList]);

  // Darkstores vs Mother Warehouses classification
  const locationStats = useMemo(() => {
    return allLocations.map((loc) => {
      const isMotherDC = loc.toLowerCase().includes('mother') || loc.toLowerCase().includes('dc') || loc.toLowerCase().includes('central');
      const locRecords = inventoryList.filter((inv) => inv.warehouse === loc);

      const totalAvailable = locRecords.reduce((sum, r) => sum + (r.availableStock || r.closingStock || 0), 0);
      const totalInbound = locRecords.reduce((sum, r) => sum + (r.inboundStock || 0), 0);
      const totalReserved = locRecords.reduce((sum, r) => sum + (r.reservedStock || 0), 0);
      const totalDamaged = locRecords.reduce((sum, r) => sum + (r.damagedStock || 0), 0);

      const criticalSkus = locRecords.filter((r) => (r.availableStock || r.closingStock || 0) < stockThreshold);
      const warningSkus = locRecords.filter((r) => {
        const stock = r.availableStock || r.closingStock || 0;
        return stock >= stockThreshold && stock < stockThreshold * 2;
      });

      const avgDoi = locRecords.length > 0
        ? Math.round(locRecords.reduce((sum, r) => sum + (r.daysOfInventory || 8), 0) / locRecords.length)
        : 12;

      let health: 'Critical' | 'Warning' | 'Healthy' = 'Healthy';
      if (criticalSkus.length > 0) health = 'Critical';
      else if (warningSkus.length > 0) health = 'Warning';

      return {
        name: loc,
        isMotherDC,
        type: isMotherDC ? 'Regional Fulfillment Center' : 'Quick Commerce Darkstore (10-min)',
        totalAvailable,
        totalInbound,
        totalReserved,
        totalDamaged,
        skuCount: locRecords.length,
        criticalCount: criticalSkus.length,
        warningCount: warningSkus.length,
        criticalSkus,
        avgDoi,
        health,
      };
    });
  }, [allLocations, inventoryList, stockThreshold]);

  // Overall Global Threshold Alerts
  const globalCriticalRecords = useMemo(() => {
    return inventoryList.filter((inv) => (inv.availableStock || inv.closingStock || 0) < stockThreshold);
  }, [inventoryList, stockThreshold]);

  const globalWarningRecords = useMemo(() => {
    return inventoryList.filter((inv) => {
      const s = inv.availableStock || inv.closingStock || 0;
      return s >= stockThreshold && s < stockThreshold * 2;
    });
  }, [inventoryList, stockThreshold]);

  // Filtered Table Records
  const filteredRecords = useMemo(() => {
    return inventoryList
      .filter((inv) => {
        const prod = productMap.get(inv.sku);
        const name = prod?.name || inv.sku;
        const category = prod?.category || 'General';
        const stock = inv.availableStock || inv.closingStock || 0;

        // Search match
        const matchesSearch =
          inv.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
          name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          inv.warehouse.toLowerCase().includes(searchTerm.toLowerCase());

        // Warehouse filter
        const matchesWarehouse = selectedWarehouseFilter === 'All' || inv.warehouse === selectedWarehouseFilter;

        // Category filter
        const matchesCategory = selectedCategoryFilter === 'All' || category === selectedCategoryFilter;

        // Status filter
        let matchesStatus = true;
        if (statusFilter === 'Critical') matchesStatus = stock < stockThreshold;
        if (statusFilter === 'Warning') matchesStatus = stock >= stockThreshold && stock < stockThreshold * 2;
        if (statusFilter === 'Healthy') matchesStatus = stock >= stockThreshold * 2;

        return matchesSearch && matchesWarehouse && matchesCategory && matchesStatus;
      })
      .sort((a, b) => {
        const stockA = a.availableStock || a.closingStock || 0;
        const stockB = b.availableStock || b.closingStock || 0;
        const doiA = a.daysOfInventory || 10;
        const doiB = b.daysOfInventory || 10;

        if (sortBy === 'stock_asc') return stockA - stockB;
        if (sortBy === 'stock_desc') return stockB - stockA;
        if (sortBy === 'doi_asc') return doiA - doiB;
        if (sortBy === 'sku') return a.sku.localeCompare(b.sku);
        return 0;
      });
  }, [inventoryList, searchTerm, selectedWarehouseFilter, selectedCategoryFilter, statusFilter, sortBy, stockThreshold, productMap]);

  // Execute Stock Transfer Handler
  const handleExecuteTransfer = () => {
    if (!transferSku || !transferTarget || !transferSource) return;

    const updated = inventoryList.map((record) => {
      if (record.sku === transferSku && record.warehouse === transferSource) {
        return {
          ...record,
          availableStock: Math.max(0, (record.availableStock || record.closingStock || 0) - transferUnits),
          closingStock: Math.max(0, (record.closingStock || 0) - transferUnits),
        };
      }
      if (record.sku === transferSku && record.warehouse === transferTarget) {
        return {
          ...record,
          availableStock: (record.availableStock || record.closingStock || 0) + transferUnits,
          closingStock: (record.closingStock || 0) + transferUnits,
          daysOfInventory: Math.min(30, (record.daysOfInventory || 2) + Math.round(transferUnits / 10)),
          stockoutRisk: 'Low' as const,
        };
      }
      return record;
    });

    setInventoryList(updated);
    if (onUpdateInventory) {
      onUpdateInventory(updated);
    }

    const prodName = productMap.get(transferSku)?.name || transferSku;
    setTransferSuccessMessage(
      `Dispatched ${transferUnits} units of ${prodName} from ${transferSource} to ${transferTarget}. Alert updated!`
    );
    setIsTransferModalOpen(false);
    setTimeout(() => setTransferSuccessMessage(null), 5000);
  };

  const openTransferForRecord = (record: InventoryRecord) => {
    setTransferSku(record.sku);
    setTransferTarget(record.warehouse);
    setTransferSource('Noida Mother DC');
    setTransferUnits(Math.max(20, stockThreshold * 2 - (record.availableStock || 0)));
    setIsTransferModalOpen(true);
  };

  const categories = useMemo(() => {
    const cats = new Set<string>();
    data.products.forEach((p) => cats.add(p.category));
    return Array.from(cats);
  }, [data.products]);

  return (
    <div className="space-y-6">
      {/* 1. Header & Threshold Control Panel */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-lg bg-blue-50 text-blue-600 border border-blue-100">
                <Boxes className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  Darkstores &amp; Stocks Management Intelligence
                  <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-0.5 rounded-full">
                    {locationStats.length} Locations Active
                  </span>
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Real-time omnichannel stock surveillance, 10-minute darkstore replenishment, and automated buffer alerts.
                </p>
              </div>
            </div>
          </div>

          {/* Threshold Controller Widget */}
          <div className="flex items-center flex-wrap gap-3 bg-slate-50 border border-slate-200 p-2.5 rounded-xl">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700">
              <Sliders className="w-4 h-4 text-blue-600" />
              <span>Safety Threshold Alert:</span>
            </div>
            <div className="flex items-center gap-1">
              {[15, 25, 30, 50, 75, 100].map((t) => (
                <button
                  key={t}
                  onClick={() => setStockThreshold(t)}
                  className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-colors ${
                    stockThreshold === t
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  &lt;{t} units
                </button>
              ))}
            </div>
            <div className="flex items-center gap-1.5 pl-2 border-l border-slate-200 text-xs text-slate-500">
              <span>Custom:</span>
              <input
                type="number"
                min={1}
                max={500}
                value={stockThreshold}
                onChange={(e) => setStockThreshold(Math.max(1, parseInt(e.target.value) || 1))}
                className="w-14 px-2 py-0.5 text-xs font-bold bg-white border border-slate-200 rounded text-slate-900 outline-none focus:border-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Transfer Success Notification */}
      {transferSuccessMessage && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold p-3.5 rounded-xl flex items-center justify-between shadow-xs">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{transferSuccessMessage}</span>
          </div>
          <button onClick={() => setTransferSuccessMessage(null)} className="text-emerald-700 hover:text-emerald-900">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* 2. Real-Time Alert Banner if any Darkstore is below threshold */}
      {globalCriticalRecords.length > 0 ? (
        <div className="bg-gradient-to-r from-rose-500 via-rose-600 to-amber-600 text-white rounded-xl p-4 shadow-md flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-white/20 text-white shrink-0">
              <ShieldAlert className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="bg-white text-rose-700 text-[10px] font-black uppercase px-2 py-0.5 rounded tracking-wider">
                  ACTIVE STOCKOUT ALERT
                </span>
                <span className="text-xs font-bold text-rose-100">
                  Threshold: Below {stockThreshold} Units
                </span>
              </div>
              <h3 className="text-sm sm:text-base font-bold text-white mt-1">
                {globalCriticalRecords.length} Darkstore SKU Allocations Breached Safety Buffer!
              </h3>
              <p className="text-xs text-rose-100 mt-0.5">
                Quick-commerce darkstores in Bengaluru, NCR, and Mumbai require immediate intra-depot replenishment to avoid stockout cancellations.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={() => {
                setStatusFilter('Critical');
                setSortBy('stock_asc');
              }}
              className="bg-white text-rose-700 hover:bg-rose-50 text-xs font-bold px-3.5 py-2 rounded-lg transition-all shadow-xs flex items-center gap-1.5"
            >
              <Filter className="w-3.5 h-3.5" />
              Filter {globalCriticalRecords.length} Alerted SKUs
            </button>
            <button
              onClick={() => {
                if (globalCriticalRecords.length > 0) {
                  openTransferForRecord(globalCriticalRecords[0]);
                }
              }}
              className="bg-slate-900/90 hover:bg-slate-900 text-white text-xs font-bold px-3.5 py-2 rounded-lg transition-all border border-white/20 flex items-center gap-1.5"
            >
              <Truck className="w-3.5 h-3.5 text-amber-300" />
              Rebalance Stock
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl p-4 flex items-center justify-between shadow-xs">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <div>
              <h4 className="text-xs sm:text-sm font-bold text-emerald-900">
                All Darkstores &amp; Warehouses Above Safety Threshold (&gt;{stockThreshold} units)
              </h4>
              <p className="text-[11px] text-emerald-700 mt-0.5">
                Surveillance active across all 10-minute quick commerce depots and regional distribution centers.
              </p>
            </div>
          </div>
          <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-2.5 py-1 rounded-full">
            Healthy Buffer
          </span>
        </div>
      )}

      {/* 3. Darkstore Location Breakdown Cards */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Building2 className="w-4 h-4 text-indigo-600" />
            Darkstores &amp; Central DCs Inventory Health
          </h3>
          <span className="text-xs text-slate-500">
            Total {locationStats.length} storage nodes monitored
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {locationStats.map((loc) => {
            const hasAlert = loc.criticalCount > 0;
            return (
              <div
                key={loc.name}
                className={`rounded-xl border p-4.5 transition-all shadow-xs flex flex-col justify-between ${
                  hasAlert
                    ? 'bg-rose-50/40 border-rose-200'
                    : loc.warningCount > 0
                    ? 'bg-amber-50/30 border-amber-200'
                    : 'bg-white border-slate-200'
                }`}
              >
                <div>
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded text-slate-600 bg-slate-100">
                        {loc.isMotherDC ? 'Central DC' : 'Quick Commerce Darkstore'}
                      </span>
                      <h4 className="text-sm font-bold text-slate-900 mt-1.5 flex items-center gap-1.5">
                        {loc.name}
                      </h4>
                    </div>

                    {hasAlert ? (
                      <span className="px-2 py-0.5 rounded bg-rose-600 text-white font-black text-[10px] tracking-wider animate-pulse flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" />
                        {loc.criticalCount} ALERTS
                      </span>
                    ) : loc.warningCount > 0 ? (
                      <span className="px-2 py-0.5 rounded bg-amber-500 text-white font-bold text-[10px]">
                        {loc.warningCount} Low Buffer
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px] flex items-center gap-1">
                        <Check className="w-3 h-3" /> Healthy
                      </span>
                    )}
                  </div>

                  <div className="grid grid-cols-3 gap-2 mt-3.5 pt-3 border-t border-slate-100 text-center">
                    <div className="bg-white/80 border border-slate-100 rounded-lg p-2">
                      <div className="text-[10px] text-slate-500 font-medium">Available Units</div>
                      <div className="text-sm font-bold text-slate-900 mt-0.5">
                        {formatNumber(loc.totalAvailable)}
                      </div>
                    </div>
                    <div className="bg-white/80 border border-slate-100 rounded-lg p-2">
                      <div className="text-[10px] text-slate-500 font-medium">Inbound PO</div>
                      <div className="text-sm font-bold text-blue-600 mt-0.5">
                        +{formatNumber(loc.totalInbound)}
                      </div>
                    </div>
                    <div className="bg-white/80 border border-slate-100 rounded-lg p-2">
                      <div className="text-[10px] text-slate-500 font-medium">Avg DOI</div>
                      <div className="text-sm font-bold text-slate-900 mt-0.5">
                        {loc.avgDoi} days
                      </div>
                    </div>
                  </div>

                  {hasAlert && (
                    <div className="mt-3 bg-rose-100/70 border border-rose-200 rounded-lg p-2.5 text-[11px] text-rose-900 space-y-1">
                      <div className="font-bold flex items-center gap-1">
                        <AlertTriangle className="w-3.5 h-3.5 text-rose-600 shrink-0" />
                        Critical SKUs below {stockThreshold} units:
                      </div>
                      <div className="text-[10px] text-rose-700 leading-tight">
                        {loc.criticalSkus.slice(0, 2).map((s) => (
                          <div key={s.sku}>
                            • <strong className="font-bold">{s.sku}</strong> ({productMap.get(s.sku)?.name || s.sku}):{' '}
                            <span className="font-bold text-rose-800">{s.availableStock} units left</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="pt-3 mt-3 border-t border-slate-200/80 flex items-center justify-between">
                  <button
                    onClick={() => {
                      setSelectedWarehouseFilter(loc.name);
                      setStatusFilter(hasAlert ? 'Critical' : 'All');
                    }}
                    className="text-xs text-blue-600 hover:text-blue-700 font-bold"
                  >
                    View SKUs ({loc.skuCount})
                  </button>

                  <button
                    onClick={() => {
                      setTransferTarget(loc.name);
                      setTransferSource(loc.isMotherDC ? 'Mumbai Mother DC' : 'Noida Mother DC');
                      if (loc.criticalSkus.length > 0) {
                        setTransferSku(loc.criticalSkus[0].sku);
                      } else {
                        setTransferSku(data.products[0]?.sku || 'SLP0001');
                      }
                      setTransferUnits(50);
                      setIsTransferModalOpen(true);
                    }}
                    className="text-[11px] font-bold bg-slate-900 hover:bg-slate-800 text-white px-2.5 py-1 rounded-lg flex items-center gap-1 transition-colors"
                  >
                    <Truck className="w-3 h-3 text-blue-300" /> Rebalance
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 4. Filter & Search Controls */}
      <div className="bg-white border border-slate-200 rounded-xl p-4.5 shadow-xs space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2.5">
            {/* Search */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search SKU, Product, or Depot..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="bg-white border border-slate-200 text-slate-900 text-xs rounded-lg pl-8 pr-3 py-2 outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 w-60 shadow-xs"
              />
            </div>

            {/* Warehouse / Darkstore Filter */}
            <select
              value={selectedWarehouseFilter}
              onChange={(e) => setSelectedWarehouseFilter(e.target.value)}
              className="bg-white border border-slate-200 text-slate-700 text-xs rounded-lg px-3 py-2 outline-none focus:border-blue-500 shadow-xs"
            >
              <option value="All">All Locations ({allLocations.length})</option>
              {allLocations.map((w) => (
                <option key={w} value={w}>
                  {w}
                </option>
              ))}
            </select>

            {/* Category Filter */}
            <select
              value={selectedCategoryFilter}
              onChange={(e) => setSelectedCategoryFilter(e.target.value)}
              className="bg-white border border-slate-200 text-slate-700 text-xs rounded-lg px-3 py-2 outline-none focus:border-blue-500 shadow-xs"
            >
              <option value="All">All Categories ({categories.length})</option>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {/* Status Chips & Sort */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="flex items-center gap-1 bg-slate-100 border border-slate-200 p-1 rounded-lg text-xs">
              <button
                onClick={() => setStatusFilter('All')}
                className={`px-2.5 py-1 rounded font-semibold transition-colors ${
                  statusFilter === 'All' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                All ({inventoryList.length})
              </button>
              <button
                onClick={() => setStatusFilter('Critical')}
                className={`px-2.5 py-1 rounded font-semibold transition-colors flex items-center gap-1 ${
                  statusFilter === 'Critical' ? 'bg-rose-600 text-white shadow-xs' : 'text-rose-700 hover:bg-rose-50'
                }`}
              >
                <AlertTriangle className="w-3 h-3" />
                Critical ({globalCriticalRecords.length})
              </button>
              <button
                onClick={() => setStatusFilter('Warning')}
                className={`px-2.5 py-1 rounded font-semibold transition-colors ${
                  statusFilter === 'Warning' ? 'bg-amber-500 text-white shadow-xs' : 'text-amber-700 hover:bg-amber-50'
                }`}
              >
                Low Buffer ({globalWarningRecords.length})
              </button>
            </div>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="bg-white border border-slate-200 text-slate-700 text-xs rounded-lg px-2.5 py-1.5 outline-none focus:border-blue-500"
            >
              <option value="stock_asc">Sort: Lowest Stock First</option>
              <option value="stock_desc">Sort: Highest Stock First</option>
              <option value="doi_asc">Sort: Lowest DOI (Days of Inventory)</option>
              <option value="sku">Sort: SKU Code</option>
            </select>
          </div>
        </div>
      </div>

      {/* 5. Master Inventory & Darkstore Ledger Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-xs">
        <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/50">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">
              Darkstore SKU Ledger &amp; Live Stock Monitor ({filteredRecords.length} records matching)
            </h3>
            <p className="text-[11px] text-slate-500">
              Highlighted in Red when available stock is below {stockThreshold} units threshold.
            </p>
          </div>

          <button
            onClick={() => {
              setTransferSku(filteredRecords[0]?.sku || 'SLP0001');
              setTransferTarget(filteredRecords[0]?.warehouse || 'Blinkit Koramangala Hub (BLK-BGL-01)');
              setIsTransferModalOpen(true);
            }}
            className="text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg flex items-center gap-1 shadow-xs"
          >
            <Plus className="w-3.5 h-3.5" /> Transfer Stock
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-100/80 text-[11px] font-bold text-slate-700 uppercase tracking-wider border-b border-slate-200">
                <th className="py-3 px-4">SKU &amp; Product Name</th>
                <th className="py-3 px-3">Category</th>
                <th className="py-3 px-3">Location / Darkstore</th>
                <th className="py-3 px-3 text-right">Available Stock</th>
                <th className="py-3 px-3 text-right">Inbound PO</th>
                <th className="py-3 px-3 text-right">Reserved / Damaged</th>
                <th className="py-3 px-3 text-right">DOI (Days)</th>
                <th className="py-3 px-3 text-center">Buffer Status</th>
                <th className="py-3 px-4 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {filteredRecords.length > 0 ? (
                filteredRecords.map((record, index) => {
                  const prod = productMap.get(record.sku);
                  const available = record.availableStock || record.closingStock || 0;
                  const isCritical = available < stockThreshold;
                  const isWarning = available >= stockThreshold && available < stockThreshold * 2;

                  return (
                    <tr
                      key={`${record.sku}-${record.warehouse}-${index}`}
                      className={`hover:bg-slate-50/80 transition-colors ${
                        isCritical ? 'bg-rose-50/30' : isWarning ? 'bg-amber-50/20' : ''
                      }`}
                    >
                      <td className="py-3 px-4">
                        <div className="font-bold text-slate-900 flex items-center gap-1.5">
                          <Package className="w-3.5 h-3.5 text-slate-400" />
                          <span>{record.sku}</span>
                        </div>
                        <div className="text-[11px] text-slate-500 truncate max-w-xs mt-0.5">
                          {prod?.name || 'Sleepsia Product'}
                        </div>
                      </td>

                      <td className="py-3 px-3">
                        <span className="text-[11px] text-slate-600 font-medium">
                          {prod?.category || 'Sleeping Pillows'}
                        </span>
                      </td>

                      <td className="py-3 px-3">
                        <div className="font-medium text-slate-800 flex items-center gap-1">
                          <Building2 className="w-3 h-3 text-slate-400" />
                          <span className="text-[11px]">{record.warehouse}</span>
                        </div>
                      </td>

                      <td className="py-3 px-3 text-right">
                        <div
                          className={`font-black text-sm inline-flex items-center gap-1 px-2 py-0.5 rounded ${
                            isCritical
                              ? 'bg-rose-100 text-rose-800'
                              : isWarning
                              ? 'bg-amber-100 text-amber-800'
                              : 'text-slate-900'
                          }`}
                        >
                          {isCritical && <AlertTriangle className="w-3 h-3 text-rose-600 animate-pulse" />}
                          {formatNumber(available)}
                        </div>
                        {isCritical && (
                          <div className="text-[10px] text-rose-600 font-bold">Below {stockThreshold} threshold</div>
                        )}
                      </td>

                      <td className="py-3 px-3 text-right">
                        <span className="font-bold text-blue-600">
                          {record.inboundStock ? `+${formatNumber(record.inboundStock)}` : '-'}
                        </span>
                      </td>

                      <td className="py-3 px-3 text-right text-slate-500 text-[11px]">
                        <div>{formatNumber(record.reservedStock || 0)} res</div>
                        {record.damagedStock ? (
                          <div className="text-rose-600 text-[10px]">{record.damagedStock} dmg</div>
                        ) : null}
                      </td>

                      <td className="py-3 px-3 text-right font-bold">
                        <span
                          className={`${
                            (record.daysOfInventory || 8) < 3
                              ? 'text-rose-600'
                              : (record.daysOfInventory || 8) < 7
                              ? 'text-amber-600'
                              : 'text-slate-800'
                          }`}
                        >
                          {record.daysOfInventory || 8}d
                        </span>
                      </td>

                      <td className="py-3 px-3 text-center">
                        {isCritical ? (
                          <span className="px-2 py-0.5 rounded bg-rose-600 text-white font-black text-[10px] tracking-wider">
                            CRITICAL
                          </span>
                        ) : isWarning ? (
                          <span className="px-2 py-0.5 rounded bg-amber-500 text-white font-bold text-[10px]">
                            LOW BUFFER
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                            HEALTHY
                          </span>
                        )}
                      </td>

                      <td className="py-3 px-4 text-center">
                        <button
                          onClick={() => openTransferForRecord(record)}
                          className={`text-xs font-bold px-2.5 py-1 rounded-lg transition-colors flex items-center justify-center gap-1 mx-auto ${
                            isCritical
                              ? 'bg-rose-600 hover:bg-rose-700 text-white shadow-xs'
                              : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                          }`}
                        >
                          <Truck className="w-3 h-3" />
                          <span>Rebalance</span>
                        </button>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={9} className="py-8 text-center text-slate-500 text-xs">
                    No SKU records matching the selected filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* 6. Stock Transfer / Replenishment Modal */}
      {isTransferModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-lg w-full shadow-2xl space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-blue-50 text-blue-600 border border-blue-100">
                  <Truck className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Execute Intra-Depot Stock Transfer</h3>
                  <p className="text-[11px] text-slate-500">
                    Rebalance buffer units from Surplus Hub to Depleted Darkstore
                  </p>
                </div>
              </div>
              <button onClick={() => setIsTransferModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3.5 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Target SKU</label>
                <select
                  value={transferSku}
                  onChange={(e) => setTransferSku(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-medium text-slate-900 outline-none focus:border-blue-500"
                >
                  {data.products.map((p) => (
                    <option key={p.sku} value={p.sku}>
                      {p.sku} - {p.productName}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Origin Source (Surplus)</label>
                  <select
                    value={transferSource}
                    onChange={(e) => setTransferSource(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-medium text-slate-900 outline-none focus:border-blue-500"
                  >
                    {allLocations.map((w) => (
                      <option key={w} value={w}>
                        {w}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Destination Darkstore</label>
                  <select
                    value={transferTarget}
                    onChange={(e) => setTransferTarget(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-medium text-slate-900 outline-none focus:border-blue-500"
                  >
                    {allLocations.map((w) => (
                      <option key={w} value={w}>
                        {w}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Transfer Units</label>
                <input
                  type="number"
                  min={1}
                  max={500}
                  value={transferUnits}
                  onChange={(e) => setTransferUnits(Math.max(1, parseInt(e.target.value) || 1))}
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-bold text-slate-900 outline-none focus:border-blue-500"
                />
                <div className="text-[10px] text-slate-500 mt-1">
                  Transfers from central DCs to darkstores resolve low stock within 2 to 4 hours via dedicated logistics.
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2.5">
              <button
                onClick={() => setIsTransferModalOpen(false)}
                className="px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleExecuteTransfer}
                className="px-4 py-2 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white shadow-xs flex items-center gap-1.5 transition-colors"
              >
                <Send className="w-3.5 h-3.5" /> Dispatch Stock Transfer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
