import sys
import os
import pytest
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.schemas import TravelAdvisoryReport, CurrentWeather, DailyForecast
from src.report_writer import build_travel_advisory_report
def test_final_report_schema_valid():
    normalized_data = {
        "destination": "Jaipur",
        "region": "Rajasthan",
        "country": "India",
        "forecast_days": 1,
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
                "max_chance_of_rain": 60.0,
                "weather_description": "Partly cloudy"
            }
        ]
    }
    
    risk_assessment = {
        "weather_risk": "MEDIUM",
        "risk_factors": ["Maximum temperature is expected to be above 35°C."],
        "recommended_actions": ["Carry water and avoid long outdoor exposure during afternoon hours."]
    }
    
    packing_suggestions = ["Water bottle", "Sunscreen"]
    travel_readiness = "Travel appears manageable with basic weather precautions."
    risk_explanation = "The risk level is medium because moderate heat and wind indicators are present."
    
    report_dict = build_travel_advisory_report(
        normalized_data=normalized_data,
        risk_assessment=risk_assessment,
        packing_suggestions=packing_suggestions,
        travel_readiness_advisory=travel_readiness,
        weather_risk_explanation=risk_explanation
    )
    
    try:
        report_obj = TravelAdvisoryReport(**report_dict)
    except ValidationError as e:
        pytest.fail(f"Report validation failed against TravelAdvisoryReport schema: {e}")
    
    assert report_obj.destination == "Jaipur"
    assert report_obj.region == "Rajasthan"
    assert report_obj.country == "India"
    assert report_obj.forecast_days == 1
    assert report_obj.current_weather.temperature_c == 31.0
    assert report_obj.daily_forecast[0].date == "2026-06-26"
    assert report_obj.weather_risk == "MEDIUM"
    assert "Maximum temperature is expected to be above 35°C." in report_obj.risk_factors
    assert "Carry water and avoid long outdoor exposure during afternoon hours." in report_obj.recommended_actions
    assert report_obj.packing_suggestions == ["Water bottle", "Sunscreen"]
    assert report_obj.travel_readiness_advisory == travel_readiness
    assert report_obj.weather_risk_explanation == risk_explanation
    
    
    assert "validate_city_input_tool" in report_obj.tools_used
    assert "resource://travel/checklist" in report_obj.resources_used
    assert "travel_readiness_prompt" in report_obj.prompts_used
