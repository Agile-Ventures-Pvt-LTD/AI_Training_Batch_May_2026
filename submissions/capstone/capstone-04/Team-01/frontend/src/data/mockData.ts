import {
  SKUListing,
  MarketplaceConfig,
  DarkStoreInventory,
  MotherHub,
  BatchPerishableInfo,
  MAPBreach,
  SearchKeywordItem,
  CompetitorMove,
  ReviewVOC,
  AdCampaign,
  ReturnRecord,
  AlertAnomaly,
  AutonomousAction,
  AIAgentInfo,
  ExecutiveReport,
  EmailDispatchLog
} from '../types';

export const OWNER_EMAIL = 'vikashr984@gmail.com';
export const SENDER_GMAIL = 'vikashr984@gmail.com';

// Format INR helpers (Guarantees zero NaN / undefined)
export function formatINR(val: number | undefined | null, options?: { abbreviate?: boolean }): string {
  if (val === undefined || val === null || isNaN(val)) return '₹0';
  const num = Number(val);
  if (options?.abbreviate) {
    if (Math.abs(num) >= 10000000) {
      return `₹${(num / 10000000).toFixed(2)}Cr`;
    }
    if (Math.abs(num) >= 100000) {
      return `₹${(num / 100000).toFixed(2)}L`;
    }
    if (Math.abs(num) >= 1000) {
      return `₹${(num / 1000).toFixed(1)}k`;
    }
    return `₹${num.toLocaleString('en-IN')}`;
  }
  return `₹${num.toLocaleString('en-IN')}`;
}

export function formatPercent(val: number | undefined | null): string {
  if (val === undefined || val === null || isNaN(val)) return '0.0%';
  const prefix = val > 0 ? '+' : '';
  return `${prefix}${val.toFixed(1)}%`;
}

export const MARKETPLACE_CONFIGS: MarketplaceConfig[] = [
  {
    id: 'amazon',
    name: 'Amazon India',
    type: 'ecommerce',
    color: '#f59e0b',
    coverageSkus: 94,
    apiLatencyMs: 142,
    syncFrequency: 'Every 15 min',
    lastSynced: '4 mins ago',
    status: 'Healthy',
    webhookActive: true
  },
  {
    id: 'flipkart',
    name: 'Flipkart',
    type: 'ecommerce',
    color: '#3b82f6',
    coverageSkus: 88,
    apiLatencyMs: 198,
    syncFrequency: 'Every 15 min',
    lastSynced: '12 mins ago',
    status: 'Healthy',
    webhookActive: true
  },
  {
    id: 'myntra',
    name: 'Myntra',
    type: 'ecommerce',
    color: '#ec4899',
    coverageSkus: 52,
    apiLatencyMs: 420,
    syncFrequency: 'Every 15 min',
    lastSynced: '1.8 hrs ago',
    status: 'Delayed',
    webhookActive: false
  },
  {
    id: 'blinkit',
    name: 'Blinkit',
    type: 'quick_commerce',
    color: '#eab308',
    coverageSkus: 76,
    apiLatencyMs: 110,
    syncFrequency: 'Every 15 min',
    lastSynced: '2 mins ago',
    status: 'Healthy',
    webhookActive: true
  },
  {
    id: 'zepto',
    name: 'Zepto',
    type: 'quick_commerce',
    color: '#a855f7',
    coverageSkus: 68,
    apiLatencyMs: 128,
    syncFrequency: 'Every 15 min',
    lastSynced: '6 mins ago',
    status: 'Healthy',
    webhookActive: true
  },
  {
    id: 'instamart',
    name: 'Swiggy Instamart',
    type: 'quick_commerce',
    color: '#f97316',
    coverageSkus: 72,
    apiLatencyMs: 155,
    syncFrequency: 'Every 15 min',
    lastSynced: '9 mins ago',
    status: 'Healthy',
    webhookActive: true
  },
  {
    id: 'jiomart',
    name: 'JioMart',
    type: 'quick_commerce',
    color: '#06b6d4',
    coverageSkus: 64,
    apiLatencyMs: 210,
    syncFrequency: 'Every 30 min',
    lastSynced: '14 mins ago',
    status: 'Healthy',
    webhookActive: true
  }
];

export const MOTHER_HUBS: MotherHub[] = [
  {
    id: 'HUB-BLR-01',
    name: 'Bengaluru Central Mother Hub (Nelamangala)',
    location: 'Nelamangala, Bengaluru, Karnataka',
    pincode: '562123',
    totalCapacity: 250000,
    currentStockUnits: 184500,
    coverageDarkStores: 24,
    manager: 'Arunachalam V.',
    contactEmail: 'blr-hub.ops@agileventures.net'
  },
  {
    id: 'HUB-BOM-02',
    name: 'Bhiwandi Central Logistics Mother Hub',
    location: 'Bhiwandi Industrial Complex, Thane, Maharashtra',
    pincode: '421302',
    totalCapacity: 350000,
    currentStockUnits: 290000,
    coverageDarkStores: 32,
    manager: 'Rajesh Sawant',
    contactEmail: 'bhiwandi.logistics@agileventures.net'
  },
  {
    id: 'HUB-DEL-03',
    name: 'Bilaspur Super Hub (Gurgaon Logistics Corridor)',
    location: 'Bilaspur, NH-48, Gurugram, Haryana',
    pincode: '122413',
    totalCapacity: 400000,
    currentStockUnits: 310500,
    coverageDarkStores: 28,
    manager: 'Harpreet Singh',
    contactEmail: 'gurgaon.motherhub@agileventures.net'
  },
  {
    id: 'HUB-HYD-04',
    name: 'Shamshabad Airport Multi-Modal Mother Hub',
    location: 'Shamshabad Logistics Park, Hyderabad, Telangana',
    pincode: '501218',
    totalCapacity: 180000,
    currentStockUnits: 135000,
    coverageDarkStores: 16,
    manager: 'Kalyan Rao',
    contactEmail: 'hyd-hub.dispatch@agileventures.net'
  }
];

