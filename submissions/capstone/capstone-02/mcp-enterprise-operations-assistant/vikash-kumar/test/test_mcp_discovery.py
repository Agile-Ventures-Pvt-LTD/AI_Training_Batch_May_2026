import pytest
import src.tool_discovery as discovery

@pytest.mark.asyncio
async def test_export_tool_manifest_keys():
    result = getattr(discovery, "export_tool_manifest", getattr(discovery, "export_manifest", None))
    assert result is not None
    
    manifest = await result()
    assert "service-health" in manifest or "service_health_server" in manifest
    assert "support-ticket" in manifest or "support_ticket_server" in manifest
    assert "change-management" in manifest or "change_management_server" in manifest

@pytest.mark.asyncio
async def test_export_tool_manifest_contents():
    result = getattr(discovery, "export_tool_manifest", getattr(discovery, "export_manifest", None))
    manifest = await result()
    
    health_key = "service-health" if "service-health" in manifest else "service_health_server"
    ticket_key = "support-ticket" if "support-ticket" in manifest else "support_ticket_server"
    change_key = "change-management" if "change-management" in manifest else "change_management_server"
    
    assert any(t in manifest[health_key] for t in ["list_services", "check_service_metrics"])
    assert any(t in manifest[ticket_key] for t in ["search_tickets", "fetch_high_impact_incidents"])
    assert any(t in manifest[change_key] for t in ["list_recent_changes", "get_recent_deployments"])
