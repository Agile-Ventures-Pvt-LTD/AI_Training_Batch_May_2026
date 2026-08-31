import React, { useState, useMemo } from 'react';
import { Building2, X, Search, AlertTriangle, CheckCircle, Truck, MapPin, Package, ExternalLink } from 'lucide-react';
import { useData } from '../context/DataContext';

interface DarkStoreShortageModalProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenStockTransfer: (sku: string, hub: string, units?: number, darkStoreId?: string) => void;
}

export const DarkStoreShortageModal: React.FC<DarkStoreShortageModalProps> = ({
  isOpen,
  onClose,
  onOpenStockTransfer,
}) => {
  const { darkStores, skus } = useData();
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'Out Of Stock' | 'Low Stock' | 'In Stock'>('all');
  const [skuFilter, setSkuFilter] = useState<string>('all');
  const [platformFilter, setPlatformFilter] = useState<string>('all');

  const filteredStores = useMemo(() => {
    return darkStores.filter((store) => {
      if (statusFilter !== 'all' && store.status !== statusFilter) return false;
      if (skuFilter !== 'all' && store.sku !== skuFilter) return false;
      if (platformFilter !== 'all' && store.platform !== platformFilter) return false;
      if (
        searchQuery &&
        !store.storeName.toLowerCase().includes(searchQuery.toLowerCase()) &&
        !store.storeId.toLowerCase().includes(searchQuery.toLowerCase()) &&
        !store.city.toLowerCase().includes(searchQuery.toLowerCase()) &&
        !(store.sku && store.sku.toLowerCase().includes(searchQuery.toLowerCase())) &&
        !(store.productName && store.productName.toLowerCase().includes(searchQuery.toLowerCase()))
      ) {
        return false;
      }
      return true;
    });
  }, [darkStores, statusFilter, skuFilter, platformFilter, searchQuery]);

  const oosCount = darkStores.filter((d) => d.status === 'Out Of Stock').length;
  const lowStockCount = darkStores.filter((d) => d.status === 'Low Stock').length;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 overflow-y-auto animate-fadeIn">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden">
        
        {/* Modal Header */}
        <div className="px-6 py-4 bg-slate-900 text-white flex items-center justify-between shrink-0">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 bg-blue-600 rounded-xl flex items-center justify-center shadow-xs">
              <Building2 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-sm font-bold tracking-wide">Dark Store Pod Shortage & SKU Allocation Matrix</h2>
              <p className="text-xs text-slate-400">
                Analyze precise micro-fulfillment inventory shortages by pod, city, and SKU for targeted Mother Hub replenishment
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Filters & KPI Bar */}
        <div className="p-4 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3 shrink-0 text-xs">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-semibold text-slate-600">Status Filter:</span>
            {(['all', 'Out Of Stock', 'Low Stock', 'In Stock'] as const).map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-3 py-1.5 rounded-lg font-bold transition-all ${
                  statusFilter === st
                    ? st === 'Out Of Stock'
                      ? 'bg-red-600 text-white shadow-2xs'
                      : st === 'Low Stock'
                      ? 'bg-amber-600 text-white shadow-2xs'
                      : 'bg-blue-600 text-white shadow-2xs'
                    : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
                }`}
              >
                {st === 'all' ? `All Pods (${darkStores.length})` : st === 'Out Of Stock' ? `🚨 OOS (${oosCount})` : st === 'Low Stock' ? `⚠️ Low Stock (${lowStockCount})` : '✅ Healthy'}
              </button>
            ))}
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <select
              value={skuFilter}
              onChange={(e) => setSkuFilter(e.target.value)}
              className="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-slate-800 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All SKUs ({skus.length})</option>
              {skus.map((s) => (
                <option key={s.sku} value={s.sku}>{s.sku} - {s.name.substring(0, 30)}...</option>
              ))}
            </select>

            <select
              value={platformFilter}
              onChange={(e) => setPlatformFilter(e.target.value)}
              className="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-slate-800 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Platforms</option>
              <option value="blinkit">Blinkit</option>
              <option value="zepto">Zepto</option>
              <option value="instamart">Instamart</option>
              <option value="jiomart">JioMart</option>
            </select>
          </div>
        </div>

        {/* Search Bar */}
        <div className="px-6 py-3 bg-white border-b border-slate-100 flex items-center gap-3 shrink-0">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by pod name, store ID, city, SKU code or product name..."
              className="w-full pl-9 pr-4 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <span className="text-xs font-semibold text-slate-500 shrink-0">
            Showing <strong className="text-slate-900">{filteredStores.length}</strong> matching pods
          </span>
        </div>

        {/* Dark Stores Table Content */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-50/50">
          <div className="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase text-[10px] font-bold">
                  <th className="py-3 px-4">Dark Store Pod</th>
                  <th className="py-3 px-3">Platform</th>
                  <th className="py-3 px-3">Location</th>
                  <th className="py-3 px-4">Assigned SKU & Item</th>
                  <th className="py-3 px-3">Pod Stock Status</th>
                  <th className="py-3 px-3">Connected Mother Hub</th>
                  <th className="py-3 px-4 text-right">Replenish Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredStores.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-12 text-center text-slate-400">
                      No dark store pods match your filter criteria.
                    </td>
                  </tr>
                ) : (
                  filteredStores.map((store) => {
                    const isOos = store.status === 'Out Of Stock';
                    const isLow = store.status === 'Low Stock';
                    const suggestedUnits = Math.max(50, ((store.safetyThreshold || 25) * 3) - store.availableStock);

                    return (
                      <tr key={`${store.storeId}-${store.sku}`} className="hover:bg-slate-50 transition-colors">
                        <td className="py-3.5 px-4">
                          <div className="font-bold text-slate-900">{store.storeName}</div>
                          <div className="font-mono text-[10px] text-slate-500">{store.storeId}</div>
                        </td>
                        <td className="py-3.5 px-3">
                          <span className="px-2 py-0.5 rounded font-bold uppercase text-[10px] bg-slate-100 border border-slate-200 text-slate-700">
                            {store.platform}
                          </span>
                        </td>
                        <td className="py-3.5 px-3">
                          <div className="font-medium text-slate-800">{store.city}</div>
                          <div className="text-[10px] text-slate-500 font-mono">PIN: {store.pincode}</div>
                        </td>
                        <td className="py-3.5 px-4">
                          <div className="font-mono font-bold text-blue-700">{store.sku || 'SKU-SC-001'}</div>
                          <div className="text-slate-600 text-[11px] truncate max-w-xs">{store.productName || 'Cooling Gel Memory Foam Pillow'}</div>
                        </td>
                        <td className="py-3.5 px-3">
                          <span className={`inline-flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-bold ${
                            isOos
                              ? 'bg-red-50 text-red-700 border border-red-200'
                              : isLow
                              ? 'bg-amber-50 text-amber-800 border border-amber-200'
                              : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          }`}>
                            {isOos && <AlertTriangle className="w-3 h-3 text-red-600" />}
                            {isLow && <AlertTriangle className="w-3 h-3 text-amber-600" />}
                            {!isOos && !isLow && <CheckCircle className="w-3 h-3 text-emerald-600" />}
                            <span>{isOos ? '0 Units (OOS)' : `${store.availableStock} Units (${store.status})`}</span>
                          </span>
                          <div className="text-[10px] text-slate-400 mt-0.5">SLA: {store.deliverySlaMins || 10} mins</div>
                        </td>
                        <td className="py-3.5 px-3">
                          <div className="font-bold text-slate-900">{store.motherHubName || 'Bengaluru Central Mother Hub'}</div>
                          <div className="text-[10px] text-emerald-700 font-medium">Hub Stock: {store.motherHubStock?.toLocaleString()} units</div>
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <button
                            onClick={() => {
                              onOpenStockTransfer(
                                store.sku || 'SKU-SC-001',
                                store.motherHubName || 'Bengaluru Central Mother Hub (Nelamangala)',
                                suggestedUnits,
                                store.storeId
                              );
                              onClose();
                            }}
                            className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center space-x-1.5 ml-auto transition-colors shadow-2xs ${
                              isOos || isLow
                                ? 'bg-red-600 hover:bg-red-700 text-white'
                                : 'bg-blue-600 hover:bg-blue-700 text-white'
                            }`}
                          >
                            <Truck className="w-3.5 h-3.5" />
                            <span>Transfer {suggestedUnits} Units</span>
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

        {/* Modal Footer */}
        <div className="px-6 py-4 bg-white border-t border-slate-200 flex items-center justify-between shrink-0 text-xs">
          <div className="text-slate-500">
            💡 Click <strong className="text-slate-800">Transfer</strong> on any dark store pod to instantly dispatch buffer stock from the assigned Mother Hub.
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg font-bold transition-colors"
          >
            Close Matrix
          </button>
        </div>

      </div>
    </div>
  );
};
