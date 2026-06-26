TRAVEL_READINESS_PROMPT = """
Destination: {destination}
Forecast Summary: {forecast_summary}
Weather Risk: {weather_risk}
Recommended Actions:
{recommended_actions}

Explain whether travel looks comfortable, manageable with precautions, or risky due to weather.
Keep the answer practical and easy to understand.
"""

WEATHER_RISK_SUMMARY_PROMPT = """
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors:
{risk_factors}

Use simple language and explain the main reason behind the risk level.
"""

PACKING_RECOMMENDATION_PROMPT = """
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors:
{risk_factors}

Return a short list of useful packing suggestions.
"""


RISK_DESCRIPTIONS = {
    "heat_high": "Maximum temperature is expected to be above 40.C.",
    "heat_moderate": "Maximum temperature is expected to be above 35.C.",
    "rain_high": "Heavy precipitation expected.",
    "rain_moderate": "Moderate precipitation expected during.",
    "rain_chance_high": "High chance of rain during the forecast period.",
    "rain_chance_moderate": "Chance of rain may increase during the forecast period.",
    "wind_high": "High wind speeds expected during the forecast period.",
    "wind_moderate": "Wind speed may be moderately high during the forecast period.",
}

RISK_ACTIONS = {
    "heat_high": "Avoid outdoor exposure during high heat hours.",
    "heat_moderate": "Carry water and avoid long outdoor during afternoon.",
    "rain_high": "Avoid outdoor travel during heavy rainfall.",
    "rain_moderate": "Carry an umbrella or raincoat.",
    "rain_chance_high": "Plan indoor activities and carry rain protection.",
    "rain_chance_moderate": "Carry an umbrella or raincoat",
    "wind_high": "Avoid exposed outdoor areas during high wind conditions.",
    "wind_moderate": "Avoid exposed outdoor areas during high wind conditions.",
}

PACKING_SUGGESTIONS = {
    "HIGH": ["Water bottle", "Umbrella", "First aid kit", "Flashlight", "Power bank"],
    "MEDIUM": ["Water bottle", "Light cotton clothing", "Sunscreen", "Cap or hat"],
    "LOW": ["Light clothing", "Sunscreen", "Comfortable walking shoes"],
}

TRAVEL_READINESS = {
    "HIGH": "Travel is risky due to severe weather conditions. Consider postponing non-essential travel.",
    "MEDIUM": "Travel appears manageable with basic weather precautions.",
    "LOW": "Travel looks comfortable with no significant weather concerns.",
}

RISK_EXPLANATION = {
    "HIGH": "The risk level is high because severe heat, rain, or wind conditions are present.",
    "MEDIUM": "The risk level is medium because moderate heat, rain, or wind indicators are present.",
    "LOW": "The risk level is low because no major weather risk factors are present.",
}


def register_prompts(mcp):
    @mcp.prompt()
    def travel_readiness(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: list) -> str:
        return TRAVEL_READINESS_PROMPT.format(destination=destination, weather_risk=weather_risk,
                                               forecast_summary=forecast_summary,
                                               recommended_actions="\n".join(f"- {a}" for a in recommended_actions))

    @mcp.prompt()
    def weather_risk_summary(destination: str, weather_risk: str, risk_factors: list) -> str:
        return WEATHER_RISK_SUMMARY_PROMPT.format(destination=destination, weather_risk=weather_risk,
                                                   risk_factors="\n".join(f"- {f}" for f in risk_factors))

    @mcp.prompt()
    def packing_recommendation(destination: str, weather_risk: str, risk_factors: list) -> str:
        return PACKING_RECOMMENDATION_PROMPT.format(destination=destination, weather_risk=weather_risk,
                                                     risk_factors="\n".join(f"- {f}" for f in risk_factors))