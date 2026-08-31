/**
 * Sleepsia Commerce Intelligence Platform - Type Definitions
 * Covers Unified Commerce Data Model, KPIs, Multi-Agent Architecture, Reports & Settings
 */

export type MarketplaceChannel =
  | 'Amazon'
  | 'Flipkart'
  | 'Blinkit'
  | 'Instamart'
  | 'Myntra'
  | 'FirstCry'
  | 'Nykaa'
  | 'Meesho'
  | 'JioMart'
  | 'Pepperfry'
  | 'Sleepbee'
  | 'Tata 1mg'
  | 'MyStore'
  | 'MyStore / ONDC'
  | 'ZOOZLE'
  | 'Zoozle'
  | 'D2C'
  | 'D2C / Sleepsia Website';

export type ProductCategory =
  | 'Sleeping Pillows'
  | 'Memory Foam Pillows'
  | 'Orthopedic & Cervical Pillows'
  | 'Microfiber Pillows'
  | 'Pregnancy & Body Pillows'
  | 'Kids & Baby Pillows'
  | 'Travel & Car Comfort'
  | 'Travel & Car Comfort Products'
  | 'Back Support & Seat Cushions'
  | 'Pillow Covers & Protectors'
  | 'Bedding Products'
  | 'Pet Products'
  | 'Wellness & Home'
  | 'Wellness & Home Products'
  | 'Speciality Pillows'
  | string;

export interface ProductMaster {
  sku: string;
  productId: string;
  productName: string;
  category: ProductCategory;
  brand: string;
  variant: string;
  size: string;
  material: string;
  colour: string;
  eanGtin: string;
  productLifecycle: 'Launch' | 'Growth' | 'Mature' | 'Declining' | 'Active';
  mrp: number;
  standardCost: number;
}

export interface MarketplaceMaster {
  platform: MarketplaceChannel;
  platformType: 'General E-Commerce' | 'Quick Commerce' | 'Vertical / Niche' | 'D2C Brand Site' | 'Government / ONDC';
  commissionRate: number; // e.g. 0.15 for 15%
  settlementDays: number;
  returnWindowDays: number;
  activeStatus: boolean;
}

export interface InternalSalesRecord {
  orderId: string;
  date: string; // YYYY-MM-DD
  channel: MarketplaceChannel;
  sku: string;
  productName: string;
  units: number;
  grossSales: number;
  discounts: number;
  netSales: number;
  returnUnits?: number;
  return_units?: number;
  returns: number;
  cancellations: number;
  netRealizedRevenue: number;
  customerId?: string;
  state?: string;
}

export interface MarketplaceRecord {
  platform: MarketplaceChannel;
  date: string;
  sku: string;
  marketplaceProductId: string;
  price: number;
  mrp: number;
  discount: number;
  availability: 'In Stock' | 'Low Stock' | 'Out of Stock';
  inventory: number;
  orders: number;
  unitsSold: number;
  gmv: number;
  returns: number;
  cancellations: number;
  marketplaceFees: number;
  settlement: number;
  rating: number;
  reviewCount: number;
  productContentScore: number; // 0 - 100
  organicSearchPosition: number;
  sponsoredSearchPosition: number;
  categoryPosition: number;
  promotion?: string;
}

export interface AdvertisingRecord {
  date: string;
  platform: MarketplaceChannel;
  campaignId: string;
  campaignName: string;
  campaignType: 'Sponsored Products' | 'Sponsored Brands' | 'Display' | 'Search Ads' | 'Performance Max';
  status: 'ENABLED' | 'PAUSED' | 'ARCHIVED';
  sku: string;
  productId: string;
  impressions: number;
  clicks: number;
  spend: number;
  orders: number;
  units: number;
  attributedRevenue: number;
  ctr: number;
  cpc: number;
  roas: number;
  acos: number;
}

export interface InventoryRecord {
  date: string;
  sku: string;
  motherWarehouse?: string;
  warehouse: string;
  darkstore?: string;
  darkstoreId?: string;
  openingStock?: number;
  availableStock?: number;
  availableInventory: number;
  closingStock: number;
  reservedStock: number;
  inboundStock: number;
  damagedStock: number;
  daysOfInventory: number;
  stockoutRisk: 'Low' | 'Medium' | 'High' | 'Critical';
}

export interface CostRecord {
  sku: string;
  date: string;
  cogs: number;
  manufacturingCost: number;
  packaging: number;
  freight: number;
  warehouseCost: number;
  marketplaceFees: number;
  paymentFees: number;
  returnsCost: number;
  otherVariableCosts: number;
}

