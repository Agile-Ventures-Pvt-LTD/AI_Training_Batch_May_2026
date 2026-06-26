import os
import json
from dotenv import load_dotenv
from api_client import get_weather_from_wttr

load_dotenv()
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "outputs")

def validate_city_input_tool(city_name: str) -> dict:
    if not city_name or not str(city_name).strip():
        return {"success": False, "message": "City name cannot be empty."}
    cleaned = str(city_name).strip()
    if len(cleaned) < 2:
        return {
            "success": False,
            "message": "City name must be at least 2 characters long."
        }
    normalized = cleaned.replace(" ", "+")
    
    return {
        "success": True,
        "original_city_name": city_name,
        "normalized_city_name": normalized
    }

def get_weather_forecast_tool(normalized_city_name: str) -> dict:
    if not normalized_city_name or not normalized_city_name.strip():
        return {
            "success": False,
            "city_name": normalized_city_name,
            "message": "Normalized city name cannot be empty."
        }
    result = get_weather_from_wttr(normalized_city_name)
    if result.get("success"):
        return {
            "success": True,
            "city_name": normalized_city_name,
            "raw_weather_data": result["raw_weather_data"]
        }
    return {
        "success": False,
        "city_name": normalized_city_name,
        "message": result.get("message", "Unable to fetch weather data.")
    }

