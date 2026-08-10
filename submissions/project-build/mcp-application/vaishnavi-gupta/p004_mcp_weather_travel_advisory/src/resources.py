import json  
import requests  
from typing import List, Dict, Optional  
from fastmcp import FastMCP  
from pathlib import Path  
import os 
from dotenv import load_dotenv 
load_dotenv()

mcp = FastMCP("Weather Travel Advisory")

@mcp.resource("resource://travel/checklist")      # Provides a static travel-readiness checklists.
async def get_static_travel_readiness_checklist() -> str:
    """
    Return a static checklist of travel-readiness.
    """
    
           


@mcp.resource("resource://travel/advisory-rules")  # Provides static rules for interpreting weather risks.
async def get_advisory_rules() -> str:
    """
    Weather Advisory Rules:
    LOW:
    - No major heat, rain, or wind indicators.
    - Normal travel precautions are enough.
    MEDIUM:
    - Moderate heat, rain, or wind indicators exist.
    - Travel is possible, but the traveler should plan with basic 
    precautions.
    HIGH:
    - High heat, high rain probability, heavy precipitation, or high wind 
    condition exists.
    - The traveler should reconsider non-essential outdoor travel or plan 
    with extra caution.
    """


@mcp.resource("resource://weather/normalized-forecast-schema")   # Describes the normalized forecast schema expected by this project.
async def get_normalized_forecast_schema() -> str:
    """
    Required Content
    {
    "destination": "string",
    "region": "string",
    "country": "string",
    "forecast_days": "number",
    "current_weather": {
    "temperature_c": "number",
    "humidity": "number",
    "precipitation_mm": "number",
    "wind_speed_kmph": "number",
    "weather_description": "string

    },

    "daily_forecast": [
    {
    "date": "string",
    "max_temp_c": "number",
    "min_temp_c": "number",
    "avg_temp_c": "number",
    "total_precipitation_mm": "number",
    "max_wind_kmph": "number",
    "max_chance_of_rain": "number",
    "weather_description": "string"
    }
 
    """
