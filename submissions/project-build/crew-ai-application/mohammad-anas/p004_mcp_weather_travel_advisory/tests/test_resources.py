import pytest
from fastmcp import FastMCP

from src.resources import register_resources


@pytest.mark.anyio
async def test_required_resources_available():
    mcp = FastMCP("Test")

    register_resources(mcp)

    resources = await mcp.list_resources()
    uris = {str(resource.uri) for resource in resources}

    assert "resource://travel/checklist" in uris
    assert "resource://travel/advisory-rules" in uris
    assert "resource://weather/normalized-forecast-schema" in uris