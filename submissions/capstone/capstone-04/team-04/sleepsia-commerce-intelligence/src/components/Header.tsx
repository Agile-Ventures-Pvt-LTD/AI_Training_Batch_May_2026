import React from 'react';
import {
  Sparkles,
  FileSpreadsheet,
  Send,
  RefreshCw,
  TrendingUp,
  Calendar,
  Layers,
  Filter,
  CheckCircle2,
  Shield,
  Clock,
  ChevronDown,
  Cpu,
  ArrowRight,
} from 'lucide-react';
import { MarketplaceChannel, ProductCategory } from '../types/commerce';
import { UserProfile } from '../types/rbac';
import { SleepsiaLogo } from './SleepsiaLogo';

interface HeaderProps {
  selectedDate: string;
  onDateChange: (date: string) => void;
  availableDates: string[];
  selectedChannel: MarketplaceChannel | 'All';
  onChannelChange: (channel: MarketplaceChannel | 'All') => void;
  availableChannels: MarketplaceChannel[];
  selectedCategory: string;
  onCategoryChange: (cat: string) => void;
  availableCategories: string[];
  onOpenUpload: () => void;
  onRunAnalysis: () => void;
  onOpenEmailModal: () => void;
  onResetData: () => void;
  isAnalyzing: boolean;
  activeTab: string;
  currentUser: UserProfile;
  onOpenRoleSwitcher: () => void;
  timeRangePreset: 'today' | 'yesterday' | '7d' | '30d' | 'custom';
  onTimeRangeChange: (preset: 'today' | 'yesterday' | '7d' | '30d' | 'custom') => void;
  onNavigateToTab?: (tab: string) => void;
  onOpenAgentExecution?: () => void;
  activeAgentsCount?: number;
  activeFindingsCount?: number;
}

