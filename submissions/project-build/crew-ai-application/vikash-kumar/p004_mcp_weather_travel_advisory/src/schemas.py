from pydantic import BaseModel
from typing import List

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

class FinalReport(BaseModel):
    destination: str
    region: str
    country: str
    forecast_days: int = 3
    current_weather: CurrentWeather
    daily_forecast: List[DailyForecast]
    weather_risk: str
    risk_factors: List[str]
    recommended_actions: List[str]
    packing_suggestions: List[str]
    travel_readiness_advisory: str
    weather_risk_explanation: str
    resources_used: List[str]
    tools_used: List[str]
    # weather_risk_explanation
    prompts_used: List[str]
