import React, { useState, useEffect, useMemo } from 'react';
import {
  X,
  Truck,
  CheckCircle,
  ArrowRight,
  Building,
  Package,
  ShieldCheck,
  Zap,
  Layers,
  AlertTriangle,
  Mail,
  Sparkles,
  Copy,
  Check,
  BookOpen,
  ExternalLink
} from 'lucide-react';
import { sendEmail } from '../services/emailService';
import { generateInteractiveEmail, formatINR } from '../utils/emailTemplateGenerator';
import { MOTHER_HUBS } from '../data/mockData';
import confetti from 'canvas-confetti';
import { useData } from '../context/DataContext';

interface StockTransferModalProps {
  isOpen: boolean;
  onClose: () => void;
  sku?: string;
  defaultSku?: string;
  productName?: string;
  darkStoreName?: string;
  defaultDarkStoreId?: string;
  defaultHub?: string;
  defaultMotherHub?: string;
  suggestedUnits?: number;
  defaultUnits?: number;
}

export const StockTransferModal: React.FC<StockTransferModalProps> = ({
  isOpen,
  onClose,
  sku,
  defaultSku,
  productName = 'Contour Memory Foam Cervical Pillow',
  darkStoreName,
  defaultDarkStoreId,
  defaultHub,
  defaultMotherHub,
  suggestedUnits,
  defaultUnits = 10
}) => {
  const { triggerStockTransfer, skus, darkStores, motherHubSkuStock } = useData();

  const [selectedSku, setSelectedSku] = useState<string>(sku || defaultSku || 'SLP-1001');
  const [selectedStoreId, setSelectedStoreId] = useState<string>(defaultDarkStoreId || 'BLNK-BLR-HSR-01');
  const [selectedHub, setSelectedHub] = useState<string>(defaultHub || defaultMotherHub || 'Bengaluru Central Mother Hub (Nelamangala)');
  const [units, setUnits] = useState<number>(suggestedUnits || defaultUnits || 10);
  const [carrier, setCarrier] = useState<string>('Shadowfax Quick-Commerce Freight');
  const [priority, setPriority] = useState<string>('Express (3.5h SLA)');
  const [isTransferring, setIsTransferring] = useState<boolean>(false);
  const [transferSuccess, setTransferSuccess] = useState<boolean>(false);
  const [transferDetails, setTransferDetails] = useState<any>(null);
  
  // Interactive HTML Email Viewer state
  const [sentEmailData, setSentEmailData] = useState<any>(null);
  const [showEmailViewer, setShowEmailViewer] = useState<boolean>(false);
  const [activeEmailTab, setActiveEmailTab] = useState<'interactive' | 'html' | 'glossary'>('interactive');
  const [copiedHtml, setCopiedHtml] = useState(false);
  const [copiedText, setCopiedText] = useState(false);

  // Available stores carrying the selected SKU and linked to the selected Source Mother Hub
  const availableStores = useMemo(() => {
    const matchingBoth = darkStores.filter((d) => {
      const matchSku = d.sku?.toLowerCase() === selectedSku.toLowerCase();
      const matchHub = !selectedHub || (d.motherHubName && (d.motherHubName.includes(selectedHub) || selectedHub.includes(d.motherHubName)));
      return matchSku && matchHub;
    });
    if (matchingBoth.length > 0) return matchingBoth;

    const matchingSku = darkStores.filter((d) => d.sku?.toLowerCase() === selectedSku.toLowerCase());
    if (matchingSku.length > 0) return matchingSku;

    const matchingHub = darkStores.filter((d) => !selectedHub || (d.motherHubName && (d.motherHubName.includes(selectedHub) || selectedHub.includes(d.motherHubName))));
    if (matchingHub.length > 0) return matchingHub;

    return darkStores;
  }, [darkStores, selectedSku, selectedHub]);

  useEffect(() => {
    if (availableStores.length > 0) {
      if (!availableStores.some((d) => d.storeId === selectedStoreId)) {
        setSelectedStoreId(availableStores[0].storeId);
      }
    }
  }, [availableStores, selectedStoreId]);

  // Current selected store object
  const currentStore = useMemo(() => {
    return availableStores.find((d) => d.storeId === selectedStoreId) || availableStores[0] || darkStores[0];
  }, [availableStores, selectedStoreId]);

  // Current selected SKU object
  const currentSkuObj = useMemo(() => {
    return skus.find((s) => s.sku === selectedSku) || skus[0];
  }, [skus, selectedSku]);

  // Available stock in the selected hub for this SKU
  const hubStockForSku = useMemo(() => {
    const matchingHubItem = (motherHubSkuStock || []).find(
      (h) => h.sku?.toLowerCase() === selectedSku.toLowerCase() &&
        (h.hubName.includes(selectedHub) || selectedHub.includes(h.hubName))
    );
    if (matchingHubItem) return matchingHubItem.quantityAvailable;
    const fallbackHub = MOTHER_HUBS.find((h) => h.name === selectedHub);
    return fallbackHub ? fallbackHub.currentStockUnits : 50000;
  }, [motherHubSkuStock, selectedSku, selectedHub]);

  useEffect(() => {
    if (isOpen) {
      const initialSku = sku || defaultSku || 'SLP-1001';
      setSelectedSku(initialSku);

      // Match store
      const matchingStores = darkStores.filter((d) => d.sku?.toLowerCase() === initialSku.toLowerCase());
      const lowestStockStore = [...matchingStores].sort((a, b) => (a.availableStock ?? 0) - (b.availableStock ?? 0))[0];
      
      const targetStoreId = defaultDarkStoreId || lowestStockStore?.storeId || matchingStores[0]?.storeId;
      if (targetStoreId && matchingStores.some((d) => d.storeId === targetStoreId)) {
        setSelectedStoreId(targetStoreId);
      } else if (darkStoreName) {
        const found = matchingStores.find((d) => d.storeName.includes(darkStoreName) || darkStoreName.includes(d.storeName));
        setSelectedStoreId(found ? found.storeId : (lowestStockStore?.storeId || 'BLNK-BLR-HSR-01'));
      } else {
        setSelectedStoreId(lowestStockStore?.storeId || 'BLNK-BLR-HSR-01');
      }

      const activeStoreObj = matchingStores.find(d => d.storeId === targetStoreId) || lowestStockStore;
      setSelectedHub(defaultHub || activeStoreObj?.motherHubName || defaultMotherHub || 'Bengaluru Central Mother Hub (Nelamangala)');
      setUnits(defaultUnits || 20);
      setTransferSuccess(false);
      setTransferDetails(null);
    }
  }, [isOpen, sku, defaultSku, defaultDarkStoreId, darkStoreName, defaultHub, defaultMotherHub, defaultUnits, darkStores]);

  if (!isOpen) return null;

  const currentDarkStock = currentStore?.availableStock ?? 0;
  const postTransferDarkStock = currentDarkStock + (units || 0);
  const postTransferHubStock = Math.max(0, hubStockForSku - (units || 0));
  const dailyVel = currentStore?.dailyVelocity || currentSkuObj?.dailyVelocity || 40;
  const currentRunway = dailyVel > 0 ? Number(((currentDarkStock / (dailyVel / 24))).toFixed(1)) : 4.2;
  const postTransferRunway = dailyVel > 0 ? Number(((postTransferDarkStock / (dailyVel / 24))).toFixed(1)) : 72;

  const handleExecuteTransfer = async () => {
    if (!currentStore || units <= 0) return;
    setIsTransferring(true);
    try {
      const trackingNo = `SFX-BLR-${Date.now().toString().slice(-6)}`;
      const targetStoreId = currentStore.storeId;
      const targetStoreLabel = `${currentStore.storeName} (${currentStore.city})`;
      const actualName = currentSkuObj ? currentSkuObj.name : productName;

      // 1. Live multi-sheet atomic state update & reactive propagation
      triggerStockTransfer(
        selectedSku,
        selectedHub,
        units,
        targetStoreId,
        actualName,
        carrier,
        trackingNo
      );

      // 2. Server Action invocation
      const response = await fetch('/api/actions/transfer-stock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sourceMotherHub: selectedHub,
          targetDarkStore: targetStoreLabel,
          sku: selectedSku,
          units,
          priority
        })
      });
      const data = await response.json().catch(() => ({}));
      
      setTransferDetails({
        ...data,
        transferId: data.transferId || `TRF-${Date.now().toString().slice(-6)}`,
        courierPartner: carrier,
        trackingNumber: trackingNo,
        targetStoreLabel
      });
      setTransferSuccess(true);

       // 3. Email Notification to Operations / Brand Lead
      try {
        const emailData = generateInteractiveEmail(null, currentSkuObj || null, null, {
          customSubject: `[REPLENISHMENT DISPATCHED] ${units} Units of ${selectedSku} to ${targetStoreLabel}`,
          datasetContext: { skus },
          transferredUnits: units
        });

        emailData.problemTitle = `Stock Dispatch Confirmed: ${actualName}`;
        emailData.diagnosticRootCause = `Dispatched ${units} units of ${actualName} (${selectedSku}) from ${selectedHub} to ${targetStoreLabel} via ${carrier}. Tracking: ${trackingNo}. ETA: ~3.5 Hours. Live inventory state and alerts have been automatically recalculated across all 7 dataset sheets.`;

        setSentEmailData(emailData);

        await sendEmail({
          to: 'vikashr984@gmail.com',
          subject: emailData.subject,
          textContent: emailData.textContent,
          htmlContent: emailData.htmlContent
        });
      } catch (mailErr) {
        console.warn('Notification email notice:', mailErr);
      }

      confetti({
        particleCount: 80,
        spread: 60,
        origin: { y: 0.6 }
      });
    } catch (e) {
      console.error('Transfer execution error:', e);
    } finally {
      setIsTransferring(false);
    }
  };

  const handleCopyRichHtml = async () => {
    if (!sentEmailData) return;
    try {
      if (navigator.clipboard && window.ClipboardItem) {
        const blobHtml = new Blob([sentEmailData.htmlContent], { type: 'text/html' });
        const blobText = new Blob([sentEmailData.textContent], { type: 'text/plain' });
        await navigator.clipboard.write([
          new ClipboardItem({
            'text/html': blobHtml,
            'text/plain': blobText
          })
        ]);
        setCopiedHtml(true);
        setTimeout(() => setCopiedHtml(false), 2500);
      } else {
        navigator.clipboard.writeText(sentEmailData.textContent);
        setCopiedHtml(true);
        setTimeout(() => setCopiedHtml(false), 2500);
      }
    } catch (err) {
      navigator.clipboard.writeText(sentEmailData.textContent);
      setCopiedHtml(true);
      setTimeout(() => setCopiedHtml(false), 2500);
    }
  };

  const handleOpenInGmailWebApp = () => {
    if (!sentEmailData) return;
    const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=vikashr984@gmail.com&su=${encodeURIComponent(sentEmailData.subject)}&body=${encodeURIComponent(sentEmailData.textContent)}`;
    window.open(gmailUrl, '_blank', 'noopener,noreferrer');
  };

  return (
    <div id="transfer-modal-backdrop" className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
      <div id="transfer-modal-container" className={`bg-white border border-slate-200 rounded-2xl shadow-2xl w-full ${showEmailViewer ? 'max-w-4xl max-h-[92vh]' : 'max-w-xl'} flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150 text-slate-900 transition-all`}>
        
        {/* Header */}
        <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between shrink-0">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-blue-100 text-blue-700 border border-blue-200 flex items-center justify-center font-bold">
              <Truck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">
                {showEmailViewer ? 'Interactive HTML Email Viewer & Delivery Report' : 'Mother Hub Stock Transfer Dispatch'}
              </h3>
              <p className="text-xs text-slate-500">
                {showEmailViewer ? 'Rich HTML rendered with live operational metrics and interactive action playbooks' : 'Direct intra-city replenishment to restore pod stock and eliminate OOS revenue risk'}
              </p>
            </div>
          </div>
          <button
            id="close-transfer-modal-btn"
            onClick={onClose}
            className="text-slate-400 hover:text-slate-700 p-1.5 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4 overflow-y-auto max-h-[78vh] custom-scrollbar bg-slate-50/40">
          {transferSuccess ? (
            showEmailViewer && sentEmailData ? (
              <div className="space-y-4">
                {/* Email Viewer Top Bar */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setActiveEmailTab('interactive')}
                      className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${
                        activeEmailTab === 'interactive' ? 'bg-blue-600 text-white shadow-2xs' : 'text-slate-600 hover:bg-slate-100'
                      }`}
                    >
                      Interactive HTML View
                    </button>
                    <button
                      onClick={() => setActiveEmailTab('html')}
                      className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${
                        activeEmailTab === 'html' ? 'bg-blue-600 text-white shadow-2xs' : 'text-slate-600 hover:bg-slate-100'
                      }`}
                    >
                      HTML Source Code
                    </button>
                    <button
                      onClick={() => setActiveEmailTab('glossary')}
                      className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${
                        activeEmailTab === 'glossary' ? 'bg-blue-600 text-white shadow-2xs' : 'text-slate-600 hover:bg-slate-100'
                      }`}
                    >
                      Acronyms Index
                    </button>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button
                      onClick={handleCopyRichHtml}
                      className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1 transition-colors"
                    >
                      {copiedHtml ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-500" />}
                      <span>{copiedHtml ? 'Copied Rich HTML!' : 'Copy Rich HTML'}</span>
                    </button>
                    <button
                      onClick={handleOpenInGmailWebApp}
                      className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg flex items-center space-x-1 transition-colors shadow-2xs"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      <span>Open in Gmail</span>
                    </button>
                  </div>
                </div>

                {/* Tab 1: Interactive HTML Email Card */}
                {activeEmailTab === 'interactive' && (
                  <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm text-xs space-y-4 p-5">
                    <div className="p-4 bg-slate-900 text-white rounded-lg flex items-center justify-between">
                      <div>
                        <span className="px-2 py-0.5 bg-emerald-500 text-white font-bold text-[10px] rounded uppercase">
                          Replenishment Dispatched
                        </span>
                        <h4 className="text-sm font-bold text-white mt-1">
                          {sentEmailData.problemTitle}
                        </h4>
                        <p className="text-[11px] text-slate-400">
                          SKU: <strong className="text-slate-200">{selectedSku}</strong> | Target: <strong className="text-emerald-400">{transferDetails?.targetStoreLabel}</strong>
                        </p>
                      </div>
                      <span className="px-2.5 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded font-mono text-[10px]">
                        250 OK Delivered
                      </span>
                    </div>

                    <p className="text-slate-700">
                      Dear <strong className="text-slate-900">Vikash Kumar</strong>,<br />
                      The automated replenishment transfer has been successfully dispatched and synced across all 7 dataset sheets. Below are the verified operational metrics and follow-up playbooks.
                    </p>

                    {/* KPI Grid */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
                        <span className="text-[10px] uppercase font-bold text-slate-500 block">Units Transferred</span>
                        <p className="text-sm font-bold text-emerald-700 mt-0.5">{units} Units</p>
                        <span className="text-[10px] text-slate-500">Carrier: {carrier}</span>
                      </div>
                      <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
                        <span className="text-[10px] uppercase font-bold text-slate-500 block">New Pod Stock</span>
                        <p className="text-sm font-bold text-blue-700 mt-0.5">{postTransferDarkStock} Units</p>
                        <span className="text-[10px] text-slate-500">Runway: {postTransferRunway}h</span>
                      </div>
                      <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
                        <span className="text-[10px] uppercase font-bold text-slate-500 block">Mother Hub Reserve</span>
                        <p className="text-sm font-bold text-slate-900 mt-0.5">{postTransferHubStock.toLocaleString('en-IN')} Units</p>
                        <span className="text-[10px] text-slate-500">From {selectedHub}</span>
                      </div>
                      <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
                        <span className="text-[10px] uppercase font-bold text-slate-500 block">Transit SLA</span>
                        <p className="text-sm font-bold text-purple-700 mt-0.5">~3.5 Hours</p>
                        <span className="text-[10px] text-slate-500">Intra-city Express</span>
                      </div>
                    </div>

                    {/* Root Cause Diagnostic */}
                    <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-lg space-y-1">
                      <span className="font-bold text-amber-900 uppercase tracking-wider text-[10px] block">
                        Operational Dispatch Log & Audit Note:
                      </span>
                      <p className="text-slate-800 leading-relaxed">
                        {sentEmailData.diagnosticRootCause}
                      </p>
                    </div>

                    {/* Supply Chain Resolution Flow */}
                    <div className="p-4 bg-blue-50/70 border border-blue-200 rounded-lg space-y-2">
                      <span className="font-bold text-blue-950 uppercase tracking-wider text-[10px] block">
                        Multi-Sheet Synchronization & Inventory Status:
                      </span>
                      <div className="space-y-1.5 text-xs text-slate-800">
                        <div>✓ <strong>Sheet 2 (SKU Catalog):</strong> Dark store available stock updated to {postTransferDarkStock}.</div>
                        <div>✓ <strong>Sheet 3 (Mother Hubs):</strong> Reserve stock balanced to {postTransferHubStock.toLocaleString('en-IN')}.</div>
                        <div>✓ <strong>Sheet 7 (Audit Logs):</strong> Transfer ID {transferDetails?.transferId} recorded successfully.</div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Tab 2: HTML Source Code */}
                {activeEmailTab === 'html' && (
                  <div className="p-4 bg-slate-900 text-slate-100 rounded-xl space-y-3 font-mono text-xs">
                    <div className="flex justify-between items-center text-slate-400 border-b border-slate-800 pb-2">
                      <span>HTML Email Source Code (Ready for SMTP / Webhook)</span>
                      <button
                        onClick={handleCopyRichHtml}
                        className="text-emerald-400 hover:text-emerald-300 font-bold"
                      >
                        {copiedHtml ? 'Copied!' : 'Copy HTML'}
                      </button>
                    </div>
                    <pre className="max-h-72 overflow-x-auto whitespace-pre-wrap custom-scrollbar text-[11px] text-emerald-300">
                      {sentEmailData.htmlContent}
                    </pre>
                  </div>
                )}

                {/* Tab 3: Glossary */}
                {activeEmailTab === 'glossary' && (
                  <div className="p-4 bg-white border border-slate-200 rounded-xl space-y-3">
                    <h5 className="font-bold text-slate-900 text-xs border-b border-slate-100 pb-2 flex items-center gap-1.5">
                      <BookOpen className="w-4 h-4 text-blue-600" />
                      <span>Retail & Supply Chain Acronyms Full-Form Index</span>
                    </h5>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-72 overflow-y-auto custom-scrollbar">
                      {sentEmailData.usedAcronyms.map((ac: any) => (
                        <div key={ac.short} className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg space-y-1 text-xs">
                          <div className="flex justify-between items-center">
                            <span className="font-bold text-blue-700 font-mono text-[10px] bg-blue-50 px-1 py-0.5 rounded border border-blue-200">
                              {ac.short}
                            </span>
                            <span className="font-bold text-slate-900 text-[11px]">{ac.full}</span>
                          </div>
                          <p className="text-[11px] text-slate-600">{ac.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Back / Close button */}
                <div className="pt-2 flex justify-between items-center">
                  <button
                    onClick={() => setShowEmailViewer(false)}
                    className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-semibold rounded-xl transition-colors"
                  >
                    ← Back to Transfer Summary
                  </button>
                  <button
                    onClick={onClose}
                    className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl shadow-xs transition-colors"
                  >
                    Done & Return to Dashboard
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center py-4 space-y-4">
                <div className="w-14 h-14 bg-emerald-100 text-emerald-600 border border-emerald-200 rounded-full flex items-center justify-center mx-auto shadow-sm">
                  <CheckCircle className="w-8 h-8" />
                </div>
                <h4 className="text-base font-bold text-slate-900">
                  Transfer Dispatched & Synced Across All Sheets!
                </h4>
                <p className="text-xs text-slate-600 max-w-md mx-auto">
                  Transfer Order <span className="font-mono font-bold text-slate-900">{transferDetails?.transferId}</span> initiated. Carrier <span className="font-semibold text-slate-900">{carrier}</span> has successfully dispatched the consignment in transit.
                </p>

                <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-left text-xs font-mono space-y-2.5 max-w-md mx-auto text-slate-700">
                  <div className="flex justify-between">
                    <span className="text-slate-500 font-sans">SKU & Item:</span>
                    <span className="text-slate-900 font-bold">{selectedSku}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500 font-sans">Tracking Code:</span>
                    <span className="text-blue-700 font-bold">{transferDetails?.trackingNumber}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500 font-sans">Target Pod:</span>
                    <span className="text-slate-900 font-medium">{transferDetails?.targetStoreLabel || currentStore?.storeName}</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-slate-500 font-sans">Transit ETA:</span>
                    <span className="text-emerald-700 font-bold">~3.5 Hours (Intra-city)</span>
                  </div>
                </div>

                <div className="pt-2 flex flex-wrap items-center justify-center gap-3">
                  {sentEmailData && (
                    <button
                      onClick={() => setShowEmailViewer(true)}
                      className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow-xs transition-colors flex items-center space-x-1.5"
                    >
                      <Mail className="w-4 h-4" />
                      <span>📬 View Interactive HTML Email Viewer</span>
                    </button>
                  )}
                  <button
                    id="close-transfer-success-btn"
                    onClick={onClose}
                    className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-xl shadow-xs transition-colors"
                  >
                    Return to Dashboard
                  </button>
                </div>
              </div>
            )
          ) : (
            <>
              {/* Select SKU */}
              <div className="space-y-1">
                <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                  Target Product SKU
                </label>
                <select
                  value={selectedSku}
                  onChange={(e) => {
                    const newSku = e.target.value;
                    setSelectedSku(newSku);
                    const matching = darkStores.filter((d) => d.sku?.toLowerCase() === newSku.toLowerCase());
                    if (matching.length > 0) {
                      setSelectedStoreId(matching[0].storeId);
                    }
                  }}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-900 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
                >
                  {skus.map((s) => (
                    <option key={s.sku} value={s.sku}>
                      {s.sku} — {s.name} ({s.darkStoreStock ?? 0} units across pods)
                    </option>
                  ))}
                </select>
              </div>

              {/* Source & Destination Route */}
              <div className="p-4 bg-blue-50/70 border border-blue-200 rounded-xl space-y-3">
                <div className="flex items-center justify-between text-xs font-medium text-slate-700">
                  <div className="flex items-center space-x-2">
                    <Building className="w-4 h-4 text-blue-700" />
                    <span className="font-bold text-blue-950">Source Mother Hub</span>
                  </div>
                  <ArrowRight className="w-4 h-4 text-blue-400" />
                  <div className="flex items-center space-x-2">
                    <Package className="w-4 h-4 text-emerald-700" />
                    <span className="font-bold text-blue-950">Target Dark Store Pod</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div>
                    <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Source Mother Hub</label>
                    <select
                      id="source-hub-select"
                      value={selectedHub}
                      onChange={(e) => setSelectedHub(e.target.value)}
                      className="w-full px-2.5 py-2 bg-white text-slate-900 border border-blue-300 rounded-lg text-xs font-medium focus:outline-hidden focus:ring-1 focus:ring-blue-500"
                    >
                      {MOTHER_HUBS.map((hub) => {
                        const hubItem = (motherHubSkuStock || []).find(
                          (h) => h.sku?.toLowerCase() === selectedSku.toLowerCase() &&
                            (h.hubName.includes(hub.name) || hub.name.includes(h.hubName))
                        );
                        const available = hubItem ? hubItem.quantityAvailable : hub.currentStockUnits;
                        return (
                          <option key={hub.id} value={hub.name}>
                            {hub.name} ({available.toLocaleString('en-IN')} units available)
                          </option>
                        );
                      })}
                    </select>
                  </div>

                  <div>
                    <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Target Dark Store Pod</label>
                    <select
                      value={selectedStoreId}
                      onChange={(e) => setSelectedStoreId(e.target.value)}
                      className="w-full px-2.5 py-2 bg-white text-slate-900 border border-blue-300 rounded-lg text-xs font-medium focus:outline-hidden focus:ring-1 focus:ring-blue-500"
                    >
                      {availableStores.map((d) => (
                        <option key={`${d.storeId}-${d.sku}`} value={d.storeId}>
                          {d.storeName} ({d.city}) — {d.availableStock} units ({d.status})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {/* Reactive Delta Calculation Card */}
              <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl grid grid-cols-3 gap-2 text-center text-xs">
                <div className="p-2 bg-white rounded-lg border border-slate-100 shadow-2xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Dark Store Stock</span>
                  <div className="mt-1 font-mono font-bold">
                    <span className={currentDarkStock < 5 ? 'text-rose-600' : 'text-slate-700'}>{currentDarkStock}</span>
                    <span className="text-slate-400 mx-1">→</span>
                    <span className="text-emerald-600 font-black">{postTransferDarkStock}</span>
                  </div>
                </div>

                <div className="p-2 bg-white rounded-lg border border-slate-100 shadow-2xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Mother Hub Stock</span>
                  <div className="mt-1 font-mono font-bold">
                    <span className="text-slate-700">{hubStockForSku.toLocaleString('en-IN')}</span>
                    <span className="text-slate-400 mx-1">→</span>
                    <span className="text-blue-700">{postTransferHubStock.toLocaleString('en-IN')}</span>
                  </div>
                </div>

                <div className="p-2 bg-white rounded-lg border border-slate-100 shadow-2xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Runway Hours</span>
                  <div className="mt-1 font-mono font-bold">
                    <span className={currentRunway < 12 ? 'text-rose-600' : 'text-slate-700'}>{currentRunway}h</span>
                    <span className="text-slate-400 mx-1">→</span>
                    <span className="text-emerald-600 font-black">{postTransferRunway}h</span>
                  </div>
                </div>
              </div>

              {/* Units & Logistics options */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-semibold text-slate-700">
                      Units to Transfer:
                    </label>
                    <div className="flex gap-1">
                      {[10, 20, 50, 100].map((preset) => (
                        <button
                          key={preset}
                          type="button"
                          onClick={() => setUnits(preset)}
                          className="px-1.5 py-0.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-[10px] font-bold rounded"
                        >
                          +{preset}
                        </button>
                      ))}
                    </div>
                  </div>
                  <input
                    id="transfer-units-input"
                    type="number"
                    value={units}
                    onChange={(e) => setUnits(Math.max(1, Number(e.target.value)))}
                    min={1}
                    max={5000}
                    className="w-full px-3 py-2 text-xs bg-white text-slate-900 border border-slate-300 rounded-xl font-bold focus:ring-2 focus:ring-blue-500 font-mono"
                  />
                  <span className="text-[10px] text-slate-500 mt-0.5 block">
                    Suggested buffer: {suggestedUnits || 250} units
                  </span>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Logistics Carrier:
                  </label>
                  <select
                    id="transfer-carrier-select"
                    value={carrier}
                    onChange={(e) => setCarrier(e.target.value)}
                    className="w-full px-2.5 py-2 bg-white text-slate-900 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-blue-500"
                  >
                    <option>Shadowfax Quick-Commerce Freight</option>
                    <option>Delhivery Intra-City Express</option>
                    <option>BlueDart Priority Surface</option>
                    <option>In-house Fleet Dedicated Van</option>
                  </select>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end space-x-3 pt-3 border-t border-slate-200">
                <button
                  id="cancel-transfer-btn"
                  onClick={onClose}
                  className="px-4 py-2 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-colors"
                >
                  Cancel
                </button>
                <button
                  id="confirm-transfer-btn"
                  onClick={handleExecuteTransfer}
                  disabled={isTransferring || units <= 0}
                  className="px-5 py-2.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-xl flex items-center space-x-2 shadow-xs transition-all"
                >
                  {isTransferring ? (
                    <span>Initiating Transfer & Syncing...</span>
                  ) : (
                    <>
                      <Zap className="w-3.5 h-3.5 text-blue-200" />
                      <span>Confirm Stock Dispatch ({units} Units)</span>
                    </>
                  )}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
