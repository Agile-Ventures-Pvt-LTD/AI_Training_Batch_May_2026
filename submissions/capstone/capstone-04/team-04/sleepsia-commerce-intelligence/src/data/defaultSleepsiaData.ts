/**
 * Sleepsia Commerce Intelligence Platform - Unified Prototype Dataset
 * Extracted and normalized from Sleepsia_Commerce_Intelligence_Prototype_Data_v2_with_Shipping.xlsx
 */

import {
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
  SleepsiaWorkbookData,
} from '../types/commerce';

import {
  CSV_PRODUCT_MASTER,
  getParsedCostRows,
  getParsedFinanceRows,
  getParsedInventoryRows,
} from './rawSleepsiaDatasetRows';

import {
  getParsedCompetitorRows,
  getParsedCustomerRows,
} from './rawSleepsiaSalesRows';

import {
  generateRawSalesAndMarketplace,
} from './rawSleepsiaAdSalesRows';

import {
  getParsedShippingRows,
} from './rawSleepsiaShippingRows';

// 1. PRODUCT MASTER (All 81 SKUs)
export const SLEEPSIA_PRODUCTS: ProductMaster[] = [
  { sku: 'SLP0001', productId: 'PID-0001', productName: 'Memory Foam Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'Black', eanGtin: '890610000001', productLifecycle: 'Active', mrp: 1000, standardCost: 336.73 },
  { sku: 'SLP0002', productId: 'PID-0002', productName: 'Memory Foam Pillow with Cooling Gel', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'Beige', eanGtin: '890610000002', productLifecycle: 'Active', mrp: 710, standardCost: 222.26 },
  { sku: 'SLP0003', productId: 'PID-0003', productName: 'Memory Foam Pillow with Ventilated Cooling Gel', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Grey', eanGtin: '890610000003', productLifecycle: 'Active', mrp: 880, standardCost: 294.71 },
  { sku: 'SLP0004', productId: 'PID-0004', productName: 'Small Memory Foam Pillow with Cooling Gel', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Microfiber', colour: 'Beige', eanGtin: '890610000004', productLifecycle: 'Active', mrp: 980, standardCost: 355.67 },
  { sku: 'SLP0005', productId: 'PID-0005', productName: 'Ventilated Memory Foam Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Grey', eanGtin: '890610000005', productLifecycle: 'Active', mrp: 890, standardCost: 360.20 },
  { sku: 'SLP0006', productId: 'PID-0006', productName: 'Bamboo Memory Foam Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Black', eanGtin: '890610000006', productLifecycle: 'Active', mrp: 830, standardCost: 261.73 },
  { sku: 'SLP0007', productId: 'PID-0007', productName: 'Shredded Memory Foam Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Cotton', colour: 'Beige', eanGtin: '890610000007', productLifecycle: 'Active', mrp: 850, standardCost: 288.73 },
  { sku: 'SLP0008', productId: 'PID-0008', productName: 'Adjustable Shredded Memory Foam Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Satin', colour: 'White', eanGtin: '890610000008', productLifecycle: 'Active', mrp: 660, standardCost: 294.34 },
  { sku: 'SLP0009', productId: 'PID-0009', productName: 'Bamboo Adjustable Memory Foam Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Cotton', colour: 'Beige', eanGtin: '890610000009', productLifecycle: 'Active', mrp: 850, standardCost: 367.90 },
  { sku: 'SLP0010', productId: 'PID-0010', productName: 'Premium Bamboo Memory Foam Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'White', eanGtin: '890610000010', productLifecycle: 'Active', mrp: 840, standardCost: 257.77 },
  { sku: 'SLP0011', productId: 'PID-0011', productName: 'Orthopedic Cervical Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Grey', eanGtin: '890610000011', productLifecycle: 'Active', mrp: 760, standardCost: 326.78 },
  { sku: 'SLP0012', productId: 'PID-0012', productName: 'Orthopedic Cervical Pillow with Cooling Gel', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'Black', eanGtin: '890610000012', productLifecycle: 'Active', mrp: 850, standardCost: 275.74 },
  { sku: 'SLP0013', productId: 'PID-0013', productName: 'Contour Orthopedic Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Cotton', colour: 'White', eanGtin: '890610000013', productLifecycle: 'Active', mrp: 840, standardCost: 328.75 },
  { sku: 'SLP0014', productId: 'PID-0014', productName: 'Contour Orthopedic Pillow with Ventilated Cooling Gel', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Microfiber', colour: 'Grey', eanGtin: '890610000014', productLifecycle: 'Active', mrp: 730, standardCost: 269.62 },
  { sku: 'SLP0015', productId: 'PID-0015', productName: 'Butterfly Pillow for Neck Pain', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Polyester', colour: 'Beige', eanGtin: '890610000015', productLifecycle: 'Active', mrp: 790, standardCost: 263.02 },
  { sku: 'SLP0016', productId: 'PID-0016', productName: 'Neck Pain Relief Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'White', eanGtin: '890610000016', productLifecycle: 'Active', mrp: 820, standardCost: 345.02 },
  { sku: 'SLP0017', productId: 'PID-0017', productName: 'Cervical Support Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Beige', eanGtin: '890610000017', productLifecycle: 'Active', mrp: 860, standardCost: 371.05 },
  { sku: 'SLP0018', productId: 'PID-0018', productName: 'Microfiber Sleeping Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Bamboo', colour: 'Blue', eanGtin: '890610000018', productLifecycle: 'Active', mrp: 810, standardCost: 350.49 },
  { sku: 'SLP0019', productId: 'PID-0019', productName: 'Hotel Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Cotton', colour: 'Grey', eanGtin: '890610000019', productLifecycle: 'Active', mrp: 1010, standardCost: 340.36 },
  { sku: 'SLP0020', productId: 'PID-0020', productName: 'Premium Microfiber Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'Beige', eanGtin: '890610000020', productLifecycle: 'Active', mrp: 960, standardCost: 349.69 },
  { sku: 'SLP0021', productId: 'PID-0021', productName: 'Ultra Soft Down Alternative Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Grey', eanGtin: '890610000021', productLifecycle: 'Active', mrp: 970, standardCost: 365.14 },
  { sku: 'SLP0022', productId: 'PID-0022', productName: 'Luxury Microfiber Pillow', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Grey', eanGtin: '890610000022', productLifecycle: 'Active', mrp: 680, standardCost: 268.00 },
  { sku: 'SLP0023', productId: 'PID-0023', productName: 'Cloud Pillow - Red', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Satin', colour: 'White', eanGtin: '890610000023', productLifecycle: 'Active', mrp: 1090, standardCost: 389.91 },
  { sku: 'SLP0024', productId: 'PID-0024', productName: 'Cloud Pillow - Green', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Satin', colour: 'Black', eanGtin: '890610000024', productLifecycle: 'Active', mrp: 980, standardCost: 436.75 },
  { sku: 'SLP0025', productId: 'PID-0025', productName: 'Family Pillows', category: 'Sleeping Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'White', eanGtin: '890610000025', productLifecycle: 'Active', mrp: 1130, standardCost: 454.55 },
  { sku: 'SLP0026', productId: 'PID-0026', productName: 'Full Body Long Cuddle Pillow', category: 'Pregnancy & Body Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'Black', eanGtin: '890610000026', productLifecycle: 'Active', mrp: 1470, standardCost: 465.60 },
  { sku: 'SLP0027', productId: 'PID-0027', productName: 'Full Body Pillow', category: 'Pregnancy & Body Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Black', eanGtin: '890610000027', productLifecycle: 'Active', mrp: 1380, standardCost: 615.18 },
  { sku: 'SLP0028', productId: 'PID-0028', productName: 'C-Shape Pregnancy Pillow', category: 'Pregnancy & Body Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Memory Foam', colour: 'Black', eanGtin: '890610000028', productLifecycle: 'Active', mrp: 1670, standardCost: 711.84 },
  { sku: 'SLP0029', productId: 'PID-0029', productName: 'J-Shape Pregnancy Pillow', category: 'Pregnancy & Body Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Black', eanGtin: '890610000029', productLifecycle: 'Active', mrp: 1440, standardCost: 596.70 },
  { sku: 'SLP0030', productId: 'PID-0030', productName: 'U-Shape Pregnancy Pillow', category: 'Pregnancy & Body Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Memory Foam', colour: 'Beige', eanGtin: '890610000030', productLifecycle: 'Active', mrp: 1470, standardCost: 512.48 },
  { sku: 'SLP0031', productId: 'PID-0031', productName: 'Full Body Shredded Memory Foam Pillow', category: 'Pregnancy & Body Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Cotton', colour: 'Grey', eanGtin: '890610000031', productLifecycle: 'Active', mrp: 1000, standardCost: 308.69 },
  { sku: 'SLP0032', productId: 'PID-0032', productName: 'Kids Bamboo Pillow', category: 'Kids & Baby Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Blue', eanGtin: '890610000032', productLifecycle: 'Active', mrp: 830, standardCost: 350.59 },
  { sku: 'SLP0033', productId: 'PID-0033', productName: 'Kids Microfiber Pillow', category: 'Kids & Baby Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Microfiber', colour: 'Grey', eanGtin: '890610000033', productLifecycle: 'Active', mrp: 870, standardCost: 347.10 },
  { sku: 'SLP0034', productId: 'PID-0034', productName: 'Kids Cat Shape Memory Foam Pillow', category: 'Kids & Baby Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Cotton', colour: 'Beige', eanGtin: '890610000034', productLifecycle: 'Active', mrp: 860, standardCost: 370.54 },
  { sku: 'SLP0035', productId: 'PID-0035', productName: 'Kids Butterfly Shape Memory Foam Pillow', category: 'Kids & Baby Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Satin', colour: 'Grey', eanGtin: '890610000035', productLifecycle: 'Active', mrp: 630, standardCost: 256.37 },
  { sku: 'SLP0036', productId: 'PID-0036', productName: 'Kids Alpha Pillow', category: 'Kids & Baby Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Polyester', colour: 'Black', eanGtin: '890610000036', productLifecycle: 'Active', mrp: 620, standardCost: 226.74 },
  { sku: 'SLP0037', productId: 'PID-0037', productName: 'Baby Pillow', category: 'Kids & Baby Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Grey', eanGtin: '890610000037', productLifecycle: 'Active', mrp: 670, standardCost: 207.43 },
  { sku: 'SLP0038', productId: 'PID-0038', productName: 'Baby Feeding Pillow', category: 'Kids & Baby Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Microfiber', colour: 'Beige', eanGtin: '890610000038', productLifecycle: 'Active', mrp: 460, standardCost: 153.19 },
  { sku: 'SLP0039', productId: 'PID-0039', productName: 'Microfiber Baby Pillow', category: 'Kids & Baby Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Memory Foam', colour: 'Grey', eanGtin: '890610000039', productLifecycle: 'Active', mrp: 480, standardCost: 148.85 },
  { sku: 'SLP0040', productId: 'PID-0040', productName: 'Memory Foam Travel Neck Pillow', category: 'Travel & Car Comfort', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Beige', eanGtin: '890610000040', productLifecycle: 'Active', mrp: 500, standardCost: 167.85 },
  { sku: 'SLP0041', productId: 'PID-0041', productName: 'Snoozed Travel Neck Pillow', category: 'Travel & Car Comfort', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Satin', colour: 'Grey', eanGtin: '890610000041', productLifecycle: 'Active', mrp: 790, standardCost: 322.72 },
  { sku: 'SLP0042', productId: 'PID-0042', productName: 'Velvet Travel Neck Pillow', category: 'Travel & Car Comfort', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Bamboo', colour: 'Grey', eanGtin: '890610000042', productLifecycle: 'Active', mrp: 890, standardCost: 371.75 },
  { sku: 'SLP0043', productId: 'PID-0043', productName: 'Car Neck Rest Memory Foam Pillow', category: 'Travel & Car Comfort', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'White', eanGtin: '890610000043', productLifecycle: 'Active', mrp: 860, standardCost: 343.01 },
  { sku: 'SLP0044', productId: 'PID-0044', productName: 'Car Head Rest Pillow', category: 'Travel & Car Comfort', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Bamboo', colour: 'White', eanGtin: '890610000044', productLifecycle: 'Active', mrp: 650, standardCost: 260.65 },
  { sku: 'SLP0045', productId: 'PID-0045', productName: 'Ergonomic Semi Roll Pillow', category: 'Travel & Car Comfort', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Blue', eanGtin: '890610000045', productLifecycle: 'Active', mrp: 940, standardCost: 384.68 },
  { sku: 'SLP0046', productId: 'PID-0046', productName: 'Wedge Pillow', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Grey', eanGtin: '890610000046', productLifecycle: 'Active', mrp: 1220, standardCost: 400.81 },
  { sku: 'SLP0047', productId: 'PID-0047', productName: 'Lumbar Support Pillow', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Black', eanGtin: '890610000047', productLifecycle: 'Active', mrp: 990, standardCost: 365.70 },
  { sku: 'SLP0048', productId: 'PID-0048', productName: 'Lumbar Support Pillow with Cooling Gel', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Bamboo', colour: 'Beige', eanGtin: '890610000048', productLifecycle: 'Active', mrp: 1270, standardCost: 399.65 },
  { sku: 'SLP0049', productId: 'PID-0049', productName: 'Lumbar Support Pillow with Ventilated Cooling Gel', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Memory Foam', colour: 'White', eanGtin: '890610000049', productLifecycle: 'Active', mrp: 1120, standardCost: 491.63 },
  { sku: 'SLP0050', productId: 'PID-0050', productName: 'Half Lumbar Support Pillow', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Bamboo', colour: 'Blue', eanGtin: '890610000050', productLifecycle: 'Active', mrp: 1250, standardCost: 465.25 },
  { sku: 'SLP0051', productId: 'PID-0051', productName: 'Backrest Cushion', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Blue', eanGtin: '890610000051', productLifecycle: 'Active', mrp: 1260, standardCost: 378.41 },
  { sku: 'SLP0052', productId: 'PID-0052', productName: 'Coccyx Seat Cushion', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Cotton', colour: 'Blue', eanGtin: '890610000052', productLifecycle: 'Active', mrp: 950, standardCost: 384.26 },
  { sku: 'SLP0053', productId: 'PID-0053', productName: 'U-Shaped Coccyx Cushion', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Polyester', colour: 'Blue', eanGtin: '890610000053', productLifecycle: 'Active', mrp: 1170, standardCost: 378.17 },
  { sku: 'SLP0054', productId: 'PID-0054', productName: 'Donut Seat Cushion with Cooling Gel', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Satin', colour: 'Beige', eanGtin: '890610000054', productLifecycle: 'Active', mrp: 890, standardCost: 275.14 },
  { sku: 'SLP0055', productId: 'PID-0055', productName: 'Orthopedic Seat Cushion', category: 'Back Support & Seat Cushions', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Satin', colour: 'Blue', eanGtin: '890610000055', productLifecycle: 'Active', mrp: 900, standardCost: 337.88 },
  { sku: 'SLP0056', productId: 'PID-0056', productName: 'Pillow Protectors', category: 'Pillow Covers & Protectors', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Beige', eanGtin: '890610000056', productLifecycle: 'Active', mrp: 560, standardCost: 174.73 },
  { sku: 'SLP0057', productId: 'PID-0057', productName: 'Pillow Covers', category: 'Pillow Covers & Protectors', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Memory Foam', colour: 'Grey', eanGtin: '890610000057', productLifecycle: 'Active', mrp: 370, standardCost: 133.41 },
  { sku: 'SLP0058', productId: 'PID-0058', productName: 'Pillow Cases', category: 'Pillow Covers & Protectors', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Microfiber', colour: 'Beige', eanGtin: '890610000058', productLifecycle: 'Active', mrp: 590, standardCost: 229.61 },
  { sku: 'SLP0059', productId: 'PID-0059', productName: 'Satin Pillow Cover - Rose Taupe', category: 'Pillow Covers & Protectors', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'Beige', eanGtin: '890610000059', productLifecycle: 'Active', mrp: 500, standardCost: 192.39 },
  { sku: 'SLP0060', productId: 'PID-0060', productName: 'Satin Pillow Cover - Silver', category: 'Pillow Covers & Protectors', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Black', eanGtin: '890610000060', productLifecycle: 'Active', mrp: 410, standardCost: 137.68 },
  { sku: 'SLP0061', productId: 'PID-0061', productName: 'Satin Pillow Cover - Brown', category: 'Pillow Covers & Protectors', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Polyester', colour: 'Black', eanGtin: '890610000061', productLifecycle: 'Active', mrp: 430, standardCost: 158.49 },
  { sku: 'SLP0062', productId: 'PID-0062', productName: 'Satin Pillow Cover - Beige', category: 'Pillow Covers & Protectors', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Blue', eanGtin: '890610000062', productLifecycle: 'Active', mrp: 590, standardCost: 231.97 },
  { sku: 'SLP0063', productId: 'PID-0063', productName: 'Satin Pillow Cover - Black', category: 'Pillow Covers & Protectors', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Beige', eanGtin: '890610000063', productLifecycle: 'Active', mrp: 480, standardCost: 159.35 },
  { sku: 'SLP0064', productId: 'PID-0064', productName: 'King Size Bedsheets', category: 'Bedding Products', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Memory Foam', colour: 'Grey', eanGtin: '890610000064', productLifecycle: 'Active', mrp: 1090, standardCost: 387.42 },
  { sku: 'SLP0065', productId: 'PID-0065', productName: 'Queen Size Bedsheets', category: 'Bedding Products', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Polyester', colour: 'Black', eanGtin: '890610000065', productLifecycle: 'Active', mrp: 1000, standardCost: 391.75 },
  { sku: 'SLP0066', productId: 'PID-0066', productName: 'Satin Bedsheets', category: 'Bedding Products', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Satin', colour: 'White', eanGtin: '890610000066', productLifecycle: 'Active', mrp: 1680, standardCost: 672.30 },
  { sku: 'SLP0067', productId: 'PID-0067', productName: 'Bedsheet + Pillow Combo', category: 'Bedding Products', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Memory Foam', colour: 'Grey', eanGtin: '890610000067', productLifecycle: 'Active', mrp: 1330, standardCost: 451.76 },
  { sku: 'SLP0068', productId: 'PID-0068', productName: 'Dog Beds', category: 'Pet Products', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Satin', colour: 'Grey', eanGtin: '890610000068', productLifecycle: 'Active', mrp: 1850, standardCost: 630.58 },
  { sku: 'SLP0069', productId: 'PID-0069', productName: 'Pet Beds', category: 'Pet Products', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Cotton', colour: 'Grey', eanGtin: '890610000069', productLifecycle: 'Active', mrp: 1590, standardCost: 640.97 },
  { sku: 'SLP0070', productId: 'PID-0070', productName: 'Electric Aroma Diffuser 200ml', category: 'Wellness & Home', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Bamboo', colour: 'Black', eanGtin: '890610000070', productLifecycle: 'Active', mrp: 1820, standardCost: 793.16 },
  { sku: 'SLP0071', productId: 'PID-0071', productName: 'Electric Aroma Diffuser 300ml', category: 'Wellness & Home', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Polyester', colour: 'Blue', eanGtin: '890610000071', productLifecycle: 'Active', mrp: 1810, standardCost: 768.17 },
  { sku: 'SLP0072', productId: 'PID-0072', productName: 'Electric Aroma Diffuser 400ml', category: 'Wellness & Home', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Black', eanGtin: '890610000072', productLifecycle: 'Active', mrp: 1060, standardCost: 343.69 },
  { sku: 'SLP0073', productId: 'PID-0073', productName: 'Electric Glass Aroma Diffuser', category: 'Wellness & Home', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Bamboo', colour: 'Beige', eanGtin: '890610000073', productLifecycle: 'Active', mrp: 1430, standardCost: 431.07 },
  { sku: 'SLP0074', productId: 'PID-0074', productName: 'Electric Plastic Aroma Diffuser', category: 'Wellness & Home', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Microfiber', colour: 'Beige', eanGtin: '890610000074', productLifecycle: 'Active', mrp: 1090, standardCost: 332.89 },
  { sku: 'SLP0075', productId: 'PID-0075', productName: 'Ultrasonic Room Humidifier', category: 'Wellness & Home', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Microfiber', colour: 'Blue', eanGtin: '890610000075', productLifecycle: 'Active', mrp: 1360, standardCost: 434.00 },
  { sku: 'SLP0076', productId: 'PID-0076', productName: 'Humidifier 4L', category: 'Wellness & Home', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Cotton', colour: 'Grey', eanGtin: '890610000076', productLifecycle: 'Active', mrp: 1310, standardCost: 527.03 },
  { sku: 'SLP0077', productId: 'PID-0077', productName: 'Heart-Shaped Pillow', category: 'Speciality Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Satin', colour: 'Blue', eanGtin: '890610000077', productLifecycle: 'Active', mrp: 1080, standardCost: 481.76 },
  { sku: 'SLP0078', productId: 'PID-0078', productName: 'Bamboo Pillow', category: 'Speciality Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Microfiber', colour: 'Grey', eanGtin: '890610000078', productLifecycle: 'Active', mrp: 1130, standardCost: 488.40 },
  { sku: 'SLP0079', productId: 'PID-0079', productName: 'Cooling Gel Pillow', category: 'Speciality Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Medium', material: 'Cotton', colour: 'Blue', eanGtin: '890610000079', productLifecycle: 'Active', mrp: 680, standardCost: 285.83 },
  { sku: 'SLP0080', productId: 'PID-0080', productName: 'Orthopedic Memory Foam Pillow', category: 'Speciality Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Cotton', colour: 'Grey', eanGtin: '890610000080', productLifecycle: 'Active', mrp: 1200, standardCost: 501.73 },
  { sku: 'SLP0081', productId: 'PID-0081', productName: 'Pain Relief Pillow', category: 'Speciality Pillows', brand: 'Sleepsia', variant: 'Standard', size: 'Standard', material: 'Bamboo', colour: 'Grey', eanGtin: '890610000081', productLifecycle: 'Active', mrp: 730, standardCost: 240.85 },
];

// 2. MARKETPLACE MASTER (14 Channels)
export const SLEEPSIA_MARKETPLACES: MarketplaceMaster[] = [
  { platform: 'Amazon', platformType: 'General E-Commerce', commissionRate: 0.16, settlementDays: 7, returnWindowDays: 10, activeStatus: true },
  { platform: 'Flipkart', platformType: 'General E-Commerce', commissionRate: 0.15, settlementDays: 10, returnWindowDays: 10, activeStatus: true },
  { platform: 'Blinkit', platformType: 'Quick Commerce', commissionRate: 0.22, settlementDays: 3, returnWindowDays: 2, activeStatus: true },
  { platform: 'Instamart', platformType: 'Quick Commerce', commissionRate: 0.21, settlementDays: 3, returnWindowDays: 2, activeStatus: true },
  { platform: 'Myntra', platformType: 'Vertical / Niche', commissionRate: 0.18, settlementDays: 14, returnWindowDays: 14, activeStatus: true },
  { platform: 'FirstCry', platformType: 'Vertical / Niche', commissionRate: 0.17, settlementDays: 14, returnWindowDays: 7, activeStatus: true },
  { platform: 'Nykaa', platformType: 'Vertical / Niche', commissionRate: 0.19, settlementDays: 14, returnWindowDays: 7, activeStatus: true },
  { platform: 'Meesho', platformType: 'General E-Commerce', commissionRate: 0.05, settlementDays: 7, returnWindowDays: 7, activeStatus: true },
  { platform: 'JioMart', platformType: 'General E-Commerce', commissionRate: 0.12, settlementDays: 10, returnWindowDays: 7, activeStatus: true },
  { platform: 'Pepperfry', platformType: 'Vertical / Niche', commissionRate: 0.20, settlementDays: 15, returnWindowDays: 10, activeStatus: true },
  { platform: 'Sleepbee', platformType: 'Vertical / Niche', commissionRate: 0.14, settlementDays: 7, returnWindowDays: 15, activeStatus: true },
  { platform: 'Tata 1mg', platformType: 'Vertical / Niche', commissionRate: 0.15, settlementDays: 10, returnWindowDays: 7, activeStatus: true },
  { platform: 'MyStore', platformType: 'Government / ONDC', commissionRate: 0.04, settlementDays: 5, returnWindowDays: 7, activeStatus: true },
  { platform: 'Zoozle', platformType: 'General E-Commerce', commissionRate: 0.08, settlementDays: 7, returnWindowDays: 7, activeStatus: true },
];

export const PROTOTYPE_DATES = [
  '2026-08-01',
  '2026-08-02',
  '2026-08-03',
  '2026-08-04',
  '2026-08-05',
  '2026-08-06',
  '2026-08-07',
];

function cleanNum(val: any): number {
  if (typeof val === 'number') return isNaN(val) ? 0 : val;
  if (!val) return 0;
  const str = String(val).replace(/[₹,$,%,? ]/g, '').trim();
  const n = parseFloat(str);
  return isNaN(n) ? 0 : n;
}

export function generateDefaultDataset(): SleepsiaWorkbookData {
  const productMap = new Map(SLEEPSIA_PRODUCTS.map((p) => [p.sku, p]));
  const { sales: rawSales, marketplace: rawMarketplace, advertising: rawAds } = generateRawSalesAndMarketplace();

  // 1. Sales Records
  const sales: InternalSalesRecord[] = rawSales.map((r, idx) => {
    const prod = productMap.get(r.sku);
    return {
      orderId: r.orderId,
      date: r.date,
      channel: r.channel as any,
      sku: r.sku,
      productName: prod ? prod.productName : r.sku,
      units: r.units,
      grossSales: r.grossSales,
      discounts: r.discounts,
      netSales: r.grossSales - r.discounts,
      returns: r.returns,
      cancellations: r.cancellations,
      netRealizedRevenue: r.netRealizedRevenue,
      customerId: `CUST${String((idx % 20) + 1).padStart(5, '0')}`,
      state: ['Delhi NCR', 'Maharashtra', 'Karnataka', 'Telangana', 'Tamil Nadu', 'West Bengal', 'Gujarat'][idx % 7],
    };
  });

  // 2. Marketplace Records
  const marketplaceData: MarketplaceRecord[] = rawMarketplace.map((r) => ({
    platform: r.platform as any,
    date: r.date,
    sku: r.sku,
    marketplaceProductId: r.marketplaceProductId,
    price: r.price,
    mrp: r.mrp,
    discount: r.discount,
    availability: r.availability as any,
    inventory: r.inventory,
    orders: r.orders,
    unitsSold: r.unitsSold,
    gmv: r.gmv,
    returns: r.returns,
    cancellations: r.cancellations,
    marketplaceFees: r.marketplaceFees,
    settlement: r.settlement,
    rating: r.rating,
    reviewCount: r.reviewCount,
    productContentScore: r.productContentScore,
    organicSearchPosition: r.organicSearchPosition,
    sponsoredSearchPosition: r.sponsoredSearchPosition,
    categoryPosition: r.categoryPosition,
    promotion: r.promotion,
  }));

  // 3. Advertising Records
  const advertising: AdvertisingRecord[] = rawAds.map((r) => ({
    date: r.date,
    platform: r.platform as any,
    campaignId: r.campaignId,
    campaignName: r.campaignName,
    campaignType: r.campaignType as any,
    status: r.status as any,
    sku: r.sku,
    productId: r.productId,
    impressions: r.impressions,
    clicks: r.clicks,
    spend: r.spend,
    orders: r.orders,
    units: r.units,
    attributedRevenue: r.attributedRevenue,
    ctr: r.ctr,
    cpc: r.cpc,
    roas: r.roas,
    acos: r.acos,
  }));

  // 4. Inventory Records (Expanded from 120 Mother Warehouse records to 600 Darkstore records across 15 Darkstores)
  const darkstorePrefixMap: Record<string, string> = {
    'Noida': 'NOI',
    'Bengaluru': 'BLR',
    'Mumbai': 'MUM',
  };
  const darkstoreAllocations = [
    { id: '01', pct: 0.14, doiFactor: 0.8 },
    { id: '02', pct: 0.17, doiFactor: 0.9 },
    { id: '03', pct: 0.20, doiFactor: 1.0 },
    { id: '04', pct: 0.23, doiFactor: 1.1 },
    { id: '05', pct: 0.26, doiFactor: 1.2 },
  ];

  const inventory: InventoryRecord[] = [];
  getParsedInventoryRows().forEach((r) => {
    const motherWh = r.warehouse || 'Noida';
    const prefix = darkstorePrefixMap[motherWh] || 'NOI';
    const baseOpening = cleanNum(r.openingStock);
    const baseClosing = cleanNum(r.closingStock);
    const baseAvailable = cleanNum(r.availableStock);
    const baseReserved = cleanNum(r.reservedStock);
    const baseInbound = cleanNum(r.inboundStock);
    const baseDamaged = cleanNum(r.damagedStock);
    const baseDoi = cleanNum(r.daysOfInventory);

    darkstoreAllocations.forEach((ds) => {
      const darkstoreId = `${prefix}-DS-${ds.id}`;
      const openStock = Math.round(baseOpening * ds.pct);
      const closeStock = Math.round(baseClosing * ds.pct);
      const availStock = Math.round(baseAvailable * ds.pct);
      const resStock = Math.round(baseReserved * ds.pct);
      const inStock = Math.round(baseInbound * ds.pct);
      const damStock = Math.round(baseDamaged * ds.pct);
      const doi = Number((baseDoi * ds.doiFactor * 0.2).toFixed(1)); // darkstore local DOI ~18 days avg
      const risk: 'Low' | 'Medium' | 'High' | 'Critical' = 
        doi <= 7 ? 'Critical' : doi <= 14 ? 'High' : doi <= 45 ? 'Medium' : 'Low';

      inventory.push({
        date: r.date,
        motherWarehouse: motherWh,
        warehouse: motherWh,
        darkstore: darkstoreId,
        darkstoreId,
        sku: r.sku,
        openingStock: openStock,
        closingStock: closeStock,
        availableStock: availStock,
        availableInventory: availStock,
        reservedStock: resStock,
        inboundStock: inStock,
        damagedStock: damStock,
        daysOfInventory: doi,
        stockoutRisk: risk,
      });
    });
  });

  // 5. Cost Records
  const costs: CostRecord[] = getParsedCostRows().map((r) => {
    const cogs = cleanNum(r.cogs);
    return {
      sku: r.sku,
      date: '2026-08-01',
      cogs,
      manufacturingCost: cleanNum(r.manufacturingCost),
      packaging: cleanNum(r.packagingCost),
      freight: cleanNum(r.freightCost),
      warehouseCost: cleanNum(r.warehouseCost),
      marketplaceFees: cleanNum(r.marketplaceFeeBenchmark),
      paymentFees: cleanNum(r.paymentFeesBenchmark),
      returnsCost: cleanNum(r.returnsCostBenchmark),
      otherVariableCosts: Math.round(cogs * 0.05),
    };
  });

  // 6. Customer Records
  const customers: CustomerRecord[] = getParsedCustomerRows().map((r) => ({
    customerId: r.customerId,
    name: `Customer ${r.customerId.replace('CUST', '')}`,
    city: r.location,
    state: r.location === 'Mumbai' || r.location === 'Pune' ? 'Maharashtra' : r.location === 'Bengaluru' ? 'Karnataka' : r.location === 'Hyderabad' ? 'Telangana' : 'Delhi NCR',
    segment: r.segment as any,
    repeatCustomer: cleanNum(r.orderFrequency) > 1,
    totalOrders: cleanNum(r.orderFrequency),
    lifetimeValue: cleanNum(r.lifetimeValue),
    feedbackScore: 4.5,
  }));

  // 7. Finance Records
  const finance: FinanceRecord[] = getParsedFinanceRows().map((r) => {
    const grossRevenue = cleanNum(r.revenue);
    const netProfit = cleanNum(r.profit);
    return {
      date: r.date,
      channel: r.platform as any,
      grossRevenue,
      netRevenue: grossRevenue,
      totalCogs: cleanNum(r.cogs),
      adSpend: cleanNum(r.adSpend),
      marketplaceCommission: cleanNum(r.marketplaceFees),
      shippingCost: Math.round(grossRevenue * 0.04),
      paymentGatewayFee: Math.round(grossRevenue * 0.015),
      operatingExpense: cleanNum(r.operatingCost),
      netProfit,
      ebitdaMargin: grossRevenue > 0 ? Number(((netProfit / grossRevenue) * 100).toFixed(1)) : 0,
    };
  });

  // 8. Competitor Records
  const competitors: CompetitorRecord[] = getParsedCompetitorRows().map((r) => {
    const compPrice = cleanNum(r.price);
    const mrp = cleanNum(r.mrp);
    const discount = cleanNum(r.discount);
    const isSevere = r.availability === 'In Stock' && cleanNum(r.organicSearchPosition) < 20;
    return {
      date: r.date,
      category: r.category as any,
      competitorBrand: r.competitorBrand,
      competitorProductName: `${r.competitorBrand} ${r.comparableProduct}`,
      competitorPrice: compPrice,
      sleepsiaTargetSku: r.comparableProduct.includes('Cooling') ? 'SLP0002' : 'SLP0001',
      discountPercent: mrp > 0 ? Math.round((discount / mrp) * 100) : 10,
      rating: cleanNum(r.rating) || 4.2,
      reviewCount: cleanNum(r.reviewCount) || 3000,
      availability: (r.availability || 'In Stock') as any,
      searchPosition: cleanNum(r.organicSearchPosition) || 25,
      activePromotion: r.promotion && r.promotion !== 'None' ? r.promotion : 'Standard Price',
      threatLevel: isSevere ? 'Severe' : cleanNum(r.organicSearchPosition) < 50 ? 'High' : 'Medium',
    };
  });

  // 9. Shipping Records (Mapped directly from updated logistics manifest)
  const parsedShipping = getParsedShippingRows();
  const shippingMap = new Map(parsedShipping.map((sh) => [sh.orderId, sh]));

  const shipping: ShippingRecord[] = sales.map((s, idx) => {
    const matched = shippingMap.get(s.orderId);
    if (matched) {
      return {
        orderId: matched.orderId,
        date: matched.date,
        platform: matched.platform as any,
        sku: matched.sku,
        warehouse: matched.warehouse,
        carrier: matched.carrier as any,
        orderDate: matched.orderDate,
        shipDate: matched.shipDate,
        expectedDeliveryDate: matched.expectedDeliveryDate,
        actualDeliveryDate: matched.actualDeliveryDate,
        shipmentStatus: (matched.shipmentStatus === 'Delivered' ? 'Delivered' : matched.shipmentStatus === 'Failed' ? 'RTO' : 'Delayed') as any,
        deliveryStatus: (matched.deliveryStatus === 'On-time' ? 'On-Time' : matched.deliveryStatus === 'Late' ? 'Delayed' : 'Failed') as any,
        shippingCost: matched.shippingCost,
        delayReason: matched.delayReason,
        delayDays: matched.deliveryStatus === 'Late' ? 2 : 0,
      };
    }

    const fallbackCarrier = s.channel === 'Amazon' ? 'Blue Dart' : s.channel === 'Flipkart' ? 'Ekart' : 'Delhivery';
    const fallbackWarehouse = idx % 2 === 0 ? 'Bengaluru Hub (South DC)' : 'Noida Warehouse (North DC)';
    return {
      orderId: s.orderId,
      date: s.date,
      platform: s.channel,
      sku: s.sku,
      warehouse: fallbackWarehouse,
      carrier: fallbackCarrier as any,
      orderDate: s.date,
      shipDate: s.date,
      expectedDeliveryDate: s.date,
      actualDeliveryDate: s.date,
      shipmentStatus: 'Delivered',
      deliveryStatus: 'On-Time',
      shippingCost: Math.round(48 + (idx % 3) * 12),
      delayDays: 0,
    };
  });

  return {
    products: SLEEPSIA_PRODUCTS,
    marketplaceMasters: SLEEPSIA_MARKETPLACES,
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
      loadedAt: '2026-08-20 00:27',
      totalOrders: sales.length,
      dateRange: {
        start: PROTOTYPE_DATES[0],
        end: PROTOTYPE_DATES[PROTOTYPE_DATES.length - 1],
      },
      totalSkus: SLEEPSIA_PRODUCTS.length,
      activeChannels: SLEEPSIA_MARKETPLACES.length,
      sourceFileName: 'Sleepsia_Commerce_Intelligence_Prototype_Data_v2_with_Shipping.xlsx',
    },
  };
}
