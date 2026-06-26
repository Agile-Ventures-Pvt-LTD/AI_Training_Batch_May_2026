import json
from report_writer import assemble_report
from tools import calculate_weather_risk_tool

def test_final_report_schema_valid(sample_normalized_data, sample_raw_wttr_response):
    risk_result = calculate_weather_risk_tool(sample_normalized_data)
    report = assemble_report(sample_normalized_data, risk_result)
    
    required_keys = [
        "destination", "region", "country", "forecast_days",
        "current_weather", "daily_forecast",
        "weather_risk", "risk_factors", "recommended_actions",
        "packing_suggestions",
        "travel_readiness_advisory", "weather_risk_explanation",
        "resources_used", "tools_used", "prompts_used"
    ]
    for key in required_keys:
        assert key in report
        
    assert isinstance(report["destination"], str)
    assert isinstance(report["region"], str)
    assert isinstance(report["country"], str)
    assert isinstance(report["forecast_days"], int)
    assert isinstance(report["current_weather"], dict)
    assert isinstance(report["daily_forecast"], list)
    assert report["weather_risk"] in ["LOW", "MEDIUM", "HIGH"]
    assert isinstance(report["risk_factors"], list)
    assert isinstance(report["recommended_actions"], list)
    assert isinstance(report["packing_suggestions"], list)
    assert isinstance(report["travel_readiness_advisory"], str)
    assert isinstance(report["weather_risk_explanation"], str)
    assert isinstance(report["resources_used"], list)
    assert isinstance(report["tools_used"], list)
    assert isinstance(report["prompts_used"], list)
    
    assert "resource://travel/checklist" in report["resources_used"]
    assert "resource://travel/advisory-rules" in report["resources_used"]
    assert "resource://weather/normalized-forecast-schema" in report["resources_used"]
    
    expected_tools = [
        "validate_city_input_tool",
        "get_weather_forecast_tool",
        "normalize_weather_data_tool",
        "calculate_weather_risk_tool",
        "save_travel_advisory_tool"
    ]
    for tool in expected_tools:
        assert tool in report["tools_used"]
        
    expected_prompts = [
        "travel_readiness_prompt",
        "weather_risk_summary_prompt",
        "packing_recommendation_prompt"
    ]
    for prompt in expected_prompts:
        assert prompt in report["prompts_used"]
        
    cw = report["current_weather"]
    assert isinstance(cw["temperature_c"], (int, float))
    assert isinstance(cw["humidity"], (int, float))
    assert isinstance(cw["precipitation_mm"], (int, float))
    assert isinstance(cw["wind_speed_kmph"], (int, float))
    assert isinstance(cw["weather_description"], str)
    
    for day in report["daily_forecast"]:
        assert isinstance(day["date"], str)
        assert isinstance(day["max_temp_c"], (int, float))
        assert isinstance(day["min_temp_c"], (int, float))
        assert isinstance(day["avg_temp_c"], (int, float))
        assert isinstance(day["total_precipitation_mm"], (int, float))
        assert isinstance(day["max_wind_kmph"], (int, float))
        assert isinstance(day["max_chance_of_rain"], (int, float))
        assert isinstance(day["weather_description"], str)

def test_report_serializable_to_json(sample_normalized_data):
    risk_result = calculate_weather_risk_tool(sample_normalized_data)
    report = assemble_report(sample_normalized_data, risk_result)
    json_str = json.dumps(report, indent=2)
    parsed = json.loads(json_str)
    assert parsed["destination"] == report["destination"]