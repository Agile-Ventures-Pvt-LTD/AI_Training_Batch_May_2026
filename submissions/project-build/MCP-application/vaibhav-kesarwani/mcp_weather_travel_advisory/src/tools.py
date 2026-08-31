import os
import json
import requests
from dotenv import load_dotenv
from typing import Any, Dict, List
from utils import to_float, to_int
from schemas import (
    CityInput,
    CityOutput
)

load_dotenv()


def validate_city_input(data: CityInput) -> CityOutput:
    cleaned = data.city_name.strip()

    if not cleaned:
        return CityOutput(success=False, message="City name cannot be empty.")

    if len(cleaned) < 2:
        return CityOutput(success=False, message="City name must be at least 2 characters long.")

    normalized = "+".join(cleaned.split())

    return CityOutput(
        success=True,
        original_city_name=cleaned,
        normalized_city_name=normalized
    )


WTTR_PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")

def get_weather_from_wttr(normalized_city_name: str) -> dict:
    urls = [
        f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
        f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1"
    ]

    last_error = None

    for url in urls:
        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                last_error = f"status code: {response.status_code}"
                continue

            try:
                weather_data = response.json()

                result = {
                    "success": True,
                    "city_name": normalized_city_name.replace("+", " "),
                    "url_used": url,
                    "raw_weather_data": weather_data
                }

                with open("tools_outputs/raw_weather.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)

            except ValueError:
                last_error = "Invalid JSON response"
                continue

            return result

        except Exception as e:
            last_error = str(e)

    return {
        "success": False,
        "city_name": normalized_city_name.replace("+", " "),
        "message": f"Unable to fetch weather data. Error -> {last_error}"
    }


def normalize_weather_data(raw_weather_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        nearest_area = raw_weather_data.get("nearest_area", [{}])[0]
        destination = nearest_area.get("areaName", [{}])[0].get("value")
        region = nearest_area.get("region", [{}])[0].get("value")
        country = nearest_area.get("country", [{}])[0].get("value")

        current = raw_weather_data.get("current_condition", [{}])[0]
        current_weather = {
            "temperature_c": to_float(current.get("temp_C")),
            "humidity": to_int(current.get("humidity")),
            "precipitation_mm": to_float(current.get("precipMM")),
            "wind_speed_kmph": to_float(current.get("windspeedKmph")),
            "weather_description": (
                current.get("weatherDesc", [{}])[0].get("value") or "Unknown"
            )
        }

        weather_days = raw_weather_data.get("weather", [])
        daily_forecast: List[Dict[str, Any]] = []

        for day in weather_days[:3]:
            date = day.get("date")
            max_temp_c = to_float(day.get("maxtempC"))
            min_temp_c = to_float(day.get("mintempC"))
            avg_temp_c = to_float(day.get("avgtempC"))

            hourly_data = day.get("hourly", [])
            max_wind_kmph = max(
                (to_float(h.get("windspeedKmph")) or 0) for h in hourly_data
            ) if hourly_data else None

            max_chance_of_rain = max(
                (to_int(h.get("chanceofrain")) or 0) for h in hourly_data
            ) if hourly_data else None

            total_precipitation_mm = sum(
                (to_float(h.get("precipMM")) or 0.0) for h in hourly_data
            ) if hourly_data else None

            weather_description = (
                hourly_data[0].get("weatherDesc", [{}])[0].get("value")
                if hourly_data else "Unknown"
            )

            daily_forecast.append({
                "date": date,
                "max_temp_c": max_temp_c,
                "min_temp_c": min_temp_c,
                "avg_temp_c": avg_temp_c,
                "total_precipitation_mm": total_precipitation_mm,
                "max_wind_kmph": max_wind_kmph,
                "max_chance_of_rain": max_chance_of_rain,
                "weather_description": weather_description
            })


        if not destination or not region or not country:
            return {
                "success": False,
                "message": "Required fields are missing."
            }

        result = {
            "success": True,
            "destination": destination,
            "region": region,
            "country": country,
            "forecast_days": len(daily_forecast),
            "current_weather": current_weather,
            "daily_forecast": daily_forecast
        }

        
        with open("tools_outputs/normalize_weather.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        return result

    except Exception as e:
        return {
            "success": False,
            "message": f"Erorr -> {str(e)}"
        }


def assess_weather_risk(normalized_weather: Dict[str, Any]) -> Dict[str, Any]:
    try:
        forecast = normalized_weather.get("daily_forecast", [])
        if not forecast:
            return {
                "success": False,
                "message": "No forecast data available."
            }

        risk_factors: List[str] = []
        recommended_actions: List[str] = []
        high_risk = False
        moderate_risk = False

        for day in forecast:
            max_temp = day.get("max_temp_c")
            max_rain_chance = day.get("max_chance_of_rain")
            max_wind = day.get("max_wind_kmph")

            if max_temp is not None:
                if max_temp >= 40:
                    high_risk = True
                    risk_factors.append("Extreme heat expected (>= 40°C).")
                    recommended_actions.append("Avoid outdoor activities during peak heat hours.")
                elif max_temp > 35:
                    moderate_risk = True
                    risk_factors.append("Maximum temperature is expected to be above 35°C.")
                    recommended_actions.append("Carry water and avoid long outdoor exposure during afternoon hours.")

            if max_rain_chance is not None:
                if max_rain_chance >= 70:
                    high_risk = True
                    risk_factors.append("High probability of heavy rain (>= 70%).")
                    recommended_actions.append("Carry waterproof clothing and avoid flood areas.")
                elif max_rain_chance >= 40:
                    moderate_risk = True
                    risk_factors.append("Chance of rain may increase during the forecast period.")
                    recommended_actions.append("Carry an umbrella.")

            if max_wind is not None:
                if max_wind >= 40:
                    high_risk = True
                    risk_factors.append("Strong winds expected (>= 40 km/h).")
                    recommended_actions.append("Secure loose outdoor items and avoid tall structures.")
                elif max_wind >= 25:
                    moderate_risk = True
                    risk_factors.append("Moderate wind speeds expected (25-39 km/h).")
                    recommended_actions.append("Just a Normal wind speed you cna go outside.")

        if high_risk:
            weather_risk = "HIGH"
        elif moderate_risk:
            weather_risk = "MEDIUM"
        else:
            weather_risk = "LOW"

        result = {
            "success": True,
            "weather_risk": weather_risk,
            "risk_factors": risk_factors,
            "recommended_actions": recommended_actions
        }

        with open("tools_outputs/assess_weather_risk.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        return result

    except Exception as e:
        return {
            "success": False,
            "message": f"Error -> {str(e)}"
        }
