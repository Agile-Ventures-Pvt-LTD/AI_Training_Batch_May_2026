import pytest
import json
from src.tools import (
    validate_city_input_tool,
    calculate_weather_risk_tool
)

def test_validate_city_input_tool_valid_city():
    """Valid city is accepted"""
    res_str = validate_city_input_tool("Jaipur")
    res = json.loads(res_str) # JSON String ko dictionary me convert kiya
    assert res["success"] is True
    assert res["original_city_name"] == "Jaipur"

def test_validate_city_input_tool_city_with_space():
    """New Delhi becomes New+Delhi"""
    res_str = validate_city_input_tool("New Delhi")
    res = json.loads(res_str)
    assert res["success"] is True
    assert res["normalized_city_name"] == "New+Delhi"

def test_validate_city_input_tool_empty_city():
    """Empty city is rejected"""
    res_str = validate_city_input_tool("")
    res = json.loads(res_str)
    assert res["success"] is False
    assert "cannot be empty" in res["message"]

def test_calculate_weather_risk_tool_valid_risk_level():
    """Risk is one of LOW, MEDIUM, HIGH"""
    mock_normalized = {
        "daily_forecast": [
            {
                "max_temp_c": 32.0,
                "total_precipitation_mm": 1.2,
                "max_chance_of_rain": 45,
                "max_wind_kmph": 15.0
            }
        ]
    }
    res_str = calculate_weather_risk_tool(json.dumps(mock_normalized))
    res = json.loads(res_str)
    assert res["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]
