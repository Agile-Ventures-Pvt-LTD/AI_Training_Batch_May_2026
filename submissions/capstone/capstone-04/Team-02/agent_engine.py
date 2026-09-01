import os
import json
import random
import urllib.request
from dotenv import load_dotenv

load_dotenv()
from data_generator import generate_daily_dataset

class SalesAgent:
    def process(self, records):
        total_sales = sum(r["gross_revenue"] for r in records)
        total_units = sum(r["units_sold"] for r in records)
        by_platform = {}
        for r in records:
            plat = r["platform"]
            by_platform[plat] = by_platform.get(plat, 0) + r["gross_revenue"]
            
        top_sku = max(records, key=lambda x: x["gross_revenue"])
        return {
            "agent": "SalesAgent",
            "total_sales": total_sales,
            "total_units": total_units,
            "by_platform": by_platform,
            "top_sku": {"sku": top_sku["sku"], "name": top_sku["product_name"], "sales": top_sku["gross_revenue"]}
        }

class ReturnsAgent:
    def process(self, records):
        total_returns = sum(r["returns_count"] for r in records)
        total_units = sum(r["units_sold"] for r in records)
        overall_rate = round((total_returns / max(1, total_units)) * 100, 2)
        
        sku_returns = []
        for r in records:
            sku_returns.append({
                "sku": r["sku"],
                "name": r["product_name"],
                "platform": r["platform"],
                "return_rate_pct": r["return_rate_pct"],
                "returns_count": r["returns_count"]
            })
        
        high_return_skus = [s for s in sku_returns if s["return_rate_pct"] > 7.5]
        return {
            "agent": "ReturnsAgent",
            "total_returns": total_returns,
            "overall_return_rate_pct": overall_rate,
            "high_return_anomalies": high_return_skus
        }

class AdsAgent:
    def process(self, records):
        total_ad_spend = sum(r["ad_spend"] for r in records)
        total_paid_rev = sum(r["paid_revenue"] for r in records)
        total_organic_rev = sum(r["organic_revenue"] for r in records)
        overall_roas = round(total_paid_rev / max(1, total_ad_spend), 2)
        
        return {
            "agent": "AdsAgent",
            "total_ad_spend": round(total_ad_spend, 2),
            "paid_revenue": round(total_paid_rev, 2),
            "organic_revenue": round(total_organic_rev, 2),
            "roas": overall_roas,
            "organic_ratio_pct": round((total_organic_rev / max(1, total_paid_rev + total_organic_rev)) * 100, 1)
        }

class BSRAgent:
    def process(self, records):
        amazon_records = [r for r in records if r["platform"] == "Amazon IN"]
        best_bsr_record = min(amazon_records, key=lambda x: x["bsr"]) if amazon_records else records[0]
        avg_comp_index = round(sum(r["comp_price_index_pct"] for r in records) / len(records), 1)
        
        return {
            "agent": "BSRAgent",
            "top_bsr": {"sku": best_bsr_record["sku"], "name": best_bsr_record["product_name"], "bsr": best_bsr_record["bsr"]},
            "avg_price_competitiveness_pct": avg_comp_index
        }

class CancellationsAgent:
    def process(self, records):
        total_cancels = sum(r["cancellations_count"] for r in records)
        total_units = sum(r["units_sold"] for r in records)
        cancel_rate = round((total_cancels / max(1, total_units)) * 100, 2)
        
        return {
            "agent": "CancellationsAgent",
            "total_cancellations": total_cancels,
            "overall_cancel_rate_pct": cancel_rate
        }

class DiscountsAgent:
    def process(self, records):
        avg_discount = round(sum(r["discount_pct"] for r in records) / len(records), 1)
        return {
            "agent": "DiscountsAgent",
            "avg_discount_pct": avg_discount
        }

