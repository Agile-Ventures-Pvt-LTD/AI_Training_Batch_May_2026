from mcp.server.fastmcp import FastMCP
from tools import (validate_city_input_tool,get_weather_forecast_tool,normalize_weather_data_tool,calculate_weather_risk_tool,save_travel_advisory_tool,)
from resources import (TRAVEL_CHECKLIST,ADVISORY_RULES,NORMALIZED_FORECAST_SCHEMA,)
from prompts import (travel_readiness_prompt,weather_risk_summary_prompt,packing_recommendation_prompt,)
mcp = FastMCP(name="weather-travel-advisory-server",)
@mcp.tool()
def validate_city(city_name: str) -> dict:
    """
    Validate and normalize city name.
    """
    return validate_city_input_tool(city_name)
@mcp.tool()
def get_weather_forecast(normalized_city_name: str) -> dict:
    """
    Fetch weather from wttr.in API.
    """
    return get_weather_forecast_tool(normalized_city_name)
@mcp.tool()
def normalize_weather(raw_weather_data: dict) -> dict:
    """
    Convert wttr.in payload into normalized schema.
    """
    return normalize_weather_data_tool(raw_weather_data)
@mcp.tool()
def calculate_weather_risk(normalized_weather_data: dict) -> dict:
    """
    Calculate deterministic weather risk.
    """
    return calculate_weather_risk_tool(normalized_weather_data)
@mcp.tool()
def save_travel_advisory(report: dict) -> dict:
    """
    Save advisory report to JSON file.
    """
    return save_travel_advisory_tool(report)
@mcp.resource("resource://travel/checklist")
def travel_checklist() -> str:
    """
    Static travel readiness checklist.
    """
    return TRAVEL_CHECKLIST
@mcp.resource("resource://travel/advisory-rules")
def advisory_rules() -> str:
    """
    Static weather advisory rules.
    """
    return ADVISORY_RULES

@mcp.resource("resource://weather/normalized-forecast-schema")
def normalized_forecast_schema() -> dict:
    """
    Normalized forecast schema reference.
    """
    return NORMALIZED_FORECAST_SCHEMA
@mcp.prompt()
def travel_readiness(destination: str,weather_risk: str,forecast_summary: str,recommended_actions: list[str],) -> str:
    """
    Travel readiness advisory prompt.
    """
    return travel_readiness_prompt(destination=destination,weather_risk=weather_risk,forecast_summary=forecast_summary,recommended_actions=recommended_actions,)
@mcp.prompt()
def weather_risk_summary(destination: str,weather_risk: str,risk_factors: list[str],) -> str:
    """
    Weather risk explanation prompt.
    """
    return weather_risk_summary_prompt(destination=destination,weather_risk=weather_risk,risk_factors=risk_factors,)
@mcp.prompt()
def packing_recommendation(destination: str,weather_risk: str,risk_factors: list[str],) -> str:
    """
    Packing recommendation prompt.
    """
    return packing_recommendation_prompt(destination=destination,weather_risk=weather_risk,risk_factors=risk_factors,)

if __name__ == "__main__":
    print("Starting Weather & Travel Advisory MCP Server.")
    mcp.run()