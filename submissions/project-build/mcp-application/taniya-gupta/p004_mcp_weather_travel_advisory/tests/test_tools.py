import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.tools import (
    validate_city_input_tool,
    get_weather_forecast_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool,
)

def test_validate_city_input_tool():
   
    res1 = validate_city_input_tool("New York")
    assert res1["success"] is True
    assert res1["normalized_city_name"] == "New+York"

    res2 = validate_city_input_tool("")
    assert res2["success"] is False

    res3 = validate_city_input_tool("A")
    assert res3["success"] is False

def test_get_weather_forecast_tool(mocker):
    mocker.patch(
        f"{get_weather_forecast_tool.__module__}.get_weather",
        return_value={"raw_weather_data": "mock_data"}
    )
    res = get_weather_forecast_tool("Jaipur")
    assert res["success"] is True
    assert res["raw_weather_data"] == "mock_data"

def test_normalize_weather_data_tool():
    raw_data = {
        "nearest_area": [{
            "areaName": [{"value": "Jaipur"}],
            "region": [{"value": "Rajasthan"}],
            "country": [{"value": "India"}]
        }],
        "current_condition": [{
            "temp_C": "35",
            "humidity": "40",
            "precipMM": "0.0",
            "windspeedKmph": "15",
            "weatherDesc": [{"value": "Sunny"}]
        }],
        "weather": [{
            "date": "2026-06-26",
            "maxtempC": "40",
            "mintempC": "30",
            "avgtempC": "35",
            "hourly": []
        }]
    }
    
    res = normalize_weather_data_tool(raw_data)
    assert res["success"] is True
    assert res["destination"] == "Jaipur"
    assert res["region"] == "Rajasthan"
    assert res["country"] == "India"
    assert res["current_weather"]["temperature_c"] == 35.0
    assert len(res["daily_forecast"]) == 1

def test_calculate_weather_risk_tool_low():
    normalized = {
        "daily_forecast": [{
            "max_temp_c": 30.0,
            "total_precipitation_mm": 0.0,
            "max_chance_of_rain": 10,
            "max_wind_kmph": 15.0
        }]
    }
    res = calculate_weather_risk_tool(normalized)
    assert res["weather_risk"] == "LOW"

def test_calculate_weather_risk_tool_high():
    normalized = {
        "daily_forecast": [{
            "max_temp_c": 42.0,  
            "total_precipitation_mm": 0.0,
            "max_chance_of_rain": 10,
            "max_wind_kmph": 15.0
        }]
    }
    res = calculate_weather_risk_tool(normalized)
    assert res["weather_risk"] == "HIGH"

