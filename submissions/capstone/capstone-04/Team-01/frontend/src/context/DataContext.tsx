import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {
  SKUListing,
  DarkStoreInventory,
  MotherHub,
  MotherHubSkuStock,
  ManufacturerSupplyInfo,
  MAPBreach,
  ChannelPricingItem,
  AlertAnomaly,
  AutonomousAction,
  UserPersona,
  UserRole,
  DatasetSyncState,
  ViewMode,
  StockTransferLog
} from '../types';
import {
  exportDatasetToExcelWorkbook,
  exportTransferLogsToExcel as exportTransferLogsToExcelService,
  exportAlertsLogToExcel as exportAlertsLogToExcelService,
  parseUploadedSpreadsheet,
  fetchPublishedGoogleSheet,
  fetchPublishedGoogleSheetCsv,
  createDynamicSkuFromRow,
  buildChannelPricingFromCatalog,
  SLEEP_SKU_CATALOG,
  SLEEP_DARK_STORES,
  MOTHER_HUB_SKU_DATA,
  MANUFACTURER_SUPPLY_DATA,
  SLEEP_CHANNEL_PRICING,
  SLEEP_MAP_BREACHES,
  SLEEP_ALERTS
} from '../services/datasetService';
import { MOTHER_HUBS } from '../data/mockData';
import { sendEmail } from '../services/emailService';
import { generateInteractiveEmail } from '../utils/emailTemplateGenerator';

// Dynamic revenue at risk calculation helper across dark store pods
export const computeRevenueAtRisk = (darkStoreStock: number, dailyVelocity: number, sellingPrice: number, skuStores?: DarkStoreInventory[]): number => {
  if (skuStores && skuStores.length > 0) {
    let totalRisk = 0;
    for (const store of skuStores) {
      const stock = store.availableStock ?? 15;
      if (stock < 10) {
        const deficit = Math.max(1, 10 - stock);
        const storeVelocity = (dailyVelocity || 50) / Math.max(1, skuStores.length);
        totalRisk += Math.round(sellingPrice * storeVelocity * (deficit / 3));
      }
    }
    return totalRisk;
  }
  if (darkStoreStock >= 10) return 0;
  const stockDeficit = Math.max(1, 10 - darkStoreStock);
  return Math.round(sellingPrice * (dailyVelocity || 50) * (stockDeficit / 3));
};

// Pure logic connection helper: Dark Store Stock is always dynamically derived as the exact sum of available stock across all dark store pods for each SKU
export const computeSkusWithDarkStores = (skuList: SKUListing[], storeList: DarkStoreInventory[]): SKUListing[] => {
  return skuList.map(s => {
    const skuStores = storeList.filter(d => d.sku?.toLowerCase() === s.sku.toLowerCase());
    const storeSum = skuStores.reduce((sum, d) => sum + (d.availableStock ?? 0), 0);
    const darkStoreStock = storeSum;
    const hasLowStores = skuStores.some(d => (d.availableStock ?? 15) < 10);
    const stockStatus = hasLowStores || darkStoreStock <= 10 ? 'Low Stock' : 'Active';
    return {
      ...s,
      darkStoreStock,
      stockStatus,
      revenueAtRisk: computeRevenueAtRisk(darkStoreStock, s.dailyVelocity || 50, s.sellingPrice, skuStores)
    };
  });
};

export const USER_PERSONAS: UserPersona[] = [
  {
    id: 'user-owner',
    name: 'Agile Owner',
    role: 'Owner',
    email: 'owner@agileventures.net',
    avatar: 'AO',
    allowedViews: [
      'command-center',
      'digital-shelf',
      'supply-chain',
      'autonomous-ai',
      'dataset-sync',
      'executive-tower',
      'sales-intelligence',
      'price-map-intel',
      'dark-stores-supply-chain',
      'alerts-anomalies',
      'autonomous-actions',
      'settings-rbac'
    ],
    canEditData: true,
    canTriggerTransfers: true,
    canSendEmails: true,
    canManageUsers: true,
    canEditPricing: true
  },
  {
    id: 'user-analyst',
    name: 'Rohan Mehta (E-commerce Analyst)',
    role: 'Analyst',
    email: 'rohan.m@agileventures.net',
    avatar: '📊',
    allowedViews: [
      'command-center'
    ],
    canEditData: false,
    canTriggerTransfers: false,
    canSendEmails: false,
    canManageUsers: false,
    canEditPricing: false
  }
];

