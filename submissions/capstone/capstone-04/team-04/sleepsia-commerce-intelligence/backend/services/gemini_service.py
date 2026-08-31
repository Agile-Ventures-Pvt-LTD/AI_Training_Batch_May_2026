"""
Server-side Gemini AI Multi-Agent & Chat BI Service in Python.
Powered by dynamic specialist agent data extraction and the google-genai Python SDK.

✅ M-4: Includes comprehensive logging for API calls, model cascade, and error tracking.
"""

import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
from .kpi_engine import calculate_kpis
from .multi_agent_supervisor import run_orchestrated_agent_pipeline, fmt_curr, fmt_num

# ✅ M-4: Import logging utilities
from backend.utils.logging_utils import StructuredLogger, get_correlation_id

logger = logging.getLogger(__name__)

# Model cascade in order of speed and capability
MODEL_CASCADE = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']

def get_genai_client():
    """✅ M-4: Initialize Gemini client with logging"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.warning("GEMINI_API_KEY not configured")
        return None
    try:
        from google import genai
        logger.debug("Initializing Gemini client")
        return genai.Client(api_key=api_key)
    except Exception as e:
        logger.error("Failed to initialize Gemini client", extra={
            'error': str(e),
            'correlation_id': get_correlation_id(),
        }, exc_info=e)
        return None

def generate_content_with_fallback(prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
    """✅ M-4: Generate content with fallback and comprehensive logging"""
    start_time = time.time()
    client = get_genai_client()
    if not client:
        logger.warning("Gemini client unavailable")
        return None

    logger.debug("Starting model cascade", extra={
        'model_count': len(MODEL_CASCADE),
        'has_system_instruction': system_instruction is not None,
        'correlation_id': get_correlation_id(),
    })

    for attempt, model_name in enumerate(MODEL_CASCADE, 1):
        try:
            model_start = time.time()
            config = {}
            if system_instruction:
                config['system_instruction'] = system_instruction

            logger.debug(f"Attempting {model_name}", extra={
                'attempt': attempt,
                'total_attempts': len(MODEL_CASCADE),
            })

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config if config else None,
            )

            model_duration = (time.time() - model_start) * 1000

            if response and response.text:
                total_duration = (time.time() - start_time) * 1000

                # ✅ M-4: Log successful API call
                StructuredLogger.log_external_api_call(
                    logger, 'Gemini', f'/models/{model_name}/generateContent',
                    200, model_duration
                )

                logger.info("Gemini content generation succeeded", extra={
                    'model': model_name,
                    'attempt': attempt,
                    'model_duration_ms': f"{model_duration:.1f}",
                    'total_duration_ms': f"{total_duration:.1f}",
                    'response_length': len(response.text),
                })
                return response.text

        except Exception as e:
            model_duration = (time.time() - model_start) * 1000

            # ✅ M-4: Log failed API call attempt
            logger.warning(f"Gemini model {model_name} failed", extra={
                'model': model_name,
                'attempt': attempt,
                'total_attempts': len(MODEL_CASCADE),
                'error': str(e),
                'duration_ms': f"{model_duration:.1f}",
                'will_retry': attempt < len(MODEL_CASCADE),
                'correlation_id': get_correlation_id(),
            })
            continue

    total_duration = (time.time() - start_time) * 1000
    logger.error("All Gemini models failed", extra={
        'attempted_models': len(MODEL_CASCADE),
        'total_duration_ms': f"{total_duration:.1f}",
        'correlation_id': get_correlation_id(),
    })

    return None

def run_gemini_supervisor_agent(data: Dict[str, Any], selected_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """✅ M-4: Run supervisor agent with comprehensive logging"""
    start_time = time.time()

    date_to_analyze = selected_date or data.get('metadata', {}).get('dateRange', {}).get('end', '2026-08-07')

    logger.info("Supervisor agent started", extra={
        'correlation_id': get_correlation_id(),
        'date': date_to_analyze,
        'data_size': sum(len(data.get(k, [])) for k in ['sales', 'advertising', 'shipping', 'inventory']),
    })

    kpis = calculate_kpis(data, {'date': date_to_analyze})
    orchestrated = run_orchestrated_agent_pipeline(data, date_to_analyze)
    fallback_findings = orchestrated.get('findings', [])

    client = get_genai_client()
    if not client:
        duration_ms = (time.time() - start_time) * 1000
        logger.warning("Supervisor agent using fallback (no Gemini client)", extra={
            'duration_ms': f"{duration_ms:.1f}",
            'fallback_findings_count': len(fallback_findings),
        })
        return fallback_findings

    sales = kpis.get('sales', {})
    prof = kpis.get('profitability', {})
    ads = kpis.get('advertising', {})
    inv = kpis.get('inventory', {})
    ship = kpis.get('shipping', {})

    prompt = f"""
