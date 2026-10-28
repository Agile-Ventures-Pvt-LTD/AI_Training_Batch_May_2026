import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import requests

def get_latitude_longitude(country_name: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={country_name}&count=1&language=en&format=json"

    response = requests.get(url, timeout=10)
    weather = response.json()

    latitude = weather["results"][0]["latitude"]
    longitude =  weather["results"][0]["longitude"]

    return query_weather(latitude=latitude, longitude=longitude)
    

def query_weather(latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)


    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
    }
    responses = openmeteo.weather_api(url, params = params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return hourly_dataframe



if __name__ == "__main__":
    a = get_latitude_longitude("India")
    print(a)
