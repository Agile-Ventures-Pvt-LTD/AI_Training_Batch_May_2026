from src.api_client import get_weather_from_wttr


def test_get_weather_api_mock():
    res = get_weather_from_wttr("Jaipur")
    assert "success" in res