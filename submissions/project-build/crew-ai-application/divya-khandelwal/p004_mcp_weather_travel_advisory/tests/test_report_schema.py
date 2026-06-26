import json
import pytest
from src.schemas import FinalReport

def test_final_report_schema_valid():
    data = {
        "destination": "Jaipur", "region": "Rajasthan", "country": "India", "forecast_days": 3,
        "current_weather": {}, "daily_forecast": [], "weather_risk": "MEDIUM",
        "risk_factors": ["Heat matches above 35C."], "recommended_actions": ["Avoid afternoon sun."],
        "packing_suggestions": ["Sunscreen"], "travel_readiness_advisory": "Manageable with caution.",
        "weather_risk_explanation": "Temperature limits exceeded."
    }
    report = FinalReport(**data)
    assert report.destination == "Jaipur"
    assert "validate_city_input_tool" in report.tools_used
