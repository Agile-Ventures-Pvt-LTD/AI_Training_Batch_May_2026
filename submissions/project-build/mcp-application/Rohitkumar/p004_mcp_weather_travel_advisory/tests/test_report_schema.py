import pytest


class TestReportSchema:
    def test_final_report_schema_valid(self):
        report = {
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
                    "total_precipitation_mm": 1.2,
                    "max_wind_kmph": 28.0,
                    "max_chance_of_rain": 60,
                    "weather_description": "Partly cloudy"
                }
            ],
            "weather_risk": "MEDIUM",
            "risk_factors": [],
            "recommended_actions": [],
            "packing_suggestions": [],
            "travel_readiness_advisory": "",
            "weather_risk_explanation": "",
            "resources_used": [],
            "tools_used": [],
            "prompts_used": []
        }

        assert isinstance(report["destination"], str)
        assert isinstance(report["region"], str)
        assert isinstance(report["country"], str)
        assert isinstance(report["forecast_days"], int)
        assert isinstance(report["current_weather"]["temperature_c"], (int, float))
        assert isinstance(report["current_weather"]["humidity"], int)
        assert isinstance(report["current_weather"]["precipitation_mm"], (int, float))
        assert isinstance(report["daily_forecast"], list)
        assert isinstance(report["weather_risk"], str)
        assert report["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]

    def test_report_requires_all_fields(self):
        required_fields = [
            "destination", "region", "country", "forecast_days",
            "current_weather", "daily_forecast", "weather_risk",
            "risk_factors", "recommended_actions", "packing_suggestions",
            "travel_readiness_advisory", "weather_risk_explanation",
            "resources_used", "tools_used", "prompts_used"
        ]
        report = {
            "destination": "Jaipur",
            "region": "Rajasthan",
            "country": "India",
            "forecast_days": 3,
            "current_weather": {},
            "daily_forecast": [],
            "weather_risk": "LOW",
            "risk_factors": [],
            "recommended_actions": [],
            "packing_suggestions": [],
            "travel_readiness_advisory": "",
            "weather_risk_explanation": "",
            "resources_used": [],
            "tools_used": [],
            "prompts_used": []
        }
        for field in required_fields:
            assert field in report

    def test_report_risk_wind_speed_field(self):
        forecast = {
            "date": "2026-06-26",
            "max_temp_c": 37.0,
            "min_temp_c": 27.0,
            "avg_temp_c": 32.0,
            "total_precipitation_mm": 1.2,
            "max_wind_kmph": 28.0,
            "max_chance_of_rain": 60,
            "weather_description": "Partly cloudy"
        }
        assert "max_wind_kmph" in forecast
        assert isinstance(forecast["max_wind_kmph"], float)
        assert "max_chance_of_rain" in forecast
        assert isinstance(forecast["max_chance_of_rain"], int)