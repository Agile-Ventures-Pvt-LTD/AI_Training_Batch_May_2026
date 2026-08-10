import os
import requests
from typing import Any, Dict

def get_weather_from_wttr(city_name: str) -> Dict[str, Any]:
    """Calls wttr.in JSON API and returns raw weather data with fallback support."""
    normalized_city = city_name.strip().replace(" ", "+")
    primary_url = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
    fallback_url = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")
    
    urls = [
        f"{primary_url}/{normalized_city}?format=j1",
        f"{fallback_url}/{normalized_city}?format=j1"
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return {
                    "success": True,
                    "url_used": url,
                    "raw_weather_data": response.json()
                }
        except Exception:
            continue
    return {
        "success": False,
        "message": "Unable to fetch weather data from any endpoint."
    }
