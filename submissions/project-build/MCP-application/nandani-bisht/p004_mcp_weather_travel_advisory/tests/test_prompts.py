import pytest
from src.server import mcp

@pytest.mark.anyio
async def test_required_prompts_available():
    
    prompts = await mcp.list_prompts()
    prompt_names = [p.name for p in prompts]
    
    
    assert "travel_readiness_prompt" in prompt_names
    assert "weather_risk_summary_prompt" in prompt_names
    assert "packing_recommendation_prompt" in prompt_names
    
  
    travel_prompt = next(p for p in prompts if p.name == "travel_readiness_prompt")
    assert travel_prompt.description == "Creates a concise travel-readiness advisory."
