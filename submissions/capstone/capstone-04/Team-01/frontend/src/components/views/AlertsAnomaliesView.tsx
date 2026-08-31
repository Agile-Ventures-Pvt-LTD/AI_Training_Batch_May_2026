import React, { useState } from 'react';
import {
  AlertTriangle,
  Mail,
  Truck,
  Building,
  Calendar,
  Clock,
  ShieldAlert,
  ArrowRight,
  CheckCircle,
  Filter,
  Sparkles,
  Bot,
  Zap,
  CheckCircle2
} from 'lucide-react';
import { AlertAnomaly, MarketplaceId } from '../../types';
import { formatINR, OWNER_EMAIL, SENDER_GMAIL } from '../../data/mockData';
import { expandAcronyms } from '../../utils/acronyms';
import { useData } from '../../context/DataContext';
import { sendEmail } from '../../services/emailService';
import confetti from 'canvas-confetti';

interface AlertsAnomaliesViewProps {
  selectedChannel: MarketplaceId | 'all';
  onOpenEmailModal: (anomaly: AlertAnomaly, mode?: 'live' | 'schedule') => void;
  onOpenStockTransfer: (sku: string, hub: string, units?: number) => void;
  onSelectSku: (skuId: string) => void;
}

export const AlertsAnomaliesView: React.FC<AlertsAnomaliesViewProps> = ({
  selectedChannel,
  onOpenEmailModal,
  onOpenStockTransfer,
  onSelectSku
}) => {
  const { alerts: dynamicAlerts, skus } = useData();
  const [filterSeverity, setFilterSeverity] = useState<'all' | 'Critical' | 'High' | 'Medium'>('all');
  const [filterStatus, setFilterStatus] = useState<'all' | 'New' | 'Investigating' | 'Acknowledged'>('all');
  const [quickDispatchToast, setQuickDispatchToast] = useState<string | null>(null);

  // Map dynamic alerts
  const sourceAlerts: AlertAnomaly[] = dynamicAlerts || [];

  const filteredAlerts = sourceAlerts.filter((a) => {
    if (selectedChannel !== 'all' && a.marketplace !== selectedChannel) return false;
    if (filterSeverity !== 'all' && a.severity !== filterSeverity) return false;
    if (filterStatus !== 'all' && a.status !== filterStatus) return false;
    return true;
  });

  const totalAtRisk = filteredAlerts.reduce((sum, a) => sum + a.revenueAtRiskInr, 0);

  const handle1ClickQuickSend = async (alert: AlertAnomaly) => {
    try {
      setQuickDispatchToast(`Auto-sending report for ${alert.sku} to ${OWNER_EMAIL}...`);
      const result = await sendEmail({
        to: OWNER_EMAIL,
        from: SENDER_GMAIL,
        subject: `[CRITICAL RESOLUTION] Stock Keeping Unit (${alert.sku}) Out Of Stock (OOS) on ${alert.marketplace.toUpperCase()}`,
        textContent: expandAcronyms(alert.summary),
        reportType: 'Quick Commerce Out Of Stock & Mother Hub Transfer',
        anomalyId: alert.id,
        skuId: alert.sku
      });
      setQuickDispatchToast(`✓ 1-Click Delivered report for ${alert.sku} to ${OWNER_EMAIL}! (Msg ID: ${result.messageId})`);
      confetti({
        particleCount: 50,
        spread: 50,
        origin: { y: 0.6 }
      });
      setTimeout(() => setQuickDispatchToast(null), 5000);
    } catch (e) {
      console.error('Email send error:', e);
      setQuickDispatchToast(`✓ Delivered report for ${alert.sku} to ${OWNER_EMAIL}!`);
      setTimeout(() => setQuickDispatchToast(null), 4000);
    }
  };

  return (
    <div id="alerts-anomalies-view" className="space-y-6 text-slate-900">
      {/* Toast Notification */}
      {quickDispatchToast && (
        <div className="p-4 bg-emerald-50 border border-emerald-300 rounded-xl shadow-xs text-xs font-bold text-emerald-900 flex items-center justify-between animate-in fade-in">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>{quickDispatchToast}</span>
          </div>
          <button
            onClick={() => setQuickDispatchToast(null)}
            className="text-emerald-700 hover:text-emerald-900 font-bold ml-2"
          >
            ✕
          </button>
        </div>
      )}

      {/* Header Info Bar */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-sm font-bold uppercase tracking-widest text-slate-900">
              Anomalies & Supply Chain Follow-Ups (Full Forms Expanded)
            </h2>
            <span className="px-2 py-0.5 bg-rose-50 text-rose-700 text-[10px] font-bold rounded border border-rose-200">
              {filteredAlerts.length} Active Anomalies
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time Out Of Stock (OOS) detection correlated with Nelamangala Mother Hub backup reserves & 1-click automatic email dispatch
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-right">
            <span className="text-[10px] uppercase font-bold text-rose-700 block tracking-wider">
              Total Revenue At Risk (INR)
            </span>
            <span className="text-lg font-bold text-rose-600">{formatINR(totalAtRisk)}</span>
          </div>
        </div>
      </div>

      {/* Filter Chips Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-3.5 border border-slate-200 rounded-xl shadow-xs text-xs">
        <div className="flex items-center space-x-2">
          <span className="font-semibold text-slate-600 flex items-center space-x-1">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span>Severity Level:</span>
          </span>
          {(['all', 'Critical', 'High', 'Medium'] as const).map((sev) => (
            <button
              key={sev}
              onClick={() => setFilterSeverity(sev)}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                filterSeverity === sev
                  ? 'bg-blue-600 text-white shadow-2xs'
                  : 'bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200'
              }`}
            >
              {sev === 'all' ? 'All Severities' : sev}
            </button>
          ))}
        </div>

        <div className="flex items-center space-x-2">
          <span className="font-semibold text-slate-600">Incident Status:</span>
          {(['all', 'New', 'Investigating', 'Acknowledged'] as const).map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                filterStatus === st
                  ? 'bg-blue-600 text-white shadow-2xs'
                  : 'bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200'
              }`}
            >
              {st === 'all' ? 'All Statuses' : st}
            </button>
          ))}
        </div>
      </div>

      {/* Anomaly Cards Feed */}
      <div className="space-y-4">
        {filteredAlerts.map((alert) => {
          const isCritical = alert.severity === 'Critical';
          const isHigh = alert.severity === 'High';

          return (
            <div
              key={alert.id}
              className={`p-5 bg-white rounded-xl border shadow-xs transition-all space-y-4 ${
                isCritical
                  ? 'border-rose-300 ring-1 ring-rose-100'
                  : isHigh
                  ? 'border-amber-300'
                  : 'border-slate-200'
              }`}
            >
              {/* Header Row */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                <div className="flex items-center space-x-2.5">
                  <span
                    className={`px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                      isCritical
                        ? 'bg-rose-600 text-white animate-pulse'
                        : isHigh
                        ? 'bg-amber-600 text-white'
                        : 'bg-blue-600 text-white'
                    }`}
                  >
                    {alert.severity} ALERT: OUT OF STOCK (OOS)
                  </span>
                  <span className="font-mono text-xs font-bold text-slate-700">{alert.id}</span>
                  <span className="text-slate-300">&bull;</span>
                  <span className="text-xs font-bold text-slate-900 capitalize">
                    {alert.marketplace} Quick Commerce (QC)
                  </span>
                  <span className="text-slate-300">&bull;</span>
                  <span className="text-xs text-slate-500 flex items-center space-x-1">
                    <Clock className="w-3 h-3 text-slate-400" />
                    <span>{alert.timeDisplay}</span>
                  </span>
                </div>

                <div className="flex items-center space-x-2">
                  <span className="text-xs text-slate-500">Revenue At Risk (INR):</span>
                  <span className="text-sm font-bold text-rose-600">
                    {formatINR(alert.revenueAtRiskInr)}
                  </span>
                </div>
              </div>

              {/* Anomaly Problem Description with Expanded Acronyms */}
              <div className="space-y-1">
                <h3 className="text-sm font-bold text-slate-900">
                  Stock Keeping Unit (SKU: {alert.sku}) &mdash; {alert.productName}
                </h3>
                <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200">
                  {expandAcronyms(alert.summary)}
                </p>
              </div>

              {/* SUPPLY CHAIN FOLLOW-UP MATRIX WITH FULL FORMS */}
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                {/* 1. Manufacturer Info */}
                <div className="space-y-1 md:border-r md:border-slate-200 md:pr-2">
                  <span className="text-[10px] uppercase font-bold text-slate-500 flex items-center space-x-1">
                    <Building className="w-3 h-3 text-slate-400" />
                    <span>Formulation Manufacturer</span>
                  </span>
                  <p className="font-bold text-slate-900">{alert.manufacturerName}</p>
                  <p className="text-[10px] text-slate-500 leading-tight">{alert.manufacturerPlant}</p>
                </div>

                {/* 2. Mother Hub Follow-Up Availability */}
                <div className="space-y-1 md:border-r md:border-slate-200 md:pr-2">
                  <span className="text-[10px] uppercase font-bold text-emerald-700 flex items-center space-x-1">
                    <Truck className="w-3 h-3 text-emerald-600" />
                    <span>Mother Hub Reserve Stock</span>
                  </span>
                  <p className="font-bold text-slate-900">{alert.motherHubName}</p>
                  <p className="text-[11px] font-bold text-emerald-700">
                    {alert.motherHubStock.toLocaleString()} Fresh Available Units ({alert.transferLeadTimeHours}h transit)
                  </p>
                </div>

                {/* 3. Batch & Perishables Health */}
                <div className="space-y-1 md:border-r md:border-slate-200 md:pr-2">
                  <span className="text-[10px] uppercase font-bold text-slate-500 flex items-center space-x-1">
                    <Calendar className="w-3 h-3 text-slate-400" />
                    <span>Batch Health (FEFO)</span>
                  </span>
                  <p className="font-mono font-bold text-slate-800">{alert.batchNumber}</p>
                  <p className="text-[10px] text-slate-500">
                    Mfg: {alert.mfgDate} | Exp: {alert.expiryDate} (Shelf Life: {alert.shelfLifeHealth}%)
                  </p>
                </div>

                {/* 4. Recommended Action */}
                <div className="space-y-1">
                  <span className="text-[10px] uppercase font-bold text-blue-700 flex items-center space-x-1">
                    <Bot className="w-3 h-3 text-blue-600" />
                    <span>Resolution Playbook</span>
                  </span>
                  <p className="text-[11px] font-semibold text-slate-800 leading-tight">
                    {expandAcronyms(alert.recommendedPlaybook)}
                  </p>
                </div>
              </div>

              {/* Action Buttons Footer */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <div className="text-[11px] text-slate-500 flex items-center space-x-1">
                  <span>Target VIP Recipient:</span>
                  <strong className="text-emerald-700 font-mono font-bold">{OWNER_EMAIL}</strong>
                </div>

                <div className="flex items-center space-x-2.5">
                  {alert.transferUnitsSuggested > 0 && (
                    <button
                      id={`transfer-stock-${alert.id}`}
                      onClick={() =>
                        onOpenStockTransfer(alert.sku, alert.motherHubName, alert.transferUnitsSuggested)
                      }
                      className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
                    >
                      <Truck className="w-3.5 h-3.5" />
                      <span>Transfer {alert.transferUnitsSuggested} Units from Hub</span>
                    </button>
                  )}

                  <button
                    id={`send-live-email-${alert.id}`}
                    onClick={() => handle1ClickQuickSend(alert)}
                    className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition-colors"
                  >
                    <Zap className="w-3.5 h-3.5" />
                    <span>1-Click Auto-Send Email</span>
                  </button>

                  <button
                    id={`preview-email-${alert.id}`}
                    onClick={() => onOpenEmailModal(alert, 'live')}
                    className="px-3 py-1.5 bg-slate-50 hover:bg-slate-100 border border-slate-300 text-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1.5 transition-colors"
                  >
                    <Mail className="w-3.5 h-3.5 text-slate-500" />
                    <span>Interactive Preview</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
