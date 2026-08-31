import pytest
from src.tool_discovery import generate_mcp_schema_snapshot

@pytest.mark.asyncio
async def test_mcp_servers_expose_required_tools():
    discovery_map = await generate_mcp_schema_snapshot()
    
    assert "service-health" in discovery_map
    assert "list_services" in discovery_map["service-health"]
    assert "get_service_health" in discovery_map["service-health"]
    assert "get_active_incidents" in discovery_map["service-health"]
    
    assert "support-ticket" in discovery_map
    assert "search_tickets" in discovery_map["support-ticket"]
    assert "get_ticket_details" in discovery_map["support-ticket"]
    assert "get_high_priority_tickets" in discovery_map["support-ticket"]
    
    assert "change-management" in discovery_map
    assert "list_recent_changes" in discovery_map["change-management"]
    assert "get_change_details" in discovery_map["change-management"]
    assert "get_changes_for_service" in discovery_map["change-management"]