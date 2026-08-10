

from __future__ import annotations
from datetime import date
import os
from typing import Any, Optional, Dict, List
from dataclasses import dataclass
from dotenv import load_dotenv
import openmeteo_requests
import json
import pandas as pd
import requests_cache
from retry_requests import retry
import requests

load_dotenv()
os.environ['WEATHERAPI_KEY'] = os.getenv('WEATHERAPI_KEY')

class WeatherAPIError(RuntimeError):
    """Raised when WeatherAPI returns an error or an unexpected response."""



async def get_weather(
        
        latitude: float,
        longitude: float,
        hourly: Optional[str],
        forecast_days : int = 7,
        start_date : str = date.today()
    ):
  
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        
    }

    if hourly:
        params["hourly"] = hourly

    if forecast_days:
        params["forecast_days"]=forecast_days

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()

    data = resp.json()

    if isinstance(data, dict) and "error" in data:
        err = data["error"] or {}
        code = err.get("code")
        msg = err.get("message", "Unknown WeatherAPI error")
        raise WeatherAPIError(f"WeatherAPI error (code={code}): {msg}")
    
    return data


# result=get_weather(latitude= 52.52,
# 	longitude=13.41,
# 	hourly="temperature_2m")

# print (result)