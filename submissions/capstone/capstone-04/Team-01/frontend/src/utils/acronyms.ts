/**
 * E-commerce & Supply Chain Acronyms Dictionary & Expansion Utilities
 * Expands all retail short forms into their complete full forms with explanations.
 */

export interface AcronymDefinition {
  short: string;
  full: string;
  category: 'Inventory & Supply Chain' | 'Finance & Revenue' | 'Marketing & Advertising' | 'Operations & Quality' | 'E-commerce Channels';
  description: string;
}

export const ACRONYMS_DICTIONARY: Record<string, AcronymDefinition> = {
  OOS: {
    short: 'OOS',
    full: 'Out Of Stock',
    category: 'Inventory & Supply Chain',
    description: 'Inventory level at zero in micro-fulfillment pods or dark stores, causing instant lost sales and search rank drops.'
  },
  SKU: {
    short: 'SKU',
    full: 'Stock Keeping Unit',
    category: 'Inventory & Supply Chain',
    description: 'Unique alphanumeric identifier assigned to each individual product variant, size, shade, or pack configuration.'
  },
  MAP: {
    short: 'MAP',
    full: 'Minimum Advertised Price',
    category: 'Operations & Quality',
    description: 'Legally enforceable lower price limit established by brand manufacturer to prevent unauthorized third-party retailer price erosion.'
  },
  ROAS: {
    short: 'ROAS',
    full: 'Return On Ad Spend',
    category: 'Marketing & Advertising',
    description: 'Revenue generated per monetary unit spent on advertising campaigns (Calculated as: Attributed Ad Revenue ÷ Ad Spend).'
  },
  ACOS: {
    short: 'ACOS',
    full: 'Advertising Cost of Sales',
    category: 'Marketing & Advertising',
    description: 'Direct ratio of advertising spend to total ad-attributed sales revenue, expressed as a percentage.'
  },
  TACOS: {
    short: 'TACOS',
    full: 'Total Advertising Cost of Sales',
    category: 'Marketing & Advertising',
    description: 'Ratio of total advertising spend against overall catalog gross revenue (organic + paid).'
  },
  WBR: {
    short: 'WBR',
    full: 'Weekly Business Review',
    category: 'Operations & Quality',
    description: 'Executive weekly operating cadence assessing multi-channel revenue, stock availability, and advertising performance.'
  },
  QC: {
    short: 'QC',
    full: 'Quick Commerce (10-15 Min Delivery)',
    category: 'E-commerce Channels',
    description: 'Hyperlocal ultra-fast delivery retail model (Blinkit, Zepto, Swiggy Instamart) fulfilling orders from localized dark stores.'
  },
  FEFO: {
    short: 'FEFO',
    full: 'First Expired, First Out',
    category: 'Inventory & Supply Chain',
    description: 'Inventory management and dispatch methodology ensuring batches closest to expiration are allocated and sold first.'
  },
  ASP: {
    short: 'ASP',
    full: 'Average Selling Price',
    category: 'Finance & Revenue',
    description: 'Effective realized selling price per unit sold after deducting coupons, discounts, and marketplace promotions.'
  },
  MRP: {
    short: 'MRP',
    full: 'Maximum Retail Price',
    category: 'Finance & Revenue',
    description: 'Statutory maximum retail price printed on product packaging mandated under Indian Legal Metrology regulations.'
  },
  SLA: {
    short: 'SLA',
    full: 'Service Level Agreement',
    category: 'Operations & Quality',
    description: 'Committed operational standard for dark store delivery speed (10-15 mins) or mother hub intra-city stock transfers (3-4 hours).'
  },
  VOC: {
    short: 'VOC',
    full: 'Voice of Customer',
    category: 'Operations & Quality',
    description: 'Aggregated sentiment analysis and customer feedback clustering from verified post-purchase product reviews.'
  },
  CSAT: {
    short: 'CSAT',
    full: 'Customer Satisfaction Score',
    category: 'Operations & Quality',
    description: 'Percentage benchmark measuring customer delight from 4-star and 5-star ratings across marketplace listings.'
  },
  PLA: {
    short: 'PLA',
    full: 'Product Listing Ads',
    category: 'Marketing & Advertising',
    description: 'Sponsored product search ads positioned at the top of marketplace search results pages.'
  },
  '3P': {
    short: '3P',
    full: 'Third-Party Resellers',
    category: 'E-commerce Channels',
    description: 'Independent marketplace merchants or unauthorized resellers selling goods on open marketplaces.'
  },
  '1P': {
    short: '1P',
    full: 'First-Party Direct Retail',
    category: 'E-commerce Channels',
    description: 'Direct wholesale vendor relationship where the marketplace directly purchases inventory and retails it.'
  },
  D2C: {
    short: 'D2C',
    full: 'Direct To Consumer',
    category: 'E-commerce Channels',
    description: 'Brand owned webstore and standalone digital channels bypassing third-party marketplace commissions.'
  },
  MoM: {
    short: 'MoM',
    full: 'Month-over-Month',
    category: 'Finance & Revenue',
    description: 'Metric growth or decline rate compared to the preceding 30-day calendar period.'
  },
  YoY: {
    short: 'YoY',
    full: 'Year-over-Year',
    category: 'Finance & Revenue',
    description: 'Metric growth or decline rate compared to the corresponding period in the prior financial year.'
  },
  POD: {
    short: 'POD',
    full: 'Micro-Fulfillment Pod (Dark Store)',
    category: 'Inventory & Supply Chain',
    description: 'Localized urban mini-warehouse (2,000-4,000 sq ft) servicing high-density 3km consumer radius in 10-15 minutes.'
  },
  WMS: {
    short: 'WMS',
    full: 'Warehouse Management System',
    category: 'Inventory & Supply Chain',
    description: 'Software platform governing mother hub stock movements, batch FEFO tracking, and dispatch manifests.'
  },
  Mfg: {
    short: 'Mfg',
    full: 'Manufacturing Date',
    category: 'Operations & Quality',
    description: 'Date of batch production at certified pharmaceutical/cosmeceutical formulation manufacturing facility.'
  },
  Exp: {
    short: 'Exp',
    full: 'Expiry Date',
    category: 'Operations & Quality',
    description: 'Cutoff date after which product formulation cannot be sold or distributed under perishables guidelines.'
  },
  INR: {
    short: 'INR',
    full: 'Indian Rupees (₹)',
    category: 'Finance & Revenue',
    description: 'Indian currency format formatted in Lakhs (₹1,00,000) and Crores (₹1,00,00,000).'
  },
  CTR: {
    short: 'CTR',
    full: 'Click-Through Rate',
    category: 'Marketing & Advertising',
    description: 'Percentage of shoppers who click on a search ad or organic listing upon viewing it in search results.'
  },
  CVR: {
    short: 'CVR',
    full: 'Conversion Rate',
    category: 'Marketing & Advertising',
    description: 'Percentage of product detail page visitors who complete a checkout order purchase.'
  },
  NDR: {
    short: 'NDR',
    full: 'Non-Delivery Report',
    category: 'Operations & Quality',
    description: 'Automated exception log raised by logistics courier when a customer delivery attempt fails.'
  },
  RTO: {
    short: 'RTO',
    full: 'Return To Origin',
    category: 'Operations & Quality',
    description: 'Package returned back to source fulfillment center due to customer refusal, defect, or repeated delivery failure.'
  },
  GMV: {
    short: 'GMV',
    full: 'Gross Merchandise Value',
    category: 'Finance & Revenue',
    description: 'Total retail sales value of merchandise sold across multi-channel marketplaces before deductions.'
  }
};

