
from langgraph.graph import START,StateGraph,END
from state import LogisticsIncidentState
from nodes import parse_incident,policy_rag_lookup,load_alternative_routes,select_route, check_warehouse,analyze_route,route_clarification,finalize_route,escalate_incident,generate_report,decision_routing


# Define the workflow graph
graph = StateGraph(LogisticsIncidentState)

#adding all nodes
graph.add_node("parse_incident",parse_incident)
graph.add_node("policy_rag_lookup",policy_rag_lookup)
graph.add_node("load_alternative_routes",load_alternative_routes)
graph.add_node("select_route",select_route)
graph.add_node("check_warehouse",check_warehouse)
graph.add_node("analyze_route",analyze_route)
graph.add_node("route_clarification",route_clarification)
graph.add_node("finalize_route",finalize_route)
graph.add_node("escalate_incident",escalate_incident)
graph.add_node("generate_report",generate_report)
graph.add_node("decision_routing",decision_routing)

#adding all edges
graph.add_edge(START, "parse_incident")
graph.add_edge("parse_incident","policy_rag_lookup")
graph.add_edge("policy_rag_lookup","load_alternative_routes")
graph.add_edge("load_alternative_routes","select_route")
graph.add_edge("select_route","check_warehouse")
graph.add_edge("check_warehouse","analyze_route")
graph.add_conditional_edges("analyze_route","decision_routing",{
    "OPTIMAL_PATH_FOUND":"finalize_route",
    "ROUTE_CLARIFICATION":"route_clarification",
    "CRITICAL_DELAY":"escalate_incident"
})
graph.add_edge("route_clarification","select_route")
graph.add_edge("finalize_route","generate_report")
graph.add_edge("escalate_incident","generate_report")
graph.add_edge("generate_report",END)

compiled_workflow = graph.compile()


def run_custom_agent(query):
    query=query
    if query==1:
        data={
            "incident_id": "INC-001",
            "manifest_text": "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle due to an active worker strike. The vessel is carrying 550 tons of industrial electronics originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling components and cannot sustain delays exceeding 72 hours.""",
            "disrupted_port_id": "PORT-SEATTLE-02"
        }
    if query==2:
        data={
            "incident_id": "INC-002",
            "manifest_text": "Shipment SH-4105 is delayed because the primary port is temporarily closed. The shipment contains 250 tons of consumer electronics and is scheduled for WH-SOUTH-303.",
            "disrupted_port_id": "PORT-SEATTLE-02"
        }
    if query==3:
        data={
            "incident_id": "INC-003",
            "manifest_text": "Cargo SH-4208 contains 700 tons of industrial machinery.The primary maritime route is unavailable and delivery was planned for WHEAST-101.",
            "disrupted_port_id": "PORT-SEATTLE-02"
        }
    
    initial_state={
        
        "incident_id":data.get("incident_id"),
        "manifest_text":data.get("manifest_text"),
        "disrupted_port_id":data.get("disrupted_port_id")
    }
    result = compiled_workflow.invoke(initial_state)
    return {
        "final response": result["final_report"]
    }

