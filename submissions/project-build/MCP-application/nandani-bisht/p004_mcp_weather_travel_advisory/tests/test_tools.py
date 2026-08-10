import pytest
from src.tools import validate_city_input, normalize_weather_data, calculate_weather_risk

def test_validate_city_input_tool_valid_city():
    result = validate_city_input("Jaipur")
    assert result["success"] is True
    assert result["original_city_name"] == "Jaipur"
    assert result["normalized_city_name"] == "Jaipur"

def test_validate_city_input_tool_city_with_space():
    result = validate_city_input("New Delhi")
    assert result["success"] is True
    assert result["original_city_name"] == "New Delhi"
    assert result["normalized_city_name"] == "New+Delhi"

def test_validate_city_input_tool_empty_city():
    
    res1 = validate_city_input("")
    assert res1["success"] is False
    assert res1["message"] == "City name cannot be empty."

    
    res2 = validate_city_input("   ")
    assert res2["success"] is False
    assert res2["message"] == "City name cannot be empty."

    
    res3 = validate_city_input("a")
    assert res3["success"] is False
    assert "must be at least 2 characters" in res3["message"]

def test_normalize_weather_data_tool_schema():
    raw_data = {
        "current_condition": [
            {
                "temp_C": "31",
                "humidity": "48",
                "precipMM": "0.0",
                "windspeedKmph": "12",
                "weatherDesc": [{"value": "Sunny"}]
            }
        ],
        "nearest_area": [
            {
                "areaName": [{"value": "Jaipur"}],
                "region": [{"value": "Rajasthan"}],
                "country": [{"value": "India"}]
            }
        ],
        "weather": [
            {
                "date": "2026-06-26",
                "maxtempC": "37",
                "mintempC": "27",
                "avgtempC": "32",
                "hourly": [
                    {
                        "windspeedKmph": "28",
                        "chanceofrain": "60",
                        "precipMM": "1.2",
                        "weatherDesc": [{"value": "Partly cloudy"}]
                    }
                ]
            }
        ]
    }
    
    result = normalize_weather_data(raw_data)
    assert result["success"] is True
    assert result["destination"] == "Jaipur"
    assert result["region"] == "Rajasthan"
    assert result["country"] == "India"
    assert result["forecast_days"] == 1
    assert result["current_weather"]["temperature_c"] == 31.0
    assert result["current_weather"]["humidity"] == 48
    assert result["current_weather"]["precipitation_mm"] == 0.0
    assert result["current_weather"]["wind_speed_kmph"] == 12.0
    assert result["current_weather"]["weather_description"] == "Sunny"
    
    day_forecast = result["daily_forecast"][0]
    assert day_forecast["date"] == "2026-06-26"
    assert day_forecast["max_temp_c"] == 37.0
    assert day_forecast["min_temp_c"] == 27.0
    assert day_forecast["avg_temp_c"] == 32.0
    assert day_forecast["total_precipitation_mm"] == 1.2
    assert day_forecast["max_wind_kmph"] == 28.0
    assert day_forecast["max_chance_of_rain"] == 60
    assert day_forecast["weather_description"] == "Partly cloudy"

def test_normalize_weather_data_tool_missing_fields():

    result = normalize_weather_data({})
    assert result["success"] is False
    assert result["message"] == "Unable to normalize weather data because required fields are missing."

def test_calculate_weather_risk_tool_valid_risk_level():

    low_risk_data = {
        "daily_forecast": [
            {
                "max_temp_c": 30.0,
                "total_precipitation_mm": 0.0,
                "max_chance_of_rain": 10,
                "max_wind_kmph": 15.0
            }
        ]
    }
    res1 = calculate_weather_risk(low_risk_data)
    assert res1["weather_risk"] == "LOW"
    assert "No major weather risks identified." in res1["risk_factors"]
    assert "Normal travel precautions are sufficient." in res1["recommended_actions"]


    med_risk_data = {
        "daily_forecast": [
            {
                "max_temp_c": 36.0,
                "total_precipitation_mm": 0.0,
                "max_chance_of_rain": 10,
                "max_wind_kmph": 15.0
            }
        ]
    }
    res2 = calculate_weather_risk(med_risk_data)
    assert res2["weather_risk"] == "MEDIUM"
    assert "Maximum temperature is expected to be above 35°C." in res2["risk_factors"]
    high_risk_data = {
        "daily_forecast": [
            {
                "max_temp_c": 42.0,
                "total_precipitation_mm": 0.0,
                "max_chance_of_rain": 10,
                "max_wind_kmph": 15.0
            }
        ]
    }
    res3 = calculate_weather_risk(high_risk_data)
    assert res3["weather_risk"] == "HIGH"
    assert "Maximum temperature is expected to be 40°C or above." in res3["risk_factors"]
