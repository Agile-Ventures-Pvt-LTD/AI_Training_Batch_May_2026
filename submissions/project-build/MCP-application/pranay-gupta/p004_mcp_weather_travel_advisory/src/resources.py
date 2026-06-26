TRAVEL_CHECKLIST = """Travel Readiness Checklist:
- Confirm destination and travel date.
- Check weather forecast before departure.
- Carry water during high-temperature conditions.
- Carry umbrella or rain protection if rain risk exists.
- Avoid unnecessary outdoor exposure during extreme heat.
- Avoid exposed outdoor areas during high wind conditions.
- Keep phone charged.
- Carry essential documents."""

CHECKLIST_URI = "resource://travel/checklist"

def get_travel_checklist() -> str:
    return TRAVEL_CHECKLIST

ADVISORY_RULES = """Weather Advisory Rules:
LOW:
- No major heat, rain, or wind indicators.
- Normal travel precautions are enough.
MEDIUM:
- Moderate heat, rain, or wind indicators exist.
- Travel is possible, but the traveler should plan with basic precautions.
HIGH:
- High heat, high rain probability, heavy precipitation, or high wind condition exists.
- The traveler should reconsider non-essential outdoor travel or plan with extra caution."""

ADVISORY_RULES_URI = "resource://travel/advisory-rules"

def get_advisory_rules() -> str:
    return ADVISORY_RULES

NORMALIZED_FORECAST_SCHEMA = """{
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
}"""

SCHEMA_URI = "resource://weather/normalized-forecast-schema"

def get_normalized_forecast_schema() -> str:
    return NORMALIZED_FORECAST_SCHEMA

ALL_RESOURCES = [CHECKLIST_URI, ADVISORY_RULES_URI, SCHEMA_URI]