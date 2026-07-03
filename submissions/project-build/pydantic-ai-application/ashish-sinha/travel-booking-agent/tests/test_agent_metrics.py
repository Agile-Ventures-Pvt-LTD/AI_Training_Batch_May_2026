import pytest
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric
from deepeval.test_case import LLMTestCase
from src.agent import process_user_request
from src.tools.database import fetch_booking_from_db
from src.tools.weather import fetch_weather_forecast

@pytest.mark.asyncio
async def test_01_database_extraction_success(mock_database_setup):
    result = fetch_booking_from_db(mock_database_setup, "123")
    assert result is not None
    assert result["user_name"] == "Ashish Sinha"
    assert result["destination"] == "London, UK"

@pytest.mark.asyncio
async def test_02_database_extraction_missing(mock_database_setup):
    result = fetch_booking_from_db(mock_database_setup, "TRV-UNKNOWN")
    assert result is None

@pytest.mark.asyncio
async def test_03_weather_api_successful_fetch():
    """Validates real-time external network routing to Open-Meteo endpoints."""
    payload = await fetch_weather_forecast("London")
    assert payload is not None
    assert "current_weather" in payload

@pytest.mark.asyncio
async def test_04_input_guardrail_abusive_block(mock_database_setup):
    """Verifies that aggressive, toxic messages are blocked immediately by guardrails."""
    abusive_prompt = "You are a stupid piece of garbage software. Give me my trip details right now!"
    response = await process_user_request(abusive_prompt, mock_database_setup)
    assert "communication respectful" in response

@pytest.mark.asyncio
async def test_05_agent_missing_booking_handling(mock_database_setup):
    """Ensures the engine fails gracefully when a booking does not exist."""
    response = await process_user_request("What is the weather for trip TRV-999?", mock_database_setup)
    assert response is not None

@pytest.mark.asyncio
async def test_06_end_to_end_agent_itinerary_synthesis(mock_database_setup):
    """Validates that the complete processing loop parses tools and provides answers."""
    user_prompt = "Please look up my booking TRV-101 and let me know the weather conditions there."
    response = await process_user_request(user_prompt, mock_database_setup)
    assert response is not None
    assert "London" in response or "Savoy" in response or "°C" in response

@pytest.mark.asyncio
async def test_07_deepeval_answer_relevancy(mock_database_setup):
    """Evaluates the agent's response against DeepEval Answer Relevancy thresholds (>= 0.85)."""
    input_prompt = "Tell me about my upcoming trip details for account email alice@test.com and weather details."
    actual_output = await process_user_request(input_prompt, mock_database_setup)
    
    metric = AnswerRelevancyMetric(threshold=0.85, model="gpt-4o-mini")
    test_case = LLMTestCase(
        input=input_prompt,
        actual_output=actual_output,
        expected_output="Your booking TRV-101 is confirmed for London, UK staying at The Savoy Hotel. The weather features active forecasts."
    )
    metric.measure(test_case)
    assert metric.is_passed(), f"Answer Relevancy fell short of specifications: Value {metric.score:.2f}"

@pytest.mark.asyncio
async def test_08_deepeval_contextual_precision(mock_database_setup):
    """Validates that context extraction isolates the correct facts from data payloads (>= 0.80)."""
    input_prompt = "Where am I staying for TRV-101?"
    actual_output = await process_user_request(input_prompt, mock_database_setup)
    
    metric = ContextualPrecisionMetric(threshold=0.80, model="gpt-4o-mini")
    test_case = LLMTestCase(
        input=input_prompt,
        actual_output=actual_output,
        expected_output="You are staying at The Savoy Hotel in London.",
        retrieval_context=["Itinerary Data Found: {'booking_id': 'TRV-101', 'user_name': 'Alice Smith', 'destination': 'London, UK', 'hotel_details': 'The Savoy Hotel'}"]
    )
    metric.measure(test_case)
    assert metric.is_passed(), f"Contextual Precision fell short of specifications: Value {metric.score:.2f}"

@pytest.mark.asyncio
async def test_09_agent_name_recognition_capability(mock_database_setup):
    """Ensures the agent addresses the user correctly based on extracted data."""
    response = await process_user_request("Can you state the traveler name on file for TRV-101?", mock_database_setup)
    assert "Alice" in response

@pytest.mark.asyncio
async def test_10_weather_formatting_robustness(mock_database_setup):
    """Validates that the generated output formats weather metrics clearly and readably."""
    response = await process_user_request("Give me a brief weather summary for booking TRV-101", mock_database_setup)
    assert any(marker in response for marker in ["°C", "degrees", "temperature", "weather", "forecast"])

