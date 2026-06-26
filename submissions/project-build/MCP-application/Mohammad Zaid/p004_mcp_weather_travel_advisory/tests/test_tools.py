# tests/test_tools.py
import pytest
import asyncio
from src.server import mcp
import json

@pytest.mark.asyncio
async def test_validate_city_input_tool_valid_city():
    result = await mcp.call_tool("validate_city_input_tool", {"city_name": "New York"})
    assert "New+York" in result[0].text

@pytest.mark.asyncio
async def test_validate_city_input_tool_city_with_space():
    result = await mcp.call_tool("validate_city_input_tool", {"city_name": "New Delhi"})
    assert "New+Delhi" in result[0].text

@pytest.mark.asyncio
async def test_validate_city_input_tool_empty_city():
    result = await mcp.call_tool("validate_city_input_tool", {"city_name": ""})
    assert "false" in result[0].text.lower()

@pytest.mark.asyncio
async def test_get_weather_forecast_tool_mock_success():
    result = await mcp.call_tool("get_weather_forecast_tool", {"normalized_city_name": "Jaipur"})
    assert "success" in result[0].text.lower()

@pytest.mark.asyncio
async def test_normalize_weather_data_tool_schema():
    result = await mcp.call_tool("get_weather_forecast_tool", {"normalized_city_name": "Jaipur"})
    raw_data = json.loads(result[0].text)
    if raw_data.get("success"):
        norm_result = await mcp.call_tool("normalize_weather_data_tool", {"raw_weather_data": raw_data["raw_weather_data"]})
        norm_data = json.loads(norm_result[0].text)
        assert "current_weather" in norm_data

@pytest.mark.asyncio
async def test_calculate_weather_risk_tool_valid_risk_level():
    norm_data = {
        "daily_forecast": [
            {"max_temp_c": 36, "total_precipitation_mm": 0, "max_chance_of_rain": 0, "max_wind_kmph": 10}
        ]
    }
    result = await mcp.call_tool("calculate_weather_risk_tool", {"normalized_weather_data": norm_data})
    risk_data = json.loads(result[0].text)
    assert risk_data["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]

