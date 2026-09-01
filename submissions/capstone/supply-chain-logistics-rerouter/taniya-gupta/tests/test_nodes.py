import pytest
import os
from src.nodes import parse_incident

@pytest.mark.integration
def test_parse_incident_required_fields():
    """Test 4: Metadata extraction using LLM structured output."""

    manifest = (
        "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle "
        "due to an active worker strike. The vessel is carrying 550 tons of industrial electronics "
        "originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling "
        "components and cannot sustain delays exceeding 72 hours."
    )
    state = {
        "incident_id": "INC-001",
        "manifest_text": manifest,
        "disrupted_port_id": "PORT-SEATTLE-02",
        "extracted_metadata": {},
        "logs": []
    }
    
    res = parse_incident(state)
    metadata = res.get("extracted_metadata", {})
    
    assert "shipment_id" in metadata
    assert "cargo_weight_tons" in metadata
    assert "cargo_type" in metadata
    assert "target_warehouse_id" in metadata
    assert "has_perishables" in metadata
    assert "maximum_tolerable_delay_hours" in metadata
    
    assert metadata["shipment_id"] == "SH-4002"
    assert metadata["cargo_weight_tons"] == 550
    assert "electronics" in metadata["cargo_type"].lower()
    assert metadata["target_warehouse_id"] == "WH-WEST-202"
    assert metadata["has_perishables"] is True
    assert metadata["maximum_tolerable_delay_hours"] == 72

def test_final_report_schema():
    """Verify that generate_report creates a report with the correct schema."""
   