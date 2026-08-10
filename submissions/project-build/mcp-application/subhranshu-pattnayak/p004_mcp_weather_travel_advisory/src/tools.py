from typing import Any
from api_client import get_weather_from_wttr
import os
from config import OUTPUT_DIR
import json

def validate_city_input_tool(city_name: str) -> dict[str, Any]:
    """Validates the city name entered by the user.

    Args:
        city_name (str): Name of the city

    Returns:
        dict[str, Any]: Returns status, cleaned city name, and original city name.
    """
    try:
        if not city_name or isinstance(city_name, str):
            raise Exception({
            "success": False,
            "message": "City name cannot be empty and must be a string."
            })
        
        cleaned_city_name = city_name.strip()
        
        if len(cleaned_city_name) < 2:
            raise Exception({
            "success": False,
            "message": "City name is too short."
            })
        
        cleaned_city_name = cleaned_city_name.replace(" ", "+")
        
        return {
            "success": False,
            "original_city_name": city_name,
            "normalized_city_name": cleaned_city_name
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


def get_weather_forecast_tool(cleaned_city_name: str) -> dict[str, Any]:
    """Calls the wttr.in JSON API Client and returns the raw weather response in structured format.

    Args:
        cleaned_city_name (str): Normalized city name

    Returns:
        dict[str, Any]: Returns status, raw data and url used. Returns status and error message on failure.
    """
    try:
        raw_data = get_weather_from_wttr(cleaned_city_name)
        raw_json_data = raw_data.json()
        loc = cleaned_city_name.replace("+", " ")
        if not raw_json_data:
            raise Exception({
                "success": False,
                "city_name": "InvalidCity",
                "message": "Unable to fetch weather data."
            })
        return {
            "success": True,
            "city_name": loc,
            "raw_weather_data": raw_json_data
        }
    
    except Exception as e:
        return {
            "success": False,
            "city_name": "InvalidCity",
            "message": str(e)
        }


def normalize_weather_data_tool(raw_weather_data: dict[str, Any]) -> dict[str, Any]:
    try:
        daily_forecast = []
        
        for i in range(3):
            total_precipitation_mm = 0.0
            max_wind_kmph = 0.0
            max_chance_of_rain = 0.0
            for hour in raw_weather_data["weather"][0]["hourly"]:
                total_precipitation_mm += float(hour["precipMM"])
                max_wind_kmph = max(float(hour["windspeedKmph"]), max_wind_kmph)
                max_chance_of_rain = max(float(hour["chanceofrain"]), max_chance_of_rain)
            
            daily_forecast.append(
                {
                    "date": raw_weather_data["weather"][i]["date"],
                    "max_temp_c": float(raw_weather_data["weather"][i]["maxtempC"]),
                    "min_temp_c": float(raw_weather_data["weather"][i]["mintempC"]),
                    "avg_temp_c": float(raw_weather_data["weather"][i]["avgtempC"]),
                    "total_precipitation_mm": total_precipitation_mm,
                    "max_wind_kmph": max_wind_kmph,
                    "max_chance_of_rain": max_chance_of_rain,
                    "weather_description": raw_weather_data["weather"][i]["hourly"][0]["weatherDesc"][0]["value"].strip()
                }
            )
        
        return {
            "success": True,
            "destination": raw_weather_data["nearest_area"][0]["areaName"][0]["value"],
            "region": raw_weather_data["nearest_area"][0]["region"][0]["value"],
            "country": raw_weather_data["nearest_area"][0]["country"][0]["value"],
            "forecast_days": 3,
            "current_weather": {
                "temperature_c": float(raw_weather_data["current_condition"][0]["temp_C"]),
                "humidity": int(raw_weather_data["current_condition"][0]["humidity"]),
                "precipitation_mm": float(raw_weather_data["current_condition"][0]["precipMM"]),
                "wind_speed_kmph": float(raw_weather_data["current_condition"][0]["windspeedKmph"]),
                "weather_description": raw_weather_data["current_condition"][0]["weatherDesc"][0]["value"].strip()
            },
            "daily_forecast": daily_forecast
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Unable to normalize weather data because required fields are missing."
        }



def calculate_weather_risk_tool(normalized_weather_data: dict[str, Any]) -> dict[str, Any]:
    """Calculates deterministic travel weather risk from normalized weather data.

    Args:
        normalized_weather_data (dict[str, Any]): Normalized weather data.

    Returns:
        dict[str, Any]: Travel risk due to weather, risk factors, and recommended actions. Error message on failure.
    """
    
    try:
        max_temp_c = normalized_weather_data["daily_forecast"][0]["max_temp_c"]
        total_precipitation_mm = normalized_weather_data["daily_forecast"][0]["total_precipitation_mm"]
        max_chance_of_rain = normalized_weather_data["daily_forecast"][0]["max_chance_of_rain"]
        max_wind_kmph = normalized_weather_data["daily_forecast"][0]["max_wind_kmph"]
        
        weather_risk = "LOW"
        risk_factors = []
        recommended_actions = []
        
        if max_temp_c >= 40:
            weather_risk = "HIGH"
            risk_factors.append("Maximum temperature is expected to be above 40°C.")
            recommended_actions.append("Avoid all outdoor activities during peak afternoon hours and stay in air-conditioned environments.")
        elif 35 <= max_temp_c < 40:
            weather_risk = "MEDIUM" if weather_risk != "HIGH" else "HIGH"
            risk_factors.append("Maximum temperature is expected to be above 35°C.")
            recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")

        if total_precipitation_mm >= 20:
            weather_risk = "HIGH"
            risk_factors.append("Accumulation over 20mm creates a high risk of flash flooding.")
            recommended_actions.append("Avoid driving through flooded areas and seek immediate shelter away from trees.")
        elif 5 <= total_precipitation_mm < 20:
            weather_risk = "MEDIUM" if weather_risk != "HIGH" else "HIGH"
            risk_factors.append("5mm to 20mm precipitation expected, causing wet surfaces.")
            recommended_actions.append("Carry an umbrella and allow extra travel time for slippery roads.")
        
        if max_chance_of_rain >= 70:
            weather_risk = "HIGH"
            risk_factors.append("Very high chance of rain may during the forecast period.")
            recommended_actions.append("CPlan outdoor events with a backup indoor location and carry rain protection.")
        elif 40 <= max_chance_of_rain < 70:
            weather_risk = "MEDIUM" if weather_risk != "HIGH" else "HIGH"
            risk_factors.append("Chance of rain may increase during the forecast period.")
            recommended_actions.append("Carry an umbrella and allow extra travel time for slippery roads.")
        
        if max_wind_kmph >= 40:
            weather_risk = "HIGH"
            risk_factors.append("Gusts exceeding 40 km/h risk falling debris and structural damage.")
            recommended_actions.append("Secure loose outdoor objects and avoid driving high-profile vehicles.")
        elif 25 <= max_wind_kmph < 40:
            weather_risk = "MEDIUM" if weather_risk != "HIGH" else "HIGH"
            risk_factors.append("Winds between 25 km/h and 40 km/h expected.")
            recommended_actions.append("Use caution when driving on exposed roads and secure lightweight items.")
        
        return {
            "weather_risk": weather_risk,
            "risk_factors": risk_factors,
            "recommended_actions": recommended_actions
        }
    except Exception as e:
        return {
            "error": str(e)
        }


def save_travel_advisory_tool(report: dict[str, Any]) -> dict[str, Any]:
    try:
        output_path = os.path.join(OUTPUT_DIR, "travel_advisory_report.json")
        with open(str(output_path), 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        return {
            "success": True,
            "saved_path": str(output_path)
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }