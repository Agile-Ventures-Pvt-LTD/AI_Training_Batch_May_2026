import json
from report_writer import report_writers
from state import LogisticsIncidentState
from config import call_llm
from tools import query_warehouse_inventory_tool
from prompts import parce_incident_prompt, select_route_prompt, incident_summary, final_operational_breif_prompt
from rag import retriever
from langchain_core.documents import Document
from typing import Literal

def parse_incident(incident_id: dict) -> LogisticsIncidentState:
    """
    This will parse the incident_status give the required metadata

    Args:
        incident_id: The incident id which will used to fetch the manifest text from the incidents
        
    Returns:
        LogisticsIncidentState: Updating the incident_id, manifest_text and extracted_metadata
    """
    
    INCIDENT_PATH = "./data/sample_incidents.json"

    try: 
        with open(INCIDENT_PATH, "r") as f:
            data = json.load(f)

    except Exception as e:
        print(f"Error loading the smaple incidents file : {e}")

    
    ids = []
    for i in range(0, len(data)):
        ids.append(data[i]["incident_id"])

    idx = 0
    for i in range(0, len(ids)):
        if ids[i] == incident_id:
            idx = i

    manifest_text = data[idx]["manifest_text"]
    disrupted_port_id = data[idx]["disrupted_port_id"]

    prompt = [
        {"role" : "system", "content" : parce_incident_prompt.format(manifest_text=manifest_text)}
    ]

    response = call_llm(prompt=prompt)

    extracted_metadata = json.loads(response)

    print("--parsing--")

    return {
        "incident_id" : incident_id["incident_id"],
        "manifest_text": manifest_text,
        "disrupted_port_id": disrupted_port_id,
        "extracted_metadata": extracted_metadata
    }


