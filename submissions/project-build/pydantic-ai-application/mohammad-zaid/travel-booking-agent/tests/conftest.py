
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent import travel_agent, run_travel_agent, TravelDeps


@pytest.fixture
def agent():
  
    return travel_agent


@pytest.fixture
def run_agent():

    return run_travel_agent


@pytest.fixture
def deps():

    return TravelDeps(session_id="test-session")


@pytest.fixture
def sample_booking():

    return {
        "booking_id": "TRV-101",
        "user_name": "John Smith",
        "user_email": "john.smith@email.com",
        "destination": "London, UK",
        "travel_dates": "2025-02-15 to 2025-02-20",
        "hotel_details": "The Ritz London"
    }


@pytest.fixture
def sample_weather():
  
    return {
        "location": "London, United Kingdom",
        "date": "2025-02-15",
        "temperature_max": 8.5,
        "temperature_min": 3.2,
        "precipitation_probability": 75.0,
        "weather_description": "Moderate rain"
    }