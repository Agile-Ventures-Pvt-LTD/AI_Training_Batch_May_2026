import pytest
from src.tools import (
    validate_city_input_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool,
    save_travel_advisory_tool
)


class TestValidateCityInputTool:
    def test_valid_city(self):
        result = validate_city_input_tool("Jaipur")
        assert result["success"] is True
        assert result["original_city_name"] == "Jaipur"
        assert result["normalized_city_name"] == "Jaipur"

    def test_city_with_space(self):
        result = validate_city_input_tool("New Delhi")
        assert result["success"] is True
        assert result["original_city_name"] == "New Delhi"
        assert result["normalized_city_name"] == "New+Delhi"

    def test_empty_city(self):
        result = validate_city_input_tool("")
        assert result["success"] is False
        assert "empty" in result["message"].lower()

    def test_short_city(self):
        result = validate_city_input_tool("a")
        assert result["success"] is False
        assert "2 characters" in result["message"].lower()

    def test_city_strips_whitespace(self):
        result = validate_city_input_tool("  Mumbai  ")
        assert result["success"] is True
        assert result["original_city_name"] == "Mumbai"


class TestNormalizeWeatherDataTool:
    def test_normalize_success(self):
        raw_data = {
            "nearest_area": [{"areaName": [{"value": "Jaipur"}], "region": [{"value": "Rajasthan"}], "country": [{"value": "India"}]}],
            "current_condition": [{"temp_C": "31", "humidity": "48", "precipMM": "0.0", "windspeedKmph": "12", "weatherDesc": [{"value": "Sunny"}]}],
            "weather": [
                {
                    "date": "2026-06-26",
                    "maxtempC": "37", "mintempC": "27", "avgtempC": "32",
                    "hourly": [{"windspeedKmph": "28", "chanceofrain": "60", "precipMM": "1.2", "weatherDesc": [{"value": "Partly cloudy"}]}]
                }
            ]
        }
        result = normalize_weather_data_tool(raw_data)
        assert result["success"] is True
        assert result["destination"] == "Jaipur"
        assert result["current_weather"]["temperature_c"] == 31.0
        assert result["daily_forecast"][0]["max_chance_of_rain"] == 60


class TestCalculateWeatherRiskTool:
    def test_risk_low(self):
        data = {"daily_forecast": [{"max_temp_c": 25, "total_precipitation_mm": 0, "max_chance_of_rain": 10, "max_wind_kmph": 10}]}
        result = calculate_weather_risk_tool(data)
        assert result["weather_risk"] == "LOW"
        assert result["risk_keys"] == []

    def test_risk_medium_temp(self):
        data = {"daily_forecast": [{"max_temp_c": 37, "total_precipitation_mm": 0, "max_chance_of_rain": 10, "max_wind_kmph": 10}]}
        result = calculate_weather_risk_tool(data)
        assert result["weather_risk"] == "MEDIUM"
        assert "heat_moderate" in result["risk_keys"]

    def test_risk_high_temp(self):
        data = {"daily_forecast": [{"max_temp_c": 42, "total_precipitation_mm": 0, "max_chance_of_rain": 10, "max_wind_kmph": 10}]}
        result = calculate_weather_risk_tool(data)
        assert result["weather_risk"] == "HIGH"
        assert "heat_high" in result["risk_keys"]

    def test_risk_valid_level(self):
        data = {"daily_forecast": [{"max_temp_c": 25, "total_precipitation_mm": 0, "max_chance_of_rain": 10, "max_wind_kmph": 10}]}
        result = calculate_weather_risk_tool(data)
        assert result["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]


class TestSaveTravelAdvisoryTool:
    def test_save_report(self, tmp_path, monkeypatch):
        monkeypatch.setenv("OUTPUT_PATH", str(tmp_path))
        result = save_travel_advisory_tool({"test": "data"})
        assert result["success"] is True
        assert "travel_advisory_report.json" in result["saved_path"]