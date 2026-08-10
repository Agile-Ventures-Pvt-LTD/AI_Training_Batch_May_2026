# src/schemas.py
def get_normalized_schema():
    return {
        "destination": "string",
        "region": "string",
        "country": "string",
        "forecast_days": "number",
        "current_weather": {
            "temperature_c": "number",
            "humidity": "number",
            "precipitation_mm": "number",
            "wind_speed_kmph": "number",
            "weather_description": "string"
        },
        "daily_forecast": [
            {
                "date": "string",
                "max_temp_c": "number",
                "min_temp_c": "number",
                "avg_temp_c": "number",
                "total_precipitation_mm": "number",
                "max_wind_kmph": "number",
                "max_chance_of_rain": "number",
                "weather_description": "string"
            }
        ]
    }

def get_final_report_schema():
    return {
        "destination": "",
        "region": "",
        "country": "",
        "forecast_days": 3,
        "current_weather": {
            "temperature_c": 0,
            "humidity": 0,
            "precipitation_mm": 0,
            "wind_speed_kmph": 0,
            "weather_description": ""
        },
        "daily_forecast": [],
        "weather_risk": "LOW | MEDIUM | HIGH",
        "risk_factors": [],
        "recommended_actions": [],
        "packing_suggestions": [],
        "travel_readiness_advisory": "",
        "weather_risk_explanation": "",
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