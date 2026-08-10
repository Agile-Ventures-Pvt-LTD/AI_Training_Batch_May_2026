import logging
import os

import requests
from dotenv import load_dotenv
try:
    from src.schemas import APIResponse
except ModuleNotFoundError:
    from schemas import APIResponse

load_dotenv()

logger = logging.getLogger(__name__)

PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")
TIMEOUT = 10


def get_weather_from_wttr(normalized_city_name: str) -> APIResponse:
    urls = (
        f"{PRIMARY_URL}/{normalized_city_name}?format=j1",
        f"{FALLBACK_URL}/{normalized_city_name}?format=j1",
    )

    last_error = "Unable to fetch weather data."

    for url in urls:
        try:
            response = requests.get(url, timeout=TIMEOUT)

            if response.status_code != 200:
                last_error = f"HTTP {response.status_code}"
                continue

            try:
                data = response.json()
            except ValueError:
                last_error = "Invalid JSON response."
                continue

            return APIResponse(
                success=True,
                city_name=normalized_city_name.replace("+", " "),
                url_used=url,
                raw_weather_data=data,
            )

        except requests.Timeout:
            logger.warning("Weather API timeout: %s", url)
            last_error = "Request timed out."

        except requests.ConnectionError:
            logger.warning("Weather API connection failed: %s", url)
            last_error = "Connection failed."

        except requests.RequestException:
            logger.exception("Weather API request failed")
            last_error = "Request failed."

    return APIResponse(
        success=False,
        city_name=normalized_city_name.replace("+", " "),
        message=last_error,
    )