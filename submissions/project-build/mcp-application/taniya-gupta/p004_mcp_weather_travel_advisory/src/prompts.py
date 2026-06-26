def get_travel_readiness(destination, weather_risk, forecast_summary, recommended_actions):
    return f"""Create a concise travel-readiness advisory for the destination.

Destination: {destination}
Forecast Summary: {forecast_summary}
Weather Risk: {weather_risk}
Recommended Actions: {recommended_actions}

Explain whether travel looks comfortable, manageable with precautions, or risky due to weather.
Keep the answer practical and easy to understand."""

def get_weather_risk_summary(destination, weather_risk, risk_factors):
    return f"""
Explain the weather risk level for the destination.
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors: {risk_factors}
Use simple language and explain the main reason behind the risk level.

"""

def get_packing_recommendation(destination, weather_risk, risk_factors):
    return f"""
Suggest practical packing items for the destination based on the
weather risk.
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors: {risk_factors}
Return a short list of useful packing suggestions.
"""