interface DataContextType {
  skus: SKUListing[];
  darkStores: DarkStoreInventory[];
  motherHubs: MotherHub[];
  motherHubSkuStock: MotherHubSkuStock[];
  manufacturerSupply: ManufacturerSupplyInfo[];
  channelPricing: ChannelPricingItem[];
  mapBreaches: MAPBreach[];
  alerts: AlertAnomaly[];
  autonomousActions: AutonomousAction[];
  syncState: DatasetSyncState;
  currentUser: UserPersona;
  setCurrentUser: (user: UserPersona) => void;
  updateSKU: (skuCode: string, updates: Partial<SKUListing>) => void;
  updateDarkStore: (storeId: string, updates: Partial<DarkStoreInventory>, skuCode?: string) => void;
  updateMotherHubSkuStock: (id: string, updates: Partial<MotherHubSkuStock>) => void;
  updateManufacturerSupply: (id: string, updates: Partial<ManufacturerSupplyInfo>) => void;
  pushDarkStoreToGoogleSheet: (store: DarkStoreInventory) => Promise<{ success: boolean; message: string }>;
  pushMotherHubToGoogleSheet: (hub: MotherHubSkuStock) => Promise<{ success: boolean; message: string }>;
  pushManufacturerSupplyToGoogleSheet: (mfg: ManufacturerSupplyInfo) => Promise<{ success: boolean; message: string }>;
  updateAlert: (alertId: string, updates: Partial<AlertAnomaly>) => void;
  pushAlertToGoogleSheet: (alert: AlertAnomaly) => Promise<{ success: boolean; message: string }>;
  updateChannelPricing: (id: string, updates: Partial<ChannelPricingItem>) => void;
  pushChannelPricingToGoogleSheet: (item: ChannelPricingItem) => Promise<{ success: boolean; message: string }>;
  exportToExcel: () => void;
  exportTransferLogsToExcel: () => void;
  exportAlertsLogToExcel: () => void;
  importFromExcel: (file: File) => Promise<{ success: boolean; message: string }>;
  syncFromGoogleSheet: (url: string) => Promise<{ success: boolean; message: string }>;
  pushFullDatasetToGoogleSheet: () => Promise<{ success: boolean; message: string }>;
  googleSheetWebhookUrl: string;
  setGoogleSheetWebhookUrl: (url: string) => void;
  pushToGoogleSheet: (skuCode: string, customUpdates?: Partial<SKUListing>) => Promise<{ success: boolean; message: string }>;
  resetToDefaults: () => void;
  triggerStockTransfer: (sku: string, hub: string, units: number, storeId?: string, productName?: string, carrier?: string, trackingNumber?: string) => void;
  transferLogs: StockTransferLog[];
  approveAction: (actionId: string) => Promise<void>;
  rejectAction: (actionId: string) => void;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

function buildActionsFromAlerts(activeAlerts: AlertAnomaly[]): AutonomousAction[] {
  return activeAlerts.map((a, idx) => ({
    id: `ACT-${a.id}`,
    actionCode: `PLAYBOOK-${a.sku}-${idx + 1}`,
    title: a.recommendedPlaybook,
    description: a.summary,
    channel: a.marketplace,
    marketplace: a.marketplace,
    category: a.severity === 'Critical' ? 'Quick Commerce Supply Chain' : 'Marketplace MAP Enforcement',
    agentName: a.severity === 'Critical' ? 'Quick Commerce Supply Agent' : 'Pricing & MAP Sentinel',
    targetSku: a.sku,
    sku: a.sku,
    status: 'Pending Approval',
    confidencePercent: 98,
    confidenceScore: 98,
    projectedRoiInr: a.revenueAtRiskInr,
    estimatedValueRecoveredInr: a.revenueAtRiskInr,
    approvalRequired: true,
    safetyGuardrail: `Verified against Mother Hub inventory (${a.motherHubStock?.toLocaleString('en-IN') || '1,84,500'} units). Route pre-approved.`,
    guardrailsCheck: 'Passed (Guardrail verified)',
    playbookType: a.severity === 'Critical' ? 'Stock Transfer Dispatch' : 'MAP Enforcement Notice',
    triggerAlertId: a.id,
    transferDetails: a.transferUnitsSuggested > 0 ? {
      fromMotherHub: a.motherHubName || 'Bengaluru Central Mother Hub (Nelamangala)',
      targetDarkStore: `${a.marketplace.toUpperCase()} Dark Store Pod`,
      units: a.transferUnitsSuggested
    } : undefined
  }));
}

function buildAllAutonomousActions(activeAlerts: AlertAnomaly[], skusList: SKUListing[]): AutonomousAction[] {
  // Filter activeAlerts to exclude static stock alerts, keeping only policy / MAP breach alerts
  const nonStockAlerts = activeAlerts.filter(a => !a.id.includes('oos') && !a.summary.toLowerCase().includes('stock dropped'));
  const alertActions = buildActionsFromAlerts(nonStockAlerts);
  
  // Dynamically generate actions for any SKU with low dark store stock (<= 50) using real dataset values
  const lowStockSKUs = skusList.filter(s => (s.darkStoreStock ?? 50) <= 50);
  const skuActions: AutonomousAction[] = lowStockSKUs.map((sku) => {
    const unitsToTransfer = 250;
    return {
      id: `ACT-SKU-${sku.sku}`,
      actionCode: `PLAYBOOK-STOCK-${sku.sku}`,
      title: `Auto-Replenishment Transfer Order for ${sku.name} (${sku.sku})`,
      description: `Dark store stock dropped to ${sku.darkStoreStock} units (Below 50-unit safety threshold). Recommended dispatch of ${unitsToTransfer} units from ${sku.defaultMotherHub || 'Bengaluru Central Mother Hub (Nelamangala)'}.`,
      channel: 'blinkit' as const,
      marketplace: 'Blinkit',
      category: 'Quick Commerce Supply Chain',
      agentName: 'Quick Commerce Supply Agent',
      targetSku: sku.sku,
      sku: sku.sku,
      status: 'Pending Approval',
      confidencePercent: 96,
      confidenceScore: 96,
      projectedRoiInr: Math.round(sku.dailyVelocity * sku.sellingPrice * 14),
      estimatedValueRecoveredInr: Math.round(sku.dailyVelocity * sku.sellingPrice * 14),
      approvalRequired: true,
      safetyGuardrail: `Verified against Mother Hub inventory (${sku.motherHubStock?.toLocaleString('en-IN') || '1,84,500'} units). SLA 3.5h.`,
      guardrailsCheck: 'Passed (Guardrail verified)',
      playbookType: 'Stock Transfer Dispatch',
      triggerAlertId: `alt-sku-${sku.sku}`,
      transferDetails: {
        fromMotherHub: sku.defaultMotherHub || 'Bengaluru Central Mother Hub (Nelamangala)',
        targetDarkStore: 'Blinkit HSR Layout Hub 04 (Bengaluru)',
        units: unitsToTransfer
      }
    };
  });

  const combinedMap = new Map<string, AutonomousAction>();
  [...skuActions, ...alertActions].forEach(act => {
    if (!combinedMap.has(act.sku || act.id)) {
      combinedMap.set(act.sku || act.id, act);
    }
  });
  return Array.from(combinedMap.values());
}

export const DataProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // Load initial from localStorage if available, or fallback to real baseline dataset
  const [darkStores, setDarkStores] = useState<DarkStoreInventory[]>(() => {
    const saved = localStorage.getItem('agile_sleep_dark_stores');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length >= 20) return parsed;
      } catch (e) {}
    }
    return SLEEP_DARK_STORES;
  });

  const [motherHubs, setMotherHubs] = useState<MotherHub[]>(MOTHER_HUBS);

  const [skus, setSkus] = useState<SKUListing[]>(() => {
    const saved = localStorage.getItem('agile_sleep_skus');
    let loaded: SKUListing[] = SLEEP_SKU_CATALOG;
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length >= 8) loaded = parsed;
      } catch (e) {}
    }
    const currentStores = (() => {
      const savedStores = localStorage.getItem('agile_sleep_dark_stores');
      if (savedStores) {
        try {
          const parsed = JSON.parse(savedStores);
          if (Array.isArray(parsed) && parsed.length >= 20) return parsed;
        } catch (e) {}
      }
      return SLEEP_DARK_STORES;
    })();

    return computeSkusWithDarkStores(loaded, currentStores);
  });

  const [motherHubSkuStock, setMotherHubSkuStock] = useState<MotherHubSkuStock[]>(() => {
    const saved = localStorage.getItem('agile_sleep_mother_hub_skus');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length >= 10) return parsed;
      } catch (e) {}
    }
    return MOTHER_HUB_SKU_DATA;
  });

  const [manufacturerSupply, setManufacturerSupply] = useState<ManufacturerSupplyInfo[]>(() => {
    const saved = localStorage.getItem('agile_sleep_manufacturer_supply');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      } catch (e) {}
    }
    return MANUFACTURER_SUPPLY_DATA;
  });

  const [channelPricing, setChannelPricing] = useState<ChannelPricingItem[]>(() => {
    const saved = localStorage.getItem('agile_sleep_channel_pricing');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      } catch (e) {}
    }
    return SLEEP_CHANNEL_PRICING;
  });

  const [mapBreaches, setMapBreaches] = useState<MAPBreach[]>(() => {
    const saved = localStorage.getItem('agile_sleep_map_breaches');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length >= 4) {
          return parsed.map((b: MAPBreach) => ({
            ...b,
            estimatedLossInr: b.estimatedLossInr || ((b.enforcedMap - b.violatedPrice) * 150),
            priceGapInr: b.priceGapInr || (b.enforcedMap - b.violatedPrice)
          }));
        }
      } catch (e) {}
    }
    return SLEEP_MAP_BREACHES;
  });

  const [alerts, setAlerts] = useState<AlertAnomaly[]>(() => {
    const saved = localStorage.getItem('agile_sleep_alerts');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      } catch (e) {}
    }
    return SLEEP_ALERTS;
  });

  useEffect(() => {
    setAlerts(prevAlerts => {
      let updatedAlerts = [...prevAlerts];
      let changed = false;
      darkStores.forEach(store => {
        const stock = store.availableStock ?? 15;
        if (stock < 10) {
          const skuCode = store.sku || 'SLP-1001';
          const parentSku = skus.find(s => s.sku.toLowerCase() === skuCode.toLowerCase()) || skus[0];
          const alertId = `alt-oos-${store.storeId}-${skuCode}`;
          const suggestedUnits = Math.max(50, ((store.dailyVelocity || parentSku?.dailyVelocity || 40) * 2) - stock);
          const newAlert: AlertAnomaly = {
            id: alertId,
            sku: skuCode,
            productName: store.productName || parentSku?.name || 'Contour Memory Foam Cervical Pillow',
            marketplace: store.platform || 'blinkit',
            severity: stock < 5 ? 'Critical' : 'High',
            status: 'New',
            timestamp: new Date().toISOString(),
            timeDisplay: 'Just now',
            summary: `Micro-OOS Risk in ${store.storeName} (${store.storeId}): Stock dropped to ${stock} units (${((stock / (store.dailyVelocity || parentSku?.dailyVelocity || 40)) * 24).toFixed(1)} hrs cover). Recommended dispatch of ${suggestedUnits} units from ${store.motherHubName || parentSku?.defaultMotherHub || 'Bengaluru Central Mother Hub (Nelamangala)'}.`,
            revenueAtRiskInr: Math.round((store.sellingPrice || parentSku?.sellingPrice || 2499) * (store.dailyVelocity || parentSku?.dailyVelocity || 40) * 3),
            manufacturerName: parentSku?.manufacturerName || 'OrthoRest FoamTech India Pvt Ltd',
            manufacturerPlant: parentSku?.manufacturerPlant || 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
            darkStoreStock: stock,
            motherHubName: store.motherHubName || parentSku?.defaultMotherHub || 'Bengaluru Central Mother Hub (Nelamangala)',
            motherHubStock: store.motherHubStock || 150000,
            motherHubPincode: store.pincode || '562123',
            batchNumber: 'BAT-2026-088C',
            mfgDate: '2026-04-10',
            expiryDate: '2029-04-10',
            shelfLifeHealth: 98,
            transferLeadTimeHours: 1.2,
            recommendedPlaybook: 'Autonomous Stock Transfer Dispatch',
            transferUnitsSuggested: suggestedUnits,
            logisticsPartner: 'BlueDart Express Intra-City Corridor',
            targetOwnerEmail: 'vikashr984@gmail.com'
          };

          const existingIndex = updatedAlerts.findIndex(a => a.id === alertId || (a.sku === skuCode && a.summary.includes(store.storeId)));

          if (existingIndex >= 0) {
            const existing = updatedAlerts[existingIndex];
            if (existing.darkStoreStock !== stock || existing.status === 'Resolved' || existing.id !== alertId) {
              updatedAlerts.splice(existingIndex, 1);
              updatedAlerts.unshift(newAlert);
              changed = true;
            }
          } else {
            updatedAlerts.unshift(newAlert);
            changed = true;
          }
        }
      });
      return changed ? updatedAlerts : prevAlerts;
    });
  }, [darkStores, skus]);

  // Automatically send email to owner whenever a new stock drop alert/log appears at the top
  useEffect(() => {
    if (!alerts || alerts.length === 0) return;
    try {
      const latestAlert = alerts[0];
      const lastEmailedId = localStorage.getItem('agile_sleep_last_emailed_alert_id');

      if (latestAlert && latestAlert.id !== lastEmailedId) {
        const emailData = generateInteractiveEmail(latestAlert, skus.find(s => s.sku === latestAlert.sku), null, {
          datasetContext: { skus, darkStores, alerts }
        });
        
        // Send automated alert email
        sendEmail({
          to: latestAlert.targetOwnerEmail || 'vikashr984@gmail.com',
          subject: emailData.subject,
          textContent: emailData.textContent,
          htmlContent: emailData.htmlContent,
          reportType: `Stock Drop Incident Alert (${latestAlert.sku})`,
          anomalyId: latestAlert.id,
          skuId: latestAlert.sku
        }).then(result => {
          console.log('Automated stock drop alert email sent:', latestAlert.id, result);
        }).catch(err => {
          console.error('Failed to send alert email:', err);
        });

        localStorage.setItem('agile_sleep_last_emailed_alert_id', latestAlert.id);
      }
    } catch (e) {
      console.error('Error in automated alert email dispatch:', e);
    }
  }, [alerts, skus, darkStores]);

  const [autonomousActions, setAutonomousActions] = useState<AutonomousAction[]>(() => {
    return buildAllAutonomousActions(alerts, skus);
  });

  useEffect(() => {
    setAutonomousActions(buildAllAutonomousActions(alerts, skus));
  }, [skus, alerts]);

  const approveAction = async (actionId: string) => {
    const actionToApprove = autonomousActions.find(a => a.id === actionId);
    if (actionToApprove) {
      if (actionToApprove.transferDetails && actionToApprove.sku) {
        const targetSkuObj = skus.find(s => s.sku === actionToApprove.sku);
        const productName = targetSkuObj ? targetSkuObj.name : actionToApprove.title;
        triggerStockTransfer(
          actionToApprove.sku,
          actionToApprove.transferDetails.fromMotherHub,
          actionToApprove.transferDetails.units,
          'BLNK-BLR-HSR-01',
          productName
        );
      }

      setAutonomousActions(prev =>
        prev.map(a => (a.id === actionId ? { ...a, status: 'Executed', executionStatus: 'Completed Live' } : a))
      );

      try {
        await sendEmail({
          to: 'vikashr984@gmail.com',
          subject: `[EXECUTED PLAYBOOK] ${actionToApprove.title}`,
          textContent: `Autonomous Playbook "${actionToApprove.title}" was successfully executed via 1-Click Approval.\n\nSKU: ${actionToApprove.sku}\nImpact: INR ${actionToApprove.estimatedValueRecoveredInr?.toLocaleString('en-IN')}\nStatus: Completed Live, Stock Transferred & Logged to Audit Trail.`,
          reportType: 'Autonomous Action Execution & Supply Chain Briefing'
        });
      } catch (e) {
        console.error('Playbook execution notification email failed:', e);
      }
    }
  };

  const rejectAction = (actionId: string) => {
    setAutonomousActions(prev =>
      prev.map(a => (a.id === actionId ? { ...a, status: 'Rejected' } : a))
    );
  };

  const [transferLogs, setTransferLogs] = useState<StockTransferLog[]>(() => {
    const saved = localStorage.getItem('agile_sleep_transfer_logs');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      } catch (e) {}
    }
    return [
      {
        id: 'TRF-849201',
        timestamp: '17 Aug 2026, 07:16 AM',
        sku: 'SKU-SC-001',
        productName: 'Sleepsia Orthopedic Memory Foam Pillow',
        sourceMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
        targetDarkStore: 'Blinkit HSR Layout Hub 04 (Bengaluru)',
        unitsTransferred: 250,
        carrier: 'Shadowfax Quick-Commerce Freight',
        trackingNumber: 'SFX-BLR-849201',
        status: 'Completed',
        executedBy: 'Vikash (Super Admin)'
      }
    ];
  });

  const [syncState, setSyncState] = useState<DatasetSyncState>(() => {
    const savedUrl = localStorage.getItem('agile_google_sheet_url');
    return {
      source: savedUrl ? 'google_sheet' : 'local',
      googleSheetUrl: savedUrl || 'https://docs.google.com/spreadsheets/d/1eIbxGYnjNqjFJVb9aJ-P8xzinZk',
      lastSynced: 'Just now',
      rowCount: skus.length,
      syncStatus: 'synced'
    };
  });

  const [googleSheetWebhookUrl, setGoogleSheetWebhookUrlState] = useState<string>(() => {
    return localStorage.getItem('agile_google_sheet_webhook_url') || '';
  });

  const setGoogleSheetWebhookUrl = (url: string) => {
    setGoogleSheetWebhookUrlState(url);
    localStorage.setItem('agile_google_sheet_webhook_url', url);
  };

  const [currentUser, setCurrentUser] = useState<UserPersona>(USER_PERSONAS[0]);

  // Persist state updates to localStorage cleanly
  useEffect(() => {
    localStorage.setItem('agile_sleep_skus', JSON.stringify(skus));
  }, [skus]);

  useEffect(() => {
    localStorage.setItem('agile_sleep_dark_stores', JSON.stringify(darkStores));
    setSkus(prevSkus => computeSkusWithDarkStores(prevSkus, darkStores));
  }, [darkStores]);

  useEffect(() => {
    localStorage.setItem('agile_sleep_transfer_logs', JSON.stringify(transferLogs));
  }, [transferLogs]);

  useEffect(() => {
    localStorage.setItem('agile_sleep_channel_pricing', JSON.stringify(channelPricing));
  }, [channelPricing]);

  useEffect(() => {
    localStorage.setItem('agile_sleep_map_breaches', JSON.stringify(mapBreaches));
  }, [mapBreaches]);

  useEffect(() => {
    localStorage.setItem('agile_sleep_alerts', JSON.stringify(alerts));
    setAutonomousActions(buildActionsFromAlerts(alerts));
  }, [alerts]);

  // Update a specific SKU with reactive multi-table propagation
  const updateSKU = (skuCode: string, updates: Partial<SKUListing>) => {
    if (updates.darkStoreStock !== undefined) {
      const newStock = Number(updates.darkStoreStock) || 0;
      setDarkStores((prevStores) => {
        const skuStores = prevStores.filter(d => d.sku?.toLowerCase() === skuCode.toLowerCase());
        if (skuStores.length > 0) {
          // Assign newStock to the lowest stock store (or first store) and 0 to others so the total sum matches newStock
          const lowestStoreId = [...skuStores].sort((a, b) => (a.availableStock ?? 0) - (b.availableStock ?? 0))[0]?.storeId || skuStores[0].storeId;
          return prevStores.map(d => {
            if (d.sku?.toLowerCase() === skuCode.toLowerCase()) {
              if (d.storeId === lowestStoreId) {
                return { ...d, availableStock: newStock };
              } else {
                return { ...d, availableStock: 0 };
              }
            }
            return d;
          });
        }
        return prevStores;
      });
    }

    setSkus((prev) =>
      prev.map((s) => {
        if (s.sku.toLowerCase() === skuCode.toLowerCase()) {
          const sellingPrice = updates.sellingPrice !== undefined ? updates.sellingPrice : s.sellingPrice;
          const dailyVelocity = updates.dailyVelocity !== undefined ? updates.dailyVelocity : (s.dailyVelocity || 50);
          const darkStoreStock = updates.darkStoreStock !== undefined ? updates.darkStoreStock : (s.darkStoreStock || 0);
          const grossSales30d = updates.grossSales30d !== undefined ? updates.grossSales30d : Math.round(sellingPrice * dailyVelocity * 30);
          const revenueAtRisk = computeRevenueAtRisk(darkStoreStock, dailyVelocity, sellingPrice);
          const stockStatus = darkStoreStock > 10 ? 'Active' : 'Low Stock';

          return {
            ...s,
            ...updates,
            sellingPrice,
            dailyVelocity,
            grossSales30d,
            revenueAtRisk,
            stockStatus
          };
        }
        return s;
      })
    );

    // Propagate sellingPrice / targetMap changes to Channel Pricing matrix
    if (updates.sellingPrice !== undefined || updates.targetMap !== undefined) {
      setChannelPricing((prev) =>
        prev.map((cp) => {
          if (cp.sku.toLowerCase() === skuCode.toLowerCase()) {
            const currentSellingPrice = updates.sellingPrice !== undefined ? updates.sellingPrice : cp.currentSellingPrice;
            const targetMap = updates.targetMap !== undefined ? updates.targetMap : cp.targetMap;
            const mapBreached = targetMap > 0 && currentSellingPrice < targetMap;
            const priceDelta = currentSellingPrice - targetMap;
            return {
              ...cp,
              currentSellingPrice,
              targetMap,
              mapBreached,
              priceDelta,
              status: mapBreached ? 'Active Breach' : 'Compliant',
              complianceAction: mapBreached ? 'Auto Cease-and-Desist Notice Drafted' : 'Active - Price Protected'
            };
          }
          return cp;
        })
      );
    }

    // Propagate price / velocity changes to Dark Stores
    setDarkStores((prev) => {
      return prev.map((d) => {
        if (d.sku.toLowerCase() === skuCode.toLowerCase()) {
          const sellingPrice = updates.sellingPrice !== undefined ? updates.sellingPrice : d.sellingPrice;
          const dailyVelocity = updates.dailyVelocity !== undefined ? updates.dailyVelocity : d.dailyVelocity;
          const runwayHours = dailyVelocity ? Number(((d.availableStock / (dailyVelocity / 24))).toFixed(1)) : d.runwayHours;
          return {
            ...d,
            sellingPrice,
            dailyVelocity,
            runwayHours
          };
        }
        return d;
      });
    });

    setSyncState((prev) => ({ ...prev, syncStatus: 'modified_locally', lastSynced: 'Just now' }));

    // If Google Sheet Webhook is configured, automatically push in background
    if (googleSheetWebhookUrl) {
      fetch('/api/sheets/push-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webhookUrl: googleSheetWebhookUrl,
          sku: skuCode,
          updates
        })
      }).catch((e) => console.warn('Background Google Sheet webhook push failed:', e));
    }
  };

  // Update a Channel Pricing Item (Selling Price, MAP, Stock, etc.)
  const updateChannelPricing = (id: string, updates: Partial<ChannelPricingItem>) => {
    let targetItem: ChannelPricingItem | null = null;

    setChannelPricing((prev) => {
      const next = prev.map((item) => {
        if (item.id === id || (item.sku === updates.sku && String(item.marketplace).toLowerCase() === String(updates.marketplace).toLowerCase())) {
          const currentSellingPrice = updates.currentSellingPrice !== undefined ? updates.currentSellingPrice : item.currentSellingPrice;
          const targetMap = updates.targetMap !== undefined ? updates.targetMap : item.targetMap;
          const mapBreached = updates.mapBreached !== undefined ? updates.mapBreached : (targetMap > 0 && currentSellingPrice < targetMap);
          const priceDelta = currentSellingPrice - targetMap;
          const status = updates.status || (mapBreached ? 'Active Breach' : 'Compliant');
          const complianceAction = mapBreached ? (updates.complianceAction || 'Auto Cease-and-Desist Notice Drafted') : 'Active - Price Protected';

          const updated: ChannelPricingItem = {
            ...item,
            ...updates,
            currentSellingPrice,
            targetMap,
            mapBreached,
            priceDelta,
            status,
            complianceAction
          };
          targetItem = updated;
          return updated;
        }
        return item;
      });
      return next;
    });

    if (targetItem) {
      const item = targetItem as ChannelPricingItem;
      // Sync into SKU Master marketplace price map
      setSkus((prevSkus) => {
        return prevSkus.map((s) => {
          if (s.sku.toLowerCase() === item.sku.toLowerCase()) {
            const mpKey = String(item.marketplace).toLowerCase() as any;
            const existingMp = s.marketplacePrices?.[mpKey] || { price: item.currentSellingPrice, inStock: item.inStock, shareOfSearch: item.shareOfSearch, revenue30d: item.revenue30d, buyBoxOwner: item.buyBoxOwner };
            return {
              ...s,
              targetMap: item.targetMap,
              marketplacePrices: {
                ...s.marketplacePrices,
                [mpKey]: {
                  ...existingMp,
                  price: item.currentSellingPrice,
                  inStock: item.inStock,
                  buyBoxOwner: item.buyBoxOwner
                }
              }
            };
          }
          return s;
        });
      });

      // Synchronize MAP Breach dataset
      setMapBreaches((prevBreaches) => {
        const breachExists = prevBreaches.some((b) => b.sku.toLowerCase() === item.sku.toLowerCase() && b.channel.toLowerCase() === String(item.marketplace).toLowerCase());
        if (item.mapBreached) {
          if (breachExists) {
            return prevBreaches.map((b) => {
              if (b.sku.toLowerCase() === item.sku.toLowerCase() && b.channel.toLowerCase() === String(item.marketplace).toLowerCase()) {
                return {
                  ...b,
                  violatedPrice: item.currentSellingPrice,
                  enforcedMap: item.targetMap,
                  violatingSeller: item.buyBoxOwner,
                  status: item.status as any,
                  discountPercent: Number((((item.targetMap - item.currentSellingPrice) / item.targetMap) * 100).toFixed(1))
                };
              }
              return b;
            });
          } else {
            return [
              ...prevBreaches,
              {
                id: `MAP-${item.sku}-${item.marketplace}`,
                sku: item.sku,
                productName: item.productName,
                channel: String(item.marketplace).toLowerCase() as any,
                violatingSeller: item.buyBoxOwner,
                enforcedMap: item.targetMap,
                violatedPrice: item.currentSellingPrice,
                discountPercent: Number((((item.targetMap - item.currentSellingPrice) / item.targetMap) * 100).toFixed(1)),
                breachDurationHours: 1.0,
                status: 'Active Breach',
                evidenceUrl: `https://${String(item.marketplace).toLowerCase()}.com/dp/${item.sku}`,
                complianceAction: 'Auto Cease-and-Desist Notice Drafted'
              }
            ];
          }
        } else {
          return prevBreaches.filter((b) => !(b.sku.toLowerCase() === item.sku.toLowerCase() && b.channel.toLowerCase() === String(item.marketplace).toLowerCase()));
        }
      });

      setSyncState((prev) => ({ ...prev, syncStatus: 'modified_locally', lastSynced: 'Just now' }));

      // Background webhook push if configured
      if (googleSheetWebhookUrl) {
        fetch('/api/sheets/push-webhook', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            webhookUrl: googleSheetWebhookUrl,
            type: 'channel_pricing',
            sku: item.sku,
            marketplace: item.marketplace,
            updates: item
          })
        }).catch((e) => console.warn('Background Google Sheet webhook push failed:', e));
      }
    }
  };

  // Push updates to Google Sheet Webhook for SKU Master
  const pushToGoogleSheet = async (skuCode: string, customUpdates?: Partial<SKUListing>): Promise<{ success: boolean; message: string }> => {
    if (!googleSheetWebhookUrl) {
      return {
        success: false,
        message: 'No Google Apps Script Webhook URL configured. Please paste your Webhook URL in the sync settings below.'
      };
    }

    try {
      const targetSku = skus.find((s) => s.sku === skuCode);
      const updatesToSend = customUpdates || (targetSku ? {
        sellingPrice: targetSku.sellingPrice,
        mrp: targetSku.mrp,
        targetMap: targetSku.targetMap,
        darkStoreStock: targetSku.darkStoreStock,
        motherHubStock: targetSku.motherHubStock,
        revenueAtRisk: targetSku.revenueAtRisk,
        RevenueAtRisk_INR: targetSku.revenueAtRisk
      } : {});

      const res = await fetch('/api/sheets/push-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webhookUrl: googleSheetWebhookUrl,
          sheetTab: '1_SKU_Master',
          sku: skuCode,
          updates: updatesToSend
        })
      });

      const data = await res.json();
      if (data.success) {
        return { success: true, message: data.message || `Successfully pushed ${skuCode} to Google Sheets!` };
      }
      return { success: false, message: data.message || 'Google Sheet update failed.' };
    } catch (err: any) {
      return { success: false, message: err.message || 'Failed to connect to Google Sheets Webhook.' };
    }
  };

  // Push updates to Google Sheet Webhook for Channel Pricing & MAP
  const pushChannelPricingToGoogleSheet = async (item: ChannelPricingItem): Promise<{ success: boolean; message: string }> => {
    if (!googleSheetWebhookUrl) {
      return {
        success: false,
        message: 'No Google Apps Script Webhook URL configured. Please paste your Webhook URL in the dataset sync settings.'
      };
    }

    try {
      const res = await fetch('/api/sheets/push-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webhookUrl: googleSheetWebhookUrl,
          sheetTab: '3_Channel_Pricing_MAP',
          sku: item.sku,
          marketplace: item.marketplace,
          updates: {
            SKU: item.sku,
            ProductName: item.productName,
            Marketplace: String(item.marketplace).toUpperCase(),
            CurrentSellingPrice_INR: item.currentSellingPrice,
            Target_MAP_INR: item.targetMap,
            MAP_Breached: item.mapBreached ? 'YES (BREACH)' : 'NO',
            PriceDelta_INR: item.priceDelta,
            InStock: item.inStock ? 'TRUE' : 'FALSE',
            BuyBoxOwner: item.buyBoxOwner,
            ShareOfSearch: item.shareOfSearch,
            Revenue30d_INR: item.revenue30d
          }
        })
      });

      const data = await res.json();
      if (data.success) {
        return { success: true, message: data.message || `Successfully pushed ${item.sku} (${String(item.marketplace).toUpperCase()}) to Google Sheets!` };
      }
      return { success: false, message: data.message || 'Google Sheet update failed.' };
    } catch (err: any) {
      return { success: false, message: err.message || 'Failed to connect to Google Sheets Webhook.' };
    }
  };

  useEffect(() => {
    localStorage.setItem('agile_sleep_mother_hub_skus', JSON.stringify(motherHubSkuStock));
  }, [motherHubSkuStock]);

  useEffect(() => {
    localStorage.setItem('agile_sleep_manufacturer_supply', JSON.stringify(manufacturerSupply));
  }, [manufacturerSupply]);

  // Update a specific Dark Store with automatic cross-table SKU and Alert propagation
  const updateDarkStore = (storeId: string, updates: Partial<DarkStoreInventory>, skuCode?: string) => {
    let affectedSku: string | null = skuCode || updates.sku || null;

    setDarkStores((prev) => {
      const next = prev.map((d) => {
        const isMatch = d.storeId === storeId && (!skuCode || d.sku === skuCode);
        if (isMatch) {
          if (!affectedSku) affectedSku = d.sku;
          const availableStock = updates.availableStock !== undefined ? Number(updates.availableStock) : d.availableStock;
          const safetyThreshold = updates.safetyThreshold !== undefined ? Number(updates.safetyThreshold) : (d.safetyThreshold || 15);
          const dailyVelocity = updates.dailyVelocity !== undefined ? Number(updates.dailyVelocity) : (d.dailyVelocity || 40);
          const runwayHours = dailyVelocity > 0 ? Number(((availableStock / (dailyVelocity / 24))).toFixed(1)) : 48;
          const status = availableStock <= 0 ? 'Out Of Stock' : availableStock <= safetyThreshold ? 'Low Stock' : 'In Stock';

          return {
            ...d,
            ...updates,
            availableStock,
            safetyThreshold,
            dailyVelocity,
            runwayHours,
            status: status as any,
            lastChecked: 'Just now'
          };
        }
        return d;
      });

      // Synchronize aggregated darkStoreStock into SKU Master
      if (affectedSku) {
        const currentTargetSku = affectedSku;
        const totalStockForSku = next
          .filter((d) => d.sku?.toLowerCase() === currentTargetSku.toLowerCase())
          .reduce((sum, d) => sum + (d.availableStock ?? 0), 0);

        setSkus((prevSkus) =>
          prevSkus.map((s) => {
            if (s.sku.toLowerCase() === currentTargetSku.toLowerCase()) {
              const revenueAtRisk = computeRevenueAtRisk(totalStockForSku, s.dailyVelocity || 50, s.sellingPrice);
              const stockStatus = totalStockForSku > 10 ? 'Active' : 'Low Stock';
              return {
                ...s,
                darkStoreStock: totalStockForSku,
                revenueAtRisk,
                stockStatus
              };
            }
            return s;
          })
        );
      }

      return next;
    });

    setSyncState((prev) => ({ ...prev, syncStatus: 'modified_locally', lastSynced: 'Just now' }));
  };

  // Update a Mother Hub SKU Stock record with SKU Master sync
  const updateMotherHubSkuStock = (id: string, updates: Partial<MotherHubSkuStock>) => {
    let affectedSku: string | null = updates.sku || null;

    setMotherHubSkuStock((prev) => {
      const next = prev.map((m) => {
        if (m.id === id) {
          if (!affectedSku) affectedSku = m.sku;
          const quantityAvailable = updates.quantityAvailable !== undefined ? Number(updates.quantityAvailable) : m.quantityAvailable;
          const safetyStockThreshold = updates.safetyStockThreshold !== undefined ? Number(updates.safetyStockThreshold) : m.safetyStockThreshold;
          const bufferHealth = quantityAvailable < safetyStockThreshold * 0.5
            ? 'Critical'
            : quantityAvailable < safetyStockThreshold
            ? 'Adequate'
            : 'Optimal';

          return {
            ...m,
            ...updates,
            quantityAvailable,
            safetyStockThreshold,
            bufferHealth: bufferHealth as any
          };
        }
        return m;
      });

      if (affectedSku) {
        const currentSku = affectedSku;
        const totalHubStock = next
          .filter((m) => m.sku?.toLowerCase() === currentSku.toLowerCase())
          .reduce((sum, m) => sum + (m.quantityAvailable ?? 0), 0);

        setSkus((prevSkus) =>
          prevSkus.map((s) => {
            if (s.sku.toLowerCase() === currentSku.toLowerCase()) {
              return {
                ...s,
                motherHubStock: totalHubStock
              };
            }
            return s;
          })
        );
      }

      return next;
    });

    setSyncState((prev) => ({ ...prev, syncStatus: 'modified_locally', lastSynced: 'Just now' }));
  };

  // Update a Manufacturer Supply record
  const updateManufacturerSupply = (id: string, updates: Partial<ManufacturerSupplyInfo>) => {
    setManufacturerSupply((prev) =>
      prev.map((m) => (m.id === id ? { ...m, ...updates } : m))
    );
    setSyncState((prev) => ({ ...prev, syncStatus: 'modified_locally', lastSynced: 'Just now' }));
  };

  // Push Dark Store Inventory to Google Sheet Webhook
  const pushDarkStoreToGoogleSheet = async (store: DarkStoreInventory): Promise<{ success: boolean; message: string }> => {
    if (!googleSheetWebhookUrl) {
      return {
        success: false,
        message: 'No Google Apps Script Webhook URL configured. Please paste your Webhook URL in the dataset sync settings.'
      };
    }
    try {
      const res = await fetch('/api/sheets/push-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webhookUrl: googleSheetWebhookUrl,
          sheetTab: '2_Dark_Stores_Inventory',
          sku: store.sku || 'SLP-1001',
          marketplace: store.platform,
          updates: {
            Store_ID: store.storeId,
            Store_Name: store.storeName,
            SKU: store.sku || 'SLP-1001',
            Platform: String(store.platform).toUpperCase(),
            City_Pincode: `${store.city} (${store.pincode})`,
            Available_Stock: store.availableStock,
            Stock_Status: store.status,
            Delivery_SLA_Mins: store.deliverySlaMins || 10,
            Mother_Hub: store.motherHubName || 'Bengaluru Central Mother Hub',
            Mother_Hub_Stock: store.motherHubStock,
            Transit_Hours: store.transitHoursFromHub || 1.2
          }
        })
      });
      const data = await res.json();
      if (data.success) {
        return { success: true, message: data.message || `Successfully pushed ${store.storeName} to Google Sheets!` };
      }
      return { success: false, message: data.message || 'Google Sheet update failed.' };
    } catch (err: any) {
      return { success: false, message: err.message || 'Failed to connect to Google Sheets Webhook.' };
    }
  };

  // Update a specific Alert Anomaly
  const updateAlert = (alertId: string, updates: Partial<AlertAnomaly>) => {
    setAlerts((prev) =>
      prev.map((a) => (a.id === alertId ? { ...a, ...updates } : a))
    );
    setSyncState((prev) => ({ ...prev, syncStatus: 'modified_locally', lastSynced: 'Just now' }));
  };

  // Push Trigger / Alert Log to Google Sheet Webhook
  const pushAlertToGoogleSheet = async (alert: AlertAnomaly): Promise<{ success: boolean; message: string }> => {
    if (!googleSheetWebhookUrl) {
      return {
        success: false,
        message: 'No Google Apps Script Webhook URL configured. Please paste your Webhook URL in the dataset sync settings.'
      };
    }
    try {
      const res = await fetch('/api/sheets/push-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webhookUrl: googleSheetWebhookUrl,
          sheetTab: '4_Triggers_Alerts_Log',
          sku: alert.sku,
          marketplace: alert.marketplace,
          updates: {
            Alert_ID: alert.id,
            SKU: alert.sku,
            Product_Name: alert.productName,
            Marketplace: String(alert.marketplace).toUpperCase(),
            Severity: alert.severity,
            Revenue_At_Risk_INR: alert.revenueAtRiskInr,
            Summary: alert.summary,
            Transfer_Units: alert.transferUnitsSuggested,
            Target_Owner: alert.targetOwnerEmail,
            Status: alert.status
          }
        })
      });
      const data = await res.json();
      if (data.success) {
        return { success: true, message: data.message || `Successfully pushed alert ${alert.id} to Google Sheets!` };
      }
      return { success: false, message: data.message || 'Google Sheet update failed.' };
    } catch (err: any) {
      return { success: false, message: err.message || 'Failed to connect to Google Sheets Webhook.' };
    }
  };

  // Trigger automated stock replenishment transfer with complete multi-sheet reactive balance
  const triggerStockTransfer = (
    sku: string,
    hub: string,
    units: number,
    storeId?: string,
    productName = 'Sleepsia Orthopedic Memory Foam Pillow',
    carrier = 'Shadowfax Quick-Commerce Freight',
    trackingNumber = `SFX-BLR-${Date.now().toString().slice(-6)}`
  ) => {
    let resolvedStoreName = 'Dark Store Pod';

    // 1. Update Dark Store Pod
    setDarkStores((prev) => {
      const updated = prev.map((d) => {
        const isMatch = (storeId && d.storeId === storeId && (!sku || d.sku === sku)) ||
          (!storeId && d.sku === sku);
        if (isMatch) {
          resolvedStoreName = `${d.storeName} (${d.city})`;
          const newStock = d.availableStock + units;
          const currentHubStock = d.motherHubStock !== undefined ? d.motherHubStock : 50000;
          const newHubStock = Math.max(0, currentHubStock - units);
          const safety = d.safetyThreshold || 15;
          const velocity = d.dailyVelocity || 40;
          const newRunway = Number(((newStock / (velocity / 24))).toFixed(1));

          return {
            ...d,
            availableStock: newStock,
            motherHubStock: newHubStock,
            runwayHours: newRunway,
            status: (newStock <= 0 ? 'Out Of Stock' : newStock <= safety ? 'Low Stock' : 'In Stock') as any,
            lastChecked: 'Just now'
          };
        }
        return d;
      });
      return updated;
    });

    // 2. Decrement Mother Hub SKU stock reserves
    setMotherHubSkuStock((prev) => {
      return prev.map((h) => {
        const isMatch = h.sku.toLowerCase() === sku.toLowerCase() &&
          (h.hubName.toLowerCase().includes(hub.toLowerCase()) || hub.toLowerCase().includes(h.hubName.toLowerCase()) || h.hubId === hub);
        if (isMatch) {
          const newQty = Math.max(0, h.quantityAvailable - units);
          const bufferHealth = newQty < h.safetyStockThreshold * 0.5 ? 'Critical' : newQty < h.safetyStockThreshold ? 'Adequate' : 'Optimal';
          return {
            ...h,
            quantityAvailable: newQty,
            bufferHealth: bufferHealth as any
          };
        }
        return h;
      });
    });

    // 3. Decrement Mother Hub total capacity
    setMotherHubs((prev) => {
      return prev.map((mh) => {
        if (mh.name.toLowerCase().includes(hub.toLowerCase()) || hub.toLowerCase().includes(mh.name.toLowerCase()) || mh.id === hub) {
          return {
            ...mh,
            currentStockUnits: Math.max(0, mh.currentStockUnits - units)
          };
        }
        return mh;
      });
    });

    // 4. Update SKU Master (recalculate aggregate dark store stock, clear risk, restore status)
    setSkus((prev) => {
      const updated = prev.map((s) => {
        if (s.sku.toLowerCase() === sku.toLowerCase()) {
          const newDarkStock = (s.darkStoreStock || 3) + units;
          const currentHubStock = s.motherHubStock !== undefined ? s.motherHubStock : 100000;
          const newHubStock = Math.max(0, currentHubStock - units);
          return {
            ...s,
            darkStoreStock: newDarkStock,
            motherHubStock: newHubStock,
            revenueAtRisk: computeRevenueAtRisk(newDarkStock, s.dailyVelocity || 50, s.sellingPrice),
            stockStatus: (newDarkStock > 10 ? 'Active' : 'Low Stock') as any
          };
        }
        return s;
      });
      return updated;
    });

    // 5. Automatically resolve active Low Stock alerts for this SKU
    setAlerts((prev) =>
      prev.map((a) => {
        if (a.sku.toLowerCase() === sku.toLowerCase() && a.status !== 'Resolved' && (a.summary.toLowerCase().includes('stock') || a.severity === 'Critical')) {
          return {
            ...a,
            status: 'Resolved',
            summary: `Resolved via automated stock transfer: Dispatched ${units} units from ${hub} (Tracking ${trackingNumber})`
          };
        }
        return a;
      })
    );

    // 6. Update Connected Manufacturer Supply / Factory Production stock if applicable
    setManufacturerSupply((prev) =>
      prev.map((m) => {
        if (m.sku.toLowerCase() === sku.toLowerCase() && (m.destinationMotherHub.toLowerCase().includes(hub.toLowerCase()) || hub.toLowerCase().includes(m.destinationMotherHub.toLowerCase()))) {
          const newFinishedGoods = Math.max(0, m.factoryFinishedGoodsStock - Math.round(units * 0.5));
          return {
            ...m,
            factoryFinishedGoodsStock: newFinishedGoods,
            workInProgressUnits: m.workInProgressUnits + Math.round(units * 0.5) // Auto-replenishing WIP batch
          };
        }
        return m;
      })
    );

    // 7. Record Audit Log
    const newLog: StockTransferLog = {
      id: `TRF-${Math.floor(100000 + Math.random() * 900000)}`,
      timestamp: new Date().toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' }),
      sku,
      productName,
      sourceMotherHub: hub,
      targetDarkStore: resolvedStoreName || 'Dark Store Pod Hub',
      unitsTransferred: units,
      carrier,
      trackingNumber,
      status: 'In Transit (~3.5h SLA)',
      executedBy: currentUser?.name || 'Vikash (Super Admin)'
    };

    setTransferLogs((prev) => [newLog, ...prev]);
    setSyncState((prev) => ({ ...prev, syncStatus: 'modified_locally', lastSynced: 'Just now' }));
  };

  const exportTransferLogsToExcel = () => {
    exportTransferLogsToExcelService(transferLogs);
  };

  const exportAlertsLogToExcel = () => {
    exportAlertsLogToExcelService(alerts);
  };

  // Push Mother Hub record to Google Sheet Webhook
  const pushMotherHubToGoogleSheet = async (hub: MotherHubSkuStock): Promise<{ success: boolean; message: string }> => {
    if (!googleSheetWebhookUrl) {
      return {
        success: false,
        message: 'No Google Apps Script Webhook URL configured. Please paste your Webhook URL in the dataset sync settings.'
      };
    }
    try {
      const res = await fetch('/api/sheets/push-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webhookUrl: googleSheetWebhookUrl,
          sheetTab: '5_Mother_Hubs_Inventory',
          sku: hub.sku || 'SLP-1001',
          marketplace: 'mother_hub',
          updates: {
            Hub_ID: hub.hubId,
            Hub_Name: hub.hubName,
            City_Region: hub.city,
            Pincode: hub.pincode,
            SKU: hub.sku,
            Product_Name: hub.productName,
            Quantity_Available: hub.quantityAvailable,
            Reserved_Quantity: hub.reservedQuantity,
            Safety_Stock_Threshold: hub.safetyStockThreshold,
            Buffer_Health: hub.bufferHealth,
            Connected_Pods: hub.connectedDarkStoresCount,
            Dispatch_SLA_Hours: hub.dispatchSlaHours
          }
        })
      });
      const data = await res.json();
      if (data.success) {
        return { success: true, message: data.message || `Successfully pushed ${hub.hubName} (${hub.sku}) to Google Sheets!` };
      }
      return { success: false, message: data.message || 'Google Sheet update failed.' };
    } catch (err: any) {
      return { success: false, message: err.message || 'Failed to connect to Google Sheets Webhook.' };
    }
  };

  // Push Manufacturer Supply record to Google Sheet Webhook
  const pushManufacturerSupplyToGoogleSheet = async (mfg: ManufacturerSupplyInfo): Promise<{ success: boolean; message: string }> => {
    if (!googleSheetWebhookUrl) {
      return {
        success: false,
        message: 'No Google Apps Script Webhook URL configured. Please paste your Webhook URL in the dataset sync settings.'
      };
    }
    try {
      const res = await fetch('/api/sheets/push-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webhookUrl: googleSheetWebhookUrl,
          sheetTab: '6_Manufacturers_Supply',
          sku: mfg.sku || 'SLP-1001',
          marketplace: 'factory',
          updates: {
            Manufacturer_Name: mfg.manufacturerName,
            Plant_Name: mfg.plantName,
            Location_City: mfg.location,
            Pincode: mfg.pincode,
            SKU: mfg.sku,
            Product_Name: mfg.productName,
            Finished_Goods_Stock: mfg.factoryFinishedGoodsStock,
            WIP_Units: mfg.workInProgressUnits,
            Monthly_Capacity: mfg.monthlyCapacityUnits,
            Daily_Production_Rate: mfg.dailyProductionRate,
            Lead_Time_Hours: mfg.leadTimeToMotherHubHours,
            Destination_Hub: mfg.destinationMotherHub,
            Active_Batch: mfg.activeBatchNumber,
            Mfg_Date: mfg.mfgDate,
            Quality_Pass_Rate: mfg.qualityPassRate
          }
        })
      });
      const data = await res.json();
      if (data.success) {
        return { success: true, message: data.message || `Successfully pushed ${mfg.plantName} (${mfg.sku}) to Google Sheets!` };
      }
      return { success: false, message: data.message || 'Google Sheet update failed.' };
    } catch (err: any) {
      return { success: false, message: err.message || 'Failed to connect to Google Sheets Webhook.' };
    }
  };

  // Push ALL active records across all 6 tabs to Google Sheet Webhook (Two-Way Harmonization)
  const pushFullDatasetToGoogleSheet = async (): Promise<{ success: boolean; message: string }> => {
    if (!googleSheetWebhookUrl) {
      return {
        success: false,
        message: 'No Google Apps Script Webhook URL configured. Please paste your Webhook URL in the dataset sync settings.'
      };
    }
    try {
      let successCount = 0;
      let totalCount = 0;

      // 1. SKU Master
      for (const s of skus) {
        totalCount++;
        const res = await pushToGoogleSheet(s.sku);
        if (res.success) successCount++;
      }

      // 2. Dark Stores
      for (const d of darkStores) {
        totalCount++;
        const res = await pushDarkStoreToGoogleSheet(d);
        if (res.success) successCount++;
      }

      // 3. Channel Pricing
      for (const cp of channelPricing) {
        totalCount++;
        const res = await pushChannelPricingToGoogleSheet(cp);
        if (res.success) successCount++;
      }

      // 4. Alerts
      for (const a of alerts) {
        totalCount++;
        const res = await pushAlertToGoogleSheet(a);
        if (res.success) successCount++;
      }

      // 5. Mother Hubs
      for (const h of motherHubSkuStock) {
        totalCount++;
        const res = await pushMotherHubToGoogleSheet(h);
        if (res.success) successCount++;
      }

      // 6. Manufacturer Supply
      for (const m of manufacturerSupply) {
        totalCount++;
        const res = await pushManufacturerSupplyToGoogleSheet(m);
        if (res.success) successCount++;
      }

      setSyncState((prev) => ({
        ...prev,
        syncStatus: 'synced',
        lastSynced: new Date().toLocaleTimeString()
      }));

      return {
        success: true,
        message: `Successfully synchronized ${successCount}/${totalCount} total records across all 6 workbook sheets directly to your Google Sheet!`
      };
    } catch (err: any) {
      return {
        success: false,
        message: err.message || 'Failed to push complete dataset to Google Sheets.'
      };
    }
  };

  // Export current dataset to Excel (all 6 tabs)
  const exportToExcel = () => {
    exportDatasetToExcelWorkbook(
      skus,
      darkStores,
      mapBreaches,
      alerts,
      channelPricing,
      motherHubSkuStock,
      manufacturerSupply
    );
  };

  // Non-destructive intelligent merger for parsed workbook data
  const applyNonDestructiveIngestion = (parsed: {
    skus?: SKUListing[];
    darkStores?: DarkStoreInventory[];
    channelPricing?: ChannelPricingItem[];
    mapBreaches?: MAPBreach[];
    alerts?: AlertAnomaly[];
    motherHubSkuStock?: MotherHubSkuStock[];
    manufacturerSupply?: ManufacturerSupplyInfo[];
  }) => {
    // 1. Merge SKUs non-destructively
    if (parsed.skus && parsed.skus.length > 0) {
      setSkus((prevSkus) => {
        const updated = prevSkus.map((existingSku) => {
          const incoming = parsed.skus?.find(
            (s) => s.sku.trim().toLowerCase() === existingSku.sku.trim().toLowerCase()
          );
          if (incoming) {
            return {
              ...existingSku,
              ...incoming,
              marketplacePrices: {
                ...existingSku.marketplacePrices,
                ...(incoming.marketplacePrices || {})
              },
              batches: incoming.batches && incoming.batches.length > 0 ? incoming.batches : existingSku.batches,
              activeMarketplaces:
                incoming.activeMarketplaces && incoming.activeMarketplaces.length > 0
                  ? incoming.activeMarketplaces
                  : existingSku.activeMarketplaces
            };
          }
          return existingSku;
        });

        const newSkus = (parsed.skus || []).filter(
          (s) => !prevSkus.some((existing) => existing.sku.trim().toLowerCase() === s.sku.trim().toLowerCase())
        );
        return [...updated, ...newSkus];
      });
    }

    // 2. Merge Dark Stores non-destructively (NEVER remove existing pods)
    if (parsed.darkStores && parsed.darkStores.length > 0) {
      setDarkStores((prevStores) => {
        const makeKey = (storeId: string, sku?: string) =>
          `${(storeId || '').trim().toLowerCase()}___${(sku || '').trim().toLowerCase()}`;

        const incomingMap = new Map<string, DarkStoreInventory>();
        parsed.darkStores!.forEach((d) => {
          incomingMap.set(makeKey(d.storeId, d.sku), d);
          if (!d.sku || d.sku === 'SLP-1001') {
            incomingMap.set(d.storeId.trim().toLowerCase(), d);
          }
        });

        const updated = prevStores.map((existing) => {
          const keyWithSku = makeKey(existing.storeId, existing.sku);
          const keyStoreOnly = existing.storeId.trim().toLowerCase();
          const incoming = incomingMap.get(keyWithSku) || (existing.sku === 'SLP-1001' ? incomingMap.get(keyStoreOnly) : undefined);

          if (incoming) {
            const avail = incoming.availableStock !== undefined ? Number(incoming.availableStock) : existing.availableStock;
            const safety = incoming.safetyThreshold !== undefined ? Number(incoming.safetyThreshold) : (existing.safetyThreshold || 15);
            const velocity = incoming.dailyVelocity !== undefined ? Number(incoming.dailyVelocity) : (existing.dailyVelocity || 20);
            const runway = Number(((avail / (velocity / 24))).toFixed(1));
            const status = avail <= 0 ? 'Out Of Stock' : avail <= safety ? 'Low Stock' : 'In Stock';

            return {
              ...existing,
              ...incoming,
              sku: existing.sku, // Keep SKU intact
              productName: incoming.productName || existing.productName,
              availableStock: avail,
              safetyThreshold: safety,
              dailyVelocity: velocity,
              runwayHours: isNaN(runway) ? (existing.runwayHours || 36) : runway,
              status: status as any,
              lastChecked: 'Synced from Google Sheet'
            };
          }
          return existing;
        });

        const newStores = parsed.darkStores!.filter((d) => {
          const key = makeKey(d.storeId, d.sku);
          return !prevStores.some((existing) => makeKey(existing.storeId, existing.sku) === key);
        });

        return [...updated, ...newStores];
      });
    }

    // 3. Merge Channel Pricing & MAP non-destructively
    if (parsed.channelPricing && parsed.channelPricing.length > 0) {
      setChannelPricing((prevPricing) => {
        const makeKey = (sku: string, mp: string) =>
          `${(sku || '').trim().toLowerCase()}___${(mp || '').trim().toLowerCase()}`;

        const updated = prevPricing.map((existing) => {
          const incoming = parsed.channelPricing?.find(
            (cp) => makeKey(cp.sku, String(cp.marketplace)) === makeKey(existing.sku, String(existing.marketplace))
          );
          if (incoming) {
            return {
              ...existing,
              ...incoming
            };
          }
          return existing;
        });

        const newPricing = parsed.channelPricing!.filter(
          (cp) => !prevPricing.some((existing) => makeKey(existing.sku, String(existing.marketplace)) === makeKey(cp.sku, String(cp.marketplace)))
        );
        return [...updated, ...newPricing];
      });
    }

    // 4. Merge MAP Breaches non-destructively
    if (parsed.mapBreaches && parsed.mapBreaches.length > 0) {
      setMapBreaches((prevBreaches) => {
        const makeKey = (sku: string, channel: string) =>
          `${(sku || '').trim().toLowerCase()}___${(channel || '').trim().toLowerCase()}`;

        const updated = prevBreaches.map((existing) => {
          const incoming = parsed.mapBreaches?.find(
            (mb) => makeKey(mb.sku, String(mb.channel)) === makeKey(existing.sku, String(existing.channel))
          );
          return incoming ? { ...existing, ...incoming } : existing;
        });

        const newBreaches = parsed.mapBreaches!.filter(
          (mb) => !prevBreaches.some((existing) => makeKey(existing.sku, String(existing.channel)) === makeKey(mb.sku, String(mb.channel)))
        );
        return [...updated, ...newBreaches];
      });
    }

    // 5. Merge Mother Hubs non-destructively (NEVER remove existing allocations)
    if (parsed.motherHubSkuStock && parsed.motherHubSkuStock.length > 0) {
      setMotherHubSkuStock((prevHubs) => {
        const makeKey = (hubId: string, sku: string) =>
          `${(hubId || '').trim().toLowerCase()}___${(sku || '').trim().toLowerCase()}`;

        const updated = prevHubs.map((existing) => {
          const incoming = parsed.motherHubSkuStock?.find(
            (h) => makeKey(h.hubId, h.sku) === makeKey(existing.hubId, existing.sku) ||
              (h.hubName.toLowerCase() === existing.hubName.toLowerCase() && h.sku.toLowerCase() === existing.sku.toLowerCase())
          );
          return incoming ? { ...existing, ...incoming } : existing;
        });

        const newHubs = parsed.motherHubSkuStock!.filter(
          (h) => !prevHubs.some((existing) => makeKey(existing.hubId, existing.sku) === makeKey(h.hubId, h.sku))
        );
        return [...updated, ...newHubs];
      });
    }

    // 6. Merge Manufacturer Supply non-destructively (NEVER remove existing plant records)
    if (parsed.manufacturerSupply && parsed.manufacturerSupply.length > 0) {
      setManufacturerSupply((prevMfg) => {
        const makeKey = (plantName: string, sku: string) =>
          `${(plantName || '').trim().toLowerCase()}___${(sku || '').trim().toLowerCase()}`;

        const updated = prevMfg.map((existing) => {
          const incoming = parsed.manufacturerSupply?.find(
            (m) => makeKey(m.plantName, m.sku) === makeKey(existing.plantName, existing.sku) ||
              (m.id && m.id === existing.id)
          );
          return incoming ? { ...existing, ...incoming } : existing;
        });

        const newMfg = parsed.manufacturerSupply!.filter(
          (m) => !prevMfg.some((existing) => makeKey(existing.plantName, existing.sku) === makeKey(m.plantName, m.sku))
        );
        return [...updated, ...newMfg];
      });
    }

    // 7. Merge Alerts non-destructively
    if (parsed.alerts && parsed.alerts.length > 0) {
      setAlerts((prevAlerts) => {
        const updated = prevAlerts.map((existing) => {
          const incoming = parsed.alerts?.find((a) => a.id === existing.id);
          return incoming ? { ...existing, ...incoming } : existing;
        });

        const newAlerts = parsed.alerts!.filter((a) => !prevAlerts.some((existing) => existing.id === a.id));
        return [...updated, ...newAlerts];
      });
    }
  };

  // Import from Excel / CSV file (Non-destructive)
  const importFromExcel = async (file: File): Promise<{ success: boolean; message: string }> => {
    try {
      setSyncState((prev) => ({ ...prev, syncStatus: 'syncing' }));
      const parsed = await parseUploadedSpreadsheet(file);

      if (!parsed.skus || parsed.skus.length === 0) {
        throw new Error('No valid SKU rows found in the uploaded workbook.');
      }

      applyNonDestructiveIngestion(parsed);

      setSyncState({
        source: 'excel',
        fileName: file.name,
        lastSynced: new Date().toLocaleTimeString(),
        rowCount: parsed.skus.length,
        syncStatus: 'synced'
      });

      return {
        success: true,
        message: `Successfully synchronized ${parsed.skus.length} SKUs, ${(parsed.darkStores || []).length} dark store pods, and connected sheets from ${file.name} without data loss!`
      };
    } catch (err: any) {
      setSyncState((prev) => ({
        ...prev,
        syncStatus: 'error',
        errorMessage: err.message || 'Failed to parse Excel file.'
      }));
      return { success: false, message: err.message || 'Excel import failed.' };
    }
  };

  // Sync live data from Google Sheet URL (Non-destructive intelligent two-way merge)
  const syncFromGoogleSheet = async (url: string): Promise<{ success: boolean; message: string }> => {
    try {
      setSyncState((prev) => ({ ...prev, syncStatus: 'syncing' }));
      const parsed = await fetchPublishedGoogleSheet(url);

      if (!parsed.skus || parsed.skus.length === 0) {
        throw new Error('Google Sheet returned 0 SKU rows. Ensure the spreadsheet is shared as "Anyone with link can view".');
      }

      applyNonDestructiveIngestion(parsed);

      localStorage.setItem('agile_google_sheet_url', url);

      setSyncState({
        source: 'google_sheet',
        googleSheetUrl: url,
        lastSynced: new Date().toLocaleTimeString(),
        rowCount: parsed.skus.length,
        syncStatus: 'synced'
      });

      const sheetsFound = parsed.sheetNames && parsed.sheetNames.length > 0
        ? ` (${parsed.sheetNames.length} tabs: ${parsed.sheetNames.join(', ')})`
        : '';

      return {
        success: true,
        message: `Successfully harmonized ${parsed.skus.length} SKUs and all connected pods from Google Sheet${sheetsFound} — all existing catalog records safely retained!`
      };
    } catch (err: any) {
      setSyncState((prev) => ({
        ...prev,
        syncStatus: 'error',
        errorMessage: err.message || 'Failed to sync Google Sheet.'
      }));
      return { success: false, message: err.message || 'Google Sheet sync failed.' };
    }
  };

  // Reset to original clean defaults
  const resetToDefaults = () => {
    localStorage.removeItem('agile_sleep_skus');
    localStorage.removeItem('agile_sleep_dark_stores');
    localStorage.removeItem('agile_sleep_mother_hub_skus');
    localStorage.removeItem('agile_sleep_manufacturer_supply');
    localStorage.removeItem('agile_sleep_channel_pricing');
    localStorage.removeItem('agile_sleep_map_breaches');
    localStorage.removeItem('agile_sleep_alerts');
    localStorage.removeItem('agile_google_sheet_url');

    setDarkStores(SLEEP_DARK_STORES);
    setSkus(computeSkusWithDarkStores(SLEEP_SKU_CATALOG, SLEEP_DARK_STORES));
    setMotherHubSkuStock(MOTHER_HUB_SKU_DATA);
    setManufacturerSupply(MANUFACTURER_SUPPLY_DATA);
    setChannelPricing(SLEEP_CHANNEL_PRICING);
    setMapBreaches(SLEEP_MAP_BREACHES);
    setAlerts(SLEEP_ALERTS);

    setSyncState({
      source: 'local',
      lastSynced: 'Just now',
      rowCount: SLEEP_SKU_CATALOG.length,
      syncStatus: 'synced'
    });
  };

  return (
    <DataContext.Provider
      value={{
        skus,
        darkStores,
        motherHubs,
        motherHubSkuStock,
        manufacturerSupply,
        channelPricing,
        mapBreaches,
        alerts,
        autonomousActions,
        syncState,
        currentUser,
        setCurrentUser,
        updateSKU,
        updateDarkStore,
        updateMotherHubSkuStock,
        updateManufacturerSupply,
        pushDarkStoreToGoogleSheet,
        pushMotherHubToGoogleSheet,
        pushManufacturerSupplyToGoogleSheet,
        updateAlert,
        pushAlertToGoogleSheet,
        updateChannelPricing,
        pushChannelPricingToGoogleSheet,
        exportToExcel,
        exportTransferLogsToExcel,
        exportAlertsLogToExcel,
        importFromExcel,
        syncFromGoogleSheet,
        pushFullDatasetToGoogleSheet,
        googleSheetWebhookUrl,
        setGoogleSheetWebhookUrl,
        pushToGoogleSheet,
        resetToDefaults,
        triggerStockTransfer,
        transferLogs,
        approveAction,
        rejectAction
      }}
    >
      {children}
    </DataContext.Provider>
  );
};

export const useData = (): DataContextType => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};
