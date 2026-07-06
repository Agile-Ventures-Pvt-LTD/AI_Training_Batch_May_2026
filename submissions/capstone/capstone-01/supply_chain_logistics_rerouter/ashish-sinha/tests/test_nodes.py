import pytest
from src.nodes import parse_incident

@pytest.mark.integration
def test_parse_incident_required_fields():
    sample_manifest = "Manifest Data: Shipment SH-9942 heading to WH-WEST-202 with 14.5 tons of Electronics..."
    extracted_output = parse_incident(sample_manifest)
    required_fields = [
        "shipment_id",
        "cargo_weight_tons",
        "cargo_type",
        "target_warehouse_id",
        "has_perishables",
        "maximum_tolerable_delay_hours"
    ]
    for field in required_fields:
        assert field in extracted_output

