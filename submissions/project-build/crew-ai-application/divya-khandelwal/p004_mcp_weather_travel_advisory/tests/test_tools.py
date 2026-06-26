import pytest
import src.tools as t

def test_validate_city_input_tool_valid_city():
    res = t.validate_city_input_tool("Jaipur")
    assert res["success"] is True
    assert res["normalized_city_name"] == "Jaipur"

def test_validate_city_input_tool_city_with_space():
    res = t.validate_city_input_tool("New Delhi")
    assert res["success"] is True
    assert res["normalized_city_name"] == "New+Delhi"

def test_validate_city_input_tool_empty_city():
    res = t.validate_city_input_tool("   ")
    assert res["success"] is False
    assert "empty" in res["message"]

def test_normalize_weather_data_tool_schema():
    raw_mock = {
        "nearest_area": [{"areaName": [{"value": "Pune"}], "region": [{"value": "MH"}], "country": [{"value": "India"}]}],
        "current_condition": [{"temp_C": "30", "humidity": "50", "precipMM": "0.0", "windspeedKmph": "10", "weatherDesc": [{"value": "Sunny"}]}],
        "weather": [{"date": "2026-06-26", "maxtempC": "35", "mintempC": "25", "avgtempC": "30", "hourly": [{"windspeedKmph": "12", "chanceofrain": "10", "precipMM": "0.1", "weatherDesc": [{"value": "Clear"}]}]}]
    }
    res = t.normalize_weather_data_tool(raw_mock)
    assert res["success"] is True
    assert res["destination"] == "Pune"
    assert res["current_weather"]["temperature_c"] == 30.0

def test_calculate_weather_risk_tool_valid_risk_level():
    mock_norm = {
        "destination": "Mumbai", "region": "MH", "country": "India", "forecast_days": 1,
        "current_weather": {"temperature_c": 31.0, "humidity": 48, "precipitation_mm": 0.0, "wind_speed_kmph": 12.0, "weather_description": "Sunny"},
        "daily_forecast": [{"date": "2026-06-26", "max_temp_c": 37.0, "min_temp_c": 27.0, "avg_temp_c": 32.0, "total_precipitation_mm": 1.2, "max_wind_kmph": 28.0, "max_chance_of_rain": 60, "weather_description": "Partly cloudy"}]
    }
    res = t.calculate_weather_risk_tool(mock_norm)
    assert res["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]
