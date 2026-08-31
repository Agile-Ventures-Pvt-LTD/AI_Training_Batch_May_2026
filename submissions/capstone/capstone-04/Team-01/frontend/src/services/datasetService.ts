import * as XLSX from 'xlsx';
import {
  SKUListing,
  DarkStoreInventory,
  MotherHub,
  MotherHubSkuStock,
  ManufacturerSupplyInfo,
  MAPBreach,
  ChannelPricingItem,
  AlertAnomaly,
  BatchPerishableInfo,
  MarketplaceId,
  SearchKeywordItem,
  CompetitorMove,
  ReviewVOC,
  AdCampaign,
  ReturnRecord,
  AutonomousAction,
  AIAgentInfo,
  ExecutiveReport,
  EmailDispatchLog,
  StockTransferLog
} from '../types';

export const SLEEP_SKU_CATALOG: SKUListing[] = [
  {
    id: 'sku-slp-1001',
    sku: 'SLP-1001',
    name: 'Contour Memory Foam Cervical Pillow',
    category: 'Sleep & Ergonomics',
    subcategory: 'Cervical Pillows',
    brand: 'OrthoRest',
    productType: 'Cervical Pillow',
    material: 'Memory Foam',
    intendedUse: 'Adult sleep support',
    mrp: 1999,
    targetMap: 1499,
    sellingPrice: 1499,
    effectiveAsp: 1449,
    activeMarketplaces: ['amazon', 'flipkart', 'myntra', 'blinkit', 'zepto', 'instamart', 'jiomart'],
    stockStatus: 'Low Stock',
    digitalShelfScore: 94,
    shareOfSearchPercent: 42.6,
    rating: 4.6,
    reviewCount: 3840,
    dailyVelocity: 148,
    grossSales30d: 6655560,
    unitsSold30d: 4440,
    revenueAtRisk: 148500,
    contentScore: 96,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 3, // Low stock triggering Micro-OOS simulation
    motherHubStock: 184500,
    batches: [
      {
        batchNumber: 'BAT-2026-088C',
        skuId: 'SLP-1001',
        productName: 'Contour Memory Foam Cervical Pillow',
        manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
        manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
        mfgDate: '2026-04-10',
        expiryDate: '2029-04-10',
        daysRemaining: 960,
        shelfLifeHealthPercent: 98,
        inventoryUnits: 184500,
        inventoryValueInr: 276565500,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 1499, inStock: true, shareOfSearch: 44.2, revenue30d: 2980000, buyBoxOwner: 'OrthoRest Official' },
      flipkart: { price: 1399, inStock: true, shareOfSearch: 38.5, revenue30d: 1950000, buyBoxOwner: 'DiscountDeals_IN (Breach)' },
      myntra: { price: 1499, inStock: true, shareOfSearch: 32.0, revenue30d: 820000, buyBoxOwner: 'OrthoRest Official' },
      blinkit: { price: 1499, inStock: true, shareOfSearch: 48.0, revenue30d: 1120000, buyBoxOwner: 'Dark Store Pod' },
      zepto: { price: 1499, inStock: true, shareOfSearch: 46.5, revenue30d: 890000, buyBoxOwner: 'Zepto Pod' },
      instamart: { price: 1499, inStock: true, shareOfSearch: 39.0, revenue30d: 650000, buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: 1499, inStock: true, shareOfSearch: 28.0, revenue30d: 420000, buyBoxOwner: 'JioMart Pod' }
    }
  },
  {
    id: 'sku-slp-1002',
    sku: 'SLP-1002',
    name: 'Travel Neck Memory Foam Pillow',
    category: 'Sleep & Ergonomics',
    subcategory: 'Travel Pillows',
    brand: 'OrthoRest',
    productType: 'Travel Pillow',
    material: 'Memory Foam',
    intendedUse: 'Travel neck support',
    mrp: 999,
    targetMap: 749,
    sellingPrice: 749,
    effectiveAsp: 729,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto', 'instamart'],
    stockStatus: 'Active',
    digitalShelfScore: 91,
    shareOfSearchPercent: 36.8,
    rating: 4.5,
    reviewCount: 2190,
    dailyVelocity: 115,
    grossSales30d: 2584050,
    unitsSold30d: 3450,
    revenueAtRisk: 0,
    contentScore: 92,
    imageGalleryCount: 6,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 45,
    motherHubStock: 96000,
    batches: [
      {
        batchNumber: 'BAT-2026-092A',
        skuId: 'SLP-1002',
        productName: 'Travel Neck Memory Foam Pillow',
        manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
        manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
        mfgDate: '2026-05-01',
        expiryDate: '2029-05-01',
        daysRemaining: 980,
        shelfLifeHealthPercent: 100,
        inventoryUnits: 96000,
        inventoryValueInr: 71904000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 749, inStock: true, shareOfSearch: 38.0, revenue30d: 1250000, buyBoxOwner: 'OrthoRest Official' },
      flipkart: { price: 749, inStock: true, shareOfSearch: 35.5, revenue30d: 890000, buyBoxOwner: 'OrthoRest Official' },
      myntra: { price: 749, inStock: true, shareOfSearch: 28.0, revenue30d: 240000, buyBoxOwner: 'OrthoRest Official' },
      blinkit: { price: 749, inStock: true, shareOfSearch: 41.0, revenue30d: 450000, buyBoxOwner: 'Dark Store Pod' },
      zepto: { price: 749, inStock: true, shareOfSearch: 39.0, revenue30d: 380000, buyBoxOwner: 'Zepto Pod' },
      instamart: { price: 749, inStock: true, shareOfSearch: 33.0, revenue30d: 280000, buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: 749, inStock: true, shareOfSearch: 22.0, revenue30d: 140000, buyBoxOwner: 'JioMart Pod' }
    }
  },
  {
    id: 'sku-slp-1003',
    sku: 'SLP-1003',
    name: 'Alpha Kids Memory Foam Pillow',
    category: 'Sleep & Ergonomics',
    subcategory: 'Kids Pillows',
    brand: 'OrthoRest',
    productType: 'Kids Pillow',
    material: 'Memory Foam',
    intendedUse: "Children's sleep support",
    mrp: 1499,
    targetMap: 1199,
    sellingPrice: 1199,
    effectiveAsp: 1169,
    activeMarketplaces: ['amazon', 'flipkart', 'myntra', 'blinkit', 'zepto'],
    stockStatus: 'Active',
    digitalShelfScore: 88,
    shareOfSearchPercent: 29.4,
    rating: 4.7,
    reviewCount: 1420,
    dailyVelocity: 74,
    grossSales30d: 2661780,
    unitsSold30d: 2220,
    revenueAtRisk: 0,
    contentScore: 90,
    imageGalleryCount: 6,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 2 - Chakan Industrial Belt, Pune, MH',
    defaultMotherHub: 'Mumbai Mega Hub (Bhiwandi)',
    darkStoreStock: 28,
    motherHubStock: 64000,
    batches: [
      {
        batchNumber: 'BAT-2026-074K',
        skuId: 'SLP-1003',
        productName: 'Alpha Kids Memory Foam Pillow',
        manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
        manufacturerPlant: 'Plant 2 - Chakan Industrial Belt, Pune, MH',
        mfgDate: '2026-03-15',
        expiryDate: '2029-03-15',
        daysRemaining: 940,
        shelfLifeHealthPercent: 96,
        inventoryUnits: 64000,
        inventoryValueInr: 76736000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 1199, inStock: true, shareOfSearch: 31.0, revenue30d: 1180000, buyBoxOwner: 'OrthoRest Official' },
      flipkart: { price: 1199, inStock: true, shareOfSearch: 28.0, revenue30d: 790000, buyBoxOwner: 'OrthoRest Official' },
      myntra: { price: 1199, inStock: true, shareOfSearch: 34.0, revenue30d: 420000, buyBoxOwner: 'OrthoRest Official' },
      blinkit: { price: 1199, inStock: true, shareOfSearch: 26.0, revenue30d: 280000, buyBoxOwner: 'Dark Store Pod' },
      zepto: { price: 1199, inStock: true, shareOfSearch: 24.0, revenue30d: 220000, buyBoxOwner: 'Zepto Pod' },
      instamart: { price: 1199, inStock: true, shareOfSearch: 20.0, revenue30d: 160000, buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: 1199, inStock: true, shareOfSearch: 18.0, revenue30d: 110000, buyBoxOwner: 'JioMart Pod' }
    }
  },
  {
    id: 'sku-slp-1004',
    sku: 'SLP-1004',
    name: 'Lumbar Support Cushion',
    category: 'Sleep & Ergonomics',
    subcategory: 'Lumbar Pillows',
    brand: 'OrthoRest',
    productType: 'Lumbar Pillow',
    material: 'Memory Foam',
    intendedUse: 'Seated lumbar support',
    mrp: 1299,
    targetMap: 999,
    sellingPrice: 999,
    effectiveAsp: 969,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto', 'instamart'],
    stockStatus: 'Active',
    digitalShelfScore: 92,
    shareOfSearchPercent: 38.2,
    rating: 4.5,
    reviewCount: 3120,
    dailyVelocity: 130,
    grossSales30d: 3896100,
    unitsSold30d: 3900,
    revenueAtRisk: 0,
    contentScore: 94,
    imageGalleryCount: 7,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 62,
    motherHubStock: 88000,
    batches: [
      {
        batchNumber: 'BAT-2026-081L',
        skuId: 'SLP-1004',
        productName: 'Lumbar Support Cushion',
        manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
        manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
        mfgDate: '2026-04-01',
        expiryDate: '2029-04-01',
        daysRemaining: 955,
        shelfLifeHealthPercent: 97,
        inventoryUnits: 88000,
        inventoryValueInr: 87912000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 999, inStock: true, shareOfSearch: 41.0, revenue30d: 1850000, buyBoxOwner: 'OrthoRest Official' },
      flipkart: { price: 999, inStock: true, shareOfSearch: 36.0, revenue30d: 1240000, buyBoxOwner: 'OrthoRest Official' },
      myntra: { price: 999, inStock: true, shareOfSearch: 30.0, revenue30d: 350000, buyBoxOwner: 'OrthoRest Official' },
      blinkit: { price: 999, inStock: true, shareOfSearch: 40.0, revenue30d: 580000, buyBoxOwner: 'Dark Store Pod' },
      zepto: { price: 999, inStock: true, shareOfSearch: 38.0, revenue30d: 490000, buyBoxOwner: 'Zepto Pod' },
      instamart: { price: 999, inStock: true, shareOfSearch: 31.0, revenue30d: 320000, buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: 999, inStock: true, shareOfSearch: 20.0, revenue30d: 190000, buyBoxOwner: 'JioMart Pod' }
    }
  },
  {
    id: 'sku-slp-1005',
    sku: 'SLP-1005',
    name: 'Cooling Gel Memory Foam Pillow',
    category: 'Sleep & Ergonomics',
    subcategory: 'Bed Pillows',
    brand: 'OrthoRest',
    productType: 'Bed Pillow',
    material: 'Memory Foam + Gel',
    intendedUse: 'Adult sleep support',
    mrp: 2499,
    targetMap: 1899,
    sellingPrice: 1899,
    effectiveAsp: 1849,
    activeMarketplaces: ['amazon', 'flipkart', 'myntra', 'blinkit', 'zepto'],
    stockStatus: 'Active',
    digitalShelfScore: 95,
    shareOfSearchPercent: 44.0,
    rating: 4.8,
    reviewCount: 4620,
    dailyVelocity: 162,
    grossSales30d: 9229140,
    unitsSold30d: 4860,
    revenueAtRisk: 0,
    contentScore: 98,
    imageGalleryCount: 8,
    hasAplus: true,
    bulletPointsCount: 6,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 80,
    motherHubStock: 154000,
    batches: [
      {
        batchNumber: 'BAT-2026-095G',
        skuId: 'SLP-1005',
        productName: 'Cooling Gel Memory Foam Pillow',
        manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
        manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
        mfgDate: '2026-05-10',
        expiryDate: '2029-05-10',
        daysRemaining: 990,
        shelfLifeHealthPercent: 100,
        inventoryUnits: 154000,
        inventoryValueInr: 292446000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 1899, inStock: true, shareOfSearch: 46.0, revenue30d: 4500000, buyBoxOwner: 'OrthoRest Official' },
      flipkart: { price: 1899, inStock: true, shareOfSearch: 42.0, revenue30d: 2850000, buyBoxOwner: 'OrthoRest Official' },
      myntra: { price: 1899, inStock: true, shareOfSearch: 38.0, revenue30d: 980000, buyBoxOwner: 'OrthoRest Official' },
      blinkit: { price: 1899, inStock: true, shareOfSearch: 45.0, revenue30d: 1450000, buyBoxOwner: 'Dark Store Pod' },
      zepto: { price: 1899, inStock: true, shareOfSearch: 43.0, revenue30d: 1120000, buyBoxOwner: 'Zepto Pod' },
      instamart: { price: 1899, inStock: true, shareOfSearch: 36.0, revenue30d: 780000, buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: 1899, inStock: true, shareOfSearch: 25.0, revenue30d: 450000, buyBoxOwner: 'JioMart Pod' }
    }
  },
  {
    id: 'sku-slp-1006',
    sku: 'SLP-1006',
    name: 'Wedge Support Pillow',
    category: 'Sleep & Ergonomics',
    subcategory: 'Wedge Pillows',
    brand: 'OrthoRest',
    productType: 'Wedge Pillow',
    material: 'Foam',
    intendedUse: 'Positioning support',
    mrp: 2199,
    targetMap: 1699,
    sellingPrice: 1699,
    effectiveAsp: 1649,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto'],
    stockStatus: 'Active',
    digitalShelfScore: 89,
    shareOfSearchPercent: 31.5,
    rating: 4.4,
    reviewCount: 1280,
    dailyVelocity: 55,
    grossSales30d: 2803350,
    unitsSold30d: 1650,
    revenueAtRisk: 0,
    contentScore: 88,
    imageGalleryCount: 6,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 3 - Manesar Industrial Estate, Gurugram, HR',
    defaultMotherHub: 'Delhi NCR Hub (Bilaspur)',
    darkStoreStock: 24,
    motherHubStock: 48000,
    batches: [
      {
        batchNumber: 'BAT-2026-068W',
        skuId: 'SLP-1006',
        productName: 'Wedge Support Pillow',
        manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
        manufacturerPlant: 'Plant 3 - Manesar Industrial Estate, Gurugram, HR',
        mfgDate: '2026-03-01',
        expiryDate: '2029-03-01',
        daysRemaining: 925,
        shelfLifeHealthPercent: 95,
        inventoryUnits: 48000,
        inventoryValueInr: 81552000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 1699, inStock: true, shareOfSearch: 34.0, revenue30d: 1350000, buyBoxOwner: 'OrthoRest Official' },
      flipkart: { price: 1699, inStock: true, shareOfSearch: 30.0, revenue30d: 920000, buyBoxOwner: 'OrthoRest Official' },
      myntra: { price: 1699, inStock: true, shareOfSearch: 22.0, revenue30d: 210000, buyBoxOwner: 'OrthoRest Official' },
      blinkit: { price: 1699, inStock: true, shareOfSearch: 28.0, revenue30d: 380000, buyBoxOwner: 'Dark Store Pod' },
      zepto: { price: 1699, inStock: true, shareOfSearch: 25.0, revenue30d: 290000, buyBoxOwner: 'Zepto Pod' },
      instamart: { price: 1699, inStock: true, shareOfSearch: 20.0, revenue30d: 190000, buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: 1699, inStock: true, shareOfSearch: 15.0, revenue30d: 120000, buyBoxOwner: 'JioMart Pod' }
    }
  },
  {
    id: 'sku-slp-1007',
    sku: 'SLP-1007',
    name: 'Car Neck Rest Pillow',
    category: 'Sleep & Ergonomics',
    subcategory: 'Travel/Car Pillows',
    brand: 'OrthoRest',
    productType: 'Travel/Car Pillow',
    material: 'Memory Foam',
    intendedUse: 'Car neck support',
    mrp: 899,
    targetMap: 699,
    sellingPrice: 699,
    effectiveAsp: 679,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto', 'instamart'],
    stockStatus: 'Active',
    digitalShelfScore: 90,
    shareOfSearchPercent: 35.0,
    rating: 4.5,
    reviewCount: 2840,
    dailyVelocity: 92,
    grossSales30d: 1929240,
    unitsSold30d: 2760,
    revenueAtRisk: 0,
    contentScore: 91,
    imageGalleryCount: 6,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 35,
    motherHubStock: 76000,
    batches: [
      {
        batchNumber: 'BAT-2026-085C',
        skuId: 'SLP-1007',
        productName: 'Car Neck Rest Pillow',
        manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
        manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
        mfgDate: '2026-04-18',
        expiryDate: '2029-04-18',
        daysRemaining: 970,
        shelfLifeHealthPercent: 99,
        inventoryUnits: 76000,
        inventoryValueInr: 53124000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 699, inStock: true, shareOfSearch: 36.0, revenue30d: 940000, buyBoxOwner: 'OrthoRest Official' },
      flipkart: { price: 699, inStock: true, shareOfSearch: 34.0, revenue30d: 680000, buyBoxOwner: 'OrthoRest Official' },
      myntra: { price: 699, inStock: true, shareOfSearch: 26.0, revenue30d: 180000, buyBoxOwner: 'OrthoRest Official' },
      blinkit: { price: 699, inStock: true, shareOfSearch: 37.0, revenue30d: 340000, buyBoxOwner: 'Dark Store Pod' },
      zepto: { price: 699, inStock: true, shareOfSearch: 35.0, revenue30d: 290000, buyBoxOwner: 'Zepto Pod' },
      instamart: { price: 699, inStock: true, shareOfSearch: 28.0, revenue30d: 210000, buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: 699, inStock: true, shareOfSearch: 19.0, revenue30d: 120000, buyBoxOwner: 'JioMart Pod' }
    }
  },
  {
    id: 'sku-slp-1008',
    sku: 'SLP-1008',
    name: 'Microfiber Sleep Pillow',
    category: 'Sleep & Ergonomics',
    subcategory: 'Bed Pillows',
    brand: 'OrthoRest',
    productType: 'Bed Pillow',
    material: 'Microfiber',
    intendedUse: 'General sleep comfort',
    mrp: 799,
    targetMap: 599,
    sellingPrice: 599,
    effectiveAsp: 579,
    activeMarketplaces: ['amazon', 'flipkart', 'myntra', 'blinkit', 'zepto', 'instamart', 'jiomart'],
    stockStatus: 'Active',
    digitalShelfScore: 93,
    shareOfSearchPercent: 41.2,
    rating: 4.6,
    reviewCount: 5120,
    dailyVelocity: 185,
    grossSales30d: 3324450,
    unitsSold30d: 5550,
    revenueAtRisk: 0,
    contentScore: 93,
    imageGalleryCount: 6,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
    defaultMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock: 110,
    motherHubStock: 189000,
    batches: [
      {
        batchNumber: 'BAT-2026-090M',
        skuId: 'SLP-1008',
        productName: 'Microfiber Sleep Pillow',
        manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
        manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
        mfgDate: '2026-05-02',
        expiryDate: '2029-05-02',
        daysRemaining: 985,
        shelfLifeHealthPercent: 100,
        inventoryUnits: 189000,
        inventoryValueInr: 113211000,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: 599, inStock: true, shareOfSearch: 43.0, revenue30d: 1650000, buyBoxOwner: 'OrthoRest Official' },
      flipkart: { price: 599, inStock: true, shareOfSearch: 40.0, revenue30d: 1180000, buyBoxOwner: 'OrthoRest Official' },
      myntra: { price: 599, inStock: true, shareOfSearch: 35.0, revenue30d: 420000, buyBoxOwner: 'OrthoRest Official' },
      blinkit: { price: 599, inStock: true, shareOfSearch: 42.0, revenue30d: 650000, buyBoxOwner: 'Dark Store Pod' },
      zepto: { price: 599, inStock: true, shareOfSearch: 39.0, revenue30d: 520000, buyBoxOwner: 'Zepto Pod' },
      instamart: { price: 599, inStock: true, shareOfSearch: 34.0, revenue30d: 390000, buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: 599, inStock: true, shareOfSearch: 24.0, revenue30d: 210000, buyBoxOwner: 'JioMart Pod' }
    }
  }
];

