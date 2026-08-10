from langchain_groq import ChatGroq
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from tools import get_alternative_routes_tool, query_warehouse_inventory_tool
from langchain.vectorstores.faiss import FAISS
import os 
from typing import Literal
from dotenv import load_dotenv
load_dotenv()
faiss_save_path=os.getenv("faiss_save_path")
from rag import get_embedding_model
from report_writer import save_result
import os
from dotenv import load_dotenv
load_dotenv()

def get_api_key():
    try:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("API key not found")
        return key

    except Exception as e:
        print(f"API KEY not found: {e}")
        return None

def get_model():
    try:
        model = os.getenv("GROQ_MODEL")
        if not model:
            raise ValueError("model not found")
        return model

    except Exception as e:
        print(f"Model not found: {e}")
        return None 

llm = ChatGroq(
    model=get_model(),
    groq_api_key=get_api_key(),
)

from state import LogisticsIncidentState


# This is a function used to get meta data from input
def parse_incident(state:LogisticsIncidentState)->dict:
    """Extract meta data from manifest_text provided """
    manifest_text=state["manifest_text"]

    class metadata(BaseModel):
        """Schema for outline validation result."""
        shipment_id:str
        cargo_weight_tons: int
        cargo_type:str
        target_warehouse_id:str
        has_perishables:bool
        maximum_tolerable_delay_hours:int

    system_prompt="""you are an helpful agent. your task is to parse te data and extract meta information
    from it.
    instructions:
    -do not add any thing by yourself
    -return a valid json only
    Required output format:
    {
    "shipment_id": ,
    "cargo_weight_tons": ,
    "cargo_type": ,
    "target_warehouse_id": 
    "has_perishables": ,
    "maximum_tolerable_delay_hours":
    }
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "manifest_text: {manifest_text}")
    ])


    extraction_chain = prompt | llm.with_structured_output(metadata)

    try:
        result: metadata = extraction_chain.invoke({"manifest_text": manifest_text})
        return {"extracted_metadata": result}
    except Exception as e:
        print(f"Error during classification: {e}")
        return {"extracted_metadata": {"unknown":"meta data not found"}, "logs": [f"Classification failed: {e}"]}
    





def policy_rag_lookup(state:LogisticsIncidentState)->dict:
    data=state["extracted_metadata"]
    new_store = FAISS.load_local(faiss_save_path, get_embedding_model(), allow_dangerous_deserialization=True)
    results = new_store.similarity_search(data, k=3)
    return{"routing_rag_context":results}
    


def load_alternative_routes(state:LogisticsIncidentState)->dict:
    disrupted_port_id=state["disrupted_port_id"]
    result=get_alternative_routes_tool(disrupted_port_id)
    return {"available_routes": result,
            "current_route_index":0,
            "clarification_attempts":0,
            "max_clarification_attempts":2
            }



def select_route(state:LogisticsIncidentState)->dict:
    current_route_index=state["current_route_index"]
    available_routes=state["available_routes"]
    selected_route=available_routes[current_route_index]
    return{"selected_route":selected_route}



def check_warehouse(state:LogisticsIncidentState)->dict:
    selected_route=state["selected_route"]
    warehouse_id=selected_route["warehouse_id"]
    result=query_warehouse_inventory_tool(warehouse_id)
    return{
        "warehouse_db_context": result
    }



def analyze_route(state:LogisticsIncidentState)->dict:
    meta_data=state["extracted_metadata"]
    rag_data=state["routing_rag_context"]
    selected_route=state["selected_route"]
    ware_data=state["warehouse_db_context"]

    current_utilization_pct=ware_data.get("current_utilization_pct")
    operational_status=ware_data.get("operational_status")
    risk_tier=ware_data.get("risk_tier")
    added_delay_hours=select_route.get("added_delay_hours")

    context={
        "meta_data":meta_data,
        "rules":rag_data,
        "Route":selected_route,
        "warehouse details":ware_data

    }
    
    if current_utilization_pct > 85:
        response="ROUTE_CLARIFICATION"
    elif operational_status != "ACTIVE":
        response="ROUTE_CLARIFICATION"
    elif risk_tier == "ELEVATED":
        response="ROUTE_CLARIFICATION"
    elif added_delay_hours > 120:
        response="CRITICAL_DELAY"
    # elif added_delay_hours > maximum_tolerable_delay_hours:
    #     response="ROUTE_CLARIFICATION"
    else:
        response="OPTIMAL_PATH_FOUND"

    system_prompt="""you are an evaluator. and you are provided with the details.
    based of provided data. analyze routing specified and based on that . find reroute_impact_score
    analyze every aspect and rule in detail and return the score only. do not include any explaination or reasoning"""

    messages=[
        {"role":"system", "content":system_prompt},
        {"role":"user", "content":context}
    ]

    result=llm.invoke(messages).content
    return{
        "reroute_impact_score":result,
        "routing_decision":response
    }


def decision_routing(state:LogisticsIncidentState)->Literal["OPTIMAL_PATH_FOUND","ROUTE_CLARIFICATION","CRITICAL_DELAY"]:
    routing_decision=state["routing_decision"]
    if routing_decision=="OPTIMAL_PATH_FOUND":
        return "OPTIMAL_PATH_FOUND"
    if routing_decision=="ROUTE_CLARIFICATION":
        return "ROUTE_CLARIFICATION"
    else:
        return "CRITICAL_DELAY"



def route_clarification(state:LogisticsIncidentState)->dict:
    clarification_attempts=state["clarification_attempts"]
    current_route_index=state["current_route_index"]
    max_clarification_attempts=state["max_clarification_attempts"]
    clarification_attempts=clarification_attempts+1
    current_route_index=current_route_index+1

    if clarification_attempts>max_clarification_attempts:
        return{
            "routing_decision":"CRITICAL_DELAY"
        }   

    return{
         "current_route_index":current_route_index,
         "clarification_attempts":clarification_attempts,
     }




    
def finalize_route(state:LogisticsIncidentState):
    selected_route=state["selected_route"]
    return{
        "final_state":selected_route
    }


def escalate_incident(state:LogisticsIncidentState):
    routing_decision=state["routing_decision"]
    max_tries=state["max_clarification_attempts"]
    if routing_decision=="CRITICAL_DELAY":
        return{
            "logs":"escalated",
            "final_state":{}
        }
     

def generate_report(state:LogisticsIncidentState):
    incident_id=state["incident_id"]
    manifest_text=state['manifest_text']
    disrupted_port_id=state["disrupted_port_id"]
    extracted_metadata=state["extracted_metadata"]
    routing_rag_context=state["routing_rag_context"]
    available_routes=state["available_routes"]
    current_route_index=state["current_route_index"]
    selected_route=state["selected_route"]
    warehouse_db_context=state["warehouse_db_context"]
    reroute_impact_score=state["reroute_impact_score"]
    routing_decision=state["routing_decision"]
    clarification_attempts=state["clarification_attempts"]
    max_clarification_attempts=state["max_clarification_attempts"]
    final_state=state["final_state"]

    data={
        "incident_id":incident_id,
        "original_incident_summary":manifest_text,
        "parsed_metadata":extracted_metadata,
        "rag_validation_rules_applied":routing_rag_context,
        "routes_evaluated":available_routes,
        "final_selected_route":selected_route,
        "queried_warehouse_metrics":warehouse_db_context,
        "graph_routing_metadata":{
            "loops_executed":clarification_attempts,
            "final_decision_state":final_state,
            "reroute_impact_score":reroute_impact_score
        }
    }
    final_belief=llm.invoke( messages=[
        {"role":"system", "content":"analyze the data and give the summary"},
        {"role":"user", "content":data}
    ])

    data["final_belief"]=final_belief

    save_result(data)
    

   