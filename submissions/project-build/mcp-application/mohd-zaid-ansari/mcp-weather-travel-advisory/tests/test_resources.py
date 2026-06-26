import pytest
from src.resources import travel_checklist_resource, travel_advisory_rules_resource, normalized_forecast_schema_resource

@pytest.mark.asyncio
async def test_required_resources_available():
    """Verify that all 3 custom resources are live and expose their matching data strings."""
    checklist = await travel_checklist_resource()
    rules = await travel_advisory_rules_resource()
    schema = await normalized_forecast_schema_resource()
    
    assert "Travel Readiness Checklist:" in checklist
    assert "Weather Advisory Rules:" in rules
    assert '"destination": "string"' in schema