export const SLEEP_DARK_STORES: DarkStoreInventory[] = [
  // SLP-1001: Contour Memory Foam Cervical Pillow
  {
    storeId: 'BLNK-BLR-HSR-01',
    storeName: 'Blinkit HSR Layout Pod #04',
    city: 'Bengaluru',
    pincode: '560102',
    platform: 'blinkit',
    availableStock: 3,
    status: 'Low Stock',
    deliverySlaMins: 10,
    sellingPrice: 1999,
    lastChecked: '2 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 68500,
    transitHoursFromHub: 1.2,
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    safetyThreshold: 25,
    runwayHours: 1.8,
    dailyVelocity: 28
  },
  {
    storeId: 'ZEPTO-BLR-KOR-04',
    storeName: 'Zepto Koramangala 6th Block Pod',
    city: 'Bengaluru',
    pincode: '560034',
    platform: 'zepto',
    availableStock: 45,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1999,
    lastChecked: '4 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 68500,
    transitHoursFromHub: 1.1,
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    safetyThreshold: 20,
    runwayHours: 36.0,
    dailyVelocity: 24
  },
  {
    storeId: 'INSTA-BLR-IND-02',
    storeName: 'Swiggy Instamart Indiranagar 100ft',
    city: 'Bengaluru',
    pincode: '560038',
    platform: 'instamart',
    availableStock: 28,
    status: 'In Stock',
    deliverySlaMins: 12,
    sellingPrice: 1999,
    lastChecked: '7 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 68500,
    transitHoursFromHub: 1.3,
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    safetyThreshold: 15,
    runwayHours: 28.5,
    dailyVelocity: 18
  },
  {
    storeId: 'BLNK-MUM-AND-01',
    storeName: 'Blinkit Andheri West Lokhandwala Pod',
    city: 'Mumbai',
    pincode: '400053',
    platform: 'blinkit',
    availableStock: 52,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1999,
    lastChecked: '3 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 58000,
    transitHoursFromHub: 1.8,
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    safetyThreshold: 20,
    runwayHours: 42.0,
    dailyVelocity: 22
  },
  {
    storeId: 'ZEPTO-MUM-BAN-02',
    storeName: 'Zepto Bandra West Hill Road Pod',
    city: 'Mumbai',
    pincode: '400050',
    platform: 'zepto',
    availableStock: 38,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1999,
    lastChecked: '9 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 58000,
    transitHoursFromHub: 1.6,
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    safetyThreshold: 20,
    runwayHours: 32.5,
    dailyVelocity: 19
  },
  {
    storeId: 'BLNK-DEL-GUR-01',
    storeName: 'Blinkit DLF CyberCity Phase 2 Pod',
    city: 'Gurgaon',
    pincode: '122002',
    platform: 'blinkit',
    availableStock: 64,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1999,
    lastChecked: '5 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Delhi NCR Hub (Bilaspur)',
    motherHubStock: 58000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    safetyThreshold: 25,
    runwayHours: 48.0,
    dailyVelocity: 26
  },
  {
    storeId: 'INSTA-HYD-JUB-01',
    storeName: 'Swiggy Instamart Jubilee Hills Rd 36',
    city: 'Hyderabad',
    pincode: '500033',
    platform: 'instamart',
    availableStock: 34,
    status: 'In Stock',
    deliverySlaMins: 11,
    sellingPrice: 1999,
    lastChecked: '6 mins ago',
    motherHubId: 'HUB-HYD-04',
    motherHubName: 'Shamshabad Airport Multi-Modal Hub',
    motherHubStock: 68500,
    transitHoursFromHub: 1.5,
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    safetyThreshold: 18,
    runwayHours: 36.0,
    dailyVelocity: 16
  },

  // SLP-1002: Travel Neck Memory Foam Pillow
  {
    storeId: 'BLNK-BLR-KOR-02',
    storeName: 'Blinkit Koramangala 4th Block Pod',
    city: 'Bengaluru',
    pincode: '560034',
    platform: 'blinkit',
    availableStock: 45,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 760,
    lastChecked: '5 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 34000,
    transitHoursFromHub: 1.2,
    sku: 'SLP-1002',
    productName: 'Travel Neck Memory Foam Pillow',
    safetyThreshold: 20,
    runwayHours: 45.0,
    dailyVelocity: 18
  },
  {
    storeId: 'ZEPTO-BLR-IND-01',
    storeName: 'Zepto Indiranagar Metro Pod',
    city: 'Bengaluru',
    pincode: '560038',
    platform: 'zepto',
    availableStock: 32,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 760,
    lastChecked: '7 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 34000,
    transitHoursFromHub: 1.3,
    sku: 'SLP-1002',
    productName: 'Travel Neck Memory Foam Pillow',
    safetyThreshold: 15,
    runwayHours: 38.0,
    dailyVelocity: 15
  },
  {
    storeId: 'INSTA-DEL-GUR-05',
    storeName: 'Swiggy Instamart Golf Course Road',
    city: 'Gurgaon',
    pincode: '122003',
    platform: 'instamart',
    availableStock: 22,
    status: 'In Stock',
    deliverySlaMins: 12,
    sellingPrice: 760,
    lastChecked: '8 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Delhi NCR Hub (Bilaspur)',
    motherHubStock: 34000,
    transitHoursFromHub: 1.5,
    sku: 'SLP-1002',
    productName: 'Travel Neck Memory Foam Pillow',
    safetyThreshold: 15,
    runwayHours: 32.0,
    dailyVelocity: 14
  },
  {
    storeId: 'BLNK-MUM-POW-01',
    storeName: 'Blinkit Powai Galleria Pod',
    city: 'Mumbai',
    pincode: '400076',
    platform: 'blinkit',
    availableStock: 36,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 760,
    lastChecked: '11 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 34000,
    transitHoursFromHub: 1.7,
    sku: 'SLP-1002',
    productName: 'Travel Neck Memory Foam Pillow',
    safetyThreshold: 15,
    runwayHours: 40.0,
    dailyVelocity: 16
  },
  {
    storeId: 'ZEPTO-HYD-BAN-01',
    storeName: 'Zepto Banjara Hills Road 12 Pod',
    city: 'Hyderabad',
    pincode: '500034',
    platform: 'zepto',
    availableStock: 28,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 760,
    lastChecked: '14 mins ago',
    motherHubId: 'HUB-HYD-04',
    motherHubName: 'Shamshabad Airport Multi-Modal Hub',
    motherHubStock: 34000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1002',
    productName: 'Travel Neck Memory Foam Pillow',
    safetyThreshold: 12,
    runwayHours: 34.0,
    dailyVelocity: 13
  },

  // SLP-1003: Alpha Kids Memory Foam Pillow
  {
    storeId: 'BLNK-BLR-WHT-03',
    storeName: 'Blinkit Whitefield ITPL Pod',
    city: 'Bengaluru',
    pincode: '560066',
    platform: 'blinkit',
    availableStock: 30,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1199,
    lastChecked: '6 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 28000,
    transitHoursFromHub: 1.6,
    sku: 'SLP-1003',
    productName: 'Alpha Kids Memory Foam Pillow',
    safetyThreshold: 15,
    runwayHours: 40.0,
    dailyVelocity: 12
  },
  {
    storeId: 'ZEPTO-MUM-POW-03',
    storeName: 'Zepto Powai Hiranandani Pod',
    city: 'Mumbai',
    pincode: '400076',
    platform: 'zepto',
    availableStock: 24,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1199,
    lastChecked: '12 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 28000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1003',
    productName: 'Alpha Kids Memory Foam Pillow',
    safetyThreshold: 15,
    runwayHours: 35.0,
    dailyVelocity: 11
  },
  {
    storeId: 'INSTA-DEL-SAK-01',
    storeName: 'Swiggy Instamart Saket District Centre',
    city: 'Delhi',
    pincode: '110017',
    platform: 'instamart',
    availableStock: 18,
    status: 'In Stock',
    deliverySlaMins: 12,
    sellingPrice: 1199,
    lastChecked: '15 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Delhi NCR Hub (Bilaspur)',
    motherHubStock: 28000,
    transitHoursFromHub: 1.6,
    sku: 'SLP-1003',
    productName: 'Alpha Kids Memory Foam Pillow',
    safetyThreshold: 12,
    runwayHours: 30.0,
    dailyVelocity: 10
  },
  {
    storeId: 'BLNK-HYD-GAC-02',
    storeName: 'Blinkit Gachibowli Financial Dist',
    city: 'Hyderabad',
    pincode: '500032',
    platform: 'blinkit',
    availableStock: 26,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1199,
    lastChecked: '9 mins ago',
    motherHubId: 'HUB-HYD-04',
    motherHubName: 'Shamshabad Airport Multi-Modal Hub',
    motherHubStock: 28000,
    transitHoursFromHub: 1.3,
    sku: 'SLP-1003',
    productName: 'Alpha Kids Memory Foam Pillow',
    safetyThreshold: 14,
    runwayHours: 38.0,
    dailyVelocity: 12
  },

  // SLP-1004: Lumbar Support Cushion
  {
    storeId: 'BLNK-BLR-JAY-02',
    storeName: 'Blinkit Jayanagar 4th Block Pod',
    city: 'Bengaluru',
    pincode: '560011',
    platform: 'blinkit',
    availableStock: 62,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 999,
    lastChecked: '4 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 32000,
    transitHoursFromHub: 1.2,
    sku: 'SLP-1004',
    productName: 'Lumbar Support Cushion',
    safetyThreshold: 20,
    runwayHours: 52.0,
    dailyVelocity: 18
  },
  {
    storeId: 'ZEPTO-DEL-SAK-01',
    storeName: 'Zepto Saket District Centre Pod',
    city: 'Delhi',
    pincode: '110017',
    platform: 'zepto',
    availableStock: 48,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 999,
    lastChecked: '10 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Delhi NCR Hub (Bilaspur)',
    motherHubStock: 32000,
    transitHoursFromHub: 1.8,
    sku: 'SLP-1004',
    productName: 'Lumbar Support Cushion',
    safetyThreshold: 20,
    runwayHours: 42.0,
    dailyVelocity: 16
  },
  {
    storeId: 'INSTA-MUM-LOW-01',
    storeName: 'Swiggy Instamart Lower Parel High St',
    city: 'Mumbai',
    pincode: '400013',
    platform: 'instamart',
    availableStock: 55,
    status: 'In Stock',
    deliverySlaMins: 11,
    sellingPrice: 999,
    lastChecked: '8 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 32000,
    transitHoursFromHub: 1.5,
    sku: 'SLP-1004',
    productName: 'Lumbar Support Cushion',
    safetyThreshold: 18,
    runwayHours: 46.0,
    dailyVelocity: 17
  },
  {
    storeId: 'BLNK-HYD-MAD-01',
    storeName: 'Blinkit Madhapur Cyber Towers Pod',
    city: 'Hyderabad',
    pincode: '500081',
    platform: 'blinkit',
    availableStock: 40,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 999,
    lastChecked: '5 mins ago',
    motherHubId: 'HUB-HYD-04',
    motherHubName: 'Shamshabad Airport Multi-Modal Hub',
    motherHubStock: 32000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1004',
    productName: 'Lumbar Support Cushion',
    safetyThreshold: 15,
    runwayHours: 44.0,
    dailyVelocity: 15
  },

  // SLP-1005: Cooling Gel Memory Foam Pillow
  {
    storeId: 'BLNK-BLR-BEL-01',
    storeName: 'Blinkit Bellandur Outer Ring Road Pod',
    city: 'Bengaluru',
    pincode: '560103',
    platform: 'blinkit',
    availableStock: 80,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1800,
    lastChecked: '2 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 50000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1005',
    productName: 'Cooling Gel Memory Foam Pillow',
    safetyThreshold: 25,
    runwayHours: 64.0,
    dailyVelocity: 25
  },
  {
    storeId: 'ZEPTO-HYD-HIT-02',
    storeName: 'Zepto Hitec City Cyber Towers Pod',
    city: 'Hyderabad',
    pincode: '500081',
    platform: 'zepto',
    availableStock: 55,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1800,
    lastChecked: '6 mins ago',
    motherHubId: 'HUB-HYD-04',
    motherHubName: 'Shamshabad Airport Multi-Modal Hub',
    motherHubStock: 50000,
    transitHoursFromHub: 1.5,
    sku: 'SLP-1005',
    productName: 'Cooling Gel Memory Foam Pillow',
    safetyThreshold: 20,
    runwayHours: 50.0,
    dailyVelocity: 20
  },
  {
    storeId: 'INSTA-MUM-BAN-01',
    storeName: 'Swiggy Instamart Bandra Pali Hill',
    city: 'Mumbai',
    pincode: '400050',
    platform: 'instamart',
    availableStock: 48,
    status: 'In Stock',
    deliverySlaMins: 12,
    sellingPrice: 1800,
    lastChecked: '7 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 50000,
    transitHoursFromHub: 1.6,
    sku: 'SLP-1005',
    productName: 'Cooling Gel Memory Foam Pillow',
    safetyThreshold: 18,
    runwayHours: 42.0,
    dailyVelocity: 18
  },
  {
    storeId: 'BLNK-DEL-VAS-01',
    storeName: 'Blinkit Vasant Kunj Sector C',
    city: 'Delhi',
    pincode: '110070',
    platform: 'blinkit',
    availableStock: 60,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1800,
    lastChecked: '4 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Delhi NCR Hub (Bilaspur)',
    motherHubStock: 50000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1005',
    productName: 'Cooling Gel Memory Foam Pillow',
    safetyThreshold: 22,
    runwayHours: 52.0,
    dailyVelocity: 22
  },

  // SLP-1006: Wedge Support Pillow
  {
    storeId: 'BLNK-BLR-HSR-02',
    storeName: 'Blinkit HSR Sector 2 Pod',
    city: 'Bengaluru',
    pincode: '560102',
    platform: 'blinkit',
    availableStock: 2,
    status: 'Low Stock',
    deliverySlaMins: 10,
    sellingPrice: 1699,
    lastChecked: '1 min ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 48000,
    transitHoursFromHub: 1.2,
    sku: 'SLP-1006',
    productName: 'Wedge Support Pillow',
    safetyThreshold: 15,
    runwayHours: 1.2,
    dailyVelocity: 14
  },
  {
    storeId: 'INSTA-MUM-AND-03',
    storeName: 'Swiggy Instamart Andheri West Pod',
    city: 'Mumbai',
    pincode: '400053',
    platform: 'instamart',
    availableStock: 18,
    status: 'In Stock',
    deliverySlaMins: 12,
    sellingPrice: 1699,
    lastChecked: '5 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 48000,
    transitHoursFromHub: 1.7,
    sku: 'SLP-1006',
    productName: 'Wedge Support Pillow',
    safetyThreshold: 12,
    runwayHours: 24.0,
    dailyVelocity: 9
  },
  {
    storeId: 'ZEPTO-DEL-GAL-01',
    storeName: 'Zepto DLF Phase 4 Galleria Pod',
    city: 'Gurgaon',
    pincode: '122009',
    platform: 'zepto',
    availableStock: 22,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1699,
    lastChecked: '8 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Delhi NCR Hub (Bilaspur)',
    motherHubStock: 48000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1006',
    productName: 'Wedge Support Pillow',
    safetyThreshold: 14,
    runwayHours: 28.0,
    dailyVelocity: 12
  },
  {
    storeId: 'BLNK-HYD-KON-01',
    storeName: 'Blinkit Kondapur RTO Pod',
    city: 'Hyderabad',
    pincode: '500084',
    platform: 'blinkit',
    availableStock: 16,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 1699,
    lastChecked: '12 mins ago',
    motherHubId: 'HUB-HYD-04',
    motherHubName: 'Shamshabad Airport Multi-Modal Hub',
    motherHubStock: 48000,
    transitHoursFromHub: 1.6,
    sku: 'SLP-1006',
    productName: 'Wedge Support Pillow',
    safetyThreshold: 12,
    runwayHours: 22.0,
    dailyVelocity: 10
  },

  // SLP-1007: Car Neck Rest Pillow
  {
    storeId: 'ZEPTO-BLR-JAY-03',
    storeName: 'Zepto Jayanagar 9th Block Pod',
    city: 'Bengaluru',
    pincode: '560069',
    platform: 'zepto',
    availableStock: 23,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 699,
    lastChecked: '8 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 31000,
    transitHoursFromHub: 1.3,
    sku: 'SLP-1007',
    productName: 'Car Neck Rest Pillow',
    safetyThreshold: 15,
    runwayHours: 32.0,
    dailyVelocity: 12
  },
  {
    storeId: 'JIOMART-MUM-BAN-01',
    storeName: 'JioMart Express Bandra Pod',
    city: 'Mumbai',
    pincode: '400050',
    platform: 'jiomart',
    availableStock: 35,
    status: 'In Stock',
    deliverySlaMins: 15,
    sellingPrice: 699,
    lastChecked: '14 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 31000,
    transitHoursFromHub: 1.6,
    sku: 'SLP-1007',
    productName: 'Car Neck Rest Pillow',
    safetyThreshold: 15,
    runwayHours: 42.0,
    dailyVelocity: 10
  },
  {
    storeId: 'BLNK-DEL-SEC-04',
    storeName: 'Blinkit Sector 54 Rapid Metro Pod',
    city: 'Gurgaon',
    pincode: '122011',
    platform: 'blinkit',
    availableStock: 31,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 699,
    lastChecked: '7 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Delhi NCR Hub (Bilaspur)',
    motherHubStock: 31000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1007',
    productName: 'Car Neck Rest Pillow',
    safetyThreshold: 16,
    runwayHours: 36.0,
    dailyVelocity: 14
  },
  {
    storeId: 'INSTA-HYD-BEG-01',
    storeName: 'Swiggy Instamart Begumpet Airport Rd',
    city: 'Hyderabad',
    pincode: '500016',
    platform: 'instamart',
    availableStock: 27,
    status: 'In Stock',
    deliverySlaMins: 11,
    sellingPrice: 699,
    lastChecked: '10 mins ago',
    motherHubId: 'HUB-HYD-04',
    motherHubName: 'Shamshabad Airport Multi-Modal Hub',
    motherHubStock: 31000,
    transitHoursFromHub: 1.3,
    sku: 'SLP-1007',
    productName: 'Car Neck Rest Pillow',
    safetyThreshold: 14,
    runwayHours: 35.0,
    dailyVelocity: 12
  },

  // SLP-1008: Microfiber Sleep Pillow
  {
    storeId: 'BLNK-BLR-MG-01',
    storeName: 'Blinkit MG Road Central Pod',
    city: 'Bengaluru',
    pincode: '560001',
    platform: 'blinkit',
    availableStock: 112,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 599,
    lastChecked: '3 mins ago',
    motherHubId: 'HUB-BLR-01',
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 189000,
    transitHoursFromHub: 1.1,
    sku: 'SLP-1008',
    productName: 'Microfiber Sleep Pillow',
    safetyThreshold: 30,
    runwayHours: 72.0,
    dailyVelocity: 32
  },
  {
    storeId: 'ZEPTO-DEL-VAS-02',
    storeName: 'Zepto Vasant Kunj Pod',
    city: 'Delhi',
    pincode: '110070',
    platform: 'zepto',
    availableStock: 88,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 599,
    lastChecked: '5 mins ago',
    motherHubId: 'HUB-DEL-03',
    motherHubName: 'Delhi NCR Hub (Bilaspur)',
    motherHubStock: 189000,
    transitHoursFromHub: 1.5,
    sku: 'SLP-1008',
    productName: 'Microfiber Sleep Pillow',
    safetyThreshold: 25,
    runwayHours: 60.0,
    dailyVelocity: 28
  },
  {
    storeId: 'INSTA-MUM-DAD-01',
    storeName: 'Swiggy Instamart Dadar Shivaji Park',
    city: 'Mumbai',
    pincode: '400028',
    platform: 'instamart',
    availableStock: 95,
    status: 'In Stock',
    deliverySlaMins: 11,
    sellingPrice: 599,
    lastChecked: '8 mins ago',
    motherHubId: 'HUB-BOM-02',
    motherHubName: 'Mumbai Mega Hub (Bhiwandi)',
    motherHubStock: 189000,
    transitHoursFromHub: 1.7,
    sku: 'SLP-1008',
    productName: 'Microfiber Sleep Pillow',
    safetyThreshold: 28,
    runwayHours: 62.0,
    dailyVelocity: 26
  },
  {
    storeId: 'BLNK-HYD-BAN-02',
    storeName: 'Blinkit Banjara Hills Road No 12',
    city: 'Hyderabad',
    pincode: '500034',
    platform: 'blinkit',
    availableStock: 78,
    status: 'In Stock',
    deliverySlaMins: 10,
    sellingPrice: 599,
    lastChecked: '6 mins ago',
    motherHubId: 'HUB-HYD-04',
    motherHubName: 'Shamshabad Airport Multi-Modal Hub',
    motherHubStock: 189000,
    transitHoursFromHub: 1.4,
    sku: 'SLP-1008',
    productName: 'Microfiber Sleep Pillow',
    safetyThreshold: 24,
    runwayHours: 58.0,
    dailyVelocity: 24
  }
];

