def get_checklist():
    return """
Travel Readiness Checklist:
- Confirm destination and travel date.
- Check weather forecast before departure.
- Carry water during high-temperature conditions.
- Carry umbrella or rain protection if rain risk exists.
- Avoid unnecessary outdoor exposure during extreme heat.
- Avoid exposed outdoor areas during high wind conditions.
- Keep phone charged.
- Carry essential documents.
"""


def get_advisory_rules():
    return """
Weather Advisory Rules:

LOW:
- No major heat, rain, or wind indicators.
- Normal travel precautions are enough.

MEDIUM:
- Moderate weather conditions exist.
- Travel is possible with precautions.

HIGH:
- Extreme weather conditions present.
- Avoid non-essential outdoor travel.
"""


def get_schema():
    return {
        "destination": "string",
        "region": "string",
        "country": "string",
        "forecast_days": "number",
        "current_weather": {},
        "daily_forecast": []
    }
# def get_checklist():
#     return "Travel checklist data"


# def get_advisory_rules():
#     return "Rules data"


# def get_schema():
#     return "Schema info"