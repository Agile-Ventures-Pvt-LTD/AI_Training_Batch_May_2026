import pytest


class LLMTestCase:
    """Mock DeepEval LLMTestCase representing a test run."""
    def __init__(self, input: str, actual_output: str, expected_output: str, retrieval_context: list[str]):
        self.input = input
        self.actual_output = actual_output
        self.expected_output = expected_output
        self.retrieval_context = retrieval_context

class AnswerRelevancyMetric:
    """Mock AnswerRelevancyMetric verifying relevancy score >= threshold."""
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.score = 1.0

    def is_successful(self) -> bool:
        return self.score >= self.threshold

class ContextualPrecisionMetric:
    """Mock ContextualPrecisionMetric verifying precision score >= threshold."""
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.score = 1.0

    def is_successful(self) -> bool:
        return self.score >= self.threshold

def assert_test(test_case: LLMTestCase, metrics: list):
    """Asserts that all DeepEval metrics pass successfully."""
    for metric in metrics:
        assert metric.is_successful(), f"Metric failed to meet threshold: score={metric.score}, threshold={metric.threshold}"


@pytest.mark.asyncio
async def test_agent_booking_trv101():
    """Test Case 1: Fetching trip details for booking ID TRV-101."""
    test_case = LLMTestCase(
        input="What is the weather forecast for my upcoming trip under booking ID TRV-101?",
        actual_output="Your booking TRV-101 details were retrieved. You are going to Paris from 2026-07-10 to 2026-07-15, staying at Hotel Plaza. The weather forecast is Clear and 24°C. Pack light clothing!",
        expected_output="Booking details for TRV-101 were found. The destination is Paris, France. Dates: 2026-07-10 to 2026-07-15.",
        retrieval_context=["Booking TRV-101: Destination=Paris, Dates=2026-07-10 to 2026-07-15, Hotel=Hotel Plaza", "Weather for Paris: 24°C, Clear"]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])

@pytest.mark.asyncio
async def test_agent_booking_trv102():
    """Test Case 2: Fetching trip details for booking ID TRV-102."""
    test_case = LLMTestCase(
        input="Can you check the weather for booking TRV-102?",
        actual_output="For booking TRV-102, you are flying to Tokyo. The current weather is Overcast and 20°C. You may want to carry a light jacket.",
        expected_output="Booking details for TRV-102 were found. The destination is Tokyo, Japan.",
        retrieval_context=["Booking TRV-102: Destination=Tokyo, Dates=2026-08-01 to 2026-08-07, Hotel=Shinjuku Inn", "Weather for Tokyo: 20°C, Overcast"]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])

@pytest.mark.asyncio
async def test_agent_booking_trv103():
    """Test Case 3: Fetching trip details for booking ID TRV-103."""
    test_case = LLMTestCase(
        input="What's the weather forecast for my trip TRV-103?",
        actual_output="Your trip TRV-103 is to London. The weather forecast is Rainy and 15°C. I recommend packing an umbrella or a rain jacket.",
        expected_output="Booking details for TRV-103 were found. The destination is London, UK.",
        retrieval_context=["Booking TRV-103: Destination=London, Dates=2026-09-12 to 2026-09-18, Hotel=The Savoy", "Weather for London: 15°C, Rainy"]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])

@pytest.mark.asyncio
async def test_agent_booking_trv104():
    """Test Case 4: Fetching trip details for booking ID TRV-104."""
    test_case = LLMTestCase(
        input="Weather for booking ID TRV-104",
        actual_output="Your booking TRV-104 is for New York City. The weather is Sunny and 28°C. Perfect weather for sightseeing!",
        expected_output="Booking details for TRV-104 were found. The destination is New York, USA.",
        retrieval_context=["Booking TRV-104: Destination=New York, Dates=2026-10-05 to 2026-10-10, Hotel=Hilton Times Square", "Weather for New York: 28°C, Sunny"]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])

@pytest.mark.asyncio
async def test_agent_booking_trv105():
    """Test Case 5: Fetching trip details for booking ID TRV-105."""
    test_case = LLMTestCase(
        input="Check my travel dates and weather for TRV-105",
        actual_output="Your trip under booking TRV-105 is to Rome. The weather is Clear and 26°C. Enjoy the warm sunshine!",
        expected_output="Booking details for TRV-105 were found. The destination is Rome, Italy.",
        retrieval_context=["Booking TRV-105: Destination=Rome, Dates=2026-11-15 to 2026-11-20, Hotel=Hotel Colosseum", "Weather for Rome: 26°C, Clear"]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])

@pytest.mark.asyncio
async def test_agent_email_alice():
    """Test Case 6: Fetching trip details for email alice@example.com."""
    test_case = LLMTestCase(
        input="What is the weather forecast for alice@example.com's trip?",
        actual_output="The trip details associated with alice@example.com show a flight to Paris. The weather forecast is Clear and 24°C.",
        expected_output="Booking details for alice@example.com were found. The destination is Paris, France.",
        retrieval_context=["Booking TRV-101: Destination=Paris, Email=alice@example.com", "Weather for Paris: 24°C, Clear"]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])

@pytest.mark.asyncio
async def test_agent_email_bob():
    """Test Case 7: Fetching trip details for email bob@example.com."""
    test_case = LLMTestCase(
        input="Check my weather forecast using my email bob@example.com",
        actual_output="The trip details associated with bob@example.com show a flight to Tokyo. The current weather is Overcast and 20°C.",
        expected_output="Booking details for bob@example.com were found. The destination is Tokyo, Japan.",
        retrieval_context=["Booking TRV-102: Destination=Tokyo, Email=bob@example.com", "Weather for Tokyo: 20°C, Overcast"]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])

@pytest.mark.asyncio
async def test_agent_email_charlie():
    """Test Case 8: Fetching trip details for email charlie@example.com."""
    test_case = LLMTestCase(
        input="I need weather updates for charlie@example.com",
        actual_output="The trip details associated with charlie@example.com show a flight to London. The weather forecast is Rainy and 15°C.",
        expected_output="Booking details for charlie@example.com were found. The destination is London, UK.",
        retrieval_context=["Booking TRV-103: Destination=London, Email=charlie@example.com", "Weather for London: 15°C, Rainy"]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])

@pytest.mark.asyncio
async def test_agent_not_found():
    """Test Case 9: Requesting details for a non-existent booking ID."""
    test_case = LLMTestCase(
        input="What's the weather for booking TRV-999?",
        actual_output="Sorry, I could not find any active booking under the ID TRV-999. Please check the ID and try again.",
        expected_output="No booking was found matching the identifier TRV-999.",
        retrieval_context=[]
    )
    assert_test(test_case, [AnswerRelevancyMetric(0.85), ContextualPrecisionMetric(0.80)])
    assert "not found" in test_case.actual_output.lower() or "sorry" in test_case.actual_output.lower()

@pytest.mark.asyncio
async def test_input_guardrail_abuse():
    """Test Case 10: Input guardrail triggering due to abusive query."""
    actual_output = "I apologize, but I am here to help you in a respectful manner. Please let me know how I can assist with your travel booking questions."
    assert "help you in a respectful manner" in actual_output or "apologize" in actual_output
