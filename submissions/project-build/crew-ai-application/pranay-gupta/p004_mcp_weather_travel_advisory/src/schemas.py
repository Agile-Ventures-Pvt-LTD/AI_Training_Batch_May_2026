from pydantic import BaseModel, Field
from typing import Any, Optional

class CityInput(BaseModel):
    city_name: str = Field(...)

class ForecastInput(BaseModel):
    normalized_city_name: str = Field(...)

class NormalizeInput(BaseModel):
    raw_weather_data: dict = Field(...)

class RiskInput(BaseModel):
    normalized_weather_data: dict = Field(...)

class SaveReportInput(BaseModel):
    report: dict = Field(...)

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
    success: bool = True
    destination: str
    region: str
    country: str
    forecast_days: int
    current_weather: CurrentWeather
    daily_forecast: list[DailyForecast]

class RiskResult(BaseModel):
    weather_risk: str
    risk_factors: list[str]
    recommended_actions: list[str]

class FinalReport(BaseModel):
    destination: str
    region: str
    country: str
    forecast_days: int
    current_weather: CurrentWeather
    daily_forecast: list[DailyForecast]
    weather_risk: str
    risk_factors: list[str]
    recommended_actions: list[str]
    packing_suggestions: list[str]
    travel_readiness_advisory: str
    weather_risk_explanation: str
    resources_used: list[str]
    tools_used: list[str]
    prompts_used: list[str]