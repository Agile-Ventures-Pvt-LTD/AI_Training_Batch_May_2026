/**
 * Agile Solutions
 * Autonomous Control Tower & E-commerce Intelligence
 */

import React, { useState, useEffect } from 'react';
import { ViewMode, MarketplaceId, UserRole, AlertAnomaly, SKUListing, MAPBreach } from './types';
import { OWNER_EMAIL, SENDER_GMAIL, formatINR } from './data/mockData';
import { useData, USER_PERSONAS } from './context/DataContext';

// Components
import { Sidebar } from './components/Sidebar';
import { Topbar } from './components/Topbar';
import { AIAssistantDrawer } from './components/AIAssistantDrawer';
import { EmailDispatchModal } from './components/EmailDispatchModal';
import { StockTransferModal } from './components/StockTransferModal';
import { DarkStoreShortageModal } from './components/DarkStoreShortageModal';

// Views
import { CommandCenterView } from './components/views/CommandCenterView';
import { DigitalShelfView } from './components/views/DigitalShelfView';
import { SupplyChainView } from './components/views/SupplyChainView';
import { AutonomousAIView } from './components/views/AutonomousAIView';
import { DatasetSyncView } from './components/views/DatasetSyncView';

export default function App() {
  const { skus, alerts, currentUser, setCurrentUser } = useData();

  // Navigation & Filtering State
  const [activeView, setActiveView] = useState<ViewMode>('command-center');
  const [selectedChannel, setSelectedChannel] = useState<MarketplaceId | 'all'>('all');
  const [selectedDateRange, setSelectedDateRange] = useState<string>('Last 30 Days (WBR)');
  const [userRole, setUserRole] = useState<UserRole>('Owner');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedSkuId, setSelectedSkuId] = useState<string>('SLP-1001');

  const handleRoleChange = (newRole: UserRole) => {
    setUserRole(newRole);
    const persona = USER_PERSONAS.find(p => p.role === newRole) || USER_PERSONAS[0];
    setCurrentUser(persona);
    if (newRole === 'Analyst' && (activeView === 'dataset-sync' || activeView === 'autonomous-ai' || activeView === 'supply-chain')) {
      setActiveView('command-center');
    }
  };

  // Keep selectedSkuId valid if SKUs load/change
  useEffect(() => {
    if (skus.length > 0 && !skus.some(s => s.sku === selectedSkuId || s.id === selectedSkuId)) {
      setSelectedSkuId(skus[0].sku || skus[0].id);
    }
  }, [skus, selectedSkuId]);

  // Modals & Drawers State
  const [isAiDrawerOpen, setIsAiDrawerOpen] = useState(false);
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false);
  const [emailAnomalyContext, setEmailAnomalyContext] = useState<AlertAnomaly | undefined>(undefined);
  const [emailSkuContext, setEmailSkuContext] = useState<SKUListing | undefined>(undefined);
  const [emailMapContext, setEmailMapContext] = useState<MAPBreach[] | null>(null);
  const [emailModalMode, setEmailModalMode] = useState<'live' | 'schedule'>('live');

  const [isTransferModalOpen, setIsTransferModalOpen] = useState(false);
  const [transferSkuId, setTransferSkuId] = useState<string>('SLP-1001');
  const [transferMotherHub, setTransferMotherHub] = useState<string>('Bengaluru Central Mother Hub (Nelamangala)');
  const [transferDefaultUnits, setTransferDefaultUnits] = useState<number>(250);

  const [isDarkStoreShortageModalOpen, setIsDarkStoreShortageModalOpen] = useState(false);

  // Audio Voice Briefing
  const [isVoicePlaying, setIsVoicePlaying] = useState(false);

  const activeAnomaliesCount = alerts.filter(a => a.status !== 'Resolved').length;

  const handleToggleVoiceBriefing = () => {
    if (!isVoicePlaying) {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const totalSales = skus.reduce((sum, s) => sum + (s.grossSales30d || (s.sellingPrice * 100)), 0);
        const lowStockCount = skus.filter(s => (s.darkStoreStock ?? 15) < 10).length;
        const text = `Autonomous Control Tower Audio Briefing for Vikash Kumar. Active dataset contains ${skus.length} live SKUs. Total estimated 30-day catalog revenue is ${formatINR(totalSales, { abbreviate: true })}. Currently, there are ${activeAnomaliesCount} active critical anomalies and ${lowStockCount} SKUs requiring dark-store rebalancing from Mother Hub.`;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.onend = () => setIsVoicePlaying(false);
        utterance.onerror = () => setIsVoicePlaying(false);
        window.speechSynthesis.speak(utterance);
        setIsVoicePlaying(true);
      } else {
        setIsVoicePlaying(true);
        setTimeout(() => setIsVoicePlaying(false), 8000);
      }
    } else {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      setIsVoicePlaying(false);
    }
  };

  // Handlers for cross-component triggers
  const handleOpenEmailModal = (
    arg1?: AlertAnomaly | SKUListing | MAPBreach[] | null | string,
    arg2?: SKUListing | null | string,
    arg3: 'live' | 'schedule' = 'live'
  ) => {
    if (typeof arg1 === 'string') {
      setEmailAnomalyContext(undefined);
      setEmailSkuContext(undefined);
      setEmailMapContext(undefined);
      setEmailModalMode(arg1 === 'schedule' ? 'schedule' : 'live');
    } else if (Array.isArray(arg1)) {
      setEmailAnomalyContext(undefined);
      setEmailSkuContext(undefined);
      setEmailMapContext(arg1 as MAPBreach[]);
      setEmailModalMode((arg2 as 'live' | 'schedule') || 'live');
    } else if (arg1 && typeof arg1 === 'object' && 'sku' in arg1 && 'name' in arg1 && !('marketplace' in arg1)) {
      // arg1 is SKUListing
      setEmailAnomalyContext(undefined);
      setEmailSkuContext(arg1 as SKUListing);
      setEmailMapContext(undefined);
      setEmailModalMode((arg2 as 'live' | 'schedule') || 'live');
    } else if (arg1 && typeof arg1 === 'object' && 'marketplace' in arg1) {
      // arg1 is AlertAnomaly
      setEmailAnomalyContext(arg1 as AlertAnomaly);
      setEmailSkuContext(undefined);
      setEmailMapContext(undefined);
      setEmailModalMode((arg2 as 'live' | 'schedule') || 'live');
    } else {
      setEmailAnomalyContext((arg1 as AlertAnomaly) || undefined);
      setEmailSkuContext((arg2 as SKUListing) || undefined);
      setEmailMapContext(null);
      setEmailModalMode(arg3);
    }
    setIsEmailModalOpen(true);
  };

  const handleOpenStockTransfer = (sku: string, hub: string, units?: number) => {
    setTransferSkuId(sku);
    setTransferMotherHub(hub);
    setTransferDefaultUnits(units || 20);
    setIsTransferModalOpen(true);
  };

  const handleSelectSku = (skuId: string) => {
    setSelectedSkuId(skuId);
    setActiveView('sku-360');
  };

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 font-sans antialiased overflow-hidden">
      {/* 1. Left Sidebar Navigation */}
      <Sidebar
        activeView={activeView}
        onSelectView={setActiveView}
        activeAnomaliesCount={activeAnomaliesCount}
        currentUserRole={userRole}
      />

      {/* 2. Main Content Canvas */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-slate-50">
        {/* Topbar */}
        <Topbar
          selectedChannel={selectedChannel}
          onSelectChannel={setSelectedChannel}
          selectedDateRange={selectedDateRange}
          onSelectDateRange={setSelectedDateRange}
          userRole={userRole}
          onChangeUserRole={handleRoleChange}
          onOpenAIAssistant={() => setIsAiDrawerOpen(true)}
          onOpenEmailModal={() => handleOpenEmailModal(undefined, 'live')}
          onSearchQuery={setSearchQuery}
          searchQuery={searchQuery}
          onToggleVoiceBriefing={handleToggleVoiceBriefing}
          isVoicePlaying={isVoicePlaying}
          activeAnomaliesCount={activeAnomaliesCount}
        />

        {/* Scrollable View Area */}
        <main className="flex-1 overflow-y-auto p-6 custom-scrollbar bg-slate-50">
          <div className="max-w-7xl mx-auto space-y-6">
            
            {(activeView === 'command-center' || activeView === 'executive-tower' || activeView === 'sales-intelligence') && (
              <CommandCenterView
                selectedChannel={selectedChannel}
                onSelectSku={handleSelectSku}
                onOpenStockTransfer={handleOpenStockTransfer}
                onOpenEmailModal={handleOpenEmailModal}
                onNavigateView={setActiveView}
              />
            )}

            {(activeView === 'digital-shelf' || activeView === 'price-map-intel' || activeView === 'search-share' || activeView === 'competitor-watch' || activeView === 'content-studio' || activeView === 'reviews-voc' || activeView === 'advertising-roas' || activeView === 'returns-quality') && (
              <DigitalShelfView
                selectedChannel={selectedChannel}
                onSelectSku={handleSelectSku}
                onOpenEmailModal={handleOpenEmailModal}
              />
            )}

            {(activeView === 'supply-chain' || activeView === 'dark-stores-supply-chain' || activeView === 'perishables-expiry' || activeView === 'sku-360') && (
              currentUser?.role === 'Analyst' ? (
                <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 shadow-sm space-y-4">
                  <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-full flex items-center justify-center mx-auto font-bold text-xl">🔒</div>
                  <h3 className="text-lg font-bold text-slate-900">Supply Chain & Dark Stores Restricted</h3>
                  <p className="text-sm text-slate-500 max-w-md mx-auto">This workspace is restricted to Owner access. Analysts have read-only telemetry permissions on the Command Center.</p>
                </div>
              ) : (
                <SupplyChainView
                  selectedChannel={selectedChannel}
                  onOpenStockTransfer={handleOpenStockTransfer}
                  onOpenEmailModal={handleOpenEmailModal}
                  onOpenShortageModal={() => setIsDarkStoreShortageModalOpen(true)}
                />
              )
            )}

            {(activeView === 'autonomous-ai' || activeView === 'alerts-anomalies' || activeView === 'autonomous-actions' || activeView === 'ai-agents') && (
              currentUser?.role === 'Analyst' ? (
                <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 shadow-sm space-y-4">
                  <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-full flex items-center justify-center mx-auto font-bold text-xl">🔒</div>
                  <h3 className="text-lg font-bold text-slate-900">Autonomous AI Restricted</h3>
                  <p className="text-sm text-slate-500 max-w-md mx-auto">This workspace is restricted to Owner access.</p>
                </div>
              ) : (
                <AutonomousAIView
                  onOpenStockTransfer={handleOpenStockTransfer}
                  onOpenEmailModal={handleOpenEmailModal}
                />
              )
            )}

            {(activeView === 'dataset-sync' || activeView === 'settings-rbac' || activeView === 'executive-reports') && (
              currentUser?.role === 'Analyst' ? (
                <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 shadow-sm space-y-4">
                  <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-full flex items-center justify-center mx-auto font-bold text-xl">🔒</div>
                  <h3 className="text-lg font-bold text-slate-900">Dataset & Sync Restricted</h3>
                  <p className="text-sm text-slate-500 max-w-md mx-auto">This workspace is restricted to Owner access. Analysts have read-only telemetry permissions on the Command Center.</p>
                </div>
              ) : (
                <DatasetSyncView />
              )
            )}

          </div>
        </main>

        {/* Clean Light Bottom Status Bar */}
        <footer className="h-8 bg-white border-t border-slate-200 px-6 flex items-center justify-between text-[10px] text-slate-500 uppercase tracking-widest shrink-0 select-none">
          <div className="flex items-center gap-3">
            <span>System Role: <strong className="text-slate-800 font-semibold">{userRole}</strong> (Full Access)</span>
            <span className="text-slate-300">|</span>
            <span>Channel Sync: <span className="text-emerald-600 font-bold">100% Operational</span></span>
          </div>
          <div className="flex items-center gap-4">
            <span>Amazon: <strong className="text-slate-700">Stable</strong></span>
            <span>Zepto: <strong className="text-slate-700">Active</strong></span>
            <span>Blinkit: <strong className="text-slate-700">Connected</strong></span>
            <span>Agent Status: <strong className="text-blue-600 font-bold">Monitoring</strong></span>
          </div>
        </footer>
      </div>

      {/* 3. AI Assistant Floating Drawer */}
      <AIAssistantDrawer
        isOpen={isAiDrawerOpen}
        onClose={() => setIsAiDrawerOpen(false)}
        onOpenEmailModal={handleOpenEmailModal}
        onOpenStockTransfer={handleOpenStockTransfer}
      />

      {/* 4. Live & Scheduled Email Modal */}
      <EmailDispatchModal
        isOpen={isEmailModalOpen}
        onClose={() => setIsEmailModalOpen(false)}
        anomaly={emailAnomalyContext}
        skuContext={emailSkuContext}
        mapAuditContext={emailMapContext}
        defaultMode={emailModalMode}
      />

      {/* 5. Stock Transfer Modal from Mother Hub */}
      <StockTransferModal
        isOpen={isTransferModalOpen}
        onClose={() => setIsTransferModalOpen(false)}
        defaultSku={transferSkuId}
        defaultMotherHub={transferMotherHub}
        defaultUnits={transferDefaultUnits}
      />

      {/* 6. Dark Store Shortage & SKU Allocation Matrix Modal */}
      <DarkStoreShortageModal
        isOpen={isDarkStoreShortageModalOpen}
        onClose={() => setIsDarkStoreShortageModalOpen(false)}
        onOpenStockTransfer={handleOpenStockTransfer}
      />
    </div>
  );
}
