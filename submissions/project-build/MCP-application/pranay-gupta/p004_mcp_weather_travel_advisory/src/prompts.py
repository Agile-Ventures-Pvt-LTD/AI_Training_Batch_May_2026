def travel_readiness_prompt(destination: str, weather_risk: str, forecast_summary: str = "", recommended_actions: list = None) -> str:
    actions_str = "; ".join(recommended_actions) if recommended_actions else "None"
    return f"""Create a concise travel-readiness advisory for the destination.
            Destination: {destination}
            Forecast Summary: {forecast_summary}
            Weather Risk: {weather_risk}
            Recommended Actions: {actions_str}

            Explain whether travel looks comfortable, manageable with precautions, or risky due to weather.
            Keep the answer practical and easy to understand.
            """

def weather_risk_summary_prompt(destination: str, weather_risk: str, risk_factors: list = None) -> str:
    factors_str = "; ".join(risk_factors) if risk_factors else "None"
    return f"""Explain the weather risk level for the destination.

            Destination: {destination}
            Risk Level: {weather_risk}
            Risk Factors: {factors_str}

            Use simple language and explain the main reason behind the risk level.
            """

def packing_recommendation_prompt(destination: str, weather_risk: str, risk_factors: list = None) -> str:
    factors_str = "; ".join(risk_factors) if risk_factors else "None"
    return f"""Suggest practical packing items for the destination based on the weather risk.

            Destination: {destination}
            Risk Level: {weather_risk}
            Risk Factors: {factors_str}

            Return a short list of useful packing suggestions.
            """

ALL_PROMPTS = ["travel_readiness_prompt","weather_risk_summary_prompt","packing_recommendation_prompt"]