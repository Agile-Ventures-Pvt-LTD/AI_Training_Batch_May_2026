import os
import json
import requests
from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("Weather Travel Advisory Tools")

@mcp_server.tool(name="validate_city_input_tool")
def validate_city_input_tool(city_name: str) -> str:
    """Validates and sanitizes the user-entered city name."""
    if not city_name:
        return json.dumps({"success": False, "message": "City name cannot be empty."})
    
    cleaned = city_name.strip()
    if len(cleaned) < 2:
        return json.dumps({"success": False, "message": "City name must be at least 2 characters long."})
    
    normalized = "+".join(cleaned.split())
    return json.dumps({
        "success": True,
        "original_city_name": cleaned,
        "normalized_city_name": normalized
    })


@mcp_server.tool(name="get_weather_forecast_tool")
def get_weather_forecast_tool(normalized_city_name: str) -> str:
    """Calls wttr.in JSON API securely and handles structural network issues."""
    url = f"https://wttr.in/{normalized_city_name}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return json.dumps({
                "success": False, 
                "city_name": normalized_city_name, 
                "message": f"Server responded with code {response.status_code}"
            })
        
        return json.dumps({
            "success": True,
            "city_name": normalized_city_name,
            "raw_weather_data": response.json()
        })
    except (requests.exceptions.RequestException, ValueError) as e:
        return json.dumps({
            "success": False,
            "city_name": normalized_city_name,
            "message": f"Unable to fetch weather data. Error: {str(e)}"
        })

@mcp_server.tool(name="normalize_weather_data_tool")
def normalize_weather_data_tool(raw_weather_data_json: str) -> str:
    """Converts deep wttr.in JSON response into a flattened internal schema with accurate type conversions."""
    try:
        raw_weather_data = json.loads(raw_weather_data_json)
        
        area = raw_weather_data.get("nearest_area", [{}])[0] if raw_weather_data.get("nearest_area") else {}
        current = raw_weather_data.get("current_condition", [{}])[0] if raw_weather_data.get("current_condition") else {}
        weather_list = raw_weather_data.get("weather", [])
        
        destination = area.get("areaName", [{}])[0].get("value", "") if area.get("areaName") else ""
        region = area.get("region", [{}])[0].get("value", "") if area.get("region") else ""
        country = area.get("country", [{}])[0].get("value", "") if area.get("country") else ""
        
        if not destination or not weather_list:
            raise KeyError("Missing critical meteorology index points.")
            
        current_weather = {
            "temperature_c": float(current.get("temp_C", 0.0)),
            "humidity": int(current.get("humidity", 0)),
            "precipitation_mm": float(current.get("precipMM", 0.0)),
            "wind_speed_kmph": float(current.get("windspeedKmph", 0.0)),
            "weather_description": current.get("weatherDesc", [{}])[0].get("value", "Unknown") if current.get("weatherDesc") else "Unknown"
        }
        
        daily_forecast = []
        for day in weather_list[:3]: 
            hourly = day.get("hourly", [])
            
            max_wind = max([float(h.get("windspeedKmph", 0.0)) for h in hourly]) if hourly else 0.0
            max_rain_chance = max([int(h.get("chanceofrain", 0)) for h in hourly]) if hourly else 0
            total_precip = sum([float(h.get("precipMM", 0.0)) for h in hourly]) if hourly else 0.0
            
            desc = hourly[0].get("weatherDesc", [{}])[0].get("value", "Unknown") if (hourly and hourly[0].get("weatherDesc")) else "Unknown"
            
            daily_forecast.append({
                "date": day.get("date", ""),
                "max_temp_c": float(day.get("maxtempC", 0.0)),
                "min_temp_c": float(day.get("mintempC", 0.0)),
                "avg_temp_c": float(day.get("avgtempC", 0.0)),
                "total_snow_cm": float(day.get("totalSnow_cm", 0.0)), # Tracked from 7.5 manifest requirement
                "total_precipitation_mm": round(total_precip, 2),
                "max_wind_kmph": max_wind,
                "max_chance_of_rain": max_rain_chance,
                "weather_description": desc
            })
            
        return json.dumps({
            "success": True,
            "destination": destination,
            "region": region,
            "country": country,
            "forecast_days": len(daily_forecast),
            "current_weather": current_weather,
            "daily_forecast": daily_forecast
        })
        
    except (IndexError, KeyError, TypeError, ValueError) as e:
        return json.dumps({
            "success": False,
            "message": f"Unable to normalize weather data because required fields are missing or type conversions failed. Error: {str(e)}"
        })



