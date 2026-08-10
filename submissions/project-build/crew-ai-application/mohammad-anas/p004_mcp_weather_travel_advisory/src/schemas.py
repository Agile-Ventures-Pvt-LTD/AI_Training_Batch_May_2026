from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WeatherRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class CurrentWeather(BaseModel):
    model_config = ConfigDict(extra="forbid")

    temperature_c: float
    humidity: int
    precipitation_mm: float
    wind_speed_kmph: float
    weather_description: str


class DailyForecast(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: str
    max_temp_c: float
    min_temp_c: float
    avg_temp_c: float
    total_precipitation_mm: float
    max_wind_kmph: float
    max_chance_of_rain: int
    weather_description: str


class NormalizedWeather(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool = True
    destination: str
    region: str
    country: str
    forecast_days: int
    current_weather: CurrentWeather
    daily_forecast: list[DailyForecast]


class ValidationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool
    original_city_name: str | None = None
    normalized_city_name: str | None = None
    message: str | None = None


class APIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool
    city_name: str
    url_used: str | None = None
    raw_weather_data: dict[str, Any] | None = None
    message: str | None = None


class RiskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    weather_risk: WeatherRisk
    risk_factors: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)


class TravelReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    destination: str
    region: str
    country: str
    forecast_days: int

    current_weather: CurrentWeather
    daily_forecast: list[DailyForecast]

    weather_risk: WeatherRisk
    risk_factors: list[str]
    recommended_actions: list[str]

    packing_suggestions: list[str]
    travel_readiness_advisory: str
    weather_risk_explanation: str

    resources_used: list[str]
    tools_used: list[str]
    prompts_used: list[str]