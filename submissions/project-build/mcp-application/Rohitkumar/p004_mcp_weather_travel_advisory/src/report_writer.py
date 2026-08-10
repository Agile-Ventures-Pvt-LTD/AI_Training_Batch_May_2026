from src.prompts import RISK_DESCRIPTIONS, RISK_ACTIONS, PACKING_SUGGESTIONS, TRAVEL_READINESS, RISK_EXPLANATION

def generate_report(normalized_data: dict, risk_data: dict) -> dict:
    risk = risk_data.get("weather_risk", "LOW")
    keys = risk_data.get("risk_keys", [])

    factors = [RISK_DESCRIPTIONS.get(k) for k in keys if RISK_DESCRIPTIONS.get(k)]
    actions = [RISK_ACTIONS.get(k) for k in keys if RISK_ACTIONS.get(k)]

    if not factors:
        factors = ["No significant weather risk factors identified."]
    if not actions:
        actions = ["Normal travel precautions are enough."]

    return {
        "destination": normalized_data.get("destination", ""),
        "region": normalized_data.get("region", ""),
        "country": normalized_data.get("country", ""),
        "forecast_days": normalized_data.get("forecast_days", 0),
        "current_weather": normalized_data.get("current_weather", {}),
        "daily_forecast": normalized_data.get("daily_forecast", []),
        "weather_risk": risk,
        "risk_factors": list(dict.fromkeys(factors)),
        "recommended_actions": list(dict.fromkeys(actions)),
        "packing_suggestions": PACKING_SUGGESTIONS.get(risk, []),
        "travel_readiness_advisory": TRAVEL_READINESS.get(risk, ""),
        "weather_risk_explanation": RISK_EXPLANATION.get(risk, ""),
        "resources_used": ["resource://travel/checklist", "resource://travel/advisory-rules", "resource://weather/normalized-forecast-schema"],
        "tools_used": ["validate_city_input_tool", "get_weather_forecast_tool", "normalize_weather_data_tool", "calculate_weather_risk_tool", "save_travel_advisory_tool"],
        "prompts_used": ["travel_readiness_prompt", "weather_risk_summary_prompt", "packing_recommendation_prompt"]
    }