import logging

from fastmcp import FastMCP

try:
    from src.api_client import get_weather_from_wttr
    from src.report_writer import save_report
    from src.schemas import (
        NormalizedWeather,
        RiskResponse,
        TravelReport,
        ValidationResponse,
        WeatherRisk,
    )
except ModuleNotFoundError:
    from api_client import get_weather_from_wttr
    from report_writer import save_report
    from schemas import (
        NormalizedWeather,
        RiskResponse,
        TravelReport,
        ValidationResponse,
        WeatherRisk,
    )

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool
    def validate_city_input_tool(city_name: str) -> dict:
        city = city_name.strip()

        if not city:
            return ValidationResponse(
                success=False,
                message="City name cannot be empty.",
            ).model_dump()

        if len(city) < 2:
            return ValidationResponse(
                success=False,
                message="City name must contain at least 2 characters.",
            ).model_dump()

        return ValidationResponse(
            success=True,
            original_city_name=city,
            normalized_city_name=city.replace(" ", "+"),
        ).model_dump()

    @mcp.tool
    def get_weather_forecast_tool(normalized_city_name: str) -> dict:
        response = get_weather_from_wttr(normalized_city_name)
        return response.model_dump()

    @mcp.tool
    def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
        try:
            area = raw_weather_data["nearest_area"][0]
            current = raw_weather_data["current_condition"][0]
            weather = raw_weather_data["weather"][:3]

            daily_forecast = []

            for day in weather:
                hourly = day.get("hourly", [])

                winds = [
                    float(hour.get("windspeedKmph", 0))
                    for hour in hourly
                ]

                rain = [
                    int(hour.get("chanceofrain", 0))
                    for hour in hourly
                ]

                precipitation = [
                    float(hour.get("precipMM", 0))
                    for hour in hourly
                ]

                description = (
                    hourly[0]["weatherDesc"][0]["value"]
                    if hourly
                    else current["weatherDesc"][0]["value"]
                )

                daily_forecast.append(
                    {
                        "date": day["date"],
                        "max_temp_c": float(day["maxtempC"]),
                        "min_temp_c": float(day["mintempC"]),
                        "avg_temp_c": float(day["avgtempC"]),
                        "total_precipitation_mm": sum(precipitation),
                        "max_wind_kmph": max(winds, default=0.0),
                        "max_chance_of_rain": max(rain, default=0),
                        "weather_description": description,
                    }
                )

            normalized = NormalizedWeather(
                destination=area["areaName"][0]["value"],
                region=area["region"][0]["value"],
                country=area["country"][0]["value"],
                forecast_days=len(daily_forecast),
                current_weather={
                    "temperature_c": float(current["temp_C"]),
                    "humidity": int(current["humidity"]),
                    "precipitation_mm": float(current["precipMM"]),
                    "wind_speed_kmph": float(current["windspeedKmph"]),
                    "weather_description": current["weatherDesc"][0]["value"],
                },
                daily_forecast=daily_forecast,
            )

            return normalized.model_dump()

        except (KeyError, IndexError, TypeError, ValueError):
            logger.exception("Weather normalization failed")

            return {
                "success": False,
                "message": (
                    "Unable to normalize weather data because "
                    "required fields are missing."
                ),
            }
    @mcp.tool
    def calculate_weather_risk_tool(normalized_weather_data: dict) -> dict:
        risk = WeatherRisk.LOW
        risk_factors: list[str] = []
        recommended_actions: list[str] = []

        for day in normalized_weather_data["daily_forecast"]:
            if day["max_temp_c"] >= 40:
                risk = WeatherRisk.HIGH
                risk_factors.append(
                    "Maximum temperature is expected to reach 40°C or higher."
                )
                recommended_actions.append(
                    "Avoid prolonged outdoor exposure during peak afternoon hours."
                )

            elif day["max_temp_c"] >= 35 and risk != WeatherRisk.HIGH:
                risk = WeatherRisk.MEDIUM
                risk_factors.append(
                    "Maximum temperature is expected to be above 35°C."
                )
                recommended_actions.append(
                    "Carry water and stay hydrated."
                )

            if day["total_precipitation_mm"] >= 20:
                risk = WeatherRisk.HIGH
                risk_factors.append(
                    "Heavy rainfall is expected."
                )
                recommended_actions.append(
                    "Carry waterproof gear."
                )

            elif (
                day["total_precipitation_mm"] >= 5
                and risk != WeatherRisk.HIGH
            ):
                risk = WeatherRisk.MEDIUM
                risk_factors.append(
                    "Moderate rainfall is expected."
                )
                recommended_actions.append(
                    "Carry an umbrella."
                )

            if day["max_chance_of_rain"] >= 70:
                risk = WeatherRisk.HIGH
                risk_factors.append(
                    "Rain probability is very high."
                )
                recommended_actions.append(
                    "Plan indoor activities where possible."
                )

            elif (
                day["max_chance_of_rain"] >= 40
                and risk != WeatherRisk.HIGH
            ):
                risk = WeatherRisk.MEDIUM
                risk_factors.append(
                    "Rain probability is moderately high."
                )
                recommended_actions.append(
                    "Keep rain protection available."
                )

            if day["max_wind_kmph"] >= 40:
                risk = WeatherRisk.HIGH
                risk_factors.append(
                    "Strong winds are expected."
                )
                recommended_actions.append(
                    "Avoid exposed outdoor areas."
                )

            elif (
                day["max_wind_kmph"] >= 25
                and risk != WeatherRisk.HIGH
            ):
                risk = WeatherRisk.MEDIUM
                risk_factors.append(
                    "Moderately strong winds are expected."
                )
                recommended_actions.append(
                    "Secure loose belongings outdoors."
                )

        response = RiskResponse(
            weather_risk=risk,
            risk_factors=list(dict.fromkeys(risk_factors)),
            recommended_actions=list(dict.fromkeys(recommended_actions)),
        )

        return response.model_dump()

    @mcp.tool
    def save_travel_advisory_tool(report: dict) -> dict:
        try:
            validated_report = TravelReport.model_validate(report)
            return save_report(validated_report)

        except Exception:
            logger.exception("Report validation failed")

            return {
                "success": False,
                "message": "Final report schema validation failed.",
            }
            
def get_registered_tools() -> dict:
    class DummyMCP:
        def __init__(self):
            self.tools = {}

        def tool(self, func):
            self.tools[func.__name__] = func
            return func

    mcp = DummyMCP()
    register_tools(mcp)
    return mcp.tools