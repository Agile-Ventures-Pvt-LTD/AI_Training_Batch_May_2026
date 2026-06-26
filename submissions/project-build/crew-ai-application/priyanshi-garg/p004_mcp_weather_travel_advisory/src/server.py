import json
from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("Weather Travel Advisory Server Pipeline")

from tools import (
    validate_city_input_tool as run_validate,
    get_weather_forecast_tool as run_fetch,
    normalize_weather_data_tool as run_normalize,
    calculate_weather_risk_tool as run_risk,
    save_travel_advisory_tool as run_save
)
from resources import RESOURCES
from prompts import TRAVEL_READINESS_PROMPT, WEATHER_RISK_SUMMARY_PROMPT, PACKING_RECOMMENDATION_PROMPT # FIXED: Pointed to 'prompts'


@mcp_server.tool(name="validate_city_input_tool")
def validate_city_input_tool(city_name: str) -> str:
    """Validates and cleans incoming raw user city strings."""
    return run_validate(city_name)

@mcp_server.tool(name="get_weather_forecast_tool")
def get_weather_forecast_tool(normalized_city_name: str) -> str:
    """Fetches real-time structured weather matrices via endpoint paths."""
    return run_fetch(normalized_city_name)

@mcp_server.tool(name="normalize_weather_data_tool")
def normalize_weather_data_tool(raw_weather_data_json: str) -> str:
    """Normalizes raw payload configurations into uniform internal profiles."""
    return run_normalize(json.loads(raw_weather_data_json))

@mcp_server.tool(name="calculate_weather_risk_tool")
def calculate_weather_risk_tool(normalized_weather_data_json: str) -> str:
    """Calculates factual risk metrics dynamically via algorithm layers."""
    return run_risk(json.loads(normalized_weather_data_json))

@mcp_server.tool(name="save_travel_advisory_tool")
def save_travel_advisory_tool(report_json: str) -> str:
    """Saves finalized data schemas structurally onto local disk paths."""
    return run_save(json.loads(report_json))

@mcp_server.resource("resource://travel/checklist")
def get_travel_checklist() -> str:
    return RESOURCES["resource://travel/checklist"]

@mcp_server.resource("resource://travel/advisory-rules")
def get_travel_advisory_rules() -> str:
    return RESOURCES["resource://travel/advisory-rules"]

@mcp_server.resource("resource://weather/normalized-forecast-schema")
def get_weather_forecast_schema() -> str:
    return json.dumps(RESOURCES["resource://weather/normalized-forecast-schema"], indent=2)


@mcp_server.prompt("travel_readiness_prompt")
def mcp_travel_readiness_prompt(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: str) -> str:
    return TRAVEL_READINESS_PROMPT.format(
        destination=destination, weather_risk=weather_risk,
        forecast_summary=forecast_summary, recommended_actions=recommended_actions
    )

@mcp_server.prompt("weather_risk_summary_prompt")
def mcp_weather_risk_summary_prompt(destination: str, weather_risk: str, risk_factors: str) -> str:
    return WEATHER_RISK_SUMMARY_PROMPT.format(
        destination=destination, weather_risk=weather_risk, risk_factors=risk_factors
    )

@mcp_server.prompt("packing_recommendation_prompt")
def mcp_packing_recommendation_prompt(destination: str, weather_risk: str, risk_factors: str) -> str:
    return PACKING_RECOMMENDATION_PROMPT.format(
        destination=destination, weather_risk=weather_risk, risk_factors=risk_factors
    )

if __name__ == "__main__":
    mcp_server.run()
