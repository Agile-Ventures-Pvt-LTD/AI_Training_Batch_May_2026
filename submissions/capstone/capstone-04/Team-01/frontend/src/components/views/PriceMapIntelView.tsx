import React, { useState } from 'react';
import {
  DollarSign,
  AlertTriangle,
  ShieldAlert,
  FileCheck,
  ExternalLink,
  CheckCircle,
  Building2,
  Mail,
  Zap,
  CheckCircle2,
  Edit3,
  Save,
  X,
  UploadCloud,
  Check,
  Search,
  Filter,
  Layers,
  ArrowUpDown
} from 'lucide-react';
import { MAPBreach, MarketplaceId, ChannelPricingItem } from '../../types';
import { formatINR, formatPercent, OWNER_EMAIL } from '../../data/mockData';
import { useData } from '../../context/DataContext';
import confetti from 'canvas-confetti';

interface PriceMapIntelViewProps {
  selectedChannel: MarketplaceId | 'all';
  onOpenEmailModal: (breaches: MAPBreach[]) => void;
}

export const PriceMapIntelView: React.FC<PriceMapIntelViewProps> = ({
  selectedChannel,
  onOpenEmailModal
}) => {
  const {
    mapBreaches,
    channelPricing,
    skus,
    updateChannelPricing,
    pushChannelPricingToGoogleSheet,
    googleSheetWebhookUrl
  } = useData();

  const [activeTab, setActiveTab] = useState<'breaches' | 'all_channel_pricing'>('breaches');
  const [editingItem, setEditingItem] = useState<{
    id: string;
    sku: string;
    productName: string;
    marketplace: MarketplaceId;
    currentSellingPrice: number;
    targetMap: number;
    buyBoxOwner: string;
    inStock: boolean;
  } | null>(null);

  const [searchQuery, setSearchQuery] = useState('');
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [isPushing, setIsPushing] = useState<string | null>(null);

  // Dynamically compute breaches from current SKUs / channelPricing where sellingPrice < targetMap
  const computedBreaches: MAPBreach[] = React.useMemo(() => {
    if (mapBreaches && mapBreaches.length > 0) return mapBreaches;

    const list: MAPBreach[] = [];
    skus.forEach((s) => {
      if (s.targetMap && s.sellingPrice < s.targetMap) {
        const discountAmt = s.targetMap - s.sellingPrice;
        const discountPct = Number(((discountAmt / s.targetMap) * 100).toFixed(1));
        list.push({
          id: `br-${s.sku}-flipkart`,
          sku: s.sku,
          productName: s.name,
          channel: 'flipkart',
          enforcedMap: s.targetMap,
          violatedPrice: s.sellingPrice,
          discountPercent: discountPct,
          violatingSeller: 'DiscountDeals_Unauth',
          breachDurationHours: 4.2,
          status: 'Active Breach',
          evidenceUrl: `https://flipkart.com/dp/${s.sku}`,
          complianceAction: 'Auto Cease-and-Desist Drafted & BuyBox Penalty Triggered'
        });
      }
    });
    return list;
  }, [mapBreaches, skus]);

  const [breaches, setBreaches] = React.useState<MAPBreach[]>(computedBreaches);

  React.useEffect(() => {
    setBreaches(computedBreaches);
  }, [computedBreaches]);

  const handleActionLegalNotice = (breachId: string) => {
    setBreaches((prev) =>
      prev.map((b) =>
        b.id === breachId ? { ...b, status: 'Actioned', complianceAction: 'Legal Cease & Desist Sent to Marketplace Registry' } : b
      )
    );
    confetti({
      particleCount: 60,
      spread: 45,
      origin: { y: 0.6 }
    });
    setFeedback({
      type: 'success',
      message: `Legal Notice issued for ${breachId}. Marketplace compliance notified!`
    });
  };

  const handleStartEdit = (item: {
    id: string;
    sku: string;
    productName: string;
    marketplace: MarketplaceId;
    currentSellingPrice: number;
    targetMap: number;
    buyBoxOwner: string;
    inStock?: boolean;
  }) => {
    setEditingItem({
      id: item.id,
      sku: item.sku,
      productName: item.productName,
      marketplace: item.marketplace,
      currentSellingPrice: item.currentSellingPrice,
      targetMap: item.targetMap,
      buyBoxOwner: item.buyBoxOwner,
      inStock: item.inStock ?? true
    });
  };

  const handleSaveEdit = async (pushToSheet = false) => {
    if (!editingItem) return;

    const mapBreached = editingItem.targetMap > 0 && editingItem.currentSellingPrice < editingItem.targetMap;
    const priceDelta = editingItem.currentSellingPrice - editingItem.targetMap;

    updateChannelPricing(editingItem.id, {
      sku: editingItem.sku,
      productName: editingItem.productName,
      marketplace: editingItem.marketplace,
      currentSellingPrice: editingItem.currentSellingPrice,
      targetMap: editingItem.targetMap,
      mapBreached,
      priceDelta,
      buyBoxOwner: editingItem.buyBoxOwner,
      inStock: editingItem.inStock,
      status: mapBreached ? 'Active Breach' : 'Compliant'
    });

    if (pushToSheet) {
      setIsPushing(editingItem.id);
      const res = await pushChannelPricingToGoogleSheet({
        id: editingItem.id,
        sku: editingItem.sku,
        productName: editingItem.productName,
        marketplace: editingItem.marketplace,
        currentSellingPrice: editingItem.currentSellingPrice,
        targetMap: editingItem.targetMap,
        mapBreached,
        priceDelta,
        buyBoxOwner: editingItem.buyBoxOwner,
        inStock: editingItem.inStock,
        shareOfSearch: 30,
        revenue30d: editingItem.currentSellingPrice * 50 * 30,
        status: mapBreached ? 'Active Breach' : 'Compliant',
        complianceAction: mapBreached ? 'Auto Cease-and-Desist Notice Drafted' : 'Active - Price Protected'
      });
      setIsPushing(null);
      if (res.success) {
        setFeedback({ type: 'success', message: res.message });
      } else {
        setFeedback({ type: 'error', message: res.message });
      }
    } else {
      setFeedback({
        type: 'success',
        message: `Updated pricing for ${editingItem.sku} (${String(editingItem.marketplace).toUpperCase()}) locally!`
      });
    }

    setEditingItem(null);
  };

  const filteredBreaches = breaches.filter((b) => {
    if (selectedChannel !== 'all' && b.channel !== selectedChannel) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return b.sku.toLowerCase().includes(q) || b.productName.toLowerCase().includes(q) || b.violatingSeller.toLowerCase().includes(q);
    }
    return true;
  });

  const filteredChannelPricing = (channelPricing || []).filter((item) => {
    if (selectedChannel !== 'all' && item.marketplace !== selectedChannel) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return item.sku.toLowerCase().includes(q) || item.productName.toLowerCase().includes(q) || item.buyBoxOwner.toLowerCase().includes(q);
    }
    return true;
  });

  return (
    <div id="price-map-intel-view" className="space-y-6">
      {/* Feedback Banner */}
      {feedback && (
        <div className={`p-4 rounded-xl text-xs font-semibold flex items-center justify-between border ${
          feedback.type === 'success'
            ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
            : 'bg-rose-50 text-rose-800 border-rose-200'
        }`}>
          <div className="flex items-center space-x-2">
            {feedback.type === 'success' ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <AlertTriangle className="w-4 h-4 text-rose-600" />}
            <span>{feedback.message}</span>
          </div>
          <button onClick={() => setFeedback(null)} className="text-slate-400 hover:text-slate-600">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Header */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Channel Pricing & MAP Intelligence</h2>
            <span className="px-2 py-0.5 bg-rose-50 text-rose-700 border border-rose-200 text-[10px] font-bold rounded">
              {filteredBreaches.length} Active Breaches
            </span>
            <span className="px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 text-[10px] font-bold rounded">
              {channelPricing?.length || 0} Channel Matrix Records
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time monitoring of marketplace channel pricing, MAP compliance, and direct two-way Google Sheet edit sync
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <div className="flex bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => setActiveTab('breaches')}
              className={`px-3 py-1.5 rounded-md transition-all ${
                activeTab === 'breaches' ? 'bg-white text-slate-900 shadow-xs font-bold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Active Breaches ({filteredBreaches.length})
            </button>
            <button
              onClick={() => setActiveTab('all_channel_pricing')}
              className={`px-3 py-1.5 rounded-md transition-all ${
                activeTab === 'all_channel_pricing' ? 'bg-white text-slate-900 shadow-xs font-bold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All Channel Pricing ({filteredChannelPricing.length})
            </button>
          </div>

          <button
            onClick={() => onOpenEmailModal(filteredBreaches)}
            className="px-3.5 py-2 bg-slate-50 hover:bg-slate-100 border border-slate-300 text-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
          >
            <Mail className="w-3.5 h-3.5 text-emerald-600" />
            <span>Email MAP Audit</span>
          </button>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex items-center justify-between gap-3 bg-white p-3 border border-slate-200 rounded-xl">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by SKU, Product Name, or Reseller..."
            className="w-full pl-9 pr-4 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
          />
        </div>
        <div className="text-xs text-slate-500 font-medium">
          Showing <strong className="text-slate-800">{activeTab === 'breaches' ? filteredBreaches.length : filteredChannelPricing.length}</strong> items
        </div>
      </div>

      {/* MODAL: Edit Price & MAP Dialog */}
      {editingItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-lg w-full p-6 space-y-5 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Edit Channel Price & MAP Threshold</h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  {editingItem.sku} • {editingItem.productName} ({String(editingItem.marketplace).toUpperCase()})
                </p>
              </div>
              <button onClick={() => setEditingItem(null)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <label className="block text-slate-700 font-bold mb-1">Target Enforced MAP (₹)</label>
                <input
                  type="number"
                  value={editingItem.targetMap}
                  onChange={(e) => setEditingItem({ ...editingItem, targetMap: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg font-mono text-slate-900 font-bold focus:bg-white"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-bold mb-1">Current Selling Price (₹)</label>
                <input
                  type="number"
                  value={editingItem.currentSellingPrice}
                  onChange={(e) => setEditingItem({ ...editingItem, currentSellingPrice: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg font-mono text-slate-900 font-bold focus:bg-white"
                />
              </div>

              <div className="col-span-2">
                <label className="block text-slate-700 font-bold mb-1">BuyBox Winning Seller / Reseller</label>
                <input
                  type="text"
                  value={editingItem.buyBoxOwner}
                  onChange={(e) => setEditingItem({ ...editingItem, buyBoxOwner: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg font-mono text-slate-800 focus:bg-white"
                />
              </div>

              <div className="col-span-2 flex items-center justify-between p-3 bg-slate-50 border border-slate-200 rounded-lg">
                <span className="text-slate-700 font-semibold">Inventory Availability</span>
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={editingItem.inStock}
                    onChange={(e) => setEditingItem({ ...editingItem, inStock: e.target.checked })}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span className="font-semibold text-slate-800">{editingItem.inStock ? 'In Stock' : 'Out of Stock'}</span>
                </label>
              </div>

              <div className="col-span-2 p-3 bg-blue-50 border border-blue-100 rounded-lg text-[11px] text-blue-900">
                {editingItem.targetMap > 0 && editingItem.currentSellingPrice < editingItem.targetMap ? (
                  <span className="text-rose-700 font-bold">
                    ⚠️ Selling Price (₹{editingItem.currentSellingPrice}) is ₹{editingItem.targetMap - editingItem.currentSellingPrice} below MAP (₹{editingItem.targetMap}). Will trigger MAP Breach status.
                  </span>
                ) : (
                  <span className="text-emerald-700 font-bold">
                    ✓ Price is compliant with MAP target.
                  </span>
                )}
              </div>
            </div>

            <div className="flex items-center justify-end space-x-2.5 pt-2 border-t border-slate-100">
              <button
                onClick={() => setEditingItem(null)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={() => handleSaveEdit(false)}
                className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-lg shadow-xs"
              >
                Save Locally
              </button>
              <button
                onClick={() => handleSaveEdit(true)}
                disabled={isPushing === editingItem.id}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg shadow-xs flex items-center space-x-1.5"
              >
                <UploadCloud className="w-3.5 h-3.5" />
                <span>{isPushing === editingItem.id ? 'Pushing...' : 'Save & Push to Google Sheet'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* VIEW 1: Active MAP Breaches */}
      {activeTab === 'breaches' && (
        <div className="space-y-4">
          {filteredBreaches.length === 0 ? (
            <div className="p-12 text-center bg-white border border-slate-200 rounded-xl space-y-2">
              <CheckCircle2 className="w-8 h-8 text-emerald-600 mx-auto" />
              <h3 className="text-sm font-bold text-slate-800">No Active MAP Breaches Detected</h3>
              <p className="text-xs text-slate-500">All marketplace selling prices are strictly aligned with target MAP guidelines.</p>
            </div>
          ) : (
            filteredBreaches.map((breach) => (
              <div
                key={breach.id}
                className="p-5 bg-white rounded-xl border border-rose-200 shadow-xs space-y-3.5"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                  <div className="flex items-center space-x-2.5">
                    <span className="px-2 py-0.5 bg-rose-100 text-rose-700 border border-rose-200 font-mono text-xs font-bold rounded uppercase">
                      {breach.id}
                    </span>
                    <span className="text-xs font-bold text-slate-900 uppercase">{breach.channel}</span>
                    <span className="text-slate-300">&bull;</span>
                    <span className="text-xs text-slate-500">
                      Violating Reseller: <strong className="text-rose-600">{breach.violatingSeller}</strong>
                    </span>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleStartEdit({
                        id: breach.id,
                        sku: breach.sku,
                        productName: breach.productName,
                        marketplace: breach.channel,
                        currentSellingPrice: breach.violatedPrice,
                        targetMap: breach.enforcedMap,
                        buyBoxOwner: breach.violatingSeller
                      })}
                      className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded flex items-center space-x-1 border border-slate-300 transition-colors"
                    >
                      <Edit3 className="w-3 h-3 text-slate-600" />
                      <span>Edit Price / MAP</span>
                    </button>

                    <span className={`px-2 py-0.5 rounded text-xs font-bold border ${
                      breach.status === 'Actioned'
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        : 'bg-rose-50 text-rose-700 border border-rose-200'
                    }`}>
                      {breach.status}
                    </span>
                  </div>
                </div>

                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">{breach.sku} - {breach.productName}</h4>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Breach Duration: <strong className="text-slate-800">{breach.breachDurationHours} Hours</strong> without authorization
                    </p>
                  </div>

                  <div className="flex items-center space-x-6">
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-bold block">Enforced MAP</span>
                      <span className="text-sm font-bold text-slate-900">{formatINR(breach.enforcedMap)}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-rose-600 uppercase font-bold block">Violating Price</span>
                      <span className="text-base font-bold text-rose-600">{formatINR(breach.violatedPrice)}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-rose-600 uppercase font-bold block">Discount</span>
                      <span className="text-sm font-bold text-rose-600">{breach.discountPercent}%</span>
                    </div>
                  </div>
                </div>

                {/* Compliance Action Row */}
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                  <div className="flex items-center space-x-2 text-slate-700">
                    <ShieldAlert className="w-4 h-4 text-rose-600 shrink-0" />
                    <span>{breach.complianceAction}</span>
                  </div>

                  {breach.status !== 'Actioned' && (
                    <button
                      id={`action-legal-${breach.id}`}
                      onClick={() => handleActionLegalNotice(breach.id)}
                      className="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-md text-xs shadow-2xs transition-colors shrink-0"
                    >
                      Issue 1-Click Cease & Desist
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* VIEW 2: Complete Channel Pricing Matrix */}
      {activeTab === 'all_channel_pricing' && (
        <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-100 text-slate-600 uppercase text-[10px] font-bold border-b border-slate-200 tracking-wider">
                <tr>
                  <th className="py-3 px-4">Marketplace</th>
                  <th className="py-3 px-4">SKU Code</th>
                  <th className="py-3 px-4">Product Name</th>
                  <th className="py-3 px-3 text-right">Target MAP</th>
                  <th className="py-3 px-3 text-right">Selling Price</th>
                  <th className="py-3 px-3 text-right">Delta / Breach</th>
                  <th className="py-3 px-3">BuyBox Seller</th>
                  <th className="py-3 px-3 text-center">Status</th>
                  <th className="py-3 px-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredChannelPricing.map((cp) => (
                  <tr key={cp.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-100 text-slate-800 border border-slate-200">
                        {cp.marketplace}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-slate-900">{cp.sku}</td>
                    <td className="py-3 px-4 font-semibold text-slate-900">{cp.productName}</td>
                    <td className="py-3 px-3 text-right font-mono text-slate-700">{formatINR(cp.targetMap)}</td>
                    <td className={`py-3 px-3 text-right font-mono font-bold ${
                      cp.mapBreached ? 'text-rose-600' : 'text-slate-900'
                    }`}>
                      {formatINR(cp.currentSellingPrice)}
                    </td>
                    <td className="py-3 px-3 text-right font-mono font-bold">
                      {cp.mapBreached ? (
                        <span className="text-rose-600">-{formatINR(Math.abs(cp.priceDelta))} (Breach)</span>
                      ) : (
                        <span className="text-emerald-600">+{formatINR(cp.priceDelta)} (OK)</span>
                      )}
                    </td>
                    <td className="py-3 px-3 font-mono text-[11px] text-slate-700">{cp.buyBoxOwner}</td>
                    <td className="py-3 px-3 text-center">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        cp.mapBreached
                          ? 'bg-rose-100 text-rose-800 border border-rose-200'
                          : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                      }`}>
                        {cp.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={() => handleStartEdit({
                          id: cp.id,
                          sku: cp.sku,
                          productName: cp.productName,
                          marketplace: cp.marketplace as MarketplaceId,
                          currentSellingPrice: cp.currentSellingPrice,
                          targetMap: cp.targetMap,
                          buyBoxOwner: cp.buyBoxOwner,
                          inStock: cp.inStock
                        })}
                        className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold rounded border border-slate-300 transition-colors flex items-center space-x-1 mx-auto"
                      >
                        <Edit3 className="w-3 h-3 text-slate-600" />
                        <span>Edit</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

