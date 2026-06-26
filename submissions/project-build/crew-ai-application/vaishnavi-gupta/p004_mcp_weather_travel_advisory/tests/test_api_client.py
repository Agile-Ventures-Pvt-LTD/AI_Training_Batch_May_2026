import os
import requests

from dotenv import load_dotenv

load_dotenv()

def test_weather_api():

    WTTR_PRIMRY_URL = os.getenv("WTTR_PRIMARY_URL")
    WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL")

    url = (
        f"http://api.weatherapi.com/v1/current.json"
        f"?key={city}&q=Delhi"
    )

    response = requests.get(url)

    assert response.status_code == 200

    print("✅ Weather API Working")


if __name__ == "__main__":
    test_weather_api()






import os
import requests
from dotenv import load_dotenv
load_dotenv()

def test_weather_api():
    response = requests.get(
        "http://127.0.0.1:8000/weather?location=Delhi"
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    assert response.status_code == 200

test_weather_api()