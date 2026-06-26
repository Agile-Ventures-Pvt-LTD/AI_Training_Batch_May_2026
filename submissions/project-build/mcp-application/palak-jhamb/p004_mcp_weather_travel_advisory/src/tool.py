from pathlib import Path
import requests
from mcp_use.server import MCPRouter

router = MCPRouter()



class WeatherAPIError(RuntimeError):
    """Raised when WeatherAPI returns an error or an unexpected response."""


@router.tool
async def validate_city_input_tool(city: str)->dict:
    """It is a tool that is used to validate input by user input before fetching the data.
    Args:
        city: original place 

    Returns:
        A dictionary containing validated input for url.
    """
    try:
        if not city:
            return{
                "success": False,
                "message": "City name cannot be empty."
            }
        if len(city)<=2:
            return{
                "success": False,
                "message": "City name cannot be too small."
            }
        text=city
        words = text.strip().split()
        validated_city='+'.join(words)
        return{
            "success": True,
            "original_city_name": city,
            "normalized_city_name": validated_city
        }
    except Exception as e:
        print(f"Input is not valid,",e)
        return{
            "success": False,
            "message": "City name cannot be empty."
        }
    

@router.tool
async def get_weather_forecast_tool(city:str)->dict:
    """
    It is a tool used to get weather of a city.
    Args:
        city: location

    Returns:
        A dictionary containing fetched data.

    """
    try:
        validation=validate_city_input_tool(city)
        validated_city=validation.get("normalized_city_name")
        url = f"https://wttr.in/{validated_city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()
        if isinstance(data, dict) and "error" in data:
            err = data["error"] or {}
            code = err.get("code")
            msg = err.get("message", "Unknown WeatherAPI error")
            raise WeatherAPIError(f"WeatherAPI error (code={code}): {msg}")
        if not isinstance(data, dict) or "weather" not in data:
            raise WeatherAPIError("Unexpected response shape from WeatherAPI.")
        return {
            "success": True,
            "city_name": "Jaipur",
            "raw_weather_data": data
        }
    except Exception as e:
        print(f"got an error in fetching data {e}")
        return{
        "success": False,
        "city_name": "InvalidCity",
        "message": "Unable to fetch weather data."
        }
    

@router.tool
async def normalize_weather_data_tool(raw_weather_data:dict)->dict:
    try:
        if  not raw_weather_data:
            return{
            "success": False,
            "message": "Unable to normalize weather data because required fields are missing."
            }
        else:
            return{
                "success": True,
                "destination":raw_weather_data.get("nearest_area[0].areaName[0].value","Not provided") ,
                "region": raw_weather_data.get("nearest_area[0].region[0].value","Not provided"),
                "country": raw_weather_data.get("nearest_area[0].country[0].value","Not provided"),
                "current_weather": raw_weather_data.get("current_condition[0]","not provided"),
            }
    except Exception as e:
        print(f"got an error in fetching data {e}")
        return{ 
            "success": False,
            "message": "Unable to normalize weather data because required fields are missing."
        }
@router.tool
async def calculate_weather_risk_tool(data:dict):
    """Calculates deterministic travel weather risk from normalized weather data."""
    try:
        risk=[]
        if data["daily_forecast"][0]["max_temp_c"] >= 40:
            risk.append("High")
        if ["daily_forecast"][0]["max_temp_c"]>=35 and ["daily_forecast"][0]["max_temp_c"]<40:
            risk.append("Moderate")
        if data["daily_forecast"][0]["total_precipitation_mm"]>=20:
            risk.append("High")
        if data["daily_forecast"][0]["total_precipitation_mm"]>=5 and data["daily_forecast"][0]["total_precipitation_mm"]<20:
            risk.append("Moderate")
        if data["daily_forecast"][0]["max_chance_of_rain"]>=70:
            risk.append("High")
        if data["daily_forecast"][0]["max_chance_of_rain"]>=40 and data["daily_forecast"][0]["max_chance_of_rain"]<70:
            risk.append("Moderate")
        if data["daily_forecast"][0]["max_wind_kmph"]>=40:
            risk.append("High")
        if  data["daily_forecast"][0]["max_wind_kmph"]<40 and data["daily_forecast"][0]["max_wind_kmph"]>=25:
            risk.append("Moderate")

        if len(risk)==0:
            return{
                "weather_risk": "LOW"
            }
        text="High"
        if text in risk:
            return{
                "weather_risk": "High"
            }
        text="Moderate"
        if text in risk:
            return{
                "weather_risk": "Moderate"
            }
    except Exception as e:
        print(f"got an error in calculation risk {e}") 

import json   

@router.tool
async def save_travel_advisory_tool(response):
    """Saves the final advisory report as JSON."""

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "travel_advisory_report.json"

    with open(output_file, "w") as f:
        json.dump(response, f, indent=4)