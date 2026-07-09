import pytest
from api_client import get_weather_from_wttr
def test_get_weather_forecast_tool_mock_success(monkeypatch):
    class MockResponse:
        status_code = 200
        def json(self):
            return {"current_condition": [],"nearest_area": [],"weather": [],}
    def mock_get(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr("requests.get",mock_get,)
    result = get_weather_from_wttr("Jaipur")
    assert result["success"] is True
    assert "raw_weather_data" in result
@pytest.mark.integration
def test_real_wttr_api_for_jaipur():
    result = get_weather_from_wttr("Jaipur")
    assert isinstance(result, dict)
    if result["success"]:
        assert "raw_weather_data" in result
