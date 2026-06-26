import re
from typing import Dict, Any
from api_client import get_weather_from_wttr

def validate_city_input_tool(city_name: str) -> dict:
    """Validates and processes the city name input entered by the user."""
    if not city_name or not city_name.strip():
        return {"success": False, "message": "City name cannot be empty."}
    
    cleaned = city_name.strip()
    if len(cleaned) < 2:
        return {"success": False, "message": "City name must be at least 2 characters long."}
    
    normalized = re.sub(r'\s+', '+', cleaned)
    return {
        "success": True,
        "original_city_name": cleaned,
        "normalized_city_name": normalized
    }

def get_weather_forecast_tool(normalized_city_name: str) -> dict:
    """Use the internal API client functionality to fetch weather forecasts."""
    result = get_weather_from_wttr(normalized_city_name)
    if not result.get("success"):
        return {
            "success": False,
            "city_name": normalized_city_name,
            "message": result.get("message", "Unable to fetch weather data.")
        }
    return {
        "success": True,
        "city_name": normalized_city_name,
        "raw_weather_data": result["raw_weather_data"]
    }

def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
    """Converts complex, raw wttr.in JSON structure to an internal clean weather schema."""
    try:
        nearest = raw_weather_data["nearest_area"][0]
        current = raw_weather_data["current_condition"][0]
        weather_list = raw_weather_data["weather"]
        
        destination = nearest["areaName"][0]["value"]
        region = nearest["region"][0]["value"]
        country = nearest["country"][0]["value"]
        
        current_weather = {
            "temperature_c": float(current["temp_C"]),
            "humidity": int(current["humidity"]),
            "precipitation_mm": float(current["precipMM"]),
            "wind_speed_kmph": float(current["windspeedKmph"]),
            "weather_description": current["weatherDesc"][0]["value"]
        }
        
        daily_forecast = []
        for day in weather_list[:3]:
            hourly = day["hourly"]
            
            max_wind = max(float(h["windspeedKmph"]) for h in hourly)
            max_rain_chance = max(int(h["chanceofrain"]) for h in hourly)
            total_precip = sum(float(h["precipMM"]) for h in hourly)
            
            daily_forecast.append({
                "date": day["date"],
                "max_temp_c": float(day["maxtempC"]),
                "min_temp_c": float(day["mintempC"]),
                "avg_temp_c": float(day["avgtempC"]),
                "total_precipitation_mm": round(total_precip, 2),
                "max_wind_kmph": float(max_wind),
                "max_chance_of_rain": int(max_rain_chance),
                "weather_description": hourly[0]["weatherDesc"][0]["value"]
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
    except (KeyError, IndexError, ValueError):
        return {
            "success": False,
            "message": "Unable to normalize weather data because required fields are missing."
        }

def calculate_weather_risk_tool(normalized_weather_data: dict) -> dict:
    """Processes deterministic rules to evaluate weather-based travel disruptions."""
    risk_factors = []
    recommended_actions = []
    
    curr = normalized_weather_data["current_weather"]
    if curr["temperature_c"] >= 40:
        risk_factors.append("High heat risk detected currently.")
    elif curr["temperature_c"] >= 35:
        risk_factors.append("Moderate heat risk detected currently.")
    

    for day in normalized_weather_data["daily_forecast"]:
        if day["max_temp_c"] >= 40:
            if "High heat risk" not in "".join(risk_factors):
                risk_factors.append("High heat risk expected during the forecast period.")
                recommended_actions.append("Avoid long outdoor exposure and stay hydrated.")
        elif day["max_temp_c"] >= 35:
            if "Moderate heat risk" not in "".join(risk_factors):
                risk_factors.append("Maximum temperature is expected to be above 35°C.")
                recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")
                
        if day["total_precipitation_mm"] >= 20:
            risk_factors.append(f"High rain risk on {day['date']}.")
            recommended_actions.append("Expect major travel delays, carry heavy rain gear.")
        elif day["total_precipitation_mm"] >= 5:
            risk_factors.append(f"Moderate rain risk on {day['date']}.")
            recommended_actions.append("Carry an umbrella or light rain protection.")
            
        if day["max_chance_of_rain"] >= 70:
            risk_factors.append("High rain probability.")
        elif day["max_chance_of_rain"] >= 40:
            if "Chance of rain" not in "".join(risk_factors):
                risk_factors.append("Chance of rain may increase during the forecast period.")
                
        if day["max_wind_kmph"] >= 40:
            risk_factors.append("High wind risk.")
            recommended_actions.append("Avoid open environments or temporary structural setups.")
        elif day["max_wind_kmph"] >= 25:
            if "Wind speed" not in "".join(risk_factors):
                risk_factors.append("Wind speed may be moderately high during the forecast period.")
                recommended_actions.append("Secure loose properties and execute caution while driving.")


    risk_factors = list(set(risk_factors))
    recommended_actions = list(set(recommended_actions))

    if not recommended_actions:
        recommended_actions.append("No specific high/moderate risks; preserve basic precautions.")

   
    is_high = any("High" in f for f in risk_factors)
    is_med = any("Moderate" in f or "above 35°C" in f or "Chance of rain" in f or "Wind speed" in f for f in risk_factors)
    
    if is_high:
        risk_level = "HIGH"
    elif is_med:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
        risk_factors.append("No major heat, rain, or wind indicators.")
        
    return {
        "weather_risk": risk_level,
        "risk_factors": risk_factors,
        "recommended_actions": recommended_actions
    }
