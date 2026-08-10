from __future__ import annotations

import asyncio
import sys
from typing import Any, Dict

import pytest

ROOT = str((__import__("pathlib").Path(__file__).parents[1]).resolve())
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.graph import build_incident_graph  # noqa: E402


def base_state() -> Dict[str, Any]:
    return {
        "incident_id": "TEST-INC-001",
        "manifest_text": "dummy manifest",
        "disrupted_port_id": "PORT‑A",
        "extracted_metadata": {},
        "routing_rag_context": "",
        "available_routes": [{"route_id": "R1"}, {"route_id": "R2"}],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",          
        "clarification_attempts": 0,
        "max_clarification_attempts": 3,
        "logs": [],
        "final_report": {},
    }


def _stub_parse_incident(state: Dict[str, Any]) -> Dict[str, Any]:
    state["extracted_metadata"] = {"shipment_id": "SH‑0001"}
    state["logs"].append("parse_incident")
    return state


def _stub_policy_rag_lookup(state: Dict[str, Any]) -> Dict[str, Any]:
    state["routing_rag_context"] = "policy text"
    state["logs"].append("policy_rag_lookup")
    return state


def _stub_load_alternative_routes(state: Dict[str, Any]) -> Dict[str, Any]:
    state["available_routes"] = [
        {"route_id": "R1", "added_delay_hours": 30},
        {"route_id": "R2", "added_delay_hours": 150},
    ]
    state["current_route_index"] = 0
    state["logs"].append("load_alternative_routes")
    return state


def _stub_select_route(state: Dict[str, Any]) -> Dict[str, Any]:
    idx = state["current_route_index"]
    state["selected_route"] = state["available_routes"][idx]
    state["logs"].append(f"select_route:{state['selected_route']['route_id']}")
    return state


def _stub_check_warehouse(state: Dict[str, Any]) -> Dict[str, Any]:
    state["warehouse_db_context"] = {
        "warehouse_utilization": 70,
        "operational_status": "ACTIVE",
        "risk_tier": "NORMAL",
    }
    state["logs"].append("check_warehouse")
    return state


def _stub_analyze_route_optimal(state: Dict[str, Any]) -> Dict[str, Any]:
    state["routing_decision"] = "OPTIMAL_PATH_FOUND"
    state["reroute_impact_score"] = 0
    state["logs"].append("analyze_route:OPTIMAL")
    return state


def _stub_analyze_route_clarify(state: Dict[str, Any]) -> Dict[str, Any]:
    if state.get("_analyze_called", 0) == 0:
        state["routing_decision"] = "ROUTE_CLARIFICATION"
        state["logs"].append("analyze_route:CLARIFY")
    else:
        state["routing_decision"] = "OPTIMAL_PATH_FOUND"
        state["logs"].append("analyze_route:OPTIMAL")
    state["_analyze_called"] = state.get("_analyze_called", 0) + 1
    return state


def _stub_analyze_route_critical(state: Dict[str, Any]) -> Dict[str, Any]:
    state["routing_decision"] = "CRITICAL_DELAY"
    state["reroute_impact_score"] = 100
    state["logs"].append("analyze_route:CRITICAL")
    return state


def _stub_route_clarification(state: Dict[str, Any]) -> Dict[str, Any]:
    state["clarification_attempts"] += 1
    state["current_route_index"] += 1
    state["logs"].append(
        f"route_clarification:attempt{state['clarification_attempts']}"
    )
    return state


def _stub_finalize_route(state: Dict[str, Any]) -> Dict[str, Any]:
    state["logs"].append("finalize_route")
    return state


def _stub_escalate_incident(state: Dict[str, Any]) -> Dict[str, Any]:
    state["logs"].append("escalate_incident")
    return state


def _stub_generate_report(state: Dict[str, Any]) -> Dict[str, Any]:
    state["final_report"] = {"generated": True}
    state["logs"].append("generate_report")
    return state


@pytest.fixture
def compiled_graph(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "src.nodes.parse_incident", _stub_parse_incident, raising=False
    )
    monkeypatch.setattr(
        "src.nodes.policy_rag_lookup", _stub_policy_rag_lookup, raising=False
    )
    monkeypatch.setattr(
        "src.nodes.load_alternative_routes",
        _stub_load_alternative_routes,
        raising=False,
    )
    monkeypatch.setattr("src.nodes.select_route", _stub_select_route, raising=False)
    monkeypatch.setattr(
        "src.nodes.check_warehouse", _stub_check_warehouse, raising=False
    )
    monkeypatch.setattr(
        "src.nodes.analyze_route", _stub_analyze_route_optimal, raising=False
    )
    monkeypatch.setattr(
        "src.nodes.route_clarification", _stub_route_clarification, raising=False
    )
    monkeypatch.setattr(
        "src.nodes.finalize_route", _stub_finalize_route, raising=False
    )
    monkeypatch.setattr(
        "src.nodes.escalate_incident", _stub_escalate_incident, raising=False
    )
    monkeypatch.setattr(
        "src.nodes.generate_report", _stub_generate_report, raising=False
    )

    graph = build_incident_graph()
    return graph.compile()


async def _run_graph(compiled, init_state: dict) -> dict:
    return await compiled.ainvoke(init_state)


def test_optimal_path_flow(compiled_graph):
   
    init = base_state()
    final_state = asyncio.run(_run_graph(compiled_graph, init))

    assert final_state["routing_decision"] == "OPTIMAL_PATH_FOUND"

    expected_log_sequence = [
        "parse_incident",
        "policy_rag_lookup",
        "load_alternative_routes",
        "select_route:R1",
        "check_warehouse",
        "analyze_route:OPTIMAL",
        "finalize_route",
        "generate_report",
    ]
    assert final_state["logs"][: len(expected_log_sequence)] == expected_log_sequence

    assert final_state["final_report"] == {"generated": True}


def test_route_clarification_loop(monkeypatch, compiled_graph):
   
    monkeypatch.setattr(
        "src.nodes.analyze_route",
        _stub_analyze_route_clarify,
        raising=False,
    )

    init = base_state()
    final_state = asyncio.run(_run_graph(compiled_graph, init))

    assert final_state["routing_decision"] == "OPTIMAL_PATH_FOUND"

    expected = [
        "parse_incident",
        "policy_rag_lookup",
        "load_alternative_routes",
        "select_route:R1",
        "check_warehouse",
        "analyze_route:CLARIFY",
        "route_clarification:attempt1",
        "select_route:R2",
        "check_warehouse",
        "analyze_route:OPTIMAL",
        "finalize_route",
        "generate_report",
    ]
    assert final_state["logs"] == expected

    assert final_state["selected_route"]["route_id"] == "R2"


def test_critical_delay_escalation(monkeypatch, compiled_graph):
    
    monkeypatch.setattr(
        "src.nodes.analyze_route",
        _stub_analyze_route_critical,
        raising=False,
    )

    init = base_state()
    final_state = asyncio.run(_run_graph(compiled_graph, init))

    assert final_state["routing_decision"] == "CRITICAL_DELAY"

    expected = [
        "parse_incident",
        "policy_rag_lookup",
        "load_alternative_routes",
        "select_route:R1",
        "check_warehouse",
        "analyze_route:CRITICAL",
        "escalate_incident",
        "generate_report"
    ]
    assert final_state["logs"] == expected

    assert final_state["selected_route"]["route_id"] == "R2"