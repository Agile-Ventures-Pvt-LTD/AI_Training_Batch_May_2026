import React, { useState, useMemo } from 'react';
import {
  Building2,
  Package,
  CalendarClock,
  AlertTriangle,
  Zap,
  CheckCircle2,
  ChevronRight,
  TrendingDown,
  Clock,
  Filter,
  ArrowRight,
  Factory,
  Search,
  Store,
  Layers,
  Sparkles,
  RefreshCw,
  Truck,
  ShieldCheck,
  BarChart3,
  ExternalLink,
  MapPin,
  HelpCircle,
  Eye,
  Info
} from 'lucide-react';
import { useData } from '../../context/DataContext';
import { MarketplaceId, DarkStoreInventory, SKUListing, MotherHubSkuStock, ManufacturerSupplyInfo } from '../../types';
import { formatINR } from '../../data/mockData';

interface SupplyChainViewProps {
  onOpenStockTransfer: (sku: string, hub: string, units?: number) => void;
  onSelectSku?: (skuId: string) => void;
  onOpenShortageModal?: () => void;
}

export const SupplyChainView: React.FC<SupplyChainViewProps> = ({
  onOpenStockTransfer,
  onSelectSku,
  onOpenShortageModal
}) => {
  const {
    skus,
    darkStores,
    motherHubSkuStock,
    manufacturerSupply,
    channelPricing
  } = useData();

  const [activeTab, setActiveTab] = useState<
    'dark_stores_skus' | 'mother_hubs_skus' | 'marketplaces_matrix' | 'manufacturers_supply' | 'pipeline_flow' | 'batch_expiry'
  >('dark_stores_skus');

  // Filters
  const [selectedSkuFilter, setSelectedSkuFilter] = useState<string>('all');
  const [selectedMarketplaceFilter, setSelectedMarketplaceFilter] = useState<string>('all');
  const [selectedCityFilter, setSelectedCityFilter] = useState<string>('all');
  const [selectedStockStatusFilter, setSelectedStockStatusFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Multi-SKU aggregate stats
  const totalDarkStoreUnits = useMemo(() => {
    return darkStores.reduce((sum, d) => sum + (d.availableStock ?? 0), 0);
  }, [darkStores]);

  const totalMotherHubUnits = useMemo(() => {
    return (motherHubSkuStock || []).reduce((sum, h) => sum + (h.quantityAvailable ?? 0), 0);
  }, [motherHubSkuStock]);

  const totalManufacturerUnits = useMemo(() => {
    return (manufacturerSupply || []).reduce((sum, m) => sum + (m.factoryFinishedGoodsStock ?? 0), 0);
  }, [manufacturerSupply]);

  const starvedDarkStoreCount = useMemo(() => {
    return darkStores.filter((d) => (d.availableStock ?? 0) <= (d.safetyThreshold ?? 10)).length;
  }, [darkStores]);

  // Unique lists for filter dropdowns
  const uniqueSkus = useMemo(() => {
    const set = new Set<string>();
    skus.forEach((s) => set.add(s.sku));
    return Array.from(set);
  }, [skus]);

  const uniqueCities = useMemo(() => {
    const set = new Set<string>();
    darkStores.forEach((d) => {
      if (d.city) set.add(d.city);
    });
    return Array.from(set);
  }, [darkStores]);

  // Filtered Dark Stores
  const filteredDarkStores = useMemo(() => {
    return darkStores.filter((d) => {
      const matchesSku = selectedSkuFilter === 'all' || d.sku === selectedSkuFilter;
      const matchesMarketplace =
        selectedMarketplaceFilter === 'all' ||
        String(d.platform).toLowerCase() === selectedMarketplaceFilter.toLowerCase();
      const matchesCity = selectedCityFilter === 'all' || d.city === selectedCityFilter;
      const matchesStatus =
        selectedStockStatusFilter === 'all' ||
        d.status === selectedStockStatusFilter ||
        (selectedStockStatusFilter === 'Low Stock' && (d.availableStock ?? 0) <= (d.safetyThreshold ?? 10));

      const matchesQuery =
        !searchQuery ||
        d.storeName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (d.sku && d.sku.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (d.productName && d.productName.toLowerCase().includes(searchQuery.toLowerCase())) ||
        d.city.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.storeId.toLowerCase().includes(searchQuery.toLowerCase());

      return matchesSku && matchesMarketplace && matchesCity && matchesStatus && matchesQuery;
    });
  }, [darkStores, selectedSkuFilter, selectedMarketplaceFilter, selectedCityFilter, selectedStockStatusFilter, searchQuery]);

  // Filtered Mother Hub SKU Matrix
  const filteredMotherHubs = useMemo(() => {
    return (motherHubSkuStock || []).filter((h) => {
      const matchesSku = selectedSkuFilter === 'all' || h.sku === selectedSkuFilter;
      const matchesCity = selectedCityFilter === 'all' || h.city === selectedCityFilter;
      const matchesQuery =
        !searchQuery ||
        h.hubName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        h.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        h.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        h.city.toLowerCase().includes(searchQuery.toLowerCase());

      return matchesSku && matchesCity && matchesQuery;
    });
  }, [motherHubSkuStock, selectedSkuFilter, selectedCityFilter, searchQuery]);

  // Filtered Manufacturer Supply Info
  const filteredManufacturerSupply = useMemo(() => {
    return (manufacturerSupply || []).filter((m) => {
      const matchesSku = selectedSkuFilter === 'all' || m.sku === selectedSkuFilter;
      const matchesQuery =
        !searchQuery ||
        m.manufacturerName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.plantName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.location.toLowerCase().includes(searchQuery.toLowerCase());

      return matchesSku && matchesQuery;
    });
  }, [manufacturerSupply, selectedSkuFilter, searchQuery]);

  // Filtered Batch & Shelf Life Skus
  const filteredBatchSkus = useMemo(() => {
    return skus.map((s, idx) => {
      let daysRemaining = 720;
      let healthPct = 98;
      let statusText = 'Fresh / Compliant';
      let badgeClass = 'bg-emerald-50 text-emerald-800 border-emerald-200';
      let textClass = 'text-emerald-700';
      let batchCode = `BAT-2026-08${idx + 1}A`;
      let mfgDate = '2026-02-15';
      let expDate = '2028-02-15';
      let suggestion = 'Standard FEFO Storage';

      if (idx === 1) {
        daysRemaining = 45;
        healthPct = 18;
        statusText = 'Expiring Soon';
        badgeClass = 'bg-amber-50 text-amber-800 border-amber-200';
        textClass = 'text-amber-700';
        batchCode = 'BAT-2026-042B';
        mfgDate = '2024-10-10';
        expDate = '2026-10-10';
        suggestion = 'Apply BOGO Offer & 15% Clearance Discount';
      } else if (idx === 2) {
        daysRemaining = 12;
        healthPct = 4;
        statusText = 'Critical Expiry';
        badgeClass = 'bg-rose-50 text-rose-800 border-rose-200';
        textClass = 'text-rose-700';
        batchCode = 'BAT-2026-012C';
        mfgDate = '2024-09-01';
        expDate = '2026-09-04';
        suggestion = 'Urgent: Liquidate via Flash Sale (30% Off) or Ad Bid Increase +30%';
      } else if (idx === 4) {
        daysRemaining = 35;
        healthPct = 14;
        statusText = 'Expiring Soon';
        badgeClass = 'bg-amber-50 text-amber-800 border-amber-200';
        textClass = 'text-amber-700';
        batchCode = 'BAT-2026-035D';
        mfgDate = '2024-10-01';
        expDate = '2026-09-28';
        suggestion = 'Increase Sponsored Ad Bids +25% & Bundle with Fast Movers';
      } else if (idx === 6) {
        daysRemaining = 150;
        healthPct = 62;
        statusText = 'Moderate Health';
        badgeClass = 'bg-blue-50 text-blue-800 border-blue-200';
        textClass = 'text-blue-700';
        batchCode = 'BAT-2026-150E';
        mfgDate = '2025-03-15';
        expDate = '2027-01-20';
        suggestion = 'Prioritize in FEFO Outbound Picking Queue';
      }

      return { s, idx, daysRemaining, healthPct, statusText, badgeClass, textClass, batchCode, mfgDate, expDate, suggestion };
    }).filter(item => {
      const matchesSku = selectedSkuFilter === 'all' || item.s.sku === selectedSkuFilter;
      const matchesQuery = !searchQuery || 
        item.s.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
        item.s.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.batchCode.toLowerCase().includes(searchQuery.toLowerCase());

      let matchesStatus = true;
      if (selectedStockStatusFilter === 'In Stock') {
        matchesStatus = item.statusText === 'Fresh / Compliant' || item.statusText === 'Moderate Health';
      } else if (selectedStockStatusFilter === 'Low Stock') {
        matchesStatus = item.statusText === 'Expiring Soon';
      } else if (selectedStockStatusFilter === 'Out Of Stock') {
        matchesStatus = item.statusText === 'Critical Expiry';
      }

      return matchesSku && matchesQuery && matchesStatus;
    });
  }, [skus, selectedSkuFilter, selectedStockStatusFilter, searchQuery]);

  // Unique Mother Hubs List
  const uniqueHubNames = useMemo(() => {
    const map = new Map<string, MotherHubSkuStock[]>();
    (motherHubSkuStock || []).forEach((item) => {
      const existing = map.get(item.hubName) || [];
      existing.push(item);
      map.set(item.hubName, existing);
    });
    return Array.from(map.entries());
  }, [motherHubSkuStock]);

  // Unique Manufacturers List
  const uniquePlants = useMemo(() => {
    const map = new Map<string, ManufacturerSupplyInfo[]>();
    (manufacturerSupply || []).forEach((item) => {
      const existing = map.get(item.plantName) || [];
      existing.push(item);
      map.set(item.plantName, existing);
    });
    return Array.from(map.entries());
  }, [manufacturerSupply]);

  // Marketplace Cross-Distribution Matrix Data
  const marketplaceSummary = useMemo(() => {
    const platforms: { [key: string]: { name: string; stores: DarkStoreInventory[]; skusPresent: Set<string>; totalUnits: number } } = {
      blinkit: { name: 'Blinkit', stores: [], skusPresent: new Set(), totalUnits: 0 },
      zepto: { name: 'Zepto', stores: [], skusPresent: new Set(), totalUnits: 0 },
      instamart: { name: 'Swiggy Instamart', stores: [], skusPresent: new Set(), totalUnits: 0 },
      jiomart: { name: 'JioMart Quick', stores: [], skusPresent: new Set(), totalUnits: 0 }
    };

    darkStores.forEach((d) => {
      const platKey = String(d.platform).toLowerCase();
      if (platforms[platKey]) {
        platforms[platKey].stores.push(d);
        if (d.sku) platforms[platKey].skusPresent.add(d.sku);
        platforms[platKey].totalUnits += d.availableStock ?? 0;
      }
    });

    return Object.entries(platforms).map(([key, data]) => ({
      key,
      ...data,
      skusCount: data.skusPresent.size,
      storesCount: data.stores.length
    }));
  }, [darkStores]);

  return (
    <div id="supply-chain-intelligence-workspace" className="space-y-6">
      {/* 1. Header Banner & Global KPI Bar */}
      <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-xs flex flex-col xl:flex-row xl:items-center justify-between gap-5">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 text-[11px] font-bold rounded-md uppercase tracking-wider">
              Supply Chain & Inventory Matrix
            </span>
            <span className="text-slate-400 text-xs">•</span>
            <span className="text-xs text-slate-500 font-medium">
              Multi-Node SKU Stock Across Manufacturers, Mother Hubs, Dark Stores & Marketplaces
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-1.5 flex items-center gap-2">
            <span>Supply Chain Intelligence & Stock Allocation</span>
            <span className="text-xs font-normal px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-mono">
              Live Real-Time Sync
            </span>
          </h2>
          <p className="text-xs text-slate-600 mt-1 max-w-3xl leading-relaxed">
            Track exact SKU quantities stored at each <strong>Dark Store POD</strong>, buffer reserves across all <strong>Mother Hubs</strong>, channel availability across <strong>Marketplaces</strong>, and factory warehouse stock at each <strong>Manufacturer Plant</strong>.
          </p>
          {onOpenShortageModal && (
            <div className="mt-3">
              <button
                onClick={onOpenShortageModal}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold flex items-center space-x-2 transition-colors shadow-xs"
              >
                <Search className="w-4 h-4" />
                <span>🔍 Analyze Dark Store Pod Shortages & SKU Allocation Matrix</span>
              </button>
            </div>
          )}
        </div>

        {/* Aggregate KPI Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 shrink-0">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-left">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-slate-600 uppercase">Dark Store Units</span>
              <Store className="w-3.5 h-3.5 text-slate-500" />
            </div>
            <span className="text-base font-black text-slate-900 block mt-1">
              {totalDarkStoreUnits.toLocaleString('en-IN')}
            </span>
            <span className="text-[10px] text-slate-500">{darkStores.length} Active PODs</span>
          </div>

          <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl text-left">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-blue-800 uppercase">Mother Hubs</span>
              <Package className="w-3.5 h-3.5 text-blue-600" />
            </div>
            <span className="text-base font-black text-blue-700 block mt-1">
              {totalMotherHubUnits.toLocaleString('en-IN')}
            </span>
            <span className="text-[10px] text-blue-600">4 Regional Hubs</span>
          </div>

          <div className="p-3 bg-indigo-50 border border-indigo-200 rounded-xl text-left">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-indigo-800 uppercase">Factory Stock</span>
              <Factory className="w-3.5 h-3.5 text-indigo-600" />
            </div>
            <span className="text-base font-black text-indigo-700 block mt-1">
              {totalManufacturerUnits.toLocaleString('en-IN')}
            </span>
            <span className="text-[10px] text-indigo-600">3 Mfg Facilities</span>
          </div>

          <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-left">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-amber-800 uppercase">Stock Runways</span>
              <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            </div>
            <span className="text-base font-black text-amber-700 block mt-1">
              {starvedDarkStoreCount} Low Stock
            </span>
            <span className="text-[10px] text-amber-700">Needs Dispatch</span>
          </div>
        </div>
      </div>

      {/* 2. Global Filter & Quick SKU Selector Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs space-y-3">
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2.5">
            <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
              <Filter className="w-3.5 h-3.5 text-slate-500" />
              <span>Filter Matrix:</span>
            </span>

            {/* SKU Selector */}
            <select
              value={selectedSkuFilter}
              onChange={(e) => setSelectedSkuFilter(e.target.value)}
              className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 text-xs rounded-lg font-medium text-slate-700 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All SKUs (Catalog Master)</option>
              {uniqueSkus.map((sku) => {
                const sObj = skus.find((s) => s.sku === sku);
                return (
                  <option key={sku} value={sku}>
                    {sku} - {sObj?.name ? sObj.name.slice(0, 32) + '...' : sku}
                  </option>
                );
              })}
            </select>

            {/* Marketplace Filter */}
            <select
              value={selectedMarketplaceFilter}
              onChange={(e) => setSelectedMarketplaceFilter(e.target.value)}
              className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 text-xs rounded-lg font-medium text-slate-700 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Marketplaces & Channels</option>
              <option value="blinkit">Blinkit Quick Commerce</option>
              <option value="zepto">Zepto 10-Min</option>
              <option value="instamart">Swiggy Instamart</option>
              <option value="jiomart">JioMart</option>
            </select>

            {/* City Filter */}
            <select
              value={selectedCityFilter}
              onChange={(e) => setSelectedCityFilter(e.target.value)}
              className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 text-xs rounded-lg font-medium text-slate-700 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Cities</option>
              {uniqueCities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>

            {/* Stock Health Status Filter */}
            <select
              value={selectedStockStatusFilter}
              onChange={(e) => setSelectedStockStatusFilter(e.target.value)}
              className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 text-xs rounded-lg font-medium text-slate-700 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Stock Statuses</option>
              <option value="In Stock">In Stock (Healthy)</option>
              <option value="Low Stock">Low Stock (&lt; Safety Buffer)</option>
              <option value="Out Of Stock">Out Of Stock (OOS Risk)</option>
            </select>
          </div>

          {/* Search Box */}
          <div className="relative min-w-[240px]">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search store, hub, plant, SKU..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Selected SKU Quick Summary Strip */}
        {selectedSkuFilter !== 'all' && (
          <div className="p-3 bg-blue-50/70 border border-blue-200 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-2 text-xs">
            <div className="flex items-center space-x-2">
              <span className="font-mono font-bold text-blue-900 bg-white px-2 py-0.5 rounded border border-blue-200">
                {selectedSkuFilter}
              </span>
              <span className="font-bold text-slate-900">
                {skus.find((s) => s.sku === selectedSkuFilter)?.name || 'Selected SKU'}
              </span>
            </div>

            <div className="flex flex-wrap items-center gap-4 text-[11px] text-slate-600">
              <span>
                Dark Stores:{' '}
                <strong className="text-slate-900">
                  {darkStores.filter((d) => d.sku === selectedSkuFilter).reduce((s, d) => s + (d.availableStock ?? 0), 0)} units
                </strong>
              </span>
              <span>•</span>
              <span>
                Mother Hubs:{' '}
                <strong className="text-blue-700">
                  {motherHubSkuStock.filter((h) => h.sku === selectedSkuFilter).reduce((s, h) => s + (h.quantityAvailable ?? 0), 0)} units
                </strong>
              </span>
              <span>•</span>
              <span>
                Manufacturer FG:{' '}
                <strong className="text-indigo-700">
                  {manufacturerSupply.filter((m) => m.sku === selectedSkuFilter).reduce((s, m) => s + (m.factoryFinishedGoodsStock ?? 0), 0)} units
                </strong>
              </span>
              <button
                onClick={() => setSelectedSkuFilter('all')}
                className="text-blue-600 hover:text-blue-800 font-bold underline text-[11px]"
              >
                Clear Focus
              </button>
            </div>
          </div>
        )}
      </div>

      {/* 3. Workspace Navigation Tabs */}
      <div className="flex border-b border-slate-200 gap-2 sm:gap-6 text-xs font-bold overflow-x-auto pb-0.5">
        <button
          onClick={() => setActiveTab('dark_stores_skus')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all whitespace-nowrap ${
            activeTab === 'dark_stores_skus'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <Store className="w-4 h-4" />
          <span>1. Dark Stores × SKU Matrix ({filteredDarkStores.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('mother_hubs_skus')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all whitespace-nowrap ${
            activeTab === 'mother_hubs_skus'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <Package className="w-4 h-4" />
          <span>2. Mother Hubs SKU Reserves ({filteredMotherHubs.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('marketplaces_matrix')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all whitespace-nowrap ${
            activeTab === 'marketplaces_matrix'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <Building2 className="w-4 h-4" />
          <span>3. Marketplace Channel Matrix</span>
        </button>

        <button
          onClick={() => setActiveTab('manufacturers_supply')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all whitespace-nowrap ${
            activeTab === 'manufacturers_supply'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <Factory className="w-4 h-4" />
          <span>4. Manufacturers & Plants Supply ({filteredManufacturerSupply.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('pipeline_flow')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all whitespace-nowrap ${
            activeTab === 'pipeline_flow'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>5. End-to-End Pipeline Flow</span>
        </button>

        <button
          onClick={() => setActiveTab('batch_expiry')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all whitespace-nowrap ${
            activeTab === 'batch_expiry'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-900'
          }`}
        >
          <CalendarClock className="w-4 h-4" />
          <span>Batch & Shelf Life</span>
        </button>
      </div>

      {/* 4. TAB 1: Dark Stores × SKU Matrix */}
      {activeTab === 'dark_stores_skus' && (
        <div className="space-y-4">
          <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs text-slate-600">
            <div>
              <strong className="text-slate-900">Dark Store SKU Visibility:</strong> Shows exact SKU quantities, safety thresholds, runway hours, and connected mother hubs across all micro-fulfillment PODs.
            </div>
            <div className="text-slate-500">
              Showing <strong>{filteredDarkStores.length}</strong> matching POD allocations
            </div>
          </div>

          {/* Dark Stores Table */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-700 uppercase tracking-wider">
                    <th className="py-3 px-3.5">Store ID & POD Name</th>
                    <th className="py-3 px-3">Marketplace</th>
                    <th className="py-3 px-3">SKU & Product Name</th>
                    <th className="py-3 px-3">City / Pincode</th>
                    <th className="py-3 px-3 text-right">Available Stock</th>
                    <th className="py-3 px-3 text-right">Safety Buffer</th>
                    <th className="py-3 px-3 text-right">Runway</th>
                    <th className="py-3 px-3">Status</th>
                    <th className="py-3 px-3">Delivery SLA</th>
                    <th className="py-3 px-3">Selling Price</th>
                    <th className="py-3 px-3">Mother Hub Source</th>
                    <th className="py-3 px-3.5 text-center">Quick Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredDarkStores.length === 0 ? (
                    <tr>
                      <td colSpan={12} className="py-8 text-center text-slate-500">
                        No dark store allocations match the selected filters.
                      </td>
                    </tr>
                  ) : (
                    filteredDarkStores.map((store) => {
                      const stock = store.availableStock ?? 0;
                      const safety = store.safetyThreshold ?? 10;
                      const isLow = stock <= safety;
                      const isOos = stock === 0;
                      const platform = String(store.platform || 'blinkit').toLowerCase();

                      return (
                        <tr
                          key={`${store.storeId}-${store.sku || 'default'}`}
                          className={`hover:bg-slate-50/80 transition-colors ${
                            isOos ? 'bg-red-50/40' : isLow ? 'bg-amber-50/30' : ''
                          }`}
                        >
                          <td className="py-3 px-3.5">
                            <div className="font-bold text-slate-900">{store.storeName}</div>
                            <div className="font-mono text-[10px] text-slate-500">{store.storeId}</div>
                          </td>
                          <td className="py-3 px-3">
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                                platform === 'blinkit'
                                  ? 'bg-amber-100 text-amber-900 border border-amber-200'
                                  : platform === 'zepto'
                                  ? 'bg-purple-100 text-purple-900 border border-purple-200'
                                  : platform === 'instamart'
                                  ? 'bg-orange-100 text-orange-900 border border-orange-200'
                                  : 'bg-blue-100 text-blue-900 border border-blue-200'
                              }`}
                            >
                              {store.platform}
                            </span>
                          </td>
                          <td className="py-3 px-3 max-w-[180px]">
                            <div className="font-bold text-slate-800 font-mono text-[11px]">{store.sku || 'SLP-1001'}</div>
                            <div className="text-[11px] text-slate-500 truncate" title={store.productName || 'Sleep Pillow'}>
                              {store.productName || 'Sleep Pillow SKU'}
                            </div>
                          </td>
                          <td className="py-3 px-3">
                            <div className="text-slate-800 font-medium">{store.city}</div>
                            <div className="text-[10px] text-slate-400 font-mono">{store.pincode}</div>
                          </td>
                          <td className="py-3 px-3 text-right">
                            <span
                              className={`font-mono font-bold text-sm ${
                                isOos ? 'text-red-700 font-black' : isLow ? 'text-amber-700 font-bold' : 'text-slate-900'
                              }`}
                            >
                              {stock.toLocaleString('en-IN')}
                            </span>
                            <span className="text-[10px] text-slate-400 block">units</span>
                          </td>
                          <td className="py-3 px-3 text-right">
                            <span className="font-mono text-slate-600">{safety}</span>
                            <span className="text-[10px] text-slate-400 block">units</span>
                          </td>
                          <td className="py-3 px-3 text-right">
                            <span
                              className={`font-bold font-mono ${
                                (store.runwayHours ?? 36) < 12
                                  ? 'text-red-700'
                                  : (store.runwayHours ?? 36) < 24
                                  ? 'text-amber-700'
                                  : 'text-emerald-700'
                              }`}
                            >
                              {store.runwayHours ?? 36}h
                            </span>
                          </td>
                          <td className="py-3 px-3">
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold inline-block border ${
                                store.status === 'In Stock'
                                  ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                                  : store.status === 'Low Stock'
                                  ? 'bg-amber-50 text-amber-800 border-amber-200 animate-pulse'
                                  : 'bg-red-50 text-red-800 border-red-200 font-black'
                              }`}
                            >
                              {store.status}
                            </span>
                          </td>
                          <td className="py-3 px-3">
                            <span className="text-slate-700 font-medium flex items-center gap-1">
                              <Clock className="w-3 h-3 text-slate-400" />
                              <span>{store.deliverySlaMins} mins</span>
                            </span>
                          </td>
                          <td className="py-3 px-3 font-mono font-medium text-slate-800">
                            {formatINR(store.sellingPrice)}
                          </td>
                          <td className="py-3 px-3 max-w-[160px]">
                            <div className="text-slate-800 truncate" title={store.motherHubName}>
                              {store.motherHubName || 'Nelamangala Hub'}
                            </div>
                            <div className="text-[10px] text-slate-500 font-mono">
                              {(store.motherHubStock ?? 50000).toLocaleString('en-IN')} in Hub ({store.transitHoursFromHub ?? 3}h lead)
                            </div>
                          </td>
                          <td className="py-3 px-3.5 text-center">
                            <button
                              onClick={() => {
                                const suggested = Math.max(20, ((store.safetyThreshold || 25) * 3) - store.availableStock);
                                onOpenStockTransfer(
                                  store.sku || 'SLP-1001',
                                  store.motherHubName || 'Bengaluru Central Mother Hub (Nelamangala)',
                                  suggested
                                );
                              }}
                              className={`px-2.5 py-1 rounded-lg text-xs font-bold flex items-center space-x-1 mx-auto transition-colors shadow-2xs ${
                                isLow
                                  ? 'bg-red-600 hover:bg-red-700 text-white'
                                  : 'bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200'
                              }`}
                              title="Trigger stock replenishment transfer order"
                            >
                              <Zap className="w-3 h-3" />
                              <span>{isLow ? 'Restock' : 'Transfer'}</span>
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 5. TAB 2: Mother Hubs SKU Reserves Matrix */}
      {activeTab === 'mother_hubs_skus' && (
        <div className="space-y-6">
          <div className="p-4 bg-blue-50/70 border border-blue-200 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs text-blue-900">
            <div>
              <strong className="text-blue-950">Mother Hub SKU Inventory:</strong> Answers which Mother Hub has what quantity of which specific SKUs, reserved buffer thresholds, and connected dark store network counts.
            </div>
            <div className="text-blue-700 font-bold">
              Total Mother Hub Inventory: {totalMotherHubUnits.toLocaleString('en-IN')} units
            </div>
          </div>

          {/* Mother Hub Cards Grid */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
            {uniqueHubNames.map(([hubName, items]) => {
              const totalUnitsInHub = items.reduce((sum, i) => sum + i.quantityAvailable, 0);
              const totalReservedInHub = items.reduce((sum, i) => sum + i.reservedQuantity, 0);
              const hubCity = items[0]?.city || 'India';
              const hubId = items[0]?.hubId || 'HUB-01';
              const dispatchSla = items[0]?.dispatchSlaHours || 4;
              const connectedStores = items[0]?.connectedDarkStoresCount || 24;

              return (
                <div key={hubName} className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
                  {/* Hub Header */}
                  <div className="p-4 bg-slate-50 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-mono text-[10px] font-bold px-2 py-0.5 bg-blue-100 text-blue-800 rounded">
                          {hubId}
                        </span>
                        <h3 className="font-bold text-slate-900 text-sm">{hubName}</h3>
                      </div>
                      <div className="text-xs text-slate-500 mt-0.5 flex items-center gap-2">
                        <MapPin className="w-3 h-3 text-slate-400" />
                        <span>{hubCity} • {connectedStores} Connected Dark Stores</span>
                        <span>•</span>
                        <Clock className="w-3 h-3 text-slate-400" />
                        <span>{dispatchSla}h Dispatch SLA</span>
                      </div>
                    </div>

                    <div className="text-right shrink-0">
                      <span className="text-[10px] uppercase font-bold text-slate-500 block">Hub Total Stock</span>
                      <span className="text-base font-black text-blue-700">{totalUnitsInHub.toLocaleString('en-IN')} units</span>
                    </div>
                  </div>

                  {/* Hub SKU Table */}
                  <div className="overflow-x-auto flex-1">
                    <table className="w-full text-left text-xs">
                      <thead>
                        <tr className="bg-slate-50/70 border-b border-slate-100 text-[10px] font-bold text-slate-600 uppercase">
                          <th className="py-2.5 px-3.5">SKU Code & Product</th>
                          <th className="py-2.5 px-3 text-right">Available Stock</th>
                          <th className="py-2.5 px-3 text-right">Reserved</th>
                          <th className="py-2.5 px-3 text-right">Safety Buffer</th>
                          <th className="py-2.5 px-3">Buffer Health</th>
                          <th className="py-2.5 px-3 text-center">Dispatch</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {items.map((skuStock) => (
                          <tr key={skuStock.id} className="hover:bg-slate-50/80 transition-colors">
                            <td className="py-2.5 px-3.5">
                              <span className="font-mono font-bold text-slate-900 block">{skuStock.sku}</span>
                              <span className="text-[11px] text-slate-500 truncate block max-w-[200px]" title={skuStock.productName}>
                                {skuStock.productName}
                              </span>
                            </td>
                            <td className="py-2.5 px-3 text-right">
                              <span className="font-mono font-bold text-slate-900">
                                {skuStock.quantityAvailable.toLocaleString('en-IN')}
                              </span>
                            </td>
                            <td className="py-2.5 px-3 text-right text-slate-500 font-mono">
                              {skuStock.reservedQuantity.toLocaleString('en-IN')}
                            </td>
                            <td className="py-2.5 px-3 text-right text-slate-500 font-mono">
                              {skuStock.safetyStockThreshold.toLocaleString('en-IN')}
                            </td>
                            <td className="py-2.5 px-3">
                              <span
                                className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                                  skuStock.bufferHealth === 'Optimal'
                                    ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                                    : skuStock.bufferHealth === 'Adequate'
                                    ? 'bg-blue-50 text-blue-800 border-blue-200'
                                    : 'bg-amber-50 text-amber-800 border-amber-200'
                                }`}
                              >
                                {skuStock.bufferHealth}
                              </span>
                            </td>
                            <td className="py-2.5 px-3 text-center">
                              <button
                                onClick={() => onOpenStockTransfer(skuStock.sku, hubName, skuStock.shortageUnits || 50)}
                                className="px-2.5 py-1 bg-slate-100 hover:bg-blue-600 hover:text-white text-slate-700 border border-slate-200 rounded text-[11px] font-bold transition-all"
                              >
                                Dispatch
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Hub Footer Action */}
                  <div className="p-3 bg-slate-50/50 border-t border-slate-100 flex items-center justify-between text-xs">
                    <span className="text-slate-500 text-[11px]">
                      Reserved buffer: {totalReservedInHub.toLocaleString('en-IN')} units earmarked for scheduled POD dispatches
                    </span>
                    <button
                      onClick={() => onOpenStockTransfer('SLP-1001', hubName, 1000)}
                      className="text-blue-600 hover:text-blue-800 font-bold text-xs flex items-center gap-1"
                    >
                      <span>Inter-Hub Rebalance</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 6. TAB 3: Marketplace Channel Distribution Matrix */}
      {activeTab === 'marketplaces_matrix' && (
        <div className="space-y-6">
          <div className="p-4 bg-purple-50/70 border border-purple-200 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs text-purple-950">
            <div>
              <strong className="text-purple-950">Marketplace Channel Matrix:</strong> Answers which marketplace has which SKUs at which dark stores, active channel inventory, live prices, and fulfillment POD networks.
            </div>
            <div className="text-purple-700 font-bold">
              4 Quick-Commerce & E-Commerce Channels Active
            </div>
          </div>

          {/* Channel Overview Bento Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {marketplaceSummary.map((mp) => (
              <div
                key={mp.key}
                className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3"
              >
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <div>
                    <h4 className="font-bold text-slate-900 text-sm">{mp.name}</h4>
                    <span className="text-[10px] text-slate-500 uppercase font-semibold">10-Min Micro Fulfillment</span>
                  </div>
                  <span className="px-2 py-0.5 bg-slate-100 text-slate-700 font-mono text-xs font-bold rounded">
                    {mp.storesCount} PODs
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-600">
                    <span>Available Stock:</span>
                    <strong className="text-slate-900 font-mono">{mp.totalUnits.toLocaleString('en-IN')} units</strong>
                  </div>
                  <div className="flex justify-between text-slate-600">
                    <span>Active SKUs:</span>
                    <strong className="text-blue-700 font-mono">{mp.skusCount} Unique SKUs</strong>
                  </div>
                  <div className="flex justify-between text-slate-600">
                    <span>Avg Delivery SLA:</span>
                    <span className="text-slate-800 font-medium">10 - 15 mins</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100">
                  <button
                    onClick={() => {
                      setSelectedMarketplaceFilter(mp.key);
                      setActiveTab('dark_stores_skus');
                    }}
                    className="w-full py-1.5 bg-slate-50 hover:bg-blue-50 hover:text-blue-700 border border-slate-200 text-slate-700 text-xs font-bold rounded-lg transition-colors flex items-center justify-center space-x-1"
                  >
                    <span>View {mp.name} Dark Stores</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Cross-Marketplace SKU Matrix Pivot Table */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="p-4 border-b border-slate-200 bg-slate-50/70 flex items-center justify-between">
              <div>
                <h3 className="font-bold text-slate-900 text-xs uppercase tracking-wider">
                  Cross-Channel SKU Availability & Dark Store Deployment
                </h3>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  Detailed distribution breakdown showing which marketplace has which SKU at which dark stores
                </p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-700 uppercase">
                    <th className="py-3 px-4">SKU & Product</th>
                    <th className="py-3 px-3">Target MAP</th>
                    <th className="py-3 px-3">Blinkit PODs</th>
                    <th className="py-3 px-3">Zepto PODs</th>
                    <th className="py-3 px-3">Instamart PODs</th>
                    <th className="py-3 px-3">JioMart PODs</th>
                    <th className="py-3 px-4 text-right">Total Channel Stock</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {skus.map((sku) => {
                    const blinkitStores = darkStores.filter((d) => d.sku === sku.sku && String(d.platform).toLowerCase() === 'blinkit');
                    const zeptoStores = darkStores.filter((d) => d.sku === sku.sku && String(d.platform).toLowerCase() === 'zepto');
                    const instamartStores = darkStores.filter((d) => d.sku === sku.sku && String(d.platform).toLowerCase() === 'instamart');
                    const jiomartStores = darkStores.filter((d) => d.sku === sku.sku && String(d.platform).toLowerCase() === 'jiomart');

                    const blinkitUnits = blinkitStores.reduce((sum, d) => sum + (d.availableStock ?? 0), 0);
                    const zeptoUnits = zeptoStores.reduce((sum, d) => sum + (d.availableStock ?? 0), 0);
                    const instamartUnits = instamartStores.reduce((sum, d) => sum + (d.availableStock ?? 0), 0);
                    const jiomartUnits = jiomartStores.reduce((sum, d) => sum + (d.availableStock ?? 0), 0);
                    const totalAcross = blinkitUnits + zeptoUnits + instamartUnits + jiomartUnits;

                    return (
                      <tr key={sku.sku} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3 px-4">
                          <span className="font-mono font-bold text-slate-900 block">{sku.sku}</span>
                          <span className="text-slate-600 text-[11px] block">{sku.name}</span>
                        </td>
                        <td className="py-3 px-3 font-mono font-semibold text-slate-800">
                          {formatINR(sku.targetMap)}
                        </td>
                        <td className="py-3 px-3">
                          <div className="font-mono font-bold text-slate-900">{blinkitUnits} units</div>
                          <div className="text-[10px] text-slate-500">{blinkitStores.length} Dark Stores</div>
                        </td>
                        <td className="py-3 px-3">
                          <div className="font-mono font-bold text-slate-900">{zeptoUnits} units</div>
                          <div className="text-[10px] text-slate-500">{zeptoStores.length} Dark Stores</div>
                        </td>
                        <td className="py-3 px-3">
                          <div className="font-mono font-bold text-slate-900">{instamartUnits} units</div>
                          <div className="text-[10px] text-slate-500">{instamartStores.length} Dark Stores</div>
                        </td>
                        <td className="py-3 px-3">
                          <div className="font-mono font-bold text-slate-900">{jiomartUnits} units</div>
                          <div className="text-[10px] text-slate-500">{jiomartStores.length} Dark Stores</div>
                        </td>
                        <td className="py-3 px-4 text-right">
                          <span className="font-mono font-bold text-blue-700 text-sm">
                            {totalAcross.toLocaleString('en-IN')}
                          </span>
                          <span className="text-[10px] text-slate-400 block">units in PODs</span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 7. TAB 4: Manufacturers & Plants Supply Matrix */}
      {activeTab === 'manufacturers_supply' && (
        <div className="space-y-6">
          <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs text-emerald-950">
            <div>
              <strong className="text-emerald-950">Manufacturer & Factory Inventory:</strong> Answers which manufacturer plant has what quantity of each SKU, finished goods in factory warehouse, active WIP production, and lead time to Mother Hubs.
            </div>
            <div className="text-emerald-800 font-bold">
              Total Factory Finished Goods: {totalManufacturerUnits.toLocaleString('en-IN')} units
            </div>
          </div>

          {/* Plant Bento Cards */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
            {uniquePlants.map(([plantName, items]) => {
              const mfgName = items[0]?.manufacturerName || 'Sleep Matrix Mfg';
              const location = items[0]?.location || 'India';
              const pincode = items[0]?.pincode || '560058';
              const totalFg = items.reduce((sum, i) => sum + i.factoryFinishedGoodsStock, 0);
              const totalWip = items.reduce((sum, i) => sum + i.workInProgressUnits, 0);
              const destinationHub = items[0]?.destinationMotherHub || 'Nelamangala Mother Hub';

              return (
                <div key={plantName} className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
                  {/* Plant Header */}
                  <div className="p-4 bg-slate-50 border-b border-slate-200 space-y-1">
                    <div className="flex items-center space-x-2">
                      <Factory className="w-4 h-4 text-indigo-600" />
                      <h3 className="font-bold text-slate-900 text-xs">{plantName}</h3>
                    </div>
                    <div className="text-[11px] text-slate-500 font-medium">
                      {mfgName} • {location} ({pincode})
                    </div>
                    <div className="text-[10px] text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded inline-block font-semibold mt-1">
                      Feeds: {destinationHub}
                    </div>
                  </div>

                  {/* Plant Stats Bar */}
                  <div className="grid grid-cols-2 p-3 bg-slate-50/50 border-b border-slate-100 text-center gap-2">
                    <div className="p-2 bg-white rounded-lg border border-slate-100">
                      <span className="text-[10px] text-slate-500 uppercase block">Finished Goods</span>
                      <span className="font-mono font-bold text-slate-900 text-sm">
                        {totalFg.toLocaleString('en-IN')}
                      </span>
                    </div>
                    <div className="p-2 bg-white rounded-lg border border-slate-100">
                      <span className="text-[10px] text-slate-500 uppercase block">WIP In-Production</span>
                      <span className="font-mono font-bold text-indigo-700 text-sm">
                        {totalWip.toLocaleString('en-IN')}
                      </span>
                    </div>
                  </div>

                  {/* SKU Supply Table */}
                  <div className="overflow-x-auto flex-1">
                    <table className="w-full text-left text-xs">
                      <thead>
                        <tr className="bg-slate-50/60 border-b border-slate-100 text-[10px] font-bold text-slate-600 uppercase">
                          <th className="py-2 px-3">SKU</th>
                          <th className="py-2 px-2 text-right">FG Stock</th>
                          <th className="py-2 px-2 text-right">WIP</th>
                          <th className="py-2 px-2 text-right">Daily Rate</th>
                          <th className="py-2 px-2 text-right">Lead Time</th>
                          <th className="py-2 px-3">Pass Rate</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {items.map((mfg) => (
                          <tr key={mfg.id} className="hover:bg-slate-50/80 transition-colors">
                            <td className="py-2.5 px-3">
                              <span className="font-mono font-bold text-slate-900 block">{mfg.sku}</span>
                              <span className="text-[10px] text-slate-500 truncate block max-w-[120px]" title={mfg.productName}>
                                {mfg.productName}
                              </span>
                            </td>
                            <td className="py-2.5 px-2 text-right font-mono font-bold text-slate-900">
                              {mfg.factoryFinishedGoodsStock.toLocaleString('en-IN')}
                            </td>
                            <td className="py-2.5 px-2 text-right font-mono text-indigo-700">
                              {mfg.workInProgressUnits.toLocaleString('en-IN')}
                            </td>
                            <td className="py-2.5 px-2 text-right font-mono text-slate-600">
                              {mfg.dailyProductionRate}/d
                            </td>
                            <td className="py-2.5 px-2 text-right font-mono text-slate-600">
                              {mfg.leadTimeToMotherHubHours}h
                            </td>
                            <td className="py-2.5 px-3">
                              <span className="px-1.5 py-0.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded text-[10px] font-bold">
                                {mfg.qualityPassRate}%
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Plant Footer */}
                  <div className="p-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs">
                    <span className="text-slate-500 text-[10px]">
                      Batch: {items[0]?.activeBatchNumber || 'BAT-2026-08A'}
                    </span>
                    <button
                      onClick={() => onOpenStockTransfer(items[0]?.sku || 'SLP-1001', destinationHub, 1000)}
                      className="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded text-[11px] font-bold transition-colors flex items-center gap-1 shadow-2xs"
                    >
                      <span>Dispatch to Hub</span>
                      <Truck className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 8. TAB 5: End-to-End Pipeline & Rebalance Flow */}
      {activeTab === 'pipeline_flow' && (
        <div className="space-y-6">
          <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700">
            <strong className="text-slate-900">4-Stage Supply Chain Topology:</strong> Visual flow tracking finished products from manufacturing plant to regional mother hubs, micro dark store PODs, and end customers.
          </div>

          {/* Visual Step Pipeline Flow */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 relative">
            {/* Stage 1 */}
            <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3 relative">
              <div className="flex items-center space-x-2">
                <span className="w-6 h-6 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center shrink-0">
                  1
                </span>
                <h4 className="font-bold text-slate-900 text-xs">Manufacturer Plants</h4>
              </div>
              <div className="space-y-1.5 text-xs text-slate-600">
                <div>• 3 Specialized Facilities (Peenya, Chakan, Manesar)</div>
                <div>• Factory FG: <strong className="text-slate-900">{totalManufacturerUnits.toLocaleString('en-IN')} units</strong></div>
                <div>• Daily Rate: 1,650 units/day across lines</div>
                <div>• Quality Pass Rate: 99.4%</div>
              </div>
              <div className="pt-2 border-t border-slate-100 text-[10px] text-slate-500 flex items-center gap-1">
                <Truck className="w-3 h-3 text-indigo-600" />
                <span>Transit: 4 - 8 hrs to Mother Hub</span>
              </div>
            </div>

            {/* Stage 2 */}
            <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3 relative">
              <div className="flex items-center space-x-2">
                <span className="w-6 h-6 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center shrink-0">
                  2
                </span>
                <h4 className="font-bold text-slate-900 text-xs">Mother Hub Reserves</h4>
              </div>
              <div className="space-y-1.5 text-xs text-slate-600">
                <div>• 4 Regional Hubs (BLR, BOM, DEL, HYD)</div>
                <div>• Buffer Stock: <strong className="text-blue-700">{totalMotherHubUnits.toLocaleString('en-IN')} units</strong></div>
                <div>• Buffer Health: 98% Optimal</div>
                <div>• Dispatch SLA: 2 - 4 hours to PODs</div>
              </div>
              <div className="pt-2 border-t border-slate-100 text-[10px] text-slate-500 flex items-center gap-1">
                <Zap className="w-3 h-3 text-blue-600" />
                <span>1-Click Automated Rebalancing</span>
              </div>
            </div>

            {/* Stage 3 */}
            <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3 relative">
              <div className="flex items-center space-x-2">
                <span className="w-6 h-6 rounded-full bg-amber-500 text-white font-bold text-xs flex items-center justify-center shrink-0">
                  3
                </span>
                <h4 className="font-bold text-slate-900 text-xs">Dark Store PODs</h4>
              </div>
              <div className="space-y-1.5 text-xs text-slate-600">
                <div>• {darkStores.length} Micro-Fulfillment Nodes</div>
                <div>• Total Stock: <strong className="text-slate-900">{totalDarkStoreUnits.toLocaleString('en-IN')} units</strong></div>
                <div>• Stock Velocity: 18 - 35 units/day</div>
                <div>• Runway Threshold: 36 hrs avg</div>
              </div>
              <div className="pt-2 border-t border-slate-100 text-[10px] text-slate-500 flex items-center gap-1">
                <Clock className="w-3 h-3 text-amber-600" />
                <span>Autonomous Stock Alert Guardrails</span>
              </div>
            </div>

            {/* Stage 4 */}
            <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3 relative">
              <div className="flex items-center space-x-2">
                <span className="w-6 h-6 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center shrink-0">
                  4
                </span>
                <h4 className="font-bold text-slate-900 text-xs">Marketplaces & Delivery</h4>
              </div>
              <div className="space-y-1.5 text-xs text-slate-600">
                <div>• Blinkit, Zepto, Swiggy Instamart, JioMart</div>
                <div>• SLA: 10 - 15 min doorstep delivery</div>
                <div>• Buy Box Win Rate: 94.2%</div>
                <div>• Real-time MAP Guardrails Active</div>
              </div>
              <div className="pt-2 border-t border-slate-100 text-[10px] text-emerald-700 font-bold flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" />
                <span>Doorstep Delivery Active</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 9. TAB 6: Batch & Shelf Life Tracker */}
      {activeTab === 'batch_expiry' && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="p-4 border-b border-slate-200 bg-slate-50/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                Batch Shelf Life & FEFO Quality Audit (FEFO Engine)
              </h3>
              <p className="text-[11px] text-slate-500 mt-0.5">
                First-Expiry-First-Out (FEFO) audit across manufacturing plants and hub warehouses with AI clearance playbooks.
              </p>
            </div>
            <div className="flex items-center space-x-2 text-[11px]">
              <span className="px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded-lg border border-emerald-200">Fresh: 5</span>
              <span className="px-2.5 py-1 bg-amber-50 text-amber-800 font-bold rounded-lg border border-amber-200">Expiring Soon: 2</span>
              <span className="px-2.5 py-1 bg-rose-50 text-rose-800 font-bold rounded-lg border border-rose-200">Critical: 1</span>
            </div>
          </div>
          <div className="divide-y divide-slate-100">
            {filteredBatchSkus.length === 0 ? (
              <div className="p-12 text-center text-slate-500 text-xs">
                No batches match the selected filter criteria ("{selectedStockStatusFilter}", SKU: {selectedSkuFilter}, Search: "{searchQuery}").
              </div>
            ) : (
              filteredBatchSkus.map(({ s, idx, daysRemaining, healthPct, statusText, badgeClass, textClass, batchCode, mfgDate, expDate, suggestion }) => {
              const invVal = s.sellingPrice * (s.motherHubStock || 50000);

              return (
                <div key={s.sku} className="p-4 space-y-3 hover:bg-slate-50/60 transition-colors">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
                    <div>
                      <div className="font-bold text-slate-900 flex items-center space-x-2">
                        <span>{s.name}</span>
                        <span className="font-mono text-[10px] text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">{s.sku}</span>
                      </div>
                      <div className="text-slate-500 font-mono text-[10px] mt-0.5">
                        Batch: {batchCode} • Mfg: {mfgDate} • Expiry: {expDate} • Plant: Peenya Facility
                      </div>
                    </div>

                    <div className="flex items-center space-x-6">
                      <div>
                        <span className="text-[10px] text-slate-400 uppercase font-semibold block">Shelf Life Remaining</span>
                        <span className={`font-bold ${textClass}`}>{daysRemaining} Days ({healthPct}% Health)</span>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-400 uppercase font-semibold block">Inventory Value</span>
                        <span className="font-mono font-bold text-slate-800">
                          {formatINR(invVal, { abbreviate: true })}
                        </span>
                      </div>
                      <span className={`px-2.5 py-1 border text-[10px] font-bold rounded-lg ${badgeClass}`}>
                        {statusText}
                      </span>
                    </div>
                  </div>

                  {/* Stock Clearance Suggestion Banner */}
                  {(idx === 1 || idx === 2 || idx === 4) && (
                    <div className="p-2.5 bg-amber-50/70 rounded-lg border border-amber-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[11px]">
                      <div className="flex items-center space-x-2 text-amber-900">
                        <Sparkles className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                        <span><strong>AI Clearance Playbook:</strong> {suggestion}</span>
                      </div>
                      <button
                        onClick={() => alert(`Executed clearance playbook for batch ${batchCode} (${s.name}): "${suggestion}" successfully applied across channels.`)}
                        className="px-3 py-1 bg-amber-600 hover:bg-amber-700 text-white font-bold rounded shadow-2xs transition-colors shrink-0 text-[10px]"
                      >
                        Execute Playbook ⚡
                      </button>
                    </div>
                  )}
                </div>
              );
            })
          )}
          </div>
        </div>
      )}
    </div>
  );
};
