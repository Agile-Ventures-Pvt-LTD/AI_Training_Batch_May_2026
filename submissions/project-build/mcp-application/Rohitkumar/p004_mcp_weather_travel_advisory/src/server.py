import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from src.tools import validate_city_input_tool, get_weather_forecast_tool, normalize_weather_data_tool, calculate_weather_risk_tool, save_travel_advisory_tool
from src.resources import register_resources
from src.prompts import register_prompts
from src.report_writer import generate_report

mcp = FastMCP("Weather Travel Advisory")

register_resources(mcp)
register_prompts(mcp)


@mcp.tool()
def validate_city_input(city_name: str) -> dict:
    return validate_city_input_tool(city_name)


@mcp.tool()
def get_weather_forecast(normalized_city_name: str) -> dict:
    return get_weather_forecast_tool(normalized_city_name)


@mcp.tool()
def normalize_weather_data(raw_weather_data: dict) -> dict:
    return normalize_weather_data_tool(raw_weather_data)


@mcp.tool()
def calculate_weather_risk(normalized_weather_data: dict) -> dict:
    return calculate_weather_risk_tool(normalized_weather_data)


@mcp.tool()
def save_travel_advisory(report: dict) -> dict:
    return save_travel_advisory_tool(report)


@mcp.tool()
def run_full_advisory(city_name: str) -> dict:
    val = validate_city_input_tool(city_name)
    if not val["success"]:
        return val
    fc = get_weather_forecast_tool(val["normalized_city_name"])
    if not fc["success"]:
        return fc
    norm = normalize_weather_data_tool(fc["raw_weather_data"])
    if not norm["success"]:
        return norm
    risk = calculate_weather_risk_tool(norm)
    report = generate_report(norm, risk)
    saved = save_travel_advisory_tool(report)
    report["saved_path"] = saved["saved_path"]
    return report


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sample-city" and len(sys.argv) > 2:
        city = sys.argv[2]
        result = run_full_advisory(city)
        if "weather_risk" in result:
            print(f"Report generated for {city}")
            print(f"Risk level: {result['weather_risk']}")
            print(f"Saved to: {result.get('saved_path', 'N/A')}")
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
    else:
        mcp.run(transport="stdio")