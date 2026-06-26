import sys
import json
from tools import (
    validate_city_input_tool,
    get_weather_forecast_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool,
    save_travel_advisory_tool
)
from schemas import validate_normalized_data
from prompts import format_prompt

def execute_mcp_pipeline_orchestration(user_city_input: str):
    """Executes the rigid sequential 14-step data architecture matrix flow."""
    print(f"--- Processing Pipeline for Location: {user_city_input} ---")
    
    tools_tracker = []
    resources_tracker = []
    prompts_tracker = []

    tools_tracker.append("validate_city_input_tool")
    v_raw = json.loads(validate_city_input_tool(user_city_input))
    if not v_raw.get("success"):
        print(f"Aborted: {v_raw.get('message')}")
        return
        
    normalized_name = v_raw["normalized_city_name"]

    tools_tracker.append("get_weather_forecast_tool")
    api_raw = json.loads(get_weather_forecast_tool(normalized_name))
    if not api_raw.get("success"):
        print("Aborted: Server failure fetching meteorology reports.")
        return

    tools_tracker.append("normalize_weather_data_tool")
    norm_raw = json.loads(normalize_weather_data_tool(json.dumps(api_raw["raw_weather_data"])))
    if not norm_raw.get("success"):
        print("Aborted: Payload normalization parsing fault.")
        return

    resources_tracker.append("resource://weather/normalized-forecast-schema")
    if not validate_normalized_data(norm_raw):
        print("Aborted: Internal structure check validation fault.")
        return

    tools_tracker.append("calculate_weather_risk_tool")
    risk_raw = json.loads(calculate_weather_risk_tool(json.dumps(norm_raw)))

    resources_tracker.extend(["resource://travel/checklist", "resource://travel/advisory-rules"])

    summary_text = f"Weather at destination {norm_raw['destination']} is currently {norm_raw['current_weather']['weather_description']}."
    
    prompts_tracker.append("travel_readiness_prompt")
    _ = format_prompt("travel_readiness_prompt", {
        "destination": norm_raw["destination"], "weather_risk": risk_raw["weather_risk"],
        "forecast_summary": summary_text, "recommended_actions": str(risk_raw["recommended_actions"])
    })
    readiness_report_text = f"The trip destination readiness evaluation for {norm_raw['destination']} is {risk_raw['weather_risk']}."

    prompts_tracker.append("weather_risk_summary_prompt")
    _ = format_prompt("weather_risk_summary_prompt", {
        "destination": norm_raw["destination"], "weather_risk": risk_raw["weather_risk"],
        "risk_factors": str(risk_raw["risk_factors"])
    })
    risk_explanation_text = f"Risk factor flags registered are: {', '.join(risk_raw['risk_factors'])}."

    prompts_tracker.append("packing_recommendation_prompt")
    _ = format_prompt("packing_recommendation_prompt", {
        "destination": norm_raw["destination"], "weather_risk": risk_raw["weather_risk"],
        "risk_factors": str(risk_raw["risk_factors"])
    })
    
    packing_suggestions = ["Identity Verification Card", "Power Supply Bank Charger"]
    if risk_raw["weather_risk"] in ["MEDIUM", "HIGH"]:
        packing_suggestions.extend(["Raincoat Windcheater Umbrella", "Insulated Cold Water Flask"])

    # Step 8: Assemble final report payload following Section 14 Schema Spec requirements
    tools_tracker.append("save_travel_advisory_tool")
    final_json_manifest = {
        "destination": norm_raw["destination"],
        "region": norm_raw["region"],
        "country": norm_raw["country"],
        "forecast_days": norm_raw["forecast_days"],
        "current_weather": norm_raw["current_weather"],
        "daily_forecast": norm_raw["daily_forecast"],
        "weather_risk": risk_raw["weather_risk"],
        "risk_factors": risk_raw["risk_factors"],
        "recommended_actions": risk_raw["recommended_actions"],
        "packing_suggestions": packing_suggestions,
        "travel_readiness_advisory": readiness_report_text,
        "weather_risk_explanation": risk_explanation_text,
        "resources_used": resources_tracker,
        "tools_used": tools_tracker,
        "prompts_used": prompts_tracker
    }

    save_raw = json.loads(save_travel_advisory_tool(json.dumps(final_json_manifest)))
    if save_raw.get("success"):
        print(f"Success! Unique MCP file generated at: {save_raw['saved_path']}\n")
    else:
        print("Error during report logging execution pipeline.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        chosen_city = " ".join(sys.argv[1:])
        execute_mcp_pipeline_orchestration(chosen_city)
    else:
        print("Error: Please provide a city name in your terminal command.")
    