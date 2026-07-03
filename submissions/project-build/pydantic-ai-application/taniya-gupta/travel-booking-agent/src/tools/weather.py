import httpx
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

class WeatherReport(BaseModel):
    city: str
    temperature_c: float
    condition: str

async def get_weather(ctx: RunContext[None], city: str) -> dict:
    """Fetch current weather data for a given city."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
        )
        geo_data = resp.json()
        
        if not geo_data.get("results"):
            return {"error": f"City {city} not found"}
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        
        weather_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,weather_code"
            }
        )
        data = weather_resp.json()
        current = data["current"]
        
        conditions = {0: "Clear", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast"}
        return {
            "temperature_c": current["temperature_2m"],
            "condition": conditions.get(current["weather_code"], "Unknown")
        }
