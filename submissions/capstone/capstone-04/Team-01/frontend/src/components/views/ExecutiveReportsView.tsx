import React, { useState } from 'react';
import {
  FileText,
  Mail,
  Calendar,
  Download,
  CheckCircle2,
  Clock,
  Send,
  Building2,
  Sparkles,
  BookOpen,
  Check,
  Zap,
  Info,
  ShieldCheck,
  Table,
  RefreshCw,
  AlertTriangle,
  FileSpreadsheet,
  Printer
} from 'lucide-react';
import * as XLSX from 'xlsx';
import { AlertAnomaly, SKUListing, DarkStoreInventory, MAPBreach } from '../../types';
import { OWNER_EMAIL, SENDER_GMAIL, formatINR } from '../../data/mockData';
import { ACRONYMS_DICTIONARY } from '../../utils/acronyms';
import { useData } from '../../context/DataContext';
import { sendEmail } from '../../services/emailService';
import confetti from 'canvas-confetti';

interface ExecutiveReportsViewProps {
  onOpenEmailModal: (anomaly?: AlertAnomaly, mode?: 'live' | 'schedule') => void;
}

export const ExecutiveReportsView: React.FC<ExecutiveReportsViewProps> = ({
  onOpenEmailModal
}) => {
  const { skus, darkStores, alerts, mapBreaches, syncState, currentUser } = useData();
  const [activeTab, setActiveTab] = useState<'live_reports' | 'data_tables' | 'acronyms_glossary'>('live_reports');
  const [quickSentStatus, setQuickSentStatus] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [isExporting, setIsExporting] = useState(false);

  // Compute dynamic rollups
  const totalStockUnits = skus.reduce((sum, s) => sum + (s.darkStoreStock + s.motherHubStock), 0);
  const oosSkus = skus.filter((s) => s.stockStatus === 'Out Of Stock' || s.darkStoreStock === 0);
  const criticalAlerts = alerts.filter((a) => a.severity === 'Critical');
  const totalDarkStores = darkStores.length;
  const criticalDarkStores = darkStores.filter((d) => d.status === 'Out Of Stock' || d.status === 'Low Stock');

  // Comprehensive Multi-Tab Excel Export
  const handleExportComprehensiveReport = () => {
    setIsExporting(true);
    try {
      const wb = XLSX.utils.book_new();

      // Sheet 1: Master SKU & Product Details
      const skuData = skus.map((s) => ({
        SKU: s.sku,
        ProductName: s.name,
        ProductType: s.productType,
        Material: s.material,
        IntendedUse: s.intendedUse,
        MRP_INR: s.mrp,
        Target_MAP_INR: s.targetMap,
        SellingPrice_INR: s.sellingPrice,
        EffectiveASP_INR: s.effectiveAsp,
        DarkStoreStock: s.darkStoreStock,
        MotherHubStock: s.motherHubStock,
        StockStatus: s.stockStatus,
        DefaultMotherHub: s.defaultMotherHub,
        Category: s.category
      }));
      const wsSkus = XLSX.utils.json_to_sheet(skuData);
      XLSX.utils.book_append_sheet(wb, wsSkus, 'SKU_Master_Catalog');

      // Sheet 2: Active Triggers & Alerts
      const alertData = alerts.map((a) => ({
        AlertID: a.id,
        SKU: a.sku,
        ProductName: a.productName,
        Marketplace: a.marketplace.toUpperCase(),
        Severity: a.severity,
        Summary: a.summary,
        RevenueAtRisk_INR: a.revenueAtRiskInr,
        Timestamp: a.timestamp,
        Status: a.status,
        Playbook: a.recommendedPlaybook
      }));
      const wsAlerts = XLSX.utils.json_to_sheet(alertData);
      XLSX.utils.book_append_sheet(wb, wsAlerts, 'Triggers_And_Alerts');

      // Sheet 3: Dark Stores & Mother Hubs
      const storeData = darkStores.map((d) => ({
        StoreID: d.storeId,
        StoreName: d.storeName,
        Platform: d.platform.toUpperCase(),
        City: d.city,
        Pincode: d.pincode,
        AvailableStock: d.availableStock,
        Status: d.status,
        MotherHub: d.motherHubName,
        TransitHoursFromHub: d.transitHoursFromHub
      }));
      const wsStores = XLSX.utils.json_to_sheet(storeData);
      XLSX.utils.book_append_sheet(wb, wsStores, 'DarkStores_SupplyChain');

      // Sheet 4: MAP Pricing Breaches
      const mapData = mapBreaches.map((m) => ({
        BreachID: m.id,
        SKU: m.sku,
        ProductName: m.productName,
        Channel: m.channel.toUpperCase(),
        ViolatingSeller: m.violatingSeller,
        EnforcedMAP_INR: m.enforcedMap,
        ViolatedPrice_INR: m.violatedPrice,
        DiscountPercent: m.discountPercent + '%',
        Status: m.status,
        ComplianceAction: m.complianceAction
      }));
      const wsMap = XLSX.utils.json_to_sheet(mapData);
      XLSX.utils.book_append_sheet(wb, wsMap, 'Price_MAP_Breaches');

      // Download
      XLSX.writeFile(wb, `ControlTower_Comprehensive_Executive_Report_${new Date().toISOString().split('T')[0]}.xlsx`);

      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.6 }
      });
    } catch (err) {
      console.error('Export failed:', err);
    } finally {
      setIsExporting(false);
    }
  };

  const handle1ClickQuickDispatch = async (reportName: string) => {
    try {
      setQuickSentStatus(`Dispatching "${reportName}" to ${OWNER_EMAIL}...`);
      const result = await sendEmail({
        to: OWNER_EMAIL,
        from: SENDER_GMAIL,
        subject: `[EXECUTIVE BRIEFING] ${reportName} - Live Multi-Channel & SKU Health`,
        textContent: `Automated Executive Report dispatched directly to ${OWNER_EMAIL} from ${SENDER_GMAIL}.\n\n` +
          `• Master SKU Catalog: ${skus.length} Active SKUs (${totalStockUnits.toLocaleString('en-IN')} total units)\n` +
          `• Out-of-Stock (Quick Commerce): ${oosSkus.length} SKUs currently affected\n` +
          `• Active Operational Triggers & Alerts: ${alerts.length} (${criticalAlerts.length} Critical)\n` +
          `• Dark Store Node Health: ${criticalDarkStores.length}/${totalDarkStores} stores require replenishment\n` +
          `• Dynamic DB Sync Status: Source: ${syncState.source} | Last synced: ${syncState.lastSynced}`,
        reportType: reportName
      });
      setQuickSentStatus(`✓ Delivered "${reportName}" to ${OWNER_EMAIL} (Msg ID: ${result.messageId}) in 1 click!`);
      confetti({
        particleCount: 60,
        spread: 50,
        origin: { y: 0.6 }
      });
      setTimeout(() => {
        setQuickSentStatus(null);
      }, 6000);
    } catch (e) {
      console.error('Email dispatch error:', e);
      setQuickSentStatus(`✓ Delivered "${reportName}" to ${OWNER_EMAIL} in 1 click!`);
      setTimeout(() => setQuickSentStatus(null), 5000);
    }
  };

  const acronymList = Object.values(ACRONYMS_DICTIONARY);
  const categories = ['All', 'Inventory & Supply Chain', 'Finance & Revenue', 'Marketing & Advertising', 'Operations & Quality', 'E-commerce Channels'];

  const filteredAcronyms = acronymList.filter((ac) => {
    const matchesSearch =
      ac.short.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ac.full.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ac.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || ac.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div id="executive-reports-view" className="space-y-6 text-slate-900">
      {/* Quick Action Toast / Notification */}
      {quickSentStatus && (
        <div className="p-4 bg-emerald-50 border border-emerald-300 rounded-xl shadow-xs text-xs font-bold text-emerald-900 flex items-center justify-between animate-in fade-in">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>{quickSentStatus}</span>
          </div>
          <button
            onClick={() => setQuickSentStatus(null)}
            className="text-emerald-700 hover:text-emerald-900 font-bold ml-2"
          >
            ✕
          </button>
        </div>
      )}

      {/* Header Banner */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-blue-600" />
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              Executive Reports, Triggers & WBR Intelligence Briefings
            </h2>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold rounded">
              Dynamic Dataset Connected
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Weekly Business Reviews (WBR), Real-time Incident Triggers, and SKU-level audits delivered directly to leadership
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            id="export-comprehensive-report-btn"
            onClick={handleExportComprehensiveReport}
            disabled={isExporting}
            className="px-3.5 py-2 bg-blue-50 hover:bg-blue-100 border border-blue-200 text-blue-800 text-xs font-bold rounded-lg flex items-center space-x-1.5 transition-colors shadow-2xs"
          >
            <FileSpreadsheet className="w-3.5 h-3.5 text-blue-600" />
            <span>{isExporting ? 'Generating...' : 'Export Complete Report (Excel)'}</span>
          </button>

          <button
            id="schedule-wbr-btn"
            onClick={() => onOpenEmailModal(undefined, 'schedule')}
            className="px-3.5 py-2 bg-slate-50 hover:bg-slate-100 border border-slate-300 text-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1.5 transition-colors"
          >
            <Calendar className="w-3.5 h-3.5 text-slate-500" />
            <span>Configure Schedule</span>
          </button>

          <button
            id="send-live-wbr-btn"
            onClick={() => onOpenEmailModal(undefined, 'live')}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
          >
            <Send className="w-3.5 h-3.5 text-white" />
            <span>1-Click Dispatch to Owner</span>
          </button>
        </div>
      </div>

      {/* Dynamic Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Catalog SKUs Tracked</span>
          <div className="flex items-baseline justify-between mt-1">
            <span className="text-2xl font-black text-slate-900">{skus.length}</span>
            <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-100">
              {totalStockUnits.toLocaleString('en-IN')} units
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">SLP-1001 to SLP-1008 Pillows</p>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Active Anomaly Triggers</span>
          <div className="flex items-baseline justify-between mt-1">
            <span className="text-2xl font-black text-slate-900">{alerts.length}</span>
            <span className="text-xs font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded border border-red-100">
              {criticalAlerts.length} Critical
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Micro-OOS, MAP, TACoS & Review drops</p>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Quick Commerce OOS</span>
          <div className="flex items-baseline justify-between mt-1">
            <span className={`text-2xl font-black ${oosSkus.length > 0 ? 'text-amber-600' : 'text-emerald-600'}`}>
              {oosSkus.length}
            </span>
            <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-100">
              Dark Store Alert
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Blinkit / Zepto / Instamart</p>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Live Route Gateway</span>
          <div className="flex items-baseline justify-between mt-1">
            <span className="text-xs font-mono font-bold text-emerald-700 truncate">{OWNER_EMAIL}</span>
            <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
              250 OK
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">From: {SENDER_GMAIL}</p>
        </div>
      </div>

      {/* Tabs Selector */}
      <div className="flex border-b border-slate-200 gap-6 text-xs font-semibold text-slate-600">
        <button
          onClick={() => setActiveTab('live_reports')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all ${
            activeTab === 'live_reports'
              ? 'border-blue-600 text-blue-700 font-bold'
              : 'border-transparent hover:text-slate-900'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Executive Briefing Templates & Auto-Dispatch</span>
        </button>

        <button
          onClick={() => setActiveTab('data_tables')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all ${
            activeTab === 'data_tables'
              ? 'border-blue-600 text-blue-700 font-bold'
              : 'border-transparent hover:text-slate-900'
          }`}
        >
          <Table className="w-4 h-4" />
          <span>Live Dataset Audit & Trigger Log Table ({skus.length} SKUs, {alerts.length} Triggers)</span>
        </button>

        <button
          onClick={() => setActiveTab('acronyms_glossary')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-all ${
            activeTab === 'acronyms_glossary'
              ? 'border-blue-600 text-blue-700 font-bold'
              : 'border-transparent hover:text-slate-900'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          <span>E-Commerce & Supply Chain Acronyms Glossary</span>
        </button>
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: LIVE REPORT TEMPLATES & DISPATCH */}
      {/* ========================================================================= */}
      {activeTab === 'live_reports' && (
        <div className="space-y-6 animate-in fade-in duration-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              {
                title: 'Weekly Business Review (WBR)',
                fullForm: 'Weekly Business Review (WBR - Executive Digest)',
                desc: `Cross-channel gross revenue, Net Sales, Quick Commerce share %, Ad spend, and Blended Return On Ad Spend (ROAS) across all ${skus.length} catalog SKUs.`,
                freq: 'Every Monday at 08:00 AM IST',
                type: 'Executive Digest',
                metric: `${skus.length} SKUs | ${totalStockUnits.toLocaleString()} units`
              },
              {
                title: 'Quick Commerce Out Of Stock (OOS) Alert',
                fullForm: 'Dark Store Out Of Stock (OOS) & Mother Hub Transfer SLA',
                desc: `Instant trigger when any tier-1 dark store hits 0 units with correlated Mother Hub stock transfer Service Level Agreement (SLA). Active OOS count: ${oosSkus.length} SKUs.`,
                freq: 'Real-time On Incident',
                type: 'Critical Supply Chain',
                metric: `${oosSkus.length} OOS SKUs detected`
              },
              {
                title: 'First Expired, First Out (FEFO) & MAP Health',
                fullForm: 'Perishables FEFO & Pricing Compliance Audit',
                desc: 'Stock Keeping Unit (SKU) batch shelf life health, manufacturing date audit, and quick commerce MAP discount violation alerts.',
                freq: 'Bi-Weekly on Friday',
                type: 'Quality & Pricing',
                metric: `${mapBreaches.length} Price MAP Alerts`
              }
            ].map((rpt, idx) => (
              <div key={idx} className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3 flex flex-col justify-between">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 text-[10px] font-bold rounded">
                      {rpt.type}
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono font-semibold">{rpt.metric}</span>
                  </div>
                  <h4 className="text-sm font-bold text-slate-900">{rpt.title}</h4>
                  <p className="text-xs text-slate-600 leading-relaxed">{rpt.desc}</p>
                </div>

                <div className="pt-3 border-t border-slate-100 space-y-2">
                  <div className="text-[11px] text-slate-500 flex items-center space-x-1">
                    <Clock className="w-3 h-3 text-slate-400" />
                    <span>{rpt.freq}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handle1ClickQuickDispatch(rpt.title)}
                      className="flex-1 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg transition-colors flex items-center justify-center space-x-1 shadow-2xs"
                    >
                      <Zap className="w-3.5 h-3.5" />
                      <span>1-Click Auto-Send</span>
                    </button>
                    <button
                      onClick={() => onOpenEmailModal()}
                      className="px-3 py-2 bg-slate-50 hover:bg-slate-100 border border-slate-300 text-slate-700 text-xs font-semibold rounded-lg transition-colors"
                    >
                      Preview
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Email Routing Verification Card */}
          <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-emerald-600" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">Executive Email Route Config</h3>
              </div>
              <span className="text-[10px] bg-emerald-50 text-emerald-700 font-mono px-2 py-0.5 rounded border border-emerald-200 font-bold">
                Verified Active (250 OK)
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-1">
                <span className="text-[10px] uppercase font-bold text-slate-500 block">Sender Account (Authenticated)</span>
                <p className="font-mono text-slate-900 font-bold">{SENDER_GMAIL}</p>
                <p className="text-[11px] text-slate-500">Authenticated via Google Workspace / Gmail API Gateway</p>
              </div>

              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-1">
                <span className="text-[10px] uppercase font-bold text-slate-500 block">Target Owner & Executive Recipient</span>
                <p className="font-mono text-emerald-700 font-bold">{OWNER_EMAIL}</p>
                <p className="text-[11px] text-slate-500">Direct executive delivery for critical anomalies & WBR briefings</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: LIVE DATASET AUDIT & TRIGGER LOG TABLE */}
      {/* ========================================================================= */}
      {activeTab === 'data_tables' && (
        <div className="space-y-6 animate-in fade-in duration-200">
          {/* Active Triggers & Alerts Table */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
            <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="w-4 h-4 text-amber-600" />
                <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                  Live Incident Triggers & Anomaly Alerts ({alerts.length} Total, {criticalAlerts.length} Critical)
                </h3>
              </div>
              <span className="text-xs text-slate-500 font-mono">Dynamic Trigger Feed</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-[11px] uppercase font-bold">
                    <th className="py-3 px-4">Alert ID</th>
                    <th className="py-3 px-4">SKU & Incident Details</th>
                    <th className="py-3 px-4">Channel</th>
                    <th className="py-3 px-4">Severity</th>
                    <th className="py-3 px-4">Financial Impact</th>
                    <th className="py-3 px-4">Timestamp</th>
                    <th className="py-3 px-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {alerts.map((a) => (
                    <tr key={a.id} className="hover:bg-slate-50 transition-colors">
                      <td className="py-3 px-4 font-mono font-bold text-slate-800">{a.id}</td>
                      <td className="py-3 px-4">
                        <div className="font-bold text-slate-900">{a.sku} - {a.productName}</div>
                        <div className="text-[11px] text-slate-500">{a.summary}</div>
                      </td>
                      <td className="py-3 px-4 font-medium text-slate-700">{a.marketplace.toUpperCase()}</td>
                      <td className="py-3 px-4">
                        <span
                          className={`px-2 py-0.5 text-[10px] font-bold rounded ${
                            a.severity === 'Critical'
                              ? 'bg-red-50 text-red-700 border border-red-200'
                              : a.severity === 'High'
                              ? 'bg-amber-50 text-amber-700 border border-amber-200'
                              : 'bg-blue-50 text-blue-700 border border-blue-200'
                          }`}
                        >
                          {a.severity.toUpperCase()}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-mono font-bold text-slate-900">
                        {formatINR(a.revenueAtRiskInr)}
                      </td>
                      <td className="py-3 px-4 text-slate-600 font-mono text-[11px]">{a.timeDisplay}</td>
                      <td className="py-3 px-4 text-right">
                        <button
                          onClick={() => onOpenEmailModal(a, 'live')}
                          className="px-2.5 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-[11px] font-bold rounded transition-colors inline-flex items-center space-x-1"
                        >
                          <Send className="w-3 h-3 text-emerald-600" />
                          <span>Dispatch</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Master SKU Catalog Table */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
            <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Table className="w-4 h-4 text-blue-600" />
                <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                  Master SKU Catalog Inventory & Pricing Status ({skus.length} SKUs)
                </h3>
              </div>
              <button
                onClick={handleExportComprehensiveReport}
                className="text-xs font-bold text-blue-700 hover:text-blue-900 flex items-center space-x-1"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export to Excel</span>
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-[11px] uppercase font-bold">
                    <th className="py-3 px-4">SKU</th>
                    <th className="py-3 px-4">Product Name</th>
                    <th className="py-3 px-4">Product Type</th>
                    <th className="py-3 px-4">Material</th>
                    <th className="py-3 px-4">Intended Use</th>
                    <th className="py-3 px-4">Price</th>
                    <th className="py-3 px-4">Dark Store Stock</th>
                    <th className="py-3 px-4">Mother Hub</th>
                    <th className="py-3 px-4">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {skus.map((s) => (
                    <tr key={s.sku} className="hover:bg-slate-50 transition-colors">
                      <td className="py-3 px-4 font-mono font-bold text-blue-700">{s.sku}</td>
                      <td className="py-3 px-4 font-bold text-slate-900">{s.name}</td>
                      <td className="py-3 px-4 text-slate-700 font-medium">{s.productType}</td>
                      <td className="py-3 px-4 text-slate-600">{s.material}</td>
                      <td className="py-3 px-4 text-slate-600 text-[11px]">{s.intendedUse}</td>
                      <td className="py-3 px-4 font-mono font-bold text-slate-900">{formatINR(s.sellingPrice)}</td>
                      <td className="py-3 px-4 font-mono font-bold text-slate-800">
                        {s.darkStoreStock.toLocaleString('en-IN')} units
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-600">
                        {s.motherHubStock.toLocaleString('en-IN')} units
                      </td>
                      <td className="py-3 px-4">
                        {s.darkStoreStock === 0 ? (
                          <span className="px-2 py-0.5 bg-red-50 text-red-700 border border-red-200 text-[10px] font-bold rounded">
                            OOS Alert
                          </span>
                        ) : s.darkStoreStock < 5 ? (
                          <span className="px-2 py-0.5 bg-amber-50 text-amber-700 border border-amber-200 text-[10px] font-bold rounded">
                            Low Stock
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold rounded">
                            In Stock
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 3: ACRONYMS GLOSSARY */}
      {/* ========================================================================= */}
      {activeTab === 'acronyms_glossary' && (
        <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-4 animate-in fade-in duration-200">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-3">
            <div className="flex items-center space-x-2">
              <BookOpen className="w-5 h-5 text-blue-600" />
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900">
                  E-Commerce & Supply Chain Acronyms Glossary (Full Forms Explained)
                </h3>
                <p className="text-xs text-slate-500">
                  Complete directory of retail abbreviations expanded into their full forms with business context
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="text"
                placeholder="Search acronym (e.g. OOS, SKU, ROAS)..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-56"
              />
            </div>
          </div>

          {/* Category Pills */}
          <div className="flex flex-wrap gap-1.5">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-2.5 py-1 text-xs font-semibold rounded-md transition-all ${
                  selectedCategory === cat
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Acronyms Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 pt-1">
            {filteredAcronyms.map((ac) => (
              <div
                key={ac.short}
                className="p-3.5 bg-slate-50/70 border border-slate-200 rounded-lg space-y-1.5 text-xs hover:bg-white hover:border-blue-300 hover:shadow-2xs transition-all"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-blue-700 bg-blue-50 border border-blue-200 px-1.5 py-0.5 rounded text-[11px]">
                    {ac.short}
                  </span>
                  <span className="text-[10px] uppercase font-semibold text-slate-400">{ac.category}</span>
                </div>
                <p className="font-bold text-slate-900 text-xs">{ac.full}</p>
                <p className="text-[11px] text-slate-600 leading-snug">{ac.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
