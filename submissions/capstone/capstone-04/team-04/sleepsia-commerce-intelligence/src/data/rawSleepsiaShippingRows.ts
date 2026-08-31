/**
 * Updated Sleepsia Shipping Records from Logistics Manifest
 */

export interface RawShippingManifestRow {
  orderId: string;
  date: string;
  platform: string;
  sku: string;
  warehouse: string;
  carrier: string;
  orderDate: string;
  shipDate: string;
  expectedDeliveryDate: string;
  actualDeliveryDate?: string;
  shipmentStatus: string;
  deliveryStatus: string;
  shippingCost: number;
  delayReason?: string;
}

export const CSV_SHIPPING_DATA = `Order_ID,Date,Platform,SKU,Warehouse,Carrier,Order_Date,Ship_Date,Expected_Delivery_Date,Actual_Delivery_Date,Shipment_Status,Delivery_Status,Shipping_Cost,Delay_Reason
ORD-0801-SLP0001-FLI,2026-08-01,Flipkart,SLP0001,Bengaluru,Ecom Express,2026-08-01,2026-08-02,2026-08-05,2026-08-04,Delivered,On-time,49.79,None
ORD-0801-SLP0001-INS,2026-08-01,Instamart,SLP0001,Mumbai,Swiggy Instamart Logistics,2026-08-01,2026-08-02,2026-08-01,2026-08-02,Delivered,Late,29.40,None
ORD-0801-SLP0001-MYN,2026-08-01,Myntra,SLP0001,Bengaluru,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,58.90,None
ORD-0801-SLP0001-MEE,2026-08-01,Meesho,SLP0001,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-06,2026-08-06,Delivered,On-time,52.40,None
ORD-0801-SLP0001-MYS,2026-08-01,MyStore,SLP0001,Bengaluru,Delhivery,2026-08-01,2026-08-01,2026-08-07,2026-08-07,Delivered,On-time,60.38,None
ORD-0801-SLP0002-AMA,2026-08-01,Amazon,SLP0002,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-03,2026-08-02,Delivered,On-time,63.96,None
ORD-0801-SLP0002-FLI,2026-08-01,Flipkart,SLP0002,Hyderabad,Ekart,2026-08-01,2026-08-01,2026-08-04,2026-08-04,Delivered,On-time,50.72,None
ORD-0801-SLP0002-MEE,2026-08-01,Meesho,SLP0002,Noida,Xpressbees,2026-08-01,2026-08-01,2026-08-07,2026-08-06,Delivered,On-time,53.11,None
ORD-0801-SLP0002-PEP,2026-08-01,Pepperfry,SLP0002,Mumbai,Delhivery,2026-08-01,2026-08-01,2026-08-07,2026-08-07,Delivered,On-time,66.10,None
ORD-0801-SLP0002-SLE,2026-08-01,Sleepbee,SLP0002,Noida,Ecom Express,2026-08-01,2026-08-01,2026-08-06,2026-08-07,Delivered,Late,43.41,Warehouse processing
ORD-0801-SLP0026-AMA,2026-08-01,Amazon,SLP0026,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-03,2026-08-05,Delivered,Late,57.55,Weather disruption
ORD-0801-SLP0026-FLI,2026-08-01,Flipkart,SLP0026,Noida,Ecom Express,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,44.25,None
ORD-0801-SLP0027-AMA,2026-08-01,Amazon,SLP0027,Hyderabad,Delhivery,2026-08-01,2026-08-01,2026-08-04,2026-08-04,Delivered,On-time,76.21,None
ORD-0801-SLP0027-FLI,2026-08-01,Flipkart,SLP0027,Hyderabad,Ekart,2026-08-01,2026-08-02,2026-08-03,2026-08-03,Delivered,On-time,60.63,None
ORD-0801-SLP0027-BLI,2026-08-01,Blinkit,SLP0027,Mumbai,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-01,,Failed,Failed,28.17,Address issue
ORD-0801-SLP0027-MYN,2026-08-01,Myntra,SLP0027,Delhi NCR,Blue Dart,2026-08-01,2026-08-02,2026-08-04,2026-08-04,Delivered,On-time,76.03,None
ORD-0801-SLP0027-MEE,2026-08-01,Meesho,SLP0027,Bengaluru,Ecom Express,2026-08-01,2026-08-02,2026-08-06,2026-08-06,Delivered,On-time,55.36,None
ORD-0801-SLP0027-SLE,2026-08-01,Sleepbee,SLP0027,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-06,2026-08-05,Delivered,On-time,52.80,None
ORD-0801-SLP0027-ZOO,2026-08-01,Zoozle,SLP0027,Noida,Delhivery,2026-08-01,2026-08-02,2026-08-06,2026-08-05,Delivered,On-time,63.86,None
ORD-0801-SLP0032-AMA,2026-08-01,Amazon,SLP0032,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-03,2026-08-02,Delivered,On-time,50.82,None
ORD-0801-SLP0032-FLI,2026-08-01,Flipkart,SLP0032,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-04,2026-08-04,Delivered,On-time,60.00,None
ORD-0801-SLP0032-BLI,2026-08-01,Blinkit,SLP0032,Mumbai,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-01,2026-08-01,Delivered,On-time,25.36,None
ORD-0801-SLP0032-MYN,2026-08-01,Myntra,SLP0032,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,55.35,None
ORD-0801-SLP0032-FIR,2026-08-01,FirstCry,SLP0032,Mumbai,Ecom Express,2026-08-01,2026-08-02,2026-08-05,2026-08-06,Shipped,Pending,57.40,Warehouse processing
ORD-0801-SLP0032-NYK,2026-08-01,Nykaa,SLP0032,Mumbai,Delhivery,2026-08-01,2026-08-01,2026-08-04,2026-08-03,Delivered,On-time,64.03,None
ORD-0801-SLP0032-MEE,2026-08-01,Meesho,SLP0032,Hyderabad,Xpressbees,2026-08-01,2026-08-01,2026-08-06,2026-08-05,Delivered,On-time,52.87,None
ORD-0801-SLP0032-JIO,2026-08-01,JioMart,SLP0032,Noida,Delhivery,2026-08-01,2026-08-02,2026-08-03,2026-08-03,Delivered,On-time,55.28,None
ORD-0801-SLP0032-TAT,2026-08-01,Tata 1mg,SLP0032,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-03,2026-08-02,Delivered,On-time,50.77,None
ORD-0801-SLP0033-AMA,2026-08-01,Amazon,SLP0033,Hyderabad,Blue Dart,2026-08-01,2026-08-01,2026-08-03,2026-08-03,Delivered,On-time,70.64,None
ORD-0801-SLP0033-FLI,2026-08-01,Flipkart,SLP0033,Hyderabad,Ekart,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,50.20,None
ORD-0801-SLP0033-MYN,2026-08-01,Myntra,SLP0033,Mumbai,Blue Dart,2026-08-01,2026-08-02,2026-08-05,2026-08-05,Delivered,On-time,58.90,None
ORD-0801-SLP0033-FIR,2026-08-01,FirstCry,SLP0033,Bengaluru,Delhivery,2026-08-01,2026-08-01,2026-08-06,2026-08-06,Delivered,On-time,58.55,None
ORD-0801-SLP0033-JIO,2026-08-01,JioMart,SLP0033,Bengaluru,Delhivery,2026-08-01,2026-08-02,2026-08-05,2026-08-05,Delivered,On-time,55.25,None
ORD-0801-SLP0033-ZOO,2026-08-01,Zoozle,SLP0033,Mumbai,Delhivery,2026-08-01,2026-08-01,2026-08-07,2026-08-07,Delivered,On-time,54.67,None
ORD-0801-SLP0040-FLI,2026-08-01,Flipkart,SLP0040,Bengaluru,Ecom Express,2026-08-01,2026-08-01,2026-08-03,2026-08-03,Delivered,On-time,59.31,None
ORD-0801-SLP0040-BLI,2026-08-01,Blinkit,SLP0040,Mumbai,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-02,2026-08-02,Delivered,On-time,23.58,None
ORD-0801-SLP0040-INS,2026-08-01,Instamart,SLP0040,Delhi NCR,Swiggy Instamart Logistics,2026-08-01,2026-08-01,2026-08-01,2026-08-01,Delivered,On-time,25.13,None
ORD-0801-SLP0040-MYN,2026-08-01,Myntra,SLP0040,Delhi NCR,Blue Dart,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,57.57,None
ORD-0801-SLP0040-NYK,2026-08-01,Nykaa,SLP0040,Bengaluru,Delhivery,2026-08-01,2026-08-02,2026-08-06,2026-08-06,Delivered,On-time,55.33,None
ORD-0801-SLP0040-MEE,2026-08-01,Meesho,SLP0040,Hyderabad,Xpressbees,2026-08-01,2026-08-02,2026-08-05,2026-08-04,Delivered,On-time,51.54,None
ORD-0801-SLP0040-JIO,2026-08-01,JioMart,SLP0040,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-06,2026-08-07,Delivered,Late,54.28,Carrier capacity
ORD-0801-SLP0040-PEP,2026-08-01,Pepperfry,SLP0040,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-08,2026-08-07,Delivered,On-time,67.28,None
ORD-0801-SLP0040-TAT,2026-08-01,Tata 1mg,SLP0040,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-04,2026-08-03,Delivered,On-time,58.17,None
ORD-0801-SLP0041-FLI,2026-08-01,Flipkart,SLP0041,Bengaluru,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-04,Delivered,On-time,52.70,None
ORD-0801-SLP0041-INS,2026-08-01,Instamart,SLP0041,Delhi NCR,Swiggy Instamart Logistics,2026-08-01,2026-08-01,2026-08-01,2026-08-04,Delivered,Late,28.94,Weather disruption
ORD-0801-SLP0041-MYN,2026-08-01,Myntra,SLP0041,Bengaluru,Ecom Express,2026-08-01,2026-08-02,2026-08-05,2026-08-05,Delivered,On-time,59.01,None
ORD-0801-SLP0041-FIR,2026-08-01,FirstCry,SLP0041,Mumbai,Ecom Express,2026-08-01,2026-08-01,2026-08-06,2026-08-05,Delivered,On-time,48.75,None
ORD-0801-SLP0041-JIO,2026-08-01,JioMart,SLP0041,Bengaluru,Shadowfax,2026-08-01,2026-08-01,2026-08-05,2026-08-04,Delivered,On-time,52.90,None
ORD-0801-SLP0041-PEP,2026-08-01,Pepperfry,SLP0041,Noida,Gati,2026-08-01,2026-08-01,2026-08-07,2026-08-07,Delivered,On-time,65.87,None
ORD-0801-SLP0041-TAT,2026-08-01,Tata 1mg,SLP0041,Noida,Blue Dart,2026-08-01,2026-08-01,2026-08-03,2026-08-03,Delivered,On-time,58.66,None
ORD-0801-SLP0046-AMA,2026-08-01,Amazon,SLP0046,Hyderabad,Delhivery,2026-08-01,2026-08-02,2026-08-04,2026-08-04,Delivered,On-time,61.95,None
ORD-0801-SLP0046-FLI,2026-08-01,Flipkart,SLP0046,Noida,Ekart,2026-08-01,2026-08-01,2026-08-04,2026-08-03,Delivered,On-time,48.75,None
ORD-0801-SLP0046-MYN,2026-08-01,Myntra,SLP0046,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-06,2026-08-05,Delivered,On-time,58.21,None
ORD-0801-SLP0046-MEE,2026-08-01,Meesho,SLP0046,Bengaluru,Xpressbees,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,43.81,None
ORD-0801-SLP0046-PEP,2026-08-01,Pepperfry,SLP0046,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-06,2026-08-07,Delivered,Late,61.32,Address verification
ORD-0801-SLP0046-MYS,2026-08-01,MyStore,SLP0046,Bengaluru,Ecom Express,2026-08-01,2026-08-02,2026-08-07,2026-08-07,Delivered,On-time,52.07,None
ORD-0801-SLP0046-ZOO,2026-08-01,Zoozle,SLP0046,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-04,2026-08-04,Delivered,On-time,42.80,None
ORD-0801-SLP0047-AMA,2026-08-01,Amazon,SLP0047,Mumbai,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,53.07,None
ORD-0801-SLP0047-BLI,2026-08-01,Blinkit,SLP0047,Delhi NCR,Blinkit Dark Store,2026-08-01,2026-08-02,2026-08-02,2026-08-02,Delivered,On-time,27.00,None
ORD-0801-SLP0047-MYN,2026-08-01,Myntra,SLP0047,Delhi NCR,Delhivery,2026-08-01,2026-08-01,2026-08-06,2026-08-06,Delivered,On-time,59.70,None
ORD-0801-SLP0047-JIO,2026-08-01,JioMart,SLP0047,Mumbai,Delhivery,2026-08-01,2026-08-02,2026-08-04,2026-08-04,Delivered,On-time,53.47,None
ORD-0801-SLP0056-FLI,2026-08-01,Flipkart,SLP0056,Bengaluru,Ecom Express,2026-08-01,2026-08-01,2026-08-03,2026-08-03,Delivered,On-time,46.93,None
ORD-0801-SLP0056-BLI,2026-08-01,Blinkit,SLP0056,Mumbai,Blinkit Dark Store,2026-08-01,2026-08-02,2026-08-02,2026-08-02,Delivered,On-time,21.47,None
ORD-0801-SLP0056-MYN,2026-08-01,Myntra,SLP0056,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,53.43,None
ORD-0801-SLP0056-JIO,2026-08-01,JioMart,SLP0056,Bengaluru,Delhivery,2026-08-01,2026-08-02,2026-08-06,2026-08-06,Delivered,On-time,45.73,None
ORD-0801-SLP0056-ZOO,2026-08-01,Zoozle,SLP0056,Mumbai,Ecom Express,2026-08-01,2026-08-01,2026-08-06,2026-08-06,Delivered,On-time,48.99,None
ORD-0801-SLP0057-AMA,2026-08-01,Amazon,SLP0057,Noida,Ecom Express,2026-08-01,2026-08-02,2026-08-05,2026-08-05,Delivered,On-time,43.42,None
ORD-0801-SLP0057-FLI,2026-08-01,Flipkart,SLP0057,Noida,Ekart,2026-08-01,2026-08-01,2026-08-04,2026-08-03,Delivered,On-time,55.42,None
ORD-0801-SLP0057-MYN,2026-08-01,Myntra,SLP0057,Delhi NCR,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,55.20,None
ORD-0801-SLP0057-FIR,2026-08-01,FirstCry,SLP0057,Bengaluru,Delhivery,2026-08-01,2026-08-01,2026-08-04,2026-08-04,Delivered,On-time,46.26,None
ORD-0801-SLP0057-MEE,2026-08-01,Meesho,SLP0057,Hyderabad,Xpressbees,2026-08-01,2026-08-01,2026-08-06,2026-08-05,Delivered,On-time,44.50,None
ORD-0801-SLP0064-AMA,2026-08-01,Amazon,SLP0064,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-03,2026-08-02,Delivered,On-time,66.97,None
ORD-0801-SLP0064-BLI,2026-08-01,Blinkit,SLP0064,Delhi NCR,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-01,2026-08-01,Delivered,On-time,19.96,None
ORD-0801-SLP0064-INS,2026-08-01,Instamart,SLP0064,Mumbai,Swiggy Instamart Logistics,2026-08-01,2026-08-01,2026-08-02,2026-08-02,Delivered,On-time,29.46,None
ORD-0801-SLP0064-MYN,2026-08-01,Myntra,SLP0064,Delhi NCR,Blue Dart,2026-08-01,2026-08-02,2026-08-06,2026-08-06,Delivered,On-time,48.66,None
ORD-0801-SLP0064-MEE,2026-08-01,Meesho,SLP0064,Bengaluru,Ecom Express,2026-08-01,2026-08-02,2026-08-05,2026-08-05,Delivered,On-time,52.31,None
ORD-0801-SLP0064-TAT,2026-08-01,Tata 1mg,SLP0064,Bengaluru,Delhivery,2026-08-01,2026-08-02,2026-08-05,2026-08-05,Delivered,On-time,50.34,None
ORD-0801-SLP0065-AMA,2026-08-01,Amazon,SLP0065,Noida,Ecom Express,2026-08-01,2026-08-02,2026-08-05,2026-08-05,Delivered,On-time,65.91,None
ORD-0801-SLP0065-FIR,2026-08-01,FirstCry,SLP0065,Noida,Ecom Express,2026-08-01,2026-08-02,2026-08-06,2026-08-06,Delivered,On-time,44.02,None
ORD-0801-SLP0065-NYK,2026-08-01,Nykaa,SLP0065,Bengaluru,Delhivery,2026-08-01,2026-08-02,2026-08-04,2026-08-06,Delivered,Late,56.57,Warehouse processing
ORD-0801-SLP0065-JIO,2026-08-01,JioMart,SLP0065,Mumbai,Shadowfax,2026-08-01,2026-08-01,2026-08-03,2026-08-02,Delivered,On-time,53.55,None
ORD-0801-SLP0065-PEP,2026-08-01,Pepperfry,SLP0065,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-06,2026-08-05,Delivered,On-time,64.47,None
ORD-0801-SLP0065-TAT,2026-08-01,Tata 1mg,SLP0065,Mumbai,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-07,Delivered,Late,51.03,Warehouse processing
ORD-0801-SLP0068-AMA,2026-08-01,Amazon,SLP0068,Bengaluru,Ecom Express,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,61.44,None
ORD-0801-SLP0068-BLI,2026-08-01,Blinkit,SLP0068,Delhi NCR,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-02,2026-08-02,Delivered,On-time,33.22,None
ORD-0801-SLP0068-MYN,2026-08-01,Myntra,SLP0068,Mumbai,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-08,Delayed,Late,52.77,Address verification
ORD-0801-SLP0068-MEE,2026-08-01,Meesho,SLP0068,Bengaluru,Delhivery,2026-08-01,2026-08-01,2026-08-06,2026-08-06,Delivered,On-time,52.56,None
ORD-0801-SLP0069-BLI,2026-08-01,Blinkit,SLP0069,Mumbai,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-02,2026-08-01,Delivered,On-time,23.11,None
ORD-0801-SLP0069-MYN,2026-08-01,Myntra,SLP0069,Mumbai,Ecom Express,2026-08-01,2026-08-01,2026-08-05,2026-08-04,Delivered,On-time,50.02,None
ORD-0801-SLP0069-FIR,2026-08-01,FirstCry,SLP0069,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-04,Delivered,On-time,47.39,None
ORD-0801-SLP0069-NYK,2026-08-01,Nykaa,SLP0069,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-04,2026-08-04,Delivered,On-time,67.80,None
ORD-0801-SLP0069-JIO,2026-08-01,JioMart,SLP0069,Noida,Shadowfax,2026-08-01,2026-08-01,2026-08-06,2026-08-06,Delivered,On-time,44.00,None
ORD-0801-SLP0069-PEP,2026-08-01,Pepperfry,SLP0069,Mumbai,Gati,2026-08-01,2026-08-02,2026-08-08,2026-08-08,Delivered,On-time,64.64,None
ORD-0801-SLP0069-TAT,2026-08-01,Tata 1mg,SLP0069,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-04,2026-08-03,Delivered,On-time,49.90,None
ORD-0801-SLP0070-AMA,2026-08-01,Amazon,SLP0070,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,75.96,None
ORD-0801-SLP0070-FLI,2026-08-01,Flipkart,SLP0070,Hyderabad,Ecom Express,2026-08-01,2026-08-01,2026-08-03,2026-08-03,Delivered,On-time,76.72,None
ORD-0801-SLP0070-BLI,2026-08-01,Blinkit,SLP0070,Delhi NCR,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-02,2026-08-02,Delivered,On-time,36.69,None
ORD-0801-SLP0070-INS,2026-08-01,Instamart,SLP0070,Delhi NCR,Swiggy Instamart Logistics,2026-08-01,2026-08-02,2026-08-02,2026-08-02,Delivered,On-time,30.40,None
ORD-0801-SLP0070-MYN,2026-08-01,Myntra,SLP0070,Mumbai,Delhivery,2026-08-01,2026-08-02,2026-08-06,2026-08-06,Delivered,On-time,54.71,None
ORD-0801-SLP0070-MEE,2026-08-01,Meesho,SLP0070,Hyderabad,Xpressbees,2026-08-01,2026-08-02,2026-08-07,2026-08-07,Delivered,On-time,49.21,None
ORD-0801-SLP0071-AMA,2026-08-01,Amazon,SLP0071,Hyderabad,Delhivery,2026-08-01,2026-08-02,2026-08-04,,Failed,Failed,70.13,Carrier exception
ORD-0801-SLP0071-BLI,2026-08-01,Blinkit,SLP0071,Bengaluru,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-01,2026-08-01,Delivered,On-time,32.21,None
ORD-0801-SLP0071-MYN,2026-08-01,Myntra,SLP0071,Delhi NCR,Ecom Express,2026-08-01,2026-08-01,2026-08-06,2026-08-05,Delivered,On-time,68.02,None
ORD-0801-SLP0071-NYK,2026-08-01,Nykaa,SLP0071,Noida,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,57.33,None
ORD-0801-SLP0071-MEE,2026-08-01,Meesho,SLP0071,Bengaluru,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,48.44,None
ORD-0801-SLP0071-JIO,2026-08-01,JioMart,SLP0071,Bengaluru,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-06,Delivered,Late,48.73,Warehouse processing
ORD-0801-SLP0071-TAT,2026-08-01,Tata 1mg,SLP0071,Bengaluru,Blue Dart,2026-08-01,2026-08-01,2026-08-04,2026-08-04,Delivered,On-time,45.30,None
ORD-0801-SLP0077-AMA,2026-08-01,Amazon,SLP0077,Bengaluru,Blue Dart,2026-08-01,2026-08-02,2026-08-05,2026-08-05,Delivered,On-time,65.62,None
ORD-0801-SLP0077-BLI,2026-08-01,Blinkit,SLP0077,Delhi NCR,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-02,2026-08-02,Delivered,On-time,31.33,None
ORD-0801-SLP0077-MEE,2026-08-01,Meesho,SLP0077,Bengaluru,Ecom Express,2026-08-01,2026-08-01,2026-08-04,2026-08-04,Delivered,On-time,51.70,None
ORD-0801-SLP0077-JIO,2026-08-01,JioMart,SLP0077,Mumbai,Delhivery,2026-08-01,2026-08-01,2026-08-05,2026-08-05,Delivered,On-time,52.72,None
ORD-0801-SLP0078-AMA,2026-08-01,Amazon,SLP0078,Bengaluru,Ecom Express,2026-08-01,2026-08-01,2026-08-03,2026-08-03,Delivered,On-time,47.14,None
ORD-0801-SLP0078-BLI,2026-08-01,Blinkit,SLP0078,Mumbai,Blinkit Dark Store,2026-08-01,2026-08-01,2026-08-02,2026-08-02,Delivered,On-time,26.38,None
ORD-0801-SLP0078-MYN,2026-08-01,Myntra,SLP0078,Delhi NCR,Ecom Express,2026-08-01,2026-08-01,2026-08-05,2026-08-04,Delivered,On-time,55.64,None
ORD-0801-SLP0078-JIO,2026-08-01,JioMart,SLP0078,Mumbai,Shadowfax,2026-08-01,2026-08-01,2026-08-06,2026-08-06,Delivered,On-time,44.84,None`;

export function getParsedShippingRows(): RawShippingManifestRow[] {
  const lines = CSV_SHIPPING_DATA.trim().split('\n');
  if (lines.length <= 1) return [];
  const records: RawShippingManifestRow[] = [];
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    const parts = line.split(',');
    if (parts.length >= 13) {
      records.push({
        orderId: parts[0],
        date: parts[1],
        platform: parts[2],
        sku: parts[3],
        warehouse: parts[4],
        carrier: parts[5],
        orderDate: parts[6],
        shipDate: parts[7],
        expectedDeliveryDate: parts[8],
        actualDeliveryDate: parts[9] || undefined,
        shipmentStatus: parts[10],
        deliveryStatus: parts[11],
        shippingCost: parseFloat(parts[12]) || 50,
        delayReason: parts[13] && parts[13] !== 'None' ? parts[13] : undefined,
      });
    }
  }
  return records;
}
