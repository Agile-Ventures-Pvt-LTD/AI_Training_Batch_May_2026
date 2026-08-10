from geopy.geocoders import Nominatim
from typing import Any

geolocator = Nominatim(user_agent="my_app")

def get_coordinates(loc: str) -> Any:
    try:
        location = geolocator.geocode(loc)
        return {
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    except Exception as e:
        return {"messege": str(e)}