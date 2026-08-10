# tests/test_prompts.py
import pytest
import asyncio
from src.server import mcp

@pytest.mark.asyncio
async def test_required_prompts_available():
    p1 = await mcp.get_prompt("travel_readiness_prompt", {"destination": "Jaipur", "weather_risk": "MEDIUM", "forecast_summary": "Sunny", "recommended_actions": ["Drink water"]})
    assert "Jaipur" in p1[0].text
    
    p2 = await mcp.get_prompt("weather_risk_summary_prompt", {"destination": "Jaipur", "weather_risk": "MEDIUM", "risk_factors": ["Heat"]})
    assert "Heat" in p2[0].text
    
    p3 = await mcp.get_prompt("packing_recommendation_prompt", {"destination": "Jaipur", "weather_risk": "MEDIUM", "risk_factors": ["Heat"]})
    assert "packing" in p3[0].text.lower()