from mcp.server.fastmcp import FastMCP


def register_resources(mcp: FastMCP):
    @mcp.resource("resource://travel/checklist")
    def travel_checklist() -> str:
        return (
            "Travel Readiness Checklist:\n"
            "- Confirm destination and travel date.\n"
            "- Check weather forecast before departure.\n"
            "- Carry water during high-temperature conditions.\n"
            "- Carry umbrella or rain protection if rain risk exists.\n"
            "- Avoid unnecessary outdoor exposure during extreme heat.\n"
            "- Avoid exposed outdoor areas during high wind conditions.\n"
            "- Keep phone charged.\n"
            "- Carry essential documents."
        )

    @mcp.resource("resource://travel/advisory-rules")
    def advisory_rules() -> str:
        return (
            "Weather Advisory Rules:\n\n"
            "LOW:\n"
            "- No major heat, rain, or wind indicators.\n"
            "- Normal travel precautions are enough.\n\n"
            "MEDIUM:\n"
            "- Moderate heat, rain, or wind indicators exist.\n"
            "- Travel is possible, but the traveler should plan with basic precautions.\n\n"
            "HIGH:\n"
            "- High heat, high rain probability, heavy precipitation, or high wind condition exists.\n"
            "- The traveler should reconsider non-essential outdoor travel or plan with extra caution."
        )

    @mcp.resource("resource://weather/normalized-forecast-schema")
    def normalized_forecast_schema() -> str:
        return (
            '{\n'
            '  "destination": "string",\n'
            '  "region": "string",\n'
            '  "country": "string",\n'
            '  "forecast_days": "number",\n'
            '  "current_weather": {\n'
            '    "temperature_c": "number",\n'
            '    "humidity": "number",\n'
            '    "precipitation_mm": "number",\n'
            '    "wind_speed_kmph": "number",\n'
            '    "weather_description": "string"\n'
            '  },\n'
            '  "daily_forecast": [\n'
            '    {\n'
            '      "date": "string",\n'
            '      "max_temp_c": "number",\n'
            '      "min_temp_c": "number",\n'
            '      "avg_temp_c": "number",\n'
            '      "total_precipitation_mm": "number",\n'
            '      "max_wind_kmph": "number",\n'
            '      "max_chance_of_rain": "number",\n'
            '      "weather_description": "string"\n'
            '    }\n'
            '  ]\n'
            '}'
        )