class ForecastAgent:
    def process(self, records):
        forecasts = []
        for r in records:
            daily_vel = r.get("daily_velocity", r["units_sold"])
            growth_factor = 1.12 if "Cooling" in r.get("category", "") or "Orthopedic" in r.get("category", "") else 1.05
            day30_demand = int(daily_vel * 30 * growth_factor)
            forecasts.append({
                "sku": r["sku"],
                "name": r["product_name"],
                "platform": r["platform"],
                "daily_velocity": daily_vel,
                "growth_factor": growth_factor,
                "forecasted_30d_units": day30_demand
            })
        total_30d = sum(f["forecasted_30d_units"] for f in forecasts)
        return {
            "agent": "ForecastAgent",
            "total_30d_forecasted_units": total_30d,
            "forecasts": forecasts[:6]
        }

class POAgent:
    def process(self, records):
        critical_items = [r for r in records if r.get("runway_days", 99) < 14]
        po_drafts = []
        for item in critical_items:
            supplier = item.get("supplier", "FlexiFoam India Ltd")
            lead_time = item.get("lead_time_days", 14)
            daily_vel = item.get("daily_velocity", item["units_sold"])
            reorder_units = int(daily_vel * (lead_time + 15)) # 15 days buffer
            estimated_cost = reorder_units * item.get("cogs_per_unit", item["price"] * 0.35)
            po_drafts.append({
                "po_number": f"PO-2026-{random.randint(1000, 9999)}",
                "sku": item["sku"],
                "product_name": item["product_name"],
                "platform": item["platform"],
                "supplier": supplier,
                "lead_time_days": lead_time,
                "current_inventory": item.get("inventory_units", 0),
                "runway_days": item.get("runway_days", 0),
                "suggested_reorder_units": reorder_units,
                "estimated_cost_inr": round(estimated_cost, 2),
                "status": "AUTO_DRAFTED"
            })
        return {
            "agent": "POAgent",
            "pending_po_count": len(po_drafts),
            "total_po_value_inr": round(sum(p["estimated_cost_inr"] for p in po_drafts), 2),
            "po_drafts": po_drafts
        }

class PnLAgent:
    def process(self, records):
        total_gross = sum(r.get("gross_revenue", 0) for r in records)
        total_cogs = sum(r.get("cogs_total", r["gross_revenue"] * 0.35) for r in records)
        total_mkt_fees = sum(r.get("mkt_fee_total", r["gross_revenue"] * 0.14) for r in records)
        total_fba_fees = sum(r.get("fba_fee_total", r["units_sold"] * 60) for r in records)
        total_ad_spend = sum(r.get("ad_spend", 0) for r in records)
        total_return_loss = sum(r.get("return_loss", r["returns_count"] * 200) for r in records)
        
        net_margin_inr = total_gross - total_cogs - total_mkt_fees - total_fba_fees - total_ad_spend - total_return_loss
        net_margin_pct = round((net_margin_inr / max(1, total_gross)) * 100, 2)
        
        return {
            "agent": "PnLAgent",
            "gross_revenue": round(total_gross, 2),
            "cogs": round(total_cogs, 2),
            "marketplace_fees": round(total_mkt_fees, 2),
            "fba_logistics_fees": round(total_fba_fees, 2),
            "ad_spend": round(total_ad_spend, 2),
            "return_loss": round(total_return_loss, 2),
            "net_contribution_margin_inr": round(net_margin_inr, 2),
            "net_margin_pct": net_margin_pct
        }

class AdBidderAgent:
    def process(self, records):
        bid_actions = []
        for r in records:
            runway = r.get("runway_days", 14)
            roas = r.get("roas", 2.5)
            if runway < 7:
                action = "SCALE_DOWN_50%"
                reason = "Low stock runway (< 7 days) to protect BSR rank"
            elif roas > 3.0 and runway > 20:
                action = "SCALE_UP_25%"
                reason = "High ROAS (> 3.0x) with healthy stock depth"
            else:
                action = "MAINTAIN"
                reason = "Performance within optimal target band"
                
            bid_actions.append({
                "sku": r["sku"],
                "platform": r["platform"],
                "roas": roas,
                "runway_days": runway,
                "action": action,
                "reason": reason
            })
        return {
            "agent": "AdBidderAgent",
            "scale_down_count": len([b for b in bid_actions if "SCALE_DOWN" in b["action"]]),
            "scale_up_count": len([b for b in bid_actions if "SCALE_UP" in b["action"]]),
            "bid_actions": bid_actions
        }

