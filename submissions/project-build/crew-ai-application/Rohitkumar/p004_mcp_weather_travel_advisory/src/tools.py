import json
import os
from src.api_client import get_weather_from_wttr
from src.schemas import NormalizedWeatherSchema, CurrentWeatherSchema, DailyForecastSchema


def validate_city_input_tool(city_name: str) -> dict:
    stripped = city_name.strip() if city_name else ""
    if not stripped:
        return {"success": False, "message": "City name cannot be empty."}
    if len(stripped) < 2:
        return {"success": False, "message": "City name must be at least 2 characters."}
    return {"success": True, "original_city_name": stripped, "normalized_city_name": stripped.replace(" ", "+")}


def get_weather_forecast_tool(normalized_city_name: str) -> dict:
    result = get_weather_from_wttr(normalized_city_name)
    if result["success"]:
        return {"success": True, "city_name": normalized_city_name.replace("+", " "), "raw_weather_data": result["raw_weather_data"]}
    return {"success": False, "city_name": normalized_city_name.replace("+", " "), "message": result.get("message", "Unable to fetch weather data.")}


def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
    try:
        area = raw_weather_data.get("nearest_area", [{}])[0]
        curr = raw_weather_data.get("current_condition", [{}])[0]
        days = raw_weather_data.get("weather", [])[:3]

        dest = area.get("areaName", [{}])[0].get("value", "Unknown")
        region = area.get("region", [{}])[0].get("value", "Unknown")
        country = area.get("country", [{}])[0].get("value", "Unknown")

        current = CurrentWeatherSchema(
            temperature_c=float(curr.get("temp_C", 0)),
            humidity=int(curr.get("humidity", 0)),
            precipitation_mm=float(curr.get("precipMM", 0)),
            wind_speed_kmph=float(curr.get("windspeedKmph", 0)),
            weather_description=curr.get("weatherDesc", [{}])[0].get("value", "Unknown")
        )

        daily = []
        for day in days:
            hourly = day.get("hourly", [])
            winds = [float(h.get("windspeedKmph", 0)) for h in hourly]
            rains = [int(h.get("chanceofrain", 0)) for h in hourly]
            precips = [float(h.get("precipMM", 0)) for h in hourly]
            desc = hourly[0].get("weatherDesc", [{}])[0].get("value", "") if hourly else ""

            daily.append(DailyForecastSchema(
                date=day.get("date", ""),
                max_temp_c=float(day.get("maxtempC", 0)),
                min_temp_c=float(day.get("mintempC", 0)),
                avg_temp_c=float(day.get("avgtempC", 0)),
                total_precipitation_mm=sum(precips),
                max_wind_kmph=max(winds) if winds else 0,
                max_chance_of_rain=max(rains) if rains else 0,
                weather_description=desc
            ))

        normalized = NormalizedWeatherSchema(destination=dest, region=region, country=country,
                                             forecast_days=len(daily), current_weather=current, daily_forecast=daily)
        return {"success": True, **normalized.model_dump()}
    except Exception:
        return {"success": False, "message": "Unable to normalize weather data because required fields are missing."}


def calculate_weather_risk_tool(normalized_weather_data: dict) -> dict:
    high = False
    moderate = False
    risk_keys = []

    for day in normalized_weather_data.get("daily_forecast", []):
        t = day.get("max_temp_c", 0)
        p = day.get("total_precipitation_mm", 0)
        r = day.get("max_chance_of_rain", 0)
        w = day.get("max_wind_kmph", 0)

        if t >= 40:
            high = True; risk_keys.append("heat_high")
        elif t >= 35:
            moderate = True; risk_keys.append("heat_moderate")

        if p >= 20:
            high = True; risk_keys.append("rain_high")
        elif p >= 5:
            moderate = True; risk_keys.append("rain_moderate")

        if r >= 70:
            high = True; risk_keys.append("rain_chance_high")
        elif r >= 40:
            moderate = True; risk_keys.append("rain_chance_moderate")

        if w >= 40:
            high = True; risk_keys.append("wind_high")
        elif w >= 25:
            moderate = True; risk_keys.append("wind_moderate")

    risk_keys = list(dict.fromkeys(risk_keys))
    risk = "HIGH" if high else ("MEDIUM" if moderate else "LOW")

    return {"weather_risk": risk, "risk_keys": risk_keys}


def save_travel_advisory_tool(report: dict) -> dict:
    output_path = os.getenv("OUTPUT_PATH", "outputs")
    os.makedirs(output_path, exist_ok=True)
    file_path = os.path.join(output_path, "travel_advisory_report.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return {"success": True, "saved_path": file_path}