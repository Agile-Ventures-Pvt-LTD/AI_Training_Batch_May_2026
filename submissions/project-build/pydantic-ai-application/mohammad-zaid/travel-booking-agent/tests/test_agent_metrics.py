
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric
from deepeval.test_case import LLMTestCase

from agent import travel_agent, run_travel_agent, TravelDeps
from tools.database import get_user_bookings
from tools.weather import get_weather_forecast, get_city_coordinates
from guardrails_config import validate_input, validate_output, INPUT_DEESCALATION_MESSAGE

RELEVANCY_METRIC = AnswerRelevancyMetric(threshold=0.85, model="gpt-4o-mini")
PRECISION_METRIC = ContextualPrecisionMetric(threshold=0.80, model="gpt-4o-mini")


async def get_response(prompt: str) -> str:
    deps = TravelDeps()
    result = await travel_agent.run(prompt, deps=deps)
    return result.data

# Test 1 : Answer Relavency
@pytest.mark.asyncio
async def test_answer_relevancy_weather_query():
    prompt = "What's the weather going to be like for my upcoming trip? My ID is TRV-101"
    
    response = await get_response(prompt)
    bookings = get_user_bookings("TRV-101")
    context = [str(i) for i in bookings]
    
    test_case = LLMTestCase(
        input=prompt,
        actual_output=response,
        expected_output="Weather forecast for London",
        retrieval_context=context
    )
    
    result = RELEVANCY_METRIC.measure(test_case)
    assert result.score >= 0.85, f"Score {result.score} < 0.85. Reason: {result.reason}"



# TEST 2: Contextual Precision
@pytest.mark.asyncio
async def test_contextual_precision_booking_data():
    
    prompt = "Tell me about my booking TRV-101"
    
    response = await get_response(prompt)
    bookings = get_user_bookings("TRV-101")
    context = [str(b) for b in bookings]
    
    test_case = LLMTestCase(
        input=prompt,
        actual_output=response,
        expected_output="Booking TRV-101 for John Smith to London",
        retrieval_context=context
    )
    
    result = PRECISION_METRIC.measure(test_case)
    assert result.score >= 0.80, f"Score {result.score} < 0.80. Reason: {result.reason}"


# TEST 3: Answer Relevancy 

@pytest.mark.asyncio
async def test_answer_relevancy_multiple_bookings():
    """Agent should give relevant response for user with multiple trips."""
    prompt = "Show me all my upcoming trips. I'm jane.doe@email.com"
    
    response = await get_response(prompt)
    bookings = get_user_bookings("jane.doe@email.com")
    context = [str(b) for b in bookings]
    
    test_case = LLMTestCase(
        input=prompt,
        actual_output=response,
        expected_output="List of Jane Doe's upcoming trips",
        retrieval_context=context
    )
    
    result = RELEVANCY_METRIC.measure(test_case)
    assert result.score >= 0.85, f"Score {result.score} < 0.85. Reason: {result.reason}"


# TEST 4: Contextual Precision - Weather integration

@pytest.mark.asyncio
async def test_contextual_precision_weather_integration():

    prompt = "I'm going to London on 2025-02-15. Should I pack an umbrella?"
    
    response = await get_response(prompt)
    context = ["London weather forecast with precipitation probability"]
    
    test_case = LLMTestCase(
        input=prompt,
        actual_output=response,
        expected_output="Packing recommendation based on London rain forecast",
        retrieval_context=context
    )
    
    result = PRECISION_METRIC.measure(test_case)
    assert result.score >= 0.80, f"Score {result.score} < 0.80. Reason: {result.reason}"


# TEST 5: Answer Relevancy - Packing advice

@pytest.mark.asyncio
async def test_answer_relevancy_packing_advice():
    """Agent should give relevant packing advice for destination."""
    prompt = "What should I pack for my Tokyo trip? My email is jane.doe@email.com"
    
    response = await get_response(prompt)
    bookings = get_user_bookings("jane.doe@email.com")
    tokyo_bookings = [b for b in bookings if "Tokyo" in b.get("destination", "")]
    context = [str(b) for b in tokyo_bookings]
    
    test_case = LLMTestCase(
        input=prompt,
        actual_output=response,
        expected_output="Packing recommendations for Tokyo trip",
        retrieval_context=context
    )
    
    result = RELEVANCY_METRIC.measure(test_case)
    assert result.score >= 0.85, f"Score {result.score} < 0.85. Reason: {result.reason}"


# TEST 6: Contextual Precision - Hotel information

@pytest.mark.asyncio
async def test_contextual_precision_hotel_info():
    prompt = "What hotel am I staying at for booking TRV-105?"
    
    response = await get_response(prompt)
    bookings = get_user_bookings("TRV-105")
    context = [str(b) for b in bookings]
    
    test_case = LLMTestCase(
        input=prompt,
        actual_output=response,
        expected_output="Shangri-La Sydney hotel information",
        retrieval_context=context
    )
    
    result = PRECISION_METRIC.measure(test_case)
    assert result.score >= 0.80, f"Score {result.score} < 0.80. Reason: {result.reason}"


# TEST 7: Answer Relevancy - Trip dates query

@pytest.mark.asyncio
async def test_answer_relevancy_trip_dates():
  
    prompt = "When exactly am I traveling to Paris? My booking is TRV-102"
    
    response = await get_response(prompt)
    bookings = get_user_bookings("TRV-102")
    context = [str(b) for b in bookings]
    
    test_case = LLMTestCase(
        input=prompt,
        actual_output=response,
        expected_output="Travel dates for Paris trip",
        retrieval_context=context
    )
    
    result = RELEVANCY_METRIC.measure(test_case)
    assert result.score >= 0.85, f"Score {result.score} < 0.85. Reason: {result.reason}"


# TEST 8: Input Guardrails - Profanity detection

def test_input_guardrails_profanity():
    profane_input = "Where the fuck is my booking"
    
    is_valid, response = validate_input(profane_input)
    
    assert is_valid is False, "Profane input should be blocked"
    assert "respectful" in response.lower(), "Should show de-escalation message"


# TEST 9: Input Guardrails - Valid input passes

def test_input_guardrails_valid():
    """Normal valid input should pass through guardrails."""
    valid_inputs = [
        "What's the weather for my trip?",
        "Check my booking TRV-101",
        "I'm traveling to Paris, what should I pack?"
    ]
    
    for input_text in valid_inputs:
        is_valid, response = validate_input(input_text)
        assert is_valid is True, f"Should pass: {input_text}"
        assert response == input_text, "Should return unchanged"


# TEST 10: Output Guardrails - Valid output passes

def test_output_guardrails_valid():
    """Normal agent output should pass output guardrails."""
    valid_output = "Based on your London booking, I recommend packing an umbrella."
    
    is_valid, response = validate_output(valid_output)
    
    assert is_valid is True, "Valid output should pass"
    assert response == valid_output, "Should return unchanged"


# TEST 11: Database tool - Booking lookup

def test_database_booking_lookup():
    """Database tool should retrieve booking by ID."""
    bookings = get_user_bookings("TRV-101")
    
    assert len(bookings) > 0, "Should find booking TRV-101"
    assert bookings[0]["destination"] == "London, UK"
    assert bookings[0]["hotel_details"] == "The Ritz London"


# TEST 12: Database tool - Non-existent booking

def test_database_nonexistent_booking():
    """Database tool should return empty list for non-existent booking."""
    bookings = get_user_bookings("TRV-999")
    
    assert len(bookings) == 0, "Should return empty list"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])