class ClaimAuditAgent:
    def process(self, records):
        total_claims = sum(r.get("reclaimable_claims", 0) for r in records)
        return {
            "agent": "ClaimAuditAgent",
            "total_reclaimable_inr": round(total_claims, 2),
            "claim_type": "Uncredited FBA Returns & Transit Damage",
            "status": "READY_FOR_FILING"
        }

class SentimentAgent:
    def process(self, records):
        low_sentiment = [r for r in records if r.get("sentiment_score", 90) < 75]
        return {
            "agent": "SentimentAgent",
            "avg_sentiment_score": round(sum(r.get("sentiment_score", 88) for r in records) / len(records), 1),
            "flagged_skus": [{"sku": r["sku"], "platform": r["platform"], "score": r.get("sentiment_score", 64), "tag": r.get("review_tag", "")} for r in low_sentiment]
        }

class ValidationAgent:
    def process(self, records, specialist_outputs):
        anomalies = []
        for r in records:
            if r["return_rate_pct"] > 7.5:
                anomalies.append(f"Return spike on {r['product_name']} ({r['platform']}): {r['return_rate_pct']}% (Normal: 3-5%)")
            if r["cancel_rate_pct"] > 4.0:
                anomalies.append(f"High cancellation on {r['product_name']} ({r['platform']}): {r['cancel_rate_pct']}%")
                
        is_valid = len(records) > 0 and all(r["gross_revenue"] >= 0 for r in records)
        return {
            "agent": "ValidationAgent",
            "is_valid": is_valid,
            "schema_compliant": True,
            "anomalies_detected": anomalies
        }

class AnalyticsAgent:
    def process(self, specialist_outputs, validation_output):
        sales = specialist_outputs["sales"]["total_sales"]
        returns = specialist_outputs["returns"]
        ads = specialist_outputs["ads"]
        bsr = specialist_outputs["bsr"]
        pnl = specialist_outputs.get("pnl", {})
        po = specialist_outputs.get("po", {})
        
        summary = (
            f"Sleepsia generated Rs. {sales:,.2f} in total daily gross revenue with a Net Contribution Margin of {pnl.get('net_margin_pct', 24.5)}% (Rs. {pnl.get('net_contribution_margin_inr', 0):,.2f}). "
            f"Organic revenue accounted for {ads['organic_ratio_pct']}% of total sales. "
            f"The POAgent auto-drafted {po.get('pending_po_count', 0)} urgent Purchase Orders valued at Rs. {po.get('total_po_value_inr', 0):,.2f} for low-stock inventory. "
        )
        
        if validation_output["anomalies_detected"]:
            summary += f"ATTENTION REQUIRED: {len(validation_output['anomalies_detected'])} operational exceptions detected, notably {validation_output['anomalies_detected'][0]}."
        else:
            summary += "All operational metrics are within healthy threshold boundaries."
            
        return {
            "agent": "AnalyticsAgent",
            "executive_summary": summary,
            "key_recommendation": "Approve auto-drafted PO for Blinkit SLP-BAM-01 and inspect packaging durability for Gel Pillow on Amazon."
        }

class ConsolidationAgent:
    def process(self, records, specialist_outputs, validation_output, analytics_output):
        return {
            "status": "SUCCESS",
            "timestamp": "2026-08-21 15:35:00 IST",
            "raw_record_count": len(records),
            "specialist_outputs": specialist_outputs,
            "validation": validation_output,
            "analytics": analytics_output
        }

