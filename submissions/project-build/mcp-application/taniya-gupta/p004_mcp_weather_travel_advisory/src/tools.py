import os
import json
from pathlib import Path
from api_client import get_weather
from dotenv import load_dotenv

load_dotenv()

def validate_city_input_tool(city_name):
    if not city_name:
        return {
            "success" : False,
            "message" : "City name cant be empty"
        }
    cleaned_name= city_name.strip()
    normalized= city_name.replace(" ", "+")
    if len(cleaned_name)<2:
        return{
            "success" : False,
            "message" : "City name has to be more than 2 characters"
        }
    return {
        "success" : True,
        "original_city_name" : city_name,
        "normalized_city_name" : normalized
    }

def get_weather_forecast_tool(normalized_city_name):
    result= get_weather(normalized_city_name)
    return {
        "success": True,
        "city_name": normalized_city_name,
        "raw_weather_data": result.get("raw_weather_data")
    }

def normalize_weather_data_tool(raw_weather_data):
    nearest_list = raw_weather_data.get("nearest_area", [])
    nearest = nearest_list[0] if nearest_list else {}
    
    area_name_list = nearest.get("areaName", [])
    destination = area_name_list[0].get("value") if area_name_list else ""
    
    region_list = nearest.get("region", [])
    region = region_list[0].get("value") if region_list else ""
    
    country_list = nearest.get("country", [])
    country = country_list[0].get("value") if country_list else ""

    current_list = raw_weather_data.get("current_condition", [])
    current = current_list[0] if current_list else {}
    
    temp_c = float(current.get("temp_C", 0.0)) if current.get("temp_C") is not None else 0.0
    humidity = float(current.get("humidity", 0.0)) if current.get("humidity") is not None else 0.0
    precip = float(current.get("precipMM", 0.0)) if current.get("precipMM") is not None else 0.0
    wind_speed = float(current.get("windspeedKmph", 0.0)) if current.get("windspeedKmph") is not None else 0.0
    
    weather_desc_list = current.get("weatherDesc", [])
    weather_desc = weather_desc_list[0].get("value") if weather_desc_list else ""

    raw_weather = raw_weather_data.get("weather", [])
    daily_forecasts = []

    for day in raw_weather[:3]:
        date_str = day.get("date")
        max_temp = float(day.get("maxtempC", 0.0))
        min_temp = float(day.get("mintempC", 0.0))
        avg_temp = float(day.get("avgtempC", 0.0))
        
        hourly_list = day.get("hourly", [])
        
        max_wind = max((float(h.get("windspeedKmph", 0.0)) for h in hourly_list), default=0.0)
        max_chance_of_rain = max((int(h.get("chanceofrain", 0)) for h in hourly_list), default=0)
        total_precip = sum(float(h.get("precipMM", 0.0)) for h in hourly_list)
        
        desc = ""
        if hourly_list:
            weather_desc_sublist = hourly_list[0].get("weatherDesc", [])
            desc = weather_desc_sublist[0].get("value") if weather_desc_sublist else ""
        if not desc:
            desc = weather_desc
            
        daily_forecasts.append({
            "date": date_str,
            "max_temp_c": max_temp,
            "min_temp_c": min_temp,
            "avg_temp_c": avg_temp,
            "total_precipitation_mm": total_precip,
            "max_wind_kmph": max_wind,
            "max_chance_of_rain": max_chance_of_rain,
            "weather_description": desc
        })
        
    return {
        "success": True,
        "destination": destination,
        "region": region,
        "country": country,
        "forecast_days": len(daily_forecasts),
        "current_weather": {
            "temperature_c": temp_c,
            "humidity": humidity,
            "precipitation_mm": precip,
            "wind_speed_kmph": wind_speed,
            "weather_description": weather_desc
        },
        "daily_forecast": daily_forecasts
    }
    

def calculate_weather_risk_tool(normalized_weather_data):
    risk_factors=[]
    recommended_actions=[]

    high=False
    moderate=False

    daily_forecasts = normalized_weather_data.get("daily_forecast")
    
    max_temps = [day.get("max_temp_c") for day in daily_forecasts]
    total_precips = [day.get("total_precipitation_mm") for day in daily_forecasts]
    max_chances = [day.get("max_chance_of_rain") for day in daily_forecasts]
    max_winds = [day.get("max_wind_kmph") for day in daily_forecasts]
    
    if any(t >= 40 for t in max_temps):
        high = True
        risk_factors.append("Max temperature is expected to be above 40°C.")
        recommended_actions.append("Extreme heat expected. Avoid outdoor activities during peak afternoon hours")
    elif any(35 <= t < 40 for t in max_temps):
        moderate = True
        risk_factors.append("Maximum temperature is expected to be above 35°C.")
        recommended_actions.append("Carry water and avoid long outdoor exposure")
        
    if any(p >= 20 for p in total_precips):
        high = True
        risk_factors.append("Heavy precipitation is expected ")
        recommended_actions.append("Reconsider non-essential outdoor travel ")
    elif any(5 <= p < 20 for p in total_precips):
        moderate = True
        risk_factors.append("Moderate rain is expected ")
        recommended_actions.append("Carry an umbrella.")
        
    if any(c >= 70 for c in max_chances):
        high = True
        risk_factors.append("High probability of rain ")
        recommended_actions.append("Keep essentials handy")
    elif any(40 <= c < 70 for c in max_chances):
        moderate = True
        risk_factors.append("Chance of rain may increase ")
        if "Carry an umbrella or light rain protection." not in recommended_actions:
            recommended_actions.append("Carry an umbrella or light rain protection.")
            
    if any(w >= 40 for w in max_winds):
        high = True
        risk_factors.append("High wind speeds are expected.")
        recommended_actions.append("Avoid exposed outdoor areas")
    elif any(25 <= w < 40 for w in max_winds):
        moderate = True
        risk_factors.append("Wind speed may be moderately high ")
        recommended_actions.append("Use sun protection if travelling outdoors")
        
    if high:
        risk_level = "HIGH"
    elif moderate:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
        risk_factors.append("No major heat, rain or wind indicators")
        recommended_actions.append("Normal precautions are enough")
        
    return {
        "weather_risk": risk_level,
        "risk_factors": risk_factors,
        "recommended_actions": recommended_actions
    }

def save_travel_advisory_tool(report):
    output_path_env = os.getenv("OUTPUT_PATH")
    output_dir = Path(output_path_env)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "travel_advisory_report.json"
    
    
    with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
    return {
            "success": True,
            "saved_path": f"outputs/travel_advisory_report.json"
        }
    


    
        