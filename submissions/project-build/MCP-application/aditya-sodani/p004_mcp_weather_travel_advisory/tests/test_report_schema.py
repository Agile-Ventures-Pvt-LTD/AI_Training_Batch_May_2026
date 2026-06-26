from src.report_writer import build_report


def test_final_report_schema_valid():
    normalized = {
        "destination": "Jaipur",
        "region": "Rajasthan",
        "country": "India",
        "forecast_days": 1,
        "current_weather": {
            "temperature_c": 30,
            "humidity": 40,
            "precipitation_mm": 0,
            "wind_speed_kmph": 10,
            "weather_description": "Sunny"
        },
        "daily_forecast": []
    }

    risk = {
        "weather_risk": "LOW",
        "risk_factors": [],
        "recommended_actions": []
    }

    report = build_report(normalized, risk)

    assert "destination" in report
    assert "weather_risk" in report
    assert "resources_used" in report
    assert "tools_used" in report
    assert "prompts_used" in report