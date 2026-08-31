import pytest
from src.tools import validate_city_input_tool,normalize_weather_data_tool,calculate_weather_risk_tool

def test_validate_city_input_sanitization():
    result = validate_city_input_tool("  New   Delhi  ")
    assert result["success"] is True
    assert result["normalized_city_name"] == "New+Delhi"

def test_validate_city_input_too_short():
    result = validate_city_input_tool("X")
    assert result["success"] is False
    assert "at least 2 characters" in result["message"]

def test_calculate_weather_risk_high_thresholds():
    mock_normalized = {
        "daily_forecast": [
            {
                "max_temp_c": 42.0, 
                "total_precipitation_mm": 0.0,
                "max_wind_kmph": 10.0,
                "max_chance_of_rain": 10
            }
        ]
    }
    result = calculate_weather_risk_tool(mock_normalized)
    assert result["weather_risk"] == "HIGH"
    assert "critically high" in result["risk_factors"][0]

def test_calculate_weather_risk_low_profile():
    mock_normalized = {
        "daily_forecast": [
            {
                "max_temp_c": 24.0,
                "total_precipitation_mm": 0.0,
                "max_wind_kmph": 5.0,
                "max_chance_of_rain": 5
            }
        ]
    }
    result = calculate_weather_risk_tool(mock_normalized)
    assert result["weather_risk"] == "LOW"
    assert "No major heat, rain, or wind threat thresholds breached." in result["risk_factors"]