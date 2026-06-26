WEATHER_SCHEMA_SPEC = {
    "destination": str,
    "region": str,
    "country": str,
    "forecast_days": int,
    "current_weather": {
        "temperature_c": float,
        "humidity": int,
        "precipitation_mm": float,
        "wind_speed_kmph": float,
        "weather_description": str
    },
    "daily_forecast": [
        {
            "date": str,
            "max_temp_c": float,
            "min_temp_c": float,
            "avg_temp_c": float,
            "total_precipitation_mm": float,
            "max_wind_kmph": float,
            "max_chance_of_rain": int,
            "weather_description": str
        }
    ]
}

def validate_normalized_data(data: dict) -> bool:
    """Performs light structural type validation against the spec."""
    try:
        for key, expected_type in WEATHER_SCHEMA_SPEC.items():
            if key not in data:
                return False
            if isinstance(expected_type, dict):
                if not isinstance(data[key], dict):
                    return False
            elif isinstance(expected_type, list):
                if not isinstance(data[key], list):
                    return False
        return True
    except Exception:
        return False
