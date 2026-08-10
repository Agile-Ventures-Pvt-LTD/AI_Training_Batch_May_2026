def travel_readiness_prompt(
    destination: str,
    weather_risk: str,
    forecast_summary: str,
    recommended_actions: list[str],
) -> str:
    return f"""
    Create a concise travel-readiness advisory.

    Destination: {destination}

    Forecast Summary:
    {forecast_summary}

    Weather Risk:
    {weather_risk}

    Recommended Actions:
    {recommended_actions}

    Explain whether travel looks comfortable,
    manageable with precautions,
    or risky due to weather.

    Keep the answer practical and easy to understand.
    """.strip()


def weather_risk_summary_prompt(
    destination: str,
    weather_risk: str,
    risk_factors: list[str],
) -> str:
    return f"""
    Explain the weather risk level.

    Destination: {destination}

    Risk Level: {weather_risk}

    Risk Factors:
    {risk_factors}

    Use simple language to explain why this risk level was assigned.
    """.strip()


def packing_recommendation_prompt(
    destination: str,
    weather_risk: str,
    risk_factors: list[str],
) -> str:
    return f"""
    Suggest practical packing items.

    Destination: {destination}

    Risk Level: {weather_risk}

    Risk Factors:
    {risk_factors}

    Return only a short bullet list of useful packing items.
    """.strip()