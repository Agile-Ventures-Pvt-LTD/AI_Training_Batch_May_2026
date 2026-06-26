import pytest
from src.prompts import travel_readiness_prompt,weather_risk_summary_prompt,packing_recommendation_prompt

def test_travel_readiness_prompt_generation():
    prompt = travel_readiness_prompt("Jaipur", "HIGH", "Sunny and Hot", ["Stay hydrated"])
    assert "Jaipur" in prompt
    assert "HIGH" in prompt
    assert "Stay hydrated" in prompt

def test_weather_risk_summary_prompt_generation():
    prompt = weather_risk_summary_prompt("Pune", "MEDIUM", ["Moderate rain risk"])
    assert "Pune" in prompt
    assert "MEDIUM" in prompt
    assert "Moderate rain risk" in prompt

def test_packing_recommendation_prompt_generation():
    prompt = packing_recommendation_prompt("Goa", "LOW", [])
    assert "Goa" in prompt
    assert "LOW" in prompt
