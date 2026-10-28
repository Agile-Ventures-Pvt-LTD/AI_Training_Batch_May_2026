import React, { useState, useEffect } from 'react';
import {
  Search,
  Calendar,
  Volume2,
  VolumeX,
  Sparkles,
  Mail,
  ChevronDown,
  Shield,
  RefreshCw,
  Check,
  Bot,
  ShieldCheck,
  Loader2,
  CheckCircle2
} from 'lucide-react';
import { MarketplaceId, UserRole } from '../types';
import { MARKETPLACE_CONFIGS, OWNER_EMAIL } from '../data/mockData';

interface TopbarProps {
  selectedChannel: MarketplaceId | 'all';
  onSelectChannel: (channel: MarketplaceId | 'all') => void;
  selectedDateRange: string;
  onSelectDateRange: (range: string) => void;
  userRole: UserRole;
  onChangeUserRole: (role: UserRole) => void;
  onOpenAIAssistant?: () => void;
  onOpenEmailModal: () => void;
  onSearchQuery: (query: string) => void;
  searchQuery: string;
  onToggleVoiceBriefing: () => void;
  isVoicePlaying: boolean;
  activeAnomaliesCount: number;
}

export const Topbar: React.FC<TopbarProps> = ({
  selectedChannel,
  onSelectChannel,
  selectedDateRange,
  onSelectDateRange,
  userRole,
  onChangeUserRole,
  onOpenAIAssistant,
  onOpenEmailModal,
  onSearchQuery,
  searchQuery,
  onToggleVoiceBriefing,
  isVoicePlaying,
  activeAnomaliesCount
}) => {
  const [roleDropdownOpen, setRoleDropdownOpen] = useState(false);
  const [dateDropdownOpen, setDateDropdownOpen] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const dateOptions = [
    'Last 30 Days (WBR)',
    'Last 7 Days (Tactical)',
    'Q3 2026 (Quarter-To-Date)',
    'Today (Real-Time Flash)'
  ];

  const roles: UserRole[] = [
    'Owner',
    'Analyst'
  ];

  const handleRefreshData = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
    }, 600);
  };

  return (
    <header id="main-topbar" className="bg-white border-b border-slate-200 sticky top-0 z-30 px-6 py-3 space-y-3 shadow-2xs">
      {/* Top Row: Search, Live Actions, Voice Briefing, User Dropdown */}
      <div className="flex items-center justify-between gap-4">
        {/* Global Search Bar */}
        <div className="relative flex-1 max-w-lg">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            id="global-search-input"
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchQuery(e.target.value)}
            placeholder="Search across 100 SKUs, ASINs, Dark Stores (#HSR-04), or Anomaly codes..."
            className="w-full pl-9 pr-4 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-md text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors"
          />
          {searchQuery && (
            <button
              onClick={() => onSearchQuery('')}
              className="absolute right-2.5 top-2 text-[10px] text-slate-400 hover:text-slate-600 font-medium"
            >
              Clear
            </button>
          )}
        </div>

        {/* Action Controls & Triggers */}
        <div className="flex items-center space-x-2.5">

          {/* Refresh telemetry */}
          <button
            id="refresh-telemetry-btn"
            onClick={handleRefreshData}
            title="Refresh All Marketplace Telemetry"
            className="p-1.5 text-slate-500 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 rounded-md border border-slate-200 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin text-blue-600' : ''}`} />
          </button>

          {/* AI Voice Briefing player button */}
          <button
            id="voice-briefing-toggle-btn"
            onClick={onToggleVoiceBriefing}
            className={`px-3 py-1.5 text-xs font-semibold rounded-md flex items-center space-x-2 border transition-all ${
              isVoicePlaying
                ? 'bg-rose-50 border-rose-300 text-rose-700 ring-1 ring-rose-500 animate-pulse'
                : 'bg-indigo-50 border-indigo-200 text-indigo-700 hover:bg-indigo-100'
            }`}
          >
            {isVoicePlaying ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5 text-indigo-600" />}
            <span className="hidden sm:inline">{isVoicePlaying ? 'Pause Audio' : 'Play Voice Briefing'}</span>
          </button>

          {/* Direct Live Email Dispatch to Owner (Hidden for Analyst) */}
          {userRole !== 'Analyst' && (
            <button
              id="topbar-send-email-btn"
              onClick={onOpenEmailModal}
              className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 text-emerald-800 text-xs font-semibold rounded-md flex items-center space-x-1.5 transition-colors"
            >
              <Mail className="w-3.5 h-3.5 text-emerald-600" />
              <span className="hidden md:inline">1-Click Auto-Send Email</span>
            </button>
          )}

          {/* AI Assistant (Top Right) */}
          <button
            id="topbar-ai-assistant-btn"
            onClick={onOpenAIAssistant}
            className="px-3 py-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white text-xs font-bold rounded-md flex items-center space-x-1.5 shadow-sm transition-all active:scale-95"
            title="Open AI Assistant & Intelligence Copilot"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-300 animate-pulse" />
            <span>AI Assistant</span>
            <span className="bg-blue-800/80 text-[10px] px-1.5 py-0.2 rounded font-mono text-blue-100 border border-blue-400/30">
              Copilot
            </span>
          </button>

          {/* Role Switcher Dropdown */}
          <div className="relative">
            <button
              id="role-dropdown-btn"
              onClick={() => setRoleDropdownOpen(!roleDropdownOpen)}
              className="px-2.5 py-1.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-xs font-semibold rounded-md flex items-center space-x-1.5 transition-colors"
            >
              <Shield className="w-3.5 h-3.5 text-blue-600" />
              <span>{userRole}</span>
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </button>

            {roleDropdownOpen && (
              <div
                id="role-dropdown-menu"
                className="absolute right-0 mt-1.5 w-52 bg-white border border-slate-200 rounded-lg shadow-xl py-1 z-50 animate-in fade-in"
              >
                <div className="px-3 py-1.5 border-b border-slate-100 text-[10px] uppercase font-bold text-slate-400">
                  Switch Active Role (RBAC)
                </div>
                {roles.map((r) => (
                  <button
                    key={r}
                    onClick={() => {
                      onChangeUserRole(r);
                      setRoleDropdownOpen(false);
                    }}
                    className={`w-full px-3 py-1.5 text-xs text-left flex items-center justify-between hover:bg-slate-50 ${
                      userRole === r ? 'font-bold text-blue-600 bg-blue-50' : 'text-slate-700'
                    }`}
                  >
                    <span>{r}</span>
                    {userRole === r && <Check className="w-3.5 h-3.5 text-blue-600" />}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Row: Marketplace Channel Filter Pills & Date Range Filter */}
      <div className="flex items-center justify-between border-t border-slate-100 pt-2.5 gap-3 overflow-x-auto custom-scrollbar">
        {/* Channel Pills */}
        <div className="flex items-center space-x-1.5 shrink-0">
          <button
            id="channel-filter-all"
            onClick={() => onSelectChannel('all')}
            className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
              selectedChannel === 'all'
                ? 'bg-blue-600 text-white shadow-2xs'
                : 'bg-slate-100 text-slate-600 border border-slate-200 hover:bg-slate-200 hover:text-slate-900'
            }`}
          >
            All Marketplaces (6)
          </button>

          {MARKETPLACE_CONFIGS.map((m) => {
            const isSelected = selectedChannel === m.id;
            return (
              <button
                key={m.id}
                id={`channel-filter-${m.id}`}
                onClick={() => onSelectChannel(m.id)}
                className={`px-2.5 py-1 text-xs font-medium rounded-md transition-all flex items-center space-x-1.5 ${
                  isSelected
                    ? 'bg-blue-600 text-white font-semibold shadow-2xs'
                    : 'bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200 hover:text-slate-900'
                }`}
              >
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: m.color }}
                />
                <span>{m.name}</span>
                {m.type === 'quick_commerce' && (
                  <span className={`text-[9px] px-1 py-0.2 rounded font-bold uppercase tracking-wider ${
                    isSelected ? 'bg-blue-800 text-white' : 'bg-amber-100 text-amber-800 border border-amber-200'
                  }`}>
                    QC
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Date Range Selector */}
        <div className="relative shrink-0">
          <button
            id="date-range-dropdown-btn"
            onClick={() => setDateDropdownOpen(!dateDropdownOpen)}
            className="px-3 py-1 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-md text-xs font-semibold text-slate-700 flex items-center space-x-1.5 transition-colors"
          >
            <Calendar className="w-3.5 h-3.5 text-slate-500" />
            <span>{selectedDateRange}</span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {dateDropdownOpen && (
            <div
              id="date-range-dropdown-menu"
              className="absolute right-0 mt-1 w-52 bg-white border border-slate-200 rounded-lg shadow-xl py-1 z-40"
            >
              {dateOptions.map((opt) => (
                <button
                  key={opt}
                  onClick={() => {
                    onSelectDateRange(opt);
                    setDateDropdownOpen(false);
                  }}
                  className={`w-full px-3 py-1.5 text-xs text-left hover:bg-slate-50 flex items-center justify-between ${
                    selectedDateRange === opt ? 'font-bold text-blue-600 bg-blue-50' : 'text-slate-700'
                  }`}
                >
                  <span>{opt}</span>
                  {selectedDateRange === opt && <Check className="w-3.5 h-3.5 text-blue-600" />}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
