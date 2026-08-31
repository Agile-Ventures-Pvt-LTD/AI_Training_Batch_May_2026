import pytest

@pytest.fixture
def sample_raw_wttr_response():
    return {
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
        "request": [{"type": "City", "query": "Jaipur"}],
        "weather": [
            {
                "date": "2026-06-26",
                "maxtempC": "37",
                "mintempC": "27",
                "avgtempC": "32",
                "totalSnow_cm": "0",
                "hourly": [
                    {
                        "chanceofrain": "60",
                        "precipMM": "0.4",
                        "windspeedKmph": "28",
                        "weatherDesc": [{"value": "Partly cloudy"}]
                    },
                    {
                        "chanceofrain": "20",
                        "precipMM": "0.0",
                        "windspeedKmph": "15",
                        "weatherDesc": [{"value": "Sunny"}]
                    }
                ]
            },
            {
                "date": "2026-06-27",
                "maxtempC": "38",
                "mintempC": "28",
                "avgtempC": "33",
                "totalSnow_cm": "0",
                "hourly": [
                    {
                        "chanceofrain": "10",
                        "precipMM": "0.0",
                        "windspeedKmph": "20",
                        "weatherDesc": [{"value": "Sunny"}]
                    }
                ]
            },
            {
                "date": "2026-06-28",
                "maxtempC": "36",
                "mintempC": "26",
                "avgtempC": "31",
                "totalSnow_cm": "0",
                "hourly": [
                    {
                        "chanceofrain": "5",
                        "precipMM": "0.0",
                        "windspeedKmph": "18",
                        "weatherDesc": [{"value": "Clear"}]
                    }
                ]
            }
        ]
    }

@pytest.fixture
def sample_normalized_data():
    return {
        "success": True,
        "destination": "Jaipur",
        "region": "Rajasthan",
        "country": "India",
        "forecast_days": 3,
        "current_weather": {
            "temperature_c": 31.0,
            "humidity": 48,
            "precipitation_mm": 0.0,
            "wind_speed_kmph": 12.0,
            "weather_description": "Sunny"
        },
        "daily_forecast": [
            {
                "date": "2026-06-26",
                "max_temp_c": 37.0,
                "min_temp_c": 27.0,
                "avg_temp_c": 32.0,
                "total_precipitation_mm": 0.4,
                "max_wind_kmph": 28.0,
                "max_chance_of_rain": 60,
                "weather_description": "Partly cloudy"
            },
            {
                "date": "2026-06-27",
                "max_temp_c": 38.0,
                "min_temp_c": 28.0,
                "avg_temp_c": 33.0,
                "total_precipitation_mm": 0.0,
                "max_wind_kmph": 20.0,
                "max_chance_of_rain": 10,
                "weather_description": "Sunny"
            },
            {
                "date": "2026-06-28",
                "max_temp_c": 36.0,
                "min_temp_c": 26.0,
                "avg_temp_c": 31.0,
                "total_precipitation_mm": 0.0,
                "max_wind_kmph": 18.0,
                "max_chance_of_rain": 5,
                "weather_description": "Clear"
            }
        ]
    }