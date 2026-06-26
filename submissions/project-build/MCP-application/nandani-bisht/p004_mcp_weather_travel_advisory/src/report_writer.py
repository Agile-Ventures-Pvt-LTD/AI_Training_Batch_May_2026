def generate_final_report(
    normalized_data: dict,
    risk_data: dict,
    packing_suggestions: list,
    travel_readiness_advisory: str,
    weather_risk_explanation: str
) -> dict:
    return {
        "destination": normalized_data["destination"],
        "region": normalized_data["region"],
        "country": normalized_data["country"],
        "forecast_days": normalized_data["forecast_days"],
        "current_weather": normalized_data["current_weather"],
        "daily_forecast": normalized_data["daily_forecast"],
        "weather_risk": risk_data["weather_risk"],
        "risk_factors": risk_data["risk_factors"],
        "recommended_actions": risk_data["recommended_actions"],
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
    