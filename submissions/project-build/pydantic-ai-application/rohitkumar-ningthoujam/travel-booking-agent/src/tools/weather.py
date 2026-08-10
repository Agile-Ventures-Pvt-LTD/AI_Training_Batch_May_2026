import openmeteo_requests
from pydantic_ai import Agent
import asyncio

@agent.tool
async def get_weather_forcast():
	openmeteo = openmeteo_requests.AsyncClient()

	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 52.52,
		"longitude": 13.41,
		"hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
		"current": ["temperature_2m", "relative_humidity_2m"],
	}
	response = await openmeteo.weather_api(url, params=params)

	
	print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation: {response.Elevation()} m asl")
	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

	current = response.Current()
	current_temperature_2m = current.Variables(0).Value()
	current_relative_humidity_2m = current.Variables(1).Value()

	print(f"Current time: {current.Time()}")
	print(f"Current temperature_2m: {current_temperature_2m}")
	print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
