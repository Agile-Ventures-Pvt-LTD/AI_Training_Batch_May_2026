"""AGENT FILE for Rag Chatbot"""

import asyncio
import warnings
from pydantic_ai import Agent
import openmeteo_requests
import requests_cache
from retry_requests import retry
try:
    from utils.prompts import SYSTEM_PROMPT
    from utils.db_conn import get_connection
    from utils.geolocation import get_coordinates
except ImportError:
    from .utils.prompts import SYSTEM_PROMPT
    from .utils.db_conn import get_connection
    from .utils.geolocation import get_coordinates

warnings.filterwarnings("ignore")

agent = Agent(
    'groq:openai/gpt-oss-20b',
    system_prompt=SYSTEM_PROMPT,
    instructions="Run Sql queries.",
)


@agent.tool_plain(name="get_user_details", description="Accepts either email or booking id and returns all values related to the user.")
def get_user_details(
    *, 
    email: str = None, 
    booking_id: str = None
) -> tuple:
    """Takes either email id or booking id as parameter.
    
    Args:
        email (str): email of the user
        booking_id (str): booking id of the user
    
    Returns:
        (tuple): all values associated with the user.
    
    """
    if not email and not booking_id:
        raise ValueError("No identifiers provided. Provide email or booking id.")
    conn = get_connection()
    cursor = conn.cursor()
    
    if email:
        cursor.execute("""Select * from bookings WHERE user_email = ?""", (email,))
    else:
        cursor.execute("""Select * from bookings WHERE booking_id = ?""", (booking_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        return {
            "status": "error",
            "message": f"User with {email or booking_id} not found."
        }
    conn.close()
    
    return row


@agent.tool_plain(name="get_weather_details", description="Accepts location in string, start date and end date and returns weather details corresponding to them.")
def get_weather_details(location: str, startDate: str, endDate: str):
    """
    Fetches daily maximum temperature for a given location and date range.

    Args:
        location (str): Name of the location (e.g., 'Berlin, Germany')
        startDate (str): Start date in 'YYYY-MM-DD' format
        endDate (str): End date in 'YYYY-MM-DD' format

    Returns:
        dict: Weather details including location, coordinates, and daily temperatures.
    """
    coordinates = get_coordinates(location)
    if coordinates["messege"]:
        raise Exception(f"Could not find the location {location}")
    
    latitude = coordinates["latitude"]
    longitude = coordinates["longitude"]
    
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": startDate,
        "end_date": endDate,
        "hourly": "temperature_2m"
    }
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Extract daily max temperatures
    daily_max_temps = response.DailyVariables().temperature_2m_max()
    dates = response.DailyVariables().time()

    # Format the output
    weather_data = {
        "location": location,
        "coordinates": f"{response.Latitude()}°N {response.Longitude()}°E",
        "start_date": startDate,
        "end_date": endDate,
        "daily_max_temperatures": [
            {"date": date, "max_temp_c": temp}
            for date, temp in zip(dates, daily_max_temps)
        ]
    }

    return weather_data


async def main():
    res = await agent.run(query)
    return res.output

if __name__ =="__main__":
    while True:
        query = input("INPUT  (write 'exit' to leave)> ")
        
        if query == 'exit':
            break
        
        result = asyncio.run(main())
        
        print(result)