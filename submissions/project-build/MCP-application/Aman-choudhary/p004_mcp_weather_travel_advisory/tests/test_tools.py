from tools import (validate_city_input_tool,normalize_weather_data_tool,calculate_weather_risk_tool,)
def test_validate_city_input_tool_valid_city():
    result = validate_city_input_tool("Jaipur")
    assert result["success"] is True
    assert result["normalized_city_name"] == "Jaipur"
def test_validate_city_input_tool_city_with_space():
    result = validate_city_input_tool("New Delhi")
    assert result["success"] is True
    assert result["normalized_city_name"] == "New+Delhi"
def test_validate_city_input_tool_empty_city():
    result = validate_city_input_tool("")
    assert result["success"] is False
def test_normalize_weather_data_tool_schema():
    sample = {"current_condition": [{
                "temp_C": "31",
                "humidity": "48",
                "precipMM": "0.0",
                "windspeedKmph": "12",
                "weatherDesc": [{"value": "Sunny"}],
            }],
        "nearest_area": [{
                "areaName": [{"value": "Jaipur"}],
                "region": [{"value": "Rajasthan"}],
                "country": [{"value": "India"}],
            }],
        "weather": [{
                "date": "2026-06-26",
                "maxtempC": "37",
                "mintempC": "27",
                "avgtempC": "32",
                "hourly": [
                    {
                        "chanceofrain": "60",
                        "precipMM": "1.2",
                        "windspeedKmph": "28",
                        "weatherDesc": [
                            {"value": "Partly cloudy"}
                        ],
                    }
                ],}],}

    result = normalize_weather_data_tool(sample)
    assert result["success"] is True
    assert result["destination"] == "Jaipur"
    assert result["country"] == "India"
def test_calculate_weather_risk_tool_valid_risk_level():
    weather = {"daily_forecast": [
            {"max_temp_c": 37,
                "total_precipitation_mm": 4,
                "max_chance_of_rain": 50,
                "max_wind_kmph": 20,}]}
    result = calculate_weather_risk_tool(weather)
    assert result["weather_risk"] in ["LOW","MEDIUM","HIGH",]