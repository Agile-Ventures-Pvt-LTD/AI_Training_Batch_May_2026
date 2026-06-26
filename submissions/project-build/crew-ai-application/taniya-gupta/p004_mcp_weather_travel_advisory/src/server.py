import json
from mcp.server.fastmcp import FastMCP
import sys

from tools import (
    validate_city_input_tool,
    get_weather_forecast_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool,
    save_travel_advisory_tool
)
from resources import(
    TRAVEL_CHECKLIST,
    WEATHER_ADVISORY_RULES,
    NORMALIZED_FORECAST_SCHEMA
)
from prompts import(
    get_travel_readiness,
    get_weather_risk_summary,
    get_packing_recommendation
)

from report_writer import save_report

mcp=FastMCP(" Weather & travel advisory MCP server")

@mcp.tool()
def validate_city_input(city_name):
    """
    Validates the city name entered by the user.
This tool does not call the weather API
    """
    return validate_city_input_tool(city_name)

@mcp.tool()
def get_weather_forecast(normalized_city_name):
    """
    Calls the wttr.in JSON API and returns the raw weather response.
This is the only tool that should call the external weather API.
    """
    return get_weather_forecast_tool(normalized_city_name)

@mcp.tool()
def normalize_weather_data(raw_weather_data):
    """
    Converts raw wttr.in JSON into a clean internal weather schema.
This tool must not call the external API.
    """
    return normalize_weather_data_tool(raw_weather_data)

@mcp.tool()
def calculate_weather_risk(normalized_weather_data):
    """
    Calculates deterministic travel weather risk from normalized weather data.
This tool must not call the API and must not use an LLM.
    """
    return calculate_weather_risk_tool(normalized_weather_data)

@mcp.tool()
def save_travel_advisory(report):
    """
    Saves the final advisory report as JSON
    """
    return save_travel_advisory_tool(report)

@mcp.resource("resource://travel/checklist")
def travel_checklist() -> str:
    return TRAVEL_CHECKLIST

@mcp.resource("resource://travel/advisory-rules")
def travel_advisory_rules() -> str:
    return WEATHER_ADVISORY_RULES

@mcp.resource("resource://weather/normalized-forecast-schema")
def weather_normalized_forecast_schema() -> str:
    return NORMALIZED_FORECAST_SCHEMA

@mcp.prompt()
def travel_readiness_prompt(
    destination: str,
    weather_risk: str ,
    forecast_summary: str,
    recommended_actions: str ) -> str:
    """Creates a concise travel-readiness advisory."""
    return get_travel_readiness(
        destination=destination,
        weather_risk=weather_risk,
        forecast_summary=forecast_summary,
        recommended_actions=recommended_actions
    )

@mcp.prompt()
def weather_risk_summary_prompt(
    destination: str,
    weather_risk: str,
    risk_factors: str
) -> str:
    """Explains why the risk level is LOW, MEDIUM or HIGH."""
    return get_weather_risk_summary(
        destination=destination,
        weather_risk=weather_risk,
        risk_factors=risk_factors
    )

@mcp.prompt()
def packing_recommendation_prompt(
    destination: str ,
    weather_risk: str ,
    risk_factors: str 
) -> str:
    """Generates practical packing suggestions."""
    return get_packing_recommendation(
        destination=destination,
        weather_risk=weather_risk,
        risk_factors=risk_factors
    )

def run_sample(city_name):
    print("Generating weather & travel advisory")
    validation=validate_city_input(city_name)
    normalized_city = validation["normalized_city_name"]
    print(f"City is validated")
    
    weather_response=get_weather_forecast(normalized_city)
    print(f"Fetched raw json successfully")

    normalized=normalize_weather_data(weather_response["raw_weather_data"])
    print("Weather data is normalized")

    risk_info=calculate_weather_risk(normalized)
    risk_level=risk_info["weather_risk"]
    print("Risk assesment is done")

    advisory_map = {
        "LOW": "Travel appears comfortable with no major weather concerns.",
        "MEDIUM": "Travel appears manageable with basic weather precautions.",
        "HIGH": "Travel should be reconsidered or planned with extra caution due to adverse weather."
    }
    travel_readiness_advisory = advisory_map.get(risk_level)
    
    factors = risk_info["risk_factors"]
    temp = any("temperature" in f or "heat" in f for f in factors)
    rain = any("rain" in f or "precipitation" in f for f in factors)
    wind = any("wind" in f for f in factors)
    
    parts = []
    if temp:
        parts.append("heat")
    if rain:
        parts.append("rain")
    if wind:
        parts.append("wind")
        
    if not parts:
        reason = "no major heat, rain, or wind indicators are present."
    elif len(parts) == 1:
        reason = f"moderate {parts[0]} indicators are present" if risk_level == "MEDIUM" else f"severe {parts[0]} indicators are present."
    else:
        conjunction = "and"
        reason = f"moderate {', '.join(parts[:-1])} {conjunction} {parts[-1]} indicators are present." if risk_level == "MEDIUM" else f"severe {', '.join(parts[:-1])} {conjunction} {parts[-1]} indicators are present."
        
    weather_risk_explanation = f"The risk level is {risk_level.lower()} because {reason}"
    
    packing = []
    if temp:
        packing.extend(["Water bottle", "Light cotton clothing", "Sunscreen", "Cap or hat"])
    if rain:
        packing.extend(["Umbrella", "Raincoat", "Waterproof shoes"])
    if wind:
        packing.extend(["Windbreaker", "Sun protection"])
        
    unique_packing = []
    for item in packing:
        if item not in unique_packing:
            unique_packing.append(item)
            
    if not unique_packing:
        unique_packing = ["Comfortable clothing", "Water bottle"]
        
    save_result = save_report(
        normalized_weather=normalized,
        risk_info=risk_info,
        travel_readiness_advisory=travel_readiness_advisory,
        weather_risk_explanation=weather_risk_explanation,
        packing_suggestions=unique_packing
    )
    
    if save_result.get("success"):
        saved_path = save_result["saved_path"]
        print(f"Report is saved successfu;llly to {saved_path}")
        
        with open(saved_path, "r") as f:
                report_data = json.load(f)
        print(json.dumps(report_data, indent=2))
        
    else:
        print("Failed to save the report")
        
if __name__=="__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sample-city":
        if len(sys.argv) > 2:
            run_sample(" ".join(sys.argv[2:]))
    else:
        mcp.run()