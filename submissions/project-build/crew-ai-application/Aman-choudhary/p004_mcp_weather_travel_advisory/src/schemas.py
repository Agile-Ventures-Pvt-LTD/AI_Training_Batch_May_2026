from __future__ import annotations
from typing import List, Literal
from pydantic import BaseModel, Field
class CurrentWeather(BaseModel):
    temperature_c: float = Field(..., ge=-100, le=100)
    humidity: int = Field(..., ge=0, le=100)
    precipitation_mm: float = Field(..., ge=0)
    wind_speed_kmph: float = Field(..., ge=0)
    weather_description: str
class DailyForecast(BaseModel):
    date: str
    max_temp_c: float
    min_temp_c: float
    avg_temp_c: float
    total_precipitation_mm: float
    max_wind_kmph: float
    max_chance_of_rain: int
    weather_description: str
class WeatherRisk(BaseModel):
    weather_risk: Literal["LOW", "MEDIUM", "HIGH"]
    risk_factors: List[str] = []
    recommended_actions: List[str] = []
class TravelAdvisoryReport(BaseModel):
    destination: str
    region: str
    country: str
    forecast_days: int
    current_weather: CurrentWeather
    daily_forecast: List[DailyForecast]
    weather_risk: Literal["LOW", "MEDIUM", "HIGH"]
    risk_factors: List[str]
    recommended_actions: List[str]
    packing_suggestions: List[str]
    travel_readiness_advisory: str
    weather_risk_explanation: str
    resources_used: List[str]
    tools_used: List[str]
    prompts_used: List[str]
class ValidateCityResponse(BaseModel):
    success: bool
    original_city_name: str | None = None
    normalized_city_name: str | None = None
    message: str | None = None
class GetWeatherForecastResponse(BaseModel):
    success: bool
    city_name: str
    raw_weather_data: dict | None = None
    message: str | None = None
class SaveReportResponse(BaseModel):
    success: bool
    saved_path: str | None = None
    message: str | None = None
TOOLS_USED = [
    "validate_city_input_tool",
    "get_weather_forecast_tool",
    "normalize_weather_data_tool",
    "calculate_weather_risk_tool",
    "save_travel_advisory_tool",
]

RESOURCES_USED = [
    "resource://travel/checklist",
    "resource://travel/advisory-rules",
    "resource://weather/normalized-forecast-schema",
]

PROMPTS_USED = [
    "travel_readiness_prompt",
    "weather_risk_summary_prompt",
    "packing_recommendation_prompt",
]
def create_empty_report() -> TravelAdvisoryReport:
    """
    Creates a valid empty report template
    matching the PRD schema.
    """

    return TravelAdvisoryReport(
        destination="",
        region="",
        country="",
        forecast_days=3,
        current_weather=CurrentWeather(
            temperature_c=0,
            humidity=0,
            precipitation_mm=0,
            wind_speed_kmph=0,
            weather_description="",
        ),
        daily_forecast=[],
        weather_risk="LOW",
        risk_factors=[],
        recommended_actions=[],
        packing_suggestions=[],
        travel_readiness_advisory="",
        weather_risk_explanation="",
        resources_used=RESOURCES_USED,
        tools_used=TOOLS_USED,
        prompts_used=PROMPTS_USED,
    )
if __name__ == "__main__":
    report = create_empty_report()
    print(report.model_dump_json(indent=4))