def policy_rag_lookup(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    This is used to retreive the logistics rules for the current incidents.

    Args: 
        state (manifest_text): The incident manifest text to retrieve the context of it.

    Returns: 
        LogisticsIncidentState: Updating the routing_rag_context in the state
    """

    manifest_text = state["manifest_text"]

    routing_rag_context = retriever.invoke(manifest_text)

    print("--rag--")

    return {
        "routing_rag_context" : routing_rag_context
    }


def load_alternative_routes(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    To load the alternatives routes for the disrupted routes

    Returns:
        LogisticsIncidentState: It will return the list of available routes.
    """

    ROUTE_OPTIONS_PATH = "./data/route_options.json"

    try:
        with open(ROUTE_OPTIONS_PATH, "r") as f:
            data = json.load(f)

    except Exception as e:
        print(f"Error loading the route options files : {e}")

    available_routes = data["PORT-SEATTLE-02"]

    print("--alternative--")

    return {
        "available_routes" : available_routes,
        "current_route_index" : 0,
        "clarification_attempts": 0,
    }


def select_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Select the Route from the available_routes

    Args: 
        state (available_routes): The list of available routes
        state (current_route_index): Maintain the routing index

    Returns:
        LogisticsIncidentState: Updating the selected_route and current_route_index
    """

    available_routes = state["available_routes"]

    prompt = [
        {"role" : "system", "content" : select_route_prompt.format(available_routes=available_routes)}
    ]

    response = call_llm(prompt=prompt)

    selected_route = json.loads(response)

    print("--select route--")

    return {
        "selected_route" : selected_route,
        "current_route_index" : state["current_route_index"] + 1
    }


def check_warehouse(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Fetch the warehouse data using the warehouse id

    Args:
        state (selected_route): Used to fetch the warehouse id

    Returns:
        LogisticsIncidentState: Update the warehouse_db_context
    """

    select_route = state["selected_route"]

    warehouse_id = select_route["warehouse_id"]

    print("--warehouse--")

    return {
        "warehouse_db_context" : query_warehouse_inventory_tool(warehouse_id)
    }


def analyze_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Analyze and Evaluate the selected route

    Args:
        state (warehouse_db_context): To get the warehouse information
        state (selected_route): To fetch the information about the selected route
        state (extracted_metadata): To get the value of maximum_tolerable_delay_hours
    
    Returns:
        LogisticsIncidentState: Updating the reroute_impact_score and routing_decision fileds in stats
    """

    reroute_impact_score = 0
    routing_decision = "finalize_route"

    warehouse = state["warehouse_db_context"]
    select_route = state["selected_route"]
    shippment = state["extracted_metadata"]

    warehouse_utilisation = warehouse["current_utilization_pct"]
    warehouse_risk_tier = warehouse["risk_tier"]
    warehouse_status = warehouse["operational_status"]
    added_delay = select_route["added_delay_hours"]
    shippment_delay = shippment["maximum_tolerable_delay_hours"]

    if warehouse_utilisation > 85:
        reroute_impact_score = reroute_impact_score + 30
        routing_decision = "route_clarification"

    if warehouse_risk_tier == "ELEVATED":
        reroute_impact_score = reroute_impact_score + 25
        routing_decision = "route_clarification"

    if warehouse_status != "ACTIVE":
        reroute_impact_score = reroute_impact_score + 30
        routing_decision = "route_clarification"

    if added_delay > int(shippment_delay):
        reroute_impact_score = reroute_impact_score + 25
        routing_decision = "route_clarification"

    if added_delay > 120:
        reroute_impact_score = reroute_impact_score + 50 
        routing_decision = "escalate_incident"

    print(routing_decision)
    print("--analyze--")

    return {
        "reroute_impact_score" : reroute_impact_score,
        "routing_decision" : routing_decision,
        "max_clarification_attempts": 2
    }


def route_clarification(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Make the route clarification should move on with this route or not.

    Args:
        state (clarification_attempts, clarification_attempts): Counter which will make sure that it will not end up in the infinite loop.

    Returns:
        LogisticsIncidentState: Maintaing the counter to exit the loop
    """
    
    cnt = state["clarification_attempts"] + 1

    print(cnt)
    print("--clarification--")

    return {
        "current_route_index" : state["current_route_index"] + 1,
        "clarification_attempts": cnt
    }


def finalize_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    To enter final route node

    Returns:
        routing_decision: Update the routing_decision
    """
    
    print("--final--")

    return {
        "routing_decision": "finalize_route"
    }


def escalate_incident(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    To Enter the the critical delay node

    Returns:
        routing_decision: Update the routing_decision to critical_delay"
    """

    print("--escalate--")

    return {
        "routing_decision": "escalate_incident"
    }


def make_routing_decision(state: LogisticsIncidentState) -> Literal["finalize_route", "escalate_incident", "route_clarification"]:
    """
    This is the conditional router which redirect to the 
    finalize_route, critical_delay and route_clarification

    Args: 
        state (routing_decision): Return the route for the next node

    Returns:
        literal: The literal for the next route
    """

    route = state["routing_decision"]

    if state["clarification_attempts"] >= state["max_clarification_attempts"]:
        route = "escalate_incident"
    

    print(route)
    print("--decision--")

    return route


def serialize_for_json(obj):
    if isinstance(obj, Document):
        return {
            "page_content": obj.page_content,
            "metadata": obj.metadata
        }
    
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    else:
        return obj

def generate_report(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """
    Generate the final report inside the outputs folder 

    Args: 
        state: Using the state to generate the final JSON response

    Returns: 
        LogisticsIncidentState: Updating the final_report state
    """

    summary = call_llm(
        prompt=[
            {"role" : "system", "content" : incident_summary.format(manifest_text=state["manifest_text"])}
        ],
        type={"type" : "text"}
    )

    final_operational_brief = call_llm(
        prompt=[
            {"role" : "system", "content" : final_operational_breif_prompt.format(
                manifest_text=state["manifest_text"],
                metadata=state["extracted_metadata"],
                selected_route=state["selected_route"],
                warehouse_context=state["warehouse_db_context"]
            )}
        ],
        type={"type" : "text"}
    )

    result = {
        "incident_id" : state["incident_id"],
        "origianl_incident_summary": summary,
        "parsed_metadata" : state["extracted_metadata"],
        "rag_validation_rules_applied" : serialize_for_json(state["routing_rag_context"]),
        "routes_evaluated" : state["available_routes"],
        "final_selected_route" : state["selected_route"],
        "queried_warehouse_metrics" : state["warehouse_db_context"],
        "graph_routing_metadata" : {
            "loops_executed" : state["clarification_attempts"],
            "final_decision_state" : state["routing_decision"],
            "reroute_impact_score" : state["reroute_impact_score"]
        },
        "final_operations_brief" : final_operational_brief
    }   

    id = state["incident_id"]
    filename = id + "_reroute_advisory_report.json"

    report_writers(data=result, filename=filename)

    print("--report generation--")

    return {
        "final_report" : result
    }