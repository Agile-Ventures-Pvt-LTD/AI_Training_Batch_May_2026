TRAVEL_READINESS_TEMPLATE = """Create a concise travel-readiness advisory for the destination.
Destination: {destination}
Forecast Summary: {forecast_summary}
Weather Risk: {weather_risk}
Recommended Actions: {recommended_actions}
Explain whether travel looks comfortable, manageable with precautions, or risky due to weather.
Keep the answer practical and easy to understand."""

WEATHER_RISK_SUMMARY_TEMPLATE = """Explain the weather risk level for the destination.
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors: {risk_factors}
Use simple language and explain the main reason behind the risk level."""

PACKING_RECOMMENDATION_TEMPLATE = """Suggest practical packing items for the destination based on the weather risk.
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors: {risk_factors}
Return a short list of useful packing suggestions."""

def format_travel_readiness(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: list) -> str:
    actions_str = ", ".join(recommended_actions) if isinstance(recommended_actions, list) else str(recommended_actions)
    return TRAVEL_READINESS_TEMPLATE.format(
        destination=destination,
        weather_risk=weather_risk,
        forecast_summary=forecast_summary,
        recommended_actions=actions_str
    )

def format_weather_risk_summary(destination: str, weather_risk: str, risk_factors: list) -> str:
    factors_str = ", ".join(risk_factors) if isinstance(risk_factors, list) else str(risk_factors)
    return WEATHER_RISK_SUMMARY_TEMPLATE.format(
        destination=destination,
        weather_risk=weather_risk,
        risk_factors=factors_str
    )

def format_packing_recommendation(destination: str, weather_risk: str, risk_factors: list) -> str:
    factors_str = ", ".join(risk_factors) if isinstance(risk_factors, list) else str(risk_factors)
    return PACKING_RECOMMENDATION_TEMPLATE.format(
        destination=destination,
        weather_risk=weather_risk,
        risk_factors=factors_str
    )

def generate_heuristic_travel_readiness(destination: str, weather_risk: str, risk_factors: list) -> str:
    if weather_risk == "HIGH":
        return f"Travel to {destination} is currently risky due to severe weather conditions. Non-essential outdoor activities should be reconsidered or planned with extreme caution."
    elif weather_risk == "MEDIUM":
        return f"Travel to {destination} appears manageable with basic weather precautions. Please monitor the local weather and adjust outdoor plans accordingly."
    else:
        return f"Travel to {destination} looks highly comfortable. No major weather risks are expected during the forecast period."

def generate_heuristic_weather_risk_explanation(destination: str, weather_risk: str, risk_factors: list) -> str:
    factors_desc = " and ".join(risk_factors) if risk_factors else "no negative weather indicators"
    if weather_risk == "HIGH":
        return f"The risk level is high because of: {factors_desc}. These conditions may impact outdoor safety and transit."
    elif weather_risk == "MEDIUM":
        return f"The risk level is medium because of: {factors_desc}. Basic safety measures will keep your travel plans safe."
    else:
        return f"The risk level is low because there are no significant heat, rain, or wind concerns forecast."

def generate_heuristic_packing_suggestions(weather_risk: str, risk_factors: list) -> list:
    suggestions = ["Standard clothing", "Mobile charger", "Personal toiletries", "First-aid kit"]
    factors_str = "".join(risk_factors).lower()
    
    if "heat" in factors_str or "temperature" in factors_str or "35" in factors_str or "40" in factors_str:
        suggestions.extend(["Water bottle", "Light cotton clothing", "Sunscreen", "Cap or hat", "Sunglasses"])
    if "rain" in factors_str or "precipitation" in factors_str or "wet" in factors_str:
        suggestions.extend(["Umbrella", "Raincoat", "Waterproof footwear", "Ziploc bags for electronics"])
    if "wind" in factors_str:
        suggestions.extend(["Windcheater or light jacket", "Dust mask or scarf", "Eye protection"])
        
    seen = set()
    deduped = []
    for item in suggestions:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
            
    return deduped[:6]
