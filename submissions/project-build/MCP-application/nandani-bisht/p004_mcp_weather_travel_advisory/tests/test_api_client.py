import pytest
from unittest.mock import patch, MagicMock
from src.tools import get_weather_forecast

def test_get_weather_forecast_tool_mock_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "current_condition": [
            {
                "temp_C": "31",
                "humidity": "48",
                "precipMM": "0.0",
                "windspeedKmph": "12",
                "weatherDesc": [{"value": "Sunny"}]
            }
        ],
        "nearest_area": [
            {
                "areaName": [{"value": "Jaipur"}],
                "region": [{"value": "Rajasthan"}],
                "country": [{"value": "India"}]
            }
        ],
        "weather": []
    }
    
    with patch("requests.get", return_value=mock_response) as mock_get:
        result = get_weather_forecast("Jaipur")
        assert result["success"] is True
        assert result["city_name"] == "Jaipur"
        assert "raw_weather_data" in result
        assert result["raw_weather_data"]["current_condition"][0]["temp_C"] == "31"
        mock_get.assert_called_once()

@pytest.mark.integration
def test_real_wttr_api_for_jaipur():
    result = get_weather_forecast("Jaipur")
    if result["success"]:
        assert result["city_name"] == "Jaipur"
        assert "raw_weather_data" in result
        assert "current_condition" in result["raw_weather_data"]
    else:
        assert result["success"] is False
        assert result["message"] == "Unable to fetch weather data."