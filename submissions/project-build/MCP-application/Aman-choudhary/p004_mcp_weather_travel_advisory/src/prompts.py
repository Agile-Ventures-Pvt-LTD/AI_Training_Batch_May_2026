from typing import List
def travel_readiness_prompt(destination: str,weather_risk: str,forecast_summary: str,recommended_actions: List[str],) -> str:
    """
    Creates a travel readiness advisory prompt.
    """
    return f"""Create a concise travel-readiness advisory for the destination.
Destination:
{destination}
Forecast Summary:
{forecast_summary}
Weather Risk:
{weather_risk}
Recommended Actions:
{', '.join(recommended_actions)}
Explain whether travel looks comfortable,
manageable with precautions,
or risky due to weather.
Keep the answer practical,
clear,
short,
and easy to understand.
""".strip()
def weather_risk_summary_prompt(destination: str,weather_risk: str,risk_factors: List[str],)-> str:
    """
    Explains why the destination received
    LOW, MEDIUM, or HIGH risk.
    """
    return f"""Explain the weather risk level for the destination.
Destination:
{destination}
Risk Level:
{weather_risk}
Risk Factors:
{', '.join(risk_factors)}
Use simple language and explain
the main reasons behind the assigned
weather risk level.
Focus on traveller safety,
comfort,
and weather conditions.
""".strip()
def packing_recommendation_prompt(destination: str,weather_risk: str,risk_factors: List[str],)-> str:
    """
    Generates practical packing suggestions.
    """
    return f"""Suggest practical packing items
for the destination based on weather risk.
Destination:
{destination}
Risk Level:
{weather_risk}
Risk Factors:
{', '.join(risk_factors)}
Return a short list of useful items
that could help the traveler.
Examples:
- Water bottle
- Umbrella
- Rain jacket
- Sunscreen
- Hat
- Comfortable clothing
Keep suggestions practical,
weather-focused,
and concise.
""".strip()
PROMPTS = {
    "travel_readiness_prompt": travel_readiness_prompt,
    "weather_risk_summary_prompt": weather_risk_summary_prompt,
    "packing_recommendation_prompt": packing_recommendation_prompt,
}
def get_prompt(prompt_name: str):
    """
    Retrieve a prompt by name.
    """
    if prompt_name not in PROMPTS:
        raise ValueError(
            f"Unknown prompt: {prompt_name}"
        )
    return PROMPTS[prompt_name]
def list_prompts() -> list[str]:
    """
    Return all available prompt names.
    Useful for testing.
    """
    return list(PROMPTS.keys())