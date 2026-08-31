export type MarketplaceId =
  | 'amazon'
  | 'flipkart'
  | 'myntra'
  | 'blinkit'
  | 'zepto'
  | 'instamart'
  | 'jiomart';

export type ViewMode =
  | 'command-center'
  | 'digital-shelf'
  | 'supply-chain'
  | 'autonomous-ai'
  | 'dataset-sync'
  // Legacy aliases for backwards compatibility
  | 'executive-tower'
  | 'alerts-anomalies'
  | 'dark-stores-supply-chain'
  | 'perishables-expiry'
  | 'sku-360'
  | 'sales-intelligence'
  | 'price-map-intel'
  | 'search-share'
  | 'competitor-watch'
  | 'content-studio'
  | 'reviews-voc'
  | 'advertising-roas'
  | 'returns-quality'
  | 'autonomous-actions'
  | 'ai-agents'
  | 'executive-reports'
  | 'settings-rbac';

export type UserRole =
  | 'Owner'
  | 'Analyst';

export interface UserPersona {
  id: string;
  name: string;
  role: UserRole;
  email: string;
  avatar: string;
  allowedViews: ViewMode[];
  canEditData: boolean;
  canTriggerTransfers: boolean;
  canSendEmails: boolean;
  canManageUsers: boolean;
  canEditPricing: boolean;
}

export interface DatasetSyncState {
  source: 'local' | 'excel' | 'google_sheet';
  lastSynced: string;
  fileName?: string;
  googleSheetUrl?: string;
  rowCount: number;
  syncStatus: 'synced' | 'syncing' | 'error' | 'modified_locally';
  errorMessage?: string;
}

export interface AIAgentStatus {
  id: string;
  name: string;
  category: string;
  description: string;
  status: string;
  frequency: string;
  lastRunTimestamp: string;
  actionsTakenCount: number;
}

export interface VOCFeedback {
  id: string;
  sku: string;
  productName: string;
  channel?: string;
  marketplace?: string;
  rating: number;
  sentiment: string;
  reviewTitle?: string;
  reviewText?: string;
  reviewBody?: string;
  extractedTopic?: string;
  categoryTag?: string;
  customerName?: string;
  date?: string;
  defectReported?: boolean;
  defectCategory?: string;
}

export interface MarketplaceConfig {
  id: MarketplaceId;
  name: string;
  type: 'ecommerce' | 'quick_commerce';
  color: string;
  coverageSkus: number;
  apiLatencyMs: number;
  syncFrequency: string;
  lastSynced: string;
  status: 'Healthy' | 'Delayed' | 'Error';
  webhookActive: boolean;
}

export interface DarkStoreInventory {
  storeId: string;
  storeName: string;
  city: string;
  pincode: string;
  platform: MarketplaceId;
  availableStock: number;
  status: 'In Stock' | 'Low Stock' | 'Out Of Stock';
  deliverySlaMins?: number;
  sellingPrice: number;
  lastChecked?: string;
  motherHubId?: string;
  motherHubName?: string;
  motherHubStock: number;
  transitHoursFromHub?: number;
  sku?: string;
  productName?: string;
  safetyThreshold?: number;
  runwayHours?: number;
  dailyVelocity?: number;
}

export interface MotherHub {
  id: string;
  name: string;
  location: string;
  pincode: string;
  totalCapacity: number;
  currentStockUnits: number;
  coverageDarkStores: number;
  manager: string;
  contactEmail: string;
}

export interface MotherHubSkuStock {
  id: string;
  hubId: string;
  hubName: string;
  city: string;
  pincode: string;
  sku: string;
  productName: string;
  quantityAvailable: number;
  reservedQuantity: number;
  safetyStockThreshold: number;
  bufferHealth: 'Optimal' | 'Adequate' | 'Critical';
  connectedDarkStoresCount: number;
  dispatchSlaHours: number;
}

