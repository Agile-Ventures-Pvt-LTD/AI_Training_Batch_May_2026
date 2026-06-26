from fastmcp import FastMCP

from src.tools import (
    validate_city_input_tool,
    get_weather_forecast_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool,
    save_travel_advisory_tool
)

from src.resources import (
    get_checklist,
    get_advisory_rules,
    get_schema
)

mcp = FastMCP("weather-travel-advisory")


# ---------------- TOOLS ---------------- #

@mcp.tool()
def validate_city_input_tool_wrapper(input_data: dict):
    return validate_city_input_tool(input_data)


@mcp.tool()
def get_weather_forecast_tool_wrapper(input_data: dict):
    return get_weather_forecast_tool(input_data)


@mcp.tool()
def normalize_weather_data_tool_wrapper(input_data: dict):
    return normalize_weather_data_tool(input_data)


@mcp.tool()
def calculate_weather_risk_tool_wrapper(input_data: dict):
    return calculate_weather_risk_tool(input_data)


@mcp.tool()
def save_travel_advisory_tool_wrapper(input_data: dict):
    return save_travel_advisory_tool(input_data)


# ---------------- RESOURCES ---------------- #

@mcp.resource("resource://travel/checklist")
def checklist():
    return get_checklist()


@mcp.resource("resource://travel/advisory-rules")
def rules():
    return get_advisory_rules()


@mcp.resource("resource://weather/normalized-forecast-schema")
def schema():
    return get_schema()


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    mcp.run()   # ✅ stdio transport