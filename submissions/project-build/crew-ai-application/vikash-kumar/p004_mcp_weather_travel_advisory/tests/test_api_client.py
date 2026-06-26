import pytest
from src.api_client import get_weather_from_wttr

@pytest.mark.integration
def test_real_wttr_api_for_jaipur():
    test = get_weather_from_wttr("Jaipur")
    assert test["success"] is True
    assert "raw_weather_data" in test
