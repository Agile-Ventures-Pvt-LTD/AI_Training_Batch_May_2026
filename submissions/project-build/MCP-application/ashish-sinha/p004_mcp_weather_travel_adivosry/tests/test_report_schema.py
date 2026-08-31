import pytest
from pydantic import ValidationError
from schemas import TravelAdvisoryReport, CurrentWeather, DailyForecast

@pytest.fixture
def valid_weather_payload():
    return {
        "temperature_c": 30.5,
        "humidity": 60,
        "precipitation_mm": 0.0,
        "wind_speed_kmph": 12.0,
        "weather_description": "Clear skies"
    }

def test_current_weather_schema_valid(valid_weather_payload):
    weather = CurrentWeather(**valid_weather_payload)
    assert weather.temperature_c == 30.5
    assert weather.humidity == 60

def test_current_weather_schema_invalid():
    with pytest.raises(ValidationError):
        CurrentWeather(humidity=60, precipitation_mm=0.0, wind_speed_kmph=12.0, weather_description="Clear")