// =======================================================
// MOTHER HUBS SKU ALLOCATION MATRIX (Which Hub has what SKU)
// =======================================================
export const MOTHER_HUB_SKU_DATA: MotherHubSkuStock[] = [
  // HUB-BLR-01: Nelamangala
  {
    id: 'MH-BLR-SLP-1001',
    hubId: 'HUB-BLR-01',
    hubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    city: 'Bengaluru, Karnataka',
    pincode: '562123',
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    quantityAvailable: 68500,
    reservedQuantity: 12000,
    safetyStockThreshold: 15000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 24,
    dispatchSlaHours: 1.2
  },
  {
    id: 'MH-BLR-SLP-1002',
    hubId: 'HUB-BLR-01',
    hubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    city: 'Bengaluru, Karnataka',
    pincode: '562123',
    sku: 'SLP-1002',
    productName: 'Travel Neck Memory Foam Pillow',
    quantityAvailable: 34000,
    reservedQuantity: 6000,
    safetyStockThreshold: 8000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 24,
    dispatchSlaHours: 1.2
  },
  {
    id: 'MH-BLR-SLP-1004',
    hubId: 'HUB-BLR-01',
    hubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    city: 'Bengaluru, Karnataka',
    pincode: '562123',
    sku: 'SLP-1004',
    productName: 'Lumbar Support Cushion',
    quantityAvailable: 32000,
    reservedQuantity: 5000,
    safetyStockThreshold: 7000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 24,
    dispatchSlaHours: 1.2
  },
  {
    id: 'MH-BLR-SLP-1005',
    hubId: 'HUB-BLR-01',
    hubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    city: 'Bengaluru, Karnataka',
    pincode: '562123',
    sku: 'SLP-1005',
    productName: 'Cooling Gel Memory Foam Pillow',
    quantityAvailable: 50000,
    reservedQuantity: 8000,
    safetyStockThreshold: 10000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 24,
    dispatchSlaHours: 1.2
  },

  // HUB-BOM-02: Bhiwandi (Mumbai)
  {
    id: 'MH-BOM-SLP-1001',
    hubId: 'HUB-BOM-02',
    hubName: 'Mumbai Mega Hub (Bhiwandi)',
    city: 'Thane / Mumbai, Maharashtra',
    pincode: '421302',
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    quantityAvailable: 58000,
    reservedQuantity: 10000,
    safetyStockThreshold: 12000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 32,
    dispatchSlaHours: 1.6
  },
  {
    id: 'MH-BOM-SLP-1003',
    hubId: 'HUB-BOM-02',
    hubName: 'Mumbai Mega Hub (Bhiwandi)',
    city: 'Thane / Mumbai, Maharashtra',
    pincode: '421302',
    sku: 'SLP-1003',
    productName: 'Alpha Kids Memory Foam Pillow',
    quantityAvailable: 28000,
    reservedQuantity: 5000,
    safetyStockThreshold: 6000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 32,
    dispatchSlaHours: 1.6
  },
  {
    id: 'MH-BOM-SLP-1007',
    hubId: 'HUB-BOM-02',
    hubName: 'Mumbai Mega Hub (Bhiwandi)',
    city: 'Thane / Mumbai, Maharashtra',
    pincode: '421302',
    sku: 'SLP-1007',
    productName: 'Car Neck Rest Pillow',
    quantityAvailable: 31000,
    reservedQuantity: 4500,
    safetyStockThreshold: 5500,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 32,
    dispatchSlaHours: 1.6
  },

  // HUB-DEL-03: Bilaspur (Gurgaon / Delhi NCR)
  {
    id: 'MH-DEL-SLP-1001',
    hubId: 'HUB-DEL-03',
    hubName: 'Delhi NCR Hub (Bilaspur Corridor)',
    city: 'Gurugram, Haryana',
    pincode: '122413',
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    quantityAvailable: 58000,
    reservedQuantity: 9500,
    safetyStockThreshold: 12000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 28,
    dispatchSlaHours: 1.4
  },
  {
    id: 'MH-DEL-SLP-1006',
    hubId: 'HUB-DEL-03',
    hubName: 'Delhi NCR Hub (Bilaspur Corridor)',
    city: 'Gurugram, Haryana',
    pincode: '122413',
    sku: 'SLP-1006',
    productName: 'Wedge Support Pillow',
    quantityAvailable: 22000,
    reservedQuantity: 4000,
    safetyStockThreshold: 5000,
    bufferHealth: 'Adequate',
    connectedDarkStoresCount: 28,
    dispatchSlaHours: 1.4
  },
  {
    id: 'MH-DEL-SLP-1008',
    hubId: 'HUB-DEL-03',
    hubName: 'Delhi NCR Hub (Bilaspur Corridor)',
    city: 'Gurugram, Haryana',
    pincode: '122413',
    sku: 'SLP-1008',
    productName: 'Microfiber Sleep Pillow',
    quantityAvailable: 78000,
    reservedQuantity: 12000,
    safetyStockThreshold: 15000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 28,
    dispatchSlaHours: 1.4
  },

  // HUB-HYD-04: Shamshabad (Hyderabad)
  {
    id: 'MH-HYD-SLP-1005',
    hubId: 'HUB-HYD-04',
    hubName: 'Shamshabad Airport Multi-Modal Hub',
    city: 'Hyderabad, Telangana',
    pincode: '501218',
    sku: 'SLP-1005',
    productName: 'Cooling Gel Memory Foam Pillow',
    quantityAvailable: 44000,
    reservedQuantity: 6000,
    safetyStockThreshold: 8000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 16,
    dispatchSlaHours: 1.5
  },
  {
    id: 'MH-HYD-SLP-1008',
    hubId: 'HUB-HYD-04',
    hubName: 'Shamshabad Airport Multi-Modal Hub',
    city: 'Hyderabad, Telangana',
    pincode: '501218',
    sku: 'SLP-1008',
    productName: 'Microfiber Sleep Pillow',
    quantityAvailable: 52000,
    reservedQuantity: 7000,
    safetyStockThreshold: 9000,
    bufferHealth: 'Optimal',
    connectedDarkStoresCount: 16,
    dispatchSlaHours: 1.5
  }
];