export interface CustomerRecord {
  customerId: string;
  name: string;
  city: string;
  state: string;
  segment: 'New' | 'Loyal' | 'At Risk' | 'VIP';
  repeatCustomer: boolean;
  totalOrders: number;
  lifetimeValue: number;
  feedbackScore: number;
}

export interface FinanceRecord {
  date: string;
  channel: MarketplaceChannel;
  grossRevenue: number;
  netRevenue: number;
  totalCogs: number;
  adSpend: number;
  marketplaceCommission: number;
  shippingCost: number;
  paymentGatewayFee: number;
  operatingExpense: number;
  netProfit: number;
  ebitdaMargin: number;
}

export interface CompetitorRecord {
  date: string;
  category: ProductCategory;
  competitorBrand: string;
  competitorProductName: string;
  competitorPrice: number;
  sleepsiaTargetSku: string;
  discountPercent: number;
  rating: number;
  reviewCount: number;
  availability: 'In Stock' | 'Out of Stock' | 'Limited';
  searchPosition: number;
  activePromotion: string;
  threatLevel: 'Low' | 'Medium' | 'High' | 'Severe';
}

export interface ShippingRecord {
  orderId: string;
  date: string;
  platform: MarketplaceChannel;
  sku: string;
  warehouse: string;
  carrier: 'BlueDart' | 'Delhivery' | 'Ecom Express' | 'Shadowfax' | 'Xpressbees' | 'Amazon ATS' | 'Ekart';
  orderDate: string;
  shipDate: string;
  expectedDeliveryDate: string;
  actualDeliveryDate?: string;
  shipmentStatus: 'Delivered' | 'In Transit' | 'Out for Delivery' | 'Delayed' | 'RTO' | 'Lost';
  deliveryStatus: 'On-Time' | 'Delayed' | 'Pending' | 'Failed';
  shippingCost: number;
  delayReason?: string;
  delayDays: number;
}

export interface SleepsiaWorkbookData {
  products: ProductMaster[];
  marketplaceMasters: MarketplaceMaster[];
  sales: InternalSalesRecord[];
  marketplaceData: MarketplaceRecord[];
  advertising: AdvertisingRecord[];
  inventory: InventoryRecord[];
  costs: CostRecord[];
  customers: CustomerRecord[];
  finance: FinanceRecord[];
  competitors: CompetitorRecord[];
  shipping: ShippingRecord[];
  metadata: {
    loadedAt: string;
    totalOrders: number;
    dateRange: { start: string; end: string };
    totalSkus: number;
    activeChannels: number;
    sourceFileName: string;
  };
}

export interface CalculatedKPIs {
  sales: {
    totalRevenue: number;
    netRevenue: number;
    gmv: number;
    unitsSold: number;
    totalOrders: number;
    aov: number; // Average Order Value
    growthPercent: number; // vs previous period
    returnRate: number; // %
    cancellationRate: number; // %
  };
  profitability: {
    totalCogs: number;
    grossMarginPercent: number;
    contributionMargin: number;
    netProfit: number;
    profitMarginPercent: number;
    profitPerSku: { sku: string; productName: string; profit: number; marginPercent: number }[];
    profitPerMarketplace: { platform: MarketplaceChannel; profit: number; marginPercent: number }[];
  };
  advertising: {
    totalSpend: number;
    impressions: number;
    clicks: number;
    ctr: number;
    cpc: number;
    attributedRevenue: number;
    roas: number;
    acos: number;
    tacos: number; // Total ACoS = Ad Spend / Total Net Revenue
    hasSufficientData: boolean;
  };
  paidVsOrganic: {
    totalSales: number;
    adAttributedSales: number;
    organicSales: number;
    adSpend: number;
    paidContributionPercent: number;
    organicContributionPercent: number;
    roas: number;
    tacos: number;
    notes: string;
    incrementalConfidence: 'High' | 'Medium' | 'Low' | 'Insufficient source data for exact calculation.';
  };
  inventory: {
    totalAvailableStock: number;
    totalClosingStock: number;
    totalReservedStock: number;
    totalInboundStock: number;
    totalDamagedStock: number;
    averageDaysOfInventory: number;
    highRiskSkusCount: number;
    stockoutRiskList: { sku: string; productName: string; daysLeft: number; risk: string; warehouse: string }[];
  };
  shipping: {
    totalShipments: number;
    deliveredOrders: number;
    delayedOrders: number;
    failedShipments: number;
    onTimeDeliveryRate: number; // %
    lateDeliveryRate: number; // %
    totalShippingCost: number;
    averageShippingCost: number;
    averageDelayDays: number;
    carrierPerformance: {
      carrier: string;
      total: number;
      totalOrders?: number;
      onTimeRate: number;
      avgCost: number;
      totalCost?: number;
      avgTransitDays?: number;
      delayedCount: number;
    }[];
    warehousePerformance: { warehouse: string; total: number; onTimeRate: number; avgDispatchTime: number }[];
    platformPerformance: { platform: MarketplaceChannel; onTimeRate: number; delayedCount: number }[];
  };
  competitor: {
    avgCompetitorPrice: number;
    sleepsiaAvgPrice: number;
    priceGapPercent: number;
    avgCompetitorDiscount: number;
    sleepsiaAvgDiscount: number;
    ratingGap: number;
    reviewGap: number;
    topThreats: { competitor: string; category: string; priceGap: number; promo: string; threatLevel: string }[];
  };
}

