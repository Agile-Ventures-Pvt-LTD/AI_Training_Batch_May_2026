import os
import requests
from typing import Any
from api_config import WTTR_PRIMARY_URL, WTTR_FALLBACK_URL


def get_weather_from_wttr(normalized_city_name: str) -> Any:
    """Calls wttr.in JSON API and returns raw weather data in json format."""
    
    urls = [
    f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
    f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response
        except Exception as error:
            last_error = str(error)
            return f"Unable to fetch weather data. Last error: {last_error}"