// =========================================================================
// MANUFACTURERS & PRODUCTION PLANTS SUPPLY MATRIX (Which Manufacturer has what)
// =========================================================================
export const MANUFACTURER_SUPPLY_DATA: ManufacturerSupplyInfo[] = [
  {
    id: 'MFG-P1-SLP-1001',
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    plantName: 'Plant 1 - Precision Memory Foam Facility',
    location: 'Peenya Industrial Area, Phase 2, Bengaluru',
    pincode: '560058',
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    factoryFinishedGoodsStock: 42500,
    workInProgressUnits: 18000,
    monthlyCapacityUnits: 65000,
    dailyProductionRate: 2150,
    leadTimeToMotherHubHours: 2.5,
    destinationMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    activeBatchNumber: 'BAT-2026-088C',
    mfgDate: '2026-08-15',
    qualityPassRate: 99.4
  },
  {
    id: 'MFG-P1-SLP-1002',
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    plantName: 'Plant 1 - Precision Memory Foam Facility',
    location: 'Peenya Industrial Area, Phase 2, Bengaluru',
    pincode: '560058',
    sku: 'SLP-1002',
    productName: 'Travel Neck Memory Foam Pillow',
    factoryFinishedGoodsStock: 26000,
    workInProgressUnits: 12000,
    monthlyCapacityUnits: 45000,
    dailyProductionRate: 1500,
    leadTimeToMotherHubHours: 2.5,
    destinationMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    activeBatchNumber: 'BAT-2026-092A',
    mfgDate: '2026-08-16',
    qualityPassRate: 99.1
  },
  {
    id: 'MFG-P1-SLP-1004',
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    plantName: 'Plant 1 - Precision Memory Foam Facility',
    location: 'Peenya Industrial Area, Phase 2, Bengaluru',
    pincode: '560058',
    sku: 'SLP-1004',
    productName: 'Lumbar Support Cushion',
    factoryFinishedGoodsStock: 21500,
    workInProgressUnits: 9500,
    monthlyCapacityUnits: 40000,
    dailyProductionRate: 1300,
    leadTimeToMotherHubHours: 2.5,
    destinationMotherHub: 'Bengaluru Central Mother Hub (Nelamangala)',
    activeBatchNumber: 'BAT-2026-081L',
    mfgDate: '2026-08-14',
    qualityPassRate: 99.6
  },
  {
    id: 'MFG-P2-SLP-1003',
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    plantName: 'Plant 2 - Kids & Ergonomics Center',
    location: 'Chakan Industrial Belt, Phase 2, Pune, MH',
    pincode: '410501',
    sku: 'SLP-1003',
    productName: 'Alpha Kids Memory Foam Pillow',
    factoryFinishedGoodsStock: 18500,
    workInProgressUnits: 8000,
    monthlyCapacityUnits: 35000,
    dailyProductionRate: 1150,
    leadTimeToMotherHubHours: 4.2,
    destinationMotherHub: 'Mumbai Mega Hub (Bhiwandi)',
    activeBatchNumber: 'BAT-2026-074K',
    mfgDate: '2026-08-12',
    qualityPassRate: 99.8
  },
  {
    id: 'MFG-P2-SLP-1005',
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    plantName: 'Plant 2 - Gel Infusion & Cooling Tech Lab',
    location: 'Chakan Industrial Belt, Phase 2, Pune, MH',
    pincode: '410501',
    sku: 'SLP-1005',
    productName: 'Cooling Gel Memory Foam Pillow',
    factoryFinishedGoodsStock: 35000,
    workInProgressUnits: 15000,
    monthlyCapacityUnits: 55000,
    dailyProductionRate: 1800,
    leadTimeToMotherHubHours: 4.2,
    destinationMotherHub: 'Mumbai Mega Hub (Bhiwandi)',
    activeBatchNumber: 'BAT-2026-095G',
    mfgDate: '2026-08-17',
    qualityPassRate: 99.2
  },
  {
    id: 'MFG-P3-SLP-1006',
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    plantName: 'Plant 3 - Heavy Cushion & Specialty Shapes',
    location: 'Manesar Industrial Estate, Sector 8, Gurugram, HR',
    pincode: '122050',
    sku: 'SLP-1006',
    productName: 'Wedge Support Pillow',
    factoryFinishedGoodsStock: 14000,
    workInProgressUnits: 6500,
    monthlyCapacityUnits: 30000,
    dailyProductionRate: 1000,
    leadTimeToMotherHubHours: 1.8,
    destinationMotherHub: 'Delhi NCR Hub (Bilaspur)',
    activeBatchNumber: 'BAT-2026-068W',
    mfgDate: '2026-08-10',
    qualityPassRate: 98.9
  },
  {
    id: 'MFG-P3-SLP-1007',
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    plantName: 'Plant 3 - Heavy Cushion & Specialty Shapes',
    location: 'Manesar Industrial Estate, Sector 8, Gurugram, HR',
    pincode: '122050',
    sku: 'SLP-1007',
    productName: 'Car Neck Rest Pillow',
    factoryFinishedGoodsStock: 22000,
    workInProgressUnits: 10500,
    monthlyCapacityUnits: 45000,
    dailyProductionRate: 1450,
    leadTimeToMotherHubHours: 1.8,
    destinationMotherHub: 'Delhi NCR Hub (Bilaspur)',
    activeBatchNumber: 'BAT-2026-085C',
    mfgDate: '2026-08-16',
    qualityPassRate: 99.5
  },
  {
    id: 'MFG-P3-SLP-1008',
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    plantName: 'Plant 3 - Fiber Carding & Pillow Encasement Unit',
    location: 'Manesar Industrial Estate, Sector 8, Gurugram, HR',
    pincode: '122050',
    sku: 'SLP-1008',
    productName: 'Microfiber Sleep Pillow',
    factoryFinishedGoodsStock: 48000,
    workInProgressUnits: 22000,
    monthlyCapacityUnits: 80000,
    dailyProductionRate: 2600,
    leadTimeToMotherHubHours: 1.8,
    destinationMotherHub: 'Delhi NCR Hub (Bilaspur)',
    activeBatchNumber: 'BAT-2026-090M',
    mfgDate: '2026-08-18',
    qualityPassRate: 99.7
  }
];

