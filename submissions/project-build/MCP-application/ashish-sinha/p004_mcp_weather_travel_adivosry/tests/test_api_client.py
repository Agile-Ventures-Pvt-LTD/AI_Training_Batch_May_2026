import pytest
from unittest.mock import patch, MagicMock
from src.api_client import get_weather_from_wttr

@patch("src.api_client.requests.get")
def test_get_weather_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"nearest_area": [], "current_condition": [], "weather": []}

    result = get_weather_from_wttr("Jaipur")
    assert result["success"] is True
    assert "raw_weather_data" in result
    assert result["city_name"] == "Jaipur"

@patch("src.api_client.requests.get")
def test_get_weather_failover_to_fallback(mock_get):
    mock_fallback_response = MagicMock()
    mock_fallback_response.status_code = 200
    mock_fallback_response.json.return_value = {"nearest_area": [], "current_condition": [], "weather": []}
    mock_get.side_effect = [Exception("Primary Timeout"), mock_fallback_response]

    result = get_weather_from_wttr("Pune")
    assert result["success"] is True
    assert "raw_weather_data" in result

@patch("src.api_client.requests.get")
def test_get_weather_total_failure(mock_get):
    mock_get.side_effect = Exception("Connection Refused")
    result = get_weather_from_wttr("InvalidCity")
    assert result["success"] is False
    assert "Unable to fetch weather data" in result["message"]
