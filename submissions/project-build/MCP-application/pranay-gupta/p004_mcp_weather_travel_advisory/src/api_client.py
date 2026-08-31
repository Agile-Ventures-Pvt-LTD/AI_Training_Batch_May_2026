import os
import requests
from dotenv import load_dotenv

load_dotenv()

WTTR_PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")
API_TIMEOUT = 10

def get_weather_from_wttr(normalized_city_name: str) -> dict:
    urls = [
        f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
        f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1",
    ]
    
    last_error = "Unknown error"
    
    for url in urls:
        try:
            response = requests.get(url, timeout=API_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "url_used": url,
                    "raw_weather_data": data
                }
            else:
                last_error = f"HTTP {response.status_code} from {url}"
        except ValueError as json_err:
            last_error = f"Invalid JSON response: {json_err}"
        except requests.exceptions.Timeout:
            last_error = f"Request timed out after {API_TIMEOUT}s for {url}"
        except requests.exceptions.ConnectionError as conn_err:
            last_error = f"Connection error: {conn_err}"
        except Exception as err:
            last_error = f"Unexpected error: {err}"
            
    return {
        "success": False,
        "message": f"Unable to fetch weather data. Last error: {last_error}"
    }