@mcp_server.tool(name="calculate_weather_risk_tool")
def calculate_weather_risk_tool(normalized_weather_data_json: str) -> str:
    """Evaluates weather patterns to flag explicit travel risks mathematically."""
    try:
        normalized_weather_data = json.loads(normalized_weather_data_json)
        risk_factors = []
        recommended_actions = []
        
        has_high = False
        has_medium = False
        
        for day in normalized_weather_data.get("daily_forecast", []):
            max_temp = day["max_temp_c"]
            total_precip = day["total_precipitation_mm"]
            rain_chance = day["max_chance_of_rain"]
            max_wind = day["max_wind_kmph"]
            
            if max_temp >= 40:
                has_high = True
                if "High heat risk" not in risk_factors:
                    risk_factors.append("High heat risk")
                    recommended_actions.append("Stay indoors during peak hours and stay heavily hydrated.")
            elif 35 <= max_temp < 40:
                has_medium = True
                if "Moderate heat risk" not in risk_factors:
                    risk_factors.append("Moderate heat risk")
                    recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")
                    
            if total_precip >= 20:
                has_high = True
                if "High rain risk" not in risk_factors:
                    risk_factors.append("High rain risk")
                    recommended_actions.append("Expect severe flooding or travel disruptions; monitor local alerts.")
            elif 5 <= total_precip < 20:
                has_medium = True
                if "Moderate rain risk" not in risk_factors:
                    risk_factors.append("Moderate rain risk")
                    recommended_actions.append("Carry robust rain gear and expect minor delays.")
                    
            if rain_chance >= 70:
                has_high = True
                if "High rain probability" not in risk_factors:
                    risk_factors.append("High rain probability")
                    recommended_actions.append("Heavy downpours likely; plan indoor alternatives.")
            elif 40 <= rain_chance < 70:
                has_medium = True
                if "Moderate rain probability" not in risk_factors:
                    risk_factors.append("Moderate rain probability")
                    recommended_actions.append("Carry an umbrella or light rain protection.")
                    
            if max_wind >= 40:
                has_high = True
                if "High wind risk" not in risk_factors:
                    risk_factors.append("High wind risk")
                    recommended_actions.append("Secure loose items and expect potential transit infrastructure closures.")
            elif 25 <= max_wind < 40:
                has_medium = True
                if "Moderate wind risk" not in risk_factors:
                    risk_factors.append("Moderate wind risk")
                    recommended_actions.append("Be cautious during outdoor high-elevation excursions.")

        if has_high:
            overall_risk = "HIGH"
        elif has_medium:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "LOW"
            risk_factors.append("No significant weather risks identified.")
            recommended_actions.append("Enjoy your trip!")

        return json.dumps({
            "weather_risk": overall_risk,
            "risk_factors": risk_factors,
            "recommended_actions": list(set(recommended_actions))
        })
    except Exception as e:
        return json.dumps({"success": False, "message": f"Risk calculation runtime failure: {str(e)}"})


@mcp_server.tool(name="save_travel_advisory_tool")
def save_travel_advisory_tool(report_json: str) -> str:
    """Persists the finished analytical JSON data payload locally using a city-specific filename."""
    try:
        report = json.loads(report_json)
        safe_city_name = "".join(c for c in report.get("destination", "unknown").lower() if c.isalnum() or c in (' ', '_')).replace(' ', '_')
        saved_path = f"outputs/travel_advisory_report_{safe_city_name}.json"
        
        os.makedirs(os.path.dirname(saved_path), exist_ok=True)
        with open(saved_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        return json.dumps({
            "success": True,
            "saved_path": saved_path
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": f"Failed to write file structure to disk. Error: {str(e)}"
        })
