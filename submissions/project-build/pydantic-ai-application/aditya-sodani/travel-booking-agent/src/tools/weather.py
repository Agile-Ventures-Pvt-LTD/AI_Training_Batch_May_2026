import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from src.config import *
from src.agent import agent



#Weather Tool


class WeatherQueryInput(BaseModel):
    city: str = Field(..., description="City name for weather lookup")
    start_date: str = Field(..., description="Trip start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Trip end date (YYYY-MM-DD)")

class WeatherForecast(BaseModel):
    date: str
    condition: str
    temperature_c: float

@agent.tool
def get_weather_forecast(ctx: RunContext,data: WeatherQueryInput) -> List[WeatherForecast]:
    """
    Fetches weather forecast for a given city and date range from an external API.
    """
    forecasts = []
    try:
        # Example: Replace with your real weather API endpoint and key
        # API_KEY = "YOUR_API_KEY"
        base_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m"


        # We'll fetch only the start date's forecast for simplicity
        params = {
            # "key": API_KEY,
            "q": data.city,
            "dt": data.start_date
        }
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        weather_data = resp.json()

        # Extract forecast data
        for day in weather_data.get("forecast", {}).get("forecastday", []):
            forecasts.append(WeatherForecast(
                date=day["date"],
                condition=day["day"]["condition"]["text"],
                temperature_c=day["day"]["avgtemp_c"]
            ))
    except requests.RequestException as e:
        raise RuntimeError(f"Weather API error: {e}")

    if not forecasts:
        raise ValueError("No weather data available for the given date.")

    return forecasts

