import pytest
from src.nodes import parse_incident, load_alternative_routes, select_route, check_warehouse

@pytest.mark.integration
def test_parse_incident_required_fields():
    mock_state = {"manifest_text": "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle due to an active worker strike. The vessel is carrying 550 tons of industrial electronics originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling components and cannot sustain delays exceeding 72 hours.","logs": [] }
    result = parse_incident(mock_state)
    metadata = result["extracted_metadata"]
    assert "shipment_id" in metadata
    assert "cargo_weight_tons" in metadata
    assert "cargo_type" in metadata
    assert "target_warehouse_id" in metadata
    assert "has_perishables" in metadata
    assert "maximum_tolerable_delay_hours" in metadata

def test_load_alternative_routes_initialization():
    mock_state = {"disrupted_port_id": "PORT-SEATTLE-02","logs": []}
    result = load_alternative_routes(mock_state)
    assert "available_routes" in result
    assert result["current_route_index"] == 0
    assert result["clarification_attempts"] == 0
    assert result["max_clarification_attempts"] == 2

def test_select_route_valid_index():
    mock_state = {"current_route_index": 0,"available_routes": [{"route_id": "ROUTE-WEST-01"}],"logs": []}
    result = select_route(mock_state)
    assert result["selected_route"] == {"route_id": "ROUTE-WEST-01"}
