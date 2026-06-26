import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from tools import (validate_city_input_tool,get_weather_forecast_tool,normalize_weather_data_tool,calculate_weather_risk_tool,
                   save_travel_advisory_tool)
from resources import (get_travel_checklist,get_advisory_rules,get_normalized_forecast_schema,CHECKLIST_URI,ADVISORY_RULES_URI,SCHEMA_URI)
from prompts import (travel_readiness_prompt,weather_risk_summary_prompt,packing_recommendation_prompt)
from report_writer import assemble_report

mcp = FastMCP("Weather Travel Advisory")

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

@mcp.resource(CHECKLIST_URI)
def travel_checklist_resource() -> str:
    return get_travel_checklist()

@mcp.resource(ADVISORY_RULES_URI)
def advisory_rules_resource() -> str:
    return get_advisory_rules()

@mcp.resource(SCHEMA_URI)
def normalized_forecast_schema_resource() -> str:
    return get_normalized_forecast_schema()

@mcp.prompt()
def travel_readiness_prompt_mcp(destination: str, weather_risk: str, forecast_summary: str = "", recommended_actions: list = None) -> str:
    return travel_readiness_prompt(destination=destination,
        weather_risk=weather_risk,
        forecast_summary=forecast_summary,
        recommended_actions=recommended_actions or []
    )

@mcp.prompt()
def weather_risk_summary_prompt_mcp(destination: str, weather_risk: str, risk_factors: list = None) -> str:
    return weather_risk_summary_prompt(destination=destination,
        weather_risk=weather_risk,
        risk_factors=risk_factors or []
    )

@mcp.prompt()
def packing_recommendation_prompt_mcp(destination: str, weather_risk: str, risk_factors: list = None) -> str:
    return packing_recommendation_prompt(destination=destination,
        weather_risk=weather_risk,
        risk_factors=risk_factors or []
    )

def run_sample_flow(city_name: str) -> dict:
    print(f"Generating Travel Advisory for: {city_name}")

    print("1 validate_city_input_tool ...")
    validation = validate_city_input_tool(city_name)
    if not validation.get("success"):
        print(f"   Validation failed: {validation.get('message')}")
        return validation
    normalized = validation["normalized_city_name"]
    print(f"   Normalized: {normalized}")

    print("2 get_weather_forecast_tool ...")
    forecast = get_weather_forecast_tool(normalized)
    if not forecast.get("success"):
        print(f"   Forecast failed: {forecast.get('message')}")
        return forecast
    raw_data = forecast["raw_weather_data"]
    print(f"   Raw data received")

    print("3 normalize_weather_data_tool ...")
    normalized_data = normalize_weather_data_tool(raw_data)
    if not normalized_data.get("success"):
        print(f"   Normalization failed: {normalized_data.get('message')}")
        return normalized_data
    print(f"   Destination: {normalized_data['destination']}, {normalized_data['country']}")

    print("4 calculate_weather_risk_tool ...")
    risk_result = calculate_weather_risk_tool(normalized_data)
    print(f"   Risk Level: {risk_result['weather_risk']}")
    print(f"   Risk Factors: {risk_result['risk_factors']}")

    print("5 Referencing MCP resources ...")
    _ = get_travel_checklist()
    _ = get_advisory_rules()
    _ = get_normalized_forecast_schema()
    print(f"   Resources: checklist, advisory-rules, forecast-schema")

    print("6 Generating advisory text from prompts ...")
    _ = travel_readiness_prompt(
        destination=normalized_data["destination"],
        weather_risk=risk_result["weather_risk"],
        forecast_summary="",
        recommended_actions=risk_result["recommended_actions"]
    )
    _ = weather_risk_summary_prompt(
        destination=normalized_data["destination"],
        weather_risk=risk_result["weather_risk"],
        risk_factors=risk_result["risk_factors"]
    )
    _ = packing_recommendation_prompt(
        destination=normalized_data["destination"],
        weather_risk=risk_result["weather_risk"],
        risk_factors=risk_result["risk_factors"]
    )
    print(f"   Prompts: travel_readiness, risk_summary, packing")

    report = assemble_report(normalized_data, risk_result)
    print(f"   Report assembled")

    print("7 save_travel_advisory_tool ...")
    save_result = save_travel_advisory_tool(report)
    if save_result.get("success"):
        print(f"   Saved to: {save_result['saved_path']}")
    else:
        print(f"   Save failed: {save_result.get('message')}")

    print(f"Travel Risk: {risk_result['weather_risk']}\n  Report saved: {save_result.get('saved_path', 'N/A')}")

    return report

if __name__ == "__main__":
    if "--sample-city" in sys.argv:
        idx = sys.argv.index("--sample-city")
        if idx + 1 < len(sys.argv):
            city = sys.argv[idx + 1]
            report = run_sample_flow(city)
            if report:
                print("\n--- Final Report Preview ---\n")
                print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print("Usage: python src/server.py --sample-city <city_name>")
            sys.exit(1)
    else:
        print("Starting MCP Weather Travel Advisory Server...\nPress Ctrl+C to stop.\n")
        mcp.run(transport="streamable-http")