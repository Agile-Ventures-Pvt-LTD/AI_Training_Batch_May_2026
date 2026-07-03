# weather.py

import httpx
from typing import Optional
from agent import travel_agent

async def get_city_coordinates(city_name: str) -> Optional[dict]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city_name, "count": 1, "language": "en"}
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get("results"):
                return None
            
            result = data["results"][0]
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "country": result.get("country", "")
            }
    except Exception:
        return None


@travel_agent.tool
async def get_weather_forecast(city_name: str, date: Optional[str] = None) -> dict:
    """
    Get weather forecast for a city using Open-Meteo API.
    
    Args:
        city_name: Name of the city
        date: (optional) in %Y-%m-%d format
    
    Returns:
        Dictionary with weather information
    """
    
    coords = await get_city_coordinates(city_name)
    if not coords:
        return {"Error": f"Could not find city: {city_name}"}
    
    if not date:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": coords["latitude"],
                    "longitude": coords["longitude"],
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode",
                    "timezone": "auto",
                    "start_date": date,
                    "end_date": date
                }
            )
            response.raise_for_status()
            data = response.json()
        
        daily = data.get("daily", {})
        
        return {
            "location": f"{coords['name']}, {coords['country']}",
            "date": date,
            "temperature_max": daily.get("temperature_2m_max", [None])[0],
            "temperature_min": daily.get("temperature_2m_min", [None])[0],
            "precipitation_probability": daily.get("precipitation_probability_max", [0])[0],
        }
    
    except httpx.TimeoutException:
        return {"Error !!": "Weather API request was timed out after 10 sec"}
    except Exception as e:
        return {"Error !!": f"Weather API error: {str(e)}"}
    