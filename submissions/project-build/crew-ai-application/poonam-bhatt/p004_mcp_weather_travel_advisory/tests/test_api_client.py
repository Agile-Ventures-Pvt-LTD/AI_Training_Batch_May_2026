import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.api_client import get_weather_from_wttr
from tests.mock_data import MOCK_RAW_WEATHER
def test_get_weather_from_wttr_mock_success(mocker):
    
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_RAW_WEATHER
    
    mocker.patch("requests.get", return_value=mock_response)
    
    res = get_weather_from_wttr("Jaipur")
    assert res["success"] is True
    assert "wttr.in" in res["url_used"]
    assert res["raw_weather_data"] == MOCK_RAW_WEATHER
def test_get_weather_from_wttr_mock_failure(mocker):
    
    mocker.patch("requests.get", side_effect=Exception("Connection timed out"))
    
    res = get_weather_from_wttr("Jaipur")
    assert res["success"] is False
    assert "Unable to fetch weather data" in res["message"]
    assert "Connection timed out" in res["message"]
@pytest.mark.integration
def test_real_wttr_api_for_jaipur():
    
    res = get_weather_from_wttr("Jaipur")
    assert res["success"] is True, f"Failed to contact wttr.in/wttr.is: {res.get('message')}"
    raw_data = res.get("raw_weather_data")
    assert "current_condition" in raw_data
    assert "weather" in raw_data
