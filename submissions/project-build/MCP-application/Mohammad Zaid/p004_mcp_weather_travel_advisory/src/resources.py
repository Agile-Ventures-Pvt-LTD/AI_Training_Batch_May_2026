# src/resources.py
import json
from fastmcp import FastMCP
from schemas import get_normalized_schema


def register_resources(mcp: FastMCP):
    @mcp.resource("resource://weather/normalized-forecast-schema")
    async def normalized_forecast_schema() -> str:
        schema = get_normalized_schema()
        return f"```json\n{json.dumps(schema, indent=2)}\n```"

    @mcp.resource("resource://travel/checklist")
    async def travel_checklist() -> str:
        return """Travel Readiness Checklist:
                - Confirm destination and travel date.
                - Check weather forecast before departure.
                - Carry water during high-temperature conditions.
                - Carry umbrella or rain protection if rain risk exists.
                - Avoid unnecessary outdoor exposure during extreme heat.
                - Avoid exposed outdoor areas during high wind conditions.
                - Keep phone charged.
                - Carry essential documents."""

    @mcp.resource("resource://travel/advisory-rules")
    async def advisory_rules() -> str:
        return """Weather Advisory Rules:
                LOW:
                - No major heat, rain, or wind indicators.
                - Normal travel precautions are enough.
                MEDIUM:
                - Moderate heat, rain, or wind indicators exist.
                - Travel is possible, but the traveler should plan with basic precautions.
                HIGH:
                - High heat, high rain probability, heavy precipitation, or high wind condition exists.
                - The traveler should reconsider non-essential outdoor travel or plan with extra caution."""