from state import LogisticsIncidentState
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from schemas import ShipmentMetadata
from langchain_core.prompts import ChatPromptTemplate
from rag import get_rag_context
from tools import get_alternative_routes_tool, query_warehouse_inventory_tool
import json
from langchain_core.tools import StructuredTool

load_dotenv()


def _get_llm():
    model=os.getenv('GROQ_MODEL')
    api_key=os.getenv('GROQ_API_KEY')
    return ChatGroq(model=model, api_key=api_key)

def get_llm():
    return _get_llm()

def parse_incident(state: LogisticsIncidentState):
    llm=get_llm()
    system_msg="You are incident extractor, extract the required fields from manifest text, Dont invent any values "
    human_msg=state["manifest_text"]
    prompt= [
        ("system", system_msg),
        ("human", human_msg)
    ]

    structured_llm = llm.with_structured_output(ShipmentMetadata)
    metadata_obj = structured_llm.invoke(prompt)
    metadata = metadata_obj.model_dump() if hasattr(metadata_obj, "model_dump") else metadata_obj
    return {
        "extracted_metadata" : metadata
    }

def policy_rag_lookup(state:LogisticsIncidentState):
    # print("policy")
    context=get_rag_context(state["manifest_text"])
    return {
        "routing_rag_context" : context
    }

def load_alternative_routes(state:LogisticsIncidentState):
    # print("load")
    llm=get_llm()
    system_msg="You are routing expert, check disrupted port id and give available routes for it Dont invent any values "
    human_msg= state["disrupted_port_id"]
    prompt= [
        ("system", system_msg),
        ("human", human_msg)
    ]

    routes = get_alternative_routes_tool.invoke({"disrupted_port_id": state["disrupted_port_id"]}) 
    
    # disrupted_port=state["disrupted_port_id"]
    # routes = get_alternative_routes_tool({"disrupted_port_id": disrupted_port})   
    return {
        "available_routes": routes,
        "current_route_index" : 0,
        "clarification_attempts" : 0,
        "loops_executed" :0,
        "routes_evaluated" : []
    }

def select_route(state:LogisticsIncidentState):
    # print("select")
    routes=state.get("available_routes")
    idx=state.get("current_route_index")
    if idx < len(routes):
        selected = routes[idx]
        return {
            "selected_route": selected,
            "routing_decision": "ROUTE_CLARIFICATION", 
        }
    else:
        return {
            "selected_route": {},
            "routing_decision": "CRITICAL_DELAY",
        }
    
def check_warehouse(state:LogisticsIncidentState):
    # print("check")
    selected=state.get("selected_route")
    warehouse_id=selected.get("warehouse_id")
    warehouse_info=query_warehouse_inventory_tool.invoke({"warehouse_id" : warehouse_id})
    return {
        "warehouse_db_context": warehouse_info,
    }

def analyze_route(state:LogisticsIncidentState):
    selected=state.get("selected_route")
    warehouse=state.get("warehouse_db_context")
    metadata=state.get("extracted_metadata")

    utilization = warehouse.get("current_utilization_pct")
    status = warehouse.get("operational_status")
    risk = warehouse.get("risk_tier")
    added_delay = selected.get("added_delay_hours")
    tolerable_delay = metadata.get("maximum_tolerable_delay_hours")
    if not tolerable_delay:
        tolerable_delay = 999999
    if not selected:
        return {
            "routing_decision": "CRITICAL_DELAY",
            "reroute_impact_score": 0
        }
            
    score = 0
    reasons = []
    decision = "OPTIMAL_PATH_FOUND"

    if utilization>85:
        score+=30
        decision= "ROUTE_CLARIFICATION"
        reasons.append("Warehouse utilization is above 85%")
    if risk=="ELEVATED":
        score+=25
        decision="ROUTE_CLARIFICATION"
        reasons.append("Warehouse risk tier is elevated")
    if status!="ACTIVE":
        score+=30
        decision="ROUTE_CLARIFICATION"
        reasons.append("Warehouse status is not active")
    if added_delay>tolerable_delay:
        score+=25
        decision="ROUTE_CLARIFICATION"
        reasons.append("Added route delay exceeds the shipment delay limit")
    if added_delay>120:
        score+=50
        decision="CRITICAL_DELAY"
        reasons.append("Added route delay exceeds 120 hours")

    reroute_impact_score=min(score,100)
    if decision=="OPTIMAL_PATH_FOUND":
        reasons_str= "All conditions are successful"
    else:
        reasons_str=" ".join(reasons)
    routes_evaluated=state.get("routes_evaluated")
    if routes_evaluated is None:
        routes_evaluated = []

    routes_evaluated.append({
        "route_id": selected.get("route_id"),
        "decision": decision,
        "reason": reasons_str
    })
    return {
        "routing_decision": decision,
        "reroute_impact_score": reroute_impact_score,
        "routes_evaluated": routes_evaluated
    }
    
