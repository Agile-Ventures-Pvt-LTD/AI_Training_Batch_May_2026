import sys
import json
from fastmcp import FastMCP
from api_client import get_weather_from_wttr
from tools import validate_city_input_tool,weather_forecast_tool,normalize_weather_data_tool,calculate_weather_risk_tool,save_travel_advisory_tool
from resources import Checklist_Content, Advisory_Rule_Content, Forecast_Schema_Content
from prompts import travel_readiness_prompt,weather_risk_summary_prompt,packing_recommendation_prompt
from report_writer import save_travel_advisory_report

mcp = FastMCP("Weather_Travel_Advisory_Server")

@mcp.tool()
def validate_city(city_name:str) -> str:
    return json.dumps(validate_city_input_tool(city_name))

@mcp.tool()
def weather_forecast(normalized_city_name:str) -> str:
    return json.dumps(weather_forecast_tool(normalized_city_name))

@mcp.tool()
def normalize_weather_data(raw_weather_json:str) -> str:
    return json.dumps(normalize_weather_data_tool(json.loads(raw_weather_json)))

@mcp.tool()
def calculate_weather_risk(normalize_weather_json:str) -> str:
    return json.dumps(calculate_weather_risk_tool(json.loads(normalize_weather_json)))

@mcp.tool()
def save_advisory(report_json:str) -> str:
    return json.dumps(save_travel_advisory_tool(json.loads(report_json)))

@mcp.resource("resource://travel/checklist")
def get_checklist() -> str:
    return Checklist_Content

@mcp.resource("resource://travel/advisory-rules")
def get_advisory_rules() -> str:
    return Advisory_Rule_Content

@mcp.resource("resource://weather/normalized-forecast-schema")
def get_forecast_schema() -> str:
    return Forecast_Schema_Content

@mcp.prompt()
def travel_readiness(destination: str, weather_risk: str, forecast_summary: str, recommended_actions: str) -> str:
    actions_list = json.loads(recommended_actions) if recommended_actions.startswith('[') else [recommended_actions]
    return travel_readiness_prompt(destination, weather_risk, forecast_summary, actions_list)

@mcp.prompt()
def weather_risk_summary(destination: str, weather_risk: str, risk_factors: str) -> str:
    factors_list = json.loads(risk_factors) if risk_factors.startswith('[') else [risk_factors]
    return weather_risk_summary_prompt(destination, weather_risk, factors_list)

@mcp.prompt()
def packing_recommendation(destination: str, weather_risk: str, risk_factors: str) -> str:
    factors_list = json.loads(risk_factors) if risk_factors.startswith('[') else [risk_factors]
    return packing_recommendation_prompt(destination, weather_risk, factors_list)

def run_server(city:str):

    print("1. Validate city input")
    validate_city = validate_city_input_tool(city)
    if not validate_city["success"]:
        print(f"Input Validation Failed: {validate_city['message']}")
        return

    print(f"2. Fetching Weather data for '{validate_city['normalized_city_name']}")
    weather_data = weather_forecast_tool(validate_city['normalized_city_name'])
    if  not weather_data["success"]:
        print(f"Weather Extraction failed: {weather_data['message']}")
        return

    print("3: Normalizing raw weather dataset")
    normalize_weather = normalize_weather_data_tool(weather_data["raw_weather_data"])
    if not normalize_weather["success"]:
        print(f" Data normalization failed: {normalize_weather['message']}")
        return
        
    print("4: Running risk assessment checks")
    risk_asses = calculate_weather_risk_tool(normalize_weather)
    
    final_report = {
        **normalize_weather, **risk_asses,
        "packing_suggestions": ["Water bottle", "Sunscreen", "Cap"] if risk_asses["weather_risk"] != "LOW" else ["Standard Travel Kit"],
        "travel_readiness_advisory": f"Travel appears manageable with basic precautions. Status: {risk_asses['weather_risk']}",
        "weather_risk_explanation": f"Calculated risk index is {risk_asses['weather_risk']} based on raw metric threshold evaluations.",
        "resources_used": [
            "resource://travel/checklist", 
            "resource://travel/advisory-rules", 
            "resource://weather/normalized-forecast-schema"
        ],
        "tools_used": [
            "validate_city_input_tool", 
            "get_weather_forecast_tool", 
            "normalize_weather_data_tool", 
            "calculate_weather_risk_tool", 
            "save_travel_advisory_tool"
        ],
        "prompts_used": [
            "travel_readiness_prompt", 
            "weather_risk_summary_prompt", 
            "packing_recommendation_prompt"
        ]
    }

    print("5: Saving generated travel advisory report file.")
    s_res = save_travel_advisory_tool(final_report)
    if s_res["success"]:
        print(f"Server executed successfully! Report saved to: {s_res.get('saved_path')}\n")
    else:
        print(f"Failed to write final report: {s_res.get('message')}\n")

if __name__ == "__main__":
    if "--sample-city" in sys.argv:
        try:
            flag_index = sys.argv.index("--sample-city")
            city_name = sys.argv[flag_index + 1]
            run_server(city_name)
        except IndexError:
            print("Error: Please provide a city name after --sample-city")
    else:
        mcp.run()
