from typing import List
from pydantic import BaseModel

class Currentweather(BaseModel):
    temperature_c:float
    humidity:int
    precipitation:float
    wind_speed: float
    weather_description: str

class Dailyforecast(BaseModel):
    date:str
    max_temp: float
    min_temp: float
    avg_temp: float
    total_precipitation: float
    max_wind: float
    max_chain_of_rain: int
    weather_description: str

class Normalizeweather(BaseModel):
    success: bool = True
    destination: str
    region: str
    country: str
    forecast_days: int
    current_weather: Currentweather
    daily_forecast: List[Dailyforecast]

class TravelAdvisoryReport(BaseModel):
    destination: str
    region: str
    country: str
    forecast_days: int
    current_weather: Currentweather
    daily_forecast: List[Dailyforecast]
    weather_risk: str
    risk_factors: List[str] 
    recommended_actions: List[str]
    packing_suggestions: List[str] 
    travel_readiness_advisory: str
    weather_risk_explanation: str
    resources_used: List[str] 
    tools_used: List[str] 
    prompts_used: List[str] 