You are the Supervisor AI Agent for Sleepsia Commerce Intelligence.
Analyze the following factual unified commerce data calculated strictly from the dataset for date: {date_to_analyze}.

KEY BUSINESS KPIS (CALCULATED FROM ACTIVE DATASET):
- Net Realized Revenue: {fmt_curr(sales.get('netRevenue', 0))} ({fmt_num(sales.get('totalOrders', 0))} Orders, {fmt_num(sales.get('unitsSold', 0))} Units, AOV: {fmt_curr(sales.get('aov', 0))})
- Net Profit: {fmt_curr(prof.get('netProfit', 0))} ({prof.get('profitMarginPercent', 0)}% Margin)
- Advertising Spend: {fmt_curr(ads.get('totalSpend', 0))} | Blended ROAS: {ads.get('roas', 0)}x | Blended ACoS: {ads.get('acos', 0)}% | TACoS: {ads.get('tacos', 0)}%
- Inventory Days of Inventory: {inv.get('averageDaysOfInventory', 0)} days avg | High Stockout Risk SKUs: {inv.get('highRiskSkusCount', 0)}
- Fleet Delivery SLA: {ship.get('onTimeDeliveryRate', 0)}% On-Time | Late Rate: {ship.get('lateDeliveryRate', 0)}%

DETERMINISTIC SPECIALIST EVIDENCE:
{json.dumps(fallback_findings, indent=2)}

