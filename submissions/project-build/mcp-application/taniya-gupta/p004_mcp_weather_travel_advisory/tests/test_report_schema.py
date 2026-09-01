import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.schemas import Currentweather, Dailyforecast

def test_current_weather_validation():
    data = {
        "temperature_c": 25.5,
        "humidity": 60,
        "precipitation": 0.0,
        "wind_speed": 12.5,
        "weather_description": "Clear"
    }
    obj = Currentweather(**data)
    assert obj.temperature_c == 25.5
    assert obj.humidity == 60

def test_daily_forecast_validation():
    data = {
        "date": "2026-06-26",
        "max_temp": 30.0,
        "min_temp": 20.0,
        "avg_temp": 25.0,
        "total_precipitation": 1.5,
        "max_wind": 15.0,
        "max_chain_of_rain": 40,
        "weather_description": "Scattered rain"
    }
    obj = Dailyforecast(**data)
    assert obj.date == "2026-06-26"
    assert obj.max_temp == 30.0