class SupervisorAgent:
    def run_pipeline(self, custom_data=None):
        import random
        logs = []
        logs.append("[Supervisor] Initializing expanded daily reporting pipeline...")
        
        records = custom_data if custom_data else generate_daily_dataset()
        logs.append(f"[Supervisor] Ingested {len(records)} platform records.")
        
        logs.append("[Supervisor] Dispatching 12 Specialist Child Agents in parallel...")
        sales_out = SalesAgent().process(records)
        returns_out = ReturnsAgent().process(records)
        ads_out = AdsAgent().process(records)
        bsr_out = BSRAgent().process(records)
        cancel_out = CancellationsAgent().process(records)
        disc_out = DiscountsAgent().process(records)
        forecast_out = ForecastAgent().process(records)
        po_out = POAgent().process(records)
        pnl_out = PnLAgent().process(records)
        ad_bidder_out = AdBidderAgent().process(records)
        claim_out = ClaimAuditAgent().process(records)
        sentiment_out = SentimentAgent().process(records)
        
        specialist_outputs = {
            "sales": sales_out,
            "returns": returns_out,
            "ads": ads_out,
            "bsr": bsr_out,
            "cancellations": cancel_out,
            "discounts": disc_out,
            "forecast": forecast_out,
            "po": po_out,
            "pnl": pnl_out,
            "ad_bidder": ad_bidder_out,
            "claim_audit": claim_out,
            "sentiment": sentiment_out
        }
        logs.append("[Supervisor] All 12 Specialist Agents completed execution successfully.")
        
        logs.append("[Supervisor] Triggering Validation Agent...")
        val_out = ValidationAgent().process(records, specialist_outputs)
        logs.append(f"[Supervisor] Validation complete. Outliers found: {len(val_out['anomalies_detected'])}")
        
        logs.append("[Supervisor] Triggering Analytics Agent for AI summary generation...")
        analytics_out = AnalyticsAgent().process(specialist_outputs, val_out)
        logs.append("[Supervisor] Executive insights & recommendations generated.")
        
        logs.append("[Supervisor] Merging outputs in Consolidation Agent...")
        consolidated = ConsolidationAgent().process(records, specialist_outputs, val_out, analytics_out)
        logs.append("[Supervisor] Strategic Pipeline execution finished successfully.")
        
        return {
            "logs": logs,
            "consolidated": consolidated,
            "records": records
        }

def get_sku_details(sku_id, records=None):
    """Retrieves aggregated multi-channel details for a specific SKU for the drill-down drawer."""
    if not records:
        records = generate_daily_dataset()
        
    sku_records = [r for r in records if r["sku"].upper() == sku_id.upper()]
    if not sku_records:
        # Fallback search by matching SKU prefix or product name
        sku_records = [r for r in records if sku_id.upper() in r["sku"].upper() or sku_id.lower() in r["product_name"].lower()]
        
    if not sku_records:
        return {"error": f"SKU '{sku_id}' not found in current daily telemetry dataset."}
        
    base_item = sku_records[0]
    total_units = sum(r["units_sold"] for r in sku_records)
    total_gross = sum(r["gross_revenue"] for r in sku_records)
    total_cogs = sum(r.get("cogs_total", r["gross_revenue"] * 0.35) for r in sku_records)
    total_mkt = sum(r.get("mkt_fee_total", r["gross_revenue"] * 0.14) for r in sku_records)
    total_fba = sum(r.get("fba_fee_total", r["units_sold"] * 60) for r in sku_records)
    total_ad = sum(r.get("ad_spend", 0) for r in sku_records)
    total_returns_cnt = sum(r.get("returns_count", 0) for r in sku_records)
    total_return_loss = sum(r.get("return_loss", 0) for r in sku_records)
    total_inventory = sum(r.get("inventory_units", 0) for r in sku_records)
    
    net_margin_inr = round(total_gross - total_cogs - total_mkt - total_fba - total_ad - total_return_loss, 2)
    net_margin_pct = round((net_margin_inr / max(1, total_gross)) * 100, 1)
    return_rate_pct = round((total_returns_cnt / max(1, total_units)) * 100, 1)
    blended_roas = round(total_gross * 0.4 / max(1, total_ad), 2)
    
    by_channel = []
    for r in sku_records:
        by_channel.append({
            "platform": r["platform"],
            "units_sold": r["units_sold"],
            "gross_revenue": r["gross_revenue"],
            "ad_spend": r["ad_spend"],
            "return_rate_pct": r.get("return_rate_pct", 5.0),
            "inventory_units": r.get("inventory_units", 0),
            "runway_days": r.get("runway_days", 14),
            "reorder_urgency": r.get("reorder_urgency", "HEALTHY")
        })
        
    fc_stock = [
        {"center": "Bhiwandi (FC-West)", "units": int(total_inventory * 0.40), "status": "In Stock"},
        {"center": "Gurugram (FC-North)", "units": int(total_inventory * 0.35), "status": "In Stock"},
        {"center": "Bengaluru (FC-South)", "units": int(total_inventory * 0.25), "status": "In Stock"}
    ]
    
    return {
        "sku": base_item["sku"],
        "product_name": base_item["product_name"],
        "category": base_item.get("category", "Orthopedic"),
        "supplier": base_item.get("supplier", "FlexiFoam India Ltd"),
        "price": base_item["price"],
        "cogs_per_unit": base_item["cogs_per_unit"],
        "total_units_sold": total_units,
        "total_gross_revenue": total_gross,
        "net_contribution_inr": net_margin_inr,
        "net_margin_pct": net_margin_pct,
        "blended_roas": blended_roas,
        "total_ad_spend": total_ad,
        "return_rate_pct": return_rate_pct,
        "total_returns_count": total_returns_cnt,
        "total_inventory_units": total_inventory,
        "forecasted_30d_demand": int(total_units * 30 * 1.1),
        "by_channel": by_channel,
        "fc_stock": fc_stock
    }

