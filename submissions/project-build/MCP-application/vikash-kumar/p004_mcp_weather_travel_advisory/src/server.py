import sys
import argparse
import asyncio
from mcp import InitializationOptions,NotificationOptions,Server,types
import mcp

from tools import validate_city_input_tool, get_weather_forecast_tool,normalize_weather_data_tool, calculate_weather_risk_tool, save_travel_advisory_tool
from resources import RESOURCES
from report_writer import generate_mock_text_from_prompts

server = Server("p004-weather-travel-advisory")

@server.list_tools()
async def handle_list_tools():
    """It will handle tools for MCP"""
    return [types.Tool(name="validate_city_input_tool",description="Validates city input name", 
            inputSchema={"type": "object", "properties": {"city_name": {"type": "string"}}, "required": ["city_name"]}),

        # types.Tool(),
        types.Tool(name="get_weather_forecast_tool", description="Get weather forecast from wttr.in", 
            inputSchema={"type": "object", "properties": {"normalized_city_name": {"type": "string"}}, "required": ["normalized_city_name"]}),
        types.Tool(name="normalize_weather_data_tool", description="it will normalize the weather data", 
            inputSchema={"type": "object", "properties": {"raw_weather_data": {"type": "object"}}, "required": ["raw_weather_data"]}),
        types.Tool(name="calculate_weather_risk_tool", description="It will decide the risk category bands", 
            inputSchema={"type": "object", "properties": {"normalized_weather_data": {"type": "object"}}, "required": ["normalized_weather_data"]}),
        types.Tool(name="save_travel_advisory_tool", description="It will save the traeval advisory", 
            inputSchema={"type": "object", "properties": {"report": {"type": "object"}}, "required": ["report"]})]

@server.list_resources()
async def handle_list_resources():
    """It will handle the resources"""
    return [types.Resource(uri="resource://travel/checklist", name="Travel Checklist"),types.Resource(uri="resource://travel/advisory-rules", name="Advisory Rules Mapping"),types.Resource(uri="resource://weather/normalized-forecast-schema", name="JSON Schema Context")]

@server.list_prompts()
async def handle_list_prompts():
    """It will handle the list prompts"""
    return [types.Prompt(name="travel_readiness_prompt", description="Advisory string summary"),types.Prompt(name="weather_risk_summary_prompt", description="Risk value explanation text"),types.Prompt(name="packing_recommendation_prompt", description="Packing item short suggestions")]

def run_pipeline(city_input: str):
    """It will run the whole pipeline"""
    print(f"Weather Travel Advisory for: {city_input} ")

    result = validate_city_input_tool(city_input)
    if not result["success"]:
        print(f"Validation Error: {result['message']}")
        return

    result2 = get_weather_forecast_tool(result["normalized_city_name"])
    if not result2["success"]:
        print(f"API Error: {result2['message']}")
        return

    result3 = normalize_weather_data_tool(result2["raw_weather_data"])
    if not result3["success"]:
        print(f"Normalization Error: {result3['message']}")
        return

    result4 = calculate_weather_risk_tool(result3)

    adv, exp, packing = generate_mock_text_from_prompts(result3["destination"], result4["weather_risk"],result4["risk_factors"])

    report = {"destination": result3["destination"],"region": result3["region"],"country": result3["country"],"forecast_days": result3["forecast_days"],"current_weather": result3["current_weather"],"daily_forecast": result3["daily_forecast"],
        "weather_risk": result3["weather_risk"],"risk_factors": result3["risk_factors"],"recommended_actions": result3["recommended_actions"],"packing_suggestions": packing,"travel_readiness_advisory": adv,"weather_risk_explanation": exp,
        "resources_used": ["resource://travel/checklist","resource://travel/advisory-rules","resource://weather/normalized-forecast-schema"],
        "tools_used": ["validate_city_input_tool","get_weather_forecast_tool","normalize_weather_data_tool","calculate_weather_risk_tool","save_travel_advisory_tool"],
        "prompts_used": ["travel_readiness_prompt","weather_risk_summary_prompt","packing_recommendation_prompt"]}

    lower_city = city_input.lower().strip()
    if "jaipur" in lower_city:
        target_filename = "sample_jaipur_advisory.json"
    elif "pune" in lower_city:
        target_filename = "sample_pune_advisory.json"
    else:
        target_filename = "travel_advisory_report.json"

    save_result = save_travel_advisory_tool(report, filename=target_filename)
    print(f"Report is saved to : {save_result['saved_path']}")

async def main_async():
    """It will run the stdio mode of communication"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream,write_stream,InitializationOptions(
                server_name="p004-weather-travel-advisory",
                capabilities=server.get_capabilities(notification_options=NotificationOptions(),experimental_capabilities={})))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Weather Server")
    parser.add_argument("sample-city", type=str, help="It will run for sample city")
    args = parser.parse_args()
    if args.sample_city:
        run_pipeline(args.sample_city)
    else:
        asyncio.run(main_async())
