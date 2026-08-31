import React, { useState, useEffect } from 'react';
import {
  Building2,
  Truck,
  Cpu,
  Zap,
  ArrowRight,
  RefreshCw,
  Play,
  Pause,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  Layers,
  Database,
  Search,
  Sparkles,
  ShieldCheck,
  Activity,
  ChevronRight,
  Info,
  GitBranch,
  Network,
  Package,
  Boxes,
  Clock,
  Radio,
  FileCode2,
  BarChart3,
  Maximize2,
  Minimize2,
  ZoomIn,
  ZoomOut,
  X,
  Mail,
  Store,
  ArrowDownRight,
  ArrowUpRight,
  Eye,
  Sliders,
  CheckCircle
} from 'lucide-react';
import { MOTHER_HUBS, DARK_STORES_INVENTORY, formatINR } from '../data/mockData';

interface NetworkArchitectureFlowProps {
  onOpenStockTransfer?: (sku: string, hub: string, units?: number) => void;
  onOpenEmailModal?: () => void;
  className?: string;
  isInitiallyEnlarged?: boolean;
  isEnlarged?: boolean;
  onToggleEnlarge?: (enlarged: boolean) => void;
}

export const NetworkArchitectureFlow: React.FC<NetworkArchitectureFlowProps> = ({
  onOpenStockTransfer,
  onOpenEmailModal,
  className = '',
  isInitiallyEnlarged = false,
  isEnlarged: controlledIsEnlarged,
  onToggleEnlarge
}) => {
  // Internal or controlled enlarge state
  const [internalIsEnlarged, setInternalIsEnlarged] = useState<boolean>(isInitiallyEnlarged);
  const isEnlarged = controlledIsEnlarged !== undefined ? controlledIsEnlarged : internalIsEnlarged;

  const handleSetEnlarged = (nextVal: boolean) => {
    setInternalIsEnlarged(nextVal);
    if (onToggleEnlarge) {
      onToggleEnlarge(nextVal);
    }
  };

  // View mode: 'simple' (Owner Plain English) vs 'technical' (System Telemetry & Wire Payload)
  const [viewMode, setViewMode] = useState<'simple' | 'technical'>('simple');

  // Zoom scale control for enlarged mode (80% to 130%)
  const [zoomScale, setZoomScale] = useState<number>(100);

  // Simulation step: 1 = Low Stock Alert, 2 = AI Inventory Scan, 3 = Autonomous Dispatch, 4 = Restocked & Protected
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [isPlaying, setIsPlaying] = useState<boolean>(true);
  const [activeCity, setActiveCity] = useState<'Bengaluru' | 'Mumbai' | 'Gurgaon'>('Bengaluru');
  const [selectedPodId, setSelectedPodId] = useState<string>('BLNK-BLR-HSR-04');

  // Handle ESC key to exit fullscreen/enlarged mode
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isEnlarged) {
        handleSetEnlarged(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isEnlarged]);

  // Simulation auto-advancing step timer
  useEffect(() => {
    let timer: any;
    if (isPlaying) {
      timer = setInterval(() => {
        setCurrentStep((prev) => (prev >= 4 ? 1 : prev + 1));
      }, 4500);
    }
    return () => clearInterval(timer);
  }, [isPlaying]);

  // Active store & hub data matching the exact app context
  const selectedPod =
    DARK_STORES_INVENTORY.find((s) => s.storeId === selectedPodId) ||
    DARK_STORES_INVENTORY.find((s) => s.city === activeCity) ||
    DARK_STORES_INVENTORY[0];

  const selectedHub =
    MOTHER_HUBS.find((h) => h.location.toLowerCase().includes(activeCity.toLowerCase())) ||
    MOTHER_HUBS[0];

  // The 4 sequential, cohesive steps for the single "Micro-OOS & Auto Dispatch" flow
  const steps = [
    {
      step: 1,
      shortTitle: '1. Low Stock Alert',
      simpleTitle: 'AI Detects Critical Low Stock at Local Dark Store',
      techTitle: 'Step 1: Edge Telemetry Ingestion & Burn Velocity Alert',
      actor: `${selectedPod.storeName} (${selectedPod.platform})`,
      actorRole: 'Local Quick Commerce Dark Store Pod',
      simpleAction: `Only a few units of this SKU remain on the shelf. Customers are purchasing at a high velocity, leaving minimal stock runway before total stockout.`,
      techAction: `POS telemetry heartbeat triggers alert: Stock level critical, burn rate high, runway below transit SLA safety threshold.`,
      badge: '⚠️ Critical Low Stock (3 units left - 22 min runway)',
      badgeColor: 'text-amber-300 bg-amber-950/80 border-amber-800',
      activeNode: 'pod',
      wirePayload: {
        event: 'POD_MICRO_OOS_ALERT',
        storeId: selectedPod.storeId,
        storeName: selectedPod.storeName,
        platform: selectedPod.platform,
        sku: 'SKU-SC-001',
        productName: 'SkinScience 10% Vitamin C Serum (30ml)',
        currentStock: 3,
        safetyBuffer: 15,
        burnRatePerHour: 8.2,
        runwayMinutes: 22,
        status: 'CRITICAL_OOS_RISK'
      }
    },
    {
      step: 2,
      shortTitle: '2. AI Warehouse Scan',
      simpleTitle: 'Central AI Brain Checks Regional Super Warehouse Reserves',
      techTitle: 'Step 2: Predictive Solver & Regional Warehouse ATP Check',
      actor: 'Agile Solutions Autonomous AI Engine',
      actorRole: 'Central Control Tower Brain',
      simpleAction: `The AI calculates an optimal replenishment batch of 250 units. It instantly queries the ${selectedHub.name}, confirming ${selectedHub.currentStockUnits.toLocaleString()} units available in fresh batch #BAT-2026-088C.`,
      techAction: `Predictive replenishment solver: TargetBatch=250 units. Queries ${selectedHub.id} Available-To-Promise (ATP) reserves: ${selectedHub.currentStockUnits.toLocaleString()} units, FEFO batch BAT-2026-088C (Exp: Apr 2028).`,
      badge: `🔍 Hub Verified (${selectedHub.currentStockUnits.toLocaleString()} units ready)`,
      badgeColor: 'text-blue-300 bg-blue-950/80 border-blue-800',
      activeNode: 'tower',
      wirePayload: {
        event: 'CONTROL_TOWER_ATP_VERIFIED',
        connectedHubId: selectedHub.id,
        hubName: selectedHub.name,
        allocatedUnits: 250,
        availableHubReserves: selectedHub.currentStockUnits,
        batchNumber: 'BAT-2026-088C',
        expiryDate: '2028-04-30',
        decision: 'TRIGGER_EXPRESS_REPLENISHMENT',
        decisionLatencyMs: 142
      }
    },
    {
      step: 3,
      shortTitle: '3. Express Dispatch',
      simpleTitle: 'AI Automatically Generates Transfer Order & Dispatches 250 Units',
      techTitle: 'Step 3: Autonomous WMS Electronic Transfer & Courier Dispatch',
      actor: `${selectedHub.name} (WMS Dispatcher)`,
      actorRole: 'Regional Super Mother Hub Warehouse',
      simpleAction: `Without waiting for manual emails or human approvals, the AI creates electronic transfer order #TRF-BLR-2026-9041 and dispatches 250 units via high-speed courier with a 45-minute delivery SLA.`,
      techAction: `Generates EDI transfer order TRF-BLR-2026-9041. Allocates 250 units from bulk pallets and assigns intra-city express delivery vehicle with 45-min transit corridor.`,
      badge: '🚚 250 Units Dispatched (45-Min Express SLA)',
      badgeColor: 'text-indigo-300 bg-indigo-950/80 border-indigo-800',
      activeNode: 'hub',
      wirePayload: {
        transferOrderId: 'TRF-BLR-2026-9041',
        sourceWarehouse: selectedHub.name,
        destinationStore: selectedPod.storeName,
        sku: 'SKU-SC-001',
        quantity: 250,
        estTransitMinutes: 45,
        dispatchStatus: 'IN_TRANSIT',
        slaTarget: 'ON_TIME'
      }
    },
    {
      step: 4,
      shortTitle: '4. Stock Restored',
      simpleTitle: 'Store Restocked, Customer Delivery Live & ₹48,500 Revenue Saved',
      techTitle: 'Step 4: Pod Inventory Restored, Catalog Rank & Revenue Secured',
      actor: `${selectedPod.storeName} & Digital Shelf`,
      actorRole: 'Restocked Pod & Blinkit Search Catalog',
      simpleAction: `The 250 units arrive at the store. Total stock is restored to 253 units. 10-minute customer delivery stays uninterrupted, #1 search ranking on Blinkit is preserved, and ₹48,500 in lost revenue is saved!`,
      techAction: `POS check-in confirmed: Stock jumps from 3 to 253 units. Quick Commerce 10-min delivery active. Search placement locked at #1, preventing competitor churn.`,
      badge: '✅ Restocked: 253 Units Live (₹48,500 Saved)',
      badgeColor: 'text-emerald-300 bg-emerald-950/80 border-emerald-800',
      activeNode: 'pod',
      wirePayload: {
        status: 'RESTOCK_COMPLETED',
        finalStockUnits: 253,
        deliverySlaMinutes: 10,
        organicSearchRank: '#1 Best Seller',
        revenueLossAvoidedINR: '₹48,500',
        humanLagEliminatedHours: '5.5 hours'
      }
    }
  ];

  const currentStepData = steps[currentStep - 1] || steps[0];

  return (
    <>
      {/* Main Flow Container (embedded or full-screen overlay) */}
      <div
        id="interactive-network-architecture"
        className={
          isEnlarged
            ? 'fixed inset-0 z-50 overflow-y-auto bg-slate-950/95 backdrop-blur-xl p-3 sm:p-5 lg:p-7 flex flex-col justify-start custom-scrollbar animate-in fade-in zoom-in-95 duration-150'
            : `bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden text-slate-100 ${className}`
        }
      >
        <div
          className={
            isEnlarged
              ? 'max-w-[1650px] w-full mx-auto space-y-5 flex flex-col justify-start pb-10'
              : 'w-full space-y-0'
          }
          style={
            isEnlarged && zoomScale !== 100
              ? { transform: `scale(${zoomScale / 100})`, transformOrigin: 'top center' }
              : undefined
          }
        >
          {/* Top Header Bar */}
          <div className="p-4 sm:p-5 bg-gradient-to-r from-slate-950 via-slate-900 to-indigo-950 border-b border-slate-800 flex flex-col lg:flex-row lg:items-center justify-between gap-4 rounded-t-2xl">
            <div>
              <div className="flex items-center space-x-3">
                <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-900/40">
                  <Network className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-sm sm:text-base font-bold tracking-tight text-white uppercase">
                      Micro-OOS & Autonomous Replenishment Dispatch Flow
                    </h3>
                    <span className="px-2.5 py-0.5 bg-blue-500/20 text-blue-300 font-mono text-[10px] font-bold rounded-full border border-blue-400/30">
                      Single Cohesive Flow
                    </span>
                    {isEnlarged && (
                      <span className="hidden sm:inline-block px-2 py-0.5 bg-slate-800 text-slate-400 font-mono text-[10px] rounded border border-slate-700">
                        Press ESC to minimize
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">
                    How Agile Solutions detects low stock at local dark stores and auto-replenishes from the super warehouse in &lt; 45 mins
                  </p>
                </div>
              </div>
            </div>

            {/* View Mode Switcher, Player & Enlarge Controls */}
            <div className="flex flex-wrap items-center gap-2">
              {/* Simple Owner vs Technical View Mode */}
              <div className="bg-slate-950/80 p-1 rounded-xl border border-slate-800 flex items-center space-x-1 text-xs">
                <button
                  onClick={() => setViewMode('simple')}
                  className={`px-3 py-1.5 rounded-lg font-bold flex items-center space-x-1.5 transition-all ${
                    viewMode === 'simple'
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  title="Owner Business Summary View"
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>Owner View</span>
                </button>
                <button
                  onClick={() => setViewMode('technical')}
                  className={`px-3 py-1.5 rounded-lg font-bold flex items-center space-x-1.5 transition-all ${
                    viewMode === 'technical'
                      ? 'bg-indigo-600 text-white shadow-xs'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  title="Technical JSON Telemetry Wire View"
                >
                  <Sliders className="w-3.5 h-3.5" />
                  <span>Technical Wire</span>
                </button>
              </div>

              {/* Simulation Player */}
              <div className="flex items-center space-x-1.5 bg-slate-800/90 p-1.5 rounded-xl border border-slate-700 text-xs">
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className={`px-3 py-1.5 rounded-lg font-bold flex items-center space-x-1.5 transition-all ${
                    isPlaying
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30'
                      : 'bg-blue-600 text-white shadow-xs hover:bg-blue-700'
                  }`}
                >
                  {isPlaying ? (
                    <>
                      <Pause className="w-3.5 h-3.5" />
                      <span>Pause</span>
                    </>
                  ) : (
                    <>
                      <Play className="w-3.5 h-3.5" />
                      <span>Simulate</span>
                    </>
                  )}
                </button>

                <button
                  onClick={() => setCurrentStep((prev) => (prev <= 1 ? 4 : prev - 1))}
                  className="px-2.5 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg font-bold transition-colors"
                  title="Previous Step"
                >
                  &larr;
                </button>

                <div className="px-2 text-xs font-mono text-slate-200 font-bold">
                  {currentStep}/4
                </div>

                <button
                  onClick={() => setCurrentStep((prev) => (prev >= 4 ? 1 : prev + 1))}
                  className="px-2.5 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg font-bold transition-colors"
                  title="Next Step"
                >
                  &rarr;
                </button>

                <button
                  onClick={() => {
                    setCurrentStep(1);
                    setIsPlaying(true);
                  }}
                  className="p-1.5 hover:bg-slate-700 text-slate-400 hover:text-slate-200 rounded-lg transition-colors"
                  title="Reset Flow to Step 1"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Zoom Controls when Enlarged */}
              {isEnlarged && (
                <div className="flex items-center space-x-1 bg-slate-800/90 p-1.5 rounded-xl border border-slate-700">
                  <button
                    onClick={() => setZoomScale((prev) => Math.max(80, prev - 10))}
                    className="p-1.5 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors"
                    title="Zoom Out"
                  >
                    <ZoomOut className="w-3.5 h-3.5" />
                  </button>
                  <span className="text-[10px] font-mono text-slate-300 font-bold px-1.5">
                    {zoomScale}%
                  </span>
                  <button
                    onClick={() => setZoomScale((prev) => Math.min(130, prev + 10))}
                    className="p-1.5 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors"
                    title="Zoom In"
                  >
                    <ZoomIn className="w-3.5 h-3.5" />
                  </button>
                  {zoomScale !== 100 && (
                    <button
                      onClick={() => setZoomScale(100)}
                      className="px-1.5 py-0.5 text-[9px] bg-slate-700 hover:bg-slate-600 text-slate-300 rounded font-mono"
                    >
                      Reset
                    </button>
                  )}
                </div>
              )}

              {/* Enlarge / Minimize Fullscreen Toggle */}
              <button
                onClick={() => handleSetEnlarged(!isEnlarged)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold flex items-center space-x-1.5 transition-all border ${
                  isEnlarged
                    ? 'bg-rose-500/20 text-rose-300 border-rose-500/40 hover:bg-rose-500/30'
                    : 'bg-indigo-600/30 text-indigo-200 border-indigo-500/40 hover:bg-indigo-600/50 hover:text-white shadow-xs'
                }`}
                title={isEnlarged ? 'Minimize Flow (Esc)' : 'Enlarge Architecture Flow to Full View'}
              >
                {isEnlarged ? (
                  <>
                    <Minimize2 className="w-3.5 h-3.5" />
                    <span>Minimize</span>
                  </>
                ) : (
                  <>
                    <Maximize2 className="w-3.5 h-3.5" />
                    <span>Enlarge</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* 4-Step Interactive Progress Bar Ribbon */}
          <div className="px-4 sm:px-6 py-3.5 bg-slate-950/80 border-b border-slate-800">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {steps.map((st) => {
                const isActive = currentStep === st.step;
                const isPassed = currentStep > st.step;

                return (
                  <button
                    key={st.step}
                    onClick={() => setCurrentStep(st.step)}
                    className={`p-2.5 rounded-xl border text-left transition-all relative overflow-hidden ${
                      isActive
                        ? 'bg-blue-950/90 border-blue-500 shadow-md shadow-blue-950 ring-1 ring-blue-400'
                        : isPassed
                        ? 'bg-slate-900/90 border-emerald-900/60 text-slate-300 hover:border-slate-700'
                        : 'bg-slate-900/40 border-slate-800 text-slate-400 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span
                        className={`text-[10px] font-mono font-bold px-1.5 py-0.2 rounded ${
                          isActive
                            ? 'bg-blue-600 text-white'
                            : isPassed
                            ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                            : 'bg-slate-800 text-slate-400'
                        }`}
                      >
                        Step {st.step}
                      </span>
                      {isPassed && <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />}
                      {isActive && <Activity className="w-3.5 h-3.5 text-blue-400 animate-pulse" />}
                    </div>
                    <div
                      className={`text-xs font-bold mt-1.5 truncate ${
                        isActive ? 'text-white' : isPassed ? 'text-slate-200' : 'text-slate-400'
                      }`}
                    >
                      {st.shortTitle}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Main 3-Column Storyline Canvas */}
          <div className="p-4 sm:p-6 space-y-6">
            
            {/* Plain English Active Step Banner & Trigger Action */}
            <div className="p-4 bg-gradient-to-r from-blue-950/50 via-slate-900 to-indigo-950/40 border border-blue-800/40 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-md">
              <div className="flex items-start space-x-3.5">
                <div className="w-8 h-8 rounded-xl bg-blue-600 text-white font-bold flex items-center justify-center text-sm shrink-0 font-mono shadow-xs">
                  {currentStep}
                </div>
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h4 className="text-sm sm:text-base font-bold text-white">
                      {viewMode === 'simple' ? currentStepData.simpleTitle : currentStepData.techTitle}
                    </h4>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed max-w-4xl">
                    {viewMode === 'simple' ? currentStepData.simpleAction : currentStepData.techAction}
                  </p>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-2 shrink-0 self-start md:self-center">
                <span className={`px-3 py-1.5 rounded-xl text-xs font-bold border ${currentStepData.badgeColor}`}>
                  {currentStepData.badge}
                </span>

                {onOpenStockTransfer && (
                  <button
                    onClick={() => onOpenStockTransfer('SKU-SC-001', selectedHub.name, 100)}
                    className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold flex items-center space-x-1.5 transition-colors shadow-xs"
                  >
                    <Truck className="w-3.5 h-3.5" />
                    <span>Dispatch 100 Units</span>
                  </button>
                )}
              </div>
            </div>

            {/* 3 Core Architecture Columns: Store -> AI Control Tower -> Regional Warehouse */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch relative">
              
              {/* COLUMN 1: LOCAL EDGE DARK STORE (4 cols) */}
              <div
                className={`lg:col-span-4 bg-slate-950/90 border rounded-2xl p-4 sm:p-5 flex flex-col justify-between space-y-4 transition-all shadow-md ${
                  currentStep === 1 || currentStep === 4
                    ? 'border-emerald-500/80 ring-2 ring-emerald-500/30'
                    : 'border-slate-800'
                }`}
              >
                {/* Column Header */}
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <div className="flex items-center space-x-2">
                    <div className="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold text-xs">
                      1
                    </div>
                    <div>
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">
                        1. Edge Dark Store (Pod)
                      </h4>
                      <span className="text-[10px] text-emerald-400">
                        10-Min Fast Delivery to Customer
                      </span>
                    </div>
                  </div>
                  <span className="px-2 py-0.5 bg-emerald-950 text-emerald-300 font-mono text-[9px] font-bold rounded border border-emerald-800">
                    Blinkit
                  </span>
                </div>

                {/* Plain English explanation */}
                <p className="text-xs text-slate-300 leading-snug">
                  {viewMode === 'simple'
                    ? 'Local neighborhood pod fulfilling 10-minute grocery and beauty orders in HSR Layout.'
                    : 'Edge node streaming POS telemetry heartbeats, depletion velocity, and inventory buffer threshold alerts.'}
                </p>

                {/* Store Status Card */}
                <div className="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-2.5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-white">{selectedPod.storeName}</span>
                    <span className="text-[10px] font-mono text-slate-400 bg-slate-950 px-1.5 py-0.5 rounded border border-slate-800">
                      Pincode: 560102
                    </span>
                  </div>

                  <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 space-y-1.5 text-xs">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">SKU:</span>
                      <span className="font-mono text-slate-200 font-bold">
                        SKU-SC-001 (Vit C Serum)
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Stock on Shelf:</span>
                      <span
                        className={`font-mono font-bold ${
                          currentStep === 4 ? 'text-emerald-400' : 'text-amber-400'
                        }`}
                      >
                        {currentStep === 4 ? '253 Units (Restocked)' : '3 Units (Critical Low)'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Sales Burn Rate:</span>
                      <span className="font-mono text-red-400 font-semibold">8.2 units / hour</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Stockout Runway:</span>
                      <span className="font-mono text-amber-300 font-bold">
                        {currentStep === 4 ? '31 Days Buffer' : '22 Minutes Left'}
                      </span>
                    </div>
                  </div>

                  {/* Dynamic Alert Banner */}
                  <div
                    className={`p-2 rounded-lg text-xs flex items-center justify-between font-semibold ${
                      currentStep === 4
                        ? 'bg-emerald-950/80 text-emerald-300 border border-emerald-800'
                        : 'bg-amber-950/80 text-amber-300 border border-amber-800 animate-pulse'
                    }`}
                  >
                    <span>
                      {currentStep === 4
                        ? '✅ Full Stock Active (10m Delivery Online)'
                        : '⚠️ Low Stock Alert Sent to AI Brain'}
                    </span>
                  </div>
                </div>

                {/* City Selector */}
                <div className="p-2.5 bg-slate-900/90 border border-slate-800 rounded-xl text-xs flex items-center justify-between">
                  <span className="text-slate-400 text-[11px]">Active Region:</span>
                  <div className="flex space-x-1">
                    {(['Bengaluru', 'Mumbai', 'Gurgaon'] as const).map((city) => (
                      <button
                        key={city}
                        onClick={() => {
                          setActiveCity(city);
                          const podInCity = DARK_STORES_INVENTORY.find((s) => s.city === city);
                          if (podInCity) setSelectedPodId(podInCity.storeId);
                        }}
                        className={`px-2 py-0.5 rounded text-[10px] font-bold transition-colors ${
                          activeCity === city
                            ? 'bg-blue-600 text-white'
                            : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                        }`}
                      >
                        {city}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* COLUMN 2: AGILE SOLUTIONS CENTRAL AI CONTROL TOWER (4 cols) */}
              <div
                className={`lg:col-span-4 bg-gradient-to-b from-slate-950 via-slate-900 to-indigo-950 border rounded-2xl p-4 sm:p-5 flex flex-col justify-between space-y-4 transition-all shadow-lg ${
                  currentStep === 2
                    ? 'border-blue-400 ring-2 ring-blue-500/30'
                    : 'border-indigo-900/60'
                }`}
              >
                {/* Column Header */}
                <div className="flex items-center justify-between pb-3 border-b border-indigo-900/40">
                  <div className="flex items-center space-x-2">
                    <div className="w-7 h-7 rounded-lg bg-blue-500/20 text-blue-400 border border-blue-500/30 flex items-center justify-center font-bold text-xs">
                      2
                    </div>
                    <div>
                      <h4 className="text-xs font-bold uppercase tracking-wider text-white">
                        2. AI Control Tower Brain
                      </h4>
                      <span className="text-[10px] text-blue-300">
                        Autonomous Ingestion & Decision Engine
                      </span>
                    </div>
                  </div>
                  <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 font-mono text-[9px] font-bold rounded border border-blue-400/30">
                    Sub-Second Solver
                  </span>
                </div>

                <p className="text-xs text-slate-300 leading-snug">
                  {viewMode === 'simple'
                    ? 'Continuously monitors all store inventories, calculates replenishment size, and routes orders to the nearest warehouse instantly.'
                    : 'Sub-second optimization broker evaluating Lead Time vs Depletion Runway and executing automated dispatch.'}
                </p>

                {/* 4 AI Decision Steps */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <div
                    className={`p-2.5 rounded-xl border transition-all ${
                      currentStep === 1
                        ? 'bg-indigo-950 border-indigo-400'
                        : 'bg-slate-900/80 border-slate-800'
                    }`}
                  >
                    <div className="flex items-center space-x-1 text-xs font-bold text-indigo-300">
                      <Activity className="w-3.5 h-3.5" />
                      <span>1. Burn Rate Check</span>
                    </div>
                    <p className="text-[10px] text-slate-400 mt-1">
                      Detected 22-min runway vs 45-min transit SLA.
                    </p>
                  </div>

                  <div
                    className={`p-2.5 rounded-xl border transition-all ${
                      currentStep === 2
                        ? 'bg-blue-950 border-blue-400 ring-1 ring-blue-400'
                        : 'bg-slate-900/80 border-slate-800'
                    }`}
                  >
                    <div className="flex items-center space-x-1 text-xs font-bold text-blue-300">
                      <Database className="w-3.5 h-3.5" />
                      <span>2. Hub Stock Match</span>
                    </div>
                    <p className="text-[10px] text-slate-400 mt-1">
                      Verified {selectedHub.currentStockUnits.toLocaleString()} units in {selectedHub.name}.
                    </p>
                  </div>

                  <div
                    className={`p-2.5 rounded-xl border transition-all ${
                      currentStep === 3
                        ? 'bg-emerald-950 border-emerald-400 ring-1 ring-emerald-400'
                        : 'bg-slate-900/80 border-slate-800'
                    }`}
                  >
                    <div className="flex items-center space-x-1 text-xs font-bold text-emerald-300">
                      <Zap className="w-3.5 h-3.5" />
                      <span>3. Auto Dispatch</span>
                    </div>
                    <p className="text-[10px] text-slate-400 mt-1">
                      Generated EDI Order #TRF-BLR-9041 (250 units).
                    </p>
                  </div>

                  <div
                    className={`p-2.5 rounded-xl border transition-all ${
                      currentStep === 4
                        ? 'bg-purple-950 border-purple-400 ring-1 ring-purple-400'
                        : 'bg-slate-900/80 border-slate-800'
                    }`}
                  >
                    <div className="flex items-center space-x-1 text-xs font-bold text-purple-300">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>4. Revenue Saved</span>
                    </div>
                    <p className="text-[10px] text-slate-400 mt-1">
                      Protected ₹48,500 sales & #1 catalog rank.
                    </p>
                  </div>
                </div>

                {/* AI Status */}
                <div className="p-2.5 bg-slate-950/90 border border-indigo-900/50 rounded-xl text-xs flex items-center justify-between">
                  <span className="text-slate-400 text-[11px]">Engine Latency:</span>
                  <span className="text-emerald-400 font-mono font-bold">142ms (Zero Human Lag)</span>
                </div>
              </div>

              {/* COLUMN 3: REGIONAL SUPER MOTHER HUB (4 cols) */}
              <div
                className={`lg:col-span-4 bg-slate-950/90 border rounded-2xl p-4 sm:p-5 flex flex-col justify-between space-y-4 transition-all shadow-md ${
                  currentStep === 3
                    ? 'border-indigo-400 ring-2 ring-indigo-500/30'
                    : 'border-slate-800'
                }`}
              >
                {/* Column Header */}
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <div className="flex items-center space-x-2">
                    <div className="w-7 h-7 rounded-lg bg-purple-500/20 text-purple-400 border border-purple-500/30 flex items-center justify-center font-bold text-xs">
                      3
                    </div>
                    <div>
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">
                        3. Super Mother Hub Warehouse
                      </h4>
                      <span className="text-[10px] text-purple-400">
                        Central Pallet Reserves & Express Dispatch
                      </span>
                    </div>
                  </div>
                  <span className="px-2 py-0.5 bg-purple-950 text-purple-300 font-mono text-[9px] font-bold rounded border border-purple-800">
                    {selectedHub.id}
                  </span>
                </div>

                <p className="text-xs text-slate-300 leading-snug">
                  {viewMode === 'simple'
                    ? 'Your large central warehouse holding bulk inventory ready for rapid dispatch across all neighborhood dark stores.'
                    : 'Regional enterprise warehouse holding bulk batch reserves and operating high-speed intra-city express dispatch.'}
                </p>

                {/* Hub Warehouse Card */}
                <div className="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-2.5">
                  <div className="flex items-center justify-between">
                    <h5 className="text-xs font-bold text-white">{selectedHub.name}</h5>
                    <span className="text-[9px] text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded font-bold border border-emerald-800">
                      WMS Online
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400">{selectedHub.location}</p>

                  <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 space-y-1 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Warehouse Reserves:</span>
                      <span className="font-bold text-emerald-400 font-mono">
                        {selectedHub.currentStockUnits.toLocaleString()} Units Ready
                      </span>
                    </div>
                    <div className="flex justify-between text-[10px] font-mono text-slate-400">
                      <span>Batch: BAT-2026-088C</span>
                      <span className="text-emerald-400">Exp: Apr 2028</span>
                    </div>
                  </div>

                  {/* Live Dispatch Indicator during Step 3 */}
                  <div
                    className={`p-2.5 rounded-xl text-xs flex items-center space-x-2 font-bold transition-all ${
                      currentStep === 3
                        ? 'bg-indigo-950 text-indigo-200 border border-indigo-700 animate-bounce'
                        : 'bg-slate-950 text-slate-400 border border-slate-800'
                    }`}
                  >
                    <Truck className="w-4 h-4 text-indigo-400 shrink-0" />
                    <span>
                      {currentStep === 3
                        ? '🚚 Express Courier: 250 Units En Route (45m SLA)'
                        : '250 Units Allocated for Transfer'}
                    </span>
                  </div>
                </div>

                {/* Hub Transit Coverage */}
                <div className="p-2.5 bg-slate-900/90 border border-slate-800 rounded-xl text-xs flex items-center justify-between">
                  <span className="text-slate-400 text-[11px]">Connected Dark Stores:</span>
                  <span className="font-mono font-bold text-slate-200">
                    {selectedHub.coverageDarkStores} Local Stores in Radius
                  </span>
                </div>
              </div>
            </div>

            {/* Technical Wire Payload Viewer (Shown in Technical View) */}
            {viewMode === 'technical' && (
              <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 sm:p-5 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-300 font-mono flex items-center space-x-2">
                    <FileCode2 className="w-4 h-4 text-emerald-400" />
                    <span>Live Step {currentStep} Telemetry Data Packet (JSON):</span>
                  </span>
                  <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
                    HTTP 200 OK Synced
                  </span>
                </div>
                <pre className="bg-slate-900/90 p-3 rounded-xl border border-slate-800 text-[11px] font-mono text-emerald-300 overflow-x-auto custom-scrollbar max-h-36">
                  {JSON.stringify(currentStepData.wirePayload, null, 2)}
                </pre>
              </div>
            )}

            {/* 4 Core Financial & Operational Pillars for the Owner */}
            <div className="pt-2 border-t border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-bold uppercase tracking-widest text-slate-400 flex items-center space-x-1.5">
                  <Info className="w-3.5 h-3.5 text-blue-400" />
                  <span>Key Business Impact (Why Micro-OOS Auto-Dispatch Protects Your Brand)</span>
                </h4>
                <span className="text-[11px] text-emerald-400 font-mono font-semibold">
                  42% Revenue Loss Avoided
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                <div className="p-3.5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-1">
                  <div className="flex items-center space-x-1.5 text-blue-400 font-bold text-xs">
                    <span>⚡</span>
                    <span>1. Eliminates Human Lag</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Replaces 24-hour delayed spreadsheets with automated sub-second restock orders.
                  </p>
                </div>

                <div className="p-3.5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-1">
                  <div className="flex items-center space-x-1.5 text-emerald-400 font-bold text-xs">
                    <span>💰</span>
                    <span>2. ₹48,500 Revenue Saved</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Preserves daily sales on top bestseller SKUs during evening surge order hours.
                  </p>
                </div>

                <div className="p-3.5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-1">
                  <div className="flex items-center space-x-1.5 text-amber-400 font-bold text-xs">
                    <span>🏆</span>
                    <span>3. Protects #1 Search Rank</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Prevents Blinkit & Zepto algorithms from penalizing and demoting your catalog.
                  </p>
                </div>

                <div className="p-3.5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-1">
                  <div className="flex items-center space-x-1.5 text-purple-400 font-bold text-xs">
                    <span>🚚</span>
                    <span>4. 45-Min Express Corridor</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Restocks local dark stores before the 22-minute runway expires.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </>
  );
};
