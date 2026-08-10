# src/api_client.py
import os
import requests

WTTR_PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")

def get_weather_from_wttr(normalized_city_name: str) -> dict:
    urls = [
        f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
        f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1"
    ]
    last_error = ""
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return {
                    "success": True,
                    "url_used": url,
                    "raw_weather_data": response.json()
                }
        except Exception as error:
            last_error = str(error)
    return {
        "success": False,
        "message": f"Unable to fetch weather data. Last error: {last_error}"
    }