TASK:
Review the computed evidence and produce 4 to 6 prioritized, structured analytical findings in valid JSON array format.
Each object must contain keys: "metric", "current_value", "previous_value", "change_percent", "severity", "finding", "possible_causes", "recommended_action", "priority", "area", "confidence", "expected_business_impact", "source", "agent".
Return ONLY the raw JSON array without markdown ticks.
"""

    res_text = generate_content_with_fallback(
        prompt,
        system_instruction='You are an enterprise AI analytics agent for Sleepsia. Return structured actionable JSON findings strictly based on the provided dataset.'
    )

    if res_text:
        try:
            clean = res_text.strip()
            if clean.startswith('```json'):
                clean = clean[7:]
            if clean.startswith('```'):
                clean = clean[3:]
            if clean.endswith('```'):
                clean = clean[:-3]
            parsed = json.loads(clean.strip())
            if isinstance(parsed, list) and len(parsed) > 0:
                for idx, item in enumerate(parsed):
                    item['id'] = f"gemini-find-{idx + 1}-{date_to_analyze}"

                duration_ms = (time.time() - start_time) * 1000
                # ✅ M-4: Log successful supervisor findings
                logger.info("Supervisor agent completed with Gemini findings", extra={
                    'duration_ms': f"{duration_ms:.1f}",
                    'findings_count': len(parsed),
                    'correlation_id': get_correlation_id(),
                })
                return parsed
        except Exception as e:
            logger.error("Failed to parse Gemini findings", extra={
                'error': str(e),
                'correlation_id': get_correlation_id(),
            }, exc_info=e)

    duration_ms = (time.time() - start_time) * 1000
    # ✅ M-4: Log fallback usage
    logger.warning("Supervisor agent using fallback findings", extra={
        'duration_ms': f"{duration_ms:.1f}",
        'fallback_findings_count': len(fallback_findings),
        'reason': 'No Gemini response or parsing failed',
    })

    return fallback_findings

def query_gemini_chat_bi(user_query: str, data: Dict[str, Any], selected_date: Optional[str] = None) -> Dict[str, Any]:
    date_to_analyze = selected_date or data.get('metadata', {}).get('dateRange', {}).get('end', '2026-08-07')
    kpis = calculate_kpis(data, {'date': date_to_analyze})

    client = get_genai_client()
    sales = kpis.get('sales', {})
    prof = kpis.get('profitability', {})
    ads = kpis.get('advertising', {})
    inv = kpis.get('inventory', {})
    ship = kpis.get('shipping', {})

    if not client:
        return {
            'answer': (
                f"Based on Sleepsia dataset for {date_to_analyze}: Net revenue was {fmt_curr(sales.get('netRevenue', 0))} "
                f"across {fmt_num(sales.get('totalOrders', 0))} orders (AOV {fmt_curr(sales.get('aov', 0))}). Net profit stood at "
                f"{fmt_curr(prof.get('netProfit', 0))} ({prof.get('profitMarginPercent', 0)}% margin). Ad spend of {fmt_curr(ads.get('totalSpend', 0))} "
                f"achieved {ads.get('roas', 0)}x ROAS. Fleet on-time delivery reached {ship.get('onTimeDeliveryRate', 0)}%."
            ),
            'sources': ['Internal_Sales', 'Marketplace_Data', 'Advertising_Data', 'Inventory_Data', 'Shipping_Data'],
        }

    prompt = f"""
You are Sleepsia Chat BI, an intelligent executive commercial assistant.
Answer the following executive query accurately and concisely using ONLY the real numbers from the active dataset below.

DATASET CONTEXT (Date: {date_to_analyze}):
- Total Net Revenue: {fmt_curr(sales.get('netRevenue', 0))} ({fmt_num(sales.get('totalOrders', 0))} orders, {fmt_num(sales.get('unitsSold', 0))} units, AOV: {fmt_curr(sales.get('aov', 0))})
- Profitability: Net Profit {fmt_curr(prof.get('netProfit', 0))}, Margin: {prof.get('profitMarginPercent', 0)}%, Total COGS: {fmt_curr(prof.get('totalCogs', 0))}
- Advertising: Spend {fmt_curr(ads.get('totalSpend', 0))}, ROAS: {ads.get('roas', 0)}x, ACoS: {ads.get('acos', 0)}%, TACoS: {ads.get('tacos', 0)}%
- Inventory: Avg Days of Inventory: {inv.get('averageDaysOfInventory', 0)} days, High Risk SKUs: {inv.get('highRiskSkusCount', 0)}
- Logistics: Total Shipments: {ship.get('totalShipments', 0)}, On-time SLA: {ship.get('onTimeDeliveryRate', 0)}%, Late: {ship.get('lateDeliveryRate', 0)}%
- Top SKUs by Profit: {json.dumps(prof.get('profitPerSku', [])[:5])}
- Top Channels by Profit: {json.dumps(prof.get('profitPerMarketplace', [])[:5])}

USER QUERY:
"{user_query}"

Provide a crisp executive-ready response with clear bullet points where relevant, linking causal relationships between marketing, channel mix, inventory, and profit.
"""

    answer_text = generate_content_with_fallback(prompt)
    return {
        'answer': answer_text or f"Sleepsia recorded {fmt_curr(sales.get('netRevenue', 0))} in net revenue and {fmt_curr(prof.get('netProfit', 0))} net profit on {date_to_analyze}.",
        'sources': ['Internal_Sales', 'Marketplace_Data', 'Advertising_Data', 'Inventory_Data', 'Shipping_Data'],
    }