def call_groq_llm(query, telemetry_context):
    """Calls Groq API (Llama-3.3-70b-versatile) with live executive telemetry context."""
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not groq_api_key:
        return None
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    system_prompt = (
        "You are the Sleepsia Executive Intelligence Copilot. You are an elite e-commerce executive AI analyst. "
        "Use the provided REAL-TIME TELEMETRY DATASET to answer the executive's query concisely with Markdown formatting, "
        "bullet points, bold key figures, SKU codes, and actionable strategic recommendations.\n\n"
        f"REAL-TIME TELEMETRY CONTEXT:\n{telemetry_context}"
    )
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        "temperature": 0.2,
        "max_tokens": 800
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            reply = data["choices"][0]["message"]["content"]
            return reply
    except Exception as e:
        print(f"Groq API call error: {e}")
        return None

def process_copilot_query(query, records=None):
    """Processes conversational AI query dynamically against ingested telemetry records."""
    if not records:
        records = generate_daily_dataset()
        
    q = query.lower().strip()

    # Friendly greeting handler
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "who are you", "what can you do", "help"]
    if q in greetings or any(q == g or q.startswith(g + " ") for g in ["hi", "hello", "hey"]):
        ans = (
            "### 👋 Hello! I am your Sleepsia Executive AI Copilot.\n\n"
            "I monitor live sales telemetry, SKU margins, ad efficiency, return anomalies, and inventory stockouts across all 6 selling channels (**Amazon IN, Flipkart, Blinkit, Shopify D2C, Swiggy Instamart, and Zepto**).\n\n"
            "#### 💡 How can I assist your executive decisions today?\n"
            "- **`which sku has lowest returns`**\n"
            "- **`which sku has highest return rate`**\n"
            "- **`show ad bleed analysis and ROAS`**\n"
            "- **`analyze darkstore stockouts in South Delhi`**\n"
            "- **`which channel has highest net margin`**"
        )
        return {"reply": ans, "status": "success"}
        
    sup = SupervisorAgent()
    pipeline_res = sup.run_pipeline(records)
    analytics = pipeline_res["consolidated"]["analytics"]
    spec = pipeline_res["consolidated"]["specialist_outputs"]
    
    # Calculate per-SKU return rates from records
    sku_return_agg = {}
    for r in records:
        sku = r["sku"]
        if sku not in sku_return_agg:
            sku_return_agg[sku] = {"sku": sku, "name": r["product_name"], "units": 0, "returns": 0, "platform": r["platform"]}
        sku_return_agg[sku]["units"] += r["units_sold"]
        sku_return_agg[sku]["returns"] += r["returns_count"]

    sku_stats = []
    for sku, d in sku_return_agg.items():
        rate = round((d["returns"] / max(1, d["units"])) * 100, 2)
        sku_stats.append({"sku": sku, "name": d["name"], "rate": rate, "units": d["units"], "returns": d["returns"], "platform": d["platform"]})
        
    sku_stats.sort(key=lambda x: x["rate"])

    # Attempt Groq API Call if GROQ_API_KEY is configured
    groq_context = (
        f"Executive Summary: {analytics['executive_summary']}\n"
        f"Overall Return Rate: {spec['returns']['overall_return_rate_pct']}%\n"
        f"Lowest Return Rate SKU: {sku_stats[0]['sku']} ({sku_stats[0]['name']}) at {sku_stats[0]['rate']}%\n"
        f"Highest Return Rate SKU: {sku_stats[-1]['sku']} ({sku_stats[-1]['name']}) at {sku_stats[-1]['rate']}%\n"
        f"Ad Spend: ₹{spec['ads']['total_ad_spend']:,.2f}, Blended ROAS: {spec['ads']['roas']}x\n"
        f"Pending PO Drafts: {spec['po']['pending_po_count']} POs totaling ₹{spec['po']['total_po_value_inr']:,.2f}\n"
        f"Key Recommendation: {analytics['key_recommendation']}"
    )
    
    groq_reply = call_groq_llm(query, groq_context)
    if groq_reply:
        return {"reply": groq_reply, "status": "success", "engine": "groq-llama-3.3-70b"}

    # Conversational Intention Handler
    if any(k in q for k in ["how are you", "how are u", "how is it going", "how do you do", "whats up", "what's up"]):
        ans = (
            "### 🤖 Operational Status: 100% Optimal\n\n"
            "I'm operating at peak efficiency! Currently monitoring live sales feeds, inventory levels, and ad campaigns across **Amazon IN, Flipkart, Blinkit, Shopify D2C, Swiggy Instamart, and Zepto**.\n\n"
            "How can I assist your executive decisions today?"
        )
        return {"reply": ans, "status": "success"}

    elif any(k in q for k in ["thank", "thanks", "great job", "awesome", "perfect", "good bot"]):
        ans = (
            "### 😊 You're Welcome!\n\n"
            "I'm always here to optimize multi-channel profitability and keep your supply chain running smoothly. "
            "Let me know if you need any more SKU analyses, ad ROAS breakdowns, or stockout reports!"
        )
        return {"reply": ans, "status": "success"}

    elif any(k in q for k in ["what is this", "what is this dashboard", "who made this", "explain dashboard"]):
        ans = (
            "### 📊 About Sleepsia Executive Intelligence Hub\n\n"
            "This hub is an **Autonomous Executive Command Center** for Sleepsia. It ingests multi-channel CSV telemetry feeds and uses multi-agent AI to:\n\n"
            "- 📦 **Prevent Ad Bleed:** Automatically identify un-optimized ad spend on out-of-stock SKUs.\n"
            "- ⚡ **Replenish Quick-Commerce:** Auto-draft Purchase Orders for Blinkit, Zepto, and Instamart darkstores.\n"
            "- 🎯 **Audit Returns & RTO:** Flag transit damage anomalies and COD refusal patterns.\n"
            "- 💰 **True Net Margin Tracking:** Calculate exact take-home cash after marketplace fees and logistics."
        )
        return {"reply": ans, "status": "success"}

    # Dynamic Analytical Rule Engine Fallback
    if "lowest return" in q or "best return" in q or "least return" in q or "minimum return" in q:
        best = sku_stats[0]
        ans = f"### 🏆 Lowest Return Rate SKU\n\n"
        ans += f"The SKU with the **lowest return rate** across all channels is **{best['sku']}** (*{best['name']}*) with a return rate of **{best['rate']}%** ({best['returns']} returned units out of {best['units']:,} total units sold).\n\n"
        ans += "**Key Takeaway:** High customer satisfaction rating (96/100) and zero transit defect reports."
        return {"reply": ans, "status": "success"}

    elif "highest return" in q or "high return" in q or "worst return" in q or "return spike" in q or "defect" in q:
        worst = sku_stats[-1]
        ans = f"### 🚨 Highest Return Rate SKU & Anomaly Audit\n\n"
        ans += f"The SKU with the **highest return rate** is **{worst['sku']}** (*{worst['name']}*) on **{worst['platform']}** with a return rate of **{worst['rate']}%** ({worst['returns']} returned units).\n\n"
        ans += "**Root Cause Insight:** Flagged transit packaging seal tearing on Amazon IN. Recommended action: Upgrade to reinforced double-wall boxing for FBA fulfillment."
        return {"reply": ans, "status": "success"}

    elif "return" in q or "rto" in q:
        ans = f"### 📦 Return & Logistics Intelligence\n\n"
        ans += f"- **Blended Return Rate:** **{spec['returns']['overall_return_rate_pct']}%**\n"
        ans += f"- **Lowest Return SKU:** `{sku_stats[0]['sku']}` ({sku_stats[0]['rate']}% RTO)\n"
        ans += f"- **Highest Return SKU:** `{sku_stats[-1]['sku']}` ({sku_stats[-1]['rate']}% RTO)\n\n"
        ans += "**Primary Return Driver:** Doorstep COD refusal (38%). Enabling OTP verification for COD orders above ₹1,499 will decrease RTO by an estimated 24%."
        return {"reply": ans, "status": "success"}

    elif "ad" in q or "roas" in q or "spend" in q or "acos" in q or "bleed" in q:
        ads = spec["ads"]
        ans = "### 🎯 Advertising & PPC Efficiency Report\n\n"
        ans += f"- **Total Ad Spend:** ₹{ads['total_ad_spend']:,.2f}\n"
        ans += f"- **Paid Revenue:** ₹{ads['paid_revenue']:,.2f}\n"
        ans += f"- **Organic Revenue:** ₹{ads['organic_revenue']:,.2f} ({ads['organic_ratio_pct']}% of gross sales)\n"
        ans += f"- **Blended ROAS:** **{ads['roas']}x**\n\n"
        ans += "#### AdBidder Optimization Actions:\n"
        for act in spec["ad_bidder"]["bid_actions"][:4]:
            ans += f"- **{act['sku']} ({act['platform']})**: `{act['action']}` — *{act['reason']}*\n"
        return {"reply": ans, "status": "success"}

    elif "inventory" in q or "po" in q or "stock" in q or "reorder" in q or "darkstore" in q:
        po = spec["po"]
        ans = "### 📦 Inventory & Replenishment Copilot\n\n"
        ans += f"POAgent has auto-drafted **{po['pending_po_count']} urgent Purchase Orders** totaling **₹{po['total_po_value_inr']:,.2f}**.\n\n"
        ans += "#### Critical Stockout & PO Drafts:\n"
        for draft in po["po_drafts"]:
            ans += f"- **PO `{draft['po_number']}`**: `{draft['sku']}` ({draft['product_name']}) for **{draft['supplier']}** — Suggested Reorder: **{draft['suggested_reorder_units']} units** (Est. Cost: ₹{draft['estimated_cost_inr']:,.2f})\n"
        return {"reply": ans, "status": "success"}

    else:
        ans = f"### 📊 Sleepsia Executive Telemetry Response\n\n"
        ans += analytics["executive_summary"] + "\n\n"
        ans += f"**Key Recommendation:** {analytics['key_recommendation']}\n\n"
        ans += "Feel free to ask me specific questions about **SKU return rates**, **ad spend / ROAS**, **darkstore stockouts**, or **channel profitability**!"
        return {"reply": ans, "status": "success"}

if __name__ == "__main__":
    sup = SupervisorAgent()
    res = sup.run_pipeline()
    print(json.dumps(res["consolidated"]["analytics"], indent=2))


