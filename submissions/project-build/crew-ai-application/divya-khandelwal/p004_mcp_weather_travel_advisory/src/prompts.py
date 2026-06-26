def travel_readiness_prompt(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: list) -> str:
    """Compiles a reusable structure providing descriptive analysis context to the agent."""

    actions_str = "\n".join([f"{a}" for a in recommended_actions])
    return f"""Create a concise travel-readiness advisory for the destination.

    Destination: {destination}
    Forecast Summary: {forecast_summary}
    Weather Risk: {weather_risk}
    Recommended Actions: 
    {actions_str}

    Explain whether travel looks comfortable, manageable with precautions, or risky due to weather.
    Keep the answer practical and easy to understand."""

def weather_risk_summary_prompt(destination: str, weather_risk: str, risk_factors: list) -> str:
    """Compiles analytical justifications for defined risk limits."""

    factors_str = "\n".join([f"{f}" for f in risk_factors])
    return f"""Explain the weather risk level for the destination.

    Destination: {destination}
    Risk Level: {weather_risk}
    Risk Factors:
    {factors_str}

    Use simple language and explain the main reason behind the risk level."""

def packing_recommendation_prompt(destination: str, weather_risk: str, risk_factors: list) -> str:
    """Compiles instructions to generate practical travel preparations."""

    factors_str = "\n".join([f"{f}" for f in risk_factors])
    return f"""Suggest practical packing items for the destination based on the weather risk.

    Destination: {destination}
    Risk Level: {weather_risk}
    Risk Factors:
    {factors_str}

    Return a short list of useful packing suggestions."""
