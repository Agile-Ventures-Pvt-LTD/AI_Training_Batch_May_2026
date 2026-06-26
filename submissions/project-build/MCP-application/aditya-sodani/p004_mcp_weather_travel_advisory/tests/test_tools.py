from src.tools import (
    validate_city_input_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool
)


def test_validate_city_input_valid_city():
    res = validate_city_input_tool({"city_name": "Jaipur"})
    assert res["success"] is True


def test_validate_city_input_city_with_space():
    res = validate_city_input_tool({"city_name": "New Delhi"})
    assert res["normalized_city_name"] == "New+Delhi"


def test_validate_city_input_empty_city():
    res = validate_city_input_tool({"city_name": ""})
    assert res["success"] is False


def test_calculate_weather_risk_tool_valid_risk_level():
    sample = {
        "normalized_weather_data": {
            "daily_forecast": [
                {"max_temp_c": 36, "total_precipitation_mm": 0, "max_chance_of_rain": 20, "max_wind_kmph": 10}
            ]
        }
    }

    res = calculate_weather_risk_tool(sample)
    assert res["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]


def test_normalize_weather_data_tool_schema():
    raw = {
        "nearest_area": [{"areaName": [{"value": "Jaipur"}],
                          "region": [{"value": "Rajasthan"}],
                          "country": [{"value": "India"}]}],
        "current_condition": [{
            "temp_C": "30",
            "humidity": "50",
            "precipMM": "0",
            "windspeedKmph": "10",
            "weatherDesc": [{"value": "Sunny"}]
        }],
        "weather": [{
            "date": "2026-06-26",
            "maxtempC": "35",
            "mintempC": "25",
            "avgtempC": "30",
            "hourly": [{
                "windspeedKmph": "10",
                "precipMM": "0",
                "chanceofrain": "10",
                "weatherDesc": [{"value": "Sunny"}]
            }]
        }]
    }

    res = normalize_weather_data_tool({"raw_weather_data": raw})
    assert res["success"] is True
    assert "current_weather" in res