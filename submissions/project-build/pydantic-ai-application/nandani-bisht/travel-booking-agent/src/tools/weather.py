import httpx
from typing import Dict, Any, Optional

WMO_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def geocode_city(city: str) -> Optional[tuple[float, float, str]]:
    """
    Geocodes a city name to latitude, longitude, and full formatted location name
    using the Open-Meteo Geocoding API.
    
    Args:
        city: Name of the city (e.g. 'Paris, France' or 'Tokyo')
        
    Returns:
        A tuple of (latitude, longitude, formatted_name) if successful, else None.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    query = city.split(",")[0].strip()
    params = {"name": query, "count": 1, "format": "json"}
    
    try:
        response = httpx.get(url, params=params, timeout=10.0)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results")
            if results:
                lat = results[0]["latitude"]
                lon = results[0]["longitude"]
                name = results[0].get("name", query)
                country = results[0].get("country", "")
                full_name = f"{name}, {country}" if country else name
                return lat, lon, full_name
    except Exception:
        pass
    return None

def fetch_weather(city: str, travel_dates: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves weather conditions for a destination.
    Attempts to fetch a forecast for specific travel dates. If dates are not
    supported (out of range), falls back to the current 7-day forecast.
    
    Args:
        city: The destination city
        travel_dates: Optional travel dates in format "YYYY-MM-DD to YYYY-MM-DD"
        
    Returns:
        A dictionary with location, forecast_type, and weather details.
    """
    coords = geocode_city(city)
    if not coords:
        return {"error": f"Could not geocode city '{city}' to coordinates."}
        
    lat, lon, full_name = coords
    url = "https://api.open-meteo.com/v1/forecast"
    
    start_date = None
    end_date = None
    if travel_dates:
        parts = travel_dates.split(" to ")
        if len(parts) == 2:
            start_date = parts[0].strip()
            end_date = parts[1].strip()
            

    if start_date and end_date:
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "timezone": "auto"
        }
        try:
            r = httpx.get(url, params=params, timeout=10.0)
            if r.status_code == 200:
                data = r.json()
                daily = data.get("daily", {})
                
    
                summaries = []
                if daily and "time" in daily:
                    for i, t in enumerate(daily["time"]):
                        code = daily.get("weather_code", [0]*len(daily["time"]))[i]
                        desc = WMO_CODE_MAP.get(code, "Unknown weather")
                        t_max = daily.get("temperature_2m_max", [None]*len(daily["time"]))[i]
                        t_min = daily.get("temperature_2m_min", [None]*len(daily["time"]))[i]
                        summaries.append({
                            "date": t,
                            "condition": desc,
                            "temp_max": t_max,
                            "temp_min": t_min
                        })
                
                return {
                    "location": full_name,
                    "latitude": lat,
                    "longitude": lon,
                    "dates": travel_dates,
                    "forecast_type": "specific_dates",
                    "daily_summaries": summaries,
                    "daily_raw": daily
                }
        except Exception:
            pass
            
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "current_weather": "true",
        "timezone": "auto"
    }
    try:
        r = httpx.get(url, params=params, timeout=10.0)
        if r.status_code == 200:
            data = r.json()
            daily = data.get("daily", {})
            current = data.get("current_weather", {})
            

            curr_code = current.get("weathercode", 0)
            curr_desc = WMO_CODE_MAP.get(curr_code, "Unknown weather")
            
            summaries = []
            if daily and "time" in daily:
                for i, t in enumerate(daily["time"]):
                    code = daily.get("weather_code", [0]*len(daily["time"]))[i]
                    desc = WMO_CODE_MAP.get(code, "Unknown weather")
                    t_max = daily.get("temperature_2m_max", [None]*len(daily["time"]))[i]
                    t_min = daily.get("temperature_2m_min", [None]*len(daily["time"]))[i]
                    summaries.append({
                        "date": t,
                        "condition": desc,
                        "temp_max": t_max,
                        "temp_min": t_min
                    })
                    
            return {
                "location": full_name,
                "latitude": lat,
                "longitude": lon,
                "dates": travel_dates,
                "forecast_type": "current_and_7day_fallback",
                "note": "Requested dates out of forecast range. Showing current conditions and upcoming week forecast.",
                "current_weather": {
                    "temp": current.get("temperature"),
                    "condition": curr_desc,
                    "wind_speed": current.get("windspeed"),
                    "time": current.get("time")
                },
                "daily_summaries": summaries,
                "daily_raw": daily
            }
    except Exception as e:
        return {"error": f"Failed to fetch weather forecast: {str(e)}"}
        
    return {"error": "Failed to fetch weather forecast due to API communication issue."}
