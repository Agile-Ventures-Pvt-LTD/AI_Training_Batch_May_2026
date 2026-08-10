import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_weather(location: str,timeout_s: float = 10.0,)->dict:
    api_key =os.getenv("WEATHERAPI_KEY")
    if not api_key:
        return{
            "fetch":False,
            "error":"api key not found"
        }
    base_url = "http://api.weatherapi.com/v1"
    url = f"{base_url}/forecast.json" 

    params = {
        "key": api_key,               
        "q": location,                  
    }

    resp = requests.get(url, params=params, timeout=timeout_s)
    resp.raise_for_status()

    data = resp.json()

    if isinstance(data, dict) and "error" in data:
        err = data["error"] or {}
        code = err.get("code")
        msg = err.get("message", "Unknown WeatherAPI error")
        return{
            "fetch":False,
            "error":"data not found"
        }

    if not isinstance(data, dict) or "current" not in data:
         return{
            "fetch":False,
            "error":"data not found"
        }
       
    return {
        "fetch":True,
        "data":data

    }


