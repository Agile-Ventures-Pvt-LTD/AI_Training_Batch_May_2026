from prompts import travel_readiness_prompt, weather_risk_summary_prompt, packing_recommendation_prompt

def final_report(normal_data: dict, risk_data: dict) -> dict:
    dest = normal_data["destination"]
    risk = risk_data["weather_risk"]
    factors = risk_data["risk_factors"]
    actions = risk_data["recommended_actions"]
    
    if risk == "LOW":
        advisory_text = "Travel looks comfortable"
        explanation_text = "The risk level is low because weather seems good"
        packing = ["Standard clothing", "Personal items", "Travel documents"]
    elif risk == "MEDIUM":
        advisory_text = "Travel appears manageable"
        explanation_text = f"The risk level is medium"
        packing = ["Umbrella", "Water bottle", "Sunscreen", "Light adaptable layers"]
    else:
        advisory_text = "Travel conditions are risky due to severe weather"
        explanation_text = f"The risk level is high due to the severe weather factors"
        packing = ["Heavy rain gear", "Emergency contact list", "Waterproof coverings"]

    return {"destination": dest,"region": normal_data["region"],"country": normal_data["country"],"forecast_days": normal_data["forecast_days"],"current_weather": normal_data["current_weather"],"daily_forecast": normal_data["daily_forecast"],"weather_risk": risk,"risk_factors": factors,"recommended_actions": actions,"packing_suggestions": packing,"travel_readiness_advisory": advisory_text,"weather_risk_explanation": explanation_text,
        "resources_used": ["resource://travel/checklist","resource://travel/advisory-rules","resource://weather/normalized-forecast-schema"],
        "tools_used": ["validate_city_input_tool","get_weather_forecast_tool","normalize_weather_data_tool","calculate_weather_risk_tool","save_travel_advisory_tool"],
        "prompts_used": ["travel_readiness_prompt","weather_risk_summary_prompt","packing_recommendation_prompt"]}
