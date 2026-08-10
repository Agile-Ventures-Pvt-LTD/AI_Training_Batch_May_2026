from rag import retrieve
from typing import Literal
from utils.llm import get_client
from tools import get_alternative_routes_tool, query_warehouse_inventory_tool
from state import LogisticsIncidentState
from schemas import ManifestTextOutput
from langchain_core.prompts import ChatPromptTemplate

def parse_incident(state: LogisticsIncidentState) -> dict:
    """Parses the manifest text to extract metadata information"""
    llm = get_client().with_structured_output(ManifestTextOutput)
    
    manifest_text = state['manifest_text']
    
    extraction_prompt = f"""
    You are an expert data extractor.
    You are given a block of manifest text. 
    Identify and extract every piece of information that appears to be important. 
    Return all extracted items concatenated into a single plain‑text string, separated only by spaces or commas—no bullet points, headings, or additional formatting. 
    If nothing relevant is found, return an empty string.
    
    Manifest text:
    {manifest_text}
    """
    response = llm.invoke(extraction_prompt)
    
    return {'extracted_metadata': response.content}

def policy_rag_lookup(state: LogisticsIncidentState) -> dict:
    """Retrieves policy rules regarding routing and logistics rules."""
    
    metadata = state['extracted_metadata']
    
    docs = retrieve(metadata)
    
    state['routing_rag_context']
    return {'routing_rag_context': docs.__dict__['content']}

def load_alternative_routes(state: LogisticsIncidentState) -> dict:
    """Fetches available routes for a disrupted port id."""
    disrupted_route = state['disrupted_port_id']
    alt_routes = get_alternative_routes_tool.invoke({"disrupted_port_id": disrupted_route})
    return {"available_routes": alt_routes, "current_route_index": 0, "clarification_attempts": 0}

def select_route(state: LogisticsIncidentState) -> dict:
    """Select a route from available routes based on route index."""
    index = state['current_route_index']
    routes = state['available_routes']
    current_route = routes[index]
    return {"selected_route": current_route}

def check_warehouse(state: LogisticsIncidentState) -> dict:
    """Fetches warehouse information based on warehouse id from the selected route"""
    warehouse_id = state['selected_route']['warehouse_id']
    warehouse_context = query_warehouse_inventory_tool.invoke({"warehouse_id": warehouse_id})
    return {'warehouse_db_context': warehouse_context}

def analyze_route(state: LogisticsIncidentState) -> dict:
    """Evaluate the selected route using
    Extracted shipment metadata, Retrieved logistics rules, Selected route details, 
    Added route delay, Warehouse utilization, Warehouse operational status, Warehouse risk tier"""
    extracted_metadata = state['extracted_metadata']
    logistic_rules = state['routing_rag_context']
    selected_route = state['selected_route']
    warehouse = state['warehouse_db_context']
    
    added_route_delay = selected_route["added_delay_hours"]
    risk_tier = warehouse['risk_tier']
    operational_status = warehouse['operational_status']
    current_utilization_pct = warehouse['current_utilization_pct']
    
    llm = get_client()
    res = llm.invoke(f"Extract value for maximum_tolerable_delay_hours from the following data {extracted_metadata}. Return only the value in string format without any decoration or formatting, just plain simple string having intger value if maximum tolerable delay hours is present, else return empty string.")
    maximum_tolerable_delay_hours = res.content
    if maximum_tolerable_delay_hours:
        maximum_tolerable_delay_hours = int(maximum_tolerable_delay_hours)
    
    status = ''
    reroute_impact_score = 0
    if current_utilization_pct > 85:
        status = 'ROUTE_CLARIFICATION'
        reroute_impact_score += 30
    if operational_status is not "ACTIVE":
        status = 'ROUTE_CLARIFICATION'
        reroute_impact_score += 30
    if risk_tier == "ELEVATED":
        status = 'ROUTE_CLARIFICATION'
        reroute_impact_score += 25
    if added_route_delay > maximum_tolerable_delay_hours:
        status = 'ROUTE_CLARIFICATION'
        reroute_impact_score += 25
    if added_route_delay > 120:
        status = 'CRITICAL_DELAY'
        reroute_impact_score += 50
    if not status:
        prompt = f"""
        Using extracted metadata: {extracted_metadata} and logistic rules: {logistic_rules}, 
        classify whether the route needs to be clarified or is a critical delay route or is an optimal path.
        Strictly answer with OPTIMAL_PATH_FOUND or CRITICAL_DELAY or ROUTE_CLARIFICATION as output only in plain string."""
        sllm = llm.with_structured_output(Literal['ROUTE_CLARIFICATION', 'CRITICAL_DELAY', 'OPTIMAL_PATH_FOUND'])
        output = sllm.invoke(prompt).content
        if 'ROUTE_CLARIFICATION' in output:
            status = 'ROUTE_CLARIFICATION'
        elif 'CRITICAL_DELAY' in output:
            status = 'CRITICAL_DELAY'
        else:
            status = 'OPTIMAL_PATH_FOUND'
    return {'routing_decision': status, "reroute_impact_score": reroute_impact_score}

def route_clarification(state: LogisticsIncidentState) -> dict:
    """Rejects the current route and check the next available route."""
    
    clarification_attempts = state['clarification_attempts'] + 1
    current_route_index = state['current_route_index'] + 1
    available_routes = state['available_routes']
    max_clarification_attempts = state['max_clarification_attempts']
    if len(available_routes) < current_route_index + 1 or clarification_attempts > max_clarification_attempts:
        return {"routing_decision": 'CRITICAL_DELAY'}
    return {"clarification_attempts": clarification_attempts, "current_route_index": current_route_index}

def finalize_route(state: LogisticsIncidentState) -> dict:
    """Finalize the accepted route."""
    finalized_route = state['available_routes']
    return {'logs': finalized_route}

def escalate_incident(state: LogisticsIncidentState) -> dict:
    """Mark the incident for escalation."""
    total = len(state['available_routes'])
    current_route_index = state['current_route_index']
    clarification_attempts = state['clarification_attempts']
    max_clarification_attempts = state['max_clarification_attempts']
    escalate = ""
    if max_clarification_attempts < clarification_attempts:
        escalate += f"clarification_attempts more than limit. "
    if total < current_route_index:
        escalate += f"No available routes left. "
    if state['routing_decision'] == 'CRITICAL_DELAY':
        escalate += f"A critical delay condition exists."
    return {'logs': escalate}

def generate_report(state: LogisticsIncidentState) -> dict:
    """Generate the final advisory report."""
    extracted_metadata = state['extracted_metadata'],
    selected_route = state['selected_route']
    logs = state['logs']
    prompt = f"""
    Using extracted_metadata: {extracted_metadata}
    and selected_route: {selected_route}
    and this information: {logs}
    generate summary for the logistics team that explains:
    - What happened.
    - Which route was selected or why the incident was escalated.
    - The major rule or warehouse condition that affected the decision.
    """
    llm = get_client()
    report = llm.invoke(prompt).content
    return {'final_report': report}