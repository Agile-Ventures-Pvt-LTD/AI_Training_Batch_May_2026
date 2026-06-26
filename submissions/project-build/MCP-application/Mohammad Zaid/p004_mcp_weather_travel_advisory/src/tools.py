# src/tools.py
import re
from fastmcp import FastMCP
from api_client import get_weather_from_wttr

def register_tools(mcp: FastMCP):
    @mcp.tool(description="Validates the city name entered by the user and normalizes it for the API.")
    async def validate_city_input_tool(city_name: str) -> dict:
        if not city_name or not isinstance(city_name, str):
            return {"success": False, "message": "City name cannot be empty."}
        cleaned = city_name.strip()
        if len(cleaned) < 2:
            return {"success": False, "message": "City name cannot be empty."}
        if not re.match(r"^[a-zA-Z\s\-\']+$", cleaned):
            return {"success": False, "message": "City name contains invalid characters."}
        normalized = cleaned.replace(" ", "+")
        return {"success": True, "original_city_name": cleaned, "normalized_city_name": normalized}

    @mcp.tool(description="Calls the wttr.in JSON API and returns the raw weather response.")
    async def get_weather_forecast_tool(normalized_city_name: str) -> dict:
        result = get_weather_from_wttr(normalized_city_name)
        if result.get("success"):
            return {
                "success": True,
                "city_name": normalized_city_name.replace("+", " "),
                "raw_weather_data": result["raw_weather_data"]
            }
        return {
            "success": False,
            "city_name": normalized_city_name.replace("+", " "),
            "message": result.get("message", "Unable to fetch weather data.")
        }

    @mcp.tool(description="Converts raw wttr.in JSON into a clean internal weather schema.")
    async def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
        try:
            area = raw_weather_data.get("nearest_area", [{}])[0]
            current = raw_weather_data.get("current_condition", [{}])[0]
            
            destination = area.get("areaName", [{}])[0].get("value", "Unknown")
            region = area.get("region", [{}])[0].get("value", "Unknown")
            country = area.get("country", [{}])[0].get("value", "Unknown")
            
            current_weather = {
                "temperature_c": float(current.get("temp_C", 0)),
                "humidity": int(current.get("humidity", 0)),
                "precipitation_mm": float(current.get("precipMM", 0)),
                "wind_speed_kmph": float(current.get("windspeedKmph", 0)),
                "weather_description": current.get("weatherDesc", [{}])[0].get("value", "Unknown")
            }
            
            daily_forecast = []
            weather_days = raw_weather_data.get("weather", [])[:3]
            
            for day in weather_days:
                hourly = day.get("hourly", [])
                max_wind = max([int(h.get("windspeedKmph", 0)) for h in hourly]) if hourly else 0
                max_rain = max([int(h.get("chanceofrain", 0)) for h in hourly]) if hourly else 0
                total_precip = sum([float(h.get("precipMM", 0)) for h in hourly]) if hourly else 0.0
                
                daily_forecast.append({
                    "date": day.get("date", ""),
                    "max_temp_c": float(day.get("maxtempC", 0)),
                    "min_temp_c": float(day.get("mintempC", 0)),
                    "avg_temp_c": float(day.get("avgtempC", 0)),
                    "total_precipitation_mm": total_precip,
                    "max_wind_kmph": max_wind,
                    "max_chance_of_rain": max_rain,
                    "weather_description": hourly[0].get("weatherDesc", [{}])[0].get("value", "Unknown") if hourly else "Unknown"
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
            return {"success": False, "message": "Unable to normalize weather data because required fields are missing."}

    @mcp.tool(description="Calculates deterministic travel weather risk from normalized weather data.")
    async def calculate_weather_risk_tool(normalized_weather_data: dict) -> dict:
        try:
            risk_factors = []
            recommended_actions = []
            has_high = False
            has_moderate = False
            
            for day in normalized_weather_data.get("daily_forecast", []):
                max_temp = day.get("max_temp_c", 0)
                precip = day.get("total_precipitation_mm", 0)
                rain_chance = day.get("max_chance_of_rain", 0)
                wind = day.get("max_wind_kmph", 0)
                
                if max_temp >= 40:
                    has_high = True
                    risk_factors.append("Maximum temperature is expected to be above 40°C.")
                    recommended_actions.append("Avoid outdoor travel completely during peak afternoon hours.")
                elif max_temp >= 35:
                    has_moderate = True
                    risk_factors.append("Maximum temperature is expected to be above 35°C.")
                    recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")
                    
                if precip >= 20:
                    has_high = True
                    risk_factors.append("Heavy precipitation is expected.")
                    recommended_actions.append("Carry sturdy rain protection and avoid waterlogged areas.")
                elif precip >= 5:
                    has_moderate = True
                    risk_factors.append("Moderate precipitation is expected.")
                    recommended_actions.append("Carry an umbrella or light rain protection.")
                    
                if rain_chance >= 70:
                    has_high = True
                    risk_factors.append("High chance of rain during the forecast period.")
                    recommended_actions.append("Be prepared for sudden downpours.")
                elif rain_chance >= 40:
                    has_moderate = True
                    risk_factors.append("Chance of rain may increase during the forecast period.")
                    recommended_actions.append("Keep rain gear accessible.")
                    
                if wind >= 40:
                    has_high = True
                    risk_factors.append("High wind speed detected in the forecast.")
                    recommended_actions.append("Avoid exposed outdoor areas and lightweight tents.")
                elif wind >= 25:
                    has_moderate = True
                    risk_factors.append("Wind speed may be moderately high during the forecast period.")
                    recommended_actions.append("Secure loose items and use wind protection if travelling outdoors.")

            if has_high:
                weather_risk = "HIGH"
            elif has_moderate:
                weather_risk = "MEDIUM"
            else:
                weather_risk = "LOW"
                
            if not risk_factors:
                risk_factors.append("No significant weather risks detected.")
                recommended_actions.append("Standard travel precautions are sufficient.")
                
            return {
                "weather_risk": weather_risk,
                "risk_factors": risk_factors,
                "recommended_actions": recommended_actions
            }
        except Exception as e:
            return {"weather_risk": "UNKNOWN", "risk_factors": ["Risk calculation failed."], "recommended_actions": []}