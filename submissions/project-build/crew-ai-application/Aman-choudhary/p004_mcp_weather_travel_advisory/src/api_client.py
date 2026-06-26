from __future__ import annotations
import logging
import os
from typing import Any, Dict
import requests
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)
WTTR_PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL","https://wttr.in")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL","https://wttr.is")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
def get_weather_from_wttr(normalized_city_name: str,) -> Dict[str, Any]:
    """
    Fetch weather data from wttr.in API.
    Args:
        normalized_city_name: Example "Jaipur" or "New+Delhi"
    Returns:
        Structured response dictionary.
    """
    if not normalized_city_name:
        return {"success": False,"message": "City name cannot be empty."}
    urls = [
        f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
        f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1",]
    last_error = "Unknown error"
    for url in urls:
        try:
            logger.info("Fetching weather data from %s",url,)
            response = requests.get(url,timeout=REQUEST_TIMEOUT,headers={"User-Agent":"WeatherTravelAdvisoryMCP/1.0"},)
            if response.status_code != 200:
                last_error = (f"HTTP {response.status_code}")
                continue
            try:
                data = response.json()
            except ValueError:
                last_error = ("Invalid JSON response received.")
                continue
            return {
                "success": True,
                "url_used": url,
                "raw_weather_data": data,
            }
        except requests.exceptions.Timeout:
            last_error = (f"Request timed out after "f"{REQUEST_TIMEOUT} seconds.")
        except requests.exceptions.ConnectionError:
            last_error = ("Connection error while ""connecting to weather service.")
        except requests.exceptions.RequestException as exc:
            last_error = str(exc)
        except Exception as exc:
            last_error = str(exc)
    return {
        "success": False,
        "message":
            f"Unable to fetch weather data. "
            f"Last error: {last_error}",}

def health_check() -> Dict[str, Any]:
    """
    Verify whether wttr service is reachable.
    """
    result = get_weather_from_wttr("Jaipur")
    return {
        "service": "wttr.in","status":"UP"
            if result.get("success")
            else "DOWN",
        "details": result,
    }
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format=("%(asctime)s - ""%(levelname)s - ""%(message)s"),)
    result = get_weather_from_wttr("Jaipur")
    print(result)