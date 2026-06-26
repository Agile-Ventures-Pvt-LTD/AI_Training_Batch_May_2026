import pytest
from src.prompts import travel_readiness_prompt, weather_risk_summary_prompt, packing_recommendation_prompt

@pytest.mark.asyncio
async def test_required_prompts_available():
    """Verify that all 3 prompts correctly merge template fields into raw text strings."""
    p1 = await travel_readiness_prompt("Jaipur", "LOW", "Sunny", ["Carry water"])
    p2 = await weather_risk_summary_prompt("Jaipur", "LOW", ["None"])
    p3 = await packing_recommendation_prompt("Jaipur", "LOW", "Sunny")
    assert "Jaipur" in p1
    assert "LOW" in p2
    assert "packing" in p3.lower()
