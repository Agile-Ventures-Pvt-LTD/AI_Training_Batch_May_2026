import json
from fastmcp import FastMCP
from pydantic import ValidationError
from prompts import packing_recommendation, travel_readiness, weather_risk_summary
from report_writer import save_travel_advisory
from tools import (
    validate_city_input,
    get_weather_from_wttr,
    normalize_weather_data,
    assess_weather_risk,
)
from resources import (
    travel_checklist,
    travel_advisory_rules,
    weather_normalized_forecast_schema
)
from schemas import CityInput, CityOutput


mcp = FastMCP("Weather MCP")


@mcp.tool()
async def validate_city_input_tool(city_name: str) -> dict:
    """
    Validates and normalizes a city name for API usage.
    """
    
    try:
        input_data = CityInput(city_name=city_name)
        result = validate_city_input(input_data)
        return result.dict()
    except ValidationError as e:
        return CityOutput(success=False, message=str(e)).dict()
    

@mcp.tool()
async def get_weather_forecast_tool(normalized_city_name: str) -> dict:
    """
    Call the weather forecast for the weather information of that city.
    """
    
    return get_weather_from_wttr(normalized_city_name)


@mcp.tool()
async def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
    """
    Converts raw JSON into a clean internal weather schema.
    """
    
    return normalize_weather_data(raw_weather_data)


@mcp.tool()
async def assess_weather_risk_tool(normalized_weather_data: dict) -> dict:
    """
    Analyises the weather risk based on normalized weather data.
    """
   
    return assess_weather_risk(normalized_weather_data)


@mcp.tool()
async def save_travel_advisory_tool(report) -> dict:
    """
    Saves the final travel advisory report as JSON.
    """
    
    return save_travel_advisory(report)


@mcp.resource("resource://travel/checklist")
async def travel_checklist_resource() -> str:
    """
    Show the Travel Checklist when someone ask for it 
    """

    return travel_checklist()


@mcp.resource("resource://travel/advisory-rules")
async def travel_advisory_rules_resource() -> str:
    """
    Rules for interpreting weather risk levels.
    """

    return travel_advisory_rules()


@mcp.resource("resource://weather/normalized-forecast-schema")
async def weather_normalized_forecast_schema_resource() -> dict:
    """
    Normalized forecast schema expected by this project.
    """

    return weather_normalized_forecast_schema()


@mcp.prompt("travel_readiness_prompt")
async def travel_readiness_prompt(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: list) -> str:
    """
    Travel readiness advisory For the destination.
    """

    result = travel_readiness(destination, weather_risk, forecast_summary, recommended_actions)

    return result


@mcp.prompt("weather_risk_summary_prompt")
async def weather_risk_summary_prompt(destination: str, weather_risk: str, risk_factors: list) -> str:
    """
    Explain the weather risk level is LOW, MEDIUM, or HIGH.
    """

    return weather_risk_summary(destination, weather_risk, risk_factors)


@mcp.prompt("packing_recommendation_prompt")
async def packing_recommendation_prompt(destination: str, weather_risk: str, risk_factors: list) -> str:
    """
    Suggest the Pratical packing items for the destination based on the weather risk. 
    """

    return packing_recommendation(destination, weather_risk, risk_factors)


if __name__ == "__main__":
    mcp.run("streamable-http", port=8001)