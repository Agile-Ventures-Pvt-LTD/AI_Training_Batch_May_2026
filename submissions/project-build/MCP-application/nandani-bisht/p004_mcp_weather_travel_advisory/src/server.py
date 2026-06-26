import argparse
from mcp.server.fastmcp import FastMCP

from .tools import (
    validate_city_input,
    get_weather_forecast,
    normalize_weather_data,
    calculate_weather_risk,
    save_travel_advisory
)
from .resources import get_checklist, get_advisory_rules, get_normalized_schema
from .prompts import (
    travel_readiness_prompt as travel_readiness_prompt_impl,
    weather_risk_summary_prompt as weather_risk_summary_prompt_impl,
    packing_recommendation_prompt as packing_recommendation_prompt_impl
)
from .report_writer import generate_final_report

mcp = FastMCP("WeatherTravelAdvisory")

@mcp.tool()
def validate_city_input_tool(city_name: str) -> dict:
    """Validates the city name entered by the user."""
    return validate_city_input(city_name)

@mcp.tool()
def get_weather_forecast_tool(normalized_city_name: str) -> dict:
    """Calls the wttr.in JSON API and returns the raw weather response."""
    return get_weather_forecast(normalized_city_name)

@mcp.tool()
def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
    """Converts raw wttr.in JSON into a clean internal weather schema."""
    return normalize_weather_data(raw_weather_data)

@mcp.tool()
def calculate_weather_risk_tool(normalized_weather_data: dict) -> dict:
    """Calculates deterministic travel weather risk from normalized weather data."""
    return calculate_weather_risk(normalized_weather_data)

@mcp.tool()
def save_travel_advisory_tool(report: dict) -> dict:
    """Saves the final advisory report as JSON."""
    return save_travel_advisory(report)

@mcp.resource("resource://travel/checklist")
def travel_checklist() -> str:
    """Provides a static travel-readiness checklist."""
    return get_checklist()

@mcp.resource("resource://travel/advisory-rules")
def travel_advisory_rules() -> str:
    """Provides static rules for interpreting weather risk."""
    return get_advisory_rules()

@mcp.resource("resource://weather/normalized-forecast-schema")
def weather_normalized_schema() -> str:
    """Describes the normalized forecast schema expected by this project."""
    return get_normalized_schema()

@mcp.prompt()
def travel_readiness_prompt(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: list) -> str:
    """Creates a concise travel-readiness advisory."""
    return travel_readiness_prompt_impl(destination, weather_risk, forecast_summary, recommended_actions)

@mcp.prompt()
def weather_risk_summary_prompt(destination: str, weather_risk: str, risk_factors: list) -> str:
    """Explains why the risk level is LOW, MEDIUM, or HIGH."""
    return weather_risk_summary_prompt_impl(destination, weather_risk, risk_factors)

@mcp.prompt()
def packing_recommendation_prompt(destination: str, weather_risk: str, risk_factors: list) -> str:
    """Generates practical packing suggestions."""
    return packing_recommendation_prompt_impl(destination, weather_risk, risk_factors)

def run_sample_flow(city_name: str):
    print(f"Starting Travel Advisory Flow for: {city_name}")
    
    val_res = validate_city_input(city_name)
    if not val_res["success"]:
        print(f"Validation failed: {val_res['message']}")
        return
    normalized_city = val_res["normalized_city_name"]
    
    weather_res = get_weather_forecast(normalized_city)
    if not weather_res["success"]:
        print(f"Fetch failed: {weather_res['message']}")
        return
    
    norm_res = normalize_weather_data(weather_res["raw_weather_data"])
    if not norm_res["success"]:
        print(f"Normalization failed: {norm_res['message']}")
        return
    
    risk_res = calculate_weather_risk(norm_res)
    
    forecast_summary = f"{norm_res['forecast_days']} days forecast. Current temp: {norm_res['current_weather']['temperature_c']}C."
    readiness_advisory = f"Travel to {norm_res['destination']} is {risk_res['weather_risk'].lower()} risk. {forecast_summary}"
    risk_explanation = f"The risk level is {risk_res['weather_risk'].lower()} because: {' '.join(risk_res['risk_factors'])}"
    
    packing_suggestions = ["Essential documents", "Phone charger"]
    if risk_res["weather_risk"] == "HIGH":
        packing_suggestions.extend(["Heavy rain gear", "Extra water", "First aid kit"])
    elif risk_res["weather_risk"] == "MEDIUM":
        packing_suggestions.extend(["Umbrella", "Sunscreen", "Light jacket"])
    else:
        packing_suggestions.extend(["Comfortable walking shoes", "Sunglasses"])

    final_report = generate_final_report(
        normalized_data=norm_res,
        risk_data=risk_res,
        packing_suggestions=packing_suggestions,
        travel_readiness_advisory=readiness_advisory,
        weather_risk_explanation=risk_explanation
    )
    
    save_res = save_travel_advisory(final_report)
    if save_res["success"]:
        print(f"Report saved successfully to: {save_res['saved_path']}")
    else:
        print(f"Save failed: {save_res['message']}")
    print("Finish Execution")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather and Travel Advisory MCP Server")
    parser.add_argument("--sample-city", type=str, help="Run the sample flow for a specific city and exit")
    args = parser.parse_args()
    
    if args.sample_city:
        run_sample_flow(args.sample_city)
    else:
        mcp.run()