export interface ManufacturerSupplyInfo {
  id: string;
  manufacturerName: string;
  plantName: string;
  location: string;
  pincode: string;
  sku: string;
  productName: string;
  factoryFinishedGoodsStock: number;
  workInProgressUnits: number;
  monthlyCapacityUnits: number;
  dailyProductionRate: number;
  leadTimeToMotherHubHours: number;
  destinationMotherHub: string;
  activeBatchNumber: string;
  mfgDate: string;
  qualityPassRate: number;
}

export interface BatchPerishableInfo {
  batchNumber: string;
  skuId: string;
  productName: string;
  manufacturerName: string;
  manufacturerPlant: string;
  mfgDate: string;
  expiryDate: string;
  daysRemaining: number;
  shelfLifeHealthPercent: number;
  inventoryUnits: number;
  inventoryValueInr: number;
  status: 'Fresh' | 'Expiring Soon' | 'Critical';
  recommendedAction?: string;
}

export interface SKUListing {
  id: string;
  sku: string;
  name: string;
  category: string;
  subcategory: string;
  brand: string;
  productType?: string;
  material?: string;
  intendedUse?: string;
  mrp: number;
  targetMap: number;
  sellingPrice: number;
  effectiveAsp: number;
  activeMarketplaces: MarketplaceId[] | readonly MarketplaceId[] | string[];
  stockStatus: 'Active' | 'Low Stock' | 'Out Of Stock';
  digitalShelfScore: number;
  shareOfSearchPercent: number;
  rating: number;
  reviewCount: number;
  dailyVelocity: number;
  grossSales30d: number;
  unitsSold30d: number;
  revenueAtRisk: number;
  roas?: number;
  acos?: number;
  tacos?: number;
  adCost30d?: number;
  contentScore: number;
  imageGalleryCount: number;
  hasAplus: boolean;
  bulletPointsCount: number;
  manufacturerName: string;
  manufacturerPlant: string;
  defaultMotherHub: string;
  darkStoreStock: number;
  motherHubStock: number;
  batches: BatchPerishableInfo[];
  marketplacePrices: Record<MarketplaceId, {
    price: number;
    inStock: boolean;
    shareOfSearch: number;
    revenue30d: number;
    buyBoxOwner?: string;
  }>;
}

export interface ChannelPricingItem {
  id: string;
  sku: string;
  productName: string;
  marketplace: MarketplaceId | string;
  currentSellingPrice: number;
  targetMap: number;
  mapBreached: boolean;
  priceDelta: number;
  inStock: boolean;
  buyBoxOwner: string;
  shareOfSearch: number;
  revenue30d: number;
  status: 'Active Breach' | 'Compliant' | 'Investigating' | 'Resolved' | 'Actioned';
  complianceAction?: string;
}

export interface MAPBreach {
  id: string;
  sku: string;
  productName: string;
  channel: MarketplaceId;
  violatingSeller: string;
  enforcedMap: number;
  violatedPrice: number;
  discountPercent: number;
  breachDurationHours: number;
  status: 'Active Breach' | 'Investigating' | 'Resolved' | 'Actioned';
  evidenceUrl?: string;
  complianceAction?: string;
  estimatedLossInr?: number;
  priceGapInr?: number;
  sellerName?: string;
  suggestedPlaybook?: string;
}

export interface SearchKeywordItem {
  id: string;
  keyword: string;
  category: string;
  marketplace: MarketplaceId;
  searchVolume: number;
  organicRank: number;
  sponsoredRank: number;
  shareOfSearch: number;
  topCompetitor: string;
  matchedSku: string;
  rankChange7d: number;
}

export interface CompetitorMove {
  id: string;
  competitorName: string;
  type: 'Price Drop' | 'Flash Sale' | 'Quick Commerce Promo' | 'New Launch' | 'OOS Defect';
  timeAgo: string;
  threatLevel: 'Critical' | 'High' | 'Medium' | 'Low';
  description: string;
  matchedSku: string;
  oldPrice: number;
  newPrice: number;
  estimatedImpactInr: number;
  recommendedPlaybook: string;
}

export interface ReviewVOC {
  id: string;
  sku: string;
  productName: string;
  marketplace: MarketplaceId;
  reviewerName: string;
  rating: number;
  date: string;
  verifiedPurchase: boolean;
  sentiment: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';
  title: string;
  body: string;
  extractedTopic: string;
  defectCategory?: string;
}

