import pytest
from unittest.mock import patch, MagicMock
from tools import (validate_city_input_tool,get_weather_forecast_tool,normalize_weather_data_tool,calculate_weather_risk_tool,save_travel_advisory_tool)

def test_validate_city_input_tool_valid_city():
    result = validate_city_input_tool("Jaipur")
    assert result["success"] is True
    assert result["normalized_city_name"] == "Jaipur"
    assert result["original_city_name"] == "Jaipur"

def test_validate_city_input_tool_city_with_space():
    result = validate_city_input_tool("New Delhi")
    assert result["success"] is True
    assert result["normalized_city_name"] == "New+Delhi"
    assert result["original_city_name"] == "New Delhi"

def test_validate_city_input_tool_empty_city():
    result = validate_city_input_tool("")
    assert result["success"] is False
    assert "empty" in result["message"].lower()

def test_validate_city_input_tool_whitespace_only():
    result = validate_city_input_tool("   ")
    assert result["success"] is False

def test_validate_city_input_tool_short_city():
    result = validate_city_input_tool("A")
    assert result["success"] is False

def test_get_weather_forecast_tool_mock_success(sample_raw_wttr_response):
    with patch("tools.get_weather_from_wttr") as mock_api:
        mock_api.return_value = {
            "success": True,
            "url_used": "https://wttr.in/Jaipur?format=j1",
            "raw_weather_data": sample_raw_wttr_response
        }
        result = get_weather_forecast_tool("Jaipur")
    assert result["success"] is True
    assert result["city_name"] == "Jaipur"
    assert "raw_weather_data" in result
    assert "current_condition" in result["raw_weather_data"]

def test_get_weather_forecast_tool_mock_failure():
    with patch("tools.get_weather_from_wttr") as mock_api:
        mock_api.return_value = {
            "success": False,
            "message": "Unable to fetch weather data. Last error: timeout"
        }
        result = get_weather_forecast_tool("InvalidCity")
    assert result["success"] is False
    assert result["city_name"] == "InvalidCity"
    assert "message" in result

def test_normalize_weather_data_tool_schema(sample_raw_wttr_response):
    result = normalize_weather_data_tool(sample_raw_wttr_response)
    assert result["success"] is True
    assert result["destination"] == "Jaipur"
    assert result["region"] == "Rajasthan"
    assert result["country"] == "India"
    assert result["forecast_days"] == 3
    cw = result["current_weather"]
    assert isinstance(cw["temperature_c"], float)
    assert isinstance(cw["humidity"], int)
    assert isinstance(cw["precipitation_mm"], float)
    assert isinstance(cw["wind_speed_kmph"], float)
    assert cw["temperature_c"] == 31.0
    assert cw["humidity"] == 48
    assert cw["weather_description"] == "Sunny"
    df = result["daily_forecast"]
    assert len(df) == 3
    assert df[0]["date"] == "2026-06-26"
    assert df[0]["max_temp_c"] == 37.0
    assert df[0]["min_temp_c"] == 27.0
    assert df[0]["avg_temp_c"] == 32.0
    assert df[0]["total_precipitation_mm"] == 0.4
    assert df[0]["max_wind_kmph"] == 28.0
    assert df[0]["max_chance_of_rain"] == 60

def test_normalize_weather_data_tool_empty_input():
    result = normalize_weather_data_tool({})
    assert result["success"] is False

def test_calculate_weather_risk_tool_valid_risk_level(sample_normalized_data):
    result = calculate_weather_risk_tool(sample_normalized_data)
    assert result["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]
    assert isinstance(result["risk_factors"], list)
    assert isinstance(result["recommended_actions"], list)

def test_calculate_weather_risk_tool_high_heat():
    data = {
        "daily_forecast": [
            {
                "date": "2026-06-26",
                "max_temp_c": 42.0,
                "min_temp_c": 30.0,
                "avg_temp_c": 36.0,
                "total_precipitation_mm": 0.0,
                "max_wind_kmph": 10.0,
                "max_chance_of_rain": 5,
                "weather_description": "Sunny"
            }
        ]
    }
    result = calculate_weather_risk_tool(data)
    assert result["weather_risk"] == "HIGH"

def test_calculate_weather_risk_tool_moderate_heat():
    data = {
        "daily_forecast": [
            {
                "date": "2026-06-26",
                "max_temp_c": 36.0,
                "min_temp_c": 26.0,
                "avg_temp_c": 31.0,
                "total_precipitation_mm": 0.0,
                "max_wind_kmph": 10.0,
                "max_chance_of_rain": 5,
                "weather_description": "Sunny"
            }
        ]
    }
    result = calculate_weather_risk_tool(data)
    assert result["weather_risk"] == "MEDIUM"

def test_calculate_weather_risk_tool_low():
    data = {
        "daily_forecast": [
            {
                "date": "2026-06-26",
                "max_temp_c": 28.0,
                "min_temp_c": 20.0,
                "avg_temp_c": 24.0,
                "total_precipitation_mm": 0.0,
                "max_wind_kmph": 10.0,
                "max_chance_of_rain": 5,
                "weather_description": "Clear"
            }
        ]
    }
    result = calculate_weather_risk_tool(data)
    assert result["weather_risk"] == "LOW"

def test_save_travel_advisory_tool(tmp_path):
    report = {"destination": "TestCity", "weather_risk": "LOW"}
    with patch("tools.OUTPUT_PATH", str(tmp_path)):
        result = save_travel_advisory_tool(report)
    assert result["success"] is True
    assert "travel_advisory_report.json" in result["saved_path"]
    import json, os
    with open(result["saved_path"], "r") as f:
        saved = json.load(f)
    assert saved["destination"] == "TestCity"

@pytest.mark.integration
def test_real_wttr_api_for_jaipur():
    result = get_weather_forecast_tool("Jaipur")
    assert result["success"] is True
    assert "raw_weather_data" in result