import re
import os
import json
import requests
from typing import Dict, Any, List

def validate_city_input_tool(city_name: str) -> Dict[str, Any]:
    """Validates and clean user input city string."""
    clean = city_name.strip()
    if not clean:
        return {"success": False, "message": "City name cannot be empty."}
    if len(clean) < 2:
        return {"success": False, "message": "City name must contain at least 2 characters."}
    
    normalized = re.sub(r'\s+', '+', clean)
    return {
        "success": True,
        "original_city_name": clean,
        "normalized_city_name": normalized
    }

def weather_forecast_tool(normalized_city_name:str) -> Dict[str,Any]:
    """Extract raw JSON weather records using primary and fallback endpoints."""
    primary_url = os.getenv ("WTTR_PRIMARY_URL","https://wttr.in")
    fallback_url = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")

    urls= [f"{primary_url}/{normalized_city_name}?format=j1",
           f"{fallback_url}/{normalized_city_name}?format=j1"]
    
    last_error = "No attempt made"
    for url in urls:
        try:
            response = requests.get(url,timeout=10)
            if response.status_code == 200:
                return {
                    "success":True,
                    "url_used":url,
                    "city_name":normalized_city_name.replace("+"," "),
                    "raw_weather_data":response.json()
                }
        except Exception as error:
            last_error = str(error)

    return {
        "success":False,
        "city_name":normalized_city_name,
        "message":f"Unable to fetch weather data. Last error:{last_error}"
    }

def normalize_weather_data_tool(raw_data:Dict[str,any]) -> Dict[str,Any]:
    """Normalizes complex string raw API outputs into our standard data schema."""
    try:
        nearest = raw_data['nearest_area'][0]
        current = raw_data['current_condition'][0]
        weather_days = raw_data['weather'][:3]

        current_weather = {
            "temperature_c": float(current["temp_C"]),
            "humidity": int(current["humidity"]),
            "precipitation_mm": float(current["precipMM"]),
            "wind_speed_kmph": float(current["windspeedKmph"]),
            "weather_description": current["weatherDesc"][0]["value"]
        } 

        daily_forecast = []
        for day in weather_days:
            hourly_list = day["hourly"]
            max_wind = max(float(h["windspeedKmph"]) for h in hourly_list)
            max_rain_chance = max(int(h["chanceofrain"]) for h in hourly_list)
            total_precip = sum(float(h["precipMM"]) for h in hourly_list)

            daily_forecast.append({
                "date": day["date"],
                "max_temp_c": float(day["maxtempC"]),
                "min_temp_c": float(day["mintempC"]),
                "avg_temp_c": float(day["avgtempC"]),
                "total_precipitation_mm": round(total_precip, 2),
                "max_wind_kmph": max_wind,
                "max_chance_of_rain": max_rain_chance,
                "weather_description": hourly_list[0]["weatherDesc"][0]["value"]
            })

        return{
            "success":True,
            "destination":nearest["areaName"][0]["value"],
            "region": nearest["region"][0]["value"],
            "country": nearest["country"][0]["value"],
            "forecast_days": len(daily_forecast),
            "current_weather": current_weather,
            "daily_forecast": daily_forecast
        }
    except (KeyError, IndexError):
        return {"success": False, "message": "Unable to normalize weather data because required fields are missing."}
    
def calculate_weather_risk_tool(normalized_data:Dict[str,any]) -> Dict[str,any]:
    """Runs deterministic safety logic to rules against weather metrics."""
    risk_factors = []
    recommended_actions = []

    for day in normalized_data.get("daily_forecast",[]):
        if day['max_temp_c']>=40:
            if "Maximum temperature is expected to be critically high (>= 40°C)." not in risk_factors:
                risk_factors.append("Maximum temperature is expected to be critically high (>= 40°C).")
                recommended_actions.append("Avoid long outdoor exposure during afternoon hours and maximize hydration(Drink more water).")
        elif day['max_temp_c'] >= 35:
            if "Maximum temperature is expected to be above 35°C." not in risk_factors:
                risk_factors.append("Maximum temperature is expected to be above 35°C.")
                recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")
        
        if day["total_precipitation_mm"] >= 20:
            if "Heavy precipitation expected (>= 20mm)." not in risk_factors:
                risk_factors.append("Heavy precipitation expected (>= 20mm).")
                recommended_actions.append("Plan for significant indoor delays or alter travel schedules.")
        elif day["total_precipitation_mm"] >= 5:
            if "Moderate rain risk expected." not in risk_factors:
                risk_factors.append("Moderate rain risk expected.")
                recommended_actions.append("Carry an umbrella or rain protection.")
        
        if day["max_chance_of_rain"] >= 70:
            if "High rain probability detected." not in risk_factors:
                risk_factors.append("High rain probability detected.")
        elif day["max_chance_of_rain"] >= 40:
            if "Chance of rain may increase during the forecast period." not in risk_factors:
                risk_factors.append("Chance of rain may increase during the forecast period.")

        if day["max_wind_kmph"] >= 40:
            if "High wind risk detected." not in risk_factors:
                risk_factors.append("High wind risk detected.")
                recommended_actions.append("Avoid exposed outdoor or structural elevated zones.")
        elif day["max_wind_kmph"] >= 25:
            if "Wind speed may be moderately high during the forecast period." not in risk_factors:
                risk_factors.append("Wind speed may be moderately high during the forecast period.")
                recommended_actions.append("Secure loose objects or outdoor items.")

    is_high = any("critically high" in f or "Heavy precipitation" in f or "High wind" in f or "High rain probability" in f for f in risk_factors)
    is_med = len(risk_factors) > 0 and not is_high
    
    risk_level = "HIGH" if is_high else ("MEDIUM" if is_med else "LOW")
    if risk_level == "LOW":
        risk_factors.append("No major heat, rain, or wind threat thresholds breached.")
        recommended_actions.append("Standard baseline destination safety rules apply.")
        
    return {
        "weather_risk": risk_level,
        "risk_factors": risk_factors,
        "recommended_actions": list(set(recommended_actions))
    }

def save_travel_advisory_tool(report_data: Dict[str, Any]) -> Dict[str, Any]:
    """Writes the compiled analytics report data to disk storage safely."""
    output_dir = os.getenv("OUTPUT_PATH", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "travel_advisory_report.json")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        return {"success": True, "saved_path": file_path}
    except Exception as e:
        return {"success": False, "message": f"Failed in writing report : {str(e)}"}