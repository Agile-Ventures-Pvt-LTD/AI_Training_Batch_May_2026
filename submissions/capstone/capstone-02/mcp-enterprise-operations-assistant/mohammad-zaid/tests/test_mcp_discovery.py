import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.tool_discovery import generate_discovery


@pytest.mark.asyncio
async def test_mcp_tool_discovery_suite():
    discovery = await generate_discovery()
    assert "service-health" in discovery
    assert "support-ticket" in discovery
    assert "change-management" in discovery
    assert "list_services" in discovery["service-health"]
    assert "search_tickets" in discovery["support-ticket"]
    assert "list_recent_changes" in discovery["change-management"]