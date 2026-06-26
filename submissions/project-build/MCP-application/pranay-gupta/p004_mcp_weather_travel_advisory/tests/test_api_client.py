import pytest
from unittest.mock import patch, MagicMock
from api_client import get_weather_from_wttr

def test_api_client_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"current_condition": [{"temp_C": "31"}]}
    with patch("api_client.requests.get", return_value=mock_response):
        result = get_weather_from_wttr("Jaipur")
    assert result["success"] is True
    assert "raw_weather_data" in result
    assert "url_used" in result

def test_api_client_http_error():
    mock_response = MagicMock()
    mock_response.status_code = 404
    with patch("api_client.requests.get", return_value=mock_response):
        result = get_weather_from_wttr("InvalidCity")
    assert result["success"] is False
    assert "message" in result

def test_api_client_timeout():
    import requests as req
    with patch("api_client.requests.get", side_effect=req.exceptions.Timeout("Timeout")):
        result = get_weather_from_wttr("Jaipur")
    assert result["success"] is False
    assert "message" in result

def test_api_client_connection_error():
    import requests as req
    with patch("api_client.requests.get", side_effect=req.exceptions.ConnectionError("No connection")):
        result = get_weather_from_wttr("Jaipur")
    assert result["success"] is False
    assert "message" in result