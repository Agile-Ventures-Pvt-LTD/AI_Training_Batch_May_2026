from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.nodes import route_clarification
from src.schemas import ShipmentMetadata

def test_graph_retry_selects_next_route():
    state = {
        "available_routes": [{"route_id": "ROUTE-1"},{"route_id": "ROUTE-2"}],
        "current_route_index": 0,
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "routing_decision": "ROUTE_CLARIFICATION",
    }

    updated_state = route_clarification(state)
    assert updated_state["current_route_index"] == 1
    assert updated_state["clarification_attempts"] == 1
    assert (updated_state["routing_decision"] == "ROUTE_CLARIFICATION")




