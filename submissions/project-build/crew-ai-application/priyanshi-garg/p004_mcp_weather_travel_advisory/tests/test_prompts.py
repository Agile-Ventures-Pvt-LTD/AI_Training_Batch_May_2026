import pytest
from src.prompts import TRAVEL_READINESS_PROMPT, WEATHER_RISK_SUMMARY_PROMPT, PACKING_RECOMMENDATION_PROMPT

def test_required_prompts_available():
    """All 3 structural prompts are exposed"""
    assert "Destination:" in TRAVEL_READINESS_PROMPT
    assert "Risk Level:" in WEATHER_RISK_SUMMARY_PROMPT
    assert "packing items" in PACKING_RECOMMENDATION_PROMPT
