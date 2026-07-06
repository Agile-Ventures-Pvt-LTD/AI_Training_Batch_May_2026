import pytest
from src.nodes import parse_incident, policy_rag_lookup, load_alternative_routes, check_warehouse
from src.state import get_initial_state

@pytest.mark.integration
def test_parse_incident_required_fields():
    """Integration test verifying structured metadata extraction from incident manifest text using LLM."""
    manifest_text = (
        "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded "
        "outside the Port of Seattle due to an active worker strike. "
        "The vessel is carrying 550 tons of industrial electronics "
        "originally scheduled for delivery to WH-WEST-202. "
        "The shipment contains perishable cooling components and "
        "cannot sustain delays exceeding 72 hours."
    )
    state = get_initial_state("INC-001", manifest_text, "PORT-SEATTLE-02")
    result = parse_incident(state)
    
    metadata = result["extracted_metadata"]
    assert metadata["shipment_id"] == "SH-4002"
    assert metadata["cargo_weight_tons"] == 550
    assert "electronics" in metadata["cargo_type"].lower()
    assert metadata["target_warehouse_id"] == "WH-WEST-202"
    assert metadata["has_perishables"] is True
    assert metadata["maximum_tolerable_delay_hours"] == 72
    assert len(result["original_incident_summary"]) > 0

def test_policy_rag_lookup():
    """Test policy_rag_lookup node to verify it retrieves relevant rules from knowledge base."""
    manifest_text = "Cargo container carrying 550 tons scheduled for Port-South with delay limits."
    state = get_initial_state("INC-TEST", manifest_text, "PORT-SEATTLE-02")
    
    result = policy_rag_lookup(state)
    
    assert "routing_rag_context" in result
    assert "rag_validation_rules_applied" in result
    assert len(result["rag_validation_rules_applied"]) > 0
    assert any("500 tons" in rule or "utilization" in rule or "delay" in rule or "risk" in rule for rule in result["rag_validation_rules_applied"])

def test_load_alternative_routes():
    """Test load_alternative_routes node retrieves routes correctly."""
    state = get_initial_state("INC-TEST", "manifest text", "PORT-SEATTLE-02")
    result = load_alternative_routes(state)
    
    assert "available_routes" in result
    assert isinstance(result["available_routes"], list)
    assert len(result["available_routes"]) == 3
    assert result["current_route_index"] == 0
    assert result["clarification_attempts"] == 0

def test_check_warehouse_node():
    """Test check_warehouse node retrieves warehouse data correctly."""
    state = get_initial_state("INC-TEST", "manifest text", "PORT-SEATTLE-02")
    state["selected_route"] = {
        "route_id": "ROUTE-WEST-01",
        "warehouse_id": "WH-WEST-202",
        "added_delay_hours": 48
    }
    
    result = check_warehouse(state)
    
    assert "warehouse_db_context" in result
    assert result["warehouse_db_context"]["warehouse_name"] == "Pacific Gateway Storage"
