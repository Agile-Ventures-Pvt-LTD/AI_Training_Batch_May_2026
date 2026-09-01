from typing import Dict
from tools import save_travel_advisory_tool

def save_report(normalized_weather, risk_info, travel_readiness_advisory, weather_risk_explanation, packing_suggestions):
    report = {
        "destination": normalized_weather.get("destination"),
        "region": normalized_weather.get("region"),
        "country": normalized_weather.get("country"),
        "forecast_days": normalized_weather.get("forecast_days", 3),
        "current_weather": normalized_weather.get("current_weather"),
        "daily_forecast": normalized_weather.get("daily_forecast"),
        "weather_risk": risk_info.get("weather_risk"),
        "risk_factors": risk_info.get("risk_factors"),
        "recommended_actions": risk_info.get("recommended_actions"),
        "packing_suggestions": packing_suggestions,
        "travel_readiness_advisory": travel_readiness_advisory,
        "weather_risk_explanation": weather_risk_explanation,
        "resources_used": [
            "resource://travel/checklist",
            "resource://travel/advisory-rules",
            "resource://weather/normalized-forecast-schema"
        ],
        "tools_used": [
            "validate_city_input_tool",
            "get_weather_forecast_tool",
            "normalize_weather_data_tool",
            "calculate_weather_risk_tool",
            "save_travel_advisory_tool"
        ],
        "prompts_used": [
            "travel_readiness_prompt",
            "weather_risk_summary_prompt",
            "packing_recommendation_prompt"
        ]
    }
    
    return save_travel_advisory_tool(report)
