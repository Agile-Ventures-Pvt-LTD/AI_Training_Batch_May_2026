from graph import LogisticsIncidentState
def test_graph_retry_selects_next_route():
    mock_routes = ["Route_A", "Route_B"]
    state = LogisticsIncidentState(routes=mock_routes)
    state = run_mock_graph_step(state)
    
    assert state.decisions[0] == "ROUTE_CLARIFICATION"
    assert state.current_route_index == 1
    assert state.status == "RUNNING"
    
    state = run_mock_graph_step(state)
    assert len(state.decisions) == 2
    assert state.decisions[1] == "OPTIMAL_PATH_FOUND"