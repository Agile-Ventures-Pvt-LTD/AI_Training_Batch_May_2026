import pytest
from src.server import mcp

@pytest.mark.anyio
async def test_required_resources_available():
    
    resources = await mcp.list_resources()
    uris = [str(r.uri) for r in resources]
    
    
    assert "resource://travel/checklist" in uris
    assert "resource://travel/advisory-rules" in uris
    assert "resource://weather/normalized-forecast-schema" in uris

   
    checklist_res = next(r for r in resources if str(r.uri) == "resource://travel/checklist")
    assert checklist_res.description == "Provides a static travel-readiness checklist."
