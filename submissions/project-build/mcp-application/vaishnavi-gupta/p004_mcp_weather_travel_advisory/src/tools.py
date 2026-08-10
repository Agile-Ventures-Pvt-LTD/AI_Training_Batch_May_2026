import json  
import requests  
from typing import List, Dict, Optional   
from fastmcp import FastMCP  
from pathlib import Path  
import os 
from dotenv import load_dotenv 
load_dotenv()

mcp = FastMCP("Weather Travel Advisory")

@mcp.tool()
async def validate_city_input(city: str):   # Validates the city name entered by the user.
    """
    The tool should:
    1. Check that city_name is not empty.
    2. Strip leading and trailing spaces.
    3. Replace internal spaces with + for API usage.
    4. Reject city names shorter than 2 characters.
    5. Return the cleaned city name.

    Args:
        city: The city for which the weather is to checked.
        
    Returns:
        A string
    """    
@mcp.tool()
async def get_weather_forecast(normalized_city_name: str): # Calls the wttr.in JSON API and returns the raw weather response.
    API_CALL = "https://wttr.in/Jaipur?format=j1", https://wttr.in/New+Delhi?format=j1

    
    """
    The API client should:
    1. Use HTTP GET.
    2. Use timeout = 10 seconds.
    3. Return structured errors for timeout, connection failure, invalid 
    JSON, or non-200 response.
    4. Not crash the application if the API call fails.
    """

@mcp.tool()
async def get_weather_forecast(normalized_city_name: str): # Calls the wttr.in JSON API and returns the raw weather response.
    API_CALL = "https://wttr.in/Jaipur?format=j1", https://wttr.in/New+Delhi?format=j1

    
    """
    The API client should:
    1. Use HTTP GET.
    2. Use timeout = 10 seconds.
    3. Return structured errors for timeout, connection failure, invalid 
    JSON, or non-200 response.
    4. Not crash the application if the API call fails.
    """


@mcp.tool()
async def get_weather_forecast(normalized_city_name: str): # Calls the wttr.in JSON API and returns the raw weather response.
    API_CALL = "https://wttr.in/Jaipur?format=j1", https://wttr.in/New+Delhi?format=j1

    
    """
    The API client should:
    1. Use HTTP GET.
    2. Use timeout = 10 seconds.
    3. Return structured errors for timeout, connection failure, invalid 
    JSON, or non-200 response.
    4. Not crash the application if the API call fails.
    """

@mcp.tool()
async def normalize_weather_data(raw_weather_data: dict): # Converts raw wttr.in JSON into a clean internal weather schema.

    """
    The tool should:
    1. Extract destination from nearest_area[0].areaName[0].value if 
    available.
    2. Extract region from nearest_area[0].region[0].value if available.
    3. Extract country from nearest_area[0].country[0].value if available.
    4. Extract current condition from current_condition[0].
    5. Extract up to 3 days from weather.
    6. Convert numeric strings into int or float.
    7. For each day, calculate max_wind_kmph from hourly[*].windspeedKmph.
    8. For each day, calculate max_chance_of_rain from 
    hourly[*].chanceofrain.
    9. For each day, calculate total_precipitation_mm from 
    hourly[*].precipMM.
    10. Use a simple weather_description from 
    hourly[0].weatherDesc[0].value or current condition where needed.
    Error Output{
    "success": false,
    "message": "Unable to normalize weather data because required fields
    are missing."
    }
    """

@mcp.tool()
async def calculate_weather_risk(normalized_weather_data: dict ):    # Calculates deterministic travel weather risk from normalized weather data.
    """
    Overall Risk Logic
    HIGH:
    Any high-risk condition exists.
    MEDIUM:
    No high-risk condition exists, but at least one moderate-risk 
    condition exists.
    LOW:
    No high-risk or moderate-risk condition exists.
    """

@mcp.tool()
async def save_travel_advisory(report: dict): # Saves the final advisory report as JSON.
    """
    Save the final advisory report as JSON.
     
    """
    required_output_file = "outputs/travel_advisory_report.json"



