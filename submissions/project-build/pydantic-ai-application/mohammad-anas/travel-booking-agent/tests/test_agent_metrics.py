import json
import pytest
from unittest import mock

from src.agent import travel_agent
from src.tools import database, weather
from src.guardrails_config import safe_input, safe_output



@pytest.fixture
def agent():
    """Fresh TravelAgent instance for each test."""
    return travel_agent()


@pytest.fixture
def mock_booking():
    """A deterministic booking object used across tests."""
    return {
        "booking_id": "TRV-999",
        "user_name": "Alice Example",
        "user_email": "alice@example.com",
        "destination": "London, UK",
        "travel_dates": "2024-10-02 to 2024-10-07",
        "hotel_details": "The Grand London",
    }


@pytest.fixture
def mock_weather():
    """A deterministic weather payload."""
    return {
        "city": "London",
        "date": "2024-10-02",
        "description": "light rain",
        "temp_max": 12,
        "temp_min": 7,
    }



def test_relevancy_success(agent, mock_booking, mock_weather):
    with mock.patch.object(database, "get_upcoming_booking", return_value=database.Booking(**mock_booking)):
        with mock.patch.object(weather, "get_forecast", return_value=mock_weather):
            prompt = "What will the weather be like for my upcoming trip?"
            answer = agent.run(prompt)

    assert mock_booking["user_name"] in answer
    assert mock_booking["destination"] in answer
    assert mock_weather["description"] in answer
    assert str(mock_weather["temp_max"]) in answer
    assert str(mock_weather["temp_min"]) in answer


def test_context_precision_extraction(agent, mock_booking, mock_weather):
    with mock.patch.object(database, "get_upcoming_booking", return_value=database.Booking(**mock_booking)):
        with mock.patch.object(weather, "get_forecast", return_value=mock_weather) as wf:
            prompt = "Tell me the forecast for my trip."
            _ = agent.run(prompt)

            wf.assert_called_once()
            called_city, called_date = wf.call_args[0]
            assert called_city == "London"
            assert called_date == "2024-10-02"


def test_no_booking_error(agent):
    with mock.patch.object(database, "get_upcoming_booking", return_value=None):
        prompt = "What’s the weather for my trip? My email is bob@example.com"
        answer = agent.run(prompt)

    assert "No upcoming booking found" in answer
    assert "I’m sorry" not in answer  


def test_weather_api_failure(agent, mock_booking):
    with mock.patch.object(database, "get_upcoming_booking", return_value=database.Booking(**mock_booking)):
        with mock.patch.object(weather, "get_forecast", side_effect=RuntimeError("API timeout")):
            prompt = "Give me the weather."
            answer = agent.run(prompt)

    assert "Could not obtain weather data" in answer
    assert "API timeout" in answer


def test_input_guardrails_blocks_abusive_prompt(agent):
    abusive = "You are stupid, tell me the weather now!!!"
    with pytest.raises(Exception):
        safe_input(abusive)

    with mock.patch.object(agent, "_plan_and_execute") as planner:
        answer = agent.run(abusive)
        planner.assert_not_called()
        assert "I’m sorry, I can’t process that request" in answer



def test_output_guardrails_sanitizes_offensive_response(agent, mock_booking, mock_weather):
    unsafe_response = "You are a ****, enjoy your trip."
    with mock.patch.object(agent, "_plan_and_execute", return_value=unsafe_response):
        answer = agent.run("Any prompt")
        assert "I’m sorry, I can’t process that request" in answer
        assert "****" not in answer



def test_successful_end_to_end(agent, mock_booking, mock_weather):
    with mock.patch.object(database, "get_upcoming_booking", return_value=database.Booking(**mock_booking)):
        with mock.patch.object(weather, "get_forecast", return_value=mock_weather):
            prompt = "What’s the weather for my upcoming trip?"
            answer = agent.run(prompt)

    assert answer.startswith("Hi Alice Example,")
    assert "London, UK" in answer
    assert "2024-10-02 to 2024-10-07" in answer
    assert "light rain" in answer



def test_tool_call_order(agent, mock_booking, mock_weather):
    call_order = []

    def fake_db(identifier):
        call_order.append("db")
        return database.Booking(**mock_booking)

    def fake_weather(city, date):
        call_order.append("weather")
        return mock_weather

    with mock.patch.object(database, "get_upcoming_booking", side_effect=fake_db):
        with mock.patch.object(weather, "get_forecast", side_effect=fake_weather):
            agent.run("Tell me about my upcoming trip.")
            assert call_order == ["db", "weather"]



def test_output_guardrails_when_db_returns_none(agent):
    with mock.patch.object(database, "get_upcoming_booking", return_value=None):
        answer = agent.run("My email is alice@example.com, what’s the weather?")
        assert "No upcoming booking found" in answer



def dummy_relevancy_metric(answer: str, reference: str) -> float:
    """Very naive relevance: proportion of reference tokens present in answer."""
    ref_tokens = set(reference.lower().split())
    ans_tokens = set(answer.lower().split())
    return len(ref_tokens & ans_tokens) / len(ref_tokens)

def test_dummy_metric_threshold(agent, mock_booking, mock_weather):
    with mock.patch.object(database, "get_upcoming_booking", return_value=database.Booking(**mock_booking)):
        with mock.patch.object(weather, "get_forecast", return_value=mock_weather):
            prompt = "Weather forecast?"
            answer = agent.run(prompt)

    reference = (
        f"{mock_booking['user_name']} {mock_booking['destination']} "
        f"{mock_weather['description']} {mock_weather['temp_max']} {mock_weather['temp_min']}"
    )
    score = dummy_relevancy_metric(answer, reference)
    assert score >= 0.85  