import requests
from geopy.geocoders import Nominatim
from typing import Dict, Any

GEOCODER = Nominatim(user_agent="travel_booking_agent")
WEATHER_ENDPOINT = "https://api.open-meteo.com/v1/forecast"


def _to_latlon(city: str) -> tuple[float, float]:
    location = GEOCODER.geocode(city, exactly_one=True, timeout=10)
    if not location:
        raise ValueError(f"Could not resolve location: {city}")
    return location.latitude, location.longitude


def get_forecast(city: str, date: str) -> Dict[str, Any]:

    lat, lon = _to_latlon(city)

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "start_date": date,
        "end_date": date,
    }
    resp = requests.get(WEATHER_ENDPOINT, params=params, timeout=8)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("daily"):
        raise RuntimeError("Weather API returned unexpected payload")

    code = data["daily"]["weathercode"][0]
    weather_desc = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "depositing rime fog",
        51: "light drizzle",
        61: "light rain",
        63: "moderate rain",
        80: "rain showers",
        95: "thunderstorm",
    }.get(code, "variable conditions")

    return {
        "city": city,
        "date": date,
        "description": weather_desc,
        "temp_max": data["daily"]["temperature_2m_max"][0],
        "temp_min": data["daily"]["temperature_2m_min"][0],
    }