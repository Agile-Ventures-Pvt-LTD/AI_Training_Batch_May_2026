from typing import Dict

from state import GraphState


def parse_incident_node(state: GraphState):

    """
    Use LangChain structured output to extract shipment information from manifest_text.
    """

    question = state["question"]

    question = question.lower()

    return state

def policy_rag_lookup_node(state: GraphState):

    """
    Retrieve logistics rules relevant to the current incident.

    """
    return state

def load_alternative_routes_node(state: GraphState):

    """
    Load routes for the disrupted port.

    current_route_index = 0
    clarification_attempts = 0
    """

    return state

def select_route_node(state: GraphState):

    """
    Select a route from "available_routes" .

    """

    return state

def check_warehouse_node(state: GraphState):

    """
    Read the {warehouse_id} from the selected route.

    """

    return state

def analyze_route_node(state: GraphState):
    """
    Evaluate the selected route using:
        1. Extracted shipment metadata
        2. Retrieved logistics rules
        3. Selected route details
        4. Added route delay
        5. Warehouse utilization
        6. Warehouse operational status
        7. Warehouse risk tier
    """

    return state

def route_clarification_node():
    """
    Reject the current route and check the next available route.

    """

def finalize_route_node():
    """
    Finalize the accepted route.

    """

def escalate_incident_node():
    """
    Mark the incident for escalation.
    Escalation should occur when:
        1. No acceptable route is available.
        2. A critical delay condition exists.
        3. The maximum route retry limit is reached.
    """

def generate_report_node(): 
    """
    Purpose:
        Generate the final result.
        Use LangChain and the Groq LLM to create a short final_operations_brief .
        The remaining report fields should be created from the graph state.
        Save the report as JSON.

    """ 

def final_node(state: GraphState):

    print()

    print(state["answer"])

    return state


