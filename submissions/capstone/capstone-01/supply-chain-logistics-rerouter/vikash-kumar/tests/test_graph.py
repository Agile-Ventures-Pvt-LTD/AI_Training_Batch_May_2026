import pytest
from src.graph import app

def test_graph_retry_selects_next_route():
    initial_state = {"incident_id": "TST-001",
        "manifest_text": "Disruption text manifest configuration context payload string.",
        "disrupted_port_id": "PORT-SEATTLE-02",
        "extracted_metadata": {"maximum_tolerable_delay_hours": 50},
        "routing_rag_context": "Mock RAG rules verification context data.",
        "available_routes": [{"route_id": "ROUTE-WEST-01", "alternative_port": "Port-West", "warehouse_id": "WH-WEST-202", "added_delay_hours": 48},{"route_id": "ROUTE-SOUTH-02", "alternative_port": "Port-South", "warehouse_id": "WH-SOUTH-303", "added_delay_hours": 72}],
        "current_route_index": 0,
        "selected_route": None,
        "warehouse_db_context": None,
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": [],
        "final_report": None
    }
    config = {"configurable": {"thread_id": "test-thread"}}
    events = app.stream(initial_state, config, stream_mode="values")
    final_state = list(events)[-1]
    assert final_state["clarification_attempts"] > 0
    assert final_state["current_route_index"] > 0
