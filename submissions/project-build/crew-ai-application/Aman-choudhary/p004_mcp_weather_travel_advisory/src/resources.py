from typing import Dict, Any
TRAVEL_CHECKLIST = """
Travel Readiness Checklist
- Confirm destination and travel date.
- Check weather forecast before departure.
- Carry water during high-temperature conditions.
- Carry umbrella or rain protection if rain risk exists.
- Avoid unnecessary outdoor exposure during extreme heat.
- Avoid exposed outdoor areas during high wind conditions.
- Keep phone charged.
- Carry essential documents.
"""
ADVISORY_RULES = """
Weather Advisory Rules
LOW:
- No major heat, rain, or wind indicators.
- Normal travel precautions are enough.
MEDIUM:
- Moderate heat, rain, or wind indicators exist.
- Travel is possible, but the traveler should plan with basic precautions.
HIGH:
- High heat, high rain probability, heavy precipitation,
  or high wind conditions exist.
- The traveler should reconsider non-essential outdoor travel
  or plan with extra caution.
"""
NORMALIZED_FORECAST_SCHEMA: Dict[str, Any] = {
    "destination": "string",
    "region": "string",
    "country": "string",
    "forecast_days": "number",
    "current_weather": {
        "temperature_c": "number",
        "humidity": "number",
        "precipitation_mm": "number",
        "wind_speed_kmph": "number",
        "weather_description": "string",
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
            "weather_description": "string",
        }
    ],
}
RESOURCES = {
    "resource://travel/checklist": TRAVEL_CHECKLIST,
    "resource://travel/advisory-rules": ADVISORY_RULES,
    "resource://weather/normalized-forecast-schema": NORMALIZED_FORECAST_SCHEMA,
}


def get_resource(resource_uri: str):
    """
    Returns resource content by URI.

    Args:
        resource_uri: MCP resource URI

    Returns:
        Resource content
    """
    if resource_uri not in RESOURCES:
        raise ValueError(f"Unknown resource requested: {resource_uri}")
    return RESOURCES[resource_uri]
def list_resources() -> list[str]:
    """
    Returns all available resources.
    Used by tests.
    Returns:
        List of resource URIs
    """
    return list(RESOURCES.keys())