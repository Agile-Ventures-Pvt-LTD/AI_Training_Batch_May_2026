TRAVEL_READINESS_PROMPT = """Create a concise travel-readiness advisory for the destination.
Destination: {destination}
Forecast Summary: {forecast_summary}
Weather Risk: {weather_risk}
Recommended Actions: {recommended_actions}

Explain whether travel looks comfortable, manageable with precautions, or risky due to weather.
Keep the answer practical and easy to understand."""

WEATHER_RISK_SUMMARY_PROMPT = """Explain the weather risk level for the destination.
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors: {risk_factors}

Use simple language and explain the main reason behind the risk level."""

PACKING_RECOMMENDATION_PROMPT = """Suggest practical packing items for the destination based on the weather risk.
Destination: {destination}
Risk Level: {weather_risk}
Risk Factors: {risk_factors}

Return a short list of useful packing suggestions."""

def format_prompt(prompt_type: str, data: dict) -> str:
    """Formats prompt templates with string metadata fields safely."""
    templates = {
        "travel_readiness_prompt": TRAVEL_READINESS_PROMPT,
        "weather_risk_summary_prompt": WEATHER_RISK_SUMMARY_PROMPT,
        "packing_recommendation_prompt": PACKING_RECOMMENDATION_PROMPT
    }
    template = templates.get(prompt_type)
    if not template:
        raise ValueError(f"Prompt type '{prompt_type}' not found.")
    return template.format(**data)
