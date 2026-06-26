import os
import json
from .api_client import get_weather_from_wttr

def validate_city_input(city_name: str) -> dict:
    if not city_name or not isinstance(city_name, str):
        return {"success": False, "message": "City name cannot be empty."}
    
    cleaned = city_name.strip()
    if not cleaned:
        return {"success": False, "message": "City name cannot be empty."}
    if len(cleaned) < 2:
        return {"success": False, "message": "City name must be at least 2 characters long."}
        
    normalized = cleaned.replace(" ", "+")
    return {
        "success": True,
        "original_city_name": cleaned,
        "normalized_city_name": normalized
    }
    
def get_weather_forecast(normalized_city_name: str) -> dict:
    result = get_weather_from_wttr(normalized_city_name)
    if not result["success"]:
        return {
            "success": False,
            "city_name": normalized_city_name,
            "message": "Unable to fetch weather data."
        }
    return {
        "success": True,
        "city_name": normalized_city_name,
        "raw_weather_data": result["raw_weather_data"]
    }
    

def normalize_weather_data(raw_weather_data: dict) -> dict:
    try:
        current_cond = raw_weather_data["current_condition"][0]
        nearest_area = raw_weather_data["nearest_area"][0]
        weather_days = raw_weather_data.get("weather", [])
        
        destination = nearest_area["areaName"][0]["value"]
        region = nearest_area["region"][0]["value"]
        country = nearest_area["country"][0]["value"]
        
        current_weather = {
            "temperature_c": float(current_cond["temp_C"]),
            "humidity": int(current_cond["humidity"]),
            "precipitation_mm": float(current_cond["precipMM"]),
            "wind_speed_kmph": float(current_cond["windspeedKmph"]),
            "weather_description": current_cond["weatherDesc"][0]["value"]
        }
        
        daily_forecast = []
        for day in weather_days[:3]:
            hourly = day.get("hourly", [])
            
            max_wind = 0.0
            max_rain_chance = 0
            total_precip = 0.0
            
            for hour in hourly:
                max_wind = max(max_wind, float(hour.get("windspeedKmph", 0)))
                max_rain_chance = max(max_rain_chance, int(hour.get("chanceofrain", 0)))
                total_precip += float(hour.get("precipMM", 0))
                
            desc = hourly[0]["weatherDesc"][0]["value"] if hourly else "Unknown"
            
            daily_forecast.append({
                "date": day["date"],
                "max_temp_c": float(day["maxtempC"]),
                "min_temp_c": float(day["mintempC"]),
                "avg_temp_c": float(day["avgtempC"]),
                "total_precipitation_mm": round(total_precip, 2),
                "max_wind_kmph": max_wind,
                "max_chance_of_rain": max_rain_chance,
                "weather_description": desc
            })
            
        return {
            "success": True,
            "destination": destination,
            "region": region,
            "country": country,
            "forecast_days": len(daily_forecast),
            "current_weather": current_weather,
            "daily_forecast": daily_forecast
        }
    except (KeyError, IndexError, ValueError, TypeError):
        return {
            "success": False,
            "message": "Unable to normalize weather data because required fields are missing."
        }

def calculate_weather_risk(normalized_weather_data: dict) -> dict:
    risk_factors = []
    recommended_actions = []
    is_high = False
    is_medium = False
    
    for day in normalized_weather_data.get("daily_forecast", []):
        max_temp = day.get("max_temp_c", 0)
        total_precip = day.get("total_precipitation_mm", 0)
        max_rain_chance = day.get("max_chance_of_rain", 0)
        max_wind = day.get("max_wind_kmph", 0)
        
        if max_temp >= 40:
            is_high = True
            if "Maximum temperature is expected to be 40°C or above." not in risk_factors:
                risk_factors.append("Maximum temperature is expected to be 40°C or above.")
                recommended_actions.append("Avoid outdoor activities during peak afternoon hours. Stay hydrated.")
        elif max_temp >= 35:
            is_medium = True
            if "Maximum temperature is expected to be above 35°C." not in risk_factors:
                risk_factors.append("Maximum temperature is expected to be above 35°C.")
                recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")
                
        if total_precip >= 20:
            is_high = True
            if "Heavy precipitation is expected." not in risk_factors:
                risk_factors.append("Heavy precipitation is expected.")
                recommended_actions.append("Avoid travel if possible. Carry heavy rain gear.")
        elif total_precip >= 5:
            is_medium = True
            if "Moderate precipitation is expected." not in risk_factors:
                risk_factors.append("Moderate precipitation is expected.")
                recommended_actions.append("Carry an umbrella or light rain protection.")
                
        if max_rain_chance >= 70:
            is_high = True
            if "High probability of rain." not in risk_factors:
                risk_factors.append("High probability of rain.")
                recommended_actions.append("Plan indoor activities. Carry waterproof gear.")
        elif max_rain_chance >= 40:
            is_medium = True
            if "Chance of rain may increase during the forecast period." not in risk_factors:
                risk_factors.append("Chance of rain may increase during the forecast period.")
                recommended_actions.append("Carry an umbrella or light rain protection.")
                
        if max_wind >= 40:
            is_high = True
            if "High wind speeds expected." not in risk_factors:
                risk_factors.append("High wind speeds expected.")
                recommended_actions.append("Avoid exposed outdoor areas and secure loose items.")
        elif max_wind >= 25:
            is_medium = True
            if "Wind speed may be moderately high during the forecast period." not in risk_factors:
                risk_factors.append("Wind speed may be moderately high during the forecast period.")
                recommended_actions.append("Be cautious in open areas.")
                
    if is_high:
        risk_level = "HIGH"
    elif is_medium:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
        risk_factors.append("No major weather risks identified.")
        recommended_actions.append("Normal travel precautions are sufficient.")
        
    return {
        "weather_risk": risk_level,
        "risk_factors": risk_factors,
        "recommended_actions": recommended_actions
    }

def save_travel_advisory(report: dict) -> dict:
    output_dir = os.getenv("OUTPUT_PATH", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "travel_advisory_report.json")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        return {"success": True, "saved_path": file_path.replace("\\", "/")}
    except Exception as e:
        return {"success": False, "message": f"Failed to save report: {str(e)}"}