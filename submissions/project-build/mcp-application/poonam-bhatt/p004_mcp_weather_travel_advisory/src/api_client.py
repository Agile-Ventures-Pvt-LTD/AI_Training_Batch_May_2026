import os
import requests
from dotenv import load_dotenv

load_dotenv()

WTTR_PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")

def get_weather_from_wttr(normalized_city_name: str) -> dict:
    urls = [
        f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
        f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1"
    ]
    
    last_error = "Unknown error"
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                try:
                    raw_data = response.json()
                    if not raw_data or not isinstance(raw_data, dict):
                        last_error = f"Invalid JSON type: expected dict, got {type(raw_data)}"
                        continue
                    if "current_condition" not in raw_data or "weather" not in raw_data:
                        last_error = "Missing core sections in weather response"
                        continue
                    return {
                        "success": True,
                        "url_used": url,
                        "raw_weather_data": raw_data
                    }
                except ValueError as json_err:
                    last_error = f"JSON decode failed: {json_err}"
            else:
                last_error = f"HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            last_error = "Timeout (10s)"
        except requests.exceptions.ConnectionError:
            last_error = "Connection error"
        except Exception as error:
            last_error = str(error)
            
    return {
        "success": False,
        "message": f"Unable to fetch weather data. Last error: {last_error}"
    }
