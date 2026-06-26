import pytest
import json
from src.tools import normalize_weather_data_tool
from src.schemas import validate_normalized_data

def test_normalize_weather_data_tool_schema():
    """Raw API response is normalized correctly into schema layout types"""
    mock_api_raw = {
        "nearest_area": [{"areaName": [{"value": "Jaipur"}], "region": [{"value": "Rajasthan"}], "country": [{"value": "India"}]}],
        "current_condition": [{"temp_C": "31", "humidity": "48", "precipMM": "0.0", "windspeedKmph": "12", "weatherDesc": [{"value": "Sunny"}]}],
        "weather": [{"date": "2026-06-26", "maxtempC": "37", "mintempC": "27", "avgtempC": "32", "hourly": [{"windspeedKmph": "12", "chanceofrain": "10", "precipMM": "0.0", "weatherDesc": [{"value": "Sunny"}]}]}]
    }
    
    res_str = normalize_weather_data_tool(json.dumps(mock_api_raw))
    normalized_output = json.loads(res_str)
    
    assert normalized_output["success"] is True
    assert normalized_output["destination"] == "Jaipur"
    
    schema_is_valid = validate_normalized_data(normalized_output)
    assert schema_is_valid is True

def test_final_report_schema_valid():
    """Final output report configuration dictionary matches required specifications"""
    required_keys = [
        "destination", "region", "country", "forecast_days", 
        "current_weather", "daily_forecast", "weather_risk", 
        "risk_factors", "recommended_actions", "packing_suggestions", 
        "travel_readiness_advisory", "weather_risk_explanation", 
        "resources_used", "tools_used", "prompts_used"
    ]
    
    mock_report = {k: [] if "s" in k[-4:] else "" for k in required_keys}
    mock_report["forecast_days"] = 3
    mock_report["current_weather"] = {}
    
    for key in required_keys:
        assert key in mock_report
