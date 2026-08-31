import openmeteo_requests

def get_weather_details(start_date: str,end_date:str,latitude:float,longitude:float):
    openmeteo = openmeteo_requests.Client()

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": latitude,
	"longitude": longitude,
	"start_date":start_date,
    "end_date":end_date
    }
    responses = openmeteo.weather_api(url, params=params)
    return responses.Current()
