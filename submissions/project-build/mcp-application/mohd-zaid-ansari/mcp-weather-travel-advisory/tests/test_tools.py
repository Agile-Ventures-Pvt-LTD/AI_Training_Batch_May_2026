import pytest
from src.tools import validate_city_input_tool, calculate_weather_risk_tool

def test_validate_city_input_tool_valid_city():
    """Verify that a clean single-word city input is accepted."""
    res = validate_city_input_tool("Jaipur")
    assert res["success"] is True
    assert res["original_city_name"] == "Jaipur"

def test_validate_city_input_tool_city_with_space():
    """Verify that spaces are replaced with plus symbols for safe URL configurations."""
    res = validate_city_input_tool("New Delhi")
    assert res["success"] is True
    assert res["normalized_city_name"] == "New+Delhi"

def test_validate_city_input_tool_empty_city():
    """Verify that blank or empty inputs are cleanly caught and rejected."""
    res = validate_city_input_tool("   ")
    assert res["success"] is False
    assert "empty" in res["message"].lower()

@pytest.mark.asyncio
async def test_calculate_weather_risk_tool_valid_risk_level():
    """Verify that our risk logic flags an overall level of LOW, MEDIUM, or HIGH."""
    mock_data = {
        "daily_forecast": [{"max_temp_c": 37.0, "total_precipitation_mm": 1.2, "max_chance_of_rain": 60, "max_wind_kmph": 28.0}]
    }
    res = await calculate_weather_risk_tool(mock_data)
    assert res["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]