def route_clarification(state:LogisticsIncidentState):
    current_attempts=state.get("clarification_attempts") + 1
    current_index=state.get("current_route_index") + 1

    routes=state.get("available_routes")
    max_attempts=state.get("max_clarification_attempts")
    loops=state.get("loops_executed", 0) + 1

    if current_index < len(routes) and current_attempts < max_attempts:
        decision = "ROUTE_CLARIFICATION"
    else:
        decision = "CRITICAL_DELAY"
        
    return {
        "clarification_attempts": current_attempts,
        "current_route_index": current_index,
        "routing_decision": decision,
        "loops_executed": loops
    }

def finalize_route(state:LogisticsIncidentState):
    selected=state.get("selected_route")

    return {
        "routing_decision" : "OPTIMAL_PATH_FOUND"
    }

def escalate_incident(state:LogisticsIncidentState):
    return {
        "routing_decision": "CRITICAL_DELAY",
        "selected_route": {}
    }

def generate_report(state:LogisticsIncidentState):
    llm=get_llm()
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a summarizer,write a short, one-sentence summary of the following"),
        ("human", "{manifest_text}")
    ])
    formatted_summary = summary_prompt.format_messages(manifest_text=state["manifest_text"])
    summary_res = llm.invoke(formatted_summary)
    original_summary = summary_res.content.strip()
    
    brief_prompt = ChatPromptTemplate.from_messages([
        ("system", "You have to summarize what happened in this incident, "
                   "which route was selected, and the key rule or warehouse condition "
                   "that drove this decision. "),
        ("human", "Incident Detail:\n"
                  "Incident ID: {incident_id}\n"
                  "Manifest Text: {manifest_text}\n"
                  "Final Decision: {routing_decision}\n"
                  "Final Selected Route: {selected_route}\n"
                  "Warehouse Metrics checked: {warehouse_db}\n"
                  "All Evaluated Routes: {routes_eval}\n"
                  "RAG Logistics Rules retrieved: {rules_context}")
    ])
    formatted_brief = brief_prompt.format_messages(
        incident_id=state["incident_id"],
        manifest_text=state["manifest_text"],
        routing_decision=state["routing_decision"],
        selected_route=json.dumps(state.get("selected_route")),
        warehouse_db=json.dumps(state.get("warehouse_db_context")),
        routes_eval=json.dumps(state.get("routes_evaluated")),
        rules_context=state.get("routing_rag_context")
    )
    brief_res = llm.invoke(formatted_brief)
    final_brief = brief_res.content.strip()
    
    rag_rules = [
        line.strip() for line in state.get("routing_rag_context").split("\n")
        if line.strip()
    ]
    
    report = {
        "incident_id": state["incident_id"],
        "original_incident_summary": original_summary,
        "parsed_metadata": state.get("extracted_metadata"),
        "rag_validation_rules_applied": rag_rules,
        "routes_evaluated": state.get("routes_evaluated"),
        "final_selected_route": state.get("selected_route"),
        "queried_warehouse_metrics": state.get("warehouse_db_context"),
        "graph_routing_metadata": {
            "loops_executed": state.get("loops_executed"),
            "final_decision_state": state["routing_decision"],
            "reroute_impact_score": state.get("reroute_impact_score")
        },
        "final_operations_brief": final_brief
    }
    
    os.makedirs("outputs", exist_ok=True)
    
    with open("outputs/reroute_advisory_report.json", "w") as f:
        json.dump(report, f, indent=4)
        
    incident_id = state["incident_id"]
    with open(f"outputs/{incident_id}_reroute_advisory_report.json", "w") as f:
        json.dump(report, f, indent=4)
        
    return {
        "final_report": report
    }
