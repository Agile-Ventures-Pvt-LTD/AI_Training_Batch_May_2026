import json 
import requests
from typing import Any, List, Dict, Optional 
from fastmcp import FastMCP
from pathlib import Path
import os
from dotenv import load_dotenv
from src.server import mcp

@mcp.resource("resources://travel/checklist")
async def travel_checklist() -> str:
    """
    Provide a statical travel-readiness checklist
    """
    return(
        "Travel Readiness Checklist:" 
            "-Confirm destination and travel date."
            "- Check weather forecast before departure."
            "- Carry water during high-temperature conditions."
            "- Carry umbrella or rain protection if rain risk exists."
            "- Avoid unnecessary outdoor exposure during extreme heat."
            "- Avoid exposed outdoor areas during high wind conditions."
            "- Keep phone charged."
            "- Carry essential documents"
    )

#===========================================================================================================================

@mcp.resource("resources://travel/advisory_rules")
async def travel_rule() -> str:
    """
    Provides static rules for interpreting weather risk.
    """
    return(
        "Weather Advisory Rules:"
        "LOW:"
        "- No major heat, rain, or wind indicators."
        "- Normal travel precautions are enough."
        "MEDIUM:"
        "- Moderate heat, rain, or wind indicators exist."
        "- Travel is possible, but the traveler should plan with basic precautions."
        "HIGH:"
        "- High heat, high rain probability, heavy precipitation, or high wind condition exists."
        "- The traveler should reconsider non-essential outdoor travel or plan with extra caution."
    )


#============================================================================================================================

@mcp.resource("resources//weather/normalized_forcast_schema")
async def forecast_schema() -> str:
    """
    Describes the normalized forecast schema expected by this project.
    """
    return(
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
    "weather_description": "string"
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
]
}

    )
