import pytest
from fastmcp import FastMCP

from src.prompts import register_prompts


@pytest.mark.anyio
async def test_required_prompts_available():
    mcp = FastMCP("Test")

    register_prompts(mcp)

    prompts = await mcp.list_prompts()
    names = {prompt.name for prompt in prompts}

    assert "travel_readiness_prompt" in names
    assert "weather_risk_summary_prompt" in names
    assert "packing_recommendation_prompt" in names