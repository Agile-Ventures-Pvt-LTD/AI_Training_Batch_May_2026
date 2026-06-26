import os
import requests
from dotenv import load_dotenv

load_dotenv()

WTTR_PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")

def get_weather_from_wttr(normalized_city_name: str) -> dict:
    urls = [
        f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
        f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1"
    ]
    
    last_error = "Unknown error"
    for url in urls:
        try:
            headers = {"User-Agent": "curl/7.68.0"}
            response = requests.get(url, timeout=10, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "current_condition" in data:
                    return {
                        "success": True,
                        "url_used": url,
                        "raw_weather_data": data
                    }
                last_error = "Invalid JSON structure: missing current_condition"
            else:
                last_error = f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            last_error = "Request timed out"
        except requests.exceptions.ConnectionError:
            last_error = "Connection failed"
        except ValueError:
            last_error = "Invalid JSON response"
        except Exception as e:
            last_error = str(e)
            
    return {
        "success": False,
        "message": f"Unable to fetch weather data. Last error: {last_error}"
    }
    