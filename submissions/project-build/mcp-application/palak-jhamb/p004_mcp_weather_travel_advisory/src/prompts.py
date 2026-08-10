from mcp_use.server import MCPRouter

router = MCPRouter()

@router.prompt()
async def travel_readiness_prompt(destination: str, weather_risk: str, forecast_summary: str,recommended_actions:list) -> str:
    """
    Analyze the job market for top {num_jobs} jobs for '{role}' in '{location}'.
    """

   
    return f"""Create a concise travel-readiness advisory for the destination.
            Destination: {destination}
            Forecast Summary: {forecast_summary}
            Weather Risk: {weather_risk}
            Recommended Actions: {recommended_actions}

            Explain whether travel looks comfortable, manageable with precautions, 
            or risky due to weather.
            Keep the answer practical and easy to understand."""

@router.prompt()
async def weather_risk_summary_prompt(destination:str,weather_risk:str,risk_factors:list)-> str:
    """Explains why the risk level is LOW, MEDIUM, or HIGH"""
    return f"""
        Explain the weather risk level for the destination.
        Destination: {destination}
        Risk Level: {weather_risk}
        Risk Factors: {risk_factors}
        Use simple language and explain the main reason behind the risk level."""


@router.prompt()
async def packing_recommendation_prompt(destination:str,weather_risk:str,risk_factors:list)->str:
    """Generates practical packing suggestions"""
    return f"""Suggest practical packing items for the destination based on the weather risk.
        Destination: {destination}
        Risk Level: {weather_risk}
        Risk Factors: {risk_factors}
        Return a short list of useful packing suggestions."""