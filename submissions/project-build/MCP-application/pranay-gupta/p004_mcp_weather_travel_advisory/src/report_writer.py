from resources import ALL_RESOURCES
from prompts import ALL_PROMPTS

TOOLS_USED = ["validate_city_input_tool","get_weather_forecast_tool","normalize_weather_data_tool","calculate_weather_risk_tool",
              "save_travel_advisory_tool"]

def generate_forecast_summary(normalized_data: dict) -> str:
    try:
        dest = normalized_data.get("destination", "the destination")
        days = normalized_data.get("forecast_days", 0)
        current = normalized_data.get("current_weather", {})
        daily = normalized_data.get("daily_forecast", [])

        temp = current.get("temperature_c", 0)
        desc = current.get("weather_description", "Unknown")

        if daily:
            all_max = [d.get("max_temp_c", 0) for d in daily]
            all_min = [d.get("min_temp_c", 0) for d in daily]
            overall_max = max(all_max) if all_max else 0
            overall_min = min(all_min) if all_min else 0
            return f"{days}-day forecast for {dest}: Temperatures ranging from {overall_min}°C to {overall_max}°C. Current conditions: {desc}, {temp}°C."
        return f"Current conditions in {dest}: {desc}, {temp}°C."
    except Exception:
        return "Forecast summary unavailable."

def generate_travel_readiness_advisory(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: list) -> str:
    actions_text = " ".join(recommended_actions) if recommended_actions else "No specific actions needed."
    if weather_risk == "LOW":
        return f"Travel to {destination} looks comfortable based on the current weather forecast. {forecast_summary} Normal travel precautions are sufficient. Recommended: {actions_text}"
    elif weather_risk == "MEDIUM":
        return f"Travel to {destination} appears manageable with basic weather precautions. {forecast_summary} {actions_text}"
    elif weather_risk == "HIGH":
        return f"Travel to {destination} may be risky due to adverse weather conditions. {forecast_summary} Consider postponing non-essential outdoor travel or take extra caution. {actions_text}"
    return f"Travel advisory for {destination}: Please review the weather forecast before traveling."

def generate_weather_risk_explanation(destination: str, weather_risk: str, risk_factors: list) -> str:
    factors_text = " ".join(risk_factors) if risk_factors else "No specific risk factors identified."
    if weather_risk == "LOW":
        return f"The risk level for {destination} is LOW because no major heat, rain, or wind indicators were detected in the forecast. {factors_text}"
    elif weather_risk == "MEDIUM":
        return f"The risk level for {destination} is MEDIUM because moderate weather indicators are present in the forecast. {factors_text} Travel is possible but requires basic precautions."
    elif weather_risk == "HIGH":
        return f"The risk level for {destination} is HIGH because severe weather conditions were detected in the forecast. {factors_text} The traveler should reconsider non-essential outdoor travel or plan with extra caution."
    return f"Weather risk for {destination}: {weather_risk}. {factors_text}"

def generate_packing_suggestions(destination: str, weather_risk: str, risk_factors: list) -> list:
    suggestions = []
    factors_combined = " ".join(risk_factors).lower() if risk_factors else ""

    if "heat" in factors_combined or "temperature" in factors_combined or "35°c" in factors_combined or "40°c" in factors_combined:
        suggestions.extend(["Water bottle", "Sunscreen", "Cap or hat", "Light cotton clothing"])
    if "rain" in factors_combined or "precipitation" in factors_combined:
        suggestions.extend(["Umbrella", "Waterproof jacket", "Waterproof shoes"])
    if "wind" in factors_combined:
        suggestions.extend(["Windbreaker", "Secure loose items"])
        
    suggestions.extend(["Phone charger", "Essential documents"])

    seen = set()
    unique_suggestions = []
    for item in suggestions:
        if item not in seen:
            seen.add(item)
            unique_suggestions.append(item)

    if weather_risk == "LOW" and len(unique_suggestions) <= 2:
        unique_suggestions = ["Comfortable clothing", "Phone charger", "Essential documents"]

    return unique_suggestions

def assemble_report(normalized_data: dict, risk_result: dict) -> dict:
    destination = normalized_data.get("destination", "Unknown")
    weather_risk = risk_result.get("weather_risk", "LOW")
    risk_factors = risk_result.get("risk_factors", [])
    recommended_actions = risk_result.get("recommended_actions", [])

    forecast_summary = generate_forecast_summary(normalized_data)

    travel_readiness_advisory = generate_travel_readiness_advisory(
        destination=destination,
        weather_risk=weather_risk,
        forecast_summary=forecast_summary,
        recommended_actions=recommended_actions
    )

    weather_risk_explanation = generate_weather_risk_explanation(
        destination=destination,
        weather_risk=weather_risk,
        risk_factors=risk_factors
    )

    packing_suggestions = generate_packing_suggestions(
        destination=destination,
        weather_risk=weather_risk,
        risk_factors=risk_factors
    )

    return {
        "destination": destination,
        "region": normalized_data.get("region", ""),
        "country": normalized_data.get("country", ""),
        "forecast_days": normalized_data.get("forecast_days", 0),
        "current_weather": normalized_data.get("current_weather", {}),
        "daily_forecast": normalized_data.get("daily_forecast", []),
        "weather_risk": weather_risk,
        "risk_factors": risk_factors,
        "recommended_actions": recommended_actions,
        "packing_suggestions": packing_suggestions,
        "travel_readiness_advisory": travel_readiness_advisory,
        "weather_risk_explanation": weather_risk_explanation,
        "resources_used": list(ALL_RESOURCES),
        "tools_used": list(TOOLS_USED),
        "prompts_used": list(ALL_PROMPTS)
    }