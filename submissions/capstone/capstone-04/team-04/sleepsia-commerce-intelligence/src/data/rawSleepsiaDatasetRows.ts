/**
 * Embedded Sleepsia CSV Prototype Dataset
 * Direct representation of attached Sleepsia CSV tables
 */

function parseCsv(csvText: string): Record<string, string>[] {
  const lines = csvText.trim().split('\n');
  if (lines.length <= 1) return [];
  
  // Custom CSV parser handling quotes with commas
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

export const CSV_PRODUCT_MASTER = `SKU,Product_ID,Product_Name,Category,Brand,Variant,Size,Material,Colour,EAN_GTIN,Product_Lifecycle,MRP,Base_COGS
SLP0001,PID-0001,Memory Foam Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Polyester,Black,890610000001,Active,"?1,000.00",?336.73
SLP0002,PID-0002,Memory Foam Pillow with Cooling Gel,Sleeping Pillows,Sleepsia,Standard,Standard,Polyester,Beige,890610000002,Active,?710.00,?222.26
SLP0003,PID-0003,Memory Foam Pillow with Ventilated Cooling Gel,Sleeping Pillows,Sleepsia,Standard,Standard,Memory Foam,Grey,890610000003,Active,?880.00,?294.71
SLP0004,PID-0004,Small Memory Foam Pillow with Cooling Gel,Sleeping Pillows,Sleepsia,Standard,Medium,Microfiber,Beige,890610000004,Active,?980.00,?355.67
SLP0005,PID-0005,Ventilated Memory Foam Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Memory Foam,Grey,890610000005,Active,?890.00,?360.20
SLP0006,PID-0006,Bamboo Memory Foam Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Microfiber,Black,890610000006,Active,?830.00,?261.73
SLP0007,PID-0007,Shredded Memory Foam Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Cotton,Beige,890610000007,Active,?850.00,?288.73
SLP0008,PID-0008,Adjustable Shredded Memory Foam Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Satin,White,890610000008,Active,?660.00,?294.34
SLP0009,PID-0009,Bamboo Adjustable Memory Foam Pillow,Sleeping Pillows,Sleepsia,Standard,Medium,Cotton,Beige,890610000009,Active,?850.00,?367.90
SLP0010,PID-0010,Premium Bamboo Memory Foam Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Polyester,White,890610000010,Active,?840.00,?257.77
SLP0011,PID-0011,Orthopedic Cervical Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Memory Foam,Grey,890610000011,Active,?760.00,?326.78
SLP0012,PID-0012,Orthopedic Cervical Pillow with Cooling Gel,Sleeping Pillows,Sleepsia,Standard,Standard,Polyester,Black,890610000012,Active,?850.00,?275.74
SLP0013,PID-0013,Contour Orthopedic Pillow,Sleeping Pillows,Sleepsia,Standard,Medium,Cotton,White,890610000013,Active,?840.00,?328.75
SLP0014,PID-0014,Contour Orthopedic Pillow with Ventilated Cooling Gel,Sleeping Pillows,Sleepsia,Standard,Medium,Microfiber,Grey,890610000014,Active,?730.00,?269.62
SLP0015,PID-0015,Butterfly Pillow for Neck Pain,Sleeping Pillows,Sleepsia,Standard,Medium,Polyester,Beige,890610000015,Active,?790.00,?263.02
SLP0016,PID-0016,Neck Pain Relief Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Microfiber,White,890610000016,Active,?820.00,?345.02
SLP0017,PID-0017,Cervical Support Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Microfiber,Beige,890610000017,Active,?860.00,?371.05
SLP0018,PID-0018,Microfiber Sleeping Pillow,Sleeping Pillows,Sleepsia,Standard,Medium,Bamboo,Blue,890610000018,Active,?810.00,?350.49
SLP0019,PID-0019,Hotel Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Cotton,Grey,890610000019,Active,"?1,010.00",?340.36
SLP0020,PID-0020,Premium Microfiber Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Polyester,Beige,890610000020,Active,?960.00,?349.69
SLP0021,PID-0021,Ultra Soft Down Alternative Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Microfiber,Grey,890610000021,Active,?970.00,?365.14
SLP0022,PID-0022,Luxury Microfiber Pillow,Sleeping Pillows,Sleepsia,Standard,Standard,Memory Foam,Grey,890610000022,Active,?680.00,?268.00
SLP0023,PID-0023,Cloud Pillow - Red,Sleeping Pillows,Sleepsia,Standard,Standard,Satin,White,890610000023,Active,"?1,090.00",?389.91
SLP0024,PID-0024,Cloud Pillow - Green,Sleeping Pillows,Sleepsia,Standard,Standard,Satin,Black,890610000024,Active,?980.00,?436.75
SLP0025,PID-0025,Family Pillows,Sleeping Pillows,Sleepsia,Standard,Standard,Polyester,White,890610000025,Active,"?1,130.00",?454.55
SLP0026,PID-0026,Full Body Long Cuddle Pillow,Pregnancy & Body Pillows,Sleepsia,Standard,Standard,Polyester,Black,890610000026,Active,"?1,470.00",?465.60
SLP0027,PID-0027,Full Body Pillow,Pregnancy & Body Pillows,Sleepsia,Standard,Standard,Memory Foam,Black,890610000027,Active,"?1,380.00",?615.18
SLP0028,PID-0028,C-Shape Pregnancy Pillow,Pregnancy & Body Pillows,Sleepsia,Standard,Medium,Memory Foam,Black,890610000028,Active,"?1,670.00",?711.84
SLP0029,PID-0029,J-Shape Pregnancy Pillow,Pregnancy & Body Pillows,Sleepsia,Standard,Standard,Microfiber,Black,890610000029,Active,"?1,440.00",?596.70
SLP0030,PID-0030,U-Shape Pregnancy Pillow,Pregnancy & Body Pillows,Sleepsia,Standard,Medium,Memory Foam,Beige,890610000030,Active,"?1,470.00",?512.48
SLP0031,PID-0031,Full Body Shredded Memory Foam Pillow,Pregnancy & Body Pillows,Sleepsia,Standard,Standard,Cotton,Grey,890610000031,Active,"?1,000.00",?308.69
SLP0032,PID-0032,Kids Bamboo Pillow,Kids & Baby Pillows,Sleepsia,Standard,Standard,Memory Foam,Blue,890610000032,Active,?830.00,?350.59
SLP0033,PID-0033,Kids Microfiber Pillow,Kids & Baby Pillows,Sleepsia,Standard,Medium,Microfiber,Grey,890610000033,Active,?870.00,?347.10
SLP0034,PID-0034,Kids Cat Shape Memory Foam Pillow,Kids & Baby Pillows,Sleepsia,Standard,Standard,Cotton,Beige,890610000034,Active,?860.00,?370.54
SLP0035,PID-0035,Kids Butterfly Shape Memory Foam Pillow,Kids & Baby Pillows,Sleepsia,Standard,Standard,Satin,Grey,890610000035,Active,?630.00,?256.37
SLP0036,PID-0036,Kids Alpha Pillow,Kids & Baby Pillows,Sleepsia,Standard,Medium,Polyester,Black,890610000036,Active,?620.00,?226.74
SLP0037,PID-0037,Baby Pillow,Kids & Baby Pillows,Sleepsia,Standard,Standard,Microfiber,Grey,890610000037,Active,?670.00,?207.43
SLP0038,PID-0038,Baby Feeding Pillow,Kids & Baby Pillows,Sleepsia,Standard,Medium,Microfiber,Beige,890610000038,Active,?460.00,?153.19
SLP0039,PID-0039,Microfiber Baby Pillow,Kids & Baby Pillows,Sleepsia,Standard,Medium,Memory Foam,Grey,890610000039,Active,?480.00,?148.85
SLP0040,PID-0040,Memory Foam Travel Neck Pillow,Travel & Car Comfort,Sleepsia,Standard,Standard,Memory Foam,Beige,890610000040,Active,?500.00,?167.85
SLP0041,PID-0041,Snoozed Travel Neck Pillow,Travel & Car Comfort,Sleepsia,Standard,Standard,Satin,Grey,890610000041,Active,?790.00,?322.72
SLP0042,PID-0042,Velvet Travel Neck Pillow,Travel & Car Comfort,Sleepsia,Standard,Medium,Bamboo,Grey,890610000042,Active,?890.00,?371.75
SLP0043,PID-0043,Car Neck Rest Memory Foam Pillow,Travel & Car Comfort,Sleepsia,Standard,Standard,Memory Foam,White,890610000043,Active,?860.00,?343.01
SLP0044,PID-0044,Car Head Rest Pillow,Travel & Car Comfort,Sleepsia,Standard,Standard,Bamboo,White,890610000044,Active,?650.00,?260.65
SLP0045,PID-0045,Ergonomic Semi Roll Pillow,Travel & Car Comfort,Sleepsia,Standard,Standard,Memory Foam,Blue,890610000045,Active,?940.00,?384.68
SLP0046,PID-0046,Wedge Pillow,Back Support & Seat Cushions,Sleepsia,Standard,Standard,Microfiber,Grey,890610000046,Active,"?1,220.00",?400.81
SLP0047,PID-0047,Lumbar Support Pillow,Back Support & Seat Cushions,Sleepsia,Standard,Standard,Microfiber,Black,890610000047,Active,?990.00,?365.70
SLP0048,PID-0048,Lumbar Support Pillow with Cooling Gel,Back Support & Seat Cushions,Sleepsia,Standard,Standard,Bamboo,Beige,890610000048,Active,"?1,270.00",?399.65
SLP0049,PID-0049,Lumbar Support Pillow with Ventilated Cooling Gel,Back Support & Seat Cushions,Sleepsia,Standard,Medium,Memory Foam,White,890610000049,Active,"?1,120.00",?491.63
SLP0050,PID-0050,Half Lumbar Support Pillow,Back Support & Seat Cushions,Sleepsia,Standard,Standard,Bamboo,Blue,890610000050,Active,"?1,250.00",?465.25
SLP0051,PID-0051,Backrest Cushion,Back Support & Seat Cushions,Sleepsia,Standard,Standard,Microfiber,Blue,890610000051,Active,"?1,260.00",?378.41
SLP0052,PID-0052,Coccyx Seat Cushion,Back Support & Seat Cushions,Sleepsia,Standard,Standard,Cotton,Blue,890610000052,Active,?950.00,?384.26
SLP0053,PID-0053,U-Shaped Coccyx Cushion,Back Support & Seat Cushions,Sleepsia,Standard,Medium,Polyester,Blue,890610000053,Active,"?1,170.00",?378.17
SLP0054,PID-0054,Donut Seat Cushion with Cooling Gel,Back Support & Seat Cushions,Sleepsia,Standard,Standard,Satin,Beige,890610000054,Active,?890.00,?275.14
SLP0055,PID-0055,Orthopedic Seat Cushion,Back Support & Seat Cushions,Sleepsia,Standard,Standard,Satin,Blue,890610000055,Active,?900.00,?337.88
SLP0056,PID-0056,Pillow Protectors,Pillow Covers & Protectors,Sleepsia,Standard,Standard,Memory Foam,Beige,890610000056,Active,?560.00,?174.73
SLP0057,PID-0057,Pillow Covers,Pillow Covers & Protectors,Sleepsia,Standard,Medium,Memory Foam,Grey,890610000057,Active,?370.00,?133.41
SLP0058,PID-0058,Pillow Cases,Pillow Covers & Protectors,Sleepsia,Standard,Medium,Microfiber,Beige,890610000058,Active,?590.00,?229.61
SLP0059,PID-0059,Satin Pillow Cover - Rose Taupe,Pillow Covers & Protectors,Sleepsia,Standard,Standard,Polyester,Beige,890610000059,Active,?500.00,?192.39
SLP0060,PID-0060,Satin Pillow Cover - Silver,Pillow Covers & Protectors,Sleepsia,Standard,Standard,Microfiber,Black,890610000060,Active,?410.00,?137.68
SLP0061,PID-0061,Satin Pillow Cover - Brown,Pillow Covers & Protectors,Sleepsia,Standard,Medium,Polyester,Black,890610000061,Active,?430.00,?158.49
SLP0062,PID-0062,Satin Pillow Cover - Beige,Pillow Covers & Protectors,Sleepsia,Standard,Standard,Memory Foam,Blue,890610000062,Active,?590.00,?231.97
SLP0063,PID-0063,Satin Pillow Cover - Black,Pillow Covers & Protectors,Sleepsia,Standard,Standard,Memory Foam,Beige,890610000063,Active,?480.00,?159.35
SLP0064,PID-0064,King Size Bedsheets,Bedding Products,Sleepsia,Standard,Standard,Memory Foam,Grey,890610000064,Active,"?1,090.00",?387.42
SLP0065,PID-0065,Queen Size Bedsheets,Bedding Products,Sleepsia,Standard,Medium,Polyester,Black,890610000065,Active,"?1,000.00",?391.75
SLP0066,PID-0066,Satin Bedsheets,Bedding Products,Sleepsia,Standard,Medium,Satin,White,890610000066,Active,"?1,680.00",?672.30
SLP0067,PID-0067,Bedsheet + Pillow Combo,Bedding Products,Sleepsia,Standard,Medium,Memory Foam,Grey,890610000067,Active,"?1,330.00",?451.76
SLP0068,PID-0068,Dog Beds,Pet Products,Sleepsia,Standard,Medium,Satin,Grey,890610000068,Active,"?1,850.00",?630.58
SLP0069,PID-0069,Pet Beds,Pet Products,Sleepsia,Standard,Medium,Cotton,Grey,890610000069,Active,"?1,590.00",?640.97
SLP0070,PID-0070,Electric Aroma Diffuser 200ml,Wellness & Home,Sleepsia,Standard,Medium,Bamboo,Black,890610000070,Active,"?1,820.00",?793.16
SLP0071,PID-0071,Electric Aroma Diffuser 300ml,Wellness & Home,Sleepsia,Standard,Standard,Polyester,Blue,890610000071,Active,"?1,810.00",?768.17
SLP0072,PID-0072,Electric Aroma Diffuser 400ml,Wellness & Home,Sleepsia,Standard,Standard,Microfiber,Black,890610000072,Active,"?1,060.00",?343.69
SLP0073,PID-0073,Electric Glass Aroma Diffuser,Wellness & Home,Sleepsia,Standard,Medium,Bamboo,Beige,890610000073,Active,"?1,430.00",?431.07
SLP0074,PID-0074,Electric Plastic Aroma Diffuser,Wellness & Home,Sleepsia,Standard,Medium,Microfiber,Beige,890610000074,Active,"?1,090.00",?332.89
SLP0075,PID-0075,Ultrasonic Room Humidifier,Wellness & Home,Sleepsia,Standard,Medium,Microfiber,Blue,890610000075,Active,"?1,360.00",?434.00
SLP0076,PID-0076,Humidifier 4L,Wellness & Home,Sleepsia,Standard,Standard,Cotton,Grey,890610000076,Active,"?1,310.00",?527.03
SLP0077,PID-0077,Heart-Shaped Pillow,Speciality Pillows,Sleepsia,Standard,Standard,Satin,Blue,890610000077,Active,"?1,080.00",?481.76
SLP0078,PID-0078,Bamboo Pillow,Speciality Pillows,Sleepsia,Standard,Standard,Microfiber,Grey,890610000078,Active,"?1,130.00",?488.40
SLP0079,PID-0079,Cooling Gel Pillow,Speciality Pillows,Sleepsia,Standard,Medium,Cotton,Blue,890610000079,Active,?680.00,?285.83
SLP0080,PID-0080,Orthopedic Memory Foam Pillow,Speciality Pillows,Sleepsia,Standard,Standard,Cotton,Grey,890610000080,Active,"?1,200.00",?501.73
SLP0081,PID-0081,Pain Relief Pillow,Speciality Pillows,Sleepsia,Standard,Standard,Bamboo,Grey,890610000081,Active,?730.00,?240.85`;

export const CSV_COST_DATA = `SKU,Product_ID,COGS,Manufacturing_Cost,Packaging_Cost,Freight_Cost,Warehouse_Cost,Marketplace_Fee_Benchmark,Payment_Fees_Benchmark,Returns_Cost_Benchmark,Cost_Type
SLP0001,PID-0001,?336.73,?10.10,?16.84,?20.20,?8.42,?120.00,?15.00,?13.47,Unit Cost
SLP0002,PID-0002,?222.26,?6.67,?11.11,?13.34,?5.56,?85.20,?10.65,?8.89,Unit Cost
SLP0003,PID-0003,?294.71,?8.84,?14.74,?17.68,?7.37,?105.60,?13.20,?11.79,Unit Cost
SLP0004,PID-0004,?355.67,?10.67,?17.78,?21.34,?8.89,?117.60,?14.70,?14.23,Unit Cost
SLP0005,PID-0005,?360.20,?10.81,?18.01,?21.61,?9.01,?106.80,?13.35,?14.41,Unit Cost
SLP0006,PID-0006,?261.73,?7.85,?13.09,?15.70,?6.54,?99.60,?12.45,?10.47,Unit Cost
SLP0007,PID-0007,?288.73,?8.66,?14.44,?17.32,?7.22,?102.00,?12.75,?11.55,Unit Cost
SLP0008,PID-0008,?294.34,?8.83,?14.72,?17.66,?7.36,?79.20,?9.90,?11.77,Unit Cost
SLP0009,PID-0009,?367.90,?11.04,?18.39,?22.07,?9.20,?102.00,?12.75,?14.72,Unit Cost
SLP0010,PID-0010,?257.77,?7.73,?12.89,?15.47,?6.44,?100.80,?12.60,?10.31,Unit Cost
SLP0011,PID-0011,?326.78,?9.80,?16.34,?19.61,?8.17,?91.20,?11.40,?13.07,Unit Cost
SLP0012,PID-0012,?275.74,?8.27,?13.79,?16.54,?6.89,?102.00,?12.75,?11.03,Unit Cost
SLP0013,PID-0013,?328.75,?9.86,?16.44,?19.72,?8.22,?100.80,?12.60,?13.15,Unit Cost
SLP0014,PID-0014,?269.62,?8.09,?13.48,?16.18,?6.74,?87.60,?10.95,?10.78,Unit Cost
SLP0015,PID-0015,?263.02,?7.89,?13.15,?15.78,?6.58,?94.80,?11.85,?10.52,Unit Cost
SLP0016,PID-0016,?345.02,?10.35,?17.25,?20.70,?8.63,?98.40,?12.30,?13.80,Unit Cost
SLP0017,PID-0017,?371.05,?11.13,?18.55,?22.26,?9.28,?103.20,?12.90,?14.84,Unit Cost
SLP0018,PID-0018,?350.49,?10.51,?17.52,?21.03,?8.76,?97.20,?12.15,?14.02,Unit Cost
SLP0019,PID-0019,?340.36,?10.21,?17.02,?20.42,?8.51,?121.20,?15.15,?13.61,Unit Cost
SLP0020,PID-0020,?349.69,?10.49,?17.48,?20.98,?8.74,?115.20,?14.40,?13.99,Unit Cost
SLP0021,PID-0021,?365.14,?10.95,?18.26,?21.91,?9.13,?116.40,?14.55,?14.61,Unit Cost
SLP0022,PID-0022,?268.00,?8.04,?13.40,?16.08,?6.70,?81.60,?10.20,?10.72,Unit Cost
SLP0023,PID-0023,?389.91,?11.70,?19.50,?23.39,?9.75,?130.80,?16.35,?15.60,Unit Cost
SLP0024,PID-0024,?436.75,?13.10,?21.84,?26.20,?10.92,?117.60,?14.70,?17.47,Unit Cost
SLP0025,PID-0025,?454.55,?13.64,?22.73,?27.27,?11.36,?135.60,?16.95,?18.18,Unit Cost
SLP0026,PID-0026,?465.60,?13.97,?23.28,?27.94,?11.64,?176.40,?22.05,?18.62,Unit Cost
SLP0027,PID-0027,?615.18,?18.46,?30.76,?36.91,?15.38,?165.60,?20.70,?24.61,Unit Cost
SLP0028,PID-0028,?711.84,?21.36,?35.59,?42.71,?17.80,?200.40,?25.05,?28.47,Unit Cost
SLP0029,PID-0029,?596.70,?17.90,?29.84,?35.80,?14.92,?172.80,?21.60,?23.87,Unit Cost
SLP0030,PID-0030,?512.48,?15.37,?25.62,?30.75,?12.81,?176.40,?22.05,?20.50,Unit Cost
SLP0031,PID-0031,?308.69,?9.26,?15.43,?18.52,?7.72,?120.00,?15.00,?12.35,Unit Cost
SLP0032,PID-0032,?350.59,?10.52,?17.53,?21.04,?8.76,?99.60,?12.45,?14.02,Unit Cost
SLP0033,PID-0033,?347.10,?10.41,?17.36,?20.83,?8.68,?104.40,?13.05,?13.88,Unit Cost
SLP0034,PID-0034,?370.54,?11.12,?18.53,?22.23,?9.26,?103.20,?12.90,?14.82,Unit Cost
SLP0035,PID-0035,?256.37,?7.69,?12.82,?15.38,?6.41,?75.60,?9.45,?10.25,Unit Cost
SLP0036,PID-0036,?226.74,?6.80,?11.34,?13.60,?5.67,?74.40,?9.30,?9.07,Unit Cost
SLP0037,PID-0037,?207.43,?6.22,?10.37,?12.45,?5.19,?80.40,?10.05,?8.30,Unit Cost
SLP0038,PID-0038,?153.19,?4.60,?7.66,?9.19,?3.83,?55.20,?6.90,?6.13,Unit Cost
SLP0039,PID-0039,?148.85,?4.47,?7.44,?8.93,?3.72,?57.60,?7.20,?5.95,Unit Cost
SLP0040,PID-0040,?167.85,?5.04,?8.39,?10.07,?4.20,?60.00,?7.50,?6.71,Unit Cost
SLP0041,PID-0041,?322.72,?9.68,?16.14,?19.36,?8.07,?94.80,?11.85,?12.91,Unit Cost
SLP0042,PID-0042,?371.75,?11.15,?18.59,?22.30,?9.29,?106.80,?13.35,?14.87,Unit Cost
SLP0043,PID-0043,?343.01,?10.29,?17.15,?20.58,?8.58,?103.20,?12.90,?13.72,Unit Cost
SLP0044,PID-0044,?260.65,?7.82,?13.03,?15.64,?6.52,?78.00,?9.75,?10.43,Unit Cost
SLP0045,PID-0045,?384.68,?11.54,?19.23,?23.08,?9.62,?112.80,?14.10,?15.39,Unit Cost
SLP0046,PID-0046,?400.81,?12.02,?20.04,?24.05,?10.02,?146.40,?18.30,?16.03,Unit Cost
SLP0047,PID-0047,?365.70,?10.97,?18.29,?21.94,?9.14,?118.80,?14.85,?14.63,Unit Cost
SLP0048,PID-0048,?399.65,?11.99,?19.98,?23.98,?9.99,?152.40,?19.05,?15.99,Unit Cost
SLP0049,PID-0049,?491.63,?14.75,?24.58,?29.50,?12.29,?134.40,?16.80,?19.67,Unit Cost
SLP0050,PID-0050,?465.25,?13.96,?23.26,?27.91,?11.63,?150.00,?18.75,?18.61,Unit Cost
SLP0051,PID-0051,?378.41,?11.35,?18.92,?22.70,?9.46,?151.20,?18.90,?15.14,Unit Cost
SLP0052,PID-0052,?384.26,?11.53,?19.21,?23.06,?9.61,?114.00,?14.25,?15.37,Unit Cost
SLP0053,PID-0053,?378.17,?11.35,?18.91,?22.69,?9.45,?140.40,?17.55,?15.13,Unit Cost
SLP0054,PID-0054,?275.14,?8.25,?13.76,?16.51,?6.88,?106.80,?13.35,?11.01,Unit Cost
SLP0055,PID-0055,?337.88,?10.14,?16.89,?20.27,?8.45,?108.00,?13.50,?13.52,Unit Cost
SLP0056,PID-0056,?174.73,?5.24,?8.74,?10.48,?4.37,?67.20,?8.40,?6.99,Unit Cost
SLP0057,PID-0057,?133.41,?4.00,?6.67,?8.00,?3.34,?44.40,?5.55,?5.34,Unit Cost
SLP0058,PID-0058,?229.61,?6.89,?11.48,?13.78,?5.74,?70.80,?8.85,?9.18,Unit Cost
SLP0059,PID-0059,?192.39,?5.77,?9.62,?11.54,?4.81,?60.00,?7.50,?7.70,Unit Cost
SLP0060,PID-0060,?137.68,?4.13,?6.88,?8.26,?3.44,?49.20,?6.15,?5.51,Unit Cost
SLP0061,PID-0061,?158.49,?4.75,?7.92,?9.51,?3.96,?51.60,?6.45,?6.34,Unit Cost
SLP0062,PID-0062,?231.97,?6.96,?11.60,?13.92,?5.80,?70.80,?8.85,?9.28,Unit Cost
SLP0063,PID-0063,?159.35,?4.78,?7.97,?9.56,?3.98,?57.60,?7.20,?6.37,Unit Cost
SLP0064,PID-0064,?387.42,?11.62,?19.37,?23.25,?9.69,?130.80,?16.35,?15.50,Unit Cost
SLP0065,PID-0065,?391.75,?11.75,?19.59,?23.50,?9.79,?120.00,?15.00,?15.67,Unit Cost
SLP0066,PID-0066,?672.30,?20.17,?33.62,?40.34,?16.81,?201.60,?25.20,?26.89,Unit Cost
SLP0067,PID-0067,?451.76,?13.55,?22.59,?27.11,?11.29,?159.60,?19.95,?18.07,Unit Cost
SLP0068,PID-0068,?630.58,?18.92,?31.53,?37.83,?15.76,?222.00,?27.75,?25.22,Unit Cost
SLP0069,PID-0069,?640.97,?19.23,?32.05,?38.46,?16.02,?190.80,?23.85,?25.64,Unit Cost
SLP0070,PID-0070,?793.16,?23.79,?39.66,?47.59,?19.83,?218.40,?27.30,?31.73,Unit Cost
SLP0071,PID-0071,?768.17,?23.05,?38.41,?46.09,?19.20,?217.20,?27.15,?30.73,Unit Cost
SLP0072,PID-0072,?343.69,?10.31,?17.18,?20.62,?8.59,?127.20,?15.90,?13.75,Unit Cost
SLP0073,PID-0073,?431.07,?12.93,?21.55,?25.86,?10.78,?171.60,?21.45,?17.24,Unit Cost
SLP0074,PID-0074,?332.89,?9.99,?16.64,?19.97,?8.32,?130.80,?16.35,?13.32,Unit Cost
SLP0075,PID-0075,?434.00,?13.02,?21.70,?26.04,?10.85,?163.20,?20.40,?17.36,Unit Cost
SLP0076,PID-0076,?527.03,?15.81,?26.35,?31.62,?13.18,?157.20,?19.65,?21.08,Unit Cost
SLP0077,PID-0077,?481.76,?14.45,?24.09,?28.91,?12.04,?129.60,?16.20,?19.27,Unit Cost
SLP0078,PID-0078,?488.40,?14.65,?24.42,?29.30,?12.21,?135.60,?16.95,?19.54,Unit Cost
SLP0079,PID-0079,?285.83,?8.57,?14.29,?17.15,?7.15,?81.60,?10.20,?11.43,Unit Cost
SLP0080,PID-0080,?501.73,?15.05,?25.09,?30.10,?12.54,?144.00,?18.00,?20.07,Unit Cost
SLP0081,PID-0081,?240.85,?7.23,?12.04,?14.45,?6.02,?87.60,?10.95,?9.63,Unit Cost`;

export const CSV_FINANCE_DATA = `Date,Platform,Orders,Units,Revenue,COGS,Gross_Margin,Marketplace_Fees,Ad_Spend,Operating_Cost,Contribution_Margin,Profit
2026-08-01,Flipkart,22,22,"?21,790.00","?9,749.59","?12,040.41","?2,638.00",?648.09,"?1,307.40","?7,446.92","?7,446.92"
2026-08-01,Instamart,6,5,"?5,350.00","?2,478.32","?2,871.68",?798.78,?0.00,?321.00,"?1,751.90","?1,751.90"
2026-08-01,Myntra,21,19,"?20,050.00","?9,505.37","?10,544.63","?2,733.45","?1,111.27","?1,203.00","?5,496.91","?5,496.91"
2026-08-01,Meesho,16,16,"?16,080.00","?7,230.26","?8,849.74","?2,041.52",?930.28,?964.80,"?4,913.14","?4,913.14"
2026-08-01,MyStore,3,3,"?2,920.00","?1,074.27","?1,845.73",?318.03,?0.00,?175.20,"?1,352.50","?1,352.50"
2026-08-01,Amazon,33,35,"?38,930.00","?17,677.49","?21,252.51","?4,590.51",?679.35,"?2,335.80","?13,646.85","?13,646.85"
2026-08-01,Pepperfry,8,7,"?6,520.00","?2,856.36","?3,663.64",?761.53,?458.64,?391.20,"?2,052.27","?2,052.27"
2026-08-01,Sleepbee,3,3,"?3,160.00","?1,452.62","?1,707.38",?309.65,?0.00,?189.60,"?1,208.13","?1,208.13"
2026-08-01,Blinkit,23,22,"?26,580.00","?12,452.92","?14,127.08","?3,647.31",?612.69,"?1,594.80","?8,272.28","?8,272.28"
2026-08-01,Zoozle,5,5,"?4,430.00","?2,153.00","?2,277.00",?479.67,?0.00,?265.80,"?1,531.53","?1,531.53"
2026-08-01,FirstCry,6,5,"?4,250.00","?2,053.13","?2,196.87",?533.08,?42.08,?255.00,"?1,366.71","?1,366.71"
2026-08-01,Nykaa,7,7,"?7,760.00","?3,601.27","?4,158.73","?1,110.65",?975.78,?465.60,"?1,606.70","?1,606.70"
2026-08-01,JioMart,12,8,"?8,090.00","?3,696.35","?4,393.65",?961.96,?417.35,?485.40,"?2,528.94","?2,528.94"
2026-08-01,Tata 1mg,7,7,"?6,620.00","?3,029.47","?3,590.53","?1,039.37",?545.85,?397.20,"?1,608.11","?1,608.11"
2026-08-02,Amazon,38,39,"?39,910.00","?18,354.37","?21,555.63","?5,358.50",?0.00,"?2,394.60","?13,802.53","?13,802.53"
2026-08-02,Instamart,13,9,"?10,020.00","?4,439.35","?5,580.65","?1,304.91",?602.28,?601.20,"?3,072.26","?3,072.26"
2026-08-02,MyStore,6,5,"?4,580.00","?2,122.35","?2,457.65",?580.52,?0.00,?274.80,"?1,602.33","?1,602.33"
2026-08-02,Flipkart,24,25,"?28,700.00","?13,160.34","?15,539.66","?3,442.97","?1,113.30","?1,722.00","?9,261.39","?9,261.39"
2026-08-02,Blinkit,8,8,"?8,780.00","?4,007.06","?4,772.94",?897.06,?328.97,?526.80,"?3,020.11","?3,020.11"
2026-08-02,Myntra,12,9,"?9,690.00","?4,289.75","?5,400.25","?1,341.97",?456.73,?581.40,"?3,020.15","?3,020.15"
2026-08-02,JioMart,11,11,"?10,240.00","?4,501.60","?5,738.40","?1,454.60","?1,293.07",?614.40,"?2,376.33","?2,376.33"
2026-08-02,Pepperfry,6,6,"?5,760.00","?2,764.75","?2,995.25",?818.36,?642.58,?345.60,"?1,188.71","?1,188.71"
2026-08-02,Meesho,15,14,"?16,400.00","?7,439.78","?8,960.22","?2,087.90","?1,110.92",?984.00,"?4,777.40","?4,777.40"
2026-08-02,Sleepbee,10,8,"?10,420.00","?4,574.30","?5,845.70","?1,338.22",?0.00,?625.20,"?3,882.28","?3,882.28"
2026-08-02,Zoozle,4,4,"?3,560.00","?1,681.75","?1,878.25",?415.88,?0.00,?213.60,"?1,248.77","?1,248.77"
2026-08-02,FirstCry,7,6,"?5,630.00","?2,521.98","?3,108.02",?671.93,"?1,211.11",?337.80,?887.18,?887.18
2026-08-02,Nykaa,14,14,"?19,470.00","?8,453.40","?11,016.60","?2,716.02",?0.00,"?1,168.20","?7,132.38","?7,132.38"
2026-08-02,Tata 1mg,11,9,"?9,420.00","?4,309.30","?5,110.70","?1,385.89",?94.07,?565.20,"?3,065.54","?3,065.54"
2026-08-03,Amazon,34,36,"?36,930.00","?16,429.31","?20,500.69","?4,936.47","?1,546.99","?2,215.80","?11,801.43","?11,801.43"
2026-08-03,Flipkart,26,27,"?26,850.00","?12,165.67","?14,684.33","?3,590.52",?389.13,"?1,611.00","?9,093.68","?9,093.68"
2026-08-03,Instamart,11,10,"?8,070.00","?3,773.65","?4,296.35",?875.81,"?1,146.76",?484.20,"?1,789.58","?1,789.58"
2026-08-03,Myntra,19,15,"?15,500.00","?7,149.15","?8,350.85","?2,177.99",?358.32,?930.00,"?4,884.54","?4,884.54"
2026-08-03,Nykaa,7,5,"?4,000.00","?1,631.69","?2,368.31",?435.81,?0.00,?240.00,"?1,692.50","?1,692.50"
2026-08-03,Meesho,15,12,"?13,250.00","?5,660.36","?7,589.64","?1,698.99",?0.00,?795.00,"?5,095.65","?5,095.65"
2026-08-03,Pepperfry,8,7,"?6,160.00","?2,348.60","?3,811.40",?868.87,?0.00,?369.60,"?2,572.93","?2,572.93"
2026-08-03,Sleepbee,7,5,"?4,060.00","?1,720.63","?2,339.37",?488.07,?0.00,?243.60,"?1,607.70","?1,607.70"
2026-08-03,Tata 1mg,3,2,"?2,710.00","?1,408.34","?1,301.66",?358.44,?0.00,?162.60,?780.62,?780.62
2026-08-03,MyStore,5,4,"?4,420.00","?1,977.47","?2,442.53",?667.28,?0.00,?265.20,"?1,510.05","?1,510.05"
2026-08-03,Blinkit,13,13,"?12,250.00","?5,748.61","?6,501.39","?1,729.62",?268.71,?735.00,"?3,768.06","?3,768.06"
2026-08-03,FirstCry,7,4,"?5,480.00","?2,526.77","?2,953.23",?605.39,?0.00,?328.80,"?2,019.04","?2,019.04"
2026-08-03,JioMart,15,15,"?18,080.00","?7,759.47","?10,320.53","?2,249.35",?141.01,"?1,084.80","?6,845.37","?6,845.37"
2026-08-03,Zoozle,11,9,"?9,560.00","?4,313.52","?5,246.48","?1,012.81",?0.00,?573.60,"?3,660.07","?3,660.07"
2026-08-04,Flipkart,36,37,"?36,620.00","?14,751.63","?21,868.37","?5,119.55","?1,548.93","?2,197.20","?13,002.69","?13,002.69"
2026-08-04,Nykaa,9,8,"?8,390.00","?3,620.56","?4,769.44",?984.03,?0.00,?503.40,"?3,282.01","?3,282.01"
2026-08-04,MyStore,8,8,"?8,610.00","?4,052.41","?4,557.59","?1,122.50",?0.00,?516.60,"?2,918.49","?2,918.49"
2026-08-04,Zoozle,12,10,"?12,080.00","?5,571.79","?6,508.21","?1,258.56",?0.00,?724.80,"?4,524.85","?4,524.85"
2026-08-04,Myntra,11,11,"?11,320.00","?5,228.28","?6,091.72","?1,474.06",?411.77,?679.20,"?3,526.69","?3,526.69"
2026-08-04,Pepperfry,11,9,"?8,510.00","?3,794.31","?4,715.69","?1,164.89","?1,279.68",?510.60,"?1,760.52","?1,760.52"
2026-08-04,Tata 1mg,9,9,"?9,390.00","?4,404.36","?4,985.64","?1,148.09",?290.94,?563.40,"?2,983.21","?2,983.21"
2026-08-04,Amazon,30,30,"?27,360.00","?12,672.26","?14,687.74","?3,717.00","?1,378.26","?1,641.60","?7,950.88","?7,950.88"
2026-08-04,Blinkit,9,9,"?9,180.00","?3,966.85","?5,213.15","?1,127.38",?228.55,?550.80,"?3,306.42","?3,306.42"
2026-08-04,Meesho,12,11,"?13,180.00","?5,575.06","?7,604.94","?1,982.68",?458.98,?790.80,"?4,372.48","?4,372.48"
2026-08-04,JioMart,13,12,"?13,350.00","?5,520.20","?7,829.80","?1,828.34",?0.00,?801.00,"?5,200.46","?5,200.46"
2026-08-04,FirstCry,4,2,?950.00,?484.00,?466.00,?97.60,?0.00,?57.00,?311.40,?311.40
2026-08-04,Sleepbee,8,7,"?8,200.00","?3,894.12","?4,305.88","?1,097.36",?0.00,?492.00,"?2,716.52","?2,716.52"
2026-08-04,Instamart,11,10,"?10,930.00","?5,388.05","?5,541.95","?1,339.46",?559.51,?655.80,"?2,987.18","?2,987.18"
2026-08-05,FirstCry,10,8,"?7,920.00","?3,548.38","?4,371.62","?1,054.78","?1,100.74",?475.20,"?1,740.90","?1,740.90"
2026-08-05,Meesho,9,8,"?7,790.00","?3,474.38","?4,315.62",?915.79,?748.58,?467.40,"?2,183.85","?2,183.85"
2026-08-05,MyStore,9,8,"?9,750.00","?3,954.00","?5,796.00","?1,367.99",?0.00,?585.00,"?3,843.01","?3,843.01"
2026-08-05,Amazon,34,36,"?37,530.00","?16,728.51","?20,801.49","?4,843.53","?1,077.07","?2,251.80","?12,629.09","?12,629.09"
2026-08-05,Flipkart,25,26,"?29,950.00","?13,902.59","?16,047.41","?4,134.32",?721.50,"?1,797.00","?9,394.59","?9,394.59"
2026-08-05,Blinkit,6,5,"?4,010.00","?1,865.73","?2,144.27",?630.80,?0.00,?240.60,"?1,272.87","?1,272.87"
2026-08-05,Sleepbee,10,10,"?11,840.00","?5,054.63","?6,785.37","?1,729.02",?0.00,?710.40,"?4,345.95","?4,345.95"
2026-08-05,Instamart,4,4,"?3,900.00","?1,871.32","?2,028.68",?560.33,?432.35,?234.00,?802.00,?802.00
2026-08-05,Nykaa,9,9,"?10,330.00","?4,827.75","?5,502.25","?1,183.71",?268.02,?619.80,"?3,430.72","?3,430.72"
2026-08-05,JioMart,12,11,"?10,660.00","?4,815.75","?5,844.25","?1,635.34",?30.58,?639.60,"?3,538.73","?3,538.73"
2026-08-05,Myntra,9,9,"?10,130.00","?4,604.82","?5,525.18","?1,487.56",?0.00,?607.80,"?3,429.82","?3,429.82"
2026-08-05,Pepperfry,8,6,"?4,600.00","?2,024.35","?2,575.65",?686.74,?879.63,?276.00,?733.28,?733.28
2026-08-05,Zoozle,5,5,"?5,940.00","?2,734.03","?3,205.97",?597.44,?0.00,?356.40,"?2,252.13","?2,252.13"
2026-08-05,Tata 1mg,4,3,"?1,710.00",?699.89,"?1,010.11",?239.73,?0.00,?102.60,?667.78,?667.78
2026-08-06,Amazon,30,31,"?33,240.00","?13,732.35","?19,507.65","?4,173.00",?62.49,"?1,994.40","?13,277.76","?13,277.76"
2026-08-06,Flipkart,16,18,"?17,980.00","?7,453.81","?10,526.19","?2,692.82",?905.58,"?1,078.80","?5,848.99","?5,848.99"
2026-08-06,Blinkit,12,11,"?12,010.00","?5,481.00","?6,529.00","?1,397.86",?970.64,?720.60,"?3,439.90","?3,439.90"
2026-08-06,Meesho,9,8,"?6,940.00","?2,835.95","?4,104.05",?918.52,?71.75,?416.40,"?2,697.38","?2,697.38"
2026-08-06,Sleepbee,11,10,"?8,270.00","?3,929.84","?4,340.16","?1,108.02",?0.00,?496.20,"?2,735.94","?2,735.94"
2026-08-06,Tata 1mg,14,12,"?13,650.00","?6,146.37","?7,503.63","?1,749.20",?517.30,?819.00,"?4,418.13","?4,418.13"
2026-08-06,Instamart,8,7,"?6,340.00","?2,700.85","?3,639.15",?851.20,?0.00,?380.40,"?2,407.55","?2,407.55"
2026-08-06,JioMart,11,9,"?10,770.00","?4,420.09","?6,349.91","?1,385.82","?2,364.18",?646.20,"?1,953.71","?1,953.71"
2026-08-06,Myntra,16,11,"?15,260.00","?6,860.94","?8,399.06","?2,432.64",?326.09,?915.60,"?4,724.73","?4,724.73"
2026-08-06,FirstCry,6,5,"?4,680.00","?2,032.36","?2,647.64",?608.09,?670.00,?280.80,"?1,088.75","?1,088.75"
2026-08-06,Nykaa,2,1,?700.00,?350.59,?349.41,?99.28,?583.53,?42.00,-?375.40,-?375.40
2026-08-06,Zoozle,7,6,"?6,960.00","?3,242.20","?3,717.80","?1,019.14",?0.00,?417.60,"?2,281.06","?2,281.06"
2026-08-06,MyStore,5,4,"?4,770.00","?2,365.49","?2,404.51",?739.80,?0.00,?286.20,"?1,378.51","?1,378.51"
2026-08-06,Pepperfry,7,7,"?8,420.00","?3,774.03","?4,645.97","?1,138.95",?0.00,?505.20,"?3,001.82","?3,001.82"
2026-08-07,Amazon,36,37,"?36,620.00","?17,063.01","?19,556.99","?4,859.83","?1,431.54","?2,197.20","?11,068.42","?11,068.42"
2026-08-07,Flipkart,16,15,"?15,150.00","?6,670.69","?8,479.31","?1,973.42",?913.78,?909.00,"?4,683.11","?4,683.11"
2026-08-07,Myntra,16,14,"?15,620.00","?7,385.29","?8,234.71","?2,200.37",?639.91,?937.20,"?4,457.23","?4,457.23"
2026-08-07,FirstCry,13,13,"?14,990.00","?6,925.15","?8,064.85","?1,602.13",?783.76,?899.40,"?4,779.56","?4,779.56"
2026-08-07,Meesho,14,11,"?10,470.00","?4,443.91","?6,026.09","?1,302.60",?540.55,?628.20,"?3,554.74","?3,554.74"
2026-08-07,JioMart,14,12,"?13,180.00","?6,041.44","?7,138.56","?1,579.69","?1,016.66",?790.80,"?3,751.41","?3,751.41"
2026-08-07,MyStore,15,14,"?15,980.00","?6,810.77","?9,169.23","?2,385.09",?0.00,?958.80,"?5,825.34","?5,825.34"
2026-08-07,Zoozle,6,5,"?6,040.00","?2,674.69","?3,365.31",?768.73,?0.00,?362.40,"?2,234.18","?2,234.18"
2026-08-07,Blinkit,15,12,"?14,980.00","?6,753.48","?8,226.52","?1,695.89",?0.00,?898.80,"?5,631.83","?5,631.83"
2026-08-07,Nykaa,6,6,"?8,240.00","?3,474.81","?4,765.19","?1,394.35",?116.82,?494.40,"?2,759.62","?2,759.62"
2026-08-07,Tata 1mg,8,6,"?6,920.00","?3,233.15","?3,686.85",?930.49,?0.00,?415.20,"?2,341.16","?2,341.16"
2026-08-07,Sleepbee,11,11,"?12,070.00","?5,233.91","?6,836.09","?1,565.79",?0.00,?724.20,"?4,546.10","?4,546.10"
2026-08-07,Instamart,8,6,"?6,920.00","?3,277.97","?3,642.03",?974.21,?0.00,?415.20,"?2,252.62","?2,252.62"
2026-08-07,Pepperfry,7,6,"?8,780.00","?4,143.18","?4,636.82","?1,170.24",?784.04,?526.80,"?2,155.74","?2,155.74"`;

export const CSV_INVENTORY_DATA = `Date,Warehouse,SKU,Opening_Stock,Closing_Stock,Available_Stock,Reserved_Stock,Inbound_Stock,Damaged_Stock,Days_of_Inventory
2026-08-01,Noida,SLP0001,160,139,118,21,25,1,69.5
2026-08-01,Bengaluru,SLP0001,235,225,199,14,4,2,112.5
2026-08-01,Mumbai,SLP0001,177,176,147,12,18,2,88
2026-08-01,Noida,SLP0002,190,160,146,10,5,0,160
2026-08-01,Bengaluru,SLP0002,134,104,101,2,12,1,104
2026-08-01,Mumbai,SLP0002,94,58,38,21,1,0,58
2026-08-01,Noida,SLP0026,171,132,108,15,20,1,132
2026-08-01,Bengaluru,SLP0026,237,234,228,8,17,0,234
2026-08-01,Mumbai,SLP0026,141,113,85,22,15,0,113
2026-08-01,Noida,SLP0027,238,213,183,25,17,1,106.5
2026-08-01,Bengaluru,SLP0027,88,63,63,8,17,0,31.5
2026-08-01,Mumbai,SLP0027,179,156,135,23,21,1,78
2026-08-01,Noida,SLP0032,161,150,146,12,17,2,150
2026-08-01,Bengaluru,SLP0032,130,98,81,21,25,1,98
2026-08-01,Mumbai,SLP0032,83,58,31,23,1,1,58
2026-08-01,Noida,SLP0033,83,53,26,11,17,0,53
2026-08-01,Bengaluru,SLP0033,255,222,195,3,9,0,222
2026-08-01,Mumbai,SLP0033,245,235,227,14,16,0,235
2026-08-01,Noida,SLP0040,208,204,190,14,21,2,204
2026-08-01,Bengaluru,SLP0040,136,128,100,24,17,2,128
2026-08-01,Mumbai,SLP0040,201,190,166,4,13,2,190
2026-08-01,Noida,SLP0041,120,103,86,9,7,1,103
2026-08-01,Bengaluru,SLP0041,255,237,215,6,22,2,237
2026-08-01,Mumbai,SLP0041,185,165,150,11,17,2,165
2026-08-01,Noida,SLP0046,258,224,211,17,12,0,224
2026-08-01,Bengaluru,SLP0046,132,103,92,4,8,0,103
2026-08-01,Mumbai,SLP0046,232,225,224,25,21,1,225
2026-08-01,Noida,SLP0047,238,198,177,19,15,2,198
2026-08-01,Bengaluru,SLP0047,165,164,164,17,17,1,164
2026-08-01,Mumbai,SLP0047,44,43,27,23,8,2,43
2026-08-01,Noida,SLP0056,173,152,139,20,19,0,152
2026-08-01,Bengaluru,SLP0056,136,116,97,22,6,1,116
2026-08-01,Mumbai,SLP0056,131,120,90,12,10,1,120
2026-08-01,Noida,SLP0057,148,120,101,1,11,0,120
2026-08-01,Bengaluru,SLP0057,172,164,158,12,17,2,164
2026-08-01,Mumbai,SLP0057,238,207,194,21,15,1,207
2026-08-01,Noida,SLP0064,120,103,83,2,7,2,103
2026-08-01,Bengaluru,SLP0064,231,193,170,19,9,2,193
2026-08-01,Mumbai,SLP0064,65,46,40,16,19,2,46
2026-08-01,Noida,SLP0065,130,114,87,10,25,1,114
2026-08-01,Bengaluru,SLP0065,239,219,209,14,8,0,219
2026-08-01,Mumbai,SLP0065,71,59,55,24,24,2,59
2026-08-01,Noida,SLP0068,83,76,49,16,11,0,76
2026-08-01,Bengaluru,SLP0068,160,135,117,3,10,1,135
2026-08-01,Mumbai,SLP0068,130,122,117,23,13,2,122
2026-08-01,Noida,SLP0069,224,218,191,7,4,1,218
2026-08-01,Bengaluru,SLP0069,258,230,206,10,8,2,230
2026-08-01,Mumbai,SLP0069,184,146,126,2,6,1,146
2026-08-01,Noida,SLP0070,174,149,136,15,12,0,149
2026-08-01,Bengaluru,SLP0070,83,49,43,23,11,0,49
2026-08-01,Mumbai,SLP0070,155,122,116,0,21,0,122
2026-08-01,Noida,SLP0071,263,249,222,14,10,2,249
2026-08-01,Bengaluru,SLP0071,275,236,217,15,22,2,236
2026-08-01,Mumbai,SLP0071,161,133,130,3,24,2,133
2026-08-01,Noida,SLP0077,98,87,64,16,3,1,87
2026-08-01,Bengaluru,SLP0077,77,50,42,17,8,0,50
2026-08-01,Mumbai,SLP0077,118,81,54,8,0,1,81
2026-08-01,Noida,SLP0078,146,124,120,21,20,0,124
2026-08-01,Bengaluru,SLP0078,83,65,46,2,6,1,65
2026-08-01,Mumbai,SLP0078,192,164,154,19,21,1,164
2026-08-07,Noida,SLP0001,239,223,207,9,20,0,223
2026-08-07,Bengaluru,SLP0001,154,116,106,23,19,2,116
2026-08-07,Mumbai,SLP0001,221,181,179,20,2,1,181
2026-08-07,Noida,SLP0002,131,107,77,17,10,0,107
2026-08-07,Bengaluru,SLP0002,216,196,172,15,24,2,196
2026-08-07,Mumbai,SLP0002,129,113,106,0,6,1,113
2026-08-07,Noida,SLP0026,236,228,222,2,4,0,228
2026-08-07,Bengaluru,SLP0026,204,195,167,20,0,2,195
2026-08-07,Mumbai,SLP0026,157,118,116,1,12,2,118
2026-08-07,Noida,SLP0027,144,141,121,4,23,0,70.5
2026-08-07,Bengaluru,SLP0027,82,69,64,3,21,2,34.5
2026-08-07,Mumbai,SLP0027,183,157,143,24,21,0,78.5
2026-08-07,Noida,SLP0032,266,248,237,16,8,1,248
2026-08-07,Bengaluru,SLP0032,128,116,91,12,5,0,116
2026-08-07,Mumbai,SLP0032,232,220,220,0,18,1,220
2026-08-07,Noida,SLP0033,286,249,241,25,5,2,249
2026-08-07,Bengaluru,SLP0033,238,211,194,16,4,1,211
2026-08-07,Mumbai,SLP0033,250,225,207,21,15,2,225
2026-08-07,Noida,SLP0040,219,217,206,3,2,1,217
2026-08-07,Bengaluru,SLP0040,87,60,39,23,1,0,60
2026-08-07,Mumbai,SLP0040,226,192,168,24,17,1,192
2026-08-07,Noida,SLP0041,79,72,51,17,22,0,72
2026-08-07,Bengaluru,SLP0041,188,168,140,8,11,1,168
2026-08-07,Mumbai,SLP0041,54,52,31,13,8,1,52
2026-08-07,Noida,SLP0046,248,242,241,0,6,2,121
2026-08-07,Bengaluru,SLP0046,238,237,223,24,12,0,118.5
2026-08-07,Mumbai,SLP0046,63,40,14,8,10,2,20
2026-08-07,Noida,SLP0047,82,58,28,17,25,1,58
2026-08-07,Bengaluru,SLP0047,71,41,39,1,25,1,41
2026-08-07,Mumbai,SLP0047,186,183,181,3,18,1,183
2026-08-07,Noida,SLP0056,57,52,42,3,10,0,52
2026-08-07,Bengaluru,SLP0056,235,224,195,11,25,2,224
2026-08-07,Mumbai,SLP0056,252,215,207,14,20,2,215
2026-08-07,Noida,SLP0057,89,83,63,25,19,2,83
2026-08-07,Bengaluru,SLP0057,219,209,207,11,16,0,209
2026-08-07,Mumbai,SLP0057,209,173,144,15,23,0,173
2026-08-07,Noida,SLP0064,175,150,144,21,9,2,150
2026-08-07,Bengaluru,SLP0064,249,237,215,7,18,1,237
2026-08-07,Mumbai,SLP0064,128,128,119,20,19,1,128
2026-08-07,Noida,SLP0065,123,106,79,21,20,2,106
2026-08-07,Bengaluru,SLP0065,170,167,164,15,6,2,167
2026-08-07,Mumbai,SLP0065,82,81,59,16,13,1,81
2026-08-07,Noida,SLP0068,72,41,20,10,7,2,13.7
2026-08-07,Bengaluru,SLP0068,125,118,98,17,10,0,39.3
2026-08-07,Mumbai,SLP0068,47,43,36,24,12,0,14.3
2026-08-07,Noida,SLP0069,133,97,69,8,13,1,97
2026-08-07,Bengaluru,SLP0069,77,44,20,21,21,2,44
2026-08-07,Mumbai,SLP0069,193,183,179,7,1,2,183
2026-08-07,Noida,SLP0070,173,169,164,4,10,2,169
2026-08-07,Bengaluru,SLP0070,87,50,25,22,10,1,50
2026-08-07,Mumbai,SLP0070,174,140,131,22,8,2,140
2026-08-07,Noida,SLP0071,75,64,39,2,11,2,32
2026-08-07,Bengaluru,SLP0071,147,115,94,3,22,1,57.5
2026-08-07,Mumbai,SLP0071,186,177,150,13,17,1,88.5
2026-08-07,Noida,SLP0077,226,188,188,14,8,2,188
2026-08-07,Bengaluru,SLP0077,170,161,137,19,13,1,161
2026-08-07,Mumbai,SLP0077,210,191,189,24,14,2,191
2026-08-07,Noida,SLP0078,92,87,58,2,22,1,43.5
2026-08-07,Bengaluru,SLP0078,140,100,96,20,14,1,50
2026-08-07,Mumbai,SLP0078,107,80,56,8,17,2,40`;

export function getParsedCostRows() {
  return parseCsv(CSV_COST_DATA).map(r => ({
    sku: r.SKU,
    productId: r.Product_ID,
    cogs: r.COGS,
    manufacturingCost: r.Manufacturing_Cost,
    packagingCost: r.Packaging_Cost,
    freightCost: r.Freight_Cost,
    warehouseCost: r.Warehouse_Cost,
    marketplaceFeeBenchmark: r.Marketplace_Fee_Benchmark,
    paymentFeesBenchmark: r.Payment_Fees_Benchmark,
    returnsCostBenchmark: r.Returns_Cost_Benchmark,
  }));
}

export function getParsedFinanceRows() {
  return parseCsv(CSV_FINANCE_DATA).map(r => ({
    date: r.Date,
    platform: r.Platform,
    orders: r.Orders,
    units: r.Units,
    revenue: r.Revenue,
    cogs: r.COGS,
    grossMargin: r.Gross_Margin,
    marketplaceFees: r.Marketplace_Fees,
    adSpend: r.Ad_Spend,
    operatingCost: r.Operating_Cost,
    contributionMargin: r.Contribution_Margin,
    profit: r.Profit,
  }));
}

export function getParsedInventoryRows() {
  return parseCsv(CSV_INVENTORY_DATA).map(r => ({
    date: r.Date,
    warehouse: r.Warehouse,
    sku: r.SKU,
    openingStock: r.Opening_Stock,
    closingStock: r.Closing_Stock,
    availableStock: r.Available_Stock,
    reservedStock: r.Reserved_Stock,
    inboundStock: r.Inbound_Stock,
    damagedStock: r.Damaged_Stock,
    daysOfInventory: r.Days_of_Inventory,
  }));
}
