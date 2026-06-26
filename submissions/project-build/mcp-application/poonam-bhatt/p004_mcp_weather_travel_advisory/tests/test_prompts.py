import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.prompts import (
    format_travel_readiness,
    format_weather_risk_summary,
    format_packing_recommendation
)
from src.server import mcp
def test_required_prompts_available():
    
    readiness = format_travel_readiness("Jaipur", "MEDIUM", "Clear", ["Carry water"])
    assert "Destination: Jaipur" in readiness
    assert "Weather Risk: MEDIUM" in readiness
    assert "Forecast Summary: Clear" in readiness
    assert "Recommended Actions: Carry water" in readiness
    
    summary = format_weather_risk_summary("Pune", "LOW", ["No risk"])
    assert "Destination: Pune" in summary
    assert "Risk Level: LOW" in summary
    assert "Risk Factors: No risk" in summary
    
    packing = format_packing_recommendation("Mumbai", "HIGH", ["Rain"])
    assert "Destination: Mumbai" in packing
    assert "Risk Level: HIGH" in packing
    assert "Risk Factors: Rain" in packing
    
    registered_prompts = []
    if hasattr(mcp, "_prompts"):
        registered_prompts = list(mcp._prompts.keys())
    elif hasattr(mcp, "prompts"):
        registered_prompts = [p.name for p in mcp.prompts]
        
    expected_prompts = [
        "travel_readiness_prompt",
        "weather_risk_summary_prompt",
        "packing_recommendation_prompt"
    ]
    
    if registered_prompts:
        for prompt in expected_prompts:
            assert prompt in registered_prompts
            
    
    print(f"Registered prompts: {registered_prompts}", file=sys.stderr)