export const SLEEP_MAP_BREACHES: MAPBreach[] = [
  {
    id: 'alt-map-SLP-1001',
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    channel: 'flipkart',
    violatingSeller: 'DiscountDeals_IN (Breach)',
    enforcedMap: 1499,
    violatedPrice: 1399,
    discountPercent: 6.7,
    breachDurationHours: 4.5,
    status: 'Active Breach',
    evidenceUrl: 'https://flipkart.com/dp/B0DXYZ981',
    complianceAction: 'Auto Cease-and-Desist Notice Drafted',
    estimatedLossInr: 24500,
    priceGapInr: 100,
    sellerName: 'DiscountDeals_IN (Breach)',
    suggestedPlaybook: 'Auto-trigger Cease & Desist via Brand Registry & BuyBox injunction.'
  },
  {
    id: 'alt-map-SLP-1002',
    sku: 'SLP-1002',
    productName: 'Travel Neck Memory Foam Pillow',
    channel: 'amazon',
    violatingSeller: 'FastRetail Direct (3P)',
    enforcedMap: 749,
    violatedPrice: 679,
    discountPercent: 9.3,
    breachDurationHours: 8.2,
    status: 'Active Breach',
    evidenceUrl: 'https://amazon.in/dp/B0DXYZ982',
    complianceAction: 'Escalate to Amazon Brand Protection portal',
    estimatedLossInr: 18900,
    priceGapInr: 70,
    sellerName: 'FastRetail Direct (3P)',
    suggestedPlaybook: 'Issue automated price violation notice and restrict unauthorized seller.'
  },
  {
    id: 'alt-map-SLP-1003',
    sku: 'SLP-1003',
    productName: 'Alpha Kids Memory Foam Pillow',
    channel: 'myntra',
    violatingSeller: 'KidzComfort SuperStore',
    enforcedMap: 1199,
    violatedPrice: 1049,
    discountPercent: 12.5,
    breachDurationHours: 14.1,
    status: 'Active Breach',
    evidenceUrl: 'https://myntra.com/p/SLP-1003',
    complianceAction: 'Brand Registry Legal Notice Queued',
    estimatedLossInr: 31200,
    priceGapInr: 150,
    sellerName: 'KidzComfort SuperStore',
    suggestedPlaybook: 'Trigger automated compliance warning and suspend distributor discount.'
  },
  {
    id: 'alt-map-SLP-1005',
    sku: 'SLP-1005',
    productName: 'Cooling Gel Memory Foam Pillow',
    channel: 'blinkit',
    violatingSeller: 'QuickCart Express',
    enforcedMap: 1899,
    violatedPrice: 1749,
    discountPercent: 7.9,
    breachDurationHours: 3.8,
    status: 'Active Breach',
    evidenceUrl: 'https://blinkit.com/pr/SLP-1005',
    complianceAction: 'Quick Commerce Price Correction Alert',
    estimatedLossInr: 27400,
    priceGapInr: 150,
    sellerName: 'QuickCart Express',
    suggestedPlaybook: 'Direct instant inventory rebalance & platform MAP enforcement.'
  },
  {
    id: 'alt-map-SLP-1006',
    sku: 'SLP-1006',
    productName: 'Orthopedic Wedge Bed Pillow',
    channel: 'amazon',
    violatingSeller: 'PrimeDealz Direct',
    enforcedMap: 2299,
    violatedPrice: 2099,
    discountPercent: 8.7,
    breachDurationHours: 6.5,
    status: 'Active Breach',
    evidenceUrl: 'https://amazon.in/dp/B0DXYZ986',
    complianceAction: 'Cease & Desist Legal Notice Sent',
    estimatedLossInr: 45000,
    priceGapInr: 200,
    sellerName: 'PrimeDealz Direct',
    suggestedPlaybook: 'Issue automated legal notice via Brand Registry and request listing suspension.'
  },
  {
    id: 'alt-map-SLP-1008',
    sku: 'SLP-1008',
    productName: 'Luxury Bamboo Charcoal Pillow',
    channel: 'flipkart',
    violatingSeller: 'SuperSeller India 3P',
    enforcedMap: 2799,
    violatedPrice: 2599,
    discountPercent: 7.1,
    breachDurationHours: 11.4,
    status: 'Active Breach',
    evidenceUrl: 'https://flipkart.com/dp/B0DXYZ988',
    complianceAction: 'BuyBox Injunction & MAP Notice Queued',
    estimatedLossInr: 52000,
    priceGapInr: 200,
    sellerName: 'SuperSeller India 3P',
    suggestedPlaybook: 'Automated BuyBox rotation block and authorized distributor enforcement.'
  }
];

export function buildChannelPricingFromCatalog(catalog: SKUListing[]): ChannelPricingItem[] {
  const list: ChannelPricingItem[] = [];
  catalog.forEach((s) => {
    if (s.marketplacePrices) {
      Object.entries(s.marketplacePrices).forEach(([mp, data]) => {
        const isBreached = data.price < s.targetMap;
        list.push({
          id: `CP-${s.sku}-${mp.toUpperCase()}`,
          sku: s.sku,
          productName: s.name,
          marketplace: mp.toLowerCase() as MarketplaceId,
          currentSellingPrice: data.price,
          targetMap: s.targetMap,
          mapBreached: isBreached,
          priceDelta: data.price - s.targetMap,
          inStock: data.inStock,
          buyBoxOwner: data.buyBoxOwner || (isBreached ? 'DiscountDeals_IN (Breach)' : 'OrthoRest Official'),
          shareOfSearch: data.shareOfSearch,
          revenue30d: data.revenue30d,
          status: isBreached ? 'Active Breach' : 'Compliant',
          complianceAction: isBreached ? 'Auto Cease-and-Desist Notice Drafted' : 'Active - Price Protected'
        });
      });
    }
  });
  return list;
}

export const SLEEP_CHANNEL_PRICING: ChannelPricingItem[] = buildChannelPricingFromCatalog(SLEEP_SKU_CATALOG);

export const SLEEP_ALERTS: AlertAnomaly[] = [
  {
    id: 'alt-oos-BLNK-B',
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    marketplace: 'blinkit',
    severity: 'Critical',
    status: 'New',
    timestamp: '2026-08-19T16:00:00Z',
    timeDisplay: '12 mins ago',
    summary: 'Micro-OOS Risk: Stock dropped to 3 units (0.5 hrs cover) for Contour Memory Foam Cervical Pillow (SLP-1001).',
    revenueAtRiskInr: 148500,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
    darkStoreStock: 3,
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 184500,
    motherHubPincode: '562123',
    batchNumber: 'BAT-2026-088C',
    mfgDate: '2026-04-10',
    expiryDate: '2029-04-10',
    shelfLifeHealth: 98,
    transferLeadTimeHours: 1.2,
    recommendedPlaybook: 'Autonomous 250 Units Stock Transfer Dispatch',
    transferUnitsSuggested: 250,
    logisticsPartner: 'BlueDart Express Intra-City Corridor',
    targetOwnerEmail: 'vikashr984@gmail.com'
  },
  {
    id: 'alt-map-SLP-10',
    sku: 'SLP-1001',
    productName: 'Contour Memory Foam Cervical Pillow',
    marketplace: 'flipkart',
    severity: 'High',
    status: 'New',
    timestamp: '2026-08-19T16:15:00Z',
    timeDisplay: '35 mins ago',
    summary: 'MAP Price Breach on FLIPKART: Contour Memory Foam Cervical Pillow selling at ₹1,399 (Target MAP ₹1,499, -₹100 gap).',
    revenueAtRiskInr: 207200,
    manufacturerName: 'OrthoRest FoamTech India Pvt Ltd',
    manufacturerPlant: 'Plant 1 - Peenya Industrial Area, Bengaluru, KA',
    darkStoreStock: 45,
    motherHubName: 'Bengaluru Central Mother Hub (Nelamangala)',
    motherHubStock: 184500,
    motherHubPincode: '562123',
    batchNumber: 'BAT-2026-088C',
    mfgDate: '2026-04-10',
    expiryDate: '2029-04-10',
    shelfLifeHealth: 98,
    transferLeadTimeHours: 1.2,
    recommendedPlaybook: 'Issue automated Cease-and-Desist notice',
    transferUnitsSuggested: 0,
    logisticsPartner: 'N/A',
    targetOwnerEmail: 'vikashr984@gmail.com'
  }
];

// ==========================================
// EXCEL EXPORT & IMPORT ENGINE
// ==========================================

