import json
import pytest
from unittest.mock import AsyncMock, Mock

from src.nodes import (
    parse_incident,
    policy_rag_lookup,
    load_alternative_routes,
    select_route,
    check_warehouse,
    evaluate,
    analyze_route,
    route_clarification,
    finalize_route,
    escalate_incident,
    generate_report,
)

@pytest.fixture
def base_state():
    return {
        "incident_id": "INC-001",
        "manifest_text": "Shipment SH-4002, 550 tons, industrial electronics, target WH-WEST-202, perishables: true, max delay 72h",
        "disrupted_port_id": "PORT-01",
        "extracted_metadata": {
            "shipment_id": "SH-4002",
            "cargo_weight_tons": 550,
            "cargo_type": "industrial electronics",
            "target_warehouse_id": "WH-WEST-202",
            "has_perishables": True,
            "maximum_tolerable_delay_hours": 72,
        },
        "routing_rag_context": "",
        "available_routes": [],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 0,
        "logs": [],
        "final_report": {},
    }

def test_parse_incident(monkeypatch):
    fake_llm = Mock()
    fake_llm.invoke.return_value = Mock(content=json.dumps({
        "shipment_id": "SH-4002",
        "cargo_weight_tons": 550,
        "cargo_type": "industrial electronics",
        "target_warehouse_id": "WH-WEST-202",
        "has_perishables": True,
    }))
    monkeypatch.setattr("src.node.get_llm", lambda: fake_llm)
    state = {
        "manifest_text": "dummy manifest",
    }
    result = parse_incident(state)
    assert result["extracted_metadata"]["shipment_id"] == "SH-4002"

def test_policy_rag_lookup(monkeypatch):
    monkeypatch.setattr("src.node.retrieve_rules", lambda q: "Rule text")
    state = {"disrupted_port_id": "PORT-01"}
    result = policy_rag_lookup(state)
    assert result["routing_rag_context"] == "Rule text"

def test_load_alternative_routes(monkeypatch):
    routes = [{"route_id": "R1"}, {"route_id": "R2"}]
    monkeypatch.setattr("src.node.get_alternative_routes_tool", lambda _: routes)
    state = {"disrupted_port_id": "PORT-01"}
    result = load_alternative_routes(state)
    assert result["available_routes"] == routes
    assert result["current_route_index"] == 0
    assert result["max_clarification_attempts"] == 2

def test_select_route():
    state = {
        "available_routes": [{"route_id": "R1"}, {"route_id": "R2"}],
        "current_route_index": 1,
    }
    result = select_route(state)
    assert result["selected_route"]["route_id"] == "R2"

def test_select_route_out_of_bounds():
    state = {
        "available_routes": [{"route_id": "R1"}],
        "current_route_index": 5,
    }
    result = select_route(state)
    assert result["selected_route"] == {}

def test_check_warehouse(monkeypatch):
    wh = {"utilization_percent": 70}
    monkeypatch.setattr("src.node.query_warehouse_inventory_tool", lambda _: wh)
    state = {"extracted_metadata": {"target_warehouse_id": "WH-001"}}
    result = check_warehouse(state)
    assert result["warehouse_db_context"] == wh

def test_evaluate_optimal():
    state = {
        "warehouse_db_context": {"utilization_percent": 50, "operational_status": "ACTIVE", "risk_tier": "LOW"},
        "extracted_metadata": {"maximum_tolerable_delay_hours": 100},
        "selected_route": {"added_delay_hours": 20},
    }
    decision, score, reasons = evaluate(state)
    assert decision == "OPTIMAL_PATH_FOUND"
    assert score == 0
    assert reasons == []

def test_evaluate_clarification():
    state = {
        "warehouse_db_context": {"utilization_percent": 90, "operational_status": "ACTIVE", "risk_tier": "LOW"},
        "extracted_metadata": {"maximum_tolerable_delay_hours": 100},
        "selected_route": {"added_delay_hours": 20},
    }
    decision, score, reasons = evaluate(state)
    assert decision == "ROUTE_CLARIFICATION"
    assert score == 30
    assert "warehouse utilization > 85%" in reasons[0]

def test_analyze_route():
    state = {
        "warehouse_db_context": {"utilization_percent": 90, "operational_status": "ACTIVE", "risk_tier": "LOW"},
        "extracted_metadata": {"maximum_tolerable_delay_hours": 100},
        "selected_route": {"route_id": "R1", "added_delay_hours": 20},
        "logs": [],
    }
    result = analyze_route(state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 30
    assert "R1" in result["logs"][0]

def test_route_clarification_increment():
    state = {
        "routing_decision": "ROUTE_CLARIFICATION",
        "clarification_attempts": 0,
        "current_route_index": 0,
        "max_clarification_attempts": 3,
    }
    result = route_clarification(state)
    assert result["clarification_attempts"] == 1
    assert result["current_route_index"] == 1
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"

def test_route_clarification_exhausted():
    state = {
        "routing_decision": "ROUTE_CLARIFICATION",
        "clarification_attempts": 2,
        "current_route_index": 2,
        "max_clarification_attempts": 3,
    }
    result = route_clarification(state)
    assert result["routing_decision"] == "CRITICAL_DELAY"

def test_finalize_route_returns_state():
    state = {"foo": "bar"}
    assert finalize_route(state) is state

def test_escalate_incident_triggers():
    state = {
        "routing_decision": "ROUTE_CLARIFICATION",
        "clarification_attempts": 3,
        "max_clarification_attempts": 3,
        "logs": [],
    }
    result = escalate_incident(state)
    assert result["routing_decision"] == "CRITICAL_DELAY"
    assert "Escalation triggered" in result["logs"][0]

def test_generate_report(monkeypatch):
    fake_llm = AsyncMock()
    fake_llm.ainvoke.return_value = Mock(content="Brief summary")
    monkeypatch.setattr("src.node.get_llm", lambda: fake_llm)
    write_mock = Mock()
    monkeypatch.setattr("src.node.write_report", write_mock)
    state = {
        "incident_id": "INC-001",
        "manifest_text": "manifest",
        "extracted_metadata": {"shipment_id": "S1"},
        "routing_rag_context": "rule1\nrule2",
        "available_routes": [{"route_id": "R1"}],
        "selected_route": {"route_id": "R1"},
        "warehouse_db_context": {"utilization_percent": 70},
        "clarification_attempts": 0,
        "routing_decision": "OPTIMAL_PATH_FOUND",
        "reroute_impact_score": 0,
    }
    result = generate_report(state)
    assert result["final_report"]["incident_id"] == "INC-001"
    write_mock.assert_called_once()