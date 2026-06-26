import pytest
import json
from unittest.mock import patch
from src.tools import get_weather_forecast_tool

def test_get_weather_forecast_tool_mock_success():
    """Mocked API response is handled correctly"""
    mock_raw_response = {"current_condition": [{"temp_C": "31"}], "weather": []}
    
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_raw_response
        
        # 1. Capture the MCP JSON string output
        res_str = get_weather_forecast_tool("Jaipur")
        
        # 2. Parse it back into a dictionary for testing assertions
        res = json.loads(res_str)
        
        assert res["success"] is True
        assert "raw_weather_data" in res

@pytest.mark.integration
def test_real_wttr_api_for_jaipur():
    """Real live integration API test wrapper"""
    res_str = get_weather_forecast_tool("Jaipur")
    
    res = json.loads(res_str)
    
    assert res["success"] is True
