/**
 * Raw Sales, Advertising, and Marketplace data generator aligned with Sleepsia CSVs
 */

export interface RawSaleRow {
  orderId: string;
  date: string;
  channel: string;
  sku: string;
  units: number;
  grossSales: number;
  discounts: number;
  returnUnits?: number;
  returns: number;
  cancellations: number;
  netRealizedRevenue: number;
}

export interface RawMarketplaceRow {
  platform: string;
  date: string;
  sku: string;
  marketplaceProductId: string;
  price: number;
  mrp: number;
  discount: number;
  availability: string;
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
  productContentScore: number;
  organicSearchPosition: number;
  sponsoredSearchPosition: number;
  categoryPosition: number;
  promotion?: string;
}

export interface RawAdRow {
  date: string;
  platform: string;
  campaignId: string;
  campaignName: string;
  campaignType: string;
  status: string;
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

const CHANNELS = ['Amazon', 'Flipkart', 'Blinkit', 'Instamart', 'Myntra', 'FirstCry', 'Nykaa', 'Meesho', 'JioMart', 'Pepperfry', 'Sleepbee', 'Tata 1mg', 'MyStore', 'Zoozle'];
const HERO_SKUS = ['SLP0001', 'SLP0002', 'SLP0003', 'SLP0006', 'SLP0011', 'SLP0013', 'SLP0026', 'SLP0028', 'SLP0032', 'SLP0040', 'SLP0046', 'SLP0047', 'SLP0056', 'SLP0064', 'SLP0068', 'SLP0070', 'SLP0077'];
const DATES = ['2026-08-01', '2026-08-02', '2026-08-03', '2026-08-04', '2026-08-05', '2026-08-06', '2026-08-07'];

export function generateRawSalesAndMarketplace(): { sales: RawSaleRow[]; marketplace: RawMarketplaceRow[]; advertising: RawAdRow[] } {
  const sales: RawSaleRow[] = [];
  const marketplace: RawMarketplaceRow[] = [];
  const advertising: RawAdRow[] = [];

  let orderSeq = 1000;

  DATES.forEach((date, dIdx) => {
    // Exact Daily Platform volumes matching Finance_Data
    const platformDailyData: Record<string, { orders: number; revenue: number; adSpend: number; adRev: number; skuCount: number }> = {
      'Amazon': { orders: 30 + (dIdx % 5) * 2, revenue: 36620 + (dIdx % 3) * 1200, adSpend: 1200 + (dIdx * 65), adRev: 4800 + (dIdx * 180), skuCount: 14 },
      'Flipkart': { orders: 18 + (dIdx % 4) * 2, revenue: 21790 + (dIdx % 4) * 1100, adSpend: 750 + (dIdx * 45), adRev: 2800 + (dIdx * 140), skuCount: 11 },
      'Blinkit': { orders: 15 + (dIdx % 3) * 3, revenue: 14980 + (dIdx % 5) * 1500, adSpend: 450 + (dIdx * 30), adRev: 2200 + (dIdx * 120), skuCount: 10 },
      'Instamart': { orders: 8 + (dIdx % 3) * 2, revenue: 6920 + (dIdx % 2) * 800, adSpend: 250, adRev: 950, skuCount: 7 },
      'Myntra': { orders: 14 + (dIdx % 3) * 2, revenue: 15620 + (dIdx % 3) * 900, adSpend: 550, adRev: 1950, skuCount: 9 },
      'FirstCry': { orders: 10 + (dIdx % 2) * 2, revenue: 9800 + (dIdx % 3) * 1200, adSpend: 320, adRev: 1200, skuCount: 8 },
      'Nykaa': { orders: 7 + (dIdx % 2), revenue: 8240, adSpend: 300, adRev: 1100, skuCount: 6 },
      'Meesho': { orders: 12 + (dIdx % 3), revenue: 10470, adSpend: 150, adRev: 850, skuCount: 8 },
      'JioMart': { orders: 12 + (dIdx % 2) * 2, revenue: 13180, adSpend: 400, adRev: 1400, skuCount: 9 },
      'Pepperfry': { orders: 7 + (dIdx % 2), revenue: 8780, adSpend: 380, adRev: 1300, skuCount: 6 },
      'Sleepbee': { orders: 10 + (dIdx % 2), revenue: 12070, adSpend: 0, adRev: 0, skuCount: 8 },
      'Tata 1mg': { orders: 8 + (dIdx % 2), revenue: 6920, adSpend: 120, adRev: 540, skuCount: 7 },
      'MyStore': { orders: 10 + (dIdx % 4), revenue: 11500, adSpend: 0, adRev: 0, skuCount: 8 },
      'Zoozle': { orders: 6, revenue: 6040, adSpend: 0, adRev: 0, skuCount: 5 },
    };

    CHANNELS.forEach((channel) => {
      const pData = platformDailyData[channel] || { orders: 8, revenue: 7500, adSpend: 200, adRev: 800, skuCount: 6 };
      const skusForChannel = HERO_SKUS.slice(0, pData.skuCount || 8);
      const ordersPerSku = Math.max(1, Math.floor(pData.orders / skusForChannel.length));

      skusForChannel.forEach((sku, sIdx) => {
        orderSeq++;
        const units = ordersPerSku;
        const unitPrice = 750 + (sIdx % 5) * 180;
        const grossSales = units * unitPrice;
        const discounts = Math.round(grossSales * 0.10);
        const netSales = grossSales - discounts;

        sales.push({
          orderId: `ORD-${date.replace(/-/g, '').slice(4)}-${sku}-${channel.slice(0, 3).toUpperCase()}-${orderSeq}`,
          date,
          channel,
          sku,
          units,
          grossSales,
          discounts,
          returns: 0,
          cancellations: 0,
          netRealizedRevenue: netSales,
        });

        marketplace.push({
          platform: channel,
          date,
          sku,
          marketplaceProductId: `MP-${channel.slice(0, 3).toUpperCase()}-${sku}`,
          price: unitPrice - 50,
          mrp: unitPrice + 250,
          discount: 300,
          availability: 'In Stock',
          inventory: 85 + (sIdx * 12),
          orders: units,
          unitsSold: units,
          gmv: grossSales,
          returns: 0,
          cancellations: 0,
          marketplaceFees: Math.round(grossSales * 0.15),
          settlement: Math.round(netSales * 0.85),
          rating: 4.4,
          reviewCount: 1450 + sIdx * 80,
          productContentScore: 88,
          organicSearchPosition: 4 + sIdx,
          sponsoredSearchPosition: 2 + (sIdx % 3),
          categoryPosition: 3 + sIdx,
          promotion: (sIdx % 3 === 0) ? '10% Coupon' : undefined,
        });
      });

      // Advertising campaigns
      if (pData.adSpend > 0) {
        const campaignTypes = ['Sponsored Products', 'Sponsored Brands', 'Sponsored Display'];
        campaignTypes.forEach((cType, cIdx) => {
          const spend = Math.round(pData.adSpend / campaignTypes.length);
          const attributedRevenue = Math.round(pData.adRev / campaignTypes.length);
          const impressions = spend * 45;
          const clicks = Math.round(impressions * 0.038);
          const ctr = 3.8;
          const cpc = clicks > 0 ? Number((spend / clicks).toFixed(2)) : 12;
          const roas = spend > 0 ? Number((attributedRevenue / spend).toFixed(2)) : 3.5;
          const acos = attributedRevenue > 0 ? Number(((spend / attributedRevenue) * 100).toFixed(1)) : 28.5;

          advertising.push({
            date,
            platform: channel,
            campaignId: `CAMP-${channel.slice(0, 3).toUpperCase()}-${date.slice(5)}-${cIdx + 1}`,
            campaignName: `${channel} ${cType} - ${HERO_SKUS[cIdx]} Hero Growth`,
            campaignType: cType,
            status: 'Enabled',
            sku: HERO_SKUS[cIdx],
            productId: `PID-000${cIdx + 1}`,
            impressions,
            clicks,
            spend,
            orders: Math.round(clicks * 0.12),
            units: Math.round(clicks * 0.14),
            attributedRevenue,
            ctr,
            cpc,
            roas,
            acos,
          });
        });
      }
    });
  });

  // Ensure exactly 799 sales rows
  while (sales.length < 799) {
    orderSeq++;
    const padIdx = sales.length % HERO_SKUS.length;
    const padSku = HERO_SKUS[padIdx];
    const padChan = CHANNELS[sales.length % CHANNELS.length];
    const padDate = DATES[sales.length % DATES.length];
    const padPrice = 850 + (padIdx % 4) * 150;
    sales.push({
      orderId: `ORD-${padDate.replace(/-/g, '').slice(4)}-${padSku}-${padChan.slice(0, 3).toUpperCase()}-${orderSeq}`,
      date: padDate,
      channel: padChan,
      sku: padSku,
      units: 1,
      grossSales: padPrice,
      discounts: 85,
      returns: 0,
      cancellations: 0,
      netRealizedRevenue: padPrice - 85,
    });
  }
  if (sales.length > 799) {
    sales.splice(799);
  }

  // Populate exactly 37 returns totaling ~₹37,750 on positive units/sales orders
  const returnIndices = [12, 34, 56, 78, 95, 114, 138, 162, 185, 204, 227, 249, 271, 293, 315, 338, 360, 382, 405, 427, 449, 471, 493, 516, 538, 560, 583, 605, 627, 649, 672, 694, 716, 738, 759, 778, 792];
  let returnAllocated = 0;
  returnIndices.forEach((idx, rIdx) => {
    if (sales[idx]) {
      const isLast = rIdx === returnIndices.length - 1;
      const retVal = isLast ? (37750 - returnAllocated) : Math.min(sales[idx].grossSales - sales[idx].discounts, Math.round(37750 / returnIndices.length) + ((rIdx % 5) - 2) * 50);
      sales[idx].returns = retVal;
      sales[idx].returnUnits = 1;
      returnAllocated += retVal;
    }
  });

  // Populate exactly 10 cancellations totaling ~₹9,930 on positive units/sales orders
  const cancelIndices = [45, 122, 210, 288, 375, 460, 545, 630, 705, 780];
  let cancelAllocated = 0;
  cancelIndices.forEach((idx, cIdx) => {
    if (sales[idx]) {
      const isLast = cIdx === cancelIndices.length - 1;
      const canVal = isLast ? (9930 - cancelAllocated) : Math.min(sales[idx].grossSales - sales[idx].discounts - sales[idx].returns, Math.round(9930 / cancelIndices.length) + ((cIdx % 3) - 1) * 70);
      sales[idx].cancellations = canVal;
      cancelAllocated += canVal;
    }
  });

  // Recompute net realized revenue for all rows
  sales.forEach((s) => {
    const netSales = s.grossSales - s.discounts;
    s.netRealizedRevenue = Math.max(0, netSales - s.returns - s.cancellations);
  });

  return { sales, marketplace, advertising };
}
