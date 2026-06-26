import os
import json
from src.api_client import get_weather_from_wttr


# tool used to for city name validation
def validate_city_input_tool(city_name: str) -> dict:
    if not city_name:
        return {
            "success": False,
            "message": "City name cannot be empty."
        }
        
    cleaned = city_name.strip()
    if not cleaned:
        return {
            "success": False,
            "message": "City name cannot be empty."
        }
        
    if len(cleaned) < 2:
        return {
            "success": False,
            "message": "City name must be at least 2 characters long."
        }
        
    normalized = "+".join([word for word in cleaned.split(" ") if word])
    
    return {
        "success": True,
        "original_city_name": cleaned,
        "normalized_city_name": normalized
    }

def get_weather_forecast_tool(normalized_city_name: str) -> dict:
    res = get_weather_from_wttr(normalized_city_name)
    if res.get("success"):
        return {
            "success": True,
            "city_name": normalized_city_name,
            "raw_weather_data": res.get("raw_weather_data")
        }
    else:
        return {
            "success": False,
            "city_name": normalized_city_name,
            "message": res.get("message", "Unable to fetch weather data.")
        }


# tool used to normalize the weather data collected.
def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
    try:
        area_info = raw_weather_data.get("nearest_area", [{}])[0]
        destination = area_info.get("areaName", [{}])[0].get("value", "Unknown")
        region = area_info.get("region", [{}])[0].get("value", "Unknown")
        country = area_info.get("country", [{}])[0].get("value", "Unknown")
        
        current = raw_weather_data.get("current_condition", [{}])[0]
        current_weather = {
            "temperature_c": float(current.get("temp_C", 0.0)),
            "humidity": int(current.get("humidity", 0)),
            "precipitation_mm": float(current.get("precipMM", 0.0)),
            "wind_speed_kmph": float(current.get("windspeedKmph", 0.0)),
            "weather_description": current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        }
        
        raw_forecasts = raw_weather_data.get("weather", [])[:3]
        daily_forecast = []
        
        for day in raw_forecasts:
            hourly_list = day.get("hourly", [])
            
            max_wind = 0.0
            max_chance_rain = 0.0
            total_precip = 0.0
            
            for hr in hourly_list:
                wind = float(hr.get("windspeedKmph", 0.0))
                chance = float(hr.get("chanceofrain", 0.0))
                precip = float(hr.get("precipMM", 0.0))
                
                if wind > max_wind:
                    max_wind = wind
                if chance > max_chance_rain:
                    max_chance_rain = chance
                total_precip += precip
                
            total_precip = round(total_precip, 2)
            desc = hourly_list[0].get("weatherDesc", [{}])[0].get("value", "Unknown") if hourly_list else "Unknown"
            
            daily_forecast.append({
                "date": day.get("date", ""),
                "max_temp_c": float(day.get("maxtempC", 0.0)),
                "min_temp_c": float(day.get("mintempC", 0.0)),
                "avg_temp_c": float(day.get("avgtempC", 0.0)),
                "total_precipitation_mm": total_precip,
                "max_wind_kmph": max_wind,
                "max_chance_of_rain": max_chance_rain,
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
    except Exception as error:
        return {
            "success": False,
            "message": f"Unable to normalize weather data. Error: {str(error)}"
        }


# tool to calculate the weather risk 
def calculate_weather_risk_tool(normalized_weather_data: dict) -> dict:
    risk_factors = []
    recommended_actions = []
    
    has_high_heat = False
    has_mod_heat = False
    has_high_rain = False
    has_mod_rain = False
    has_high_rain_prob = False
    has_mod_rain_prob = False
    has_high_wind = False
    has_mod_wind = False
    
    daily_forecast = normalized_weather_data.get("daily_forecast", [])
    
    for day in daily_forecast:
        max_temp = day.get("max_temp_c", 0.0)
        total_precip = day.get("total_precipitation_mm", 0.0)
        max_chance_rain = day.get("max_chance_of_rain", 0.0)
        max_wind = day.get("max_wind_kmph", 0.0)
        
        if max_temp >= 40:
            has_high_heat = True
        elif 35 <= max_temp < 40:
            has_mod_heat = True
            
        if total_precip >= 20:
            has_high_rain = True
        elif 5 <= total_precip < 20:
            has_mod_rain = True
            
        if max_chance_rain >= 70:
            has_high_rain_prob = True
        elif 40 <= max_chance_rain < 70:
            has_mod_rain_prob = True
            
        if max_wind >= 40:
            has_high_wind = True
        elif 25 <= max_wind < 40:
            has_mod_wind = True
            
    if has_high_heat:
        risk_factors.append("Extreme heat risk: Maximum temperature is expected to reach 40°C or above.")
        recommended_actions.append("Avoid outdoor exposure during peak afternoon hours and stay hydrated.")
    elif has_mod_heat:
        risk_factors.append("Maximum temperature is expected to be above 35°C.")
        recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")
        recommended_actions.append("Use sun protection if travelling outdoors.")
        
    if has_high_rain:
        risk_factors.append("High rain risk: Heavy precipitation is expected (20mm or above).")
        recommended_actions.append("Avoid non-essential outdoor travel during heavy rain.")
    elif has_mod_rain:
        risk_factors.append("Moderate rain risk: Precipitation is expected (5mm - 20mm).")
        recommended_actions.append("Carry an umbrella or light rain protection.")
        
    if has_high_rain_prob:
        risk_factors.append("High rain probability.")
        if "Carry an umbrella or rain gear." not in recommended_actions:
            recommended_actions.append("Carry an umbrella or rain gear.")
    elif has_mod_rain_prob:
        risk_factors.append("Chance of rain may increase during the forecast period.")
        if "Carry an umbrella or light rain protection." not in recommended_actions and "Carry an umbrella or rain gear." not in recommended_actions:
            recommended_actions.append("Carry an umbrella or light rain protection.")
            
    if has_high_wind:
        risk_factors.append("High wind risk: Wind speeds are expected to be 40 km/h or above.")
        recommended_actions.append("Avoid exposed outdoor areas during high wind conditions.")
    elif has_mod_wind:
        risk_factors.append("Wind speed may be moderately high during the forecast period.")
        recommended_actions.append("Use caution if travelling outdoors.")
        
    is_high = has_high_heat or has_high_rain or has_high_rain_prob or has_high_wind
    is_medium = has_mod_heat or has_mod_rain or has_mod_rain_prob or has_mod_wind
    
    if is_high:
        weather_risk = "HIGH"
    elif is_medium:
        weather_risk = "MEDIUM"
    else:
        weather_risk = "LOW"
        risk_factors.append("No major weather risks identified.")
        recommended_actions.append("Normal travel precautions are enough.")
        
    return {
        "weather_risk": weather_risk,
        "risk_factors": risk_factors,
        "recommended_actions": recommended_actions
    }

## tool to save the travel advisory.
def save_travel_advisory_tool(report: dict) -> dict:
    try:
        output_dir = os.path.dirname("outputs/travel_advisory_report.json")
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        with open("outputs/travel_advisory_report.json", "w") as f:
            json.dump(report, f, indent=2)
            
        return {
            "success": True,
            "saved_path": "outputs/travel_advisory_report.json"
        }
    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to save report: {str(error)}"
        }
