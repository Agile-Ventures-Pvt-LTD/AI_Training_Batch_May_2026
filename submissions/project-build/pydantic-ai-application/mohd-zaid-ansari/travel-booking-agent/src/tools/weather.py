from src.agent import agent
from pydantic_ai import Agent, RunContext
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
def get_city_coordinates(city_name: str) -> tuple[float, float] | None:
    """
    Converts a city name into latitude and longitude coordinates.
    """
    geolocator = Nominatim(user_agent="city_coordinator_app")
    try:
        location = geolocator.geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
        return None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None
    
# if __name__ == "__main__":
#     city = "Chicago"
#     coordinates = get_city_coordinates(city)
#     if coordinates:
#         lat, lon = coordinates
#         print(f"{city} Coordinates -> Latitude: {lat}, Longitude: {lon}")
#     else:
#         print(f"Could not find coordinates for: {city}")


#==============================================================================================================================

@agent.tool
def weather_information(city:RunContext[str]):
    """You have to get the weather of the city using the coordinates of the city or the name of the city."""
    
    coordinates=get_city_coordinates(city_name=city)

    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "coordinates":coordinates,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "wind_speed_180m", "temperature_80m"],
    }
    responses=openmeteo.weather_api(url, params)

    for response in responses:
        
        response=responses[0]

        # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        # print(f"Elevation: {response.Elevation()} m asl")
        # print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        hourly=response.Hourly()
        hourly_temperature_2m=hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m=hourly.Variables(1).ValuesAsNumpy()
        hourly_precipitation_probability=hourly.Variables(2).ValuesAsNumpy()
        hourly_precipitation=hourly.Variables(3).ValuesAsNumpy()
        hourly_rain=hourly.Variables(4).ValuesAsNumpy()
        hourly_showers=hourly.Variables(5).ValuesAsNumpy()
        hourly_snowfall=hourly.Variables(6).ValuesAsNumpy()
        hourly_snow_depth=hourly.Variables(7).ValuesAsNumpy()
        hourly_wind_speed_180m=hourly.Variables(8).ValuesAsNumpy()
        hourly_temperature_80m=hourly.Variables(9).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )
        }

        hourly_data["temperature_2m"]=hourly_temperature_2m
        hourly_data["relative_humidity_2m"]=hourly_relative_humidity_2m
        hourly_data["precipitation_probability"]=hourly_precipitation_probability
        hourly_data["precipitation"]=hourly_precipitation
        hourly_data["rain"]=hourly_rain
        hourly_data["showers"]=hourly_showers
        hourly_data["snowfall"]=hourly_snowfall
        hourly_data["snow_depth"]=hourly_snow_depth
        hourly_data["wind_speed_180m"]=hourly_wind_speed_180m
        hourly_data["temperature_80m"]=hourly_temperature_80m

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        # print("\nHourly data\n", hourly_dataframe)
        return hourly_dataframe
