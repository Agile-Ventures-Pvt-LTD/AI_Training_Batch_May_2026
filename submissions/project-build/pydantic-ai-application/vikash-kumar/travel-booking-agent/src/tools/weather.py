import httpx

async def weather_forecast(city: str) -> str:
    location_url = f"https://open-meteo.com{city}&count=1&format=json"
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            location = await client.get(location_url)
            results = location.json().get("results")
            if not results:
                return f"Cordinate are not found: {city}."
            
            latitude = results[0]["latitude"]
            longitude = results[0]["longitude"]
            
            weather_url = f"https://open-meteo.com{latitude}&longitude={longitude}&current_weather=true"
            weather = await client.get(weather_url)
            current_weather= weather.json().get("current_weather", {})
            return f"THe current temperature in {city} is {current_weather.get('temperature')}°C."
        except Exception:
            return "Info. is not available for weather"
