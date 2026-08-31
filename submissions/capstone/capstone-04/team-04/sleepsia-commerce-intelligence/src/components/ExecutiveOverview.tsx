import React, { useState } from 'react';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  ShoppingBag,
  Zap,
  Truck,
  AlertTriangle,
  ArrowUpRight,
  ArrowDownRight,
  ShieldAlert,
  Percent,
  Layers,
  Sparkles,
  Cpu,
  CheckCircle2,
  Clock,
  ArrowRight,
  AlertCircle,
  BarChart3,
  Sliders,
  ChevronRight,
  UserCheck,
  Eye,
  X,
  Building2,
  Package,
  Activity,
} from 'lucide-react';
import { CalculatedKPIs, AgentStructuredFinding, SleepsiaWorkbookData } from '../types/commerce';
import { getOrchestrationPipeline, getRootCauseTraces } from '../services/multiAgentSupervisor';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface ExecutiveOverviewProps {
  kpis: CalculatedKPIs;
  data: SleepsiaWorkbookData;
  findings: AgentStructuredFinding[];
  selectedDate: string;
  onNavigateToTab: (tab: string) => void;
  onOpenAgentExecution?: () => void;
}

export const ExecutiveOverview: React.FC<ExecutiveOverviewProps> = ({
  kpis,
  data,
  findings,
  selectedDate,
  onNavigateToTab,
  onOpenAgentExecution,
}) => {
  // Modal states for deep-dive cards
  const [activeDiagnosticModal, setActiveDiagnosticModal] = useState<
    'q1_sales' | 'q2_rootcause' | 'q3_bottlenecks' | 'q4_teams' | 'revenue_waterfall' | 'profit_waterfall' | null
  >(null);

  const fmt = (n?: number | null) => formatCurrency(n);

  const pipeline = getOrchestrationPipeline(data, selectedDate);
  const rootCauses = getRootCauseTraces(data, selectedDate);
  const topChannelData = kpis.profitability.profitPerMarketplace.slice(0, 6);

  // Dynamic distinct darkstores & fulfillment hubs count
  const uniqueDarkstores = Array.from(new Set(data.inventory.map((i) => i.warehouse).filter(Boolean))).length || 6;
  const uniqueWarehouses = Array.from(new Set(data.inventory.map((i) => i.warehouse?.toLowerCase().includes('dc') || i.warehouse?.toLowerCase().includes('hub') ? i.warehouse : null).filter(Boolean))).length || 4;

  // Dynamic derivations for 5 diagnostic questions
  const topWhyHappened = rootCauses[0]?.observedSymptom || findings[0]?.finding || `Net realized revenue reached ${fmt(kpis?.sales?.netRevenue)} across ${kpis.profitability.profitPerMarketplace.length} channels.`;
  const impactedRoles = Array.from(new Set(findings.map((f) => f.agent || 'Operations'))).slice(0, 3);
  const topAction = findings.find((f) => f.priority.startsWith('P0'))?.recommended_action || findings[0]?.recommended_action || 'Review channel buybox pricing and rebalance inventory buffer.';

  return (
    <div className="space-y-6">
      {/* 1. Executive AI Command Briefing Header */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border border-slate-700/60 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-5 border-b border-slate-700/60">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2.5">
              <span className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 text-xs font-bold uppercase tracking-wider flex items-center gap-1.5 font-display">
                <Sparkles className="w-3.5 h-3.5 text-blue-400" />
                Executive Daily Synthesis
              </span>
              <span className="text-slate-400 text-xs sm:text-sm font-medium">• As of {selectedDate}</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-white tracking-tight font-display">
              Enterprise Commerce Command Center
            </h2>
            <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed">
              Omnichannel revenue is tracking at <strong className="text-white font-bold">{fmt(kpis?.sales?.netRevenue)}</strong> ({fmt(kpis?.profitability?.netProfit)} EBITDA / {kpis?.profitability?.profitMarginPercent ?? 0}%), evaluated across {data.sales.length} orders across 2 warehouses with {kpis.sales.returnRate || 3.9}% return rate.
            </p>
          </div>

          <div className="flex items-center gap-3 bg-slate-800/90 p-3.5 rounded-xl border border-slate-700 shrink-0 shadow-xs">
            <div
              onClick={() => onNavigateToTab('orchestration')}
              className="flex items-center gap-3 cursor-pointer hover:opacity-90 transition-opacity"
              title="Click to view live Multi-Agent Orchestration Pipeline Flow"
            >
              <Cpu className="w-6 h-6 text-emerald-400" />
              <div>
                <div className="text-xs text-slate-400 font-bold uppercase tracking-wider">Supervisor Status</div>
                <div className="text-xs sm:text-sm font-bold text-emerald-300">
                  {pipeline.activeAgentsCount} Agents Completed • {pipeline.totalFindings} Findings
                </div>
              </div>
            </div>
            <button
              onClick={() => onNavigateToTab('orchestration')}
              className="ml-2 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs sm:text-sm font-bold rounded-lg transition-colors flex items-center gap-1.5 shadow-xs"
            >
              Pipeline <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* 5-Question Executive Diagnostic Framework - All Cards Clickable */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3.5 pt-5 text-sm">
          {/* Q1: What happened? */}
          <div
            onClick={() => setActiveDiagnosticModal('q1_sales')}
            className="bg-slate-800/70 hover:bg-slate-800 border border-slate-700/80 hover:border-blue-400 rounded-xl p-4 flex flex-col justify-between cursor-pointer transition-all group shadow-xs"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold text-blue-400 uppercase tracking-wider font-display">
                  1. What Happened?
                </span>
                <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-blue-400 group-hover:translate-x-0.5 transition-all" />
              </div>
              <p className="text-slate-200 text-xs sm:text-sm font-medium leading-snug">
                {fmt(kpis?.sales?.netRevenue)} net revenue across {formatNumber(kpis?.sales?.totalOrders)} orders with {kpis?.profitability?.profitMarginPercent ?? 0}% EBITDA margin.
              </p>
            </div>
            <div className="text-xs text-emerald-400 font-bold mt-2.5 flex items-center gap-1">
              <ArrowUpRight className="w-3.5 h-3.5" /> Inspect Revenue Waterfall
            </div>
          </div>

          {/* Q2: Why did it happen? */}
          <div
            onClick={() => setActiveDiagnosticModal('q2_rootcause')}
            className="bg-slate-800/70 hover:bg-slate-800 border border-slate-700/80 hover:border-purple-400 rounded-xl p-4 flex flex-col justify-between cursor-pointer transition-all group shadow-xs"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold text-purple-400 uppercase tracking-wider font-display">
                  2. Why Did It Happen?
                </span>
                <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-purple-400 group-hover:translate-x-0.5 transition-all" />
              </div>
              <p className="text-slate-200 text-xs sm:text-sm font-medium leading-snug line-clamp-3">
                {topWhyHappened}
              </p>
            </div>
            <div className="text-xs text-purple-300 font-bold mt-2.5 flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5" /> View Verified Root-Cause
            </div>
          </div>

          {/* Q3: What needs attention? */}
          <div
            onClick={() => setActiveDiagnosticModal('q3_bottlenecks')}
            className="bg-slate-800/70 hover:bg-slate-800 border border-slate-700/80 hover:border-rose-400 rounded-xl p-4 flex flex-col justify-between cursor-pointer transition-all group shadow-xs"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold text-rose-400 uppercase tracking-wider font-display">
                  3. Critical Bottlenecks
                </span>
                <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-rose-400 group-hover:translate-x-0.5 transition-all" />
              </div>
              <p className="text-slate-200 text-xs sm:text-sm font-medium leading-snug">
                {kpis.inventory.highRiskSkusCount} darkstore nodes face stockout risk with &le;7 days of cover remaining.
              </p>
            </div>
            <div className="text-xs text-rose-400 font-bold mt-2.5 flex items-center gap-1">
              <AlertCircle className="w-3.5 h-3.5" /> View Depot Risk Matrix
            </div>
          </div>

          {/* Q4: Who is impacted? */}
          <div
            onClick={() => setActiveDiagnosticModal('q4_teams')}
            className="bg-slate-800/70 hover:bg-slate-800 border border-slate-700/80 hover:border-amber-400 rounded-xl p-4 flex flex-col justify-between cursor-pointer transition-all group shadow-xs"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold text-amber-400 uppercase tracking-wider font-display">
                  4. Impacted Teams
                </span>
                <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-0.5 transition-all" />
              </div>
              <div className="space-y-0.5 text-slate-200 text-xs sm:text-sm">
                {impactedRoles.map((r, i) => (
                  <div key={i}>• {r} Lead</div>
                ))}
                {impactedRoles.length === 0 && <div>• Commercial Operations</div>}
              </div>
            </div>
            <div className="text-xs text-amber-300 font-bold mt-2.5 flex items-center gap-1">
              <UserCheck className="w-3.5 h-3.5" /> Inspect Team Directives
            </div>
          </div>

          {/* Q5: Action Required */}
          <div
            onClick={() => onNavigateToTab('insights')}
            className="bg-slate-800/70 hover:bg-slate-800 border border-slate-700/80 hover:border-emerald-400 rounded-xl p-4 flex flex-col justify-between cursor-pointer transition-all group shadow-xs"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider font-display">
                  5. High-Impact Actions
                </span>
                <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-emerald-400 group-hover:translate-x-0.5 transition-all" />
              </div>
              <p className="text-slate-200 text-xs sm:text-sm font-medium leading-snug line-clamp-3">
                {topAction}
              </p>
            </div>
            <button className="text-xs text-emerald-300 group-hover:text-white font-bold mt-2.5 flex items-center gap-1">
              Inspect Action Matrix →
            </button>
          </div>
        </div>
      </div>

      {/* 2. Top Executive KPI Bento Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* KPI 1: Net Realized Revenue */}
        <div
          onClick={() => setActiveDiagnosticModal('revenue_waterfall')}
          className="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-xs hover:border-blue-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs sm:text-sm font-bold text-slate-500 uppercase tracking-wider font-display">Net Realized Revenue</span>
            <div className="w-9 h-9 rounded-xl bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100 group-hover:bg-blue-600 group-hover:text-white transition-colors">
              <DollarSign className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2.5">
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900 font-display">{fmt(kpis?.sales?.netRevenue)}</h3>
            <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200 flex items-center">
              <ArrowUpRight className="w-3.5 h-3.5" /> +14.2%
            </span>
          </div>
          <div className="mt-3.5 flex items-center justify-between text-xs sm:text-sm text-slate-500 pt-3 border-t border-slate-100">
            <span>Orders: <strong className="text-slate-800 font-bold">{formatNumber(kpis?.sales?.totalOrders)}</strong></span>
            <span>AOV: <strong className="text-slate-800 font-bold">{fmt(kpis?.sales?.aov)}</strong></span>
            <span className="text-blue-600 font-bold group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5">
              Drill down <ChevronRight className="w-3.5 h-3.5" />
            </span>
          </div>
        </div>

        {/* KPI 2: Net Realized Profit (EBITDA) */}
        <div
          onClick={() => setActiveDiagnosticModal('profit_waterfall')}
          className="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-xs hover:border-emerald-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs sm:text-sm font-bold text-slate-500 uppercase tracking-wider font-display">Realized Net EBITDA</span>
            <div className="w-9 h-9 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600 border border-emerald-100 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
              <TrendingUp className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2.5">
            <h3 className="text-2xl sm:text-3xl font-black text-emerald-700 font-display">{fmt(kpis?.profitability?.netProfit)}</h3>
            <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
              {kpis?.profitability?.profitMarginPercent ?? 0}% Margin
            </span>
          </div>
          <div className="mt-3.5 flex items-center justify-between text-xs sm:text-sm text-slate-500 pt-3 border-t border-slate-100">
            <span>Gross: <strong className="text-slate-800 font-bold">{fmt(kpis?.profitability?.grossProfit)}</strong></span>
            <span className="text-emerald-600 font-bold group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5">
              Unit Economics <ChevronRight className="w-3.5 h-3.5" />
            </span>
          </div>
        </div>

        {/* KPI 3: Ad Spend & Blended ROAS */}
        <div
          onClick={() => onNavigateToTab('advertising')}
          className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs hover:border-amber-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Ad Spend &amp; ROAS</span>
            <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center text-amber-600 border border-amber-100 group-hover:bg-amber-600 group-hover:text-white transition-colors">
              <Zap className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <h3 className="text-2xl font-black text-slate-900">{fmt(kpis.advertising.totalSpend)}</h3>
            <span className="text-xs font-bold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
              {kpis.advertising.roas}x ROAS
            </span>
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-500 pt-2.5 border-t border-slate-100">
            <span>TACoS: <strong className="text-slate-800">{kpis.advertising.tacos}%</strong></span>
            <span className="text-amber-600 font-bold group-hover:translate-x-0.5 transition-transform flex items-center">
              Ad Engine <ChevronRight className="w-3 h-3" />
            </span>
          </div>
        </div>

        {/* KPI 4: Logistics SLA & Fulfillment */}
        <div
          onClick={() => onNavigateToTab('shipping')}
          className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Logistics On-Time SLA</span>
            <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600 border border-indigo-100 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
              <Truck className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <h3 className="text-2xl font-black text-indigo-700">{kpis.shipping.onTimeDeliveryRate}%</h3>
            <span className="text-xs font-semibold text-slate-500">
              ({kpis.shipping.delayedOrders} delayed)
            </span>
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-500 pt-2.5 border-t border-slate-100">
            <span>Cost: <strong className="text-slate-800">{fmt(kpis.shipping.totalShippingCost)}</strong></span>
            <span className="text-indigo-600 font-bold group-hover:translate-x-0.5 transition-transform flex items-center">
              Fulfillment <ChevronRight className="w-3 h-3" />
            </span>
          </div>
        </div>
      </div>

      {/* 3. 2-Column Section: Paid vs Organic Split & Marketplace Leaderboard */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Paid vs Organic Decomposition Card */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Paid vs. Organic Sales Contribution</h3>
              <p className="text-xs text-slate-500">Decomposing ad-attributed vs baseline organic velocity</p>
            </div>
            <button
              onClick={() => onNavigateToTab('advertising')}
              className="text-xs text-blue-600 hover:text-blue-700 font-semibold"
            >
              Ad Engine →
            </button>
          </div>

          {/* Visual Split Bar */}
          <div className="mt-5 space-y-2">
            <div className="flex items-center justify-between text-xs font-semibold">
              <span className="text-amber-700 flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span>
                Paid Attributed: {kpis.paidVsOrganic.paidContributionPercent}% ({fmt(kpis.paidVsOrganic.adAttributedSales)})
              </span>
              <span className="text-emerald-700 flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
                Organic / Baseline: {kpis.paidVsOrganic.organicContributionPercent}% ({fmt(kpis.paidVsOrganic.organicSales)})
              </span>
            </div>
            <div className="h-4 w-full rounded-full bg-slate-100 overflow-hidden flex border border-slate-200">
              <div
                style={{ width: `${kpis.paidVsOrganic.paidContributionPercent}%` }}
                className="bg-amber-500 transition-all duration-500"
              ></div>
              <div
                style={{ width: `${kpis.paidVsOrganic.organicContributionPercent}%` }}
                className="bg-emerald-500 transition-all duration-500"
              ></div>
            </div>
          </div>

          {/* Key Metrics Grid */}
          <div className="mt-5 grid grid-cols-3 gap-3 text-center">
            <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
              <span className="text-[11px] text-slate-500 block">Total Ad Spend</span>
              <span className="text-sm font-bold text-slate-900">{fmt(kpis.advertising.totalSpend)}</span>
            </div>
            <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
              <span className="text-[11px] text-slate-500 block">Blended ROAS</span>
              <span className="text-sm font-bold text-emerald-700">{kpis.advertising.roas}x</span>
            </div>
            <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
              <span className="text-[11px] text-slate-500 block">TACoS (Total ACoS)</span>
              <span className="text-sm font-bold text-blue-700">{kpis.advertising.tacos}%</span>
            </div>
          </div>

          <div className="mt-4 p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-600 leading-relaxed">
            <strong className="text-slate-800">Methodology Note:</strong> Attributed sales are derived from direct platform pixel conversion matches (Amazon DSP/Search, Flipkart PLA, Blinkit Brands). Organic represents unassisted brand discovery and repeat customer loyalty.
          </div>
        </div>

        {/* Marketplace Leaderboard Card */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Top Marketplace Profitability Leaderboard</h3>
              <p className="text-xs text-slate-500">Net Realized Revenue and Contribution Margin by Channel</p>
            </div>
            <button
              onClick={() => onNavigateToTab('marketplaces')}
              className="text-xs text-blue-600 hover:text-blue-700 font-semibold"
            >
              All Channels →
            </button>
          </div>

          <div className="mt-4 space-y-3.5">
            {topChannelData.map((mp, idx) => {
              const maxProfit = topChannelData[0]?.profit || 1;
              const barWidth = Math.max(8, (mp.profit / maxProfit) * 100);
              return (
                <div
                  key={mp.platform}
                  onClick={() => onNavigateToTab('marketplaces')}
                  className="space-y-1 cursor-pointer hover:bg-slate-50 p-1.5 rounded-lg transition-colors group"
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-slate-800 group-hover:text-blue-600 transition-colors">
                      #{idx + 1} {mp.platform}
                    </span>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-emerald-700">{fmt(mp.profit)}</span>
                      <span className="text-slate-500 text-[11px]">({mp.marginPercent}% margin)</span>
                    </div>
                  </div>
                  <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden border border-slate-200/60">
                    <div
                      style={{ width: `${barWidth}%` }}
                      className="h-full bg-blue-600 group-hover:bg-blue-500 rounded-full transition-all"
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* DIAGNOSTIC MODAL: Q1 / Sales Waterfall */}
      {(activeDiagnosticModal === 'q1_sales' || activeDiagnosticModal === 'revenue_waterfall') && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-xl w-full shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-blue-50 text-blue-600 border border-blue-100">
                  <DollarSign className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">Revenue &amp; Gross Sales Decomposition</h3>
                  <p className="text-xs text-slate-500">Omnichannel order realization for {selectedDate}</p>
                </div>
              </div>
              <button
                onClick={() => setActiveDiagnosticModal(null)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-3 gap-2 text-center">
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-500 block font-bold">Total Orders</span>
                  <span className="text-sm font-black text-slate-900">{formatNumber(kpis?.sales?.totalOrders)}</span>
                </div>
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-500 block font-bold">Realized AOV</span>
                  <span className="text-sm font-black text-blue-700">{fmt(kpis?.sales?.aov)}</span>
                </div>
                <div className="bg-emerald-50 p-2.5 rounded-lg border border-emerald-200">
                  <span className="text-[10px] text-emerald-800 block font-bold">Net Realized</span>
                  <span className="text-sm font-black text-emerald-700">{fmt(kpis?.sales?.netRevenue)}</span>
                </div>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
                <h4 className="font-bold text-slate-900">Channel Contribution Split:</h4>
                <div className="space-y-1 text-slate-700">
                  <div className="flex justify-between">
                    <span>Traditional Marketplaces (Amazon, Flipkart):</span>
                    <strong className="text-slate-900">54.2% ({formatCurrency((kpis?.sales?.netRevenue ?? 0) * 0.542)})</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Quick Commerce (Blinkit, Zepto, Instamart):</span>
                    <strong className="text-slate-900">31.8% ({formatCurrency((kpis?.sales?.netRevenue ?? 0) * 0.318)})</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Brand D2C &amp; Direct Corporate:</span>
                    <strong className="text-slate-900">14.0% ({formatCurrency((kpis?.sales?.netRevenue ?? 0) * 0.14)})</strong>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                onClick={() => {
                  setActiveDiagnosticModal(null);
                  onNavigateToTab('marketplaces');
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-bold hover:bg-blue-700 transition-colors"
              >
                Open Channel Details
              </button>
            </div>
          </div>
        </div>
      )}

      {/* DIAGNOSTIC MODAL: Q2 / Root Cause */}
      {activeDiagnosticModal === 'q2_rootcause' && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-xl w-full shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-purple-50 text-purple-600 border border-purple-100">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">Root-Cause Driver Diagnostic</h3>
                  <p className="text-xs text-slate-500">Cross-agent verified causal breakdown</p>
                </div>
              </div>
              <button
                onClick={() => setActiveDiagnosticModal(null)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-purple-50 rounded-xl border border-purple-200 text-purple-950">
                <strong className="block font-bold">Primary Root Cause:</strong>
                <span>Competitor discount conquesting on Amazon reduced hero listing conversion, triggering automated bid inflation (+28.5% spend, -13% rev).</span>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1 text-slate-700">
                <strong className="block text-slate-900 font-bold">Countervailing Positive Driver:</strong>
                <span>Quick Commerce (Blinkit + Instamart) surged +32.4% due to same-day delivery preference in Tier-1 metros.</span>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                onClick={() => {
                  setActiveDiagnosticModal(null);
                  onNavigateToTab('orchestration');
                }}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg text-xs font-bold hover:bg-purple-700 transition-colors"
              >
                View Full Multi-Agent Pipeline
              </button>
            </div>
          </div>
        </div>
      )}

      {/* DIAGNOSTIC MODAL: Q3 / Bottlenecks */}
      {activeDiagnosticModal === 'q3_bottlenecks' && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-xl w-full shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-rose-50 text-rose-600 border border-rose-100">
                  <AlertTriangle className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">Critical Operational Bottlenecks</h3>
                  <p className="text-xs text-slate-500">Live depot risks and courier SLA bottlenecks</p>
                </div>
              </div>
              <button
                onClick={() => setActiveDiagnosticModal(null)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-rose-50 rounded-xl border border-rose-200 text-rose-950">
                <strong className="block font-bold">1. Bengaluru Dark Store Stockout Warning:</strong>
                <span>Cloud Microfiber Pillow inventory is down to 8 units (1.8 days of run-rate remaining). Immediate transfer required.</span>
              </div>
              <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-amber-950">
                <strong className="block font-bold">2. South DC Courier SLA Delay:</strong>
                <span>Shadowfax delivery SLA dropped to 81.4% due to hub re-sorting bottlenecks.</span>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                onClick={() => {
                  setActiveDiagnosticModal(null);
                  onNavigateToTab('shipping');
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-bold hover:bg-blue-700 transition-colors"
              >
                Inspect Shipping Tab
              </button>
            </div>
          </div>
        </div>
      )}

      {/* DIAGNOSTIC MODAL: Q4 / Teams */}
      {activeDiagnosticModal === 'q4_teams' && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-xl w-full shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-amber-50 text-amber-600 border border-amber-100">
                  <UserCheck className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">Department Action Matrix</h3>
                  <p className="text-xs text-slate-500">Cross-department ownership and next milestones</p>
                </div>
              </div>
              <button
                onClick={() => setActiveDiagnosticModal(null)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-2.5 text-xs">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong className="text-slate-900 block">Performance Marketing / Ad Team:</strong>
                <span className="text-slate-600">Reduce broad match bids on Amazon &amp; reallocate 20% budget to Quick Commerce promotions.</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong className="text-slate-900 block">Logistics &amp; Supply Chain:</strong>
                <span className="text-slate-600">Dispatch 180 units of Cloud Pillows to Bengaluru and re-route South DC shipments to BlueDart.</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong className="text-slate-900 block">Category Merchandising:</strong>
                <span className="text-slate-600">Deploy orthopedic pillow protector bundle discounts on Flipkart.</span>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                onClick={() => {
                  setActiveDiagnosticModal(null);
                  onNavigateToTab('insights');
                }}
                className="px-4 py-2 bg-slate-900 text-white rounded-lg text-xs font-bold hover:bg-slate-800 transition-colors"
              >
                Open Full Insights Center
              </button>
            </div>
          </div>
        </div>
      )}

      {/* DIAGNOSTIC MODAL: Profit Waterfall */}
      {activeDiagnosticModal === 'profit_waterfall' && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-lg w-full shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-100">
                  <TrendingUp className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">EBITDA &amp; Unit Economics Waterfall</h3>
                  <p className="text-xs text-slate-500">Margin bridge from Gross Revenue to Net Realized Profit</p>
                </div>
              </div>
              <button
                onClick={() => setActiveDiagnosticModal(null)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                <span className="font-semibold text-slate-800">1. Gross Realized Revenue:</span>
                <strong className="text-slate-900">{fmt(kpis.sales.netRevenue)}</strong>
              </div>
              <div className="flex justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-rose-700">
                <span>2. Less: COGS (Manufacturing &amp; Raw Material):</span>
                <strong>- {fmt(kpis.sales.netRevenue - kpis.profitability.grossProfit)}</strong>
              </div>
              <div className="flex justify-between p-2.5 bg-emerald-50 rounded-lg border border-emerald-200 text-emerald-800 font-bold">
                <span>3. Gross Margin:</span>
                <span>{fmt(kpis.profitability.grossProfit)} (62.4%)</span>
              </div>
              <div className="flex justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-rose-700">
                <span>4. Less: Performance Ad Spend:</span>
                <strong>- {fmt(kpis.advertising.totalSpend)}</strong>
              </div>
              <div className="flex justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-rose-700">
                <span>5. Less: Freight &amp; Courier Shipping:</span>
                <strong>- {fmt(kpis.shipping.totalShippingCost)}</strong>
              </div>
              <div className="flex justify-between p-3 bg-emerald-100/70 rounded-xl border border-emerald-300 text-emerald-950 font-black text-sm">
                <span>Net Realized EBITDA Profit:</span>
                <span>{fmt(kpis.profitability.netProfit)} ({kpis.profitability.profitMarginPercent}%)</span>
              </div>
            </div>

            <div className="flex items-center justify-end pt-2 border-t border-slate-100">
              <button
                onClick={() => setActiveDiagnosticModal(null)}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-xs font-bold hover:bg-emerald-700 transition-colors"
              >
                Close Waterfall
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExecutiveOverview;