export const HERO_SKUS: SKUListing[] = [
  {
    id: 'sku-001',
    sku: 'SKU-SC-001',
    name: 'Sleepsia Orthopedic Memory Foam Pillow',
    category: 'Sleep & Comfort',
    subcategory: 'Pillows',
    brand: 'Sleepsia',
    mrp: 699,
    targetMap: 599,
    sellingPrice: 599,
    effectiveAsp: 579,
    activeMarketplaces: ['amazon', 'flipkart', 'myntra', 'blinkit', 'zepto', 'instamart', 'jiomart'],
    stockStatus: 'Active',
    digitalShelfScore: 78,
    shareOfSearchPercent: 18.4,
    rating: 4.3,
    reviewCount: 2450,
    dailyVelocity: 160,
    grossSales30d: 2840000,
    unitsSold30d: 4800,
    revenueAtRisk: 420000,
    contentScore: 78,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
    manufacturerPlant: 'Plant #2, Baddi Industrial Area, Solan (HP) - 173205',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala, Pincode: 562123)',
    darkStoreStock: 1420,
    motherHubStock: 10350,
    batches: [
      {
        batchNumber: 'BAT-2026-088C',
        skuId: 'sku-001',
        productName: 'SkinScience Vitamin C 10% Face Glow Serum (30ml)',
        manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
        manufacturerPlant: 'Plant #2, Baddi, HP',
        mfgDate: '2026-04-12',
        expiryDate: '2028-04-28',
        daysRemaining: 618,
        shelfLifeHealthPercent: 94,
        inventoryUnits: 8400,
        inventoryValueInr: 5031600,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 599, inStock: true, shareOfSearch: 18.4, revenue30d: 1120000, buyBoxOwner: 'SkinScience Official' },
      flipkart: { price: 599, inStock: true, shareOfSearch: 16.2, revenue30d: 780000, buyBoxOwner: 'SkinScience Official' },
      myntra: { price: 599, inStock: true, shareOfSearch: 14.0, revenue30d: 310000, buyBoxOwner: 'SkinScience Direct' },
      blinkit: { price: 599, inStock: true, shareOfSearch: 22.5, revenue30d: 340000, buyBoxOwner: 'QuickCommerce Partner' },
      zepto: { price: 599, inStock: true, shareOfSearch: 19.8, revenue30d: 190000, buyBoxOwner: 'Zepto Retail' },
      instamart: { price: 599, inStock: true, shareOfSearch: 18.0, revenue30d: 100000, buyBoxOwner: 'Swiggy Instamart' },
      jiomart: { price: 599, inStock: true, shareOfSearch: 15.0, revenue30d: 0, buyBoxOwner: 'Reliance Retail' }
    }
  },
  {
    id: 'sku-002',
    sku: 'SKU-SC-002',
    name: 'SkinScience Niacinamide 10% + Zinc Daily Blemish Serum (30ml)',
    category: 'Skincare & Beauty',
    subcategory: 'Face Serums',
    brand: 'SkinScience Lab',
    mrp: 599,
    targetMap: 499,
    sellingPrice: 499,
    effectiveAsp: 499,
    activeMarketplaces: ['amazon', 'flipkart', 'myntra', 'blinkit', 'zepto', 'instamart'],
    stockStatus: 'Active',
    digitalShelfScore: 92,
    shareOfSearchPercent: 24.1,
    rating: 4.5,
    reviewCount: 1980,
    dailyVelocity: 147,
    grossSales30d: 2150000,
    unitsSold30d: 4400,
    revenueAtRisk: 0,
    contentScore: 92,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
    manufacturerPlant: 'Plant #2, Baddi Industrial Area, Solan (HP)',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 1890,
    motherHubStock: 8200,
    batches: [
      {
        batchNumber: 'BAT-2026-104A',
        skuId: 'sku-002',
        productName: 'SkinScience Niacinamide 10% + Zinc Daily Blemish Serum',
        manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
        manufacturerPlant: 'Plant #2, Baddi, HP',
        mfgDate: '2026-05-10',
        expiryDate: '2028-05-09',
        daysRemaining: 629,
        shelfLifeHealthPercent: 96,
        inventoryUnits: 6500,
        inventoryValueInr: 3243500,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 499, inStock: true, shareOfSearch: 24.1, revenue30d: 890000 },
      flipkart: { price: 499, inStock: true, shareOfSearch: 22.0, revenue30d: 580000 },
      myntra: { price: 499, inStock: true, shareOfSearch: 20.5, revenue30d: 320000 },
      blinkit: { price: 499, inStock: true, shareOfSearch: 26.0, revenue30d: 210000 },
      zepto: { price: 499, inStock: true, shareOfSearch: 25.0, revenue30d: 150000 },
      instamart: { price: 499, inStock: true, shareOfSearch: 21.0, revenue30d: 0 },
      jiomart: { price: 499, inStock: true, shareOfSearch: 18.0, revenue30d: 0 }
    }
  },
  {
    id: 'sku-003',
    sku: 'SKU-SC-003',
    name: 'SkinScience Ultra Hydrating Hyaluronic Acid Gel (50g)',
    category: 'Skincare & Beauty',
    subcategory: 'Moisturizers',
    brand: 'SkinScience Lab',
    mrp: 499,
    targetMap: 420,
    sellingPrice: 420,
    effectiveAsp: 420,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto'],
    stockStatus: 'Low Stock',
    digitalShelfScore: 64,
    shareOfSearchPercent: 12.0,
    rating: 4.2,
    reviewCount: 1120,
    dailyVelocity: 107,
    grossSales30d: 1350000,
    unitsSold30d: 3200,
    revenueAtRisk: 310000,
    contentScore: 64,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
    manufacturerPlant: 'Plant #2, Baddi Industrial Area, Solan (HP)',
    defaultMotherHub: 'Bilaspur Super Hub (Gurgaon)',
    darkStoreStock: 120,
    motherHubStock: 4800,
    batches: [
      {
        batchNumber: 'BAT-2026-092G',
        skuId: 'sku-003',
        productName: 'SkinScience Ultra Hydrating Hyaluronic Acid Gel',
        manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
        manufacturerPlant: 'Plant #2, Baddi, HP',
        mfgDate: '2026-03-20',
        expiryDate: '2027-09-19',
        daysRemaining: 397,
        shelfLifeHealthPercent: 72,
        inventoryUnits: 3200,
        inventoryValueInr: 1344000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 420, inStock: true, shareOfSearch: 12.0, revenue30d: 590000 },
      flipkart: { price: 420, inStock: true, shareOfSearch: 11.5, revenue30d: 390000 },
      myntra: { price: 420, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      blinkit: { price: 420, inStock: false, shareOfSearch: 8.0, revenue30d: 180000 },
      zepto: { price: 420, inStock: true, shareOfSearch: 14.0, revenue30d: 190000 },
      instamart: { price: 420, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      jiomart: { price: 420, inStock: false, shareOfSearch: 0, revenue30d: 0 }
    }
  },
  {
    id: 'sku-004',
    sku: 'SKU-SC-004',
    name: 'SkinScience Mineral Matte Sunscreen SPF 50 PA++++ (50g)',
    category: 'Skincare & Beauty',
    subcategory: 'Sun Protection',
    brand: 'SkinScience Lab',
    mrp: 649,
    targetMap: 549,
    sellingPrice: 549,
    effectiveAsp: 549,
    activeMarketplaces: ['amazon', 'flipkart', 'myntra', 'blinkit', 'zepto', 'instamart', 'jiomart'],
    stockStatus: 'Active',
    digitalShelfScore: 96,
    shareOfSearchPercent: 32.5,
    rating: 4.6,
    reviewCount: 3820,
    dailyVelocity: 240,
    grossSales30d: 3890000,
    unitsSold30d: 7200,
    revenueAtRisk: 0,
    contentScore: 96,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
    manufacturerPlant: 'Plant #2, Baddi Industrial Area, Solan (HP)',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 2400,
    motherHubStock: 14200,
    batches: [
      {
        batchNumber: 'BAT-2026-118M',
        skuId: 'sku-004',
        productName: 'SkinScience Mineral Matte Sunscreen SPF 50',
        manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
        manufacturerPlant: 'Plant #2, Baddi, HP',
        mfgDate: '2026-06-01',
        expiryDate: '2028-05-31',
        daysRemaining: 651,
        shelfLifeHealthPercent: 98,
        inventoryUnits: 12000,
        inventoryValueInr: 6588000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 549, inStock: true, shareOfSearch: 32.5, revenue30d: 1650000 },
      flipkart: { price: 549, inStock: true, shareOfSearch: 29.0, revenue30d: 980000 },
      myntra: { price: 549, inStock: true, shareOfSearch: 28.0, revenue30d: 480000 },
      blinkit: { price: 549, inStock: true, shareOfSearch: 38.0, revenue30d: 420000 },
      zepto: { price: 549, inStock: true, shareOfSearch: 34.0, revenue30d: 240000 },
      instamart: { price: 549, inStock: true, shareOfSearch: 30.0, revenue30d: 120000 },
      jiomart: { price: 549, inStock: true, shareOfSearch: 25.0, revenue30d: 0 }
    }
  },
  {
    id: 'sku-005',
    sku: 'SKU-SC-005',
    name: 'SkinScience Salicylic Acid 2% Deep Pore Cleanser (150ml)',
    category: 'Skincare & Beauty',
    subcategory: 'Face Wash',
    brand: 'SkinScience Lab',
    mrp: 399,
    targetMap: 349,
    sellingPrice: 349,
    effectiveAsp: 349,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto'],
    stockStatus: 'Out Of Stock',
    digitalShelfScore: 45,
    shareOfSearchPercent: 6.8,
    rating: 4.1,
    reviewCount: 890,
    dailyVelocity: 93,
    grossSales30d: 980000,
    unitsSold30d: 2800,
    revenueAtRisk: 680000,
    contentScore: 45,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
    manufacturerPlant: 'Plant #2, Baddi Industrial Area, Solan (HP)',
    defaultMotherHub: 'Bhiwandi Central Logistics Mother Hub',
    darkStoreStock: 0,
    motherHubStock: 3450,
    batches: [
      {
        batchNumber: 'BAT-2026-077B',
        skuId: 'sku-005',
        productName: 'SkinScience Salicylic Acid 2% Deep Pore Cleanser',
        manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
        manufacturerPlant: 'Plant #2, Baddi, HP',
        mfgDate: '2026-02-14',
        expiryDate: '2028-02-13',
        daysRemaining: 544,
        shelfLifeHealthPercent: 88,
        inventoryUnits: 3450,
        inventoryValueInr: 1204050,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 349, inStock: false, shareOfSearch: 6.8, revenue30d: 410000 },
      flipkart: { price: 349, inStock: false, shareOfSearch: 5.2, revenue30d: 290000 },
      myntra: { price: 349, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      blinkit: { price: 349, inStock: false, shareOfSearch: 0, revenue30d: 160000 },
      zepto: { price: 349, inStock: false, shareOfSearch: 0, revenue30d: 120000 },
      instamart: { price: 349, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      jiomart: { price: 349, inStock: false, shareOfSearch: 0, revenue30d: 0 }
    }
  },
  {
    id: 'sku-101',
    sku: 'SKU-AK-101',
    name: 'AudioKraft Pro Bass ANC Wireless Earbuds (50Hr Playtime)',
    category: 'Audio & Wearables',
    subcategory: 'TWS Earbuds',
    brand: 'AudioKraft',
    mrp: 2999,
    targetMap: 1699,
    sellingPrice: 1699,
    effectiveAsp: 1699,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto', 'instamart'],
    stockStatus: 'Active',
    digitalShelfScore: 81,
    shareOfSearchPercent: 14.8,
    rating: 4.1,
    reviewCount: 5400,
    dailyVelocity: 85,
    grossSales30d: 4330000,
    unitsSold30d: 2550,
    revenueAtRisk: 540000,
    contentScore: 81,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'Zenith ElectroCraft Labs',
    manufacturerPlant: 'Plot 48, Electronics SEZ, Sector 63, Noida (UP) - 201301',
    defaultMotherHub: 'Bilaspur Super Hub (Gurgaon Logistics Corridor)',
    darkStoreStock: 520,
    motherHubStock: 4200,
    batches: [
      {
        batchNumber: 'AK-902',
        skuId: 'sku-101',
        productName: 'AudioKraft Pro Bass ANC Wireless Earbuds',
        manufacturerName: 'Zenith ElectroCraft Labs',
        manufacturerPlant: 'Noida SEZ, UP',
        mfgDate: '2026-01-10',
        expiryDate: '2031-01-09',
        daysRemaining: 1605,
        shelfLifeHealthPercent: 100,
        inventoryUnits: 4200,
        inventoryValueInr: 7135800,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 1699, inStock: true, shareOfSearch: 14.8, revenue30d: 2100000 },
      flipkart: { price: 1699, inStock: true, shareOfSearch: 15.2, revenue30d: 1650000 },
      myntra: { price: 1699, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      blinkit: { price: 1699, inStock: true, shareOfSearch: 12.0, revenue30d: 380000 },
      zepto: { price: 1699, inStock: true, shareOfSearch: 11.5, revenue30d: 200000 },
      instamart: { price: 1699, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      jiomart: { price: 1699, inStock: false, shareOfSearch: 0, revenue30d: 0 }
    }
  },
  {
    id: 'sku-201',
    sku: 'SKU-NF-201',
    name: 'NutriFuel 100% Whey Protein Isolate Chocolate Delight (1kg)',
    category: 'Nutrition & Health',
    subcategory: 'Sports Nutrition',
    brand: 'NutriFuel',
    mrp: 2799,
    targetMap: 2299,
    sellingPrice: 2299,
    effectiveAsp: 2299,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto', 'instamart'],
    stockStatus: 'Active',
    digitalShelfScore: 94,
    shareOfSearchPercent: 28.6,
    rating: 4.7,
    reviewCount: 4200,
    dailyVelocity: 75,
    grossSales30d: 5170000,
    unitsSold30d: 2250,
    revenueAtRisk: 0,
    contentScore: 94,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'BioNutra Life Sciences Pvt Ltd',
    manufacturerPlant: 'Plot 12, SIDCUL Industrial Estate, Haridwar (Uttarakhand) - 249403',
    defaultMotherHub: 'Bilaspur Super Hub (Gurgaon)',
    darkStoreStock: 890,
    motherHubStock: 5600,
    batches: [
      {
        batchNumber: 'CON-AUG-01',
        skuId: 'sku-201',
        productName: 'NutriFuel 100% Whey Protein Isolate Chocolate Delight (1kg)',
        manufacturerName: 'BioNutra Life Sciences',
        manufacturerPlant: 'Haridwar SIDCUL Plant',
        mfgDate: '2026-06-15',
        expiryDate: '2028-06-14',
        daysRemaining: 665,
        shelfLifeHealthPercent: 98,
        inventoryUnits: 5600,
        inventoryValueInr: 12874400,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 2299, inStock: true, shareOfSearch: 28.6, revenue30d: 2450000 },
      flipkart: { price: 2299, inStock: true, shareOfSearch: 24.0, revenue30d: 1420000 },
      myntra: { price: 2299, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      blinkit: { price: 2299, inStock: true, shareOfSearch: 35.0, revenue30d: 820000 },
      zepto: { price: 2299, inStock: true, shareOfSearch: 31.0, revenue30d: 480000 },
      instamart: { price: 2299, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      jiomart: { price: 2299, inStock: false, shareOfSearch: 0, revenue30d: 0 }
    }
  },
  {
    id: 'sku-301',
    sku: 'SKU-PC-301',
    name: 'GlowBotanica Onion Redensyl Anti-Hairfall Oil (200ml)',
    category: 'Personal Care',
    subcategory: 'Hair Care',
    brand: 'GlowBotanica',
    mrp: 499,
    targetMap: 399,
    sellingPrice: 399,
    effectiveAsp: 399,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto', 'instamart'],
    stockStatus: 'Active',
    digitalShelfScore: 82,
    shareOfSearchPercent: 21.5,
    rating: 4.2,
    reviewCount: 3100,
    dailyVelocity: 110,
    grossSales30d: 1310000,
    unitsSold30d: 3300,
    revenueAtRisk: 0,
    contentScore: 82,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'BioNutra Life Sciences Pvt Ltd',
    manufacturerPlant: 'Haridwar Plant, Uttarakhand',
    defaultMotherHub: 'Bhiwandi Central Logistics Mother Hub',
    darkStoreStock: 1120,
    motherHubStock: 7400,
    batches: [
      {
        batchNumber: 'GB-OIL-2026',
        skuId: 'sku-301',
        productName: 'GlowBotanica Onion Redensyl Anti-Hairfall Oil',
        manufacturerName: 'BioNutra Life Sciences',
        manufacturerPlant: 'Haridwar Plant',
        mfgDate: '2026-03-10',
        expiryDate: '2028-03-09',
        daysRemaining: 568,
        shelfLifeHealthPercent: 90,
        inventoryUnits: 7400,
        inventoryValueInr: 2952600,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 399, inStock: true, shareOfSearch: 21.5, revenue30d: 620000 },
      flipkart: { price: 399, inStock: true, shareOfSearch: 18.0, revenue30d: 390000 },
      myntra: { price: 399, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      blinkit: { price: 399, inStock: true, shareOfSearch: 26.0, revenue30d: 180000 },
      zepto: { price: 399, inStock: true, shareOfSearch: 22.0, revenue30d: 120000 },
      instamart: { price: 399, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      jiomart: { price: 399, inStock: false, shareOfSearch: 0, revenue30d: 0 }
    }
  },
  {
    id: 'sku-401',
    sku: 'SKU-HK-401',
    name: 'PureHome Double Walled Stainless Steel Insulated Flask (1000ml)',
    category: 'Home & Kitchen',
    subcategory: 'Bottles & Flasks',
    brand: 'PureHome',
    mrp: 999,
    targetMap: 799,
    sellingPrice: 799,
    effectiveAsp: 799,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto'],
    stockStatus: 'Active',
    digitalShelfScore: 89,
    shareOfSearchPercent: 19.5,
    rating: 4.4,
    reviewCount: 1650,
    dailyVelocity: 60,
    grossSales30d: 1430000,
    unitsSold30d: 1800,
    revenueAtRisk: 160000,
    contentScore: 89,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'PureLife Homewares Ltd',
    manufacturerPlant: 'Sanand Industrial Estate, Ahmedabad (Gujarat) - 382110',
    defaultMotherHub: 'Bhiwandi Central Logistics Mother Hub',
    darkStoreStock: 480,
    motherHubStock: 3900,
    batches: [
      {
        batchNumber: 'PH-FLK-26A',
        skuId: 'sku-401',
        productName: 'PureHome Double Walled Stainless Steel Flask',
        manufacturerName: 'PureLife Homewares Ltd',
        manufacturerPlant: 'Sanand Plant, Gujarat',
        mfgDate: '2026-02-01',
        expiryDate: '2036-02-01',
        daysRemaining: 3453,
        shelfLifeHealthPercent: 100,
        inventoryUnits: 3900,
        inventoryValueInr: 3116100,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 799, inStock: true, shareOfSearch: 19.5, revenue30d: 790000 },
      flipkart: { price: 799, inStock: true, shareOfSearch: 16.0, revenue30d: 480000 },
      myntra: { price: 799, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      blinkit: { price: 799, inStock: true, shareOfSearch: 14.0, revenue30d: 160000 },
      zepto: { price: 799, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      instamart: { price: 799, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      jiomart: { price: 799, inStock: false, shareOfSearch: 0, revenue30d: 0 }
    }
  },
  {
    id: 'sku-501',
    sku: 'SKU-FA-501',
    name: 'ActiveWear BreathePro Seamless DryFit Training Tee',
    category: 'Apparel & Fashion',
    subcategory: 'Activewear',
    brand: 'ActiveWear',
    mrp: 1299,
    targetMap: 899,
    sellingPrice: 899,
    effectiveAsp: 899,
    activeMarketplaces: ['amazon', 'flipkart', 'myntra'],
    stockStatus: 'Active',
    digitalShelfScore: 74,
    shareOfSearchPercent: 11.2,
    rating: 3.9,
    reviewCount: 940,
    dailyVelocity: 42,
    grossSales30d: 1130000,
    unitsSold30d: 1260,
    revenueAtRisk: 290000,
    contentScore: 74,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'FabVibe Mills India Pvt Ltd',
    manufacturerPlant: 'Tirupur Apparel Export Zone, Tirupur (Tamil Nadu) - 641652',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 0,
    motherHubStock: 3100,
    batches: [
      {
        batchNumber: 'AW-2024-Q2',
        skuId: 'sku-501',
        productName: 'ActiveWear BreathePro Seamless DryFit Training Tee',
        manufacturerName: 'FabVibe Mills India',
        manufacturerPlant: 'Tirupur Export Zone',
        mfgDate: '2026-03-01',
        expiryDate: '2030-03-01',
        daysRemaining: 1290,
        shelfLifeHealthPercent: 100,
        inventoryUnits: 3100,
        inventoryValueInr: 2786900,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 899, inStock: true, shareOfSearch: 11.2, revenue30d: 410000 },
      flipkart: { price: 899, inStock: true, shareOfSearch: 9.8, revenue30d: 320000 },
      myntra: { price: 899, inStock: true, shareOfSearch: 18.5, revenue30d: 400000 },
      blinkit: { price: 899, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      zepto: { price: 899, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      instamart: { price: 899, inStock: false, shareOfSearch: 0, revenue30d: 0 },
      jiomart: { price: 899, inStock: false, shareOfSearch: 0, revenue30d: 0 }
    }
  }
];

// Generate 90 additional catalog SKUs to ensure 100+ active monitored SKUs
export const FULL_CATALOG_SKUS: SKUListing[] = [
  ...HERO_SKUS,
  ...Array.from({ length: 90 }).map((_, i) => {
    const idNum = i + 11;
    const catList = ['Skincare & Beauty', 'Audio & Wearables', 'Nutrition & Health', 'Personal Care', 'Home & Kitchen', 'Apparel & Fashion'];
    const cat = catList[i % catList.length];
    const mrp = 399 + (i % 8) * 200;
    const targetMap = mrp - 100;
    const isOos = i % 14 === 0;
    const isLow = i % 7 === 0;
    const stockStatus = isOos ? ('Out Of Stock' as const) : isLow ? ('Low Stock' as const) : ('Active' as const);

    return {
      id: `sku-gen-${idNum}`,
      sku: `SKU-GEN-${String(idNum).padStart(3, '0')}`,
      name: `${cat} Prime Edition #${idNum}`,
      category: cat,
      subcategory: 'Core Catalog Assortment',
      brand: i % 2 === 0 ? 'SkinScience Lab' : i % 3 === 0 ? 'AudioKraft' : 'NutriFuel',
      mrp,
      targetMap,
      sellingPrice: targetMap,
      effectiveAsp: targetMap,
      activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto'] as const,
      stockStatus,
      digitalShelfScore: Math.floor(65 + ((i * 7) % 35)),
      shareOfSearchPercent: Number((5 + ((i * 3) % 25)).toFixed(1)),
      rating: Number((3.8 + ((i * 0.1) % 1.2)).toFixed(1)),
      reviewCount: 300 + ((i * 85) % 3000),
      dailyVelocity: Math.floor(20 + ((i * 4) % 120)),
      grossSales30d: Math.floor(250000 + ((i * 120000) % 2500000)),
      unitsSold30d: Math.floor(400 + ((i * 150) % 3500)),
      revenueAtRisk: isOos ? 250000 + ((i * 30000) % 500000) : 0,
      contentScore: Math.floor(70 + (i % 30)),
      imageGalleryCount: 7,
      hasAplus: i % 2 === 0,
      bulletPointsCount: 5,
      manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
      manufacturerPlant: 'Plant #2, Baddi Industrial Area, Solan (HP)',
      defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
      darkStoreStock: isOos ? 0 : 200 + (i * 35),
      motherHubStock: 1500 + (i * 150),
      batches: [
        {
          batchNumber: `BAT-GEN-2026-${idNum}`,
          skuId: `sku-gen-${idNum}`,
          productName: `${cat} Prime Edition #${idNum}`,
          manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
          manufacturerPlant: 'Plant #2, Baddi, HP',
          mfgDate: '2026-03-01',
          expiryDate: '2028-03-01',
          daysRemaining: 560,
          shelfLifeHealthPercent: 92,
          inventoryUnits: 1500,
          inventoryValueInr: 1500 * targetMap,
          status: 'Fresh' as const
        }
      ],
      marketplacePrices: {
        amazon: { price: targetMap, inStock: !isOos, shareOfSearch: 12.0, revenue30d: 400000 },
        flipkart: { price: targetMap, inStock: !isOos, shareOfSearch: 10.0, revenue30d: 300000 },
        myntra: { price: targetMap, inStock: false, shareOfSearch: 0, revenue30d: 0 },
        blinkit: { price: targetMap, inStock: !isOos, shareOfSearch: 15.0, revenue30d: 150000 },
        zepto: { price: targetMap, inStock: !isOos, shareOfSearch: 12.0, revenue30d: 100000 },
        instamart: { price: targetMap, inStock: false, shareOfSearch: 0, revenue30d: 0 },
        jiomart: { price: targetMap, inStock: false, shareOfSearch: 0, revenue30d: 0 }
      }
    };
  })
];

// Dark Stores & Quick Commerce Pods with Pincodes & Mother Hub relationships
export const DARK_STORES_INVENTORY: DarkStoreInventory[] = [
  {
    storeId: 'DS-BLR-04',
    storeName: 'HSR Layout Hub 04',
    city: 'Bengaluru',
    pincode: '560102',
    platform: 'blinkit',
    availableStock: 0,
    status: 'Out Of Stock',
    deliverySlaMins: 0,
    sellingPrice: 599,
    lastChecked: '15 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 3450,
    transitHoursFromHub: 3.5
  },
  {
    storeId: 'DS-BLR-06',
    storeName: 'Koramangala 6th Block',
    city: 'Bengaluru',
    pincode: '560034',
    platform: 'blinkit',
    availableStock: 0,
    status: 'Out Of Stock',
    deliverySlaMins: 0,
    sellingPrice: 599,
    lastChecked: '12 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 3450,
    transitHoursFromHub: 3.2
  },
  {
    storeId: 'DS-BLR-08',
    storeName: 'Indiranagar 100ft Pod',
    city: 'Bengaluru',
    pincode: '560038',
    platform: 'zepto',
    availableStock: 18,
    status: 'In Stock',
    deliverySlaMins: 11,
    sellingPrice: 599,
    lastChecked: '8 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 3450,
    transitHoursFromHub: 3.8
  },
  {
    storeId: 'DS-BLR-12',
    storeName: 'Whitefield ITPL Pod',
    city: 'Bengaluru',
    pincode: '560066',
    platform: 'instamart',
    availableStock: 24,
    status: 'In Stock',
    deliverySlaMins: 14,
    sellingPrice: 599,
    lastChecked: '5 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 3450,
    transitHoursFromHub: 4.5
  },
  {
    storeId: 'DS-BLR-04B',
    storeName: 'HSR Layout Hub 04',
    city: 'Bengaluru',
    pincode: '560102',
    platform: 'blinkit',
    availableStock: 36,
    status: 'In Stock',
    deliverySlaMins: 9,
    sellingPrice: 549,
    lastChecked: '15 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 12000,
    transitHoursFromHub: 3.5
  },
  {
    storeId: 'DS-BLR-15',
    storeName: 'Koramangala 4th Block Pod',
    city: 'Bengaluru',
    pincode: '560034',
    platform: 'zepto',
    availableStock: 42,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 549,
    lastChecked: '4 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 12000,
    transitHoursFromHub: 3.2
  },
  {
    storeId: 'DS-BOM-01',
    storeName: 'Bandra West Linking Road',
    city: 'Mumbai',
    pincode: '400050',
    platform: 'blinkit',
    availableStock: 14,
    status: 'In Stock',
    deliverySlaMins: 12,
    sellingPrice: 599,
    lastChecked: '10 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Bhiwandi Central Logistics Mother Hub',
    motherHubStock: 8200,
    transitHoursFromHub: 4.0
  },
  {
    storeId: 'DS-BOM-05',
    storeName: 'Andheri West Lokhandwala',
    city: 'Mumbai',
    pincode: '400053',
    platform: 'zepto',
    availableStock: 22,
    status: 'In Stock',
    deliverySlaMins: 8,
    sellingPrice: 599,
    lastChecked: '6 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Bhiwandi Central Logistics Mother Hub',
    motherHubStock: 8200,
    transitHoursFromHub: 3.6
  },
  {
    storeId: 'DS-BOM-01B',
    storeName: 'Bandra West Linking Road',
    city: 'Mumbai',
    pincode: '400050',
    platform: 'blinkit',
    availableStock: 0,
    status: 'Out Of Stock',
    deliverySlaMins: 0,
    sellingPrice: 2299,
    lastChecked: '20 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Bhiwandi Central Logistics Mother Hub',
    motherHubStock: 5600,
    transitHoursFromHub: 4.0
  },
  {
    storeId: 'DS-DEL-02',
    storeName: 'CyberCity Phase 2 Pod',
    city: 'Gurgaon',
    pincode: '122002',
    platform: 'blinkit',
    availableStock: 28,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 599,
    lastChecked: '11 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Bilaspur Super Hub (Gurgaon)',
    motherHubStock: 10350,
    transitHoursFromHub: 2.8
  }
];

export const PERISHABLE_BATCHES: BatchPerishableInfo[] = [
  {
    batchNumber: 'PR-2026-B08',
    skuId: 'SKU-10023',
    productName: 'Organic Cold Pressed Virgin Coconut Oil (500ml Glass Jar)',
    manufacturerName: 'Clean Formulation Wing',
    manufacturerPlant: 'Plant HP-01 (Clean Formulation Wing, Baddi)',
    mfgDate: '2026-03-10',
    expiryDate: '2027-03-09',
    daysRemaining: 203,
    shelfLifeHealthPercent: 88,
    inventoryUnits: 1450,
    inventoryValueInr: 578550,
    status: 'Fresh',
    recommendedAction: 'Standard sales pacing'
  },
  {
    batchNumber: 'DAF-26-AUG-02',
    skuId: 'SKU-10045',
    productName: 'Artisanal Almond Milk Unsweetened (1L Tetra Pak)',
    manufacturerName: 'Cold Chain Dairy & Perishables',
    manufacturerPlant: 'Plant MH-03 (Cold Chain Dairy & Perishables, Pune)',
    mfgDate: '2026-07-20',
    expiryDate: '2026-10-18',
    daysRemaining: 61,
    shelfLifeHealthPercent: 42,
    inventoryUnits: 320,
    inventoryValueInr: 12925,
    status: 'Expiring Soon',
    recommendedAction: 'Trigger ₹20 instant clip coupon on Blinkit & Zepto for 48-hour liquidation'
  },
  {
    batchNumber: 'DAF-26-AUG-14',
    skuId: 'SKU-10088',
    productName: 'Greek Style High-Protein Mango Yogurt (150g Cup)',
    manufacturerName: 'Cold Chain Dairy & Perishables',
    manufacturerPlant: 'Plant MH-03 (Cold Chain Dairy & Perishables, Pune)',
    mfgDate: '2026-08-05',
    expiryDate: '2026-09-04',
    daysRemaining: 17,
    shelfLifeHealthPercent: 18,
    inventoryUnits: 480,
    inventoryValueInr: 28800,
    status: 'Critical',
    recommendedAction: 'Emergency 40% BOGO clearance in Bengaluru & Mumbai Dark Stores'
  },
  {
    batchNumber: 'CON-AUG-01',
    skuId: 'SKU-10112',
    productName: '100% Organic Raw Whey Protein Isolate (1kg Tub)',
    manufacturerName: 'Bio-Nutritional Granules',
    manufacturerPlant: 'Plant KA-04 (Bio-Nutritional Granules, Haridwar)',
    mfgDate: '2026-06-15',
    expiryDate: '2028-06-14',
    daysRemaining: 666,
    shelfLifeHealthPercent: 98,
    inventoryUnits: 5600,
    inventoryValueInr: 12874400,
    status: 'Fresh'
  },
  {
    batchNumber: 'HB-2026-X1',
    skuId: 'SKU-10156',
    productName: 'Herbal Anti-Hairfall Bhringraj & Amla Shampoo (300ml)',
    manufacturerName: 'Herbal Extraction Unit',
    manufacturerPlant: 'Plant UK-02 (Herbal Extraction Unit, Rishikesh)',
    mfgDate: '2026-02-10',
    expiryDate: '2028-02-09',
    daysRemaining: 540,
    shelfLifeHealthPercent: 88,
    inventoryUnits: 2800,
    inventoryValueInr: 1117200,
    status: 'Fresh'
  },
  {
    batchNumber: 'PR-2026-B12',
    skuId: 'SKU-10199',
    productName: 'Probiotic Kombucha Ginger Zing (250ml Glass Bottle)',
    manufacturerName: 'Clean Formulation Wing',
    manufacturerPlant: 'Plant HP-01 (Clean Formulation Wing, Baddi)',
    mfgDate: '2026-07-28',
    expiryDate: '2026-11-25',
    daysRemaining: 99,
    shelfLifeHealthPercent: 68,
    inventoryUnits: 650,
    inventoryValueInr: 97500,
    status: 'Fresh'
  }
];

export const MAP_BREACHES: MAPBreach[] = [
  {
    id: 'BREACH-001',
    sku: 'SKU-SC-001',
    productName: 'SkinScience 10% Vitamin C Radiance Face Serum (30ml)',
    channel: 'amazon',
    violatingSeller: 'RetailHub SuperDeals (3P)',
    enforcedMap: 599,
    violatedPrice: 549,
    discountPercent: -8.3,
    breachDurationHours: 14,
    status: 'Active Breach',
    evidenceUrl: 'https://amazon.in/dp/B09XYZ123',
    complianceAction: 'Stage automated Cease & Desist ticket with Brand Registry'
  },
  {
    id: 'BREACH-002',
    sku: 'SKU-HK-401',
    productName: 'PureHome Stainless Steel Insulated Flask (750ml)',
    channel: 'flipkart',
    violatingSeller: 'FastRetail Direct (3P)',
    enforcedMap: 799,
    violatedPrice: 699,
    discountPercent: -12.5,
    breachDurationHours: 36,
    status: 'Active Breach',
    complianceAction: 'Escalate to Flipkart Anti-Infringement legal portal'
  },
  {
    id: 'BREACH-003',
    sku: 'SKU-PC-301',
    productName: 'GlowBotanica Onion Redensyl Anti-Hairfall Oil',
    channel: 'blinkit',
    violatingSeller: 'QuickSeller Retail',
    enforcedMap: 399,
    violatedPrice: 359,
    discountPercent: -10.0,
    breachDurationHours: 6,
    status: 'Investigating',
    complianceAction: 'Warning issued to distributor network'
  }
];

export const SEARCH_KEYWORDS: SearchKeywordItem[] = [
  {
    id: 'kw-1',
    keyword: 'vitamin c serum for face glow',
    category: 'Beauty_skincare',
    marketplace: 'amazon',
    searchVolume: 165000,
    organicRank: 5,
    sponsoredRank: 1,
    shareOfSearch: 18.4,
    topCompetitor: 'Minimalist (#1)',
    matchedSku: 'SKU-SC-001',
    rankChange7d: -2
  },
  {
    id: 'kw-2',
    keyword: 'niacinamide serum for acne marks',
    category: 'Beauty_skincare',
    marketplace: 'amazon',
    searchVolume: 120000,
    organicRank: 2,
    sponsoredRank: 1,
    shareOfSearch: 24.1,
    topCompetitor: 'The Derma Co (#3)',
    matchedSku: 'SKU-SC-002',
    rankChange7d: 1
  },
  {
    id: 'kw-3',
    keyword: 'matte sunscreen spf 50',
    category: 'Beauty_skincare',
    marketplace: 'amazon',
    searchVolume: 210000,
    organicRank: 1,
    sponsoredRank: 2,
    shareOfSearch: 32.5,
    topCompetitor: 'Aqualogica (#4)',
    matchedSku: 'SKU-SC-004',
    rankChange7d: 0
  },
  {
    id: 'kw-4',
    keyword: 'anc earbuds under 2000',
    category: 'Electronics',
    marketplace: 'flipkart',
    searchVolume: 380000,
    organicRank: 6,
    sponsoredRank: 3,
    shareOfSearch: 14.8,
    topCompetitor: 'boAt (#1)',
    matchedSku: 'SKU-AK-101',
    rankChange7d: -3
  },
  {
    id: 'kw-5',
    keyword: 'whey protein isolate 1kg',
    category: 'Health_nutrition',
    marketplace: 'blinkit',
    searchVolume: 195000,
    organicRank: 2,
    sponsoredRank: 1,
    shareOfSearch: 28.6,
    topCompetitor: 'MuscleBlaze (#1)',
    matchedSku: 'SKU-NF-201',
    rankChange7d: 2
  },
  {
    id: 'kw-6',
    keyword: 'onion hair oil for hair fall',
    category: 'Personal_care',
    marketplace: 'blinkit',
    searchVolume: 145000,
    organicRank: 3,
    sponsoredRank: 2,
    shareOfSearch: 21.5,
    topCompetitor: 'Mamaearth (#1)',
    matchedSku: 'SKU-PC-301',
    rankChange7d: 0
  },
  {
    id: 'kw-7',
    keyword: 'SkinScience official serum',
    category: 'Beauty_skincare',
    marketplace: 'amazon',
    searchVolume: 45000,
    organicRank: 1,
    sponsoredRank: 1,
    shareOfSearch: 68.0,
    topCompetitor: 'Minimalist (Sponsored Conquest) (#2)',
    matchedSku: 'SKU-SC-001',
    rankChange7d: 0
  }
];

export const COMPETITOR_MOVES: CompetitorMove[] = [
  {
    id: 'comp-1',
    competitorName: 'Minimalist',
    type: 'Price Drop',
    timeAgo: '10 mins ago',
    threatLevel: 'High',
    description: 'Vitamin C Serum reduced from ₹599 to ₹549 (-8.3%) on Amazon with Deal badge.',
    matchedSku: 'SKU-SC-001',
    oldPrice: 599,
    newPrice: 549,
    estimatedImpactInr: 180000,
    recommendedPlaybook: 'Deploy 48-hour ₹50 Instant Amazon Clip Coupon to defend #3 organic rank'
  },
  {
    id: 'comp-2',
    competitorName: 'boAt',
    type: 'Flash Sale',
    timeAgo: '45 mins ago',
    threatLevel: 'Critical',
    description: 'Airdopes 141 discounted to ₹1,499 on Flipkart Mega Saver event.',
    matchedSku: 'SKU-AK-101',
    oldPrice: 1799,
    newPrice: 1499,
    estimatedImpactInr: 220000,
    recommendedPlaybook: 'Shift daily ad spend toward Blinkit Quick Commerce keywords (ROAS 7.05x)'
  },
  {
    id: 'comp-3',
    competitorName: 'MuscleBlaze',
    type: 'Quick Commerce Promo',
    timeAgo: '2 hrs ago',
    threatLevel: 'Medium',
    description: '20% Off coupon launched on Blinkit Delhi NCR dark stores.',
    matchedSku: 'SKU-NF-201',
    oldPrice: 2499,
    newPrice: 1999,
    estimatedImpactInr: 95000,
    recommendedPlaybook: 'Offer Free Shaker Bottle bundle on Zepto and Swiggy Instamart'
  },
  {
    id: 'comp-4',
    competitorName: 'Mamaearth',
    type: 'New Launch',
    timeAgo: '5 hrs ago',
    threatLevel: 'Medium',
    description: 'Rosemary Hair Growth Serum listed on Zepto & Blinkit.',
    matchedSku: 'SKU-PC-301',
    oldPrice: 0,
    newPrice: 449,
    estimatedImpactInr: 75000,
    recommendedPlaybook: 'Conquest competitor brand search terms on Quick Commerce sponsor bidding'
  }
];

export const REVIEWS_STREAM: ReviewVOC[] = [
  {
    id: 'rev-1',
    sku: 'SKU-SC-001',
    productName: 'SkinScience Vitamin C 10% Face Glow Serum (30ml)',
    marketplace: 'amazon',
    reviewerName: 'Pooja Sharma',
    rating: 5,
    date: '2026-08-15',
    verifiedPurchase: true,
    sentiment: 'POSITIVE',
    title: 'Holy grail for dull morning skin!',
    body: 'I have been using this Vitamin C serum for 3 weeks now. Absorbs in 30 seconds without leaving any oily residue. Dark spots from previous acne are 50% lighter. Will repurchase!',
    extractedTopic: 'Fast Absorption & Skin Radiance'
  },
  {
    id: 'rev-2',
    sku: 'SKU-SC-001',
    productName: 'SkinScience Vitamin C 10% Face Glow Serum (30ml)',
    marketplace: 'amazon',
    reviewerName: 'Rohan Mehra',
    rating: 2,
    date: '2026-08-14',
    verifiedPurchase: true,
    sentiment: 'NEGATIVE',
    title: 'Product is good but bottle leaked',
    body: 'The serum inside is decent, but the bottle arrived with 10% leaked serum inside the bubble wrap. The packaging seal needs improvement.',
    extractedTopic: 'Dropper Cap Leakage during Courier Transit',
    defectCategory: 'Packaging Seal Defect'
  },
  {
    id: 'rev-3',
    sku: 'SKU-AK-101',
    productName: 'AudioKraft Pro Bass ANC Wireless Earbuds',
    marketplace: 'flipkart',
    reviewerName: 'Vikram Joshi',
    rating: 2,
    date: '2026-08-16',
    verifiedPurchase: true,
    sentiment: 'NEGATIVE',
    title: 'Good sound, terrible microphone',
    body: 'Call quality while driving or walking on street is very muffled. The person on the other end cannot hear my voice clearly. Music bass is fine though.',
    extractedTopic: 'Bluetooth Mic Muffled in Outdoor Noise',
    defectCategory: 'Hardware Microphone Defect'
  },
  {
    id: 'rev-4',
    sku: 'SKU-NF-201',
    productName: 'NutriFuel 100% Whey Protein Isolate Chocolate',
    marketplace: 'blinkit',
    reviewerName: 'Ananya Verma',
    rating: 5,
    date: '2026-08-16',
    verifiedPurchase: true,
    sentiment: 'POSITIVE',
    title: 'Super fast delivery & blends like a dream',
    body: 'Got it in 8 minutes on Blinkit. Dissolves with just 4-5 shakes in cold water, zero lumps! Authentic chocolate flavor without any artificial aftertaste.',
    extractedTopic: 'Mixability & Authentic Chocolate Flavor'
  },
  {
    id: 'rev-5',
    sku: 'SKU-FA-501',
    productName: 'ActiveWear BreathePro Seamless DryFit Training Tee',
    marketplace: 'myntra',
    reviewerName: 'Siddharth Rao',
    rating: 2,
    date: '2026-08-13',
    verifiedPurchase: true,
    sentiment: 'NEGATIVE',
    title: 'Size running 1 size smaller',
    body: 'Ordered Size L but it fits like Medium at the chest. The fabric is nice but size chart in listing is misleading. Initiating return.',
    extractedTopic: 'Apparel Size Running Smaller than Expected',
    defectCategory: 'Size Chart Discrepancy'
  }
];

export const AD_CAMPAIGNS: AdCampaign[] = [
  {
    id: 'ad-1',
    name: 'AMZ_SP_SkinScience_Core_Keywords_Exact',
    marketplace: 'amazon',
    type: 'Sponsored Products',
    spend30d: 945000,
    attributedSales30d: 4120000,
    roas: 4.36,
    acosPercent: 22.94,
    status: 'Active'
  },
  {
    id: 'ad-2',
    name: 'AMZ_SB_SkinScience_Brand_Video_Banner',
    marketplace: 'amazon',
    type: 'Sponsored Brands',
    spend30d: 580000,
    attributedSales30d: 1980000,
    roas: 3.41,
    acosPercent: 29.29,
    status: 'Active'
  },
  {
    id: 'ad-3',
    name: 'FLIP_PLA_AudioKraft_Earbuds_Generic',
    marketplace: 'flipkart',
    type: 'Sponsored Products',
    spend30d: 720000,
    attributedSales30d: 1512000,
    roas: 2.10,
    acosPercent: 47.62,
    status: 'Active'
  },
  {
    id: 'ad-4',
    name: 'BLINK_QuickCommerce_Search_Boost_Top3',
    marketplace: 'blinkit',
    type: 'Quick Commerce Boost',
    spend30d: 410000,
    attributedSales30d: 2890000,
    roas: 7.05,
    acosPercent: 14.19,
    status: 'Active'
  }
];

export const RETURN_RECORDS: ReturnRecord[] = [
  {
    id: 'ret-1',
    orderId: 'OD-FLIP-89211',
    sku: 'SKU-AK-101',
    productName: 'AudioKraft Pro Bass ANC Wireless Earbuds',
    marketplace: 'flipkart',
    returnReason: 'Performance Below Expectation ("Muffled mic during phone calls")',
    batchNumber: 'AK-902',
    warehouseHub: 'Bhiwandi Hub',
    refundAmount: 1699,
    returnDate: '2026-08-16'
  },
  {
    id: 'ret-2',
    orderId: 'OD-MYN-34821',
    sku: 'SKU-FA-501',
    productName: 'ActiveWear BreathePro Seamless DryFit Training Tee',
    marketplace: 'myntra',
    returnReason: 'Size / Fit Mismatch ("Chest width is 2 inches tighter than size chart")',
    batchNumber: 'AW-2024-Q2',
    warehouseHub: 'Tirupur Facility',
    refundAmount: 899,
    returnDate: '2026-08-16'
  },
  {
    id: 'ret-3',
    orderId: 'OD-AMZ-77182',
    sku: 'SKU-SC-001',
    productName: 'SkinScience Vitamin C 10% Face Glow Serum (30ml)',
    marketplace: 'amazon',
    returnReason: 'Quality Defect / Damaged ("Dropper nozzle was loose and leaked")',
    batchNumber: 'SC-VTC-2607',
    warehouseHub: 'Bilaspur Warehouse',
    refundAmount: 599,
    returnDate: '2026-08-15'
  },
  {
    id: 'ret-4',
    orderId: 'OD-MYN-34902',
    sku: 'SKU-FA-501',
    productName: 'ActiveWear BreathePro Seamless DryFit Training Tee',
    marketplace: 'myntra',
    returnReason: 'Size / Fit Mismatch ("Length is too short for tall athletic fit")',
    batchNumber: 'AW-2024-Q2',
    warehouseHub: 'Tirupur Facility',
    refundAmount: 899,
    returnDate: '2026-08-14'
  },
  {
    id: 'ret-5',
    orderId: 'OD-FLIP-89304',
    sku: 'SKU-AK-101',
    productName: 'AudioKraft Pro Bass ANC Wireless Earbuds',
    marketplace: 'flipkart',
    returnReason: 'Performance Below Expectation ("Left earbud battery discharges in 2 hours")',
    batchNumber: 'AK-902',
    warehouseHub: 'Bhiwandi Hub',
    refundAmount: 1699,
    returnDate: '2026-08-14'
  }
];

export const ALERTS_ANOMALIES: AlertAnomaly[] = [
  {
    id: 'ALT-1001',
    sku: 'SKU-SC-001',
    productName: 'SkinScience Vitamin C 10% Face Glow Serum (30ml)',
    marketplace: 'blinkit',
    severity: 'Critical',
    status: 'New',
    timestamp: '2026-08-17T07:15:00Z',
    timeDisplay: '07:15 AM',
    summary: 'Dark stores #HSR-04 and #KRM-06 reported 0 stock for > 6 hours while search volume surged 28%.',
    revenueAtRiskInr: 145000,
    manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
    manufacturerPlant: 'Plant #2, Baddi Industrial Area, Solan (HP) - 173205',
    darkStoreStock: 0,
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 3450,
    motherHubPincode: '562123',
    batchNumber: 'BAT-2026-088C',
    mfgDate: '2026-04-12',
    expiryDate: '2028-04-28',
    shelfLifeHealth: 94,
    transferLeadTimeHours: 3.5,
    recommendedPlaybook: 'Dispatch immediate emergency intra-city stock transfer of 250 units from Nelamangala Mother Hub to #HSR-04 and #KRM-06 pods via Shadowfax Express.',
    transferUnitsSuggested: 250,
    logisticsPartner: 'Shadowfax Quick-Commerce Freight',
    targetOwnerEmail: OWNER_EMAIL,
    followUpSent: false
  },
  {
    id: 'ALT-1002',
    sku: 'SKU-SC-001',
    productName: 'SkinScience Vitamin C 10% Face Glow Serum (30ml)',
    marketplace: 'amazon',
    severity: 'High',
    status: 'Investigating',
    timestamp: '2026-08-16T23:50:00Z',
    timeDisplay: '11:50 PM',
    summary: 'Minimalist launched an Amazon Deal badge matching price at ₹549. Organic rank dropped from #3 to #5.',
    revenueAtRiskInr: 210000,
    manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
    manufacturerPlant: 'Plant #2, Baddi, HP',
    darkStoreStock: 1420,
    motherHubName: 'Bengaluru Central Mother Hub',
    motherHubStock: 10350,
    motherHubPincode: '562123',
    batchNumber: 'BAT-2026-088C',
    mfgDate: '2026-04-12',
    expiryDate: '2028-04-28',
    shelfLifeHealth: 94,
    transferLeadTimeHours: 4.0,
    recommendedPlaybook: 'Stage a ₹50 Instant Clip Coupon on Amazon India to neutralize competitor discount and defend Buy Box rank #3.',
    transferUnitsSuggested: 0,
    logisticsPartner: 'Amazon FBA Inbound',
    targetOwnerEmail: OWNER_EMAIL,
    followUpSent: false
  },
  {
    id: 'ALT-1003',
    sku: 'SKU-HK-401',
    productName: 'PureHome Double Walled Stainless Steel Flask (1000ml)',
    marketplace: 'flipkart',
    severity: 'High',
    status: 'New',
    timestamp: '2026-08-16T19:40:00Z',
    timeDisplay: '07:40 PM',
    summary: 'Unauthorized seller "FastRetail Direct" undercut Buy Box price to ₹699, winning 62% Buy Box share.',
    revenueAtRiskInr: 160000,
    manufacturerName: 'PureLife Homewares Ltd',
    manufacturerPlant: 'Sanand Industrial Estate, Ahmedabad (Gujarat)',
    darkStoreStock: 480,
    motherHubName: 'Bhiwandi Central Logistics Mother Hub',
    motherHubStock: 3900,
    motherHubPincode: '421302',
    batchNumber: 'PH-FLK-26A',
    mfgDate: '2026-02-01',
    expiryDate: '2036-02-01',
    shelfLifeHealth: 100,
    transferLeadTimeHours: 4.5,
    recommendedPlaybook: 'File automated MAP violation and cease-and-desist claim via Flipkart Brand Protection Portal against unauthorized seller FastRetail Direct.',
    transferUnitsSuggested: 0,
    logisticsPartner: 'Flipkart FBF Logistics',
    targetOwnerEmail: OWNER_EMAIL,
    followUpSent: false
  },
  {
    id: 'ALT-1004',
    sku: 'SKU-AK-101',
    productName: 'AudioKraft Pro Bass ANC Wireless Earbuds',
    marketplace: 'flipkart',
    severity: 'Medium',
    status: 'Acknowledged',
    timestamp: '2026-08-16T15:00:00Z',
    timeDisplay: '03:00 PM',
    summary: 'boAt flash sale caused conversion rate on FLIP_PLA_AudioKraft to drop from 4.1% to 2.1% while CPC rose.',
    revenueAtRiskInr: 185000,
    manufacturerName: 'Zenith ElectroCraft Labs',
    manufacturerPlant: 'Noida SEZ, Sector 63, Noida (UP)',
    darkStoreStock: 520,
    motherHubName: 'Bilaspur Super Hub (Gurgaon)',
    motherHubStock: 4200,
    motherHubPincode: '122413',
    batchNumber: 'AK-902',
    mfgDate: '2026-01-10',
    expiryDate: '2031-01-09',
    shelfLifeHealth: 100,
    transferLeadTimeHours: 3.0,
    recommendedPlaybook: 'Reallocate ₹10,000 daily ad budget from saturated generic keyword campaigns to high-converting Blinkit & Zepto dark store boosts.',
    transferUnitsSuggested: 0,
    logisticsPartner: 'Delhivery Surface',
    targetOwnerEmail: OWNER_EMAIL,
    followUpSent: false
  },
  {
    id: 'ALT-1005',
    sku: 'SKU-FA-501',
    productName: 'ActiveWear BreathePro Seamless DryFit Training Tee',
    marketplace: 'myntra',
    severity: 'High',
    status: 'Investigating',
    timestamp: '2026-08-15T21:30:00Z',
    timeDisplay: '09:30 PM',
    summary: 'Batch AW-2024-Q2 generated 142 returns in 7 days citing tighter chest fit. Size chart in listing lacks torso depth.',
    revenueAtRiskInr: 290000,
    manufacturerName: 'FabVibe Mills India Pvt Ltd',
    manufacturerPlant: 'Tirupur Apparel Export Zone, Tirupur (TN)',
    darkStoreStock: 0,
    motherHubName: 'Bengaluru Central Mother Hub',
    motherHubStock: 3100,
    motherHubPincode: '562123',
    batchNumber: 'AW-2024-Q2',
    mfgDate: '2026-03-01',
    expiryDate: '2030-03-01',
    shelfLifeHealth: 100,
    transferLeadTimeHours: 5.0,
    recommendedPlaybook: 'Trigger AI Listing Content Enhancer to update Myntra size guide graphics and add "Slim Athletic Fit - Size Up For Relaxed Feel" callout.',
    transferUnitsSuggested: 0,
    logisticsPartner: 'Myntra PPMP Logistics',
    targetOwnerEmail: OWNER_EMAIL,
    followUpSent: false
  },
  {
    id: 'ALT-1006',
    sku: 'SKU-SC-003',
    productName: 'SkinScience Ultra Hydrating Hyaluronic Acid Gel (50g)',
    marketplace: 'amazon',
    severity: 'Medium',
    status: 'Acknowledged',
    timestamp: '2026-08-15T16:50:00Z',
    timeDisplay: '04:50 PM',
    summary: 'Stock dropped below 50 units, triggering algorithmic de-prioritization on Amazon A10 search engine.',
    revenueAtRiskInr: 310000,
    manufacturerName: 'Apex Cosmeceuticals Pvt Ltd',
    manufacturerPlant: 'Plant #2, Baddi Industrial Area, Solan (HP)',
    darkStoreStock: 120,
    motherHubName: 'Bilaspur Super Hub (Gurgaon)',
    motherHubStock: 4800,
    motherHubPincode: '122413',
    batchNumber: 'BAT-2026-092G',
    mfgDate: '2026-03-20',
    expiryDate: '2027-09-19',
    shelfLifeHealth: 72,
    transferLeadTimeHours: 3.5,
    recommendedPlaybook: 'Trigger auto-replenishment shipment of 800 units from Bilaspur Super Hub to Amazon Delhi FC.',
    transferUnitsSuggested: 800,
    logisticsPartner: 'BlueDart Air Express',
    targetOwnerEmail: OWNER_EMAIL,
    followUpSent: false
  }
];

export const AUTONOMOUS_ACTIONS: AutonomousAction[] = [
  {
    id: 'act-1',
    actionCode: 'ACT-501',
    title: 'Deploy Amazon ₹50 Coupon on Vitamin C Serum (SKU-SC-001)',
    description: 'Deploys a targeted ₹50 instant digital coupon on Amazon India to restore buy-box velocity and counter competitor Minimalist ₹549 deal.',
    channel: 'amazon',
    agentName: 'Root Cause Agent',
    targetSku: 'SKU-SC-001',
    status: 'Pending Approval',
    createdAt: '2026-08-17T08:00:00Z',
    projectedRoiInr: 280000,
    confidencePercent: 94,
    approvalRequired: true,
    safetyGuardrail: 'Max discount capped at 10% below MAP'
  },
  {
    id: 'act-2',
    actionCode: 'ACT-502',
    title: 'Reallocate ₹10,000 Ad Budget from Flipkart Earbuds to Blinkit Quick Commerce',
    description: 'Transfers daily ad budget from saturated Flipkart broad campaign (ACOS 48%) to Blinkit high-converting dark store keyword boosts (ROAS 7.05x).',
    channel: 'flipkart',
    agentName: 'Advertising Agent',
    targetSku: 'SKU-SC-001',
    status: 'Pending Approval',
    createdAt: '2026-08-17T07:30:00Z',
    projectedRoiInr: 190000,
    confidencePercent: 92,
    approvalRequired: true,
    safetyGuardrail: 'Reallocation budget ceiling ₹15,000/day'
  },
  {
    id: 'act-3',
    actionCode: 'ACT-503',
    title: 'File Unauthorized Seller MAP Enforcement Notice against FastRetail Direct',
    description: 'Issues a binding cease-and-desist and MAP compliance infringement notice to Flipkart brand registry to stop price erosion below ₹799 MAP.',
    channel: 'flipkart',
    agentName: 'Compliance Agent',
    targetSku: 'SKU-HK-401',
    status: 'Approved',
    createdAt: '2026-08-17T06:00:00Z',
    approvedBy: 'Vikash Kumar (Owner)',
    projectedRoiInr: 120000,
    confidencePercent: 99,
    approvalRequired: true,
    safetyGuardrail: 'Requires signed Brand Registry authorization'
  },
  {
    id: 'act-4',
    actionCode: 'ACT-504',
    title: 'Auto-Replenishment Transfer Order to Blinkit Bengaluru Hub #HSR-04',
    description: 'Initiates express air freight dispatch of 300 units from Bilaspur DC to Blinkit HSR Layout dark store to eliminate out-of-stock lost revenue.',
    channel: 'blinkit',
    agentName: 'Availability Agent',
    targetSku: 'SKU-SC-001',
    status: 'Pending Approval',
    createdAt: '2026-08-17T07:18:00Z',
    projectedRoiInr: 400000,
    confidencePercent: 96,
    approvalRequired: true,
    safetyGuardrail: 'Dark store buffer limit ≤ 45 days forward cover'
  }
];

export const AI_AGENTS: AIAgentInfo[] = [
  {
    id: 'ag-1',
    name: 'Data Collection Agent',
    category: 'Ingestion',
    description: 'Syncs marketplace APIs, dark store inventories, and distributor feeds.',
    status: 'Active',
    frequency: 'Continuous (15m)',
    lastRun: '2 mins ago',
    accuracyPercent: 99.8,
    recordsProcessedToday: 48520,
    issuesDetected: 3,
    lastFinding: 'Successfully ingested 6 marketplace price streams and 20 dark store pods.'
  },
  {
    id: 'ag-2',
    name: 'Catalogue Mapping Agent',
    category: 'Normalization',
    description: 'Normalizes ASINs, FSNs, and EANs into unified canonical product IDs.',
    status: 'Active',
    frequency: 'Hourly',
    lastRun: '15 mins ago',
    accuracyPercent: 100.0,
    recordsProcessedToday: 1240,
    issuesDetected: 0,
    lastFinding: 'All 100 SKUs cross-mapped across Amazon, Flipkart, Myntra, Blinkit, and Zepto.'
  },
  {
    id: 'ag-3',
    name: 'Price Intelligence Agent',
    category: 'Pricing',
    description: 'Monitors buy box prices, coupons, competitor deals, and MAP guardrails.',
    status: 'Active',
    frequency: 'Continuous (15m)',
    lastRun: '5 mins ago',
    accuracyPercent: 99.4,
    recordsProcessedToday: 18200,
    issuesDetected: 3,
    lastFinding: 'Detected 3 MAP breaches on Amazon (RetailHub) and Flipkart (FastRetail).'
  },
  {
    id: 'ag-4',
    name: 'Availability & OOS Agent',
    category: 'Inventory',
    description: 'Tracks real-time dark store stock, warehouse OOS, and calculates lost sales.',
    status: 'Active',
    frequency: 'Continuous (15m)',
    lastRun: '3 mins ago',
    accuracyPercent: 99.7,
    recordsProcessedToday: 24000,
    issuesDetected: 2,
    lastFinding: 'Identified ₹1.45L revenue at risk due to HSR Layout & Koramangala Blinkit stockout.'
  },
  {
    id: 'ag-5',
    name: 'Search & Share of Search Agent',
    category: 'Visibility',
    description: 'Monitors organic vs sponsored keyword ranks, top-10 share, and keyword gaps.',
    status: 'Active',
    frequency: 'Hourly',
    lastRun: '12 mins ago',
    accuracyPercent: 98.9,
    recordsProcessedToday: 6800,
    issuesDetected: 1,
    lastFinding: 'Organic rank for "vitamin c serum" dropped to #5 following Minimalist discount.'
  },
  {
    id: 'ag-6',
    name: 'Review & Voice of Customer Agent',
    category: 'Customer Intelligence',
    description: 'Uses Gemini to extract sentiment, complaints, attribute ratings, and emerging flaws.',
    status: 'Active',
    frequency: 'Hourly',
    lastRun: '8 mins ago',
    accuracyPercent: 99.1,
    recordsProcessedToday: 1240,
    issuesDetected: 4,
    lastFinding: 'Synthesized 24 customer mentions regarding loose dropper caps in batch SC-VTC-2607.'
  },
  {
    id: 'ag-7',
    name: 'Competitor Intelligence Agent',
    category: 'Market Intel',
    description: 'Scans competitor launches, discount strategies, promo badges, and keyword conquesting.',
    status: 'Active',
    frequency: 'Continuous (15m)',
    lastRun: '10 mins ago',
    accuracyPercent: 99.2,
    recordsProcessedToday: 15400,
    issuesDetected: 4,
    lastFinding: 'Minimalist launched ₹50 coupon on Amazon; boAt launched Mega Saver on Flipkart.'
  },
  {
    id: 'ag-8',
    name: 'Advertising & ROAS Agent',
    category: 'Media',
    description: 'Monitors ad spend, CPC inflation, ACOS, TACOS, and budget pacing.',
    status: 'Active',
    frequency: 'Hourly',
    lastRun: '6 mins ago',
    accuracyPercent: 99.6,
    recordsProcessedToday: 8200,
    issuesDetected: 2,
    lastFinding: 'Recommended shifting ₹10k/day from Flipkart generic PLA (ACOS 48%) to Blinkit boost (ROAS 7.05x).'
  },
  {
    id: 'ag-9',
    name: 'Sales Intelligence Agent',
    category: 'Financials',
    description: 'Calculates gross/net sales, velocity, organic vs paid contribution, and ASP trends.',
    status: 'Active',
    frequency: 'Continuous (30m)',
    lastRun: '4 mins ago',
    accuracyPercent: 100.0,
    recordsProcessedToday: 32000,
    issuesDetected: 1,
    lastFinding: '30-day catalog gross sales tracking at ₹3.66 Cr (+8.4% YoY).'
  },
  {
    id: 'ag-10',
    name: 'Returns & Quality Agent',
    category: 'Operations',
    description: 'Correlates return reasons with review sentiment, batches, and supplier warehouses.',
    status: 'Active',
    frequency: 'Daily (06:00)',
    lastRun: '2 hrs ago',
    accuracyPercent: 99.0,
    recordsProcessedToday: 1850,
    issuesDetected: 2,
    lastFinding: 'Detected 18.2% return rate on ActiveWear tees due to size guide disparity.'
  },
  {
    id: 'ag-11',
    name: 'Compliance & MAP Agent',
    category: 'Governance',
    description: 'Enforces authorized seller rules, detects unauthorized distributors, logs evidence.',
    status: 'Active',
    frequency: 'Continuous (15m)',
    lastRun: '14 mins ago',
    accuracyPercent: 99.8,
    recordsProcessedToday: 4200,
    issuesDetected: 3,
    lastFinding: 'Staged Cease & Desist legal documentation against FastRetail Direct.'
  },
  {
    id: 'ag-12',
    name: 'Root Cause Investigation Agent',
    category: 'Autonomous Reasoning',
    description: 'Multi-source correlation engine: cross-references sales drops with OOS, price, ads, and reviews.',
    status: 'Active',
    frequency: 'Continuous (Event-Driven)',
    lastRun: '7 mins ago',
    accuracyPercent: 97.8,
    recordsProcessedToday: 420,
    issuesDetected: 6,
    lastFinding: 'Isolated primary cause of Vitamin C sales dip to Bengaluru dark store OOS + Minimalist deal.'
  },
  {
    id: 'ag-13',
    name: 'Autonomous Recommendation Agent',
    category: 'Decision Support',
    description: 'Generates prioritized playbooks ranked by (Business Impact × Confidence × Urgency).',
    status: 'Active',
    frequency: 'Continuous',
    lastRun: '6 mins ago',
    accuracyPercent: 96.5,
    recordsProcessedToday: 184,
    issuesDetected: 0,
    lastFinding: 'Generated 4 executable playbooks ready in Action Center.'
  },
  {
    id: 'ag-14',
    name: 'Autonomous Action Execution Agent',
    category: 'Execution',
    description: 'Executes approved actions via authorized marketplace API & supply chain bridges.',
    status: 'Active',
    frequency: 'Event-Driven',
    lastRun: '22 mins ago',
    accuracyPercent: 100.0,
    recordsProcessedToday: 18,
    issuesDetected: 0,
    lastFinding: 'Executed 1 approved compliance notice; 3 pending human approval.'
  },
  {
    id: 'ag-15',
    name: 'Executive Reporting Agent',
    category: 'Reporting',
    description: 'Compiles Weekly Business Review (WBR) and dispatches automated briefs to leadership.',
    status: 'Active',
    frequency: 'Scheduled / On-Demand',
    lastRun: '1 hr ago',
    accuracyPercent: 100.0,
    recordsProcessedToday: 12,
    issuesDetected: 0,
    lastFinding: 'Weekly WBR Report synthesized and queued for Vikash.Kumar@agileventures.net.'
  },
  {
    id: 'ag-16',
    name: 'Alert & Notification Agent',
    category: 'Alerting',
    description: 'Manages emergency voice broadcasts, email dispatches, and WhatsApp escalation trees.',
    status: 'Active',
    frequency: 'Instant (Real-time)',
    lastRun: '1 min ago',
    accuracyPercent: 100.0,
    recordsProcessedToday: 89,
    issuesDetected: 0,
    lastFinding: 'Dispatched real-time voice telemetry update and notification pills.'
  }
];

export const EXECUTIVE_REPORTS: ExecutiveReport[] = [
  {
    id: 'rep-001',
    title: 'Weekly Executive Business Review (WBR) - Week 33',
    period: 'Aug 10 - Aug 16, 2026',
    generatedDate: '2026-08-17T07:00:00Z',
    type: 'WBR',
    author: 'AI Reporting Agent',
    targetEmail: OWNER_EMAIL,
    executiveSummary: 'Gross brand sales stood at ₹78,40,000 across all channels, growing +8.4% YoY. Quick commerce (Blinkit, Zepto, Swiggy Instamart) expanded to represent 36.5% of total brand sales. Primary operational headwind was temporary dark store OOS in Bengaluru and aggressive promotional discounting by competitor Minimalist on Amazon.',
    strategicObservations: [
      'Digital Shelf Health Score averaged 87.4/100 across 94 active catalog listings.',
      'Quick commerce ROAS reached 7.05x, outperforming traditional e-commerce search ads (3.4x).',
      'Revenue at Risk identified at ₹16,20,000, driven by OOS, Flipkart MAP violations, and apparel sizing return rates.',
      '4 Autonomous Action proposals generated with expected revenue recovery of ₹9,80,000.'
    ],
    revenueSummary: {
      grossSalesInr: 7840000,
      growthPercent: 8.4,
      quickCommerceSharePercent: 36.5,
      revenueAtRiskInr: 1620000,
      recoveredRevenueInr: 980000
    },
    dispatchedAt: '2026-08-17T07:30:00Z',
    scheduledCron: 'Every Monday at 08:00 AM IST'
  },
  {
    id: 'rep-002',
    title: 'Digital Shelf & Price Competitiveness Audit',
    period: 'Last 30 Days',
    generatedDate: '2026-08-16T18:00:00Z',
    type: 'Digital Shelf',
    author: 'Price Intelligence Agent',
    targetEmail: OWNER_EMAIL,
    executiveSummary: 'Detailed audit of 100 SKUs across 6 marketplaces. Overall price index stands at 98.4 (competitive parity). 1 MAP violation detected on Flipkart. Share of Search in core skincare category reached 24.8%.',
    strategicObservations: [
      'SkinScience Sunscreen maintained #1 search rank on Amazon for 28 consecutive days.',
      'Content compliance score is 94.2/100, with 100% listings equipped with 7 images and A+ content.',
      'Blinkit dark stores in North India achieved 98.1% in-stock availability.'
    ],
    revenueSummary: {
      grossSalesInr: 36668000,
      growthPercent: 12.1,
      quickCommerceSharePercent: 34.2,
      revenueAtRiskInr: 12029000,
      recoveredRevenueInr: 7450000
    }
  }
];

export const EMAIL_DISPATCH_LOGS: EmailDispatchLog[] = [
  {
    id: 'mail-log-1',
    recipientEmail: OWNER_EMAIL,
    senderEmail: SENDER_GMAIL,
    subject: '[URGENT] Anomaly & Follow-Up Supply Chain Resolution: SkinScience Vitamin C (SKU-SC-001)',
    reportType: 'Quick Commerce OOS & Mother Hub Follow-up',
    sentAt: '2026-08-17 07:16 AM IST',
    deliveryStatus: 'Delivered',
    summaryPreview: 'Blinkit Bengaluru dark stores #HSR-04 and #KRM-06 reported 0 stock. Follow-up: 3,450 units available at Nelamangala Mother Hub. Transfer of 250 units initiated.',
    followUpActionsCount: 2
  },
  {
    id: 'mail-log-2',
    recipientEmail: OWNER_EMAIL,
    senderEmail: SENDER_GMAIL,
    subject: 'Weekly Business Review (WBR) - Week 33 Executive Briefing',
    reportType: 'WBR Executive Report',
    sentAt: '2026-08-17 07:30 AM IST',
    deliveryStatus: 'Delivered',
    summaryPreview: 'Gross sales ₹78.4L (+8.4% YoY). Quick commerce penetration 36.5%. ROAS 4.22x. Revenue at risk ₹16.2L.',
    followUpActionsCount: 4
  }
];

// Historical 30-day time-series for chart visualizers
export const HISTORICAL_CHART_DATA = Array.from({ length: 30 }).map((_, i) => {
  const day = i + 1;
  const dateStr = `08-${String(day).padStart(2, '0')}`;
  const grossSales = Math.floor(1100000 + Math.sin(i * 0.5) * 350000 + (i * 12000));
  const netSales = Math.floor(grossSales * 0.92);
  const adSpend = Math.floor(80000 + (grossSales * 0.075));
  const oosRate = Number((2.5 + Math.sin(i * 0.7) * 1.5).toFixed(1));
  const shareOfSearch = Number((22.0 + Math.cos(i * 0.4) * 4.0).toFixed(1));

  return {
    date: dateStr,
    fullDate: `2026-08-${String(day).padStart(2, '0')}`,
    grossSales,
    netSales,
    adSpend,
    oosRate,
    shareOfSearch,
    roas: Number((grossSales / (adSpend || 1)).toFixed(2))
  };
});

export const VOC_FEEDBACK_ITEMS = [
  {
    id: 'voc-1',
    sku: 'SKU-SC-001',
    productName: 'SkinScience Vitamin C 10% Face Glow Serum',
    channel: 'amazon',
    rating: 5,
    sentiment: 'Positive',
    reviewText: 'Holy grail for dull morning skin! Absorbs in 30 seconds without leaving any oily residue. Dark spots from previous acne are 50% lighter.',
    extractedTopic: 'Fast Absorption & Skin Radiance'
  },
  {
    id: 'voc-2',
    sku: 'SKU-SC-001',
    productName: 'SkinScience Vitamin C 10% Face Glow Serum',
    channel: 'amazon',
    rating: 2,
    sentiment: 'Negative',
    reviewText: 'The serum inside is decent, but the bottle arrived with 10% leaked serum inside the bubble wrap. The packaging seal needs improvement.',
    extractedTopic: 'Courier Transit Dropper Leakage',
    defectCategory: 'Packaging Seal / Dropper Leak'
  },
  {
    id: 'voc-3',
    sku: 'SKU-AK-101',
    productName: 'AudioKraft Pro Bass ANC Wireless Earbuds',
    channel: 'flipkart',
    rating: 2,
    sentiment: 'Negative',
    reviewText: 'Good sound, terrible microphone during phone calls. The person on the other end cannot hear my voice clearly in outdoor noise.',
    extractedTopic: 'Microphone Muffled in Outdoor Noise',
    defectCategory: 'Hardware Microphone Defect'
  },
  {
    id: 'voc-4',
    sku: 'SKU-NF-201',
    productName: 'NutriFuel 100% Whey Protein Isolate Chocolate',
    channel: 'blinkit',
    rating: 5,
    sentiment: 'Positive',
    reviewText: 'Got it in 8 minutes on Blinkit. Dissolves with just 4-5 shakes in cold water, zero lumps! Authentic chocolate flavor.',
    extractedTopic: 'Mixability & Authentic Flavor'
  },
  {
    id: 'voc-5',
    sku: 'SKU-FA-501',
    productName: 'ActiveWear BreathePro Seamless DryFit Training Tee',
    channel: 'myntra',
    rating: 2,
    sentiment: 'Negative',
    reviewText: 'Ordered Size L but it fits like Medium at the chest. The fabric is nice but size chart in listing is misleading.',
    extractedTopic: 'Size Running Smaller than Expected',
    defectCategory: 'Size Chart Discrepancy'
  }
];

export const ADVERTISING_CAMPAIGNS = [
  {
    id: 'AD-001',
    campaignName: 'AMZ_SP_SkinScience_Core_Keywords_Exact',
    marketplace: 'amazon',
    campaignType: 'Sponsored Products',
    spend30d: 945000,
    salesAttributed30d: 4120000,
    roas: 4.36,
    acos: 22.9,
    aiAction: 'Increase bid by +8% on exact search terms'
  },
  {
    id: 'AD-002',
    campaignName: 'AMZ_SB_SkinScience_Brand_Video_Banner',
    marketplace: 'amazon',
    campaignType: 'Sponsored Brands',
    spend30d: 580000,
    salesAttributed30d: 1980000,
    roas: 3.41,
    acos: 29.3,
    aiAction: 'A/B test 15-sec clinical demonstration video'
  },
  {
    id: 'AD-003',
    campaignName: 'FLIP_PLA_AudioKraft_Earbuds_Generic',
    marketplace: 'flipkart',
    campaignType: 'Sponsored Products',
    spend30d: 720000,
    salesAttributed30d: 1512000,
    roas: 2.10,
    acos: 47.6,
    aiAction: 'Reduce daily budget by -25% and shift to QC'
  },
  {
    id: 'AD-004',
    campaignName: 'BLINK_QuickCommerce_Search_Boost_Top3',
    marketplace: 'blinkit',
    campaignType: 'Quick Commerce Boost',
    spend30d: 410000,
    salesAttributed30d: 2890000,
    roas: 7.05,
    acos: 14.2,
    aiAction: 'Scale budget to ₹20,000/day during evening rush'
  }
];

export const RETURNS_AUDIT_DATA = [
  {
    id: 'RET-001',
    sku: 'SKU-FA-501',
    channel: 'myntra',
    returnRate: 14.2,
    batchCorrelated: 'AW-2024-Q2',
    topReason: 'Tighter chest fit and torso discrepancy',
    actionableSolution: 'Update size chart graphics with athletic fit callout'
  },
  {
    id: 'RET-002',
    sku: 'SKU-AK-101',
    channel: 'flipkart',
    returnRate: 9.8,
    batchCorrelated: 'AK-902',
    topReason: 'Microphone muffled in noisy outdoor environments',
    actionableSolution: 'Flag to Zenith Plant QA and stage supplier warranty claim'
  },
  {
    id: 'RET-003',
    sku: 'SKU-SC-001',
    channel: 'amazon',
    returnRate: 4.1,
    batchCorrelated: 'BAT-2026-088C',
    topReason: 'Dropper cap courier leakage during transit',
    actionableSolution: 'Induction heat sealing added to Baddi plant line #2'
  }
];

export const AI_AGENTS_LIST = [
  {
    id: 'AG-01',
    name: 'Digital Shelf Auditor',
    category: 'Digital Shelf',
    description: 'Scans 100 SKUs for title length, 7/7 images, A+ content, and search backend terms.',
    status: 'Active',
    frequency: 'Hourly',
    lastRunTimestamp: '4 mins ago',
    actionsTakenCount: 142
  },
  {
    id: 'AG-02',
    name: 'Quick Commerce Dark Store Stockout Predictor',
    category: 'Inventory & Supply Chain',
    description: 'Monitors real-time 15-min pod stocks in Blinkit, Zepto, and Instamart with Mother Hub correlation.',
    status: 'Active',
    frequency: 'Every 5 Mins',
    lastRunTimestamp: '1 min ago',
    actionsTakenCount: 89
  },
  {
    id: 'AG-03',
    name: 'MAP & Buy Box Compliance Guardian',
    category: 'Pricing & MAP',
    description: 'Identifies unauthorized 3P price erosion below MAP guardrails with automated legal cease-and-desist.',
    status: 'Active',
    frequency: 'Continuous (15m)',
    lastRunTimestamp: '6 mins ago',
    actionsTakenCount: 38
  },
  {
    id: 'AG-04',
    name: 'Perishables & FEFO Expiry Optimizer',
    category: 'Quality & Perishables',
    description: 'Tracks batch numbers, mfg/exp dates, and triggers automated quick commerce flash discounts.',
    status: 'Active',
    frequency: 'Daily 06:00 AM',
    lastRunTimestamp: '2 hrs ago',
    actionsTakenCount: 64
  },
  {
    id: 'AG-05',
    name: 'Autonomous Advertising & ROAS Maximizer',
    category: 'Advertising',
    description: 'Dynamic budget allocation shifting spend from low-ROAS broad keywords to high-converting quick commerce.',
    status: 'Active',
    frequency: 'Hourly',
    lastRunTimestamp: '12 mins ago',
    actionsTakenCount: 215
  },
  {
    id: 'AG-06',
    name: 'VOC Review & Packaging Defect Forensics',
    category: 'Customer Intelligence',
    description: 'NLP sentiment clustering that detects leaking bottles, muffled mics, or sizing discrepancies.',
    status: 'Active',
    frequency: 'Continuous',
    lastRunTimestamp: '3 mins ago',
    actionsTakenCount: 97
  }
];

