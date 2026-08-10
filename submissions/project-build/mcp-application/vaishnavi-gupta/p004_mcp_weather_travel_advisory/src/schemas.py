{
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
 "daily_forecast": [
 {
 "date": "",
 "max_temp_c": 0,
 "min_temp_c": 0,
 "avg_temp_c": 0,
 "total_precipitation_mm": 0,
 "max_wind_kmph": 0,
 "max_chance_of_rain": 0,
 "weather_description": ""
 }
 ],
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
