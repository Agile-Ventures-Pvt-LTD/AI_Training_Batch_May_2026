from src.tools import validate_city_input_tool, calculate_weather_risk_tool

def test_validate_city_input_tool_valid_city():
    city_test = validate_city_input_tool("Jaipur")
    assert city_test["success"] is True
    assert city_test["normalized_city_name"] == "Jaipur"

def test_validate_city_input_tool_city_with_space():
    input_test = validate_city_input_tool("New Delhi")
    assert input_test["success"] is True
    assert input_test["normalized_city_name"] == "New+Delhi"

def test_validate_city_input_tool_empty_city():
    empty_test = validate_city_input_tool(" ")
    assert empty_test["success"] is False

def test_calculate_weather_risk_tool_valid_risk_level():
    sample_data = {
        "daily_forecast": [{
            "max_temp_c": 36.0,
            "total_precipitation_mm": 1.5,
            "max_chance_of_rain": 55,
            "max_wind_kmph": 23.0
        }]
    }
    res = calculate_weather_risk_tool(sample_data)
    assert res["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]
