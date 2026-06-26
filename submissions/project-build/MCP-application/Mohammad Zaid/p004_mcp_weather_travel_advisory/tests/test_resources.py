# tests/test_resources.py
import pytest
import asyncio
from src.server import mcp

@pytest.mark.asyncio
async def test_required_resources_available():
    schema = await mcp.read_resource("resource://weather/normalized-forecast-schema")
    assert "temperature_c" in schema[0].text
    
    checklist = await mcp.read_resource("resource://travel/checklist")
    assert "Confirm destination" in checklist[0].text
    
    rules = await mcp.read_resource("resource://travel/advisory-rules")
    assert "HIGH:" in rules[0].text