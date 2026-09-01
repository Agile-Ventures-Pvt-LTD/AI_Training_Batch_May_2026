import pytest
from unittest.mock import MagicMock
from src.graph import app
from src.state import LogisticsIncidentState

class MockResponse:
    def __init__(self, content):
        self.content = content

class MockLLM:
    def invoke(self, *args, **kwargs):
        return MockResponse("This is a mock response (summary or brief) generated for testing.")
    
    def with_structured_output(self, schema):
        class MockstructuredLLM:
            def invoke(self, *args, **kwargs):
                return schema(
                    shipment_id="SH-4002",
                    cargo_weight_tons=550,
                    cargo_type="industrial electronics",
                    target_warehouse_id="WH-WEST-202",
                    has_perishables=True,
                    maximum_tolerable_delay_hours=72
                )
        return MockstructuredLLM()

def test_graph_retry_selects_next_route(mocker):
    mocker.patch("nodes._get_llm", return_value=MockLLM())
    
    # so mock query_route_inventory_tool returns multiple routes
    # Route 1: WH-WEST-202 (risk elevated -> ROUTE_CLARIFICATION)
    # Route 2: WH-SOUTH-303 (normal -> OPTIMAL_PATH_FOUND)
    mock_routes = [
        {
            "route_id": "ROUTE-WEST-01",
            "alternative_port": "Port-West",
            "warehouse_id": "WH-WEST-202",
            "added_delay_hours": 48
        },
        {
            "route_id": "ROUTE-SOUTH-02",
            "alternative_port": "Port-South",
            "warehouse_id": "WH-SOUTH-303",
            "added_delay_hours": 72
        }
    ]
    mocker.patch("nodes.get_alternative_routes_tool.invoke", return_value=mock_routes)
    
    # WH-WEST-202 has risk_tier = ELEVATED -> rejected
    # WH-SOUTH-303 is active and normal -> accepted
    def mock_warehouse_tool_side_effect(args):
        wh_id = args.get("warehouse_id")
        if wh_id == "WH-WEST-202":
            return {
                "warehouse_name": "Pacific Gateway Storage",
                "current_utilization_pct": 68,
                "operational_status": "ACTIVE",
                "risk_tier": "ELEVATED"
            }
        elif wh_id == "WH-SOUTH-303":
            return {
                "warehouse_name": "Southern Distribution Hub",
                "current_utilization_pct": 72,
                "operational_status": "ACTIVE",
                "risk_tier": "NORMAL"
            }
        return {}
        
    mocker.patch("nodes.query_warehouse_inventory_tool.invoke", side_effect=mock_warehouse_tool_side_effect)
    
    # Mock context okay
    mocker.patch("nodes.get_rag_context", return_value="If a warehouse has an ELEVATED risk tier, another route must be checked.")

    initial_input = {
        "incident_id": "INC-001",
        "manifest_text": "Mock disruption manifest text.",
        "disrupted_port_id": "PORT-SEATTLE-02",
        "extracted_metadata": {},
        "routing_rag_context": "",
        "available_routes": [],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": [],
        "final_report": {},
        "routes_evaluated": [],
        "loops_executed": 0
    }

    final_state = app.invoke(initial_input)
    
    assert final_state["loops_executed"] == 1
    assert final_state["current_route_index"] == 1
    assert final_state["routing_decision"] == "OPTIMAL_PATH_FOUND"
    assert final_state["selected_route"]["route_id"] == "ROUTE-SOUTH-02"
    
    evals = final_state["routes_evaluated"]
    assert len(evals) == 2
    assert evals[0]["route_id"] == "ROUTE-WEST-01"
    assert evals[0]["decision"] == "ROUTE_CLARIFICATION"
    assert evals[1]["route_id"] == "ROUTE-SOUTH-02"
    assert evals[1]["decision"] == "OPTIMAL_PATH_FOUND"

def test_graph_escalates_when_routes_exhausted(mocker):
    """Verify that the graph escalates to CRITICAL_DELAY if all alternative routes are exhausted."""
    mocker.patch("nodes._get_llm", return_value=MockLLM())
    
    # Both routes have elevated risk so the both will be rejected
    mock_routes = [
        {
            "route_id": "ROUTE-WEST-01",
            "alternative_port": "Port-West",
            "warehouse_id": "WH-WEST-202",
            "added_delay_hours": 48
        },
        {
            "route_id": "ROUTE-SOUTH-02",
            "alternative_port": "Port-South",
            "warehouse_id": "WH-WEST-202",
            "added_delay_hours": 72
        }
    ]
    mocker.patch("nodes.get_alternative_routes_tool.invoke", return_value=mock_routes)
    
    mocker.patch("nodes.query_warehouse_inventory_tool.invoke", return_value={
        "warehouse_name": "Pacific Gateway Storage",
        "current_utilization_pct": 68,
        "operational_status": "ACTIVE",
        "risk_tier": "ELEVATED"
    })
    
    mocker.patch("nodes.get_rag_context", return_value="If a warehouse has an ELEVATED risk tier, another route must be checked.")

    initial_input = {
        "incident_id": "INC-001",
        "manifest_text": "Mock disruption manifest text.",
        "disrupted_port_id": "PORT-SEATTLE-02",
        "extracted_metadata": {},
        "routing_rag_context": "",
        "available_routes": [],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": [],
        "final_report": {},
        "routes_evaluated": [],
        "loops_executed": 0
    }

    final_state = app.invoke(initial_input)
    
    assert final_state["routing_decision"] == "CRITICAL_DELAY"
    assert final_state["selected_route"] == {} 
    assert len(final_state["routes_evaluated"]) == 2 
