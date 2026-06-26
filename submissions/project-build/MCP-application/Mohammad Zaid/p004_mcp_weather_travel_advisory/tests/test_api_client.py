# tests/test_api_client.py
from src.api_client import get_weather_from_wttr

def test_api_client():
    result = get_weather_from_wttr("London")
    assert result["success"] == True
    assert "raw_weather_data" in result