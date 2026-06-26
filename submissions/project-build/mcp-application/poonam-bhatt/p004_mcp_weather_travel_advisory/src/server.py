import os
import sys
import json
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
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
    get_forecast_schema
)
from src.prompts import (
    format_travel_readiness,
    format_weather_risk_summary,
    format_packing_recommendation,
    generate_heuristic_travel_readiness,
    generate_heuristic_weather_risk_explanation,
    generate_heuristic_packing_suggestions
)
from src.report_writer import build_travel_advisory_report

load_dotenv()

mcp = FastMCP("Weather and Travel Advisory Server")

@mcp.tool(name="validate_city_input_tool")
def validate_city_input(city_name: str) -> dict:
    return validate_city_input_tool(city_name)

@mcp.tool(name="get_weather_forecast_tool")
def get_weather_forecast(normalized_city_name: str) -> dict:
    return get_weather_forecast_tool(normalized_city_name)

@mcp.tool(name="normalize_weather_data_tool")
def normalize_weather_data(raw_weather_data: dict) -> dict:
    return normalize_weather_data_tool(raw_weather_data)

@mcp.tool(name="calculate_weather_risk_tool")
def calculate_weather_risk(normalized_weather_data: dict) -> dict:
    return calculate_weather_risk_tool(normalized_weather_data)

@mcp.tool(name="save_travel_advisory_tool")
def save_travel_advisory(report: dict) -> dict:
    return save_travel_advisory_tool(report)


@mcp.resource("resource://travel/checklist")
def get_travel_checklist() -> str:
    return get_checklist()

@mcp.resource("resource://travel/advisory-rules")
def get_travel_advisory_rules() -> str:
    return get_advisory_rules()

@mcp.resource("resource://weather/normalized-forecast-schema")
def get_weather_forecast_schema() -> str:
    return get_forecast_schema()


@mcp.prompt(name="travel_readiness_prompt")
def travel_readiness(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: str) -> str:
    actions = [a.strip() for a in recommended_actions.split(",")] if isinstance(recommended_actions, str) else recommended_actions
    return format_travel_readiness(destination, weather_risk, forecast_summary, actions)

@mcp.prompt(name="weather_risk_summary_prompt")
def weather_risk_summary(destination: str, weather_risk: str, risk_factors: str) -> str:
    factors = [f.strip() for f in risk_factors.split(",")] if isinstance(risk_factors, str) else risk_factors
    return format_weather_risk_summary(destination, weather_risk, factors)

@mcp.prompt(name="packing_recommendation_prompt")
def packing_recommendation(destination: str, weather_risk: str, risk_factors: str) -> str:
    factors = [f.strip() for f in risk_factors.split(",")] if isinstance(risk_factors, str) else risk_factors
    return format_packing_recommendation(destination, weather_risk, factors)


def run_pipeline_for_city(city_name: str, save_as_sample: bool = False):
    val_res = validate_city_input_tool(city_name)
    if not val_res.get("success"):
        return False
    norm_city = val_res.get("normalized_city_name")
    
    fetch_res = get_weather_forecast_tool(norm_city)
    if not fetch_res.get("success"):
        return False
    raw_data = fetch_res.get("raw_weather_data")
    
    norm_res = normalize_weather_data_tool(raw_data)
    if not norm_res.get("success"):
        return False
    
    risk_res = calculate_weather_risk_tool(norm_res)
    risk_level = risk_res.get("weather_risk")
    risk_factors = risk_res.get("risk_factors")
    
    forecast_desc = norm_res.get("daily_forecast", [{}])[0].get("weather_description", "variable")
    
    travel_advisory = generate_heuristic_travel_readiness(city_name, risk_level, risk_factors)
    risk_explanation = generate_heuristic_weather_risk_explanation(city_name, risk_level, risk_factors)
    packing_suggs = generate_heuristic_packing_suggestions(risk_level, risk_factors)
    
    report = build_travel_advisory_report(
        normalized_data=norm_res,
        risk_assessment=risk_res,
        packing_suggestions=packing_suggs,
        travel_readiness_advisory=travel_advisory,
        weather_risk_explanation=risk_explanation
    )
    
    save_res = save_travel_advisory_tool(report)
    if save_res.get("success"):
        if save_as_sample:
            os.makedirs("sample_outputs", exist_ok=True)
            clean_name = city_name.replace(" ", "_").lower()
            sample_path = f"sample_outputs/sample_{clean_name}_advisory.json"
            with open(sample_path, "w") as sf:
                json.dump(report, sf, indent=2)
        return True
    else:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Weather & Travel Advisory Server")
    parser.add_argument("--sample-city", type=str, help="Run the offline advisory pipeline for the specified city")
    args = parser.parse_args()
    
    if args.sample_city:
        run_pipeline_for_city(args.sample_city, save_as_sample=True)
    else:
        mcp.run(transport="stdio")
