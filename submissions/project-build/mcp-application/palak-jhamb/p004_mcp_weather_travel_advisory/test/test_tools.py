
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.tool import save_travel_advisory_tool,calculate_weather_risk_tool,normalize_weather_data_tool,get_weather_forecast_tool,validate_city_input_tool


def test_read_job_description_tool_success():
    result = validate_city_input_tool.invoke({"city":"st"})
    assert result["success"] is True


def test_validate_city_input_tool_city_with_space():
    result = validate_city_input_tool.invoke({"city":"new delhi"})
    assert result["success"] is True


def test_validate_city_input_tool_empty_city():
    result = validate_city_input_tool.invoke({"city":""})
    assert result["success"] is True


def test_get_weather_forecast_tool_mock_success():
    result = get_weather_forecast_tool.invoke({"city":"sonipat"})
    assert result["success"] is True
