from src.nodes import make_routing_decision
from src.state import LogisticsIncidentState 
from typing import Literal

def test_routing():
    assert make_routing_decision(state=LogisticsIncidentState)


test = test_routing()

if test in  Literal["finalize_route", "escalate_incident", "route_clarification"]:
    assert "True"