export function exportDatasetToExcelWorkbook(
  skus: SKUListing[],
  darkStores: DarkStoreInventory[],
  mapBreaches: MAPBreach[],
  alerts: AlertAnomaly[],
  channelPricing?: ChannelPricingItem[],
  motherHubSkuStock?: MotherHubSkuStock[],
  manufacturerSupply?: ManufacturerSupplyInfo[]
): void {
  const wb = XLSX.utils.book_new();

  // Tab 1: SKU Master
  const skuRows = skus.map((s) => ({
    SKU: s.sku,
    ProductName: s.name,
    ProductType: s.productType || s.subcategory,
    Material: s.material || 'Memory Foam',
    IntendedUse: s.intendedUse || 'Ergonomic Support',
    MRP_INR: s.mrp,
    Target_MAP_INR: s.targetMap,
    SellingPrice_INR: s.sellingPrice,
    EffectiveASP_INR: s.effectiveAsp,
    StockStatus: s.stockStatus,
    DarkStoreStock: s.darkStoreStock,
    MotherHubStock: s.motherHubStock,
    DigitalShelfScore: s.digitalShelfScore,
    ShareOfSearchPct: s.shareOfSearchPercent,
    Rating: s.rating,
    ReviewCount: s.reviewCount,
    DailyVelocityUnits: s.dailyVelocity,
    GrossSales30d_INR: s.grossSales30d,
    UnitsSold30d: s.unitsSold30d,
    RevenueAtRisk_INR: s.revenueAtRisk,
    ROAS: s.roas ?? 4.2,
    ACOS: s.acos ?? 18.5,
    TACOS: s.tacos ?? 12.1,
    AdCost_INR: s.adCost30d ?? Math.round(s.grossSales30d * 0.12),
    ManufacturerName: s.manufacturerName,
    ManufacturerPlant: s.manufacturerPlant,
    DefaultMotherHub: s.defaultMotherHub
  }));
  const wsSku = XLSX.utils.json_to_sheet(skuRows);
  XLSX.utils.book_append_sheet(wb, wsSku, '1_SKU_Master');

  // Tab 2: Dark Stores Inventory (all pods and SKUs)
  const storeRows = darkStores.map((d) => ({
    StoreID: d.storeId,
    StoreName: d.storeName,
    City: d.city,
    Pincode: d.pincode,
    Platform: String(d.platform).toUpperCase(),
    SKU: d.sku || 'SLP-1001',
    ProductName: d.productName || 'Sleep Pillow SKU',
    AvailableStockUnits: d.availableStock,
    SafetyThresholdUnits: d.safetyThreshold ?? 20,
    RunwayHours: d.runwayHours ?? 36,
    DailyVelocityUnits: d.dailyVelocity ?? 20,
    Status: d.status,
    DeliverySLA_Mins: d.deliverySlaMins,
    SellingPrice_INR: d.sellingPrice,
    ConnectedMotherHub: d.motherHubName,
    MotherHubStockUnits: d.motherHubStock,
    TransitHoursFromHub: d.transitHoursFromHub,
    LastChecked: d.lastChecked
  }));
  const wsStores = XLSX.utils.json_to_sheet(storeRows);
  XLSX.utils.book_append_sheet(wb, wsStores, '2_Dark_Stores_Inventory');

  // Tab 3: Channel Pricing & MAP
  const pricingRows: any[] = [];
  if (channelPricing && channelPricing.length > 0) {
    channelPricing.forEach((cp) => {
      pricingRows.push({
        SKU: cp.sku,
        ProductName: cp.productName,
        Marketplace: String(cp.marketplace).toUpperCase(),
        CurrentSellingPrice_INR: cp.currentSellingPrice,
        Target_MAP_INR: cp.targetMap,
        MAP_Breached: cp.mapBreached ? 'YES (BREACH)' : 'NO',
        PriceDelta_INR: cp.priceDelta,
        InStock: cp.inStock ? 'TRUE' : 'FALSE',
        BuyBoxOwner: cp.buyBoxOwner,
        ShareOfSearchPct: cp.shareOfSearch,
        Revenue30d_INR: cp.revenue30d
      });
    });
  } else {
    skus.forEach((s) => {
      Object.entries(s.marketplacePrices || {}).forEach(([mp, data]) => {
        pricingRows.push({
          SKU: s.sku,
          ProductName: s.name,
          Marketplace: mp.toUpperCase(),
          CurrentSellingPrice_INR: data.price,
          Target_MAP_INR: s.targetMap,
          MAP_Breached: data.price < s.targetMap ? 'YES (BREACH)' : 'NO',
          PriceDelta_INR: data.price - s.targetMap,
          InStock: data.inStock ? 'TRUE' : 'FALSE',
          BuyBoxOwner: data.buyBoxOwner || (data.price < s.targetMap ? 'DiscountDeals_IN (Breach)' : 'OrthoRest Official'),
          ShareOfSearchPct: data.shareOfSearch,
          Revenue30d_INR: data.revenue30d
        });
      });
    });
  }
  const wsPricing = XLSX.utils.json_to_sheet(pricingRows);
  XLSX.utils.book_append_sheet(wb, wsPricing, '3_Channel_Pricing_MAP');

  // Tab 4: Active Triggers & Alerts Log
  const alertRows = alerts.map((a) => ({
    AlertID: a.id,
    SKU: a.sku,
    ProductName: a.productName,
    Marketplace: a.marketplace.toUpperCase(),
    Severity: a.severity,
    Status: a.status,
    Timestamp: a.timestamp,
    Summary: a.summary,
    RevenueAtRisk_INR: a.revenueAtRiskInr,
    RecommendedPlaybook: a.recommendedPlaybook,
    TransferUnitsSuggested: a.transferUnitsSuggested,
    TargetEmail: a.targetOwnerEmail
  }));
  const wsAlerts = XLSX.utils.json_to_sheet(alertRows);
  XLSX.utils.book_append_sheet(wb, wsAlerts, '4_Triggers_Alerts_Log');

  // Tab 5: Mother Hubs SKU Allocation Matrix
  const activeHubs = motherHubSkuStock && motherHubSkuStock.length > 0 ? motherHubSkuStock : MOTHER_HUB_SKU_DATA;
  const hubRows = activeHubs.map((h) => ({
    HubID: h.hubId,
    HubName: h.hubName,
    CityRegion: h.city,
    Pincode: h.pincode,
    SKU: h.sku,
    ProductName: h.productName,
    QuantityAvailableUnits: h.quantityAvailable,
    ReservedQuantityUnits: h.reservedQuantity,
    SafetyStockThreshold: h.safetyStockThreshold,
    BufferHealth: h.bufferHealth,
    ConnectedDarkStoresCount: h.connectedDarkStoresCount,
    DispatchSLA_Hours: h.dispatchSlaHours
  }));
  const wsHubs = XLSX.utils.json_to_sheet(hubRows);
  XLSX.utils.book_append_sheet(wb, wsHubs, '5_Mother_Hubs_Inventory');

  // Tab 6: Manufacturers & Plants Supply Matrix
  const activeMfg = manufacturerSupply && manufacturerSupply.length > 0 ? manufacturerSupply : MANUFACTURER_SUPPLY_DATA;
  const mfgRows = activeMfg.map((m) => ({
    ManufacturerName: m.manufacturerName,
    PlantName: m.plantName,
    LocationCity: m.location,
    Pincode: m.pincode,
    SKU: m.sku,
    ProductName: m.productName,
    FactoryFinishedGoodsStockUnits: m.factoryFinishedGoodsStock,
    WorkInProgressUnits: m.workInProgressUnits,
    MonthlyCapacityUnits: m.monthlyCapacityUnits,
    DailyProductionRate: m.dailyProductionRate,
    LeadTimeToMotherHubHours: m.leadTimeToMotherHubHours,
    DestinationMotherHub: m.destinationMotherHub,
    ActiveBatchNumber: m.activeBatchNumber,
    MfgDate: m.mfgDate,
    QualityPassRatePct: m.qualityPassRate
  }));
  const wsMfg = XLSX.utils.json_to_sheet(mfgRows);
  XLSX.utils.book_append_sheet(wb, wsMfg, '6_Manufacturers_Supply');

  // Trigger browser download
  XLSX.writeFile(wb, `AgileSolutions_SleepPillow_MasterDataset_${new Date().toISOString().slice(0, 10)}.xlsx`);
}

export function exportTransferLogsToExcel(transferLogs: StockTransferLog[]): void {
  const wb = XLSX.utils.book_new();
  const logRows = transferLogs.map((log) => ({
    LogID: log.id,
    Timestamp: log.timestamp,
    SKU: log.sku,
    ProductName: log.productName,
    SourceMotherHub: log.sourceMotherHub,
    TargetDarkStore: log.targetDarkStore,
    UnitsTransferred: log.unitsTransferred,
    CarrierPartner: log.carrier,
    TrackingNumber: log.trackingNumber,
    Status: log.status,
    ExecutedBy: log.executedBy
  }));
  const wsLogs = XLSX.utils.json_to_sheet(logRows);
  XLSX.utils.book_append_sheet(wb, wsLogs, '7_Stock_Transfer_Audit_Logs');
  XLSX.writeFile(wb, `AgileSolutions_StockTransfer_AuditLogs_${new Date().toISOString().slice(0, 10)}.xlsx`);
}

export function exportAlertsLogToExcel(alerts: AlertAnomaly[]): void {
  const wb = XLSX.utils.book_new();
  const alertRows = alerts.map((alert) => ({
    AlertID: alert.id,
    SKU: alert.sku,
    ProductName: alert.productName,
    Marketplace: alert.marketplace,
    Severity: alert.severity,
    Status: alert.status,
    Timestamp: alert.timestamp,
    RevenueAtRiskINR: alert.revenueAtRiskInr,
    Summary: alert.summary,
    TransferUnitsSuggested: alert.transferUnitsSuggested,
    TargetOwnerEmail: alert.targetOwnerEmail,
    RecommendedPlaybook: alert.recommendedPlaybook
  }));
  const wsAlerts = XLSX.utils.json_to_sheet(alertRows);
  XLSX.utils.book_append_sheet(wb, wsAlerts, '4_Triggers_Alerts_Log');
  XLSX.writeFile(wb, `AgileSolutions_TriggersAlerts_Log_${new Date().toISOString().slice(0, 10)}.xlsx`);
}

