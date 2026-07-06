import unittest
from unittest.mock import patch
from src.graph import (
    load_warehouse_context,
    load_available_routes,
    evaluate_routes,
    choose_best_route,
    build_final_report,
    run_graph,
)
from src.state import LogisticsIncidentState
def make_state() -> LogisticsIncidentState:
    return {
        "incident_id": "INC-TEST",
        "manifest_text": "test manifest",
        "disrupted_port_id": "PORT-XYZ",
        "extracted_metadata": {"warehouse_id": "WH-TEST-1"},
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
        "evaluated_routes": [],
        "final_report": {},
    }


# -------------------------------------------------------
# Test Suite
# -------------------------------------------------------
class TestGraphPipeline(unittest.TestCase):

    @patch("src.graph.query_warehouse_inventory_tool")
    def test_load_warehouse_context(self, mock_query):
        mock_query.return_value = {"id": "WH-TEST-1", "capacity": "OK"}

        state = make_state()
        updated = load_warehouse_context(state)

        self.assertIn("warehouse_db_context", updated)
        self.assertEqual(updated["warehouse_db_context"]["id"], "WH-TEST-1")
        self.assertIn("Loaded warehouse context", updated["logs"][0])

    @patch("src.graph.get_alternative_routes_tool")
    def test_load_available_routes(self, mock_routes):
        mock_routes.return_value = [
            {"route_id": "R1", "eta_days": 5},
            {"route_id": "R2", "eta_days": 3},
        ]

        state = make_state()
        updated = load_available_routes(state)

        self.assertEqual(len(updated["available_routes"]), 2)
        self.assertEqual(updated["available_routes"][0]["route_id"], "R1")

    def test_evaluate_routes_scoring(self):
        state = make_state()
        state["available_routes"] = [
            {"route_id": "R1", "eta_days": 10},
            {"route_id": "R2", "eta_days": 2},
        ]

        updated = evaluate_routes(state)

        # Best score should be route R2 (lower ETA)
        best = updated["evaluated_routes"][0]
        self.assertEqual(best["route"]["route_id"], "R2")
        self.assertGreater(best["score"], updated["evaluated_routes"][1]["score"])

    def test_choose_best_route(self):
        state = make_state()
        state["evaluated_routes"] = [
            {"route": {"route_id": "BEST"}, "score": 95},
            {"route": {"route_id": "OTHER"}, "score": 80},
        ]

        updated = choose_best_route(state)

        self.assertEqual(updated["selected_route"]["route_id"], "BEST")
        self.assertEqual(updated["routing_decision"], "route_selected")

    def test_build_final_report(self):
        state = make_state()
        state["selected_route"] = {"route_id": "BEST"}
        state["warehouse_db_context"] = {"id": "WH-TEST"}
        state["evaluated_routes"] = [1, 2]
        state["logs"].append("Step executed.")

        updated = build_final_report(state)

        report = updated["final_report"]
        self.assertEqual(report["incident_id"], "INC-TEST")
        self.assertEqual(report["selected_route"]["route_id"], "BEST")
        self.assertEqual(report["total_routes_analyzed"], 2)

    @patch("src.graph.query_warehouse_inventory_tool")
    @patch("src.graph.get_alternative_routes_tool")
    def test_run_graph_end_to_end(self, mock_routes, mock_query):
        mock_query.return_value = {"id": "WH-TEST-1", "status": "OK"}

        mock_routes.return_value = [
            {"route_id": "R1", "eta_days": 4},
            {"route_id": "R2", "eta_days": 6},
        ]

        state = make_state()
        result = run_graph(state)

        self.assertIn("final_report", result)
        self.assertTrue(result["final_report"])
        self.assertIn("decision", result["final_report"])
        self.assertEqual(result["final_report"]["selected_route"]["route_id"], "R1")


if __name__ == "__main__":
    unittest.main()