import React, { useState } from 'react';
import {
  FileText,
  Download,
  Send,
  Sparkles,
  TrendingUp,
  TrendingDown,
  CheckCircle2,
  AlertTriangle,
  Image as ImageIcon,
  DollarSign,
  Truck,
  ShieldAlert,
} from 'lucide-react';
import { ExecutiveReportData } from '../types/commerce';
import { jsPDF } from 'jspdf';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface DailyReportViewProps {
  report: ExecutiveReportData;
  onSendEmail: () => void;
  selectedDate: string;
}

export const DailyReportView: React.FC<DailyReportViewProps> = ({
  report,
  onSendEmail,
  selectedDate,
}) => {
  const [showImagePreview, setShowImagePreview] = useState(false);
  const fmt = (n?: number | null) => formatCurrency(n);

  const downloadDashboardImage = () => {
    const link = document.createElement('a');
    link.href = `/api/report/dashboard-image?date=${selectedDate}`;
    link.download = `sleepsia_daily_dashboard_${selectedDate}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const generateAndDownloadPdf = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();

    // Brand Header
    doc.setFillColor(15, 23, 42); // Slate 900
    doc.rect(0, 0, pageWidth, 28, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('Sleepsia Commerce Intelligence Daily Report', 14, 18);

    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.text(`Date: ${report?.reportDate || selectedDate} | Generated: ${new Date().toLocaleDateString()}`, pageWidth - 14, 18, { align: 'right' });

    // Executive Summary
    doc.setTextColor(15, 23, 42);
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.text('1. Executive Briefing', 14, 38);

    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    const splitSummary = doc.splitTextToSize(report?.executiveSummary || '', pageWidth - 28);
    doc.text(splitSummary, 14, 46);

    let yPos = 46 + splitSummary.length * 4.5 + 6;

    // Key Financial & Operational KPIs
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.text('2. Daily Commercial Health Metrics', 14, yPos);
    yPos += 8;

    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    doc.text(`• Net Realized Revenue: ${formatCurrency(report?.kpis?.revenue)} (${formatNumber(report?.kpis?.orders)} orders / ${formatNumber(report?.kpis?.units)} units)`, 16, yPos);
    yPos += 5.5;
    doc.text(`• Net Profit: ${formatCurrency(report?.kpis?.profit)} (${report?.kpis?.profitMargin ?? 0}% EBITDA Margin)`, 16, yPos);
    yPos += 5.5;
    doc.text(`• Ad Spend: ${formatCurrency(report?.kpis?.adSpend)} | Blended ROAS: ${report?.kpis?.roas ?? 0}x | Organic Sales: ${report?.kpis?.organicSalesPercent ?? 0}%`, 16, yPos);
    yPos += 5.5;
    doc.text(`• Shipping On-Time SLA: ${report?.kpis?.onTimeDeliveryPercent ?? 0}% | Inventory Risk Count: ${formatNumber(report?.kpis?.inventoryRiskCount)} SKUs`, 16, yPos);
    yPos += 10;

    // Top Wins
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.text('3. Key Daily Wins', 14, yPos);
    yPos += 6;

    doc.setFontSize(8.5);
    doc.setFont('helvetica', 'normal');
    report.topWins.forEach((win) => {
      const splitWin = doc.splitTextToSize(`✓ ${win}`, pageWidth - 28);
      doc.text(splitWin, 16, yPos);
      yPos += splitWin.length * 4 + 2;
    });
    yPos += 4;

    // Critical Risks
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.text('4. Critical Risks & Headwinds', 14, yPos);
    yPos += 6;

    doc.setFontSize(8.5);
    doc.setFont('helvetica', 'normal');
    report.topRisks.forEach((risk) => {
      const splitRisk = doc.splitTextToSize(`⚠ ${risk}`, pageWidth - 28);
      doc.text(splitRisk, 16, yPos);
      yPos += splitRisk.length * 4 + 2;
    });
    yPos += 6;

    // Recommended Actions
    if (yPos > 240) {
      doc.addPage();
      yPos = 20;
    }

    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.text('5. Prioritized Management Action Plan', 14, yPos);
    yPos += 7;

    report.recommendedActions.forEach((act) => {
      doc.setFontSize(8.5);
      doc.setFont('helvetica', 'bold');
      doc.text(`[${act.priority}] [${act.area}] ${act.recommendation}`, 16, yPos);
      yPos += 4.5;
      doc.setFont('helvetica', 'normal');
      const splitImpact = doc.splitTextToSize(`Impact: ${act.expectedImpact}`, pageWidth - 32);
      doc.text(splitImpact, 18, yPos);
      yPos += splitImpact.length * 4 + 3;
    });

    doc.save(`sleepsia_daily_report_${report.reportDate}.pdf`);
  };

  return (
    <div className="space-y-6">
      {/* Top Controls Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-blue-600" />
              <h2 className="text-base font-bold text-slate-900">
                Daily Executive Commerce Briefing ({report.reportDate})
              </h2>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Synthesized by Sleepsia Multi-Agent Supervisor Engine • Formatted for Leadership &amp; Board Distribution
            </p>
          </div>

          <div className="flex items-center flex-wrap gap-2">
            <button
              onClick={() => setShowImagePreview(!showImagePreview)}
              className="bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 text-xs font-semibold px-3 py-2 rounded-lg transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <ImageIcon className="w-3.5 h-3.5 text-blue-600" />
              <span>{showImagePreview ? 'Hide Dashboard Visual' : 'Preview Dashboard Visual'}</span>
            </button>

            <button
              onClick={downloadDashboardImage}
              className="bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 text-xs font-semibold px-3 py-2 rounded-lg transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <Download className="w-3.5 h-3.5 text-emerald-600" />
              <span>Download Image (SVG/PNG)</span>
            </button>

            <button
              onClick={generateAndDownloadPdf}
              className="bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 text-xs font-semibold px-3 py-2 rounded-lg transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <Download className="w-3.5 h-3.5 text-rose-600" />
              <span>Download PDF</span>
            </button>

            <button
              onClick={onSendEmail}
              className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3.5 py-2 rounded-lg transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Send via Gmail Now</span>
            </button>
          </div>
        </div>
      </div>

      {/* Optional Visual Dashboard Image Preview */}
      {showImagePreview && (
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-3">
          <div className="flex items-center justify-between text-xs pb-2 border-b border-slate-100">
            <span className="font-bold text-slate-900 flex items-center gap-1.5">
              <ImageIcon className="w-4 h-4 text-blue-600" />
              High-Resolution Static Dashboard Attachment (`sleepsia_daily_dashboard_{selectedDate}.png`)
            </span>
            <span className="text-slate-500 text-[11px]">Server Rendered at 1200x900px</span>
          </div>
          <div className="w-full rounded-lg overflow-hidden border border-slate-200 bg-slate-50 flex justify-center p-2">
            <img
              src={`/api/report/dashboard-image?date=${selectedDate}`}
              alt="Daily Dashboard"
              className="max-w-full h-auto rounded-lg shadow-md"
            />
          </div>
        </div>
      )}

      {/* Main Document Layout */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 sm:p-8 space-y-8 shadow-xs text-slate-800">
        {/* Executive Summary */}
        <section className="space-y-3">
          <div className="flex items-center gap-2 text-xs font-bold text-blue-600 uppercase tracking-wider">
            <Sparkles className="w-4 h-4" />
            <span>1. Executive Summary</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-700 text-xs sm:text-sm leading-relaxed">
            {report.executiveSummary}
          </div>
        </section>

        {/* 2-Column: Key Wins vs Key Risks */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Top Wins */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3">
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 uppercase tracking-wider pb-2 border-b border-slate-200">
              <CheckCircle2 className="w-4 h-4" />
              <span>Top Operational &amp; Commercial Wins</span>
            </div>
            <ul className="space-y-2.5 text-xs text-slate-700">
              {report.topWins.map((w, idx) => (
                <li key={idx} className="flex items-start gap-2 leading-relaxed">
                  <span className="text-emerald-600 font-bold mt-0.5">✓</span>
                  <span>{w}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Top Risks */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3">
            <div className="flex items-center gap-2 text-xs font-bold text-rose-700 uppercase tracking-wider pb-2 border-b border-slate-200">
              <AlertTriangle className="w-4 h-4" />
              <span>Critical Headwinds &amp; Vulnerabilities</span>
            </div>
            <ul className="space-y-2.5 text-xs text-slate-700">
              {report.topRisks.map((r, idx) => (
                <li key={idx} className="flex items-start gap-2 leading-relaxed">
                  <span className="text-rose-600 font-bold mt-0.5">⚠</span>
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* Major Product Movements */}
        <section className="space-y-3">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
            2. Major Product Catalog Movements
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {/* Growing SKUs */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
              <span className="font-bold text-emerald-700 flex items-center gap-1.5">
                <TrendingUp className="w-4 h-4" /> Top Growing SKUs
              </span>
              <div className="space-y-2 mt-2">
                {report.majorProductChanges.growing.map((p) => (
                  <div key={p.sku} className="flex items-center justify-between text-xs py-1.5 border-b border-slate-200 last:border-0">
                    <div>
                      <span className="font-semibold text-slate-900 block">{p.name}</span>
                      <span className="text-[10px] text-slate-500 font-mono">{p.sku}</span>
                    </div>
                    <div className="text-right">
                      <span className="font-bold text-emerald-700">+{p.growth}%</span>
                      <span className="text-[10px] text-slate-500 block">{fmt(p.revenue)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Declining SKUs */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
              <span className="font-bold text-rose-700 flex items-center gap-1.5">
                <TrendingDown className="w-4 h-4" /> Top Declining SKUs
              </span>
              <div className="space-y-2 mt-2">
                {report.majorProductChanges.declining.map((p) => (
                  <div key={p.sku} className="flex items-center justify-between text-xs py-1.5 border-b border-slate-200 last:border-0">
                    <div>
                      <span className="font-semibold text-slate-900 block">{p.name}</span>
                      <span className="text-[10px] text-slate-500 font-mono">{p.sku}</span>
                    </div>
                    <div className="text-right">
                      <span className="font-bold text-rose-700">{p.decline}%</span>
                      <span className="text-[10px] text-slate-500 block">{fmt(p.revenue)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Prioritized Action Plan Matrix */}
        <section className="space-y-3">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
            3. Prioritized Strategic &amp; Operational Action Plan
          </h3>
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                  <th className="py-2.5 px-4">Priority</th>
                  <th className="py-2.5 px-4">Functional Area</th>
                  <th className="py-2.5 px-4">Prescribed Recommendation</th>
                  <th className="py-2.5 px-4">Expected Financial / SLA Impact</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-800">
                {report.recommendedActions.map((act, i) => (
                  <tr key={i} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded font-black text-[11px] border ${
                        act.priority === 'P0' ? 'bg-rose-50 text-rose-700 border-rose-200' : act.priority === 'P1' ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-blue-50 text-blue-700 border-blue-200'
                      }`}>
                        {act.priority}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-700">{act.area}</td>
                    <td className="py-3 px-4 font-bold text-slate-900">{act.recommendation}</td>
                    <td className="py-3 px-4 text-slate-600 text-[11px]">{act.expectedImpact}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
};
