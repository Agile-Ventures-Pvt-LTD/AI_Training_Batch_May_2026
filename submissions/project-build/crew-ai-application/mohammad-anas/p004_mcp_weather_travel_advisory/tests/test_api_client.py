from unittest.mock import Mock, patch

import pytest
import requests

from src.api_client import get_weather_from_wttr


@patch("src.api_client.requests.get")
def test_get_weather_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "current_condition": [],
        "nearest_area": [],
        "weather": [],
    }

    mock_get.return_value = mock_response

    result = get_weather_from_wttr("Jaipur")

    assert result.success is True
    assert result.raw_weather_data is not None


@patch("src.api_client.requests.get")
def test_get_weather_http_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500

    mock_get.return_value = mock_response

    result = get_weather_from_wttr("Jaipur")

    assert result.success is False


@patch("src.api_client.requests.get")
def test_get_weather_invalid_json(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError

    mock_get.return_value = mock_response

    result = get_weather_from_wttr("Jaipur")

    assert result.success is False


@patch("src.api_client.requests.get")
def test_get_weather_timeout(mock_get):
    mock_get.side_effect = requests.Timeout

    result = get_weather_from_wttr("Jaipur")

    assert result.success is False


@patch("src.api_client.requests.get")
def test_get_weather_connection_error(mock_get):
    mock_get.side_effect = requests.ConnectionError

    result = get_weather_from_wttr("Jaipur")

    assert result.success is False


@pytest.mark.integration
def test_real_wttr_api():
    result = get_weather_from_wttr("Jaipur")

    assert result.success is True