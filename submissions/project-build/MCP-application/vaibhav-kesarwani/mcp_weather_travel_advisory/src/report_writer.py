import os
import json
from utils import read_json 

def save_travel_advisory(report: dict) -> dict:
    """
    Saves the final travel advisory report as JSON in outputs/travel_advisory_report.json.
    """
    try:
        weather_risk_data = read_json("tools_outputs/assess_weather_risk.json")
        normalize_data = read_json("tools_outputs/normalize_weather.json")

        result = {
            "destination": normalize_data.get("destination"),
            "region": normalize_data.get("region"),
            "country": normalize_data.get("country"),
            "forecast_days": normalize_data.get("forecast_days"),
            "current_weather": normalize_data.get("current_weather", {}),
            "daily_forecast" : normalize_data.get("daily_forecast", []),
            "weather_risk": weather_risk_data.get("weather_risk"),
            "risk_factors": weather_risk_data.get("risk_factors", []),
            "recommended_actions": weather_risk_data.get("recommended_actions", []),
        }

        output_path = os.path.join("outputs", "travel_advisory_report.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        return {
            "success": True,
            "saved_path": output_path
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
