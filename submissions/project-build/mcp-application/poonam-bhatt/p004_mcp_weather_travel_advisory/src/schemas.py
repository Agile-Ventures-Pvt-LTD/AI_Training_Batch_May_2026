from typing import List
from pydantic import BaseModel, Field
class CurrentWeather(BaseModel):
    temperature_c: float = Field(..., description="Current temperature in Celsius")
    humidity: int = Field(..., description="Current humidity percentage")
    precipitation_mm: float = Field(..., description="Current precipitation in millimeters")
    wind_speed_kmph: float = Field(..., description="Current wind speed in km/h")
    weather_description: str = Field(..., description="Short description of current weather")
class DailyForecast(BaseModel):
    date: str = Field(..., description="Date of the forecast (YYYY-MM-DD)")
    max_temp_c: float = Field(..., description="Maximum temperature in Celsius")
    min_temp_c: float = Field(..., description="Minimum temperature in Celsius")
    avg_temp_c: float = Field(..., description="Average temperature in Celsius")
    total_precipitation_mm: float = Field(..., description="Total expected precipitation in mm")
    max_wind_kmph: float = Field(..., description="Maximum wind speed in km/h")
    max_chance_of_rain: float = Field(..., description="Maximum chance of rain percentage")
    weather_description: str = Field(..., description="Representative weather description for the day")
class NormalizedWeatherData(BaseModel):
    destination: str = Field(..., description="Destination city name")
    region: str = Field(..., description="Region or state")
    country: str = Field(..., description="Country")
    forecast_days: int = Field(..., description="Number of forecast days")
    current_weather: CurrentWeather = Field(..., description="Current weather conditions")
    daily_forecast: List[DailyForecast] = Field(..., description="Daily weather forecasts")
class RiskAssessment(BaseModel):
    weather_risk: str = Field(..., description="Overall risk level (LOW, MEDIUM, HIGH)")
    risk_factors: List[str] = Field(..., description="Identified risk factors")
    recommended_actions: List[str] = Field(..., description="Recommended safety actions")
class TravelAdvisoryReport(BaseModel):
    destination: str
    region: str
    country: str
    forecast_days: int
    current_weather: CurrentWeather
    daily_forecast: List[DailyForecast]
    weather_risk: str
    risk_factors: List[str]
    recommended_actions: List[str]
    packing_suggestions: List[str]
    travel_readiness_advisory: str
    weather_risk_explanation: str
    resources_used: List[str] = Field(default_factory=lambda: [
        "resource://travel/checklist",
        "resource://travel/advisory-rules",
        "resource://weather/normalized-forecast-schema"
    ])
    tools_used: List[str] = Field(default_factory=lambda: [
        "validate_city_input_tool",
        "get_weather_forecast_tool",
        "normalize_weather_data_tool",
        "calculate_weather_risk_tool",
        "save_travel_advisory_tool"
    ])
    prompts_used: List[str] = Field(default_factory=lambda: [
        "travel_readiness_prompt",
        "weather_risk_summary_prompt",
        "packing_recommendation_prompt"
    ])
