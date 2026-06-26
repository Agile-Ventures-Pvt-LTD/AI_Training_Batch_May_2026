import json

from mcp_use.server import MCPRouter

router = MCPRouter()

@router.resource("resource://travel/checklist")
async def get_checklist() -> str:
    """
    Provides a static travel-readiness checklist.
    """
    
    content = """Travel Readiness Checklist:
    - Confirm destination and travel date.
    - Check weather forecast before departure.
    - Carry water during high-temperature conditions.
    - Carry umbrella or rain protection if rain risk exists.
    - Avoid unnecessary outdoor exposure during extreme heat.
    - Avoid exposed outdoor areas during high wind conditions.
    - Keep phone charged.- Carry essential documents."""
    
    return content

@router.resource("resource://travel/advisory-rules")
async def get_advisory() -> str:
    """Provides static rules for interpreting weather risk."""
    content = """Weather Advisory Rules:
    LOW:- No major heat, rain, or wind indicators.- Normal travel precautions are enough.
    MEDIUM:- Moderate heat, rain, or wind indicators exist.- Travel is possible, but the traveler should plan with basic precautions.
    HIGH:- High heat, high rain probability, heavy precipitation, or high wind 
    condition exists.- The traveler should reconsider non-essential outdoor travel or plan with extra caution"""
    return content


@router.resource("resource://weather/normalized-forecast-schema")
async def get_schema() -> str:
    """Describes the normalized forecast schema expected by this project"""
    return json.dumps({
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
        }]})