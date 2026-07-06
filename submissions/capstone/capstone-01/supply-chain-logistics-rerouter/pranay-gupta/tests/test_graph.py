import pytest
from unittest.mock import MagicMock

from src.schemas import ShipmentMetadata
from src.graph import build_workflow
from src.nodes import configure_dependencies
from src.config import MAX_CLARIFICATION_ATTEMPTS
from tests.conftest import create_mock_llm, create_mock_retriever


def _build_test_app(
    metadata=None,
    brief="Test operations brief.",
    rules_text="Mock logistics rules for testing.",
):
    if metadata is None:
        metadata = ShipmentMetadata(
            shipment_id="SH-4002",
            cargo_weight_tons=550,
            cargo_type="industrial electronics",
            target_warehouse_id="WH-WEST-202",
            has_perishables=True,
            maximum_tolerable_delay_hours=72,
        )

    llm = create_mock_llm(metadata=metadata, brief=brief)
    retriever = create_mock_retriever(rules_text=rules_text)

    app = build_workflow(llm=llm, retriever=retriever)
    return app



def test_graph_optimal_path_found(incident_001):
    metadata = ShipmentMetadata(
        shipment_id="SH-4002",
        cargo_weight_tons=550,
        cargo_type="industrial electronics",
        target_warehouse_id="WH-WEST-202",
        has_perishables=True,
        maximum_tolerable_delay_hours=72,
    )

    app = _build_test_app(metadata=metadata)

    initial_input = {
        "incident_id": incident_001["incident_id"],
        "manifest_text": incident_001["manifest_text"],
        "disrupted_port_id": incident_001["disrupted_port_id"],
    }

    final_state = app.invoke(initial_input)

    assert final_state["routing_decision"] == "OPTIMAL_PATH_FOUND"

    report = final_state.get("final_report", {})
    assert report["graph_routing_metadata"]["final_decision_state"] == "OPTIMAL_PATH_FOUND"

    final_route = report.get("final_selected_route", {})
    assert final_route.get("route_id") == "ROUTE-SOUTH-02"


def test_graph_escalates_when_routes_exhausted(incident_002):
    metadata = ShipmentMetadata(
        shipment_id="SH-4105",
        cargo_weight_tons=250,
        cargo_type="consumer electronics",
        target_warehouse_id="WH-SOUTH-303",
        has_perishables=False,
        maximum_tolerable_delay_hours=48,
    )

    app = _build_test_app(metadata=metadata)

    initial_input = {
        "incident_id": incident_002["incident_id"],
        "manifest_text": incident_002["manifest_text"],
        "disrupted_port_id": incident_002["disrupted_port_id"],
    }

    final_state = app.invoke(initial_input)

    assert final_state["routing_decision"] == "CRITICAL_DELAY"

    routes_evaluated = final_state.get("routes_evaluated", [])
    assert len(routes_evaluated) >= 2

    report = final_state.get("final_report", {})
    assert report["graph_routing_metadata"]["final_decision_state"] == "CRITICAL_DELAY"
    assert report["final_selected_route"] == {}



def test_graph_incident_003_no_max_delay(incident_003):
    metadata = ShipmentMetadata(
        shipment_id="SH-4208",
        cargo_weight_tons=700,
        cargo_type="industrial machinery",
        target_warehouse_id="WH-EAST-101",
        has_perishables=False,
        maximum_tolerable_delay_hours=None,
    )

    app = _build_test_app(metadata=metadata)

    initial_input = {
        "incident_id": incident_003["incident_id"],
        "manifest_text": incident_003["manifest_text"],
        "disrupted_port_id": incident_003["disrupted_port_id"],
    }

    final_state = app.invoke(initial_input)

    routes_evaluated = final_state.get("routes_evaluated", [])
    assert len(routes_evaluated) >= 1

    report = final_state.get("final_report", {})
    assert report["parsed_metadata"]["maximum_tolerable_delay_hours"] is None
