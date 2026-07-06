import pytest
from src.nodes import parse_incident, policy_rag_lookup, check_warehouse

@pytest.mark.integration
def test_parse_incident_required_fields():
    # Test LLM (or regex fallback) metadata extraction
    manifest_text = (
        "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle "
        "due to an active worker strike. The vessel is carrying 550 tons of industrial electronics "
        "originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling "
        "components and cannot sustain delays exceeding 72 hours."
    )
    state = {
        "incident_id": "INC-001",
        "manifest_text": manifest_text,
        "logs": []
    }
    result = parse_incident(state)
    meta = result["extracted_metadata"]
    
    assert meta["shipment_id"] == "SH-4002"
    assert meta["cargo_weight_tons"] == 550
    assert "electronics" in meta["cargo_type"].lower()
    assert meta["target_warehouse_id"] == "WH-WEST-202"
    assert meta["has_perishables"] is True
    assert meta["maximum_tolerable_delay_hours"] == 72

def test_policy_rag_lookup():
    # Test RAG query
    state = {
        "manifest_text": "Worker strike disruption",
        "extracted_metadata": {"cargo_type": "industrial electronics"},
        "logs": []
    }
    result = policy_rag_lookup(state)
    assert "routing_rag_context" in result
    assert len(result["routing_rag_context"]) > 0

def test_check_warehouse_node():
    state = {
        "selected_route": {"warehouse_id": "WH-WEST-202"},
        "logs": []
    }
    result = check_warehouse(state)
    assert "warehouse_db_context" in result
    assert result["warehouse_db_context"]["warehouse_name"] == "Pacific Gateway Storage"




### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026