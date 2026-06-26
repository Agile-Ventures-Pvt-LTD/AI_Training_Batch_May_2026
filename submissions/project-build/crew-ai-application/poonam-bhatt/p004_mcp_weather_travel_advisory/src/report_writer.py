import os
from src.schemas import TravelAdvisoryReport, CurrentWeather, DailyForecast


def build_travel_advisory_report(
    normalized_data: dict,
    risk_assessment: dict,
    packing_suggestions: list,
    travel_readiness_advisory: str,
    weather_risk_explanation: str
) -> dict:
    current = normalized_data.get("current_weather", {})
    current_weather_obj = CurrentWeather(
        temperature_c=current.get("temperature_c", 0.0),
        humidity=current.get("humidity", 0),
        precipitation_mm=current.get("precipitation_mm", 0.0),
        wind_speed_kmph=current.get("wind_speed_kmph", 0.0),
        weather_description=current.get("weather_description", "")
    )
    
    daily_list = []
    for day in normalized_data.get("daily_forecast", []):
        daily_list.append(DailyForecast(
            date=day.get("date", ""),
            max_temp_c=day.get("max_temp_c", 0.0),
            min_temp_c=day.get("min_temp_c", 0.0),
            avg_temp_c=day.get("avg_temp_c", 0.0),
            total_precipitation_mm=day.get("total_precipitation_mm", 0.0),
            max_wind_kmph=day.get("max_wind_kmph", 0.0),
            max_chance_of_rain=day.get("max_chance_of_rain", 0.0),
            weather_description=day.get("weather_description", "")
        ))
        
    report = TravelAdvisoryReport(
        destination=normalized_data.get("destination", ""),
        region=normalized_data.get("region", ""),
        country=normalized_data.get("country", ""),
        forecast_days=normalized_data.get("forecast_days", 0),
        current_weather=current_weather_obj,
        daily_forecast=daily_list,
        weather_risk=risk_assessment.get("weather_risk", "LOW"),
        risk_factors=risk_assessment.get("risk_factors", []),
        recommended_actions=risk_assessment.get("recommended_actions", []),
        packing_suggestions=packing_suggestions,
        travel_readiness_advisory=travel_readiness_advisory,
        weather_risk_explanation=weather_risk_explanation
    )
    
    return report.model_dump()
