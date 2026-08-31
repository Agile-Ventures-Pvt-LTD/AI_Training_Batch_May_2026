/**
 * Embedded Sleepsia Sales, Advertising, Customer, Marketplace & Competitor CSV Dataset
 */

function parseCsv(csvText: string): Record<string, string>[] {
  const lines = csvText.trim().split('\n');
  if (lines.length <= 1) return [];
  
  const parseLine = (line: string): string[] => {
    const values: string[] = [];
    let current = '';
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    values.push(current.trim());
    return values;
  };

  const headers = parseLine(lines[0]);
  const records: Record<string, string>[] = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    const values = parseLine(line);
    const row: Record<string, string> = {};
    headers.forEach((h, idx) => {
      row[h] = values[idx] || '';
    });
    records.push(row);
  }

  return records;
}

export const CSV_COMPETITOR_DATA = `Date,Category,Competitor_Brand,Comparable_Product,Price,MRP,Discount,Rating,Review_Count,Availability,Organic_Search_Position,Promotion
2026-08-01,Sleeping Pillows,Wakefit,Memory Foam Pillow,?799.00,"?1,299.00",?500.00,4.3,12450,In Stock,2,10% Coupon
2026-08-01,Sleeping Pillows,The Sleep Company,SmartGRID Ortho Pillow,"?1,499.00","?2,499.00","?1,000.00",4.4,8920,In Stock,4,Limited Time Deal
2026-08-01,Sleeping Pillows,Solimo,Memory Foam Pillow,?649.00,"?1,099.00",?450.00,4.1,6540,In Stock,8,None
2026-08-01,Back Support & Seat Cushions,Frido,Ergonomic Lumbar Cushion,?899.00,"?1,499.00",?600.00,4.2,4310,In Stock,3,5% Off
2026-08-01,Travel & Car Comfort,Urban Tribe,Travel Neck Pillow,?499.00,?899.00,?400.00,4.0,2890,In Stock,6,None
2026-08-04,Sleeping Pillows,Wakefit,Memory Foam Pillow,?749.00,"?1,299.00",?550.00,4.3,12680,In Stock,1,Flash Sale 45%
2026-08-04,Sleeping Pillows,The Sleep Company,SmartGRID Ortho Pillow,"?1,399.00","?2,499.00","?1,100.00",4.4,9050,In Stock,3,Super Saver Deal
2026-08-04,Sleeping Pillows,Solimo,Memory Foam Pillow,?629.00,"?1,099.00",?470.00,4.1,6610,In Stock,9,None
2026-08-04,Back Support & Seat Cushions,Frido,Ergonomic Lumbar Cushion,?849.00,"?1,499.00",?650.00,4.2,4420,In Stock,2,Lightning Deal
2026-08-04,Travel & Car Comfort,Urban Tribe,Travel Neck Pillow,?479.00,?899.00,?420.00,4.0,2940,In Stock,5,Buy 2 Get 10%
2026-08-07,Sleeping Pillows,Wakefit,Memory Foam Pillow,?799.00,"?1,299.00",?500.00,4.3,12890,In Stock,2,10% Coupon
2026-08-07,Sleeping Pillows,The Sleep Company,SmartGRID Ortho Pillow,"?1,449.00","?2,499.00","?1,050.00",4.4,9180,In Stock,4,Weekend Price Drop
2026-08-07,Sleeping Pillows,Solimo,Memory Foam Pillow,?649.00,"?1,099.00",?450.00,4.1,6700,In Stock,7,None
2026-08-07,Back Support & Seat Cushions,Frido,Ergonomic Lumbar Cushion,?899.00,"?1,499.00",?600.00,4.2,4510,In Stock,3,None
2026-08-07,Travel & Car Comfort,Urban Tribe,Travel Neck Pillow,?499.00,?899.00,?400.00,4.0,2990,In Stock,6,None`;

export const CSV_CUSTOMER_DATA = `Customer_ID,Location,Segment,Order_Frequency,Lifetime_Value
CUST00001,Mumbai,Premium,4,"?5,840.00"
CUST00002,Bengaluru,Repeat,2,"?2,340.00"
CUST00003,Delhi NCR,New,1,"?1,120.00"
CUST00004,Hyderabad,Repeat,3,"?3,890.00"
CUST00005,Pune,Premium,5,"?7,450.00"
CUST00006,Delhi NCR,Repeat,2,"?1,980.00"
CUST00007,Mumbai,New,1,?850.00
CUST00008,Bengaluru,Premium,6,"?9,200.00"
CUST00009,Kolkata,Repeat,2,"?2,450.00"
CUST00010,Ahmedabad,New,1,?990.00
CUST00011,Chennai,Repeat,3,"?3,620.00"
CUST00012,Delhi NCR,Premium,4,"?6,100.00"
CUST00013,Bengaluru,New,1,"?1,250.00"
CUST00014,Mumbai,Repeat,3,"?4,320.00"
CUST00015,Jaipur,New,1,?760.00
CUST00016,Lucknow,Repeat,2,"?2,150.00"
CUST00017,Chandigarh,Premium,4,"?5,900.00"
CUST00018,Delhi NCR,Repeat,3,"?4,120.00"
CUST00019,Bengaluru,Repeat,2,"?2,890.00"
CUST00020,Mumbai,Premium,5,"?8,100.00"`;

export function getParsedCompetitorRows() {
  return parseCsv(CSV_COMPETITOR_DATA).map(r => ({
    date: r.Date,
    category: r.Category,
    competitorBrand: r.Competitor_Brand,
    comparableProduct: r.Comparable_Product,
    price: r.Price,
    mrp: r.MRP,
    discount: r.Discount,
    rating: r.Rating,
    reviewCount: r.Review_Count,
    availability: r.Availability,
    organicSearchPosition: r.Organic_Search_Position,
    promotion: r.Promotion,
  }));
}

export function getParsedCustomerRows() {
  return parseCsv(CSV_CUSTOMER_DATA).map(r => ({
    customerId: r.Customer_ID,
    location: r.Location,
    segment: r.Segment,
    orderFrequency: r.Order_Frequency,
    lifetimeValue: r.Lifetime_Value,
  }));
}