export interface AgentStructuredFinding {
  id: string;
  metric: string;
  current_value: number | string;
  previous_value: number | string;
  change_percent: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  finding: string;
  possible_causes: string[];
  recommended_action: string;
  priority: 'P0 - Immediate' | 'P1 - Urgent' | 'P2 - High' | 'P3 - Medium';
  area: 'Sales' | 'Advertising' | 'Competitor' | 'Inventory' | 'Shipping' | 'Profitability';
  confidence: number; // 0 - 1
  expected_business_impact?: string;
  source: string[]; // e.g. ['Marketplace_Data', 'Advertising_Data']
  agent: 'Supervisor' | 'Sales' | 'Advertising' | 'Competitor' | 'Inventory & Shipping' | 'Executive Reporting';
  feedback?: 'thumbs_up' | 'thumbs_down' | null;
  feedbackNote?: string;
}

export interface ExecutiveReportData {
  reportDate: string;
  generatedAt: string;
  executiveSummary: string;
  kpis: {
    revenue: number;
    revenueGrowth: number;
    profit: number;
    profitMargin: number;
    orders: number;
    units: number;
    adSpend: number;
    roas: number;
    organicSalesPercent: number;
    inventoryRiskCount: number;
    onTimeDeliveryPercent: number;
  };
  topWins: string[];
  topRisks: string[];
  majorProductChanges: {
    growing: { sku: string; name: string; growth: number; revenue: number }[];
    declining: { sku: string; name: string; decline: number; revenue: number }[];
  };
  marketplaceRankings: {
    platform: MarketplaceChannel;
    revenue: number;
    growth: number;
    profit: number;
    orders: number;
  }[];
  advertisingSummary: {
    bestCampaigns: { name: string; platform: string; roas: number; revenue: number }[];
    worstCampaigns: { name: string; platform: string; roas: number; spend: number }[];
    tacos: number;
    paidVsOrganicNote: string;
  };
  shippingSummary: {
    onTimeRate: number;
    delayedOrders: number;
    failedShipments: number;
    worstCarrier: string;
    worstWarehouse: string;
  };
  competitiveSummary: {
    priceThreatCount: number;
    keyObservations: string[];
  };
  recommendedActions: {
    priority: 'P0' | 'P1' | 'P2' | 'P3';
    area: string;
    recommendation: string;
    reason: string;
    expectedImpact: string;
  }[];
}

export interface EmailScheduleJob {
  id: string;
  name: string;
  recipients: string[];
  ccRecipients: string[];
  reportTime: string; // e.g. "09:00"
  timezone: string; // e.g. "Asia/Kolkata"
  frequency: 'Daily' | 'Weekdays' | 'Weekly' | 'Hourly';
  weeklyDay?: 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday';
  enabled: boolean;
  subjectTemplate?: string;
  includeVisualAttachment: boolean;
  includeAnomalyAlerts: boolean;
  includeKpiSummary: boolean;
  includeStockoutRisks: boolean;
  createdDate: string;
  lastRunTimestamp?: string;
  lastRunStatus?: 'Success' | 'Failed' | 'Running';
  lastRunMessage?: string;
  lastMessageId?: string;
  lastPreviewUrl?: string;
  nextRunEstimated?: string;
}

export interface EmailSettings {
  recipients: string[];
  ccRecipients: string[];
  reportTime: string; // e.g. "09:00"
  timezone: string; // e.g. "Asia/Kolkata"
  frequency: 'Daily' | 'Weekdays' | 'Weekly';
  autoSendEnabled: boolean;
  schedules?: EmailScheduleJob[];
  lastSentTimestamp?: string;
  lastSentStatus?: 'Success' | 'Failed' | 'Pending';
  lastSentMessage?: string;
  lastMessageId?: string;
  lastPreviewUrl?: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'agent' | 'system';
  content: string;
  sources?: string[];
  timestamp: string;
  structuredCard?: AgentStructuredFinding;
}
