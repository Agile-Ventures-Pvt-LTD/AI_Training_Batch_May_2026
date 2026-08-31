import random
from datetime import datetime

def get_sleepsia_skus():
    return [
        {"sku": "SLP-BAM-01", "name": "Bamboo Memory Foam Cervical Pillow", "category": "Orthopedic", "price": 1399, "cogs": 480, "lead_time_days": 14, "supplier": "FlexiFoam India Ltd"},
        {"sku": "SLP-GEL-02", "name": "Gel-Infused Orthopedic Pillow", "category": "Cooling", "price": 1699, "cogs": 590, "lead_time_days": 12, "supplier": "ThermoGel Molders Corp"},
        {"sku": "SLP-SHR-03", "name": "Shredded Memory Foam Pillow", "category": "Standard", "price": 1099, "cogs": 360, "lead_time_days": 10, "supplier": "FlexiFoam India Ltd"},
        {"sku": "SLP-MIC-04", "name": "Microfiber Cooling Pillow", "category": "Microfiber", "price": 799, "cogs": 240, "lead_time_days": 7, "supplier": "Standard MicroTex Mills"},
        {"sku": "SLP-PREG-05", "name": "Full Body Pregnancy Pillow", "category": "Specialty", "price": 2799, "cogs": 920, "lead_time_days": 15, "supplier": "Ergotech Comfort Pvt Ltd"},
        {"sku": "SLP-LUM-06", "name": "Ergonomic Lumbar Support Cushion", "category": "Cushion", "price": 1199, "cogs": 410, "lead_time_days": 8, "supplier": "Ergotech Comfort Pvt Ltd"},
    ]

def generate_daily_dataset(date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        
    skus = get_sleepsia_skus()
    platforms = ["Amazon IN", "Flipkart", "Blinkit", "Swiggy Instamart"]
    
    records = []
    
    for item in skus:
        for platform in platforms:
            weight = 1.0
            commission_pct = 14.0
            fba_fee_per_unit = 65.0
            if platform == "Amazon IN":
                weight = 2.2
                commission_pct = 14.5
                fba_fee_per_unit = 75.0
            elif platform == "Flipkart":
                weight = 1.5
                commission_pct = 13.0
                fba_fee_per_unit = 60.0
            elif platform == "Blinkit":
                weight = 0.8
                commission_pct = 18.0
                fba_fee_per_unit = 40.0
            elif platform == "Swiggy Instamart":
                weight = 0.6
                commission_pct = 18.0
                fba_fee_per_unit = 40.0
                
            units_sold = int(random.randint(15, 60) * weight)
            gross_revenue = units_sold * item["price"]
            cogs_total = units_sold * item["cogs"]
            mkt_fee_total = round(gross_revenue * (commission_pct / 100.0), 2)
            fba_fee_total = units_sold * fba_fee_per_unit
            
            # Anomaly trigger for SLP-GEL-02 on Amazon IN
            if item["sku"] == "SLP-GEL-02" and platform == "Amazon IN":
                return_rate = round(random.uniform(0.082, 0.095), 4) # Spiked!
                sentiment_score = 64
                review_tag = "packaging seal tear in transit"
            else:
                return_rate = round(random.uniform(0.035, 0.065), 4)
                sentiment_score = random.randint(84, 96)
                review_tag = "excellent neck support"
                
            returns_count = int(units_sold * return_rate)
            cancellations_count = int(units_sold * random.uniform(0.015, 0.035))
            return_loss = returns_count * (item["price"] * 0.4 + 40) # freight + repackaging damage
            
            ad_spend = round(gross_revenue * random.uniform(0.12, 0.22), 2)
            paid_revenue = round(gross_revenue * random.uniform(0.35, 0.45), 2)
            organic_revenue = gross_revenue - paid_revenue
            
            net_contribution_margin = round(gross_revenue - cogs_total - mkt_fee_total - fba_fee_total - ad_spend - return_loss, 2)
            net_margin_pct = round((net_contribution_margin / max(1, gross_revenue)) * 100, 2)
            
            # Stock inventory & runway days calculation
            daily_velocity = max(1.0, round(units_sold / 1.0, 1))
            if item["sku"] == "SLP-BAM-01" and platform == "Blinkit":
                inventory_units = 18 # Critical low runway!
            elif item["sku"] == "SLP-GEL-02" and platform == "Amazon IN":
                inventory_units = 120
            else:
                inventory_units = int(daily_velocity * random.uniform(12, 28))
                
            runway_days = round(inventory_units / daily_velocity, 1)
            reorder_urgency = "CRITICAL" if runway_days < 7 else ("WARNING" if runway_days < 14 else "HEALTHY")
            
            reclaimable_claims = round(returns_count * random.uniform(150, 350), 2) if return_rate > 0.06 else round(random.uniform(0, 500), 2)
            
            bsr = random.randint(750, 1500) if platform == "Amazon IN" else random.randint(1200, 3000)
            
            records.append({
                "date": date_str,
                "sku": item["sku"],
                "product_name": item["name"],
                "category": item["category"],
                "supplier": item["supplier"],
                "lead_time_days": item["lead_time_days"],
                "platform": platform,
                "price": item["price"],
                "cogs_per_unit": item["cogs"],
                "units_sold": units_sold,
                "gross_revenue": gross_revenue,
                "cogs_total": cogs_total,
                "mkt_fee_total": mkt_fee_total,
                "fba_fee_total": fba_fee_total,
                "returns_count": returns_count,
                "return_rate_pct": round(return_rate * 100, 2),
                "return_loss": round(return_loss, 2),
                "cancellations_count": cancellations_count,
                "cancel_rate_pct": round((cancellations_count / max(1, units_sold)) * 100, 2),
                "ad_spend": ad_spend,
                "paid_revenue": paid_revenue,
                "organic_revenue": organic_revenue,
                "roas": round(paid_revenue / max(1, ad_spend), 2),
                "net_contribution_margin": net_contribution_margin,
                "net_margin_pct": net_margin_pct,
                "inventory_units": inventory_units,
                "daily_velocity": daily_velocity,
                "runway_days": runway_days,
                "reorder_urgency": reorder_urgency,
                "reclaimable_claims": reclaimable_claims,
                "sentiment_score": sentiment_score,
                "review_tag": review_tag,
                "bsr": bsr,
                "comp_price_index_pct": round(random.uniform(92.0, 97.5), 1),
                "discount_pct": round(random.uniform(10.0, 25.0), 1)
            })
            
    return records

if __name__ == "__main__":
    data = generate_daily_dataset()
    print(f"Generated {len(data)} records for Sleepsia reporting pipeline.")
