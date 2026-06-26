import os
import requests
from dotenv import load_dotenv

load_dotenv()

WTTR_PRIMARY_URL=os.getenv("WTTR_PRIMARY_URL")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL")

def get_weather(normalized_city_name):
    urls=[
        f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
        f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1"
    
    ]
    for url in urls: 
        response=requests.get(url, timeout=10)  #using 10 second timeout here instead of the tool
        if response.status_code == 200:
            return {
                    "success": True,
                    "url_used": url,
                    "raw_weather_data": response.json()
                }
        else:
                last_error = f"error: {response.status_code}"
    return {
        "success": False,
        "city_name": normalized_city_name,
        "message": f"Unable to fetch weather data. Last error: {last_error}"
    }