export interface AdCampaign {
  id: string;
  name: string;
  marketplace: MarketplaceId;
  type: 'Sponsored Products' | 'Sponsored Brands' | 'Quick Commerce Boost';
  spend30d: number;
  attributedSales30d: number;
  roas: number;
  acosPercent: number;
  status: 'Active' | 'Paused';
}

export interface ReturnRecord {
  id: string;
  orderId: string;
  sku: string;
  productName: string;
  marketplace: MarketplaceId;
  returnReason: string;
  batchNumber: string;
  warehouseHub: string;
  refundAmount: number;
  returnDate: string;
}

export interface AlertAnomaly {
  id: string;
  sku: string;
  productName: string;
  marketplace: MarketplaceId;
  severity: 'Critical' | 'High' | 'Medium';
  status: 'New' | 'Investigating' | 'Acknowledged' | 'Resolved';
  timestamp: string;
  timeDisplay: string;
  summary: string;
  revenueAtRiskInr: number;
  manufacturerName: string;
  manufacturerPlant: string;
  darkStoreStock: number;
  motherHubName: string;
  motherHubStock: number;
  motherHubPincode: string;
  batchNumber: string;
  mfgDate: string;
  expiryDate: string;
  shelfLifeHealth: number;
  transferLeadTimeHours: number;
  recommendedPlaybook: string;
  transferUnitsSuggested: number;
  logisticsPartner: string;
  targetOwnerEmail: string;
  followUpSent?: boolean;
}

export interface AutonomousAction {
  id: string;
  actionCode?: string;
  title: string;
  description: string;
  channel?: MarketplaceId;
  marketplace?: MarketplaceId | string;
  category?: string;
  agentName?: string;
  agentOwner?: string;
  targetSku?: string;
  sku?: string;
  status: 'Pending Approval' | 'Approved' | 'Executed' | 'Rolled Back' | 'Rejected';
  createdAt?: string;
  stagedAt?: string;
  projectedRoiInr?: number;
  confidencePercent?: number;
  confidenceScore?: number;
  estimatedValueRecoveredInr?: number;
  estimatedRevenueImpactInr?: number;
  approvalRequired?: boolean;
  approvedBy?: string;
  executedAt?: string;
  executionResult?: string;
  executionStatus?: string;
  safetyGuardrail?: string;
  guardrailsCheck?: string;
  playbookType?: string;
  triggerAlertId?: string;
  transferDetails?: {
    fromMotherHub: string;
    targetDarkStore: string;
    units: number;
  };
}

export interface AIAgentInfo {
  id: string;
  name: string;
  category: string;
  description: string;
  status: 'Active' | 'Idle' | 'Paused' | 'Error';
  frequency: string;
  lastRun: string;
  accuracyPercent: number;
  recordsProcessedToday: number;
  issuesDetected: number;
  lastFinding: string;
}

export interface ExecutiveReport {
  id: string;
  title: string;
  period: string;
  generatedDate: string;
  type: 'WBR' | 'Digital Shelf' | 'Price Intel' | 'Quick Commerce OOS' | 'VOC Sentiment';
  author: string;
  targetEmail: string;
  executiveSummary: string;
  strategicObservations: string[];
  revenueSummary: {
    grossSalesInr: number;
    growthPercent: number;
    quickCommerceSharePercent: number;
    revenueAtRiskInr: number;
    recoveredRevenueInr: number;
  };
  dispatchedAt?: string;
  scheduledCron?: string;
}

export interface StockTransferLog {
  id: string;
  timestamp: string;
  sku: string;
  productName: string;
  sourceMotherHub: string;
  targetDarkStore: string;
  unitsTransferred: number;
  carrier: string;
  trackingNumber: string;
  status: string;
  executedBy: string;
}

export interface EmailDispatchLog {
  id: string;
  recipientEmail: string;
  senderEmail: string;
  subject: string;
  reportType: string;
  sentAt: string;
  deliveryStatus: 'Delivered' | 'Scheduled' | 'Failed';
  summaryPreview: string;
  followUpActionsCount: number;
}
