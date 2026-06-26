import sys
import json
from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, Prompt
import tools as t
import resources as r
import prompts as p
import report_writer as rw

mcp = FastMCP("Weather and Travel Advisory Server")

@mcp.tool(name="validate_city_input_tool")
def validate_city(city_name: str) -> str:
    """Validates the city name input formatting."""
    return json.dumps(t.validate_city_input_tool(city_name))

@mcp.tool(name="get_weather_forecast_tool")
def get_weather(normalized_city_name: str) -> str:
    """Fetches raw weather conditions via wttr API."""
    return json.dumps(t.get_weather_forecast_tool(normalized_city_name))

@mcp.tool(name="normalize_weather_data_tool")
def normalize_data(raw_weather_data: dict) -> str:
    """Extracts required data into standard architecture format layers."""
    return json.dumps(t.normalize_weather_data_tool(raw_weather_data))

@mcp.tool(name="calculate_weather_risk_tool")
def calculate_risk(normalized_weather_data: dict) -> str:
    """Evaluates weather-based threat matrices dynamically and deterministically."""
    return json.dumps(t.calculate_weather_risk_tool(normalized_weather_data))

@mcp.tool(name="save_travel_advisory_tool")
def save_report(report: dict) -> str:
    """Saves compiled advisory parameters out to disc location targets."""
    return json.dumps(rw.save_travel_advisory_tool(report))


@mcp.resource("resource://travel/checklist")
def checklist_resource() -> str:
    """Provides a static travel-readiness checklist."""
    return r.get_resource("resource://travel/checklist")

@mcp.resource("resource://travel/advisory-rules")
def advisory_rules_resource() -> str:
    """Provides static rules for interpreting weather risk."""
    return r.get_resource("resource://travel/advisory-rules")

@mcp.resource("resource://weather/normalized-forecast-schema")
def schema_resource() -> str:
    """Describes the normalized forecast schema expected by this project."""
    return r.get_resource("resource://weather/normalized-forecast-schema")

@mcp.prompt("travel_readiness_prompt")
def tr_prompt(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: list) -> str:
    return p.travel_readiness_prompt(destination, weather_risk, forecast_summary, recommended_actions)

@mcp.prompt("weather_risk_summary_prompt")
def wrs_prompt(destination: str, weather_risk: str, risk_factors: list) -> str:
    return p.weather_risk_summary_prompt(destination, weather_risk, risk_factors)

@mcp.prompt("packing_recommendation_prompt")
def pr_prompt(destination: str, weather_risk: str, risk_factors: list) -> str:
    return p.packing_recommendation_prompt(destination, weather_risk, risk_factors)

def run_sample_pipeline(city: str):
    print(f"--- Running Sample Weather Advisory Pipeline for: {city} ---")
    val = t.validate_city_input_tool(city)
    if not val["success"]:
        print(f"Validation failed: {val['message']}")
        return
        
    raw = t.get_weather_forecast_tool(val["normalized_city_name"])
    if not raw["success"]:
        print(f"API Error: {raw['message']}")
        return
        
    norm = t.normalize_weather_data_tool(raw["raw_weather_data"])
    if not norm["success"]:
        print(f"Normalization failed: {norm['message']}")
        return
        
    risk = t.calculate_weather_risk_tool(norm)
    
    final_report = {
        "destination": norm["destination"],
        "region": norm["region"],
        "country": norm["country"],
        "forecast_days": norm["forecast_days"],
        "current_weather": norm["current_weather"],
        "daily_forecast": norm["daily_forecast"],
        "weather_risk": risk["weather_risk"],
        "risk_factors": risk["risk_factors"],
        "recommended_actions": risk["recommended_actions"],
        "packing_suggestions": ["Water bottle", "Appropriate weather gear"],
        "travel_readiness_advisory": f"Travel to {norm['destination']} evaluated as {risk['weather_risk']}.",
        "weather_risk_explanation": f"Risk profiles verified as {risk['weather_risk']} based on raw constraints.",
        "resources_used": ["resource://travel/checklist", "resource://travel/advisory-rules", "resource://weather/normalized-forecast-schema"],
        "tools_used": ["validate_city_input_tool", "get_weather_forecast_tool", "normalize_weather_data_tool", "calculate_weather_risk_tool", "save_travel_advisory_tool"],
        "prompts_used": ["travel_readiness_prompt", "weather_risk_summary_prompt", "packing_recommendation_prompt"]
    }
    
    save_res = rw.save_travel_advisory_tool(final_report)
    print(f"Advisory Generation Completed! Save Status: {save_res}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--sample-city":
        run_sample_pipeline(sys.argv[2])
    else:
        mcp.run()