export function createDynamicSkuFromRow(r: any, index: number): SKUListing {
  const skuCode = String(
    r.SKU || r.sku || r.Sku || r.SkuCode || r['SKU Code'] || r['Item Code'] || r['Product Code'] || r.Code || r.Id || r.id || `SKU-${index + 1}`
  ).trim();

  const name = String(
    r.ProductName || r.productName || r['Product Name'] || r['Item Name'] || r.Item || r.item || r.Title || r.title || r.Name || r.name || r.Description || r.description || `Catalog SKU ${skuCode}`
  ).trim();

  const category = String(
    r.Category || r.category || r.Subcategory || r.subcategory || r.ProductType || r.productType || r.Department || r.Type || 'General Merchandise'
  ).trim();

  const brand = String(
    r.Brand || r.brand || r.Manufacturer || r.manufacturer || 'Brand'
  ).trim();

  const mrp = Number(r.MRP_INR ?? r.mrp ?? r.MRP ?? r['MRP (INR)'] ?? r['Max Retail Price'] ?? r.OriginalPrice ?? r.ListPrice ?? r.Price ?? 1499) || 1499;
  const sellingPrice = Number(r.SellingPrice_INR ?? r.sellingPrice ?? r.Price ?? r.price ?? r['Selling Price'] ?? r['Live Price'] ?? r.Rate ?? mrp * 0.85) || mrp;
  const targetMap = Number(r.Target_MAP_INR ?? r.targetMap ?? r.MAP ?? r['Target MAP'] ?? r['Minimum Advertised Price'] ?? sellingPrice) || sellingPrice;
  const effectiveAsp = Number(r.EffectiveASP_INR ?? r.effectiveAsp ?? r.ASP ?? r['Effective ASP'] ?? sellingPrice * 0.96) || sellingPrice;

  const rawDarkStock = r.DarkStoreStock ?? r.Dark_Store_Stock ?? r['Dark Store Stock'] ?? r.PodStock ?? r.POD_STOCK ?? r['Pod Stock'] ?? r['POD STOCK'] ?? r.darkStoreStock ?? r.Stock ?? r.stock ?? r.Quantity ?? r.Qty ?? r['Available Qty'] ?? 20;
  const rawHubStock = r.MotherHubStock ?? r.Mother_Hub_Stock ?? r['Mother Hub Stock'] ?? r.HubStock ?? r.HUB_STOCK ?? r['Hub Stock'] ?? r['HUB STOCK'] ?? r.motherHubStock ?? r.WarehouseStock ?? r['Warehouse Stock'] ?? 5000;

  const darkStoreStock = Number(rawDarkStock) || 0;
  const motherHubStock = Number(rawHubStock) || 0;
  const dailyVelocity = Number(r.DailyVelocityUnits ?? r.dailyVelocity ?? r.DailyVelocity ?? r.Velocity ?? r.SalesVelocity ?? 30) || 30;
  const grossSales30d = Number(r.GrossSales30d_INR ?? r.grossSales30d ?? r['30D Gross Sales'] ?? r.Revenue ?? r.GrossSales ?? (sellingPrice * dailyVelocity * 30)) || (sellingPrice * 50);

  const rating = Number(r.Rating ?? r.rating ?? 4.5) || 4.5;
  const reviewCount = Number(r.ReviewCount ?? r.reviewCount ?? r.Reviews ?? 450) || 450;
  const digitalShelfScore = Number(r.DigitalShelfScore ?? r.digitalShelfScore ?? r['Shelf Score'] ?? 88) || 88;
  const shareOfSearchPercent = Number(r.ShareOfSearch ?? r.shareOfSearchPercent ?? r['Share of Search'] ?? 35) || 35;

  const rawRevenueAtRisk = r.RevenueAtRisk_INR ?? r.RevenueAtRisk ?? r.revenueAtRisk ?? r['Revenue At Risk'] ?? r['RevenueAtRisk (INR)'];
  const revenueAtRisk = rawRevenueAtRisk !== undefined && rawRevenueAtRisk !== null && rawRevenueAtRisk !== ''
    ? Number(rawRevenueAtRisk)
    : (darkStoreStock < 10 ? Math.round(sellingPrice * dailyVelocity * Math.max(1, 10 - darkStoreStock) / 3) : 0);

  return {
    id: `sku-${skuCode.toLowerCase().replace(/[^a-z0-9_-]/g, '-')}`,
    sku: skuCode,
    name,
    category,
    subcategory: category,
    brand,
    productType: category,
    material: r.Material || r.material || 'Standard',
    intendedUse: r.IntendedUse || r.intendedUse || 'Commercial',
    mrp,
    targetMap,
    sellingPrice,
    effectiveAsp,
    activeMarketplaces: ['amazon', 'flipkart', 'blinkit', 'zepto', 'instamart'],
    stockStatus: darkStoreStock === 0 ? 'Out Of Stock' : darkStoreStock < 10 ? 'Low Stock' : 'Active',
    digitalShelfScore,
    shareOfSearchPercent,
    rating,
    reviewCount,
    dailyVelocity,
    grossSales30d,
    unitsSold30d: Math.round(dailyVelocity * 30),
    revenueAtRisk,
    roas: r.ROAS !== undefined || r.roas !== undefined ? Number(r.ROAS ?? r.roas) : undefined,
    acos: r.ACOS !== undefined || r.acos !== undefined ? Number(r.ACOS ?? r.acos) : undefined,
    tacos: r.TACOS !== undefined || r.tacos !== undefined ? Number(r.TACOS ?? r.tacos) : undefined,
    adCost30d: r.AdCost_INR !== undefined || r.AdCost !== undefined || r.adCost !== undefined || r.AdSpend !== undefined ? Number(r.AdCost_INR ?? r.AdCost ?? r.adCost ?? r.AdSpend) : undefined,
    contentScore: 92,
    imageGalleryCount: 6,
    hasAplus: true,
    bulletPointsCount: 5,
    manufacturerName: r.ManufacturerName || r.manufacturerName || `${brand} Manufacturing Facilities`,
    manufacturerPlant: r.ManufacturerPlant || r.manufacturerPlant || 'Central Industrial Area',
    defaultMotherHub: r.DefaultMotherHub || r.defaultMotherHub || r['Default Mother Hub'] || r['Mother Hub'] || 'Bengaluru Central Mother Hub (Nelamangala)',
    darkStoreStock,
    motherHubStock,
    batches: [
      {
        batchNumber: `LOT-${skuCode.replace(/[^a-zA-Z0-9]/g, '')}-2026`,
        skuId: skuCode,
        productName: name,
        manufacturerName: r.ManufacturerName || `${brand} Facility`,
        manufacturerPlant: 'Central Production Unit',
        mfgDate: '2026-02-01',
        expiryDate: '2028-02-01',
        daysRemaining: 710,
        shelfLifeHealthPercent: 95,
        inventoryUnits: motherHubStock,
        inventoryValueInr: motherHubStock * sellingPrice,
        status: 'Fresh'
      }
    ],
    marketplacePrices: {
      amazon: { price: sellingPrice, inStock: darkStoreStock > 0, shareOfSearch: shareOfSearchPercent, revenue30d: Math.round(grossSales30d * 0.45), buyBoxOwner: `${brand} Official` },
      flipkart: { price: sellingPrice, inStock: darkStoreStock > 0, shareOfSearch: Math.max(15, shareOfSearchPercent - 5), revenue30d: Math.round(grossSales30d * 0.25), buyBoxOwner: 'Authorized Partner' },
      myntra: { price: sellingPrice, inStock: darkStoreStock > 0, shareOfSearch: Math.max(10, shareOfSearchPercent - 10), revenue30d: Math.round(grossSales30d * 0.10), buyBoxOwner: `${brand} Official` },
      blinkit: { price: sellingPrice, inStock: darkStoreStock > 0, shareOfSearch: Math.max(20, shareOfSearchPercent + 5), revenue30d: Math.round(grossSales30d * 0.18), buyBoxOwner: 'Quick Commerce Pod' },
      zepto: { price: sellingPrice, inStock: darkStoreStock > 0, shareOfSearch: Math.max(15, shareOfSearchPercent), revenue30d: Math.round(grossSales30d * 0.12), buyBoxOwner: 'Zepto Pod' },
      instamart: { price: sellingPrice, inStock: darkStoreStock > 0, shareOfSearch: Math.max(12, shareOfSearchPercent - 2), revenue30d: Math.round(grossSales30d * 0.08), buyBoxOwner: 'Instamart Pod' },
      jiomart: { price: sellingPrice, inStock: darkStoreStock > 0, shareOfSearch: Math.max(8, shareOfSearchPercent - 15), revenue30d: Math.round(grossSales30d * 0.05), buyBoxOwner: 'JioMart Hub' }
    }
  };
}

