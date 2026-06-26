import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools import (
    validate_city_input_tool,
    get_weather_forecast_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool
)
from tests.mock_data import MOCK_RAW_WEATHER

def test_validate_city_input_tool_valid_city():
    res = validate_city_input_tool("Jaipur")
    assert res["success"] is True
    assert res["original_city_name"] == "Jaipur"
    assert res["normalized_city_name"] == "Jaipur"

def test_validate_city_input_tool_city_with_space():
    res = validate_city_input_tool("New Delhi")
    assert res["success"] is True
    assert res["original_city_name"] == "New Delhi"
    assert res["normalized_city_name"] == "New+Delhi"

def test_validate_city_input_tool_empty_city():
    res1 = validate_city_input_tool("")
    assert res1["success"] is False
    assert "empty" in res1["message"].lower()

    res2 = validate_city_input_tool("   ")
    assert res2["success"] is False
    assert "empty" in res2["message"].lower()

    res3 = validate_city_input_tool("A")
    assert res3["success"] is False
    assert "at least" in res3["message"].lower()

def test_get_weather_forecast_tool_mock_success(mocker):
    # Mock api_client get_weather_from_wttr function
    mock_get = mocker.patch("src.tools.get_weather_from_wttr")
    mock_get.return_value = {
        "success": True,
        "url_used": "https://wttr.in/Jaipur?format=j1",
        "raw_weather_data": MOCK_RAW_WEATHER
    }
    
    res = get_weather_forecast_tool("Jaipur")
    assert res["success"] is True
    assert res["city_name"] == "Jaipur"
    assert res["raw_weather_data"] == MOCK_RAW_WEATHER

def test_normalize_weather_data_tool_schema():
    res = normalize_weather_data_tool(MOCK_RAW_WEATHER)
    assert res["success"] is True
    assert res["destination"] == "Jaipur"
    assert res["region"] == "Rajasthan"
    assert res["country"] == "India"
    assert res["forecast_days"] == 1
    
    current = res["current_weather"]
    assert current["temperature_c"] == 31.0
    assert current["humidity"] == 48
    assert current["precipitation_mm"] == 0.0
    assert current["wind_speed_kmph"] == 12.0
    assert current["weather_description"] == "Sunny"
    
    day1 = res["daily_forecast"][0]
    assert day1["date"] == "2026-06-26"
    assert day1["max_temp_c"] == 37.0
    assert day1["min_temp_c"] == 27.0
    assert day1["avg_temp_c"] == 32.0
    assert day1["total_precipitation_mm"] == 1.2
    assert day1["max_wind_kmph"] == 28.0
    assert day1["max_chance_of_rain"] == 60.0
    assert day1["weather_description"] == "Clear"

def test_calculate_weather_risk_tool_valid_risk_level():
  
    low_data = {
        "daily_forecast": [
            {
                "max_temp_c": 30.0,
                "total_precipitation_mm": 2.0,
                "max_chance_of_rain": 20.0,
                "max_wind_kmph": 15.0
            }
        ]
    }
    res_low = calculate_weather_risk_tool(low_data)
    assert res_low["weather_risk"] == "LOW"
    assert len(res_low["risk_factors"]) == 1
    assert "No major weather risks" in res_low["risk_factors"][0]
    
    
    med_data = {
        "daily_forecast": [
            {
                "max_temp_c": 36.0,
                "total_precipitation_mm": 2.0,
                "max_chance_of_rain": 20.0,
                "max_wind_kmph": 15.0
            }
        ]
    }
    res_med = calculate_weather_risk_tool(med_data)
    assert res_med["weather_risk"] == "MEDIUM"
    assert any("above 35°C" in factor for factor in res_med["risk_factors"])
    
   
    high_data = {
        "daily_forecast": [
            {
                "max_temp_c": 30.0,
                "total_precipitation_mm": 25.0,
                "max_chance_of_rain": 85.0,
                "max_wind_kmph": 45.0
            }
        ]
    }
    res_high = calculate_weather_risk_tool(high_data)
    assert res_high["weather_risk"] == "HIGH"
    assert any("Heavy precipitation" in factor for factor in res_high["risk_factors"])
    assert any("Wind speeds are expected to be 40 km/h or above" in factor for factor in res_high["risk_factors"])