def _safe_float(value, default=0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def _safe_int(value, default=0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default

def _safe_str_from_list(lst, key="value", default="Unknown") -> str:
    try:
        if lst and isinstance(lst, list) and len(lst) > 0:
            return str(lst[0].get(key, default))
        return default
    except (TypeError, IndexError, AttributeError):
        return default

def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
    try:
        if not raw_weather_data or not isinstance(raw_weather_data, dict):
            return {"success": False, "message": "Unable to normalize weather data because required fields are missing."}
            
        nearest_area = raw_weather_data.get("nearest_area", [])
        if not nearest_area:
            return {"success": False, "message": "Unable to normalize weather data because required fields are missing."}
        
        area = nearest_area[0]
        destination = _safe_str_from_list(area.get("areaName", []))
        region = _safe_str_from_list(area.get("region", []))
        country = _safe_str_from_list(area.get("country", []))
        current_conditions = raw_weather_data.get("current_condition", [])
        if not current_conditions:
            return {"success": False, "message": "Unable to normalize weather data because required fields are missing."}
            
        current = current_conditions[0]
        current_weather = {
            "temperature_c": _safe_float(current.get("temp_C")),
            "humidity": _safe_int(current.get("humidity")),
            "precipitation_mm": _safe_float(current.get("precipMM")),
            "wind_speed_kmph": _safe_float(current.get("windspeedKmph")),
            "weather_description": _safe_str_from_list(current.get("weatherDesc", []))
        }
        weather_days = raw_weather_data.get("weather", [])
        daily_forecast = []
        
        for day in weather_days[:3]:
            hourly = day.get("hourly", [])
            wind_speeds = [_safe_float(h.get("windspeedKmph")) for h in hourly]
            rain_chances = [_safe_int(h.get("chanceofrain")) for h in hourly]
            precip_values = [_safe_float(h.get("precipMM")) for h in hourly]
            max_wind = max(wind_speeds) if wind_speeds else 0.0
            max_rain_chance = max(rain_chances) if rain_chances else 0
            total_precip = sum(precip_values) if precip_values else 0.0
            weather_desc = "Unknown"
            if hourly:
                weather_desc = _safe_str_from_list(hourly[0].get("weatherDesc", []))
                
            daily_forecast.append({
                "date": str(day.get("date", "")),
                "max_temp_c": _safe_float(day.get("maxtempC")),
                "min_temp_c": _safe_float(day.get("mintempC")),
                "avg_temp_c": _safe_float(day.get("avgtempC")),
                "total_precipitation_mm": round(total_precip, 2),
                "max_wind_kmph": max_wind,
                "max_chance_of_rain": max_rain_chance,
                "weather_description": weather_desc
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
    except Exception as e:
        return {
            "success": False,
            "message": f"Unable to normalize weather data because required fields are missing. Error: {str(e)}"
        }

def calculate_weather_risk_tool(normalized_weather_data: dict) -> dict:
    try:
        daily_forecast = normalized_weather_data.get("daily_forecast", [])
        if not daily_forecast:
            return {
                "weather_risk": "LOW",
                "risk_factors": ["No forecast data available for risk assessment."],
                "recommended_actions": ["Check weather forecast closer to travel date."]
            }
        risk_factors = []
        recommended_actions = []
        has_high = False
        has_moderate = False
        
        for day in daily_forecast:
            max_temp = day.get("max_temp_c", 0)
            total_precip = day.get("total_precipitation_mm", 0)
            max_rain_chance = day.get("max_chance_of_rain", 0)
            max_wind = day.get("max_wind_kmph", 0)
            if max_temp >= 40:
                has_high = True
                if "Extreme heat conditions are expected during the forecast period." not in risk_factors:
                    risk_factors.append("Extreme heat conditions are expected during the forecast period.")
                if "Avoid outdoor exposure during peak afternoon hours." not in recommended_actions:
                    recommended_actions.append("Avoid outdoor exposure during peak afternoon hours.")
            elif max_temp >= 35:
                has_moderate = True
                if "Maximum temperature is expected to be above 35°C." not in risk_factors:
                    risk_factors.append("Maximum temperature is expected to be above 35°C.")
                if "Carry water and avoid long outdoor exposure during afternoon hours." not in recommended_actions:
                    recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")
            if total_precip >= 20:
                has_high = True
                if "Heavy precipitation is expected during the forecast period." not in risk_factors:
                    risk_factors.append("Heavy precipitation is expected during the forecast period.")
                if "Avoid outdoor activities during heavy rain." not in recommended_actions:
                    recommended_actions.append("Avoid outdoor activities during heavy rain.")
            elif total_precip >= 5:
                has_moderate = True
                if "Moderate precipitation is expected during the forecast period." not in risk_factors:
                    risk_factors.append("Moderate precipitation is expected during the forecast period.")
                if "Carry an umbrella or light rain protection." not in recommended_actions:
                    recommended_actions.append("Carry an umbrella or light rain protection.")
            if max_rain_chance >= 70:
                has_high = True
                if "High probability of rain during the forecast period." not in risk_factors:
                    risk_factors.append("High probability of rain during the forecast period.")
                if "Plan indoor activities as backup options." not in recommended_actions:
                    recommended_actions.append("Plan indoor activities as backup options.")
            elif max_rain_chance >= 40:
                has_moderate = True
                if "Chance of rain may increase during the forecast period." not in risk_factors:
                    risk_factors.append("Chance of rain may increase during the forecast period.")
                if "Carry an umbrella or light rain protection." not in recommended_actions:
                    recommended_actions.append("Carry an umbrella or light rain protection.")
            if max_wind >= 40:
                has_high = True
                if "High wind speeds are expected during the forecast period." not in risk_factors:
                    risk_factors.append("High wind speeds are expected during the forecast period.")
                if "Avoid exposed outdoor areas during high wind conditions." not in recommended_actions:
                    recommended_actions.append("Avoid exposed outdoor areas during high wind conditions.")
            elif max_wind >= 25:
                has_moderate = True
                if "Wind speed may be moderately high during the forecast period." not in risk_factors:
                    risk_factors.append("Wind speed may be moderately high during the forecast period.")
                if "Secure loose items and be cautious in open areas." not in recommended_actions:
                    recommended_actions.append("Secure loose items and be cautious in open areas.")
        if has_high:
            weather_risk = "HIGH"
        elif has_moderate:
            weather_risk = "MEDIUM"
        else:
            weather_risk = "LOW"
        if weather_risk == "LOW":
            risk_factors = ["No major heat, rain, or wind indicators detected."]
            recommended_actions = ["Normal travel precautions are sufficient."]
        return {
            "weather_risk": weather_risk,
            "risk_factors": risk_factors,
            "recommended_actions": recommended_actions
        }
    except Exception as e:
        return {
            "weather_risk": "LOW",
            "risk_factors": [f"Unable to calculate risk: {str(e)}"],
            "recommended_actions": ["Check weather forecast manually."]
        }

def save_travel_advisory_tool(report: dict) -> dict:
    try:
        output_dir = OUTPUT_PATH
        os.makedirs(output_dir, exist_ok=True)
        saved_path = os.path.join(output_dir, "travel_advisory_report.json")
        
        with open(saved_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return {"success": True, "saved_path": saved_path}
    except Exception as e:
        return {"success": False, "message": f"Failed to save report: {str(e)}"}