import pytest
from src.api_client import get_weather_from_wttr

def test_get_weather_forecast_tool_mock_success(monkeypatch):
    """Verifies valid external payload processing using mocked targets."""
    class MockResponse:
        status_code = 200
        def json(self):
            return {"weather": [], "current_condition": [{}], "nearest_area": [{}]}
            
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())
    res = get_weather_from_wttr("Jaipur")
    assert res["success"] is True
    assert "raw_weather_data" in res
