from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from api_client import get_weather_from_wttr
logger = logging.getLogger(__name__)
def validate_city_input_tool(city_name: str) -> Dict[str, Any]:
    """
    Validates and normalizes city name.
    Rules:
    - Cannot be empty
    - Minimum 2 characters
    - Strip spaces
    - Convert spaces to +
    """
    try:
        if city_name is None:
            return {"success": False,"message": "City name cannot be empty."}
        cleaned = city_name.strip()
        if not cleaned:
            return {"success": False,"message": "City name cannot be empty."}
        if len(cleaned) < 2:
            return {"success": False,"message": "City name must contain at least 2 characters."}
        normalized = "+".join(cleaned.split())
        return {"success": True,"original_city_name": cleaned,"normalized_city_name": normalized}
    except Exception as exc:
        logger.exception("City validation failed")
        return {"success": False,"message": f"Validation error: {str(exc)}"}
def get_weather_forecast_tool(normalized_city_name: str) -> Dict[str, Any]:
    """
    Fetch weather forecast from wttr.in API.
    """
    try:
        result = get_weather_from_wttr(normalized_city_name)
        if not result.get("success"):
            return {
                "success": False,
                "city_name": normalized_city_name,
                "message": result.get(
                    "message",
                    "Unable to fetch weather data."
                )
            }

        return {
            "success": True,
            "city_name": normalized_city_name,
            "raw_weather_data": result["raw_weather_data"]
        }

    except Exception as exc:
        logger.exception("Weather API error")

        return {
            "success": False,
            "city_name": normalized_city_name,
            "message": str(exc)
        }
def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default

def normalize_weather_data_tool(raw_weather_data: Dict[str, Any])-> Dict[str, Any]:
    """
    Convert wttr.in response into PRD schema.
    """
    try:
        current = raw_weather_data["current_condition"][0]
        nearest = raw_weather_data["nearest_area"][0]
        weather_data = raw_weather_data["weather"][:3]
        normalized = {
            "success": True,
            "destination": nearest["areaName"][0]["value"],
            "region": nearest["region"][0]["value"],
            "country": nearest["country"][0]["value"],
            "forecast_days": min(3, len(weather_data)),
            "current_weather": {
                "temperature_c": _safe_float(current["temp_C"]),
                "humidity": _safe_int(current["humidity"]),
                "precipitation_mm": _safe_float(
                    current["precipMM"]
                ),
                "wind_speed_kmph": _safe_float(
                    current["windspeedKmph"]
                ),
                "weather_description":
                    current["weatherDesc"][0]["value"]
            },
            "daily_forecast": []
        }
        for day in weather_data:
            hourly = day.get("hourly", [])
            max_wind = max(
                (
                    _safe_float(
                        h.get("windspeedKmph", 0)
                    )
                    for h in hourly
                ),
                default=0.0
            )

            max_rain_chance = max(
                (
                    _safe_int(
                        h.get("chanceofrain", 0)
                    )
                    for h in hourly
                ),
                default=0
            )

            total_precip = sum(
                _safe_float(h.get("precipMM", 0))
                for h in hourly
            )

            description = ""

            if hourly:
                description = (
                    hourly[0]
                    .get("weatherDesc", [{}])[0]
                    .get("value", "")
                )

            normalized["daily_forecast"].append({
                "date": day.get("date"),
                "max_temp_c":
                    _safe_float(day.get("maxtempC", 0)),
                "min_temp_c":
                    _safe_float(day.get("mintempC", 0)),
                "avg_temp_c":
                    _safe_float(day.get("avgtempC", 0)),
                "total_precipitation_mm": total_precip,
                "max_wind_kmph": max_wind,
                "max_chance_of_rain": max_rain_chance,
                "weather_description": description
            })

        return normalized

    except Exception:
        logger.exception("Weather normalization failed")

        return {
            "success": False,
            "message": (
                "Unable to normalize weather data "
                "because required fields are missing."
            )
        }
def calculate_weather_risk_tool(
    normalized_weather_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Deterministic risk calculator.
    """

    risk_factors: List[str] = []
    recommendations: List[str] = []

    has_high = False
    has_medium = False

    try:
        forecasts = normalized_weather_data.get(
            "daily_forecast",
            []
        )

        for day in forecasts:

            max_temp = day["max_temp_c"]
            precip = day["total_precipitation_mm"]
            rain_chance = day["max_chance_of_rain"]
            wind = day["max_wind_kmph"]
            if max_temp >= 40:
                has_high = True
                risk_factors.append(
                    "Maximum temperature is expected "
                    "to exceed 40°C."
                )
                recommendations.append(
                    "Avoid prolonged outdoor exposure "
                    "during peak afternoon hours."
                )
            elif 35 <= max_temp < 40:
                has_medium = True
                risk_factors.append(
                    "Maximum temperature is expected "
                    "to be above 35°C."
                )
                recommendations.append(
                    "Carry water and stay hydrated."
                )
            if precip >= 20:
                has_high = True

                risk_factors.append(
                    "Heavy rainfall may occur."
                )

                recommendations.append(
                    "Carry rain protection."
                )

            elif 5 <= precip < 20:
                has_medium = True

                risk_factors.append(
                    "Moderate rainfall is expected."
                )

                recommendations.append(
                    "Keep an umbrella available."
                )

            
            if rain_chance >= 70:
                has_high = True

                risk_factors.append(
                    "Rain probability is very high."
                )

            elif 40 <= rain_chance < 70:
                has_medium = True

                risk_factors.append(
                    "Chance of rain may increase "
                    "during the forecast period."
                )
            if wind >= 40:
                has_high = True

                risk_factors.append(
                    "Strong winds are expected."
                )

                recommendations.append(
                    "Avoid exposed outdoor areas."
                )

            elif 25 <= wind < 40:
                has_medium = True

                risk_factors.append(
                    "Wind speed may be moderately high "
                    "during the forecast period."
                )

        if has_high:
            level = "HIGH"
        elif has_medium:
            level = "MEDIUM"
        else:
            level = "LOW"

        if level == "LOW":
            recommendations.append(
                "Normal travel precautions are sufficient."
            )

        return {
            "weather_risk": level,
            "risk_factors": list(set(risk_factors)),
            "recommended_actions": list(set(recommendations))
        }

    except Exception as exc:
        logger.exception("Risk calculation failed")

        return {
            "weather_risk": "LOW",
            "risk_factors": [f"Calculation error: {str(exc)}"],
            "recommended_actions": [
                "Review weather forecast manually."
            ]
        }
def save_travel_advisory_tool(
    report: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Saves final advisory report.

    Output:
        outputs/travel_advisory_report.json
    """

    try:
        output_dir = Path("outputs")
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = (
            output_dir /
            "travel_advisory_report.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as fp:
            json.dump(
                report,
                fp,
                indent=4,
                ensure_ascii=False
            )

        return {
            "success": True,
            "saved_path": str(file_path)
        }

    except Exception as exc:
        logger.exception("Report save failure")

        return {
            "success": False,
            "message": str(exc)
        }