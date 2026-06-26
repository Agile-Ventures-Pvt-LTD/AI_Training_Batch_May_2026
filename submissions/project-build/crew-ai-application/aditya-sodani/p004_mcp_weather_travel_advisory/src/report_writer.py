from src.prompts import (
    travel_readiness_prompt,
    weather_risk_summary_prompt,
    packing_recommendation_prompt
)

from src.resources import get_checklist, get_advisory_rules

from src.schemas import FinalReport


def build_report(normalized, risk):
    # Merge normalized data + risk data
    report = {**normalized, **risk}

    # ---------------- PROMPT OUTPUTS ---------------- #

    report["packing_suggestions"] = packing_recommendation_prompt({
        "destination": normalized["destination"],
        "weather_risk": risk["weather_risk"],
        "risk_factors": risk.get("risk_factors", [])
    })

    report["travel_readiness_advisory"] = travel_readiness_prompt({
        "destination": normalized["destination"],
        "weather_risk": risk["weather_risk"],
        "forecast_summary": "3-day outlook",
        "recommended_actions": risk.get("recommended_actions", [])
    })

    report["weather_risk_explanation"] = weather_risk_summary_prompt({
        "destination": normalized["destination"],
        "weather_risk": risk["weather_risk"],
        "risk_factors": risk.get("risk_factors", [])
    })

    # ---------------- METADATA ---------------- #

    report["resources_used"] = [
        "resource://travel/checklist",
        "resource://travel/advisory-rules",
        "resource://weather/normalized-forecast-schema"
    ]

    report["tools_used"] = [
        "validate_city_input_tool",
        "get_weather_forecast_tool",
        "normalize_weather_data_tool",
        "calculate_weather_risk_tool",
        "save_travel_advisory_tool"
    ]

    report["prompts_used"] = [
        "travel_readiness_prompt",
        "weather_risk_summary_prompt",
        "packing_recommendation_prompt"
    ]

    report["checklist"] = get_checklist()
    report["advisory_rules"] = get_advisory_rules()

    # ---------------- SCHEMA VALIDATION ---------------- #

    try:
        validated = FinalReport(**report)
        return validated.dict()
    except Exception as e:
        print("Schema validation failed:", str(e))
        return report
