from pydantic import BaseModel, Field
from typing import List, Literal

class CurrentWeather(BaseModel):
    temperature_c: float
    humidity: int
    precipitation_mm: float
    wind_speed_kmph: float
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

class NormalizedWeatherData(BaseModel):
    success: bool
    destination: str
    region: str
    country: str
    forecast_days: int
    current_weather: CurrentWeather
    daily_forecast: List[DailyForecast]

class TravelAdvisoryReport(BaseModel):
    destination: str
    region: str
    country: str
    forecast_days: int = 3
    current_weather: CurrentWeather
    daily_forecast: List[DailyForecast]
    weather_risk: Literal["LOW", "MEDIUM", "HIGH"]
    risk_factors: List[str]
    recommended_actions: List[str]
    packing_suggestions: List[str]
    travel_readiness_advisory: str
    weather_risk_explanation: str
    resources_used: List[str] = [
        "resource://travel/checklist",
        "resource://travel/advisory-rules",
        "resource://weather/normalized-forecast-schema"
    ]
    tools_used: List[str] = [
        "validate_city_input_tool",
        "get_weather_forecast_tool",
        "normalize_weather_data_tool",
        "calculate_weather_risk_tool",
        "save_travel_advisory_tool"
    ]
    prompts_used: List[str] = [
        "travel_readiness_prompt",
        "weather_risk_summary_prompt",
        "packing_recommendation_prompt"
    ]
