import aiohttp
from typing import Dict, Any, Optional

GEO_REGISTRY = {
    "london": {"lat": 51.5074, "lon": -0.1278},
    "paris": {"lat": 48.8566, "lon": 2.3522},
    "tokyo": {"lat": 35.6762, "lon": 139.6503},
    "new york": {"lat": 40.7128, "lon": -74.0060},
    "dubai": {"lat": 25.2048, "lon": 55.2708},
    "new delhi": {'lat':28.62137,"lon":77.2148}
}

async def fetch_weather_forecast(destination_city: str) -> Optional[Dict[str, Any]]:
    normalized_city = destination_city.split(",")[0].strip().lower()
    coordinates = GEO_REGISTRY.get(normalized_city)
    
    if not coordinates:
        coordinates = GEO_REGISTRY["london"]
    url = "https://open-meteo.com"
    parameters = {
        "latitude": coordinates["lat"],
        "longitude": coordinates["lon"],
        "current_weather": "true",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=parameters, timeout=5) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception:
            return None