/**
 * Expands short form words into their full forms with explicit explanations.
 * e.g. "OOS in Quick Commerce pods" -> "Out Of Stock (OOS) in Quick Commerce (QC - 10-15 Min Delivery) pods"
 */
export function expandAcronyms(text: string): string {
  if (!text) return '';
  
  let result = text;
  
  // Specific regex replacements to preserve boundaries and avoid double expansion
  const replacements: Array<{ regex: RegExp; replacement: string }> = [
    { regex: /\bOOS\b/g, replacement: 'Out Of Stock (OOS)' },
    { regex: /\bSKU\b/g, replacement: 'Stock Keeping Unit (SKU)' },
    { regex: /\bSKUs\b/g, replacement: 'Stock Keeping Units (SKUs)' },
    { regex: /\bMAP\b/g, replacement: 'Minimum Advertised Price (MAP)' },
    { regex: /\bROAS\b/g, replacement: 'Return On Ad Spend (ROAS)' },
    { regex: /\bACOS\b/g, replacement: 'Advertising Cost of Sales (ACOS)' },
    { regex: /\bTACOS\b/g, replacement: 'Total Advertising Cost of Sales (TACOS)' },
    { regex: /\bWBR\b/g, replacement: 'Weekly Business Review (WBR)' },
    { regex: /\bFEFO\b/g, replacement: 'First Expired, First Out (FEFO Inventory Method)' },
    { regex: /\bASP\b/g, replacement: 'Average Selling Price (ASP)' },
    { regex: /\bMRP\b/g, replacement: 'Maximum Retail Price (MRP)' },
    { regex: /\bSLA\b/g, replacement: 'Service Level Agreement (SLA)' },
    { regex: /\bVOC\b/g, replacement: 'Voice of Customer (VOC Review Sentiment)' },
    { regex: /\bCSAT\b/g, replacement: 'Customer Satisfaction Score (CSAT)' },
    { regex: /\bPLA\b/g, replacement: 'Product Listing Ads (PLA)' },
    { regex: /\b3P\b/g, replacement: 'Third-Party Resellers (3P)' },
    { regex: /\b1P\b/g, replacement: 'First-Party Retail (1P)' },
    { regex: /\bD2C\b/g, replacement: 'Direct To Consumer (D2C)' },
    { regex: /\bMoM\b/g, replacement: 'Month-over-Month (MoM)' },
    { regex: /\bYoY\b/g, replacement: 'Year-over-Year (YoY)' },
    { regex: /\bWMS\b/g, replacement: 'Warehouse Management System (WMS)' },
    { regex: /\bCTR\b/g, replacement: 'Click-Through Rate (CTR)' },
    { regex: /\bCVR\b/g, replacement: 'Conversion Rate (CVR)' },
    { regex: /\bNDR\b/g, replacement: 'Non-Delivery Report (NDR)' },
    { regex: /\bRTO\b/g, replacement: 'Return To Origin (RTO)' },
    { regex: /\bGMV\b/g, replacement: 'Gross Merchandise Value (GMV)' }
  ];

  for (const { regex, replacement } of replacements) {
    result = result.replace(regex, replacement);
  }

  return result;
}

/**
 * Returns a list of all acronyms referenced in a given text string.
 */
export function getAcronymsInText(text: string): AcronymDefinition[] {
  if (!text) return [];
  const found: AcronymDefinition[] = [];
  const upperText = text.toUpperCase();

  for (const key of Object.keys(ACRONYMS_DICTIONARY)) {
    const reg = new RegExp(`\\b${key}\\b`, 'i');
    if (reg.test(upperText) || upperText.includes(key)) {
      found.push(ACRONYMS_DICTIONARY[key]);
    }
  }

  return found;
}
