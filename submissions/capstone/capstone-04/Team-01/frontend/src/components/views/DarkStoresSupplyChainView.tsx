import React, { useState } from 'react';
import {
  Building2,
  Truck,
  MapPin,
  Clock,
  CheckCircle,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  Search,
  PackageCheck,
  Network,
  LayoutGrid,
  Sparkles,
  Maximize2
} from 'lucide-react';
import { DarkStoreInventory, MarketplaceId } from '../../types';
import { DARK_STORES_INVENTORY, MOTHER_HUBS, formatINR } from '../../data/mockData';
import { NetworkArchitectureFlow } from '../NetworkArchitectureFlow';
import { useData } from '../../context/DataContext';

interface DarkStoresSupplyChainViewProps {
  selectedChannel: MarketplaceId | 'all';
  onOpenStockTransfer: (sku: string, hub: string, units?: number) => void;
  onOpenEmailModal: () => void;
}

export const DarkStoresSupplyChainView: React.FC<DarkStoresSupplyChainViewProps> = ({
  selectedChannel,
  onOpenStockTransfer,
  onOpenEmailModal
}) => {
  const { darkStores: dynamicStores, skus } = useData();
  const [showArchitectureDiagram, setShowArchitectureDiagram] = useState<boolean>(true);
  const [isFlowEnlarged, setIsFlowEnlarged] = useState<boolean>(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [cityFilter, setCityFilter] = useState<'all' | 'Bengaluru' | 'Mumbai' | 'Gurgaon'>('all');

  const sourceStores: DarkStoreInventory[] = dynamicStores && dynamicStores.length > 0
    ? dynamicStores
    : [];

  const filteredStores = sourceStores.filter((store) => {
    if (selectedChannel !== 'all' && store.platform !== selectedChannel) return false;
    if (cityFilter !== 'all' && store.city !== cityFilter) return false;
    if (
      searchQuery &&
      !store.storeName.toLowerCase().includes(searchQuery.toLowerCase()) &&
      !store.pincode.includes(searchQuery)
    ) {
      return false;
    }
    return true;
  });

  const oosStores = filteredStores.filter((s) => s.status === 'Out Of Stock');
  const inStockStores = filteredStores.filter((s) => s.status === 'In Stock');

  return (
    <div id="dark-stores-view" className="space-y-6">
      
      {/* Header Overview & Mode Switcher */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-sm font-bold uppercase tracking-widest text-slate-900">Quick Commerce Dark Stores & Mother Hubs</h2>
            <span className="px-2 py-0.5 bg-blue-50 text-blue-700 text-[10px] font-bold rounded border border-blue-200">
              {sourceStores.length} Pods Monitored
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time synchronization between Quick Commerce micro-fulfillment pods and regional Mother Hub reserves
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Architecture Mode Toggle */}
          <div className="bg-slate-100 p-1 rounded-lg border border-slate-200 flex items-center space-x-1 text-xs">
            <button
              id="view-architecture-diagram-btn"
              onClick={() => setShowArchitectureDiagram(true)}
              className={`px-3 py-1.5 rounded-md font-bold flex items-center space-x-1.5 transition-all ${
                showArchitectureDiagram
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Network className="w-3.5 h-3.5" />
              <span>Interactive Architecture Flow</span>
            </button>
            <button
              id="view-store-table-btn"
              onClick={() => setShowArchitectureDiagram(false)}
              className={`px-3 py-1.5 rounded-md font-bold flex items-center space-x-1.5 transition-all ${
                !showArchitectureDiagram
                  ? 'bg-white text-slate-900 shadow-2xs border border-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <LayoutGrid className="w-3.5 h-3.5" />
              <span>Store Pods Grid</span>
            </button>

            {/* Direct 1-Click Enlarge Button */}
            <button
              id="enlarge-architecture-flow-btn"
              onClick={() => {
                setShowArchitectureDiagram(true);
                setIsFlowEnlarged(true);
              }}
              className="px-2.5 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-md font-bold flex items-center space-x-1 border border-indigo-200 transition-all shadow-2xs"
              title="Enlarge Interactive Architecture Flow to Full View"
            >
              <Maximize2 className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Enlarge Flow</span>
            </button>
          </div>

          <div className="hidden sm:flex items-center space-x-2">
            <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-center">
              <span className="text-[9px] uppercase font-bold text-slate-500 block">Total Pods</span>
              <span className="text-xs font-bold text-slate-900">{DARK_STORES_INVENTORY.length}</span>
            </div>
            <div className="p-2.5 bg-red-50 border border-red-200 rounded-lg text-center">
              <span className="text-[9px] uppercase font-bold text-red-700 block">OOS Pods</span>
              <span className="text-xs font-bold text-red-600">{oosStores.length}</span>
            </div>
            <div className="p-2.5 bg-emerald-50 border border-emerald-200 rounded-lg text-center">
              <span className="text-[9px] uppercase font-bold text-emerald-700 block">Mother Hubs</span>
              <span className="text-xs font-bold text-emerald-700">{MOTHER_HUBS.length}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Interactive Visual Architecture Diagram Component */}
      {showArchitectureDiagram && (
        <NetworkArchitectureFlow
          onOpenStockTransfer={onOpenStockTransfer}
          onOpenEmailModal={onOpenEmailModal}
          isEnlarged={isFlowEnlarged}
          onToggleEnlarge={setIsFlowEnlarged}
        />
      )}

      {/* Regional Mother Hubs Status Bar */}
      <div className="space-y-3">
        <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">
          Regional Super Mother Hubs Network
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {MOTHER_HUBS.map((hub) => (
            <div key={hub.id} className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-100">
                  {hub.id}
                </span>
                <span className="text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded font-semibold">
                  {hub.coverageDarkStores} Pods Connected
                </span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 leading-tight">{hub.name}</h4>
              <p className="text-[11px] text-slate-600">{hub.location} (Pincode: {hub.pincode})</p>
              <div className="pt-2 border-t border-slate-100 flex justify-between text-xs">
                <span className="text-slate-500">Available Stock:</span>
                <span className="font-bold text-emerald-700">
                  {hub.currentStockUnits.toLocaleString()} Units
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <span className="font-semibold text-slate-600">City Filter:</span>
          {(['all', 'Bengaluru', 'Mumbai', 'Gurgaon'] as const).map((city) => (
            <button
              key={city}
              onClick={() => setCityFilter(city)}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                cityFilter === city
                  ? 'bg-blue-600 text-white shadow-2xs'
                  : 'bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200'
              }`}
            >
              {city === 'all' ? 'All Cities' : city}
            </button>
          ))}
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search store name or pincode..."
            className="w-full pl-8 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-md text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Dark Stores Inventory Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Dark Store Fulfillment Pods</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Showing {filteredStores.length} micro-warehouses and corresponding Mother Hub stock
            </p>
          </div>
          <button
            onClick={onOpenEmailModal}
            className="text-xs font-semibold text-blue-600 hover:text-blue-700"
          >
            Email Dark Store Digest to Owner &rarr;
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-[10px] uppercase font-bold">
                <th className="py-3 px-4">Dark Store Pod</th>
                <th className="py-3 px-4">Platform</th>
                <th className="py-3 px-4">City / Pincode</th>
                <th className="py-3 px-4">Dark Store Stock</th>
                <th className="py-3 px-4">Delivery SLA</th>
                <th className="py-3 px-4">Connected Mother Hub</th>
                <th className="py-3 px-4">Hub Stock</th>
                <th className="py-3 px-4 text-right">Intra-City Transfer</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredStores.map((store) => {
                const isOos = store.status === 'Out Of Stock';
                const isLow = store.status === 'Low Stock';

                return (
                  <tr key={store.storeId} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3.5 px-4">
                      <div className="font-bold text-slate-900">{store.storeName}</div>
                      <div className="font-mono text-[10px] text-slate-500">{store.storeId}</div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="px-2 py-0.5 rounded font-bold uppercase text-[10px] bg-slate-100 border border-slate-200 text-slate-700">
                        {store.platform}
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="text-slate-800 font-medium">{store.city}</div>
                      <div className="text-[10px] text-slate-500 font-mono">{store.pincode}</div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        isOos
                          ? 'bg-red-50 text-red-700 border border-red-200'
                          : isLow
                          ? 'bg-amber-50 text-amber-800 border border-amber-200'
                          : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                      }`}>
                        {isOos ? '0 Units (OOS)' : `${store.availableStock} Units`}
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="text-slate-600 font-medium">
                        {store.deliverySlaMins > 0 ? `${store.deliverySlaMins} mins` : 'Disabled (OOS)'}
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="font-bold text-slate-900">{store.motherHubName}</div>
                      <div className="text-[10px] text-slate-500">Transit: ~{store.transitHoursFromHub}h</div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="font-bold text-emerald-700">
                        {store.motherHubStock.toLocaleString()} Units
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      {isOos ? (
                        <button
                          id={`quick-transfer-${store.storeId}`}
                          onClick={() => {
                            const suggestedUnits = Math.max(20, ((store.safetyThreshold || 25) * 3) - store.availableStock);
                            onOpenStockTransfer(store.sku || 'SKU-SC-001', store.motherHubName, suggestedUnits);
                          }}
                          className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-xs font-bold transition-colors shadow-2xs"
                        >
                          Transfer {Math.max(20, ((store.safetyThreshold || 25) * 3) - store.availableStock)} Units
                        </button>
                      ) : (
                        <span className="text-[11px] text-slate-400 font-medium">Replenished</span>
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
