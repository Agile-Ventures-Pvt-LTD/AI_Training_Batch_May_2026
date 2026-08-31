/**
 * Dataset Service - Ingestion, Excel Workbook Parsing, Validation & Unified Modeling
 */

import * as XLSX from 'xlsx';
import {
  SleepsiaWorkbookData,
  ProductMaster,
  MarketplaceMaster,
  InternalSalesRecord,
  MarketplaceRecord,
  AdvertisingRecord,
  InventoryRecord,
  CostRecord,
  CustomerRecord,
  FinanceRecord,
  CompetitorRecord,
  ShippingRecord,
} from '../types/commerce';
import { generateDefaultDataset } from '../data/defaultSleepsiaData';

// Singleton in-memory store for active workbook data
let activeDataset: SleepsiaWorkbookData = generateDefaultDataset();

export function getActiveDataset(): SleepsiaWorkbookData {
  return activeDataset;
}

export function setActiveDataset(dataset: SleepsiaWorkbookData): void {
  activeDataset = dataset;
}

export function resetToDefaultDataset(): SleepsiaWorkbookData {
  activeDataset = generateDefaultDataset();
  return activeDataset;
}

/**
 * Validates and parses an uploaded Excel (.xlsx) file buffer or ArrayBuffer
 */
export function parseSleepsiaWorkbook(
  buffer: ArrayBuffer | Uint8Array,
  fileName: string = 'Uploaded_Workbook.xlsx'
): { success: boolean; data?: SleepsiaWorkbookData; errors?: string[]; warnings?: string[] } {
  try {
    const workbook = XLSX.read(buffer, { type: 'array', cellDates: true });
    const sheetNames = workbook.SheetNames;
    const warnings: string[] = [];
    const errors: string[] = [];

    // Check for standard sheets
    const getSheetData = (nameVariations: string[]): any[] => {
      for (const name of nameVariations) {
        const foundName = sheetNames.find(
          (s) => s.trim().toLowerCase() === name.trim().toLowerCase()
        );
        if (foundName && workbook.Sheets[foundName]) {
          return XLSX.utils.sheet_to_json(workbook.Sheets[foundName], { defval: null });
        }
      }
      return [];
    };

    const rawProducts = getSheetData(['Product_Master', 'Products', 'ProductMaster', 'Product Master']);
    const rawSales = getSheetData(['Internal_Sales', 'Sales_Data', 'Sales', 'InternalSales', 'Internal Sales']);
    const rawMarketplaceData = getSheetData(['Marketplace_Data', 'Marketplace', 'Channel_Data', 'Marketplace Data']);
    const rawAds = getSheetData(['Advertising_Data', 'Advertising', 'Ads_Data', 'Ad_Data', 'Advertising Data']);
    const rawInventory = getSheetData(['Inventory_Data', 'Inventory', 'Stock_Data', 'Inventory Data']);
    const rawCosts = getSheetData(['Cost_Data', 'Costs', 'COGS', 'Cost Data']);
    const rawCustomers = getSheetData(['Customer_Data', 'Customers', 'Customer Data']);
    const rawFinance = getSheetData(['Finance_Data', 'Finance', 'Financials', 'Finance Data']);
    const rawCompetitors = getSheetData(['Competitor_Data', 'Competitors', 'Competition', 'Competitor Data']);
    const rawShipping = getSheetData(['Shipping_Data', 'Shipping', 'Logistics', 'Shipping Data']);
    const rawMarketplaceMasters = getSheetData(['Marketplace_Master', 'Marketplaces', 'Channels', 'Marketplace Master']);
    const rawSummary = getSheetData(['Prototype_Summary', 'Summary', 'Prototype Summary']);

    // If critical sheets are missing, report warning and fallback to synthesized/default fields
    if (rawProducts.length === 0) {
      warnings.push('Sheet "Product_Master" was missing or empty; populated from default Sleepsia catalog.');
    }
    if (rawSales.length === 0) {
      warnings.push('Sheet "Internal_Sales" was missing or empty; using default sales transactions.');
    }

    // Helper to clean numerical values
    const parseNum = (val: any, defaultVal = 0): number => {
      if (typeof val === 'number') return isNaN(val) ? defaultVal : val;
      if (!val) return defaultVal;
      const str = String(val).replace(/[₹,$,%,? ]/g, '').trim();
      const n = parseFloat(str);
      return isNaN(n) ? defaultVal : n;
    };

    // Transform products
    const defaultData = generateDefaultDataset();
    const products: ProductMaster[] = rawProducts.length > 0
      ? rawProducts
          .filter((r: any) => {
            const name = String(r.SKU || r.sku || r.Product_Name || r.productName || '').toLowerCase();
            return !name.includes('total') && !name.includes('summary') && (r.SKU || r.sku || r.Product_Name || r.productName);
          })
          .map((r: any, idx: number) => ({
            sku: String(r.SKU || r.sku || `SLP-${idx + 1}`),
            productId: String(r.Product_ID || r.productId || r['Product ID'] || `PRD-${1000 + idx}`),
            productName: String(r.Product_Name || r.productName || r['Product Name'] || 'Sleepsia Ergonomic Pillow'),
            category: (r.Category || r.category || 'Memory Foam Pillows') as any,
            brand: String(r.Brand || r.brand || 'Sleepsia'),
            variant: String(r.Variant || r.variant || 'Standard'),
            size: String(r.Size || r.size || 'Regular'),
            material: String(r.Material || r.material || 'Memory Foam'),
            colour: String(r.Colour || r.Color || r.colour || r.color || 'White'),
            eanGtin: String(r.EAN_GTIN || r.eanGtin || r['EAN/GTIN'] || '8900000000000'),
            productLifecycle: (r.Product_Lifecycle || r.productLifecycle || r['Product Lifecycle'] || 'Active') as any,
            mrp: parseNum(r.MRP || r.mrp, 1999),
            standardCost: parseNum(r.Base_COGS || r.Standard_Cost || r.standardCost || r['Base COGS'], 500),
          }))
      : defaultData.products;

    // Transform Marketplace Masters
    const marketplaceMasters: MarketplaceMaster[] = rawMarketplaceMasters.length > 0
      ? rawMarketplaceMasters
          .filter((r: any) => r.Platform || r.platform)
          .map((r: any) => ({
            platform: String(r.Platform || r.platform) as any,
            platformType: (r.Channel_Type || r.platformType || r['Channel Type'] || 'General E-Commerce') as any,
            commissionRate: parseNum(r.Commission_Rate || r.commissionRate || r.Marketplace_Fees, 0.15),
            settlementDays: parseNum(r.Settlement_Days || r.settlementDays, 7),
            returnWindowDays: parseNum(r.Return_Window_Days || r.returnWindowDays, 10),
            activeStatus: r.Status === 'Active' || r.activeStatus === true || String(r.Status || '').toLowerCase() === 'active',
          }))
      : defaultData.marketplaceMasters;

    // Transform Sales
    const sales: InternalSalesRecord[] = rawSales.length > 0
      ? rawSales
          .filter((r: any) => {
            const rowStr = (String(r.Order_ID || r.orderId || '') + String(r.Date || r.date || '') + String(r.SKU || r.sku || '')).toLowerCase();
            return !rowStr.includes('total') && !rowStr.includes('sum') && (r.SKU || r.sku || r.Order_ID || r.orderId);
          })
          .map((r: any, idx: number) => {
            const rawDate = r.Date || r.date;
            const dateStr = rawDate instanceof Date ? rawDate.toISOString().slice(0, 10) : String(rawDate || '2026-08-01').slice(0, 10);
            const units = parseNum(r.Units || r.units, 1);
            const grossSales = parseNum(r.Gross_Sales || r.grossSales, 1500);
            const discounts = parseNum(r.Discounts || r.discounts, 150);
            const netSales = parseNum(r.Net_Sales || r.netSales, grossSales - discounts);
            const returnUnits = parseNum(r.Return_Units || r.returnUnits || r['Return Units'] || r.return_units, 0);
            const returns = parseNum(r.Returns || r.returns, 0);
            const cancellations = parseNum(r.Cancellations || r.cancellations, 0);
            
            // Calculate Net Realized Revenue = Net Sales - Returns - Cancellations
            let netRealizedRevenue = parseNum(r.Net_Realized_Revenue || r.netRealizedRevenue || r['Net Realized Revenue'], 0);
            if (netRealizedRevenue === 0 || (netRealizedRevenue === netSales && (returns > 0 || cancellations > 0))) {
              netRealizedRevenue = Math.max(0, netSales - returns - cancellations);
            }

            return {
              orderId: String(r.Order_ID || r.orderId || `ORD-${idx + 1000}`),
              date: dateStr,
              channel: String(r.Channel || r.channel || 'Amazon') as any,
              sku: String(r.SKU || r.sku || products[0].sku),
              productName: String(r.Product_Name || r.productName || 'Sleepsia Pillow'),
              units,
              grossSales,
              discounts,
              netSales,
              returnUnits: returnUnits > 0 ? returnUnits : returns > 0 ? 1 : 0,
              returns,
              cancellations,
              netRealizedRevenue,
              customerId: r.Customer_ID ? String(r.Customer_ID) : undefined,
              state: r.State ? String(r.State) : undefined,
            };
          })
      : defaultData.sales;

    // Transform Inventory Records
    const inventory: InventoryRecord[] = rawInventory.length > 0
      ? rawInventory
          .filter((r: any) => {
            const rowStr = (String(r.Date || '') + String(r.Mother_Warehouse || r.Warehouse || '') + String(r.SKU || '')).toLowerCase();
            return !rowStr.includes('total') && !rowStr.includes('sum') && !rowStr.includes('average') && (r.SKU || r.sku);
          })
          .map((r: any) => {
            const rawDate = r.Date || r.date;
            const dateStr = rawDate instanceof Date ? rawDate.toISOString().slice(0, 10) : String(rawDate || '2026-08-01').slice(0, 10);
            const motherWarehouse = String(r.Mother_Warehouse || r['Mother Warehouse'] || r.Warehouse || r.warehouse || 'Noida');
            const darkstore = String(r.Darkstore_ID || r['Darkstore ID'] || r.Darkstore || r.darkstore || r.DarkstoreId || '');
            const openingStock = parseNum(r.Opening_Stock || r['Opening Stock'] || r.openingStock, 0);
            const closingStock = parseNum(r.Closing_Stock || r['Closing Stock'] || r.closingStock, 0);
            const available = parseNum(r.Available_Stock || r['Available Stock'] || r.Available_Inventory || r['Available Inventory'] || r.availableStock || r.availableInventory, 0);
            const reserved = parseNum(r.Reserved_Stock || r['Reserved Stock'] || r.reservedStock, 0);
            const inbound = parseNum(r.Inbound_Stock || r['Inbound Stock'] || r.inboundStock, 0);
            const damaged = parseNum(r.Damaged_Stock || r['Damaged Stock'] || r.damagedStock, 0);
            const daysOfInventory = parseNum(r.Days_of_Inventory || r['Days of Inventory'] || r.daysOfInventory || r.DOI || r.doi, 18);
            
            const risk: 'Low' | 'Medium' | 'High' | 'Critical' = 
              daysOfInventory <= 7 ? 'Critical' : daysOfInventory <= 14 ? 'High' : daysOfInventory <= 45 ? 'Medium' : 'Low';

            return {
              date: dateStr,
              sku: String(r.SKU || r.sku),
              motherWarehouse,
              warehouse: motherWarehouse,
              darkstore: darkstore || undefined,
              darkstoreId: darkstore || undefined,
              openingStock,
              closingStock,
              availableStock: available,
              availableInventory: available,
              reservedStock: reserved,
              inboundStock: inbound,
              damagedStock: damaged,
              daysOfInventory,
              stockoutRisk: risk,
            };
          })
      : defaultData.inventory;

    // Transform Marketplace Records
    const marketplaceData: MarketplaceRecord[] = rawMarketplaceData.length > 0
      ? rawMarketplaceData.map((r: any) => {
          const rawDate = r.Date || r.date;
          const dateStr = rawDate instanceof Date ? rawDate.toISOString().slice(0, 10) : String(rawDate || '2026-08-19').slice(0, 10);
          return {
            platform: String(r.Platform || r.platform || 'Amazon') as any,
            date: dateStr,
            sku: String(r.SKU || r.sku),
            marketplaceProductId: String(r.Marketplace_Product_ID || r.marketplaceProductId || 'MP-001'),
            price: Number(r.Price || r.price || 1200),
            mrp: Number(r.MRP || r.mrp || 1999),
            discount: Number(r.Discount || r.discount || 30),
            availability: (r.Availability || 'In Stock') as any,
            inventory: Number(r.Inventory || r.inventory || 100),
            orders: Number(r.Orders || r.orders || 10),
            unitsSold: Number(r.Units_Sold || r.unitsSold || 12),
            gmv: Number(r.GMV || r.gmv || 14400),
            returns: Number(r.Returns || r.returns || 0),
            cancellations: Number(r.Cancellations || r.cancellations || 0),
            marketplaceFees: Number(r.Marketplace_Fees || r.marketplaceFees || 2000),
            settlement: Number(r.Settlement || r.settlement || 12400),
            rating: Number(r.Rating || r.rating || 4.5),
            reviewCount: Number(r.Review_Count || r.reviewCount || 200),
            productContentScore: Number(r.Product_Content_Score || 90),
            organicSearchPosition: Number(r.Organic_Search_Position || 2),
            sponsoredSearchPosition: Number(r.Sponsored_Search_Position || 1),
            categoryPosition: Number(r.Category_Position || 3),
            promotion: r.Promotion ? String(r.Promotion) : undefined,
          };
        })
      : defaultData.marketplaceData;

    // Transform Ads
    const advertising: AdvertisingRecord[] = rawAds.length > 0
      ? rawAds.map((r: any) => {
          const rawDate = r.Date || r.date;
          const dateStr = rawDate instanceof Date ? rawDate.toISOString().slice(0, 10) : String(rawDate || '2026-08-19').slice(0, 10);
          return {
            date: dateStr,
            platform: String(r.Platform || r.platform || 'Amazon') as any,
            campaignId: String(r.Campaign_ID || r.campaignId || 'CMP-001'),
            campaignName: String(r.Campaign_Name || r.campaignName || 'General Search Campaign'),
            campaignType: (r.Campaign_Type || 'Sponsored Products') as any,
            status: (r.Status || 'ENABLED') as any,
            sku: String(r.SKU || r.sku),
            productId: String(r.Product_ID || r.productId || 'PRD-001'),
            impressions: Number(r.Impressions || r.impressions || 1000),
            clicks: Number(r.Clicks || r.clicks || 50),
            spend: Number(r.Spend || r.spend || 600),
            orders: Number(r.Orders || r.orders || 6),
            units: Number(r.Units || r.units || 7),
            attributedRevenue: Number(r.Attributed_Revenue || r.attributedRevenue || 3000),
            ctr: Number(r.CTR || r.ctr || 5),
            cpc: Number(r.CPC || r.cpc || 12),
            roas: Number(r.ROAS || r.roas || 5),
            acos: Number(r.ACoS || r.acos || 20),
          };
        })
      : defaultData.advertising;

    // Transform Shipping
    const shipping: ShippingRecord[] = rawShipping.length > 0
      ? rawShipping.map((r: any) => {
          const rawDate = r.Date || r.date;
          const dateStr = rawDate instanceof Date ? rawDate.toISOString().slice(0, 10) : String(rawDate || '2026-08-19').slice(0, 10);
          return {
            orderId: String(r.Order_ID || r.orderId || 'ORD-SHIP-001'),
            date: dateStr,
            platform: String(r.Platform || r.platform || 'Amazon') as any,
            sku: String(r.SKU || r.sku),
            warehouse: String(r.Warehouse || r.warehouse || 'Delhi Hub NCR'),
            carrier: (r.Carrier || 'Delhivery') as any,
            orderDate: dateStr,
            shipDate: dateStr,
            expectedDeliveryDate: '2026-08-22',
            actualDeliveryDate: r.Actual_Delivery_Date ? String(r.Actual_Delivery_Date).slice(0, 10) : undefined,
            shipmentStatus: (r.Shipment_Status || 'Delivered') as any,
            deliveryStatus: (r.Delivery_Status || 'On-Time') as any,
            shippingCost: Number(r.Shipping_Cost || 120),
            delayReason: r.Delay_Reason ? String(r.Delay_Reason) : undefined,
            delayDays: Number(r.Delay_Days || 0),
          };
        })
      : defaultData.shipping;

    // Transform Costs
    const costs: CostRecord[] = rawCosts.length > 0
      ? rawCosts
          .filter((r: any) => r.SKU || r.sku)
          .map((r: any) => ({
            sku: String(r.SKU || r.sku),
            date: r.Date ? String(r.Date).slice(0, 10) : '2026-08-01',
            cogs: parseNum(r.COGS || r.cogs, 400),
            manufacturingCost: parseNum(r.Manufacturing_Cost || r.manufacturingCost, 250),
            packaging: parseNum(r.Packaging_Cost || r.packagingCost || r.packaging, 40),
            freight: parseNum(r.Freight_Cost || r.freightCost || r.freight, 50),
            warehouseCost: parseNum(r.Warehouse_Cost || r.warehouseCost, 30),
            marketplaceFees: parseNum(r.Marketplace_Fee_Benchmark || r.marketplaceFees, 150),
            paymentFees: parseNum(r.Payment_Fees_Benchmark || r.paymentFees, 25),
            returnsCost: parseNum(r.Returns_Cost_Benchmark || r.returnsCost, 35),
            otherVariableCosts: parseNum(r.Other_Variable_Costs || r.otherVariableCosts, 20),
          }))
      : defaultData.costs;

    // Transform Finance
    const finance: FinanceRecord[] = rawFinance.length > 0
      ? rawFinance
          .filter((r: any) => r.Date || r.date || r.Platform || r.platform)
          .map((r: any) => {
            const rev = parseNum(r.Revenue || r.revenue || r.Gross_Revenue, 10000);
            const prof = parseNum(r.Profit || r.profit || r.Net_Profit, 2000);
            return {
              date: r.Date ? String(r.Date).slice(0, 10) : '2026-08-01',
              channel: String(r.Platform || r.platform || r.Channel || 'Amazon') as any,
              grossRevenue: rev,
              netRevenue: rev,
              totalCogs: parseNum(r.COGS || r.cogs, rev * 0.35),
              adSpend: parseNum(r.Ad_Spend || r.adSpend, rev * 0.15),
              marketplaceCommission: parseNum(r.Marketplace_Fees || r.marketplaceFees, rev * 0.15),
              shippingCost: parseNum(r.Shipping_Cost || r.shippingCost, rev * 0.05),
              paymentGatewayFee: parseNum(r.Payment_Gateway_Fee || r.paymentGatewayFee, rev * 0.02),
              operatingExpense: parseNum(r.Operating_Cost || r.operatingCost, rev * 0.1),
              netProfit: prof,
              ebitdaMargin: rev > 0 ? Number(((prof / rev) * 100).toFixed(1)) : 0,
            };
          })
      : defaultData.finance;

    // Transform Customers
    const customers: CustomerRecord[] = rawCustomers.length > 0
      ? rawCustomers
          .filter((r: any) => r.Customer_ID || r.customerId)
          .map((r: any) => ({
            customerId: String(r.Customer_ID || r.customerId),
            name: String(r.Name || r.name || `Customer ${String(r.Customer_ID || r.customerId).replace('CUST', '')}`),
            city: String(r.Location || r.City || r.city || 'Delhi NCR'),
            state: String(r.State || r.state || 'Delhi NCR'),
            segment: (r.Segment || r.segment || 'Repeat Buyer') as any,
            repeatCustomer: parseNum(r.Order_Frequency || r.orderFrequency, 1) > 1,
            totalOrders: parseNum(r.Order_Frequency || r.orderFrequency, 1),
            lifetimeValue: parseNum(r.Lifetime_Value || r.lifetimeValue, 2500),
            feedbackScore: parseNum(r.Feedback_Score || r.feedbackScore, 4.5),
          }))
      : defaultData.customers;

    // Transform Competitors
    const competitors: CompetitorRecord[] = rawCompetitors.length > 0
      ? rawCompetitors
          .filter((r: any) => r.Competitor_Brand || r.competitorBrand)
          .map((r: any) => {
            const compPrice = parseNum(r.Price || r.price, 999);
            const mrp = parseNum(r.MRP || r.mrp, 1499);
            const discount = parseNum(r.Discount || r.discount, mrp - compPrice);
            return {
              date: r.Date ? String(r.Date).slice(0, 10) : '2026-08-01',
              category: (r.Category || 'Sleeping Pillows') as any,
              competitorBrand: String(r.Competitor_Brand || r.competitorBrand),
              competitorProductName: String(r.Comparable_Product || r.competitorProductName || `${r.Competitor_Brand} Ergonomic Pillow`),
              competitorPrice: compPrice,
              sleepsiaTargetSku: String(r.Sleepsia_Target_SKU || r.sleepsiaTargetSku || 'SLP0001'),
              discountPercent: mrp > 0 ? Math.round((discount / mrp) * 100) : 10,
              rating: parseNum(r.Rating || r.rating, 4.2),
              reviewCount: parseNum(r.Review_Count || r.reviewCount, 1500),
              availability: (r.Availability || 'In Stock') as any,
              searchPosition: parseNum(r.Organic_Search_Position || r.searchPosition, 15),
              activePromotion: r.Promotion ? String(r.Promotion) : 'Standard Price',
              threatLevel: (r.Threat_Level || 'Medium') as any,
            };
          })
      : defaultData.competitors;

    // Build unified data bundle
    const dates = sales.map((s) => s.date).sort();
    const parsedData: SleepsiaWorkbookData = {
      products,
      marketplaceMasters,
      sales,
      marketplaceData,
      advertising,
      inventory,
      costs,
      customers,
      finance,
      competitors,
      shipping,
      metadata: {
        loadedAt: new Date().toISOString(),
        totalOrders: sales.length,
        dateRange: {
          start: dates[0] || '2026-08-01',
          end: dates[dates.length - 1] || '2026-08-07',
        },
        totalSkus: products.length,
        activeChannels: Array.from(new Set(sales.map((s) => s.channel))).length,
        sourceFileName: fileName,
      },
    };

    activeDataset = parsedData;
    return { success: true, data: parsedData, warnings };
  } catch (err: any) {
    return {
      success: false,
      errors: [`Failed to parse Excel workbook: ${err?.message || 'Unknown error'}`],
    };
  }
}