// Parse Workbook into multi-sheet datasets
export function parseWorkbookData(wb: XLSX.WorkBook): {
  skus: SKUListing[];
  darkStores?: DarkStoreInventory[];
  channelPricing?: ChannelPricingItem[];
  mapBreaches?: MAPBreach[];
  alerts?: AlertAnomaly[];
  motherHubSkuStock?: MotherHubSkuStock[];
  manufacturerSupply?: ManufacturerSupplyInfo[];
  rawRowCount: number;
  sheetNames: string[];
} {
  let parsedSkus: SKUListing[] = [];
  let parsedStores: DarkStoreInventory[] = [];
  let parsedChannelPricing: ChannelPricingItem[] = [];
  let parsedMapBreaches: MAPBreach[] = [];
  let parsedAlerts: AlertAnomaly[] = [];
  let parsedMotherHubs: MotherHubSkuStock[] = [];
  let parsedMfgSupply: ManufacturerSupplyInfo[] = [];
  let rawRowCount = 0;

  // 1. Check for SKU sheet or first sheet
  const skuSheetName = wb.SheetNames.find((n) => n.toLowerCase().includes('sku') || n.toLowerCase().includes('master') || n.toLowerCase().includes('1_')) || wb.SheetNames[0];
  if (skuSheetName && wb.Sheets[skuSheetName]) {
    const ws = wb.Sheets[skuSheetName];
    const rows: any[] = XLSX.utils.sheet_to_json(ws);
    rawRowCount = rows.length;
    if (rows.length > 0) {
      parsedSkus = rows.map((r, idx) => createDynamicSkuFromRow(r, idx));
    }
  }

  // 2. Check if dark stores tab exists
  const darkStoreSheetName = wb.SheetNames.find((n) => n.toLowerCase().includes('dark') || n.toLowerCase().includes('store') || n.toLowerCase().includes('inventory') || n.toLowerCase().includes('2_') || n.toLowerCase().includes('pod'));
  if (darkStoreSheetName && wb.Sheets[darkStoreSheetName]) {
    const dsWs = wb.Sheets[darkStoreSheetName];
    const dsRows: any[] = XLSX.utils.sheet_to_json(dsWs);
    if (dsRows.length > 0) {
      parsedStores = dsRows.map((r) => {
        const stock = Number(r.AvailableStockUnits ?? r.availableStock ?? r.Stock ?? r.stock ?? r.Quantity ?? 0);
        return {
          storeId: String(r.StoreID || r.storeId || `POD-${Math.floor(100 + Math.random() * 900)}`),
          storeName: String(r.StoreName || r.storeName || 'Local Dark Store Pod'),
          city: String(r.City || r.city || 'Bengaluru'),
          pincode: String(r.Pincode || r.pincode || '560102'),
          platform: String(r.Platform || r.platform || 'blinkit').toLowerCase() as MarketplaceId,
          availableStock: stock,
          status: stock === 0 ? 'Out Of Stock' : stock < 5 ? 'Low Stock' : 'In Stock',
          deliverySlaMins: Number(r.DeliverySLA_Mins ?? r.DeliverySlaMins ?? r.deliverySlaMins ?? 10),
          sellingPrice: Number(r.SellingPrice_INR ?? r.sellingPrice ?? 1499),
          safetyThreshold: Number(r.SafetyThresholdUnits ?? r.safetyThreshold ?? 20),
          dailyVelocity: Number(r.DailyVelocityUnits ?? r.dailyVelocity ?? 20),
          runwayHours: Number(r.RunwayHours ?? r.runwayHours ?? 36),
          lastChecked: String(r.LastChecked || r.lastChecked || 'Just now'),
          motherHubId: String(r.MotherHubID || r.motherHubId || 'HUB-BLR-01'),
          motherHubName: String(r.ConnectedMotherHub || r.motherHubName || 'Bengaluru Central Mother Hub'),
          motherHubStock: Number(r.MotherHubStockUnits ?? r.motherHubStock ?? 50000),
          transitHoursFromHub: Number(r.TransitHoursFromHub ?? r.transitHoursFromHub ?? 1.2),
          sku: String(r.SKU || r.sku || parsedSkus[0]?.sku || 'SLP-1001'),
          productName: String(r.ProductName || r.productName || 'Sleep Pillow SKU')
        };
      });
    }
  }

  // 3. Check if MAP Pricing tab exists (Channel Pricing & MAP)
  const pricingSheetName = wb.SheetNames.find((n) => n.toLowerCase().includes('price') || n.toLowerCase().includes('map') || n.toLowerCase().includes('channel') || n.toLowerCase().includes('3_'));
  if (pricingSheetName && wb.Sheets[pricingSheetName]) {
    const pWs = wb.Sheets[pricingSheetName];
    const pRows: any[] = XLSX.utils.sheet_to_json(pWs);
    if (pRows.length > 0) {
      pRows.forEach((r, pIdx) => {
        const sku = String(r.SKU || r.sku || `SLP-${1001 + Math.floor(pIdx / 7)}`);
        const matchedSku = parsedSkus.find(s => s.sku.toLowerCase() === sku.toLowerCase());
        const productName = String(r.ProductName || r.productName || r.Product || matchedSku?.name || 'Product');
        const rawMarketplace = String(r.Marketplace || r.marketplace || r.Channel || r.channel || 'amazon').toLowerCase().trim();
        const currentSellingPrice = Number(r.CurrentSellingPrice_INR ?? r.CurrentSellingPrice ?? r.sellingPrice ?? r.Price ?? r.price ?? 0);
        const targetMap = Number(r.Target_MAP_INR ?? r.Target_MAP ?? r.targetMap ?? r.MAP ?? r.map ?? (matchedSku?.targetMap || currentSellingPrice));
        const mapBreachedStr = String(r.MAP_Breached || r.mapBreached || r.Breach || '').toUpperCase();
        const isBreached = mapBreachedStr.includes('YES') || mapBreachedStr.includes('BREACH') || (targetMap > 0 && currentSellingPrice > 0 && currentSellingPrice < targetMap);
        const priceDelta = Number(r.PriceDelta_INR ?? r.priceDelta ?? (currentSellingPrice - targetMap));
        const rawInStock = r.InStock ?? r.inStock ?? r.StockStatus ?? true;
        const inStock = rawInStock === true || rawInStock === 'TRUE' || rawInStock === 1 || rawInStock === 'true';
        const buyBoxOwner = String(r.BuyBoxOwner || r.buyBoxOwner || (isBreached ? 'DiscountDeals_IN (Breach)' : 'OrthoRest Official'));
        const shareOfSearch = Number(r.ShareOfSearchPct ?? r.ShareOfSearch ?? r.shareOfSearch ?? 30.0);
        const revenue30d = Number(r.Revenue30d_INR ?? r.revenue30d ?? r.Revenue ?? (currentSellingPrice * 50 * 30));

        const channelItem: ChannelPricingItem = {
          id: `CP-${sku}-${rawMarketplace.toUpperCase()}-${pIdx}`,
          sku,
          productName,
          marketplace: rawMarketplace as MarketplaceId,
          currentSellingPrice,
          targetMap,
          mapBreached: isBreached,
          priceDelta,
          inStock,
          buyBoxOwner,
          shareOfSearch,
          revenue30d,
          status: isBreached ? 'Active Breach' : 'Compliant',
          complianceAction: isBreached ? 'Auto Cease-and-Desist Notice Drafted' : 'Active - Price Protected'
        };

        parsedChannelPricing.push(channelItem);

        if (isBreached && currentSellingPrice > 0 && targetMap > 0) {
          parsedMapBreaches.push({
            id: `MAP-${sku}-${rawMarketplace}`,
            sku,
            productName,
            channel: rawMarketplace as MarketplaceId,
            violatingSeller: buyBoxOwner,
            enforcedMap: targetMap,
            violatedPrice: currentSellingPrice,
            discountPercent: Number((((targetMap - currentSellingPrice) / targetMap) * 100).toFixed(1)),
            breachDurationHours: 4.5,
            status: 'Active Breach',
            evidenceUrl: `https://${rawMarketplace}.com/dp/${sku}`,
            complianceAction: 'Auto Cease-and-Desist Notice Drafted'
          });
        }

        // Cross update SKU listing marketplace price record
        if (matchedSku) {
          if (!matchedSku.marketplacePrices) {
            matchedSku.marketplacePrices = {} as any;
          }
          matchedSku.marketplacePrices[rawMarketplace as MarketplaceId] = {
            price: currentSellingPrice,
            inStock,
            shareOfSearch,
            revenue30d,
            buyBoxOwner
          };
          if (isBreached) {
            matchedSku.revenueAtRisk = Math.max(matchedSku.revenueAtRisk || 0, Math.round((targetMap - currentSellingPrice) * (matchedSku.dailyVelocity || 30) * 30));
          }
        }
      });
    }
  }

  // If no pricing sheet was found, derive channel pricing from parsedSkus
  if (parsedChannelPricing.length === 0 && parsedSkus.length > 0) {
    parsedChannelPricing = buildChannelPricingFromCatalog(parsedSkus);
  }

  // 4. Check if Alerts tab exists
  const alertSheetName = wb.SheetNames.find((n) => n.toLowerCase().includes('alert') || n.toLowerCase().includes('trigger') || n.toLowerCase().includes('log') || n.toLowerCase().includes('4_'));
  if (alertSheetName && wb.Sheets[alertSheetName]) {
    const aWs = wb.Sheets[alertSheetName];
    const aRows: any[] = XLSX.utils.sheet_to_json(aWs);
    if (aRows.length > 0) {
      parsedAlerts = aRows.map((r, aIdx) => ({
        id: String(r.AlertID || r.id || `ALT-${aIdx + 1}`),
        sku: String(r.SKU || r.sku || 'SKU-001'),
        productName: String(r.ProductName || r.productName || 'Product'),
        marketplace: String(r.Marketplace || r.marketplace || 'blinkit').toLowerCase() as MarketplaceId,
        severity: String(r.Severity || r.severity || 'Critical') as any,
        status: String(r.Status || r.status || 'New') as any,
        timestamp: String(r.Timestamp || r.timestamp || new Date().toISOString()),
        timeDisplay: 'Live',
        summary: String(r.Summary || r.summary || 'Operational incident'),
        revenueAtRiskInr: Number(r.RevenueAtRisk_INR ?? r.revenueAtRiskInr ?? r.revenueAtRisk ?? 0),
        recommendedPlaybook: String(r.RecommendedPlaybook || r.recommendedPlaybook || 'Standard Playbook'),
        motherHubName: 'Bengaluru Central Mother Hub',
        motherHubStock: 184500,
        motherHubPincode: '562123',
        manufacturerName: 'Manufacturing Facility',
        manufacturerPlant: 'Central Plant',
        darkStoreStock: 3,
        batchNumber: `BAT-${r.SKU || '01'}-2026`,
        mfgDate: '2026-04-10',
        expiryDate: '2029-04-10',
        shelfLifeHealth: 98,
        transferLeadTimeHours: 1.2,
        transferUnitsSuggested: Number(r.TransferUnitsSuggested ?? r.transferUnitsSuggested ?? 100),
        logisticsPartner: 'Intra-City Quick Corridor',
        targetOwnerEmail: String(r.TargetEmail || r.targetOwnerEmail || 'vikashr984@gmail.com')
      }));
    }
  }

  // 5. Check if Mother Hubs tab exists
  const hubSheetName = wb.SheetNames.find((n) => n.toLowerCase().includes('hub') || n.toLowerCase().includes('mother') || n.toLowerCase().includes('buffer') || n.toLowerCase().includes('5_'));
  if (hubSheetName && wb.Sheets[hubSheetName]) {
    const hWs = wb.Sheets[hubSheetName];
    const hRows: any[] = XLSX.utils.sheet_to_json(hWs);
    if (hRows.length > 0) {
      parsedMotherHubs = hRows.map((r, hIdx) => {
        const hubId = String(r.HubID || r.hubId || `HUB-${hIdx + 1}`);
        const sku = String(r.SKU || r.sku || 'SLP-1001');
        const qty = Number(r.QuantityAvailableUnits ?? r.quantityAvailable ?? r.Quantity ?? r.Stock ?? 50000);
        const safety = Number(r.SafetyStockThreshold ?? r.safetyStockThreshold ?? 10000);
        const bufferHealth = qty < safety * 0.5 ? 'Critical' : qty < safety ? 'Adequate' : 'Optimal';
        return {
          id: `mhs-${hubId.toLowerCase()}-${sku.toLowerCase()}`,
          hubId,
          hubName: String(r.HubName || r.hubName || 'Central Mother Hub'),
          city: String(r.CityRegion || r.city || 'Bengaluru, Karnataka'),
          pincode: String(r.Pincode || r.pincode || '562123'),
          sku,
          productName: String(r.ProductName || r.productName || 'Product'),
          quantityAvailable: qty,
          reservedQuantity: Number(r.ReservedQuantityUnits ?? r.reservedQuantity ?? 10000),
          safetyStockThreshold: safety,
          bufferHealth: (r.BufferHealth || bufferHealth) as any,
          connectedDarkStoresCount: Number(r.ConnectedDarkStoresCount ?? r.connectedDarkStoresCount ?? 24),
          dispatchSlaHours: Number(r.DispatchSLA_Hours ?? r.dispatchSlaHours ?? 1.5)
        };
      });
    }
  }

  // 6. Check if Manufacturer Supply tab exists
  const mfgSheetName = wb.SheetNames.find((n) => n.toLowerCase().includes('mfg') || n.toLowerCase().includes('manufactur') || n.toLowerCase().includes('plant') || n.toLowerCase().includes('factory') || n.toLowerCase().includes('supply') || n.toLowerCase().includes('6_'));
  if (mfgSheetName && wb.Sheets[mfgSheetName]) {
    const mWs = wb.Sheets[mfgSheetName];
    const mRows: any[] = XLSX.utils.sheet_to_json(mWs);
    if (mRows.length > 0) {
      parsedMfgSupply = mRows.map((r, mIdx) => {
        const plantName = String(r.PlantName || r.plantName || `Plant ${mIdx + 1}`);
        const sku = String(r.SKU || r.sku || 'SLP-1001');
        return {
          id: `mfg-${plantName.toLowerCase().replace(/[^a-z0-9]/g, '-')}-${sku.toLowerCase()}`,
          manufacturerName: String(r.ManufacturerName || r.manufacturerName || 'OrthoRest FoamTech India Pvt Ltd'),
          plantName,
          location: String(r.LocationCity || r.location || 'Peenya Industrial Area, Bengaluru, KA'),
          pincode: String(r.Pincode || r.pincode || '560058'),
          sku,
          productName: String(r.ProductName || r.productName || 'Product'),
          factoryFinishedGoodsStock: Number(r.FactoryFinishedGoodsStockUnits ?? r.factoryFinishedGoodsStock ?? 250000),
          workInProgressUnits: Number(r.WorkInProgressUnits ?? r.workInProgressUnits ?? 85000),
          monthlyCapacityUnits: Number(r.MonthlyCapacityUnits ?? r.monthlyCapacityUnits ?? 400000),
          dailyProductionRate: Number(r.DailyProductionRate ?? r.dailyProductionRate ?? 14000),
          leadTimeToMotherHubHours: Number(r.LeadTimeToMotherHubHours ?? r.leadTimeToMotherHubHours ?? 4.0),
          destinationMotherHub: String(r.DestinationMotherHub || r.destinationMotherHub || 'Bengaluru Central Mother Hub'),
          activeBatchNumber: String(r.ActiveBatchNumber || r.activeBatchNumber || 'BAT-2026-088C'),
          mfgDate: String(r.MfgDate || r.mfgDate || '2026-04-10'),
          qualityPassRate: Number(r.QualityPassRatePct ?? r.qualityPassRate ?? 99.4)
        };
      });
    }
  }

  return {
    skus: parsedSkus,
    darkStores: parsedStores.length > 0 ? parsedStores : undefined,
    channelPricing: parsedChannelPricing.length > 0 ? parsedChannelPricing : undefined,
    mapBreaches: parsedMapBreaches.length > 0 ? parsedMapBreaches : undefined,
    alerts: parsedAlerts.length > 0 ? parsedAlerts : undefined,
    motherHubSkuStock: parsedMotherHubs.length > 0 ? parsedMotherHubs : undefined,
    manufacturerSupply: parsedMfgSupply.length > 0 ? parsedMfgSupply : undefined,
    rawRowCount,
    sheetNames: wb.SheetNames
  };
}

// Parse Excel / CSV and return updated SKU dataset
export async function parseUploadedSpreadsheet(file: File): Promise<{
  skus?: SKUListing[];
  darkStores?: DarkStoreInventory[];
  channelPricing?: ChannelPricingItem[];
  mapBreaches?: MAPBreach[];
  alerts?: AlertAnomaly[];
  motherHubSkuStock?: MotherHubSkuStock[];
  manufacturerSupply?: ManufacturerSupplyInfo[];
  rawRowCount: number;
  sheetNames?: string[];
}> {
  const buffer = await file.arrayBuffer();
  const wb = XLSX.read(buffer, { type: 'array' });
  return parseWorkbookData(wb);
}

// Fetch live published Google Sheet (All tabs via backend proxy with fallback)
export async function fetchPublishedGoogleSheet(sheetUrlOrId: string): Promise<{
  skus?: SKUListing[];
  darkStores?: DarkStoreInventory[];
  channelPricing?: ChannelPricingItem[];
  mapBreaches?: MAPBreach[];
  alerts?: AlertAnomaly[];
  motherHubSkuStock?: MotherHubSkuStock[];
  manufacturerSupply?: ManufacturerSupplyInfo[];
  rawRowCount: number;
  sheetNames?: string[];
}> {
  const url = sheetUrlOrId.trim();

  // 1. Try server-side proxy for flawless cross-origin multi-sheet export
  try {
    const proxyResp = await fetch('/api/sheets/fetch-proxy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    if (proxyResp.ok) {
      const data = await proxyResp.json();
      if (data.success && data.type === 'xlsx' && data.data) {
        const binaryStr = atob(data.data);
        const len = binaryStr.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
          bytes[i] = binaryStr.charCodeAt(i);
        }
        const wb = XLSX.read(bytes.buffer, { type: 'array' });
        return parseWorkbookData(wb);
      } else if (data.success && data.type === 'csv' && data.data) {
        const wb = XLSX.read(data.data, { type: 'string' });
        return parseWorkbookData(wb);
      }
    }
  } catch (err) {
    console.warn('Backend proxy fetch failed, attempting direct fetch:', err);
  }

  // 2. Direct browser fallback
  let sheetId = '';
  if (url.includes('docs.google.com/spreadsheets/d/')) {
    const match = url.match(/\/d\/([a-zA-Z0-9-_]+)/);
    if (match && match[1]) {
      sheetId = match[1];
    }
  } else if (!url.startsWith('http')) {
    sheetId = url;
  }

  if (sheetId) {
    const xlsxUrl = `https://docs.google.com/spreadsheets/d/${sheetId}/export?format=xlsx`;
    try {
      const resp = await fetch(xlsxUrl);
      if (resp.ok) {
        const buffer = await resp.arrayBuffer();
        const wb = XLSX.read(buffer, { type: 'array' });
        return parseWorkbookData(wb);
      }
    } catch (e) {
      console.warn('Direct XLSX fetch failed, falling back to CSV export:', e);
    }

    const csvUrl = `https://docs.google.com/spreadsheets/d/${sheetId}/export?format=csv`;
    const resp = await fetch(csvUrl);
    if (!resp.ok) {
      throw new Error(`Google Sheets fetch failed with HTTP ${resp.status}: ${resp.statusText}`);
    }

    const csvText = await resp.text();
    const wb = XLSX.read(csvText, { type: 'string' });
    return parseWorkbookData(wb);
  }

  // Direct file URL
  const resp = await fetch(url);
  if (!resp.ok) {
    throw new Error(`Fetch failed with status ${resp.status}`);
  }
  const buffer = await resp.arrayBuffer();
  const wb = XLSX.read(buffer, { type: 'array' });
  return parseWorkbookData(wb);
}

// Fetch live published Google Sheet (legacy CSV format helper)
export async function fetchPublishedGoogleSheetCsv(sheetUrlOrId: string): Promise<any[]> {
  const parsed = await fetchPublishedGoogleSheet(sheetUrlOrId);
  return parsed.skus || [];
}
