import pytest
from src.schemas import FinalReport
from src.report_writer import generate_final_report

def test_final_report_schema_valid():
    normalized_data = {
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
        ]
    }
    
    risk_data = {
        "weather_risk": "MEDIUM",
        "risk_factors": [
            "Maximum temperature is expected to be above 35°C."
        ],
        "recommended_actions": [
            "Carry water and avoid long outdoor exposure during afternoon hours."
        ]
    }
    
    packing_suggestions = ["Water bottle", "Sunscreen"]
    travel_readiness_advisory = "Travel appears manageable with basic precautions."
    weather_risk_explanation = "The risk is medium due to heat."
    
    report = generate_final_report(
        normalized_data=normalized_data,
        risk_data=risk_data,
        packing_suggestions=packing_suggestions,
        travel_readiness_advisory=travel_readiness_advisory,
        weather_risk_explanation=weather_risk_explanation
    )
    
    validated = FinalReport(**report)
    
    assert validated.destination == "Jaipur"
    assert validated.weather_risk == "MEDIUM"
    assert "resource://travel/checklist" in validated.resources_used
    assert "validate_city_input_tool" in validated.tools_used
    assert "travel_readiness_prompt" in validated.prompts_used
