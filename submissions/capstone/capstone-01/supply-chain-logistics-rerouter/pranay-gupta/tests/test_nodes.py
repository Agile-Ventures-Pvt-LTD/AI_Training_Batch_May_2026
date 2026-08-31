import pytest
from unittest.mock import MagicMock

from src.schemas import ShipmentMetadata
from src.nodes import (parse_incident,load_alternative_routes,select_route,check_warehouse,analyze_route,route_clarification,finalize_route,
                        escalate_incident,configure_dependencies,)
from tests.conftest import create_mock_llm, create_mock_retriever


@pytest.fixture
def configured_nodes():
    metadata = ShipmentMetadata(
        shipment_id="SH-4002",
        cargo_weight_tons=550,
        cargo_type="industrial electronics",
        target_warehouse_id="WH-WEST-202",
        has_perishables=True,
        maximum_tolerable_delay_hours=72,
    )
    llm = create_mock_llm(metadata=metadata)
    retriever = create_mock_retriever()
    configure_dependencies(llm=llm, retriever=retriever)
    yield llm, retriever
    configure_dependencies(llm=None, retriever=None)


@pytest.mark.integration
def test_parse_incident_required_fields(incident_001):
    from src.config import GROQ_API_KEY

    if not GROQ_API_KEY:
        pytest.skip("GROQ_API_KEY not set, skipping integration test")

    from src.nodes import configure_dependencies
    configure_dependencies(llm=None, retriever=None)

    state = {
        "incident_id": incident_001["incident_id"],
        "manifest_text": incident_001["manifest_text"],
        "disrupted_port_id": incident_001["disrupted_port_id"],
    }

    result = parse_incident(state)
    metadata = result["extracted_metadata"]

    assert "shipment_id" in metadata
    assert metadata["shipment_id"] == "SH-4002"
    assert "cargo_weight_tons" in metadata
    assert metadata["cargo_weight_tons"] == 550
    assert "cargo_type" in metadata
    assert "target_warehouse_id" in metadata
    assert metadata["target_warehouse_id"] == "WH-WEST-202"
    assert "has_perishables" in metadata
    assert metadata["has_perishables"] is True
    assert "maximum_tolerable_delay_hours" in metadata
    assert metadata["maximum_tolerable_delay_hours"] == 72


def test_load_alternative_routes(incident_001):
    state = {
        "disrupted_port_id": incident_001["disrupted_port_id"],
    }

    result = load_alternative_routes(state)

    assert isinstance(result["available_routes"], list)
    assert len(result["available_routes"]) >= 1
    assert result["current_route_index"] == 0
    assert result["clarification_attempts"] == 0
    assert result["max_clarification_attempts"] == 2
    assert result["routes_evaluated"] == []



def test_select_route_second_index(seattle_routes):
    state = {
        "available_routes": seattle_routes,
        "current_route_index": 1,
    }

    result = select_route(state)

    assert result["selected_route"]["route_id"] == "ROUTE-SOUTH-02"


def test_select_route_out_of_bounds(seattle_routes):
    state = {
        "available_routes": seattle_routes,
        "current_route_index": 99,
    }

    result = select_route(state)

    assert result["selected_route"] == {}
    assert result["routing_decision"] == "CRITICAL_DELAY"



def test_check_warehouse_empty_route():
    state = {
        "selected_route": {},
    }

    result = check_warehouse(state)

    assert "error" in result["warehouse_db_context"]

