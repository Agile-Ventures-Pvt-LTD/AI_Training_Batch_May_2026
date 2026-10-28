import React, { useState, useRef, useMemo } from 'react';
import {
  Upload,
  FileSpreadsheet,
  Link,
  Download,
  CheckCircle2,
  RefreshCw,
  Edit3,
  Save,
  Search,
  Database,
  Table,
  Check,
  AlertTriangle,
  ArrowRight,
  RotateCcw,
  Store,
  Tag,
  ShieldAlert,
  Layers,
  Package,
  Factory,
  Truck,
  Filter,
  Zap,
  ArrowUpDown,
  Building2
} from 'lucide-react';
import { useData } from '../../context/DataContext';
import { SKUListing, ChannelPricingItem, MarketplaceId, DarkStoreInventory, AlertAnomaly, MotherHubSkuStock, ManufacturerSupplyInfo } from '../../types';
import { formatINR } from '../../data/mockData';
import { StockTransferModal } from '../StockTransferModal';
import { EmailDispatchModal } from '../EmailDispatchModal';

export const DatasetSyncView: React.FC = () => {
  const {
    skus,
    darkStores,
    motherHubSkuStock,
    manufacturerSupply,
    mapBreaches,
    channelPricing,
    alerts,
    transferLogs,
    syncState,
    updateSKU,
    updateDarkStore,
    updateMotherHubSkuStock,
    updateManufacturerSupply,
    pushDarkStoreToGoogleSheet,
    pushMotherHubToGoogleSheet,
    pushManufacturerSupplyToGoogleSheet,
    updateAlert,
    pushAlertToGoogleSheet,
    updateChannelPricing,
    pushChannelPricingToGoogleSheet,
    exportToExcel,
    exportTransferLogsToExcel,
    exportAlertsLogToExcel,
    importFromExcel,
    syncFromGoogleSheet,
    pushFullDatasetToGoogleSheet,
    googleSheetWebhookUrl,
    setGoogleSheetWebhookUrl,
    pushToGoogleSheet,
    resetToDefaults
  } = useData();

  const [activeSheetTab, setActiveSheetTab] = useState<'sku_master' | 'dark_stores' | 'channel_pricing' | 'alerts_log' | 'mother_hubs' | 'manufacturers_supply' | 'transfer_logs'>('sku_master');
  const [googleSheetUrlInput, setGoogleSheetUrlInput] = useState(
    syncState.googleSheetUrl || 'https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit'
  );
  const [webhookUrlInput, setWebhookUrlInput] = useState(googleSheetWebhookUrl || '');
  const [isSyncingSheet, setIsSyncingSheet] = useState(false);
  const [isPushingSheet, setIsPushingSheet] = useState(false);
  const [isPushingRowId, setIsPushingRowId] = useState<string | null>(null);
  const [syncFeedback, setSyncFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const [searchQuery, setSearchQuery] = useState('');

  // Tab-specific SKU & category filters
  const [darkStoreSkuFilter, setDarkStoreSkuFilter] = useState<string>('all');
  const [darkStorePlatformFilter, setDarkStorePlatformFilter] = useState<string>('all');
  const [darkStoreStatusFilter, setDarkStoreStatusFilter] = useState<string>('all');
  const [darkStoreNameFilter, setDarkStoreNameFilter] = useState<string>('');

  const [motherHubSkuFilter, setMotherHubSkuFilter] = useState<string>('all');
  const [mfgSkuFilter, setMfgSkuFilter] = useState<string>('all');

  // Stock Transfer Modal state
  const [isTransferModalOpen, setIsTransferModalOpen] = useState(false);
  const [transferModalProps, setTransferModalProps] = useState<{
    sku?: string;
    productName?: string;
    darkStoreName?: string;
    defaultDarkStoreId?: string;
    defaultHub?: string;
    suggestedUnits?: number;
  }>({});

  // Editing state for SKU Master
  const [editingSkuCode, setEditingSkuCode] = useState<string | null>(null);
  const [skuEditForm, setSkuEditForm] = useState<Partial<SKUListing>>({});
  const [selectedMotherHubInspector, setSelectedMotherHubInspector] = useState<string>('Bengaluru Central Mother Hub (Nelamangala)');
  const [selectedDarkStoreInspector, setSelectedDarkStoreInspector] = useState<string>('BLNK-BLR-HSR-01');
  const [selectedEmailAlert, setSelectedEmailAlert] = useState<AlertAnomaly | null>(null);
  const [isEmailModalOpen, setIsEmailModalOpen] = useState<boolean>(false);

  // Editing state for Channel Pricing & MAP
  const [editingPricingId, setEditingPricingId] = useState<string | null>(null);
  const [pricingEditForm, setPricingEditForm] = useState<Partial<ChannelPricingItem>>({});

  // Editing state for Dark Stores (Sheet 2)
  const [editingStoreKey, setEditingStoreKey] = useState<string | null>(null); // storeId:sku
  const [storeEditForm, setStoreEditForm] = useState<Partial<DarkStoreInventory>>({});
  const [isPushingStoreRowId, setIsPushingStoreRowId] = useState<string | null>(null);

  // Editing state for Mother Hubs (Sheet 5)
  const [editingHubStockId, setEditingHubStockId] = useState<string | null>(null);
  const [hubStockEditForm, setHubStockEditForm] = useState<Partial<MotherHubSkuStock>>({});

  // Editing state for Manufacturer Supply (Sheet 6)
  const [editingMfgId, setEditingMfgId] = useState<string | null>(null);
  const [mfgEditForm, setMfgEditForm] = useState<Partial<ManufacturerSupplyInfo>>({});



  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const res = await importFromExcel(file);
    if (res.success) {
      setSyncFeedback({ type: 'success', message: res.message });
    } else {
      setSyncFeedback({ type: 'error', message: res.message });
    }
  };

  const handleSyncGoogleSheetClick = async () => {
    if (!googleSheetUrlInput) return;
    setIsSyncingSheet(true);
    setSyncFeedback(null);
    const res = await syncFromGoogleSheet(googleSheetUrlInput);
    setIsSyncingSheet(false);
    if (res.success) {
      setSyncFeedback({ type: 'success', message: res.message });
    } else {
      setSyncFeedback({ type: 'error', message: res.message });
    }
  };

  const handleSaveWebhook = () => {
    setGoogleSheetWebhookUrl(webhookUrlInput);
    setSyncFeedback({ type: 'success', message: 'Google Sheets Webhook URL saved for two-way synchronization!' });
  };

  const handlePushAllToSheet = async () => {
    if (!googleSheetWebhookUrl && !webhookUrlInput) {
      setSyncFeedback({
        type: 'error',
        message: 'Please provide your Google Apps Script Webhook URL below to enable direct two-way writing.'
      });
      return;
    }
    setIsPushingSheet(true);
    const targetUrl = webhookUrlInput || googleSheetWebhookUrl;
    setGoogleSheetWebhookUrl(targetUrl);

    let successCount = 0;
    if (activeSheetTab === 'channel_pricing') {
      for (const cp of (channelPricing || [])) {
        const res = await pushChannelPricingToGoogleSheet(cp);
        if (res.success) successCount++;
      }
      setSyncFeedback({
        type: 'success',
        message: `Pushed ${successCount}/${channelPricing?.length || 0} Channel Pricing records directly to Google Sheets (3_Channel_Pricing_MAP)!`
      });
    } else if (activeSheetTab === 'dark_stores') {
      for (const d of (darkStores || [])) {
        const res = await pushDarkStoreToGoogleSheet(d);
        if (res.success) successCount++;
      }
      setSyncFeedback({
        type: 'success',
        message: `Pushed ${successCount}/${darkStores?.length || 0} Dark Store records directly to Google Sheets (2_Dark_Stores_Inventory)!`
      });
    } else if (activeSheetTab === 'alerts_log') {
      for (const a of (alerts || [])) {
        const res = await pushAlertToGoogleSheet(a);
        if (res.success) successCount++;
      }
      setSyncFeedback({
        type: 'success',
        message: `Pushed ${successCount}/${alerts?.length || 0} Alert/Trigger logs directly to Google Sheets (4_Triggers_Alerts_Log)!`
      });
    } else if (activeSheetTab === 'mother_hubs') {
      for (const h of (motherHubSkuStock || [])) {
        const res = await pushMotherHubToGoogleSheet(h);
        if (res.success) successCount++;
      }
      setSyncFeedback({
        type: 'success',
        message: `Pushed ${successCount}/${motherHubSkuStock?.length || 0} Mother Hub stock buffers directly to Google Sheets (5_Mother_Hubs_Inventory)!`
      });
    } else if (activeSheetTab === 'manufacturers_supply') {
      for (const m of (manufacturerSupply || [])) {
        const res = await pushManufacturerSupplyToGoogleSheet(m);
        if (res.success) successCount++;
      }
      setSyncFeedback({
        type: 'success',
        message: `Pushed ${successCount}/${manufacturerSupply?.length || 0} Manufacturer supply lines directly to Google Sheets (6_Manufacturers_Supply)!`
      });
    } else {
      for (const s of skus) {
        const res = await pushToGoogleSheet(s.sku);
        if (res.success) successCount++;
      }
      setSyncFeedback({
        type: 'success',
        message: `Pushed latest pricing and stock parameters for ${successCount}/${skus.length} SKUs to Google Sheets (1_SKU_Master)!`
      });
    }
    setIsPushingSheet(false);
  };

  const handleStartEditStore = (store: DarkStoreInventory) => {
    setEditingStoreKey(`${store.storeId}:${store.sku}`);
    setStoreEditForm({
      storeId: store.storeId,
      storeName: store.storeName,
      sku: store.sku,
      availableStock: store.availableStock,
      safetyThreshold: store.safetyThreshold || 15,
      dailyVelocity: store.dailyVelocity || 40,
      deliverySlaMins: store.deliverySlaMins,
      motherHubStock: store.motherHubStock,
      motherHubName: store.motherHubName
    });
  };

  const handleSaveStoreEdit = async (storeId: string, skuCode: string, pushToSheet = false) => {
    if (!storeEditForm) return;
    const availableStock = Number(storeEditForm.availableStock ?? 0);
    const safety = Number(storeEditForm.safetyThreshold ?? 15);
    const status = availableStock <= 0 ? 'Out Of Stock' : availableStock <= safety ? 'Low Stock' : 'In Stock';
    const updated: Partial<DarkStoreInventory> = {
      ...storeEditForm,
      availableStock,
      status: status as any
    };

    // Update in Context (which triggers cross-sheet SKU and alert synchronization)
    updateDarkStore(storeId, updated, skuCode);
    setEditingStoreKey(null);

    const targetStore = darkStores.find((d) => d.storeId === storeId && d.sku === skuCode);
    if (pushToSheet && targetStore) {
      const fullStore = { ...targetStore, ...updated } as DarkStoreInventory;
      setIsPushingStoreRowId(storeId);
      const res = await pushDarkStoreToGoogleSheet(fullStore);
      setIsPushingStoreRowId(null);
      if (res.success) {
        setSyncFeedback({ type: 'success', message: res.message });
      } else {
        setSyncFeedback({ type: 'error', message: res.message });
      }
    } else {
      setSyncFeedback({
        type: 'success',
        message: `Updated Dark Store ${storeId} (${skuCode})! SKU Master total pod stock recalculated.`
      });
    }
  };

  const handleOpenTransferModal = (store: DarkStoreInventory) => {
    setTransferModalProps({
      sku: store.sku,
      productName: store.productName,
      darkStoreName: `${store.storeName} (${store.city})`,
      defaultDarkStoreId: store.storeId,
      defaultHub: store.motherHubName,
      suggestedUnits: Math.max(50, ((store.safetyThreshold || 25) * 4) - store.availableStock)
    });
    setIsTransferModalOpen(true);
  };

  const handleStartEditHubStock = (hub: MotherHubSkuStock) => {
    setEditingHubStockId(hub.id);
    setHubStockEditForm({
      id: hub.id,
      quantityAvailable: hub.quantityAvailable,
      safetyStockThreshold: hub.safetyStockThreshold,
      reservedQuantity: hub.reservedQuantity,
      dispatchSlaHours: hub.dispatchSlaHours
    });
  };

  const handleSaveHubStockEdit = (id: string) => {
    if (!hubStockEditForm) return;
    updateMotherHubSkuStock(id, hubStockEditForm);
    setEditingHubStockId(null);
    setSyncFeedback({
      type: 'success',
      message: `Updated Mother Hub stock buffer! Total hub reserves synced to SKU Master.`
    });
  };

  const handleStartEditMfg = (mfg: ManufacturerSupplyInfo) => {
    setEditingMfgId(mfg.id);
    setMfgEditForm({
      id: mfg.id,
      factoryFinishedGoodsStock: mfg.factoryFinishedGoodsStock,
      workInProgressUnits: mfg.workInProgressUnits,
      dailyProductionRate: mfg.dailyProductionRate,
      leadTimeToMotherHubHours: mfg.leadTimeToMotherHubHours
    });
  };

  const handleSaveMfgEdit = (id: string) => {
    if (!mfgEditForm) return;
    updateManufacturerSupply(id, mfgEditForm);
    setEditingMfgId(null);
    setSyncFeedback({
      type: 'success',
      message: `Updated Manufacturer production parameters locally!`
    });
  };



  const handleStartEditSku = (sku: SKUListing) => {
    setEditingSkuCode(sku.sku);
    setSkuEditForm({
      sku: sku.sku,
      name: sku.name,
      productType: sku.productType,
      category: sku.category,
      brand: sku.brand,
      mrp: sku.mrp,
      targetMap: sku.targetMap,
      sellingPrice: sku.sellingPrice,
      dailyVelocity: sku.dailyVelocity,
      darkStoreStock: sku.darkStoreStock,
      motherHubStock: sku.motherHubStock,
      revenueAtRisk: sku.revenueAtRisk
    });
  };

  const handleSaveSkuEdit = (skuCode: string) => {
    updateSKU(skuCode, skuEditForm);
    setEditingSkuCode(null);
    setSyncFeedback({
      type: 'success',
      message: `Updated ${skuCode} locally. Multi-directional prices and dark store targets synced!`
    });
  };

  const handleStartEditPricing = (item: ChannelPricingItem) => {
    setEditingPricingId(item.id);
    setPricingEditForm({
      id: item.id,
      sku: item.sku,
      productName: item.productName,
      marketplace: item.marketplace,
      currentSellingPrice: item.currentSellingPrice,
      targetMap: item.targetMap,
      buyBoxOwner: item.buyBoxOwner,
      inStock: item.inStock,
      status: item.status
    });
  };

  const handleSavePricingEdit = async (itemId: string, pushToSheet = false) => {
    if (!pricingEditForm) return;

    const targetMap = Number(pricingEditForm.targetMap || 0);
    const currentSellingPrice = Number(pricingEditForm.currentSellingPrice || 0);
    const mapBreached = targetMap > 0 && currentSellingPrice < targetMap;
    const priceDelta = currentSellingPrice - targetMap;

    const updatedItem: ChannelPricingItem = {
      id: itemId,
      sku: pricingEditForm.sku || '',
      productName: pricingEditForm.productName || '',
      marketplace: (pricingEditForm.marketplace as MarketplaceId) || 'amazon',
      currentSellingPrice,
      targetMap,
      mapBreached,
      priceDelta,
      buyBoxOwner: pricingEditForm.buyBoxOwner || 'Unknown',
      inStock: pricingEditForm.inStock ?? true,
      shareOfSearch: 30,
      revenue30d: currentSellingPrice * 50 * 30,
      status: mapBreached ? 'Active Breach' : 'Compliant',
      complianceAction: mapBreached ? 'Auto Cease-and-Desist Notice Drafted' : 'Active - Price Protected'
    };

    updateChannelPricing(itemId, updatedItem);
    setEditingPricingId(null);

    if (pushToSheet) {
      setIsPushingRowId(itemId);
      const res = await pushChannelPricingToGoogleSheet(updatedItem);
      setIsPushingRowId(null);
      if (res.success) {
        setSyncFeedback({ type: 'success', message: res.message });
      } else {
        setSyncFeedback({ type: 'error', message: res.message });
      }
    } else {
      setSyncFeedback({
        type: 'success',
        message: `Updated Channel Price for ${updatedItem.sku} (${String(updatedItem.marketplace).toUpperCase()}) locally!`
      });
    }
  };

  // Filtered dataset subsets
  const filteredSkus = useMemo(() => {
    return skus.filter(
      (s) =>
        s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        s.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (s.category && s.category.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (s.brand && s.brand.toLowerCase().includes(searchQuery.toLowerCase()))
    );
  }, [skus, searchQuery]);

  const filteredStores = useMemo(() => {
    return darkStores.filter((d) => {
      const matchSearch =
        d.storeName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.storeId.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.city.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.platform.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (d.sku && d.sku.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (d.productName && d.productName.toLowerCase().includes(searchQuery.toLowerCase()));

      const matchStoreName = !darkStoreNameFilter || darkStoreNameFilter.trim() === '' ||
        d.storeName.toLowerCase().includes(darkStoreNameFilter.toLowerCase()) ||
        d.storeId.toLowerCase().includes(darkStoreNameFilter.toLowerCase()) ||
        d.city.toLowerCase().includes(darkStoreNameFilter.toLowerCase());

      const matchSku = darkStoreSkuFilter === 'all' || d.sku?.toLowerCase() === darkStoreSkuFilter.toLowerCase();
      const matchPlatform = darkStorePlatformFilter === 'all' || d.platform?.toLowerCase() === darkStorePlatformFilter.toLowerCase();
      const matchStatus = darkStoreStatusFilter === 'all' || d.status === darkStoreStatusFilter;

      return matchSearch && matchStoreName && matchSku && matchPlatform && matchStatus;
    });
  }, [darkStores, searchQuery, darkStoreNameFilter, darkStoreSkuFilter, darkStorePlatformFilter, darkStoreStatusFilter]);

  // Dark Store tab aggregate stats
  const darkStoreStats = useMemo(() => {
    const totalPods = filteredStores.length;
    const inStock = filteredStores.filter((d) => d.status === 'In Stock').length;
    const lowStock = filteredStores.filter((d) => d.status === 'Low Stock').length;
    const outOfStock = filteredStores.filter((d) => d.status === 'Out Of Stock').length;
    const totalUnits = filteredStores.reduce((sum, d) => sum + (d.availableStock || 0), 0);
    return { totalPods, inStock, lowStock, outOfStock, totalUnits };
  }, [filteredStores]);

  const filteredChannelPricing = useMemo(() => {
    return (channelPricing || []).filter(
      (cp) =>
        cp.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cp.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cp.marketplace.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cp.buyBoxOwner.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [channelPricing, searchQuery]);

  const filteredBreaches = useMemo(() => {
    return mapBreaches.filter(
      (m) =>
        m.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.channel.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.violatingSeller.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [mapBreaches, searchQuery]);

  const filteredAlerts = useMemo(() => {
    return alerts.filter(
      (a) =>
        a.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        a.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        a.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
        a.marketplace.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [alerts, searchQuery]);

  const filteredMotherHubs = useMemo(() => {
    return (motherHubSkuStock || []).filter((h) => {
      const matchSearch =
        h.hubName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        h.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        h.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        h.city.toLowerCase().includes(searchQuery.toLowerCase());
      const matchSku = motherHubSkuFilter === 'all' || h.sku?.toLowerCase() === motherHubSkuFilter.toLowerCase();
      return matchSearch && matchSku;
    });
  }, [motherHubSkuStock, searchQuery, motherHubSkuFilter]);

  const filteredManufacturerSupply = useMemo(() => {
    return (manufacturerSupply || []).filter((m) => {
      const matchSearch =
        m.manufacturerName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.plantName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.location.toLowerCase().includes(searchQuery.toLowerCase());
      const matchSku = mfgSkuFilter === 'all' || m.sku?.toLowerCase() === mfgSkuFilter.toLowerCase();
      return matchSearch && matchSku;
    });
  }, [manufacturerSupply, searchQuery, mfgSkuFilter]);

  const filteredTransferLogs = useMemo(() => {
    return (transferLogs || []).filter(
      (t) =>
        t.sku.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.trackingNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.sourceMotherHub.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.targetDarkStore.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [transferLogs, searchQuery]);

  return (
    <div id="dataset-sync-workspace" className="space-y-6">
      {/* 1. Header Banner */}
      <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-2xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 text-[11px] font-bold rounded-md uppercase tracking-wider">
              Dataset Ingestion & Live Multi-Sheet Sync
            </span>
            <span className="text-slate-400 text-xs">•</span>
            <span className="text-xs text-slate-500 font-medium">
              Source of Truth ({skus.length} SKUs across 4 Workbook Sheets)
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-1">
            Master Assortment Dataset & Two-Way Sync
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Upload custom Excel/CSV workbooks or connect a live Google Sheet URL to dynamically power all dashboard intelligence across all 4 sheets.
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <button
            onClick={exportToExcel}
            className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1.5 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Active Dataset (.xlsx)</span>
          </button>
        </div>
      </div>

      {/* Sync Feedback Toast */}
      {syncFeedback && (
        <div
          className={`p-4 rounded-xl text-xs font-medium flex items-center justify-between border ${
            syncFeedback.type === 'success'
              ? 'bg-emerald-50 text-emerald-900 border-emerald-200'
              : 'bg-red-50 text-red-900 border-red-200'
          }`}
        >
          <div className="flex items-center space-x-2">
            {syncFeedback.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-red-600 shrink-0" />
            )}
            <span>{syncFeedback.message}</span>
          </div>
          <button
            onClick={() => setSyncFeedback(null)}
            className="text-xs opacity-60 hover:opacity-100 font-bold ml-4"
          >
            ✕
          </button>
        </div>
      )}

      {/* 2. Ingestion Cards: Drag & Drop Upload + Google Sheets Sync */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Upload Excel / CSV */}
        <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-2xs space-y-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <FileSpreadsheet className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Upload Custom Excel Workbook</h3>
              <p className="text-xs text-slate-500">Parses all 4 sheets: SKU Master, Dark Stores, MAP Pricing & Alerts</p>
            </div>
          </div>

          <div
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-slate-200 hover:border-blue-400 bg-slate-50/60 hover:bg-blue-50/30 rounded-xl p-6 text-center cursor-pointer transition-colors space-y-2"
          >
            <Upload className="w-6 h-6 text-slate-400 mx-auto" />
            <div className="text-xs font-semibold text-slate-800">
              Click to browse or drop your spreadsheet file here
            </div>
            <p className="text-[11px] text-slate-500">
              Supports .xlsx and .xls with multi-tab structure.
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".xlsx,.xls,.csv"
              onChange={handleFileUpload}
              className="hidden"
            />
          </div>
        </div>

        {/* Connect Live Google Sheet */}
        <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-2xs space-y-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Link className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Live Google Sheet URL (Multi-Tab Ingestion)</h3>
              <p className="text-xs text-slate-500">Synchronizes all 4 workbook tabs directly from Google Drive</p>
            </div>
          </div>

          <div className="space-y-3">
            <div className="space-y-1">
              <label className="text-[11px] font-bold text-slate-600 uppercase">Google Sheet URL</label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="https://docs.google.com/spreadsheets/d/..."
                  value={googleSheetUrlInput}
                  onChange={(e) => setGoogleSheetUrlInput(e.target.value)}
                  className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 text-xs rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 font-mono text-slate-800"
                />
                <button
                  onClick={handleSyncGoogleSheetClick}
                  disabled={isSyncingSheet}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs font-bold rounded-lg shadow-2xs transition-colors shrink-0 flex items-center space-x-1.5"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncingSheet ? 'animate-spin' : ''}`} />
                  <span>{isSyncingSheet ? 'Syncing...' : 'Sync Sheet'}</span>
                </button>
              </div>
            </div>

            <div className="space-y-1 pt-1">
              <label className="text-[11px] font-bold text-slate-600 uppercase">Google Apps Script Webhook (2-Way Write)</label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="https://script.google.com/macros/s/.../exec"
                  value={webhookUrlInput}
                  onChange={(e) => setWebhookUrlInput(e.target.value)}
                  className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 text-xs rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 font-mono text-slate-800"
                />
                <button
                  onClick={handleSaveWebhook}
                  className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-700 text-xs font-semibold rounded-lg shrink-0"
                >
                  Save URL
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Multi-Sheet Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-200 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveSheetTab('sku_master')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeSheetTab === 'sku_master'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          <Table className="w-4 h-4" />
          <span>1. SKU Master ({skus.length} SKUs)</span>
        </button>

        <button
          onClick={() => setActiveSheetTab('dark_stores')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeSheetTab === 'dark_stores'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          <Store className="w-4 h-4" />
          <span>2. Dark Stores Inventory ({darkStores.length} Pods)</span>
        </button>

        <button
          onClick={() => setActiveSheetTab('channel_pricing')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeSheetTab === 'channel_pricing'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          <Tag className="w-4 h-4" />
          <span>3. Channel Pricing & MAP ({mapBreaches.length} Breaches)</span>
        </button>

        <button
          onClick={() => setActiveSheetTab('alerts_log')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeSheetTab === 'alerts_log'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          <ShieldAlert className="w-4 h-4" />
          <span>4. Triggers & Alerts Log ({alerts.length} Incidents)</span>
        </button>

        <button
          onClick={() => setActiveSheetTab('mother_hubs')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeSheetTab === 'mother_hubs'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          <Package className="w-4 h-4" />
          <span>5. Mother Hubs Inventory ({(motherHubSkuStock || []).length} Records)</span>
        </button>

        <button
          onClick={() => setActiveSheetTab('manufacturers_supply')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeSheetTab === 'manufacturers_supply'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          <Factory className="w-4 h-4" />
          <span>6. Manufacturers Supply ({(manufacturerSupply || []).length} Lines)</span>
        </button>

        <button
          onClick={() => setActiveSheetTab('transfer_logs')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeSheetTab === 'transfer_logs'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>7. Stock Transfer & Action Logs ({transferLogs.length} Records)</span>
        </button>
      </div>

      {/* 4. Active Sheet Content */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        {/* Search header */}
        <div className="p-4 border-b border-slate-200 bg-slate-50/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <Layers className="w-4 h-4 text-slate-600" />
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              {activeSheetTab === 'sku_master' && `Sheet: 1_SKU_Master (${filteredSkus.length} rows)`}
              {activeSheetTab === 'dark_stores' && `Sheet: 2_Dark_Stores_Inventory (${filteredStores.length} rows)`}
              {activeSheetTab === 'channel_pricing' && `Sheet: 3_Channel_Pricing_MAP (${filteredBreaches.length} rows)`}
              {activeSheetTab === 'alerts_log' && `Sheet: 4_Triggers_Alerts_Log (${filteredAlerts.length} rows)`}
              {activeSheetTab === 'mother_hubs' && `Sheet: 5_Mother_Hubs_Inventory (${filteredMotherHubs.length} rows)`}
              {activeSheetTab === 'manufacturers_supply' && `Sheet: 6_Manufacturers_Supply (${filteredManufacturerSupply.length} rows)`}
              {activeSheetTab === 'transfer_logs' && `Sheet: 7_Stock_Transfer_Audit_Logs (${filteredTransferLogs.length} rows)`}
            </h3>
          </div>

          <div className="flex items-center space-x-3">
            {activeSheetTab === 'alerts_log' && (
              <button
                onClick={exportAlertsLogToExcel}
                className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export Alerts Log (.xlsx)</span>
              </button>
            )}
            {activeSheetTab === 'transfer_logs' && (
              <button
                onClick={exportTransferLogsToExcel}
                className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export Logs (.xlsx)</span>
              </button>
            )}
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search across active sheet columns..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 pr-3 py-1.5 bg-white border border-slate-200 text-xs rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 w-72 text-slate-800"
              />
            </div>
          </div>
        </div>

        {/* TAB 1: SKU Master Table */}
        {activeSheetTab === 'sku_master' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-100 text-slate-600 uppercase text-[10px] font-bold border-b border-slate-200 tracking-wider">
                <tr>
                  <th className="py-3 px-4">SKU Code</th>
                  <th className="py-3 px-4">Product Name</th>
                  <th className="py-3 px-3">Category</th>
                  <th className="py-3 px-3 text-right">MRP</th>
                  <th className="py-3 px-3 text-right">Target MAP</th>
                  <th className="py-3 px-3 text-right">Selling Price</th>
                  <th className="py-3 px-3 text-right">Daily Velocity</th>
                  <th className="py-3 px-3 text-right">30D Gross</th>
                  <th className="py-3 px-3 text-center">Dark Store Stock</th>
                  <th className="py-3 px-3 text-center">Mother Hub Stock</th>
                  <th className="py-3 px-3 text-right">Revenue at Risk</th>
                  <th className="py-3 px-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredSkus.map((s) => {
                  const isEditing = editingSkuCode === s.sku;

                  if (isEditing) {
                    return (
                      <tr key={s.sku} className="bg-blue-50/50">
                        <td className="py-2.5 px-4 font-mono font-bold text-slate-900">{s.sku}</td>
                        <td className="py-2.5 px-4">
                          <input
                            type="text"
                            value={skuEditForm.name || ''}
                            onChange={(e) => setSkuEditForm({ ...skuEditForm, name: e.target.value })}
                            className="w-full px-2 py-1 bg-white border border-slate-300 rounded text-xs"
                          />
                        </td>
                        <td className="py-2.5 px-3">
                          <input
                            type="text"
                            value={skuEditForm.productType || skuEditForm.category || ''}
                            onChange={(e) => setSkuEditForm({ ...skuEditForm, productType: e.target.value, category: e.target.value })}
                            className="w-full px-2 py-1 bg-white border border-slate-300 rounded text-xs"
                          />
                        </td>
                        <td className="py-2.5 px-3 text-right">
                          <input
                            type="number"
                            value={skuEditForm.mrp || 0}
                            onChange={(e) => setSkuEditForm({ ...skuEditForm, mrp: Number(e.target.value) })}
                            className="w-20 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-right font-mono"
                          />
                        </td>
                        <td className="py-2.5 px-3 text-right">
                          <input
                            type="number"
                            value={skuEditForm.targetMap || 0}
                            onChange={(e) => setSkuEditForm({ ...skuEditForm, targetMap: Number(e.target.value) })}
                            className="w-20 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-right font-mono"
                          />
                        </td>
                        <td className="py-2.5 px-3 text-right">
                          <input
                            type="number"
                            value={skuEditForm.sellingPrice || 0}
                            onChange={(e) => setSkuEditForm({ ...skuEditForm, sellingPrice: Number(e.target.value) })}
                            className="w-20 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-right font-mono"
                          />
                        </td>
                        <td className="py-2.5 px-3 text-right">
                          <input
                            type="number"
                            value={skuEditForm.dailyVelocity || 0}
                            onChange={(e) => setSkuEditForm({ ...skuEditForm, dailyVelocity: Number(e.target.value) })}
                            className="w-16 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-right font-mono"
                          />
                        </td>
                        <td className="py-2.5 px-3 text-right font-mono text-slate-500">
                          {formatINR(s.grossSales30d || (s.sellingPrice * (s.dailyVelocity || 30) * 30))}
                        </td>
                        <td className="py-2.5 px-3 text-center">
                          <input
                            type="number"
                            value={skuEditForm.darkStoreStock ?? 0}
                            onChange={(e) => setSkuEditForm({ ...skuEditForm, darkStoreStock: Number(e.target.value) })}
                            className="w-16 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                          />
                        </td>
                        <td className="py-2.5 px-3 text-center">
                          <input
                            type="number"
                            value={skuEditForm.motherHubStock ?? 0}
                            onChange={(e) => setSkuEditForm({ ...skuEditForm, motherHubStock: Number(e.target.value) })}
                            className="w-20 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                          />
                        </td>
                        <td className="py-2.5 px-3 text-right font-mono text-rose-600 font-bold">
                          {formatINR(s.revenueAtRisk || 0)}
                        </td>
                        <td className="py-2.5 px-4 text-center">
                          <div className="flex items-center justify-center space-x-1.5">
                            <button
                              onClick={() => handleSaveSkuEdit(s.sku)}
                              className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold rounded shadow-2xs"
                            >
                              Save
                            </button>
                            <button
                              onClick={() => setEditingSkuCode(null)}
                              className="px-2 py-1 bg-slate-200 hover:bg-slate-300 text-slate-700 text-[11px] rounded"
                            >
                              Cancel
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  }

                  return (
                    <tr key={s.sku} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3 px-4 font-mono font-bold text-slate-900">{s.sku}</td>
                      <td className="py-3 px-4 font-semibold text-slate-900">{s.name}</td>
                      <td className="py-3 px-3 text-slate-600">{s.productType || s.category}</td>
                      <td className="py-3 px-3 text-right font-mono text-slate-500">{formatINR(s.mrp)}</td>
                      <td className="py-3 px-3 text-right font-mono text-slate-700">{formatINR(s.targetMap)}</td>
                      <td className="py-3 px-3 text-right font-mono font-bold text-slate-900">{formatINR(s.sellingPrice)}</td>
                      <td className="py-3 px-3 text-right font-mono text-slate-700">{s.dailyVelocity || 50} / day</td>
                      <td className="py-3 px-3 text-right font-mono text-slate-700">{formatINR(s.grossSales30d || (s.sellingPrice * (s.dailyVelocity || 30) * 30))}</td>
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
                                  : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                              }`}>
                                {(s.darkStoreStock ?? 15).toLocaleString('en-IN')}
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
                      <td className="py-3 px-3 text-center font-mono text-slate-700">
                        {(s.motherHubStock || 50000).toLocaleString('en-IN')}
                      </td>
                      <td className="py-3 px-3 text-right font-mono font-semibold text-slate-800">
                        {(s.revenueAtRisk && s.revenueAtRisk > 0) ? (
                          <span className="text-rose-600 font-bold">{formatINR(s.revenueAtRisk)}</span>
                        ) : (
                          <span className="text-slate-400">₹0</span>
                        )}
                      </td>
                      <td className="py-3 px-4 text-center">
                        <div className="flex items-center justify-center space-x-1.5">
                          <button
                            onClick={() => {
                              const skuStores = darkStores.filter(d => d.sku?.toLowerCase() === s.sku.toLowerCase());
                              const lowestStore = [...skuStores].sort((a, b) => (a.availableStock ?? 0) - (b.availableStock ?? 0))[0];
                              const suggested = Math.max(50, ((s.safetyThreshold || 25) * 3) - (s.darkStoreStock ?? 15));
                              setTransferModalProps({
                                sku: s.sku,
                                productName: s.name,
                                defaultHub: s.defaultMotherHub || 'Bengaluru Central Mother Hub (Nelamangala)',
                                defaultDarkStoreId: lowestStore?.storeId,
                                darkStoreName: lowestStore?.storeName,
                                suggestedUnits: suggested
                              });
                              setIsTransferModalOpen(true);
                            }}
                            className={`px-2.5 py-1 text-[11px] font-bold rounded shadow-2xs flex items-center space-x-1 transition-colors ${
                              (s.darkStoreStock ?? 15) < 10
                                ? 'bg-red-600 hover:bg-red-700 text-white'
                                : 'bg-blue-600 hover:bg-blue-700 text-white'
                            }`}
                            title="Initiate Mother Hub Stock Transfer"
                          >
                            <Truck className="w-3 h-3" />
                            <span>Transfer</span>
                          </button>
                          <button
                            onClick={() => handleStartEditSku(s)}
                            className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold rounded border border-slate-200 transition-colors"
                          >
                            Edit
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* TAB 2: Dark Stores Inventory Table */}
        {activeSheetTab === 'dark_stores' && (
          <div className="space-y-6 p-4">
            {/* Dark Store SKU Inventory Inspector */}
            <div className="bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 rounded-2xl p-4 shadow-2xs space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-0.5 bg-emerald-600 text-white font-bold text-[10px] rounded uppercase tracking-wider">Store Inspector</span>
                    <h3 className="text-sm font-bold text-slate-900">Select Dark Store & View Contained SKUs & Quantities</h3>
                  </div>
                  <p className="text-xs text-slate-600 mt-0.5">
                    Select a specific dark store node from the dropdown to instantly examine all SKUs stocked in that store and their exact inventory quantities.
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <label className="text-xs font-bold text-slate-700 uppercase whitespace-nowrap">Select Dark Store:</label>
                  <select
                    value={selectedDarkStoreInspector}
                    onChange={(e) => setSelectedDarkStoreInspector(e.target.value)}
                    className="px-3 py-1.5 bg-white border border-emerald-300 rounded-lg text-xs font-bold text-slate-900 shadow-2xs focus:ring-2 focus:ring-emerald-500"
                  >
                    {Array.from(new Set(darkStores.map(d => d.storeId))).map(storeId => {
                      const storeSample = darkStores.find(d => d.storeId === storeId);
                      return (
                        <option key={storeId} value={storeId}>
                          {storeId} — {storeSample?.storeName} ({storeSample?.platform?.toUpperCase()})
                        </option>
                      );
                    })}
                  </select>
                </div>
              </div>

              {/* Display SKUs contained in selected Dark Store */}
              {(() => {
                const storeSkus = darkStores.filter(d => d.storeId === selectedDarkStoreInspector);
                const storeMeta = storeSkus[0];
                return (
                  <div className="space-y-3 pt-2">
                    {storeMeta && (
                      <div className="flex flex-wrap items-center justify-between gap-2 bg-white px-3 py-2 rounded-xl border border-emerald-100 text-xs">
                        <div>
                          <span className="font-bold text-slate-900">{storeMeta.storeName}</span> <span className="font-mono text-slate-500">({storeMeta.storeId})</span>
                          <span className="ml-2 px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 uppercase">{storeMeta.platform}</span>
                          <span className="ml-2 text-slate-600">{storeMeta.city} (PIN: {storeMeta.pincode})</span>
                        </div>
                        <div className="flex items-center space-x-4">
                          <span className="text-slate-500">Connected Hub: <strong className="text-slate-800">{storeMeta.motherHubName}</strong></span>
                          <span className="text-slate-500">Total Store Assortment: <strong className="text-emerald-700 font-mono">{storeSkus.length} SKUs</strong></span>
                        </div>
                      </div>
                    )}

                    <div className="bg-white rounded-xl border border-emerald-200 overflow-hidden shadow-2xs">
                      <div className="overflow-x-auto max-h-60 overflow-y-auto">
                        <table className="w-full text-left text-xs">
                          <thead className="bg-slate-50 text-slate-600 font-bold uppercase text-[10px] border-b border-slate-200 sticky top-0">
                            <tr>
                              <th className="py-2.5 px-3">SKU Code</th>
                              <th className="py-2.5 px-3">Product Name</th>
                              <th className="py-2.5 px-3 text-center">Available Stock Quantity</th>
                              <th className="py-2.5 px-3 text-center">Safety Thresh</th>
                              <th className="py-2.5 px-3 text-center">Daily Velocity</th>
                              <th className="py-2.5 px-3 text-center">Stock Status</th>
                              <th className="py-2.5 px-3 text-center">Action</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100">
                            {storeSkus.map(item => (
                              <tr key={item.sku} className="hover:bg-slate-50">
                                <td className="py-2.5 px-3 font-mono font-bold text-blue-600">{item.sku}</td>
                                <td className="py-2.5 px-3 font-semibold text-slate-900">{item.productName}</td>
                                <td className="py-2.5 px-3 text-center font-mono font-bold">
                                  <span className={`px-2 py-0.5 rounded text-[10px] border ${
                                    item.availableStock < 10 ? 'bg-red-100 text-red-800 border-red-200 animate-pulse' : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                                  }`}>
                                    {item.availableStock} Units
                                  </span>
                                </td>
                                <td className="py-2.5 px-3 text-center font-mono text-slate-600">{item.safetyThreshold || 15}</td>
                                <td className="py-2.5 px-3 text-center font-mono text-slate-600">{item.dailyVelocity || 40}/d</td>
                                <td className="py-2.5 px-3 text-center font-bold">
                                  <span className={`px-2 py-0.5 rounded text-[10px] ${item.availableStock < 10 ? 'bg-red-100 text-red-800' : 'bg-emerald-100 text-emerald-800'}`}>
                                    {item.availableStock < 10 ? 'Low Stock' : item.status}
                                  </span>
                                </td>
                                <td className="py-2.5 px-3 text-center">
                                  <button
                                    onClick={() => handleOpenTransferModal(item)}
                                    className="px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-bold rounded shadow-2xs flex items-center space-x-1 mx-auto"
                                  >
                                    <Truck className="w-3 h-3" />
                                    <span>Transfer Stock</span>
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
              })()}
            </div>

            {/* SKU Selector Quick Bar */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <Filter className="w-4 h-4 text-blue-600" />
                  <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">SKU Quick Selector & Filters</span>
                </div>
                <div className="flex items-center space-x-2 text-[11px]">
                  <span className="text-slate-500 font-medium">Active SKU:</span>
                  <span className="px-2 py-0.5 bg-blue-100 text-blue-800 rounded font-bold font-mono">
                    {darkStoreSkuFilter === 'all' ? 'All Assortment SKUs' : darkStoreSkuFilter}
                  </span>
                </div>
              </div>

              {/* SKU Pills Horizontal Scroll */}
              <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
                <button
                  onClick={() => setDarkStoreSkuFilter('all')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all whitespace-nowrap flex items-center space-x-1.5 ${
                    darkStoreSkuFilter === 'all'
                      ? 'bg-blue-600 text-white shadow-2xs'
                      : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                  }`}
                >
                  <span>All SKUs</span>
                  <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-200 text-slate-700 font-mono">
                    {darkStores.length} pods
                  </span>
                </button>
                {skus.map((s) => {
                  const podCount = darkStores.filter((d) => d.sku === s.sku).length;
                  const totalUnits = darkStores.filter((d) => d.sku === s.sku).reduce((sum, d) => sum + (d.availableStock || 0), 0);
                  const isSelected = darkStoreSkuFilter.toLowerCase() === s.sku.toLowerCase();
                  return (
                    <button
                      key={s.sku}
                      onClick={() => setDarkStoreSkuFilter(s.sku)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all whitespace-nowrap flex items-center space-x-1.5 ${
                        isSelected
                          ? 'bg-blue-600 text-white shadow-2xs'
                          : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                      }`}
                    >
                      <span className="font-mono">{s.sku}</span>
                      <span className="text-[11px] opacity-90 truncate max-w-[120px]">{s.name.split(' ').slice(0, 2).join(' ')}</span>
                      <span className={`px-1.5 py-0.2 rounded-full text-[10px] font-mono ${
                        isSelected ? 'bg-blue-500 text-white' : 'bg-slate-100 text-slate-600'
                      }`}>
                        {totalUnits}u ({podCount}p)
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* Secondary Dropdown Filter Row */}
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-2.5 pt-1 border-t border-slate-200/80">
                <div className="flex items-center space-x-2">
                  <label className="text-[11px] font-bold text-slate-500 uppercase whitespace-nowrap">Dark Store:</label>
                  <input
                    type="text"
                    placeholder="Search store name/ID..."
                    value={darkStoreNameFilter}
                    onChange={(e) => setDarkStoreNameFilter(e.target.value)}
                    className="w-full px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs text-slate-800 font-medium focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <label className="text-[11px] font-bold text-slate-500 uppercase whitespace-nowrap">SKU Filter:</label>
                  <select
                    value={darkStoreSkuFilter}
                    onChange={(e) => setDarkStoreSkuFilter(e.target.value)}
                    className="w-full px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs text-slate-800 font-medium focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="all">All Assortment SKUs ({skus.length})</option>
                    {skus.map((s) => (
                      <option key={s.sku} value={s.sku}>
                        {s.sku} - {s.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="flex items-center space-x-2">
                  <label className="text-[11px] font-bold text-slate-500 uppercase whitespace-nowrap">Platform:</label>
                  <select
                    value={darkStorePlatformFilter}
                    onChange={(e) => setDarkStorePlatformFilter(e.target.value)}
                    className="w-full px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs text-slate-800 font-medium focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="all">All Quick-Commerce Platforms</option>
                    <option value="blinkit">Blinkit</option>
                    <option value="zepto">Zepto</option>
                    <option value="instamart">Instamart</option>
                    <option value="bbnow">BB Now</option>
                  </select>
                </div>

                <div className="flex items-center space-x-2">
                  <label className="text-[11px] font-bold text-slate-500 uppercase whitespace-nowrap">Stock Status:</label>
                  <select
                    value={darkStoreStatusFilter}
                    onChange={(e) => setDarkStoreStatusFilter(e.target.value)}
                    className="w-full px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs text-slate-800 font-medium focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="all">All Stock Statuses</option>
                    <option value="In Stock">In Stock (Healthy)</option>
                    <option value="Low Stock">Low Stock (Under Threshold)</option>
                    <option value="Out Of Stock">Out Of Stock (Zero Units)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Dark Store Aggregated KPI Summary Ribbon */}
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Filtered Pods</div>
                <div className="text-lg font-bold text-slate-900 font-mono mt-0.5">{darkStoreStats.totalPods}</div>
                <div className="text-[10px] text-slate-500">Dark Store Nodes</div>
              </div>
              <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl">
                <div className="text-[10px] font-bold text-emerald-700 uppercase tracking-wider">Healthy Stock</div>
                <div className="text-lg font-bold text-emerald-800 font-mono mt-0.5">{darkStoreStats.inStock}</div>
                <div className="text-[10px] text-emerald-600">Above Threshold</div>
              </div>
              <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl">
                <div className="text-[10px] font-bold text-amber-700 uppercase tracking-wider">Low Stock Pods</div>
                <div className="text-lg font-bold text-amber-800 font-mono mt-0.5">{darkStoreStats.lowStock}</div>
                <div className="text-[10px] text-amber-600">Replenish Recommended</div>
              </div>
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl">
                <div className="text-[10px] font-bold text-rose-700 uppercase tracking-wider">Stockouts</div>
                <div className="text-lg font-bold text-rose-800 font-mono mt-0.5">{darkStoreStats.outOfStock}</div>
                <div className="text-[10px] text-rose-600">Immediate Action</div>
              </div>
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl">
                <div className="text-[10px] font-bold text-blue-700 uppercase tracking-wider">Total Units in Pods</div>
                <div className="text-lg font-bold text-blue-900 font-mono mt-0.5">{darkStoreStats.totalUnits.toLocaleString()}</div>
                <div className="text-[10px] text-blue-600">Total Available Stock</div>
              </div>
            </div>

            {/* Dark Store Data Table */}
            <div className="overflow-x-auto border border-slate-200 rounded-xl">
              <table className="w-full text-left text-xs text-slate-700">
                <thead className="bg-slate-100 text-slate-600 uppercase text-[10px] font-bold border-b border-slate-200 tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Pod Store ID</th>
                    <th className="py-3 px-4">Store Name</th>
                    <th className="py-3 px-3">SKU & Product</th>
                    <th className="py-3 px-3">Platform</th>
                    <th className="py-3 px-3">City & Pincode</th>
                    <th className="py-3 px-3 text-center">Available Stock</th>
                    <th className="py-3 px-3 text-center">Safety Thresh</th>
                    <th className="py-3 px-3 text-center">Daily Velocity</th>
                    <th className="py-3 px-3 text-center">Stock Status</th>
                    <th className="py-3 px-3 text-right">Delivery SLA</th>
                    <th className="py-3 px-3">Connected Hub</th>
                    <th className="py-3 px-3 text-center">Hub Units</th>
                    <th className="py-3 px-4 text-center">Actions & Transfers</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredStores.length === 0 ? (
                    <tr>
                      <td colSpan={13} className="py-8 text-center text-slate-500">
                        No dark stores match the active filter criteria. Try selecting "All SKUs" or resetting filters.
                      </td>
                    </tr>
                  ) : (
                    filteredStores.map((d) => {
                      const rowKey = `${d.storeId}:${d.sku}`;
                      const isEditing = editingStoreKey === rowKey;
                      const isPushing = isPushingStoreRowId === d.storeId;

                      if (isEditing) {
                        return (
                          <tr key={rowKey} className="bg-blue-50/70">
                            <td className="py-2.5 px-4 font-mono font-bold text-slate-900">{d.storeId}</td>
                            <td className="py-2.5 px-4 font-semibold text-slate-900">
                              <input
                                type="text"
                                value={storeEditForm.storeName || ''}
                                onChange={(e) => setStoreEditForm({ ...storeEditForm, storeName: e.target.value })}
                                className="w-full px-2 py-1 bg-white border border-slate-300 rounded text-xs"
                              />
                            </td>
                            <td className="py-2.5 px-3">
                              <div className="font-mono font-bold text-blue-600">{d.sku}</div>
                              <div className="text-[10px] text-slate-500 truncate max-w-[130px]">{d.productName}</div>
                            </td>
                            <td className="py-2.5 px-3 uppercase font-bold text-[10px]">{d.platform}</td>
                            <td className="py-2.5 px-3 text-slate-600">{d.city}</td>
                            <td className="py-2.5 px-3 text-center">
                              <input
                                type="number"
                                value={storeEditForm.availableStock ?? 0}
                                onChange={(e) => setStoreEditForm({ ...storeEditForm, availableStock: Number(e.target.value) })}
                                className="w-16 px-2 py-1 bg-white border border-blue-400 rounded text-xs text-center font-mono font-bold text-blue-900"
                              />
                            </td>
                            <td className="py-2.5 px-3 text-center">
                              <input
                                type="number"
                                value={storeEditForm.safetyThreshold ?? 15}
                                onChange={(e) => setStoreEditForm({ ...storeEditForm, safetyThreshold: Number(e.target.value) })}
                                className="w-14 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                              />
                            </td>
                            <td className="py-2.5 px-3 text-center">
                              <input
                                type="number"
                                value={storeEditForm.dailyVelocity ?? 40}
                                onChange={(e) => setStoreEditForm({ ...storeEditForm, dailyVelocity: Number(e.target.value) })}
                                className="w-14 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                              />
                            </td>
                            <td className="py-2.5 px-3 text-center text-xs font-bold text-slate-600">Auto-calc</td>
                            <td className="py-2.5 px-3 text-right">
                              <input
                                type="number"
                                value={storeEditForm.deliverySlaMins || 10}
                                onChange={(e) => setStoreEditForm({ ...storeEditForm, deliverySlaMins: Number(e.target.value) })}
                                className="w-14 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-right font-mono"
                              />
                            </td>
                            <td className="py-2.5 px-3">
                              <input
                                type="text"
                                value={storeEditForm.motherHubName || ''}
                                onChange={(e) => setStoreEditForm({ ...storeEditForm, motherHubName: e.target.value })}
                                className="w-full px-2 py-1 bg-white border border-slate-300 rounded text-xs text-[11px]"
                              />
                            </td>
                            <td className="py-2.5 px-3 text-center font-mono text-slate-700">
                              <input
                                type="number"
                                value={storeEditForm.motherHubStock || 0}
                                onChange={(e) => setStoreEditForm({ ...storeEditForm, motherHubStock: Number(e.target.value) })}
                                className="w-20 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                              />
                            </td>
                            <td className="py-2.5 px-4 text-center">
                              <div className="flex items-center justify-center space-x-1.5">
                                <button
                                  onClick={() => handleSaveStoreEdit(d.storeId, d.sku, false)}
                                  className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold rounded shadow-2xs"
                                >
                                  Save
                                </button>
                                <button
                                  onClick={() => setEditingStoreKey(null)}
                                  className="px-2 py-1 bg-slate-200 hover:bg-slate-300 text-slate-700 text-[11px] rounded"
                                >
                                  Cancel
                                </button>
                              </div>
                            </td>
                          </tr>
                        );
                      }

                      return (
                        <tr key={rowKey} className="hover:bg-slate-50/80 transition-colors">
                          <td className="py-3 px-4 font-mono font-bold text-slate-900">{d.storeId}</td>
                          <td className="py-3 px-4 font-semibold text-slate-900">{d.storeName}</td>
                          <td className="py-3 px-3">
                            <div className="font-mono font-bold text-blue-600">{d.sku}</div>
                            <div className="text-[10px] text-slate-500 truncate max-w-[130px]">{d.productName}</div>
                          </td>
                          <td className="py-3 px-3">
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-800 uppercase">
                              {d.platform}
                            </span>
                          </td>
                          <td className="py-3 px-3 text-slate-600">{d.city} ({d.pincode})</td>
                          <td className="py-3 px-3 text-center font-mono font-bold">
                            <span className={`px-2 py-0.5 rounded text-[10px] border ${
                              d.availableStock < 10 ? 'bg-red-100 text-red-800 border-red-200 animate-pulse' :
                              d.availableStock <= (d.safetyThreshold || 15) ? 'bg-amber-100 text-amber-800 border-amber-200' :
                              'bg-emerald-100 text-emerald-800 border-emerald-200'
                            }`}>
                              {d.availableStock} Units
                            </span>
                          </td>
                          <td className="py-3 px-3 text-center font-mono text-slate-500">{d.safetyThreshold || 15}</td>
                          <td className="py-3 px-3 text-center font-mono text-slate-700">{d.dailyVelocity || 40}/d</td>
                          <td className="py-3 px-3 text-center">
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              d.availableStock < 10 ? 'bg-red-100 text-red-800' :
                              d.status === 'Low Stock' ? 'bg-amber-100 text-amber-800' :
                              'bg-emerald-100 text-emerald-800'
                            }`}>
                              {d.availableStock < 10 ? 'Low Stock' : d.status}
                            </span>
                          </td>
                          <td className="py-3 px-3 text-right font-mono font-semibold text-slate-700">{d.deliverySlaMins} Mins</td>
                          <td className="py-3 px-3 text-slate-700 text-[11px]">{d.motherHubName}</td>
                          <td className="py-3 px-3 text-center font-mono text-slate-700">{d.motherHubStock.toLocaleString('en-IN')}</td>
                          <td className="py-3 px-4 text-center">
                            <div className="flex items-center justify-center space-x-1.5">
                              <button
                                onClick={() => handleStartEditStore(d)}
                                className="px-2 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold rounded border border-slate-200 transition-colors"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => handleOpenTransferModal(d)}
                                className="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 text-[11px] font-bold rounded border border-blue-200 transition-colors flex items-center space-x-1"
                                title="Transfer stock from Mother Hub to this Dark Store"
                              >
                                <Truck className="w-3 h-3 text-blue-600" />
                                <span>Transfer</span>
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 3: Channel Pricing & MAP Matrix */}
        {activeSheetTab === 'channel_pricing' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-100 text-slate-600 uppercase text-[10px] font-bold border-b border-slate-200 tracking-wider">
                <tr>
                  <th className="py-3 px-4">Marketplace</th>
                  <th className="py-3 px-4">SKU Code</th>
                  <th className="py-3 px-4">Product Name</th>
                  <th className="py-3 px-3">BuyBox Owner</th>
                  <th className="py-3 px-3 text-right">Target MAP</th>
                  <th className="py-3 px-3 text-right">Selling Price</th>
                  <th className="py-3 px-3 text-right">Price Delta</th>
                  <th className="py-3 px-3 text-center">Status</th>
                  <th className="py-3 px-4 text-center">Actions / Sync</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredChannelPricing.map((cp) => {
                  const isEditing = editingPricingId === cp.id;
                  const isPushing = isPushingRowId === cp.id;

                  if (isEditing) {
                    return (
                      <tr key={cp.id} className="bg-blue-50/60">
                        <td className="py-3 px-4 font-bold uppercase text-blue-800">{cp.marketplace}</td>
                        <td className="py-3 px-4 font-mono font-bold text-slate-900">{cp.sku}</td>
                        <td className="py-3 px-4 font-semibold text-slate-900">{cp.productName}</td>
                        <td className="py-3 px-3">
                          <input
                            type="text"
                            value={pricingEditForm.buyBoxOwner ?? cp.buyBoxOwner}
                            onChange={(e) => setPricingEditForm({ ...pricingEditForm, buyBoxOwner: e.target.value })}
                            className="w-full px-2 py-1 bg-white border border-blue-300 rounded text-xs"
                          />
                        </td>
                        <td className="py-3 px-3 text-right">
                          <input
                            type="number"
                            value={pricingEditForm.targetMap ?? cp.targetMap}
                            onChange={(e) => setPricingEditForm({ ...pricingEditForm, targetMap: Number(e.target.value) })}
                            className="w-20 px-2 py-1 bg-white border border-blue-300 rounded text-xs text-right font-mono"
                          />
                        </td>
                        <td className="py-3 px-3 text-right">
                          <input
                            type="number"
                            value={pricingEditForm.currentSellingPrice ?? cp.currentSellingPrice}
                            onChange={(e) => setPricingEditForm({ ...pricingEditForm, currentSellingPrice: Number(e.target.value) })}
                            className="w-20 px-2 py-1 bg-white border border-blue-300 rounded text-xs text-right font-mono font-bold text-slate-900"
                          />
                        </td>
                        <td className="py-3 px-3 text-right font-mono font-semibold text-slate-600">
                          {formatINR((pricingEditForm.currentSellingPrice ?? cp.currentSellingPrice) - (pricingEditForm.targetMap ?? cp.targetMap))}
                        </td>
                        <td className="py-3 px-3 text-center">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            ((pricingEditForm.currentSellingPrice ?? cp.currentSellingPrice) < (pricingEditForm.targetMap ?? cp.targetMap))
                              ? 'bg-rose-100 text-rose-800'
                              : 'bg-emerald-100 text-emerald-800'
                          }`}>
                            {((pricingEditForm.currentSellingPrice ?? cp.currentSellingPrice) < (pricingEditForm.targetMap ?? cp.targetMap)) ? 'Breach' : 'Compliant'}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-center">
                          <div className="flex items-center justify-center space-x-1.5">
                            <button
                              onClick={() => handleSavePricingEdit(cp.id, false)}
                              className="px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-semibold rounded shadow-xs"
                            >
                              Save
                            </button>
                            <button
                              onClick={() => setEditingPricingId(null)}
                              className="px-2 py-1 bg-slate-200 hover:bg-slate-300 text-slate-700 text-[11px] rounded"
                            >
                              Cancel
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  }

                  return (
                    <tr key={cp.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3 px-4">
                        <span className="px-2.5 py-1 rounded text-[10px] font-bold uppercase bg-blue-50 text-blue-800 border border-blue-200">
                          {cp.marketplace}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-mono font-bold text-slate-900">{cp.sku}</td>
                      <td className="py-3 px-4 font-semibold text-slate-900">{cp.productName}</td>
                      <td className="py-3 px-3 text-slate-700 font-mono text-[11px]">{cp.buyBoxOwner}</td>
                      <td className="py-3 px-3 text-right font-mono text-slate-600">{formatINR(cp.targetMap)}</td>
                      <td className="py-3 px-3 text-right font-mono font-bold text-slate-900">{formatINR(cp.currentSellingPrice)}</td>
                      <td className="py-3 px-3 text-right font-mono font-semibold">
                        <span className={cp.priceDelta < 0 ? 'text-rose-600 font-bold' : 'text-slate-600'}>
                          {cp.priceDelta > 0 ? `+${formatINR(cp.priceDelta)}` : formatINR(cp.priceDelta)}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-center">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                          cp.mapBreached
                            ? 'bg-rose-100 text-rose-800 border-rose-200'
                            : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                        }`}>
                          {cp.status}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <button
                          onClick={() => handleStartEditPricing(cp)}
                          className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold rounded border border-slate-200 transition-colors"
                        >
                          Edit
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* TAB 4: Active Triggers & Alerts Log */}
        {activeSheetTab === 'alerts_log' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-100 text-slate-600 uppercase text-[10px] font-bold border-b border-slate-200 tracking-wider">
                <tr>
                  <th className="py-3 px-4">Alert ID</th>
                  <th className="py-3 px-3">SKU</th>
                  <th className="py-3 px-4">Product Name</th>
                  <th className="py-3 px-3">Marketplace</th>
                  <th className="py-3 px-3 text-center">Severity</th>
                  <th className="py-3 px-3 text-right">Revenue at Risk</th>
                  <th className="py-3 px-4">Summary & Playbook Action</th>
                  <th className="py-3 px-3 text-center">Transfer Units</th>
                  <th className="py-3 px-4">Target Owner</th>
                  <th className="py-3 px-4 text-center">Actions / Sync</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredAlerts.map((a) => {
                  return (
                    <tr key={a.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3 px-4 font-mono font-bold text-slate-900">{a.id}</td>
                      <td className="py-3 px-3 font-mono font-bold text-blue-600">{a.sku}</td>
                      <td className="py-3 px-4 font-semibold text-slate-900">{a.productName}</td>
                      <td className="py-3 px-3 uppercase font-bold text-[10px] text-slate-700">{a.marketplace}</td>
                      <td className="py-3 px-3 text-center">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          a.severity === 'Critical' ? 'bg-rose-100 text-rose-800 border border-rose-200' :
                          a.severity === 'High' ? 'bg-amber-100 text-amber-800 border border-amber-200' :
                          'bg-blue-100 text-blue-800 border border-blue-200'
                        }`}>
                          {a.severity}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right font-mono font-bold text-rose-600">
                        {formatINR(a.revenueAtRiskInr || 0)}
                      </td>
                      <td className="py-3 px-4 space-y-0.5">
                        <p className="font-semibold text-slate-900">{a.summary}</p>
                        <p className="text-[10px] text-blue-700 font-medium">👉 {a.recommendedPlaybook}</p>
                      </td>
                      <td className="py-3 px-3 text-center font-mono font-bold text-slate-800">
                        {a.transferUnitsSuggested ? `${a.transferUnitsSuggested} Units` : '-'}
                      </td>
                      <td className="py-3 px-4 font-mono text-[11px] text-slate-600">
                        {a.targetOwnerEmail || 'vikashr984@gmail.com'}
                      </td>
                      <td className="py-3 px-4 text-center">
                        <div className="flex items-center justify-center space-x-1.5">
                          <button
                            onClick={() => {
                              setSelectedEmailAlert(a);
                              setIsEmailModalOpen(true);
                            }}
                            className="px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-bold rounded shadow-2xs flex items-center space-x-1"
                            title="Open Interactive HTML Email Viewer & Live CTAs"
                          >
                            <span>📧 Email & CTA</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* TAB 5: Mother Hubs Inventory Table */}
        {activeSheetTab === 'mother_hubs' && (
          <div className="space-y-6 p-4">
            {/* Mother Hub Selector & Connected Dark Stores Network Inspector */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-2xl p-4 shadow-2xs space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-0.5 bg-blue-600 text-white font-bold text-[10px] rounded uppercase tracking-wider">Network Drilldown</span>
                    <h3 className="text-sm font-bold text-slate-900">Mother Hub to Dark Store Network & SKU Allocation Inspector</h3>
                  </div>
                  <p className="text-xs text-slate-600 mt-0.5">
                    Select a regional Mother Hub to inspect all connected micro-fulfillment pods and the exact SKU stock quantities available in each dark store.
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <label className="text-xs font-bold text-slate-700 uppercase whitespace-nowrap">Select Mother Hub:</label>
                  <select
                    value={selectedMotherHubInspector}
                    onChange={(e) => setSelectedMotherHubInspector(e.target.value)}
                    className="px-3 py-1.5 bg-white border border-blue-300 rounded-lg text-xs font-bold text-slate-900 shadow-2xs focus:ring-2 focus:ring-blue-500"
                  >
                    {Array.from(new Set((motherHubSkuStock || []).map(h => h.hubName))).map(hubName => (
                      <option key={hubName} value={hubName}>
                        {hubName}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Connected Pods Summary */}
              {(() => {
                const connectedPods = (darkStores || []).filter(
                  d => (d.motherHubName || '').toLowerCase().includes(selectedMotherHubInspector.toLowerCase()) ||
                       selectedMotherHubInspector.toLowerCase().includes((d.motherHubName || '').toLowerCase().split(' ')[0])
                );
                return (
                  <div className="space-y-3">
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div className="bg-white p-3 rounded-xl border border-blue-100 shadow-2xs">
                        <div className="text-[10px] font-bold text-slate-500 uppercase">Connected Dark Stores</div>
                        <div className="text-lg font-bold text-blue-900 font-mono mt-0.5">{connectedPods.length} Pods</div>
                        <div className="text-[10px] text-slate-500">Active fulfillment nodes in region</div>
                      </div>
                      <div className="bg-white p-3 rounded-xl border border-blue-100 shadow-2xs">
                        <div className="text-[10px] font-bold text-slate-500 uppercase">Total Pod Stock Units</div>
                        <div className="text-lg font-bold text-emerald-700 font-mono mt-0.5">
                          {connectedPods.reduce((sum, p) => sum + (p.availableStock || 0), 0).toLocaleString()} Units
                        </div>
                        <div className="text-[10px] text-slate-500">Across all connected dark stores</div>
                      </div>
                      <div className="bg-white p-3 rounded-xl border border-blue-100 shadow-2xs">
                        <div className="text-[10px] font-bold text-slate-500 uppercase">Low Stock Pods (&lt;10 Units)</div>
                        <div className="text-lg font-bold text-rose-600 font-mono mt-0.5">
                          {connectedPods.filter(p => (p.availableStock || 0) < 10).length} Pods
                        </div>
                        <div className="text-[10px] text-slate-500">Require immediate replenishment</div>
                      </div>
                    </div>

                    {/* Breakdown Table of Each Connected Dark Store and its SKU Quantities */}
                    <div className="bg-white rounded-xl border border-blue-200 overflow-hidden shadow-2xs">
                      <div className="bg-slate-100 px-4 py-2.5 border-b border-slate-200 flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                          Connected Dark Stores & SKU Allocation Breakdown ({selectedMotherHubInspector})
                        </span>
                        <span className="text-xs text-slate-500 font-mono">{connectedPods.length} records found</span>
                      </div>
                      <div className="overflow-x-auto max-h-80 overflow-y-auto">
                        <table className="w-full text-left text-xs">
                          <thead className="bg-slate-50 text-slate-600 font-bold uppercase text-[10px] border-b border-slate-200 sticky top-0">
                            <tr>
                              <th className="py-2.5 px-3">Dark Store ID & Name</th>
                              <th className="py-2.5 px-3">Platform</th>
                              <th className="py-2.5 px-3">City & Pincode</th>
                              <th className="py-2.5 px-3">SKU & Product Name</th>
                              <th className="py-2.5 px-3 text-center">Available Stock</th>
                              <th className="py-2.5 px-3 text-center">Status</th>
                              <th className="py-2.5 px-3 text-center">Action</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100">
                            {connectedPods.length === 0 ? (
                              <tr>
                                <td colSpan={7} className="py-6 text-center text-slate-500">
                                  No connected dark store pods found for this Mother Hub.
                                </td>
                              </tr>
                            ) : (
                              connectedPods.map((pod) => (
                                <tr key={`${pod.storeId}-${pod.sku}`} className="hover:bg-slate-50">
                                  <td className="py-2.5 px-3 font-mono font-bold text-slate-900">
                                    {pod.storeId}
                                    <div className="text-[11px] font-semibold text-slate-700">{pod.storeName}</div>
                                  </td>
                                  <td className="py-2.5 px-3 uppercase text-[10px] font-bold text-slate-700">
                                    {pod.platform}
                                  </td>
                                  <td className="py-2.5 px-3 text-slate-600">
                                    {pod.city} ({pod.pincode})
                                  </td>
                                  <td className="py-2.5 px-3">
                                    <div className="font-mono font-bold text-blue-600">{pod.sku}</div>
                                    <div className="text-[10px] text-slate-500 truncate max-w-[160px]">{pod.productName}</div>
                                  </td>
                                  <td className="py-2.5 px-3 text-center font-mono font-bold">
                                    <span className={`px-2 py-0.5 rounded text-[10px] border ${
                                      (pod.availableStock ?? 15) < 10
                                        ? 'bg-red-100 text-red-800 border-red-200 animate-pulse'
                                        : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                                    }`}>
                                      {pod.availableStock ?? 15} Units
                                    </span>
                                  </td>
                                  <td className="py-2.5 px-3 text-center">
                                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                      (pod.availableStock ?? 15) < 10 ? 'text-red-700 bg-red-50' : 'text-emerald-700 bg-emerald-50'
                                    }`}>
                                      {(pod.availableStock ?? 15) < 10 ? 'Low Stock' : 'Healthy'}
                                    </span>
                                  </td>
                                  <td className="py-2.5 px-3 text-center">
                                    <button
                                      onClick={() => handleOpenTransferModal(pod)}
                                      className="px-2 py-1 bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-bold rounded shadow-2xs flex items-center space-x-1 mx-auto"
                                      title="Transfer units from Mother Hub to this Dark Store"
                                    >
                                      <Truck className="w-3 h-3" />
                                      <span>Transfer</span>
                                    </button>
                                  </td>
                                </tr>
                              ))
                            )}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                );
              })()}
            </div>

            {/* SKU Filter for Mother Hubs */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center space-x-2">
                <Building2 className="w-4 h-4 text-blue-600" />
                <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">Mother Hub Regional Buffers</span>
              </div>
              <div className="flex items-center space-x-2">
                <label className="text-[11px] font-bold text-slate-500 uppercase whitespace-nowrap">Filter by SKU:</label>
                <select
                  value={motherHubSkuFilter}
                  onChange={(e) => setMotherHubSkuFilter(e.target.value)}
                  className="px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs text-slate-800 font-medium focus:ring-1 focus:ring-blue-500"
                >
                  <option value="all">All SKUs in Regional Hubs</option>
                  {skus.map((s) => (
                    <option key={s.sku} value={s.sku}>
                      {s.sku} - {s.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="overflow-x-auto border border-slate-200 rounded-xl">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase tracking-wider text-[10px]">
                    <th className="py-3 px-4">Hub ID & Name</th>
                    <th className="py-3 px-3">City & PIN</th>
                    <th className="py-3 px-4">SKU & Product Name</th>
                    <th className="py-3 px-3 text-center">Available Units</th>
                    <th className="py-3 px-3 text-center">Reserved Units</th>
                    <th className="py-3 px-3 text-center">Safety Threshold</th>
                    <th className="py-3 px-3 text-center">Connected Pods</th>
                    <th className="py-3 px-3 text-center">Dispatch SLA</th>
                    <th className="py-3 px-3 text-center">Buffer Status</th>
                    <th className="py-3 px-4 text-center">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredMotherHubs.map((h) => {
                    const isEditing = editingHubStockId === h.id;

                    if (isEditing) {
                      return (
                        <tr key={`${h.hubId}-${h.sku}`} className="bg-blue-50/70">
                          <td className="py-3 px-4">
                            <div className="font-bold text-slate-900">{h.hubName}</div>
                            <div className="font-mono text-[10px] text-slate-500">{h.hubId}</div>
                          </td>
                          <td className="py-3 px-3 text-slate-600">{h.city}</td>
                          <td className="py-3 px-4">
                            <div className="font-bold text-slate-900">{h.productName}</div>
                            <div className="font-mono text-[10px] text-blue-600 font-bold">{h.sku}</div>
                          </td>
                          <td className="py-3 px-3 text-center">
                            <input
                              type="number"
                              value={hubStockEditForm.quantityAvailable ?? 0}
                              onChange={(e) => setHubStockEditForm({ ...hubStockEditForm, quantityAvailable: Number(e.target.value) })}
                              className="w-20 px-2 py-1 bg-white border border-blue-400 rounded text-xs text-center font-mono font-bold"
                            />
                          </td>
                          <td className="py-3 px-3 text-center">
                            <input
                              type="number"
                              value={hubStockEditForm.reservedQuantity ?? 0}
                              onChange={(e) => setHubStockEditForm({ ...hubStockEditForm, reservedQuantity: Number(e.target.value) })}
                              className="w-16 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                            />
                          </td>
                          <td className="py-3 px-3 text-center">
                            <input
                              type="number"
                              value={hubStockEditForm.safetyStockThreshold ?? 0}
                              onChange={(e) => setHubStockEditForm({ ...hubStockEditForm, safetyStockThreshold: Number(e.target.value) })}
                              className="w-16 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                            />
                          </td>
                          <td className="py-3 px-3 text-center font-mono text-slate-700">{h.connectedDarkStoresCount} Dark Stores</td>
                          <td className="py-3 px-3 text-center">
                            <input
                              type="number"
                              value={hubStockEditForm.dispatchSlaHours ?? 4}
                              onChange={(e) => setHubStockEditForm({ ...hubStockEditForm, dispatchSlaHours: Number(e.target.value) })}
                              className="w-14 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                            />
                          </td>
                          <td className="py-3 px-3 text-center text-[10px] font-bold text-slate-600">Auto-calc</td>
                          <td className="py-3 px-4 text-center">
                            <div className="flex items-center justify-center space-x-1.5">
                              <button
                                onClick={() => handleSaveHubStockEdit(h.id)}
                                className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold rounded shadow-2xs"
                              >
                                Save
                              </button>
                              <button
                                onClick={() => setEditingHubStockId(null)}
                                className="px-2 py-1 bg-slate-200 hover:bg-slate-300 text-slate-700 text-[11px] rounded"
                              >
                                Cancel
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    }

                    return (
                      <tr key={`${h.hubId}-${h.sku}`} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3 px-4">
                          <div className="font-bold text-slate-900">{h.hubName}</div>
                          <div className="font-mono text-[10px] text-slate-500 font-semibold">{h.hubId}</div>
                        </td>
                        <td className="py-3 px-3 text-slate-600">
                          <div>{h.city}</div>
                          <div className="text-[10px] text-slate-400 font-mono">PIN: {h.pincode}</div>
                        </td>
                        <td className="py-3 px-4">
                          <div className="font-bold text-slate-900">{h.productName}</div>
                          <div className="font-mono text-[10px] text-blue-600 font-semibold">{h.sku}</div>
                        </td>
                        <td className="py-3 px-3 text-center">
                          <span className={`px-2.5 py-1 rounded-full text-xs font-mono font-bold ${
                            h.quantityAvailable < h.safetyStockThreshold
                              ? 'bg-rose-100 text-rose-800'
                              : 'bg-emerald-100 text-emerald-800'
                          }`}>
                            {h.quantityAvailable.toLocaleString()} Units
                          </span>
                        </td>
                        <td className="py-3 px-3 text-center font-mono text-slate-600">
                          {h.reservedQuantity.toLocaleString()}
                        </td>
                        <td className="py-3 px-3 text-center font-mono text-slate-500">
                          {h.safetyStockThreshold.toLocaleString()}
                        </td>
                        <td className="py-3 px-3 text-center font-mono font-semibold text-slate-700">
                          {h.connectedDarkStoresCount} Dark Stores
                        </td>
                        <td className="py-3 px-3 text-center font-mono font-bold text-indigo-700">
                          {h.dispatchSlaHours}h SLA
                        </td>
                        <td className="py-3 px-3 text-center">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            h.bufferHealth === 'Critical'
                              ? 'bg-rose-100 text-rose-800 border border-rose-200'
                              : h.bufferHealth === 'Adequate'
                              ? 'bg-amber-100 text-amber-800 border border-amber-200'
                              : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                          }`}>
                            {h.bufferHealth}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-center">
                          <button
                            onClick={() => handleStartEditHubStock(h)}
                            className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold rounded border border-slate-200 transition-colors"
                          >
                            Edit
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 6: Manufacturers Supply Table */}
        {activeSheetTab === 'manufacturers_supply' && (
          <div className="space-y-4 p-4">
            {/* SKU Filter for Manufacturers */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center space-x-2">
                <Factory className="w-4 h-4 text-blue-600" />
                <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">Manufacturer Plants & Factory Lines</span>
              </div>
              <div className="flex items-center space-x-2">
                <label className="text-[11px] font-bold text-slate-500 uppercase whitespace-nowrap">Filter by SKU:</label>
                <select
                  value={mfgSkuFilter}
                  onChange={(e) => setMfgSkuFilter(e.target.value)}
                  className="px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs text-slate-800 font-medium focus:ring-1 focus:ring-blue-500"
                >
                  <option value="all">All SKUs in Production</option>
                  {skus.map((s) => (
                    <option key={s.sku} value={s.sku}>
                      {s.sku} - {s.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="overflow-x-auto border border-slate-200 rounded-xl">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase tracking-wider text-[10px]">
                    <th className="py-3 px-4">Manufacturer & Plant</th>
                    <th className="py-3 px-3">Location</th>
                    <th className="py-3 px-4">SKU & Product Name</th>
                    <th className="py-3 px-3 text-center">Finished Goods Stock</th>
                    <th className="py-3 px-3 text-center">Work in Progress (WIP)</th>
                    <th className="py-3 px-3 text-center">Daily Output</th>
                    <th className="py-3 px-3 text-center">Transit to Hub</th>
                    <th className="py-3 px-3">Active Batch</th>
                    <th className="py-3 px-3 text-center">Destination Hub</th>
                    <th className="py-3 px-3 text-center">Quality Rate</th>
                    <th className="py-3 px-4 text-center">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredManufacturerSupply.map((m) => {
                    const isEditing = editingMfgId === m.id;

                    if (isEditing) {
                      return (
                        <tr key={`${m.id}-${m.sku}`} className="bg-blue-50/70">
                          <td className="py-3 px-4">
                            <div className="font-bold text-slate-900">{m.manufacturerName}</div>
                            <div className="text-[11px] text-slate-500">{m.plantName}</div>
                          </td>
                          <td className="py-3 px-3 text-slate-600">{m.location}</td>
                          <td className="py-3 px-4">
                            <div className="font-bold text-slate-900">{m.productName}</div>
                            <div className="font-mono text-[10px] text-blue-600 font-bold">{m.sku}</div>
                          </td>
                          <td className="py-3 px-3 text-center">
                            <input
                              type="number"
                              value={mfgEditForm.factoryFinishedGoodsStock ?? 0}
                              onChange={(e) => setMfgEditForm({ ...mfgEditForm, factoryFinishedGoodsStock: Number(e.target.value) })}
                              className="w-20 px-2 py-1 bg-white border border-blue-400 rounded text-xs text-center font-mono font-bold"
                            />
                          </td>
                          <td className="py-3 px-3 text-center">
                            <input
                              type="number"
                              value={mfgEditForm.workInProgressUnits ?? 0}
                              onChange={(e) => setMfgEditForm({ ...mfgEditForm, workInProgressUnits: Number(e.target.value) })}
                              className="w-20 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                            />
                          </td>
                          <td className="py-3 px-3 text-center">
                            <input
                              type="number"
                              value={mfgEditForm.dailyProductionRate ?? 0}
                              onChange={(e) => setMfgEditForm({ ...mfgEditForm, dailyProductionRate: Number(e.target.value) })}
                              className="w-16 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                            />
                          </td>
                          <td className="py-3 px-3 text-center">
                            <input
                              type="number"
                              value={mfgEditForm.leadTimeToMotherHubHours ?? 24}
                              onChange={(e) => setMfgEditForm({ ...mfgEditForm, leadTimeToMotherHubHours: Number(e.target.value) })}
                              className="w-14 px-2 py-1 bg-white border border-slate-300 rounded text-xs text-center font-mono"
                            />
                          </td>
                          <td className="py-3 px-3 font-mono text-[11px] text-slate-800">{m.activeBatchNumber}</td>
                          <td className="py-3 px-3 text-center text-slate-700 text-[11px]">{m.destinationMotherHub}</td>
                          <td className="py-3 px-3 text-center font-mono text-emerald-700 font-bold">{m.qualityPassRate}%</td>
                          <td className="py-3 px-4 text-center">
                            <div className="flex items-center justify-center space-x-1.5">
                              <button
                                onClick={() => handleSaveMfgEdit(m.id)}
                                className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold rounded shadow-2xs"
                              >
                                Save
                              </button>
                              <button
                                onClick={() => setEditingMfgId(null)}
                                className="px-2 py-1 bg-slate-200 hover:bg-slate-300 text-slate-700 text-[11px] rounded"
                              >
                                Cancel
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    }

                    return (
                      <tr key={`${m.id}-${m.sku}`} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3 px-4">
                          <div className="font-bold text-slate-900">{m.manufacturerName}</div>
                          <div className="text-[11px] text-slate-500 font-medium">{m.plantName}</div>
                        </td>
                        <td className="py-3 px-3 text-slate-600">
                          <div>{m.location}</div>
                          <div className="text-[10px] text-slate-400 font-mono">PIN: {m.pincode}</div>
                        </td>
                        <td className="py-3 px-4">
                          <div className="font-bold text-slate-900">{m.productName}</div>
                          <div className="font-mono text-[10px] text-blue-600 font-semibold">{m.sku}</div>
                        </td>
                        <td className="py-3 px-3 text-center">
                          <span className="px-2.5 py-1 rounded-full text-xs font-mono font-bold bg-blue-50 text-blue-800 border border-blue-200">
                            {m.factoryFinishedGoodsStock.toLocaleString()} Units
                          </span>
                        </td>
                        <td className="py-3 px-3 text-center font-mono font-medium text-amber-700">
                          +{m.workInProgressUnits.toLocaleString()}
                        </td>
                        <td className="py-3 px-3 text-center font-mono text-slate-700">
                          {m.dailyProductionRate.toLocaleString()}/day
                        </td>
                        <td className="py-3 px-3 text-center font-mono font-semibold text-slate-800">
                          {m.leadTimeToMotherHubHours} Hours
                        </td>
                        <td className="py-3 px-3">
                          <div className="font-mono font-semibold text-slate-800 text-[11px]">{m.activeBatchNumber}</div>
                          <div className="text-[10px] text-slate-400">Mfg: {m.mfgDate}</div>
                        </td>
                        <td className="py-3 px-3 text-center text-slate-700 text-[11px] font-medium">
                          {m.destinationMotherHub}
                        </td>
                        <td className="py-3 px-3 text-center">
                          <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded text-[10px] font-bold">
                            {m.qualityPassRate}% Pass
                          </span>
                        </td>
                        <td className="py-3 px-4 text-center">
                          <button
                            onClick={() => handleStartEditMfg(m)}
                            className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold rounded border border-slate-200 transition-colors"
                          >
                            Edit
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 7: Transfer Audit Logs Table */}
        {activeSheetTab === 'transfer_logs' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase tracking-wider text-[10px]">
                  <th className="py-3 px-4">Log ID</th>
                  <th className="py-3 px-3">Timestamp</th>
                  <th className="py-3 px-4">SKU & Product</th>
                  <th className="py-3 px-3">Source Mother Hub</th>
                  <th className="py-3 px-3">Target Dark Store</th>
                  <th className="py-3 px-3 text-right">Units</th>
                  <th className="py-3 px-3">Carrier Partner</th>
                  <th className="py-3 px-3 font-mono">Tracking No</th>
                  <th className="py-3 px-3 text-center">Status</th>
                  <th className="py-3 px-4 text-center">Executed By</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredTransferLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4 font-mono font-bold text-slate-900">{log.id}</td>
                    <td className="py-3 px-3 font-mono text-slate-600 text-[11px]">{log.timestamp}</td>
                    <td className="py-3 px-4">
                      <div className="font-bold text-slate-900">{log.productName}</div>
                      <div className="font-mono text-[10px] text-blue-600 font-semibold">{log.sku}</div>
                    </td>
                    <td className="py-3 px-3 text-slate-700">{log.sourceMotherHub}</td>
                    <td className="py-3 px-3 text-slate-700 font-medium">{log.targetDarkStore}</td>
                    <td className="py-3 px-3 text-right font-mono font-bold text-emerald-700">+{log.unitsTransferred} Units</td>
                    <td className="py-3 px-3 text-slate-600 text-[11px]">{log.carrier}</td>
                    <td className="py-3 px-3 font-mono font-bold text-[11px] text-indigo-600">{log.trackingNumber}</td>
                    <td className="py-3 px-3 text-center">
                      <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 border border-emerald-200 rounded text-[10px] font-bold">
                        {log.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center text-slate-600 text-[11px] font-medium">{log.executedBy}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Interactive Stock Transfer Modal */}
      <StockTransferModal
        isOpen={isTransferModalOpen}
        onClose={() => setIsTransferModalOpen(false)}
        sku={transferModalProps.sku}
        productName={transferModalProps.productName}
        darkStoreName={transferModalProps.darkStoreName}
        defaultDarkStoreId={transferModalProps.defaultDarkStoreId}
        defaultHub={transferModalProps.defaultHub}
        suggestedUnits={transferModalProps.suggestedUnits}
      />

      {/* Interactive HTML Email Viewer & CTA Modal */}
      <EmailDispatchModal
        isOpen={isEmailModalOpen}
        onClose={() => {
          setIsEmailModalOpen(false);
          setSelectedEmailAlert(null);
        }}
        anomaly={selectedEmailAlert}
      />
    </div>
  );
};

