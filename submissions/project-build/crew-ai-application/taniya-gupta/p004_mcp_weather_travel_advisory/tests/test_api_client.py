import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.api_client import get_weather

def test_get_weather_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"nearest_area": [], "current_condition": []}
    
    mocker.patch("requests.get", return_value=mock_response)
    
    result = get_weather("Jaipur")
    assert result["success"] is True
    assert result["raw_weather_data"] == {"nearest_area": [], "current_condition": []}

def test_get_weather_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    
    mocker.patch("requests.get", return_value=mock_response)
    
    result = get_weather("InvalidCity")
    assert result["success"] is False
    assert "Unable to fetch weather data" in result["message"]