export const Header: React.FC<HeaderProps> = ({
  selectedDate,
  onDateChange,
  availableDates,
  selectedChannel,
  onChannelChange,
  availableChannels,
  selectedCategory,
  onCategoryChange,
  availableCategories,
  onOpenUpload,
  onRunAnalysis,
  onOpenEmailModal,
  onResetData,
  isAnalyzing,
  currentUser,
  onOpenRoleSwitcher,
  timeRangePreset,
  onTimeRangeChange,
  onNavigateToTab,
  onOpenAgentExecution,
  activeAgentsCount = 9,
  activeFindingsCount = 24,
}) => {
  return (
    <header className="bg-white border-b border-slate-200 shadow-xs">
      {/* Top Main Banner */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
        {/* Brand & Platform Identity */}
        <div className="flex items-center gap-3.5">
          <div className="h-11 px-3 py-1 rounded-xl bg-white border border-slate-200 shadow-xs flex items-center justify-center">
            <SleepsiaLogo className="h-8 w-auto" />
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <span className="font-display bg-blue-50 text-blue-700 text-xs sm:text-sm font-bold px-2.5 py-0.5 rounded-full border border-blue-200/80">
                Commerce Intelligence OS
              </span>
              <span className="hidden md:inline-flex items-center gap-1.5 text-xs font-bold bg-emerald-50 text-emerald-700 px-2.5 py-0.5 rounded-full border border-emerald-200">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                9 Agents Active
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-500 font-medium mt-0.5">Autonomous Omnichannel Decision Platform</p>
          </div>
        </div>

        {/* Global Action Workflow Controls */}
        <div className="flex items-center flex-wrap gap-2.5">
          {/* RBAC Active Role Persona Badge */}
          <button
            onClick={onOpenRoleSwitcher}
            title="Click to switch user role persona (Admin, Executive, Marketplace Manager, Ads Manager, Inventory Manager, Product Manager)"
            className="flex items-center gap-2.5 bg-slate-100/90 hover:bg-slate-200/80 border border-slate-300 rounded-xl pl-2 pr-3 py-1.5 text-sm transition-all shadow-xs"
          >
            <img
              src={currentUser.avatar}
              alt={currentUser.name}
              className="w-7 h-7 rounded-full object-cover border border-slate-300 shadow-xs"
            />
            <div className="text-left">
              <div className="text-xs sm:text-sm font-bold text-slate-900 leading-tight">{currentUser.name}</div>
              <div className="text-[11px] font-semibold text-blue-700 leading-tight">{currentUser.role}</div>
            </div>
            <span className="text-[10px] font-bold bg-blue-600 hover:bg-blue-700 text-white px-2 py-0.5 rounded-md ml-0.5 tracking-wide">
              Switch
            </span>
          </button>

          {/* Supervisor Status Button / Pill (Clickable) */}
          <button
            onClick={() => {
              if (onNavigateToTab) {
                onNavigateToTab('orchestration');
              } else if (onOpenAgentExecution) {
                onOpenAgentExecution();
              } else {
                onRunAnalysis();
              }
            }}
            title="Click to view live Supervisor Agent execution & dedicated pipeline flow canvas"
            className="flex items-center gap-2.5 bg-slate-900 hover:bg-slate-800 text-white border border-slate-700/80 rounded-xl px-3 py-1.5 text-xs transition-all shadow-xs group"
          >
            <div className="w-5 h-5 rounded-md bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <Cpu className="w-3.5 h-3.5" />
            </div>
            <div className="text-left leading-tight hidden lg:block">
              <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">SUPERVISOR STATUS</div>
              <div className="text-[11px] font-bold text-emerald-400">
                {activeAgentsCount} Agents • {activeFindingsCount} Findings
              </div>
            </div>
            <span className="bg-blue-600 group-hover:bg-blue-500 text-white font-bold text-[11px] px-2 py-0.5 rounded-md flex items-center gap-1 shadow-xs">
              Live <ArrowRight className="w-3 h-3" />
            </span>
          </button>

          {/* Run Multi-Agent Analysis */}
          <button
            id="btn-run-analysis"
            onClick={onRunAnalysis}
            disabled={isAnalyzing}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold px-4 py-2 rounded-xl shadow-xs transition-all disabled:opacity-50"
          >
            {isAnalyzing ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Running Agents...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-blue-200" />
                <span>Run Agent Analysis</span>
              </>
            )}
          </button>

          {/* Send Daily Report */}
          <button
            id="btn-send-email-top"
            onClick={onOpenEmailModal}
            className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold px-3.5 py-2 rounded-xl transition-colors shadow-xs"
          >
            <Send className="w-4 h-4" />
            <span>Send Report</span>
          </button>

          {/* Upload Dataset */}
          <button
            id="btn-upload-excel"
            onClick={onOpenUpload}
            className="flex items-center gap-2 bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 text-sm font-semibold px-3 py-2 rounded-xl transition-colors shadow-xs"
          >
            <FileSpreadsheet className="w-4 h-4 text-emerald-600" />
            <span>Upload</span>
          </button>

          <button
            id="btn-reset-data"
            onClick={onResetData}
            title="Reset to default Sleepsia dataset"
            className="p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-colors border border-slate-300 shadow-xs"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Global Interactive Filter & Time Comparison Toolbar */}
      <div className="bg-slate-100/70 border-t border-slate-200 px-4 sm:px-6 lg:px-8 py-2.5">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3 text-sm">
          <div className="flex flex-wrap items-center gap-3.5">
            {/* Quick Time Comparison Selector */}
            <div className="flex items-center bg-white border border-slate-300 rounded-xl p-1 shadow-xs">
              <span className="text-xs font-bold text-slate-500 px-2.5 uppercase tracking-wider">Period:</span>
              {(['today', 'yesterday', '7d', '30d'] as const).map((preset) => (
                <button
                  key={preset}
                  onClick={() => onTimeRangeChange(preset)}
                  className={`px-3 py-1 rounded-lg text-xs sm:text-sm font-bold transition-all ${
                    timeRangePreset === preset
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  {preset === 'today'
                    ? 'Today'
                    : preset === 'yesterday'
                    ? 'vs Yesterday'
                    : preset === '7d'
                    ? 'Last 7D'
                    : 'Last 30D'}
                </button>
              ))}
            </div>

            {/* Date Selector */}
            <div className="flex items-center gap-2 text-slate-800">
              <Calendar className="w-4 h-4 text-blue-600" />
              <span className="text-slate-600 font-semibold text-xs sm:text-sm">Reporting Date:</span>
              <select
                id="select-reporting-date"
                value={selectedDate}
                onChange={(e) => onDateChange(e.target.value)}
                className="bg-white border border-slate-300 text-slate-900 rounded-lg px-3 py-1.5 text-xs sm:text-sm shadow-xs focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none font-semibold cursor-pointer"
              >
                {availableDates.map((d) => (
                  <option key={d} value={d}>
                    {d} {d === availableDates[availableDates.length - 1] ? '(Latest)' : ''}
                  </option>
                ))}
              </select>
            </div>

            {/* Marketplace Filter */}
            <div className="flex items-center gap-2 text-slate-800">
              <Layers className="w-4 h-4 text-indigo-600" />
              <span className="text-slate-600 font-semibold text-xs sm:text-sm">Marketplace:</span>
              <select
                id="select-marketplace-filter"
                value={selectedChannel}
                onChange={(e) => onChannelChange(e.target.value as any)}
                className="bg-white border border-slate-300 text-slate-900 rounded-lg px-3 py-1.5 text-xs sm:text-sm shadow-xs focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none font-semibold cursor-pointer"
              >
                <option value="All">All 14 Channels</option>
                {availableChannels.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>

            {/* Category Filter */}
            <div className="flex items-center gap-2 text-slate-800">
              <Filter className="w-4 h-4 text-amber-600" />
              <span className="text-slate-600 font-semibold text-xs sm:text-sm">Category:</span>
              <select
                id="select-category-filter"
                value={selectedCategory}
                onChange={(e) => onCategoryChange(e.target.value)}
                className="bg-white border border-slate-300 text-slate-900 rounded-lg px-3 py-1.5 text-xs sm:text-sm shadow-xs focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none font-semibold cursor-pointer"
              >
                <option value="All">All Categories</option>
                {availableCategories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Connected Data Health Badge */}
          <div className="flex items-center gap-2.5 text-slate-600">
            <span className="flex items-center gap-2 text-emerald-700 font-bold bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 text-xs sm:text-sm shadow-2xs">
              <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-pulse"></span>
              11 Unified Data Streams
            </span>
            <span className="text-slate-300 hidden sm:inline">•</span>
            <span className="text-slate-500 font-medium text-xs sm:text-sm hidden sm:inline">IST (Asia/Kolkata)</span>
          </div>
        </div>
      </div>
    </header>
  );
};

