
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from src.schema import LangchainStructured
from src.state import LogisticsIncidentState
from src.rag import retriever
import json
from src.tools import get_alternative_routes_tool, query_warehouse_inventory_tool


os.environ['GROQ_API_KEY'] =os.getenv('GROQ_API_KEY')

llm = ChatGroq(
    model="openai/gpt-oss-120b",  # or your model
    groq_api_key=os.environ["GROQ_API_KEY"],
)

def langchain_agent(initial_input):
    system_prompt="""
        extract the information from manifest_txt given in initial_input.
        -don not invent information
        -give output in the provided structured format
        -These values must be extracted from  manifest_text .
        """
    agent = create_agent(
        model=llm,
        response_format=LangchainStructured,
        system_prompt=system_prompt
        
    )
    query= json.dumps(initial_input)

    result = agent.invoke({"messages": [{"role": "user", "content": query}]})

    return result["structured_response"]

# shipment_id='SH-4002' cargo_weight_tons=550 cargo_type='industrial electronics' target_warehouse_id='WH-WEST-202' has_perishables=True maximum_tolerable_delay_hours=72

#--------------------------NODES---------------------------


def parse_incident(state:LogisticsIncidentState) -> LogisticsIncidentState:

    """
    Use LangChain structured output to extract shipment information from  manifest_text
        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """

    incident_id = state['initial_id']
    manifest_text = state['manifest_text']
    disrupted_port_id = state['disrupted_port_id']

    initial_input={"incident_id": incident_id,
                   "manifest_text": manifest_text,
                   "disrupted_port_id": disrupted_port_id}
    
    parsed_metadata= dict(langchain_agent(initial_input))

    return {
        "extracted_metadata": parsed_metadata
    }


# initial_input = {"incident_id": "INC-001","manifest_text": "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle due to an active worker strike. The vessel is carrying 550 tons of industrial electronics originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling components and cannot sustain delays exceeding 72 hours.","disrupted_port_id": "PORT-SEATTLE-02"}
# print(langchain_agent(initial_input))




def policy_rag_lookup(state):

    """
        Retrieve documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, routing_rag_content, that contains retrieved documents
        """
    extracted_metadata = state["extracted_metadata"]

    query_str = json.dumps(extracted_metadata)

    routing_rag_content=retriever(query_str)

    return {
        "routing_rag_content": routing_rag_content
    }



def load_alternative_routes(state):

    """Load routes for the disrupted port.
        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, available_routes for the disrupted_port_id

    """
    current_route_index = 0
    clarification_attempts = 0
    disrupted_port_id = state["disrupted_port_id"]

    available_routes = get_alternative_routes_tool(disrupted_port_id)

    return {
        "available_routes": available_routes,
        "current_route_index": current_route_index,
        "clarification_attemps": clarification_attempts
    }


def select_route(state):
        
    """Select a route from  available_routes
        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, selected_route from the available_routes

    """
    available_routes=state['available_routes']
    current_route_index=state["curent_route_index"]
        

    outline_generation_system_message = """
    Select one route from  available_routes .The selected route should be based on:
    'current_route_index'
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", outline_generation_system_message),
        ("human", "Available_routes: {available_routes}, current_route_index={current_route_index}")
    ])

    chain = prompt | llm        

    response = chain.invoke({"available_routes":available_routes, "current_route_index": current_route_index})

    return {
        "selected_route": response.content
  
    }

        

def check_warehouse(state):
    """Read the  warehouse_id  from the selected route.
        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, warehouse_db_context from the selected_route
    """
    selected_route = state[selected_route]
    warehouse_id= selected_route['warehouse_id']
    warehouse_db_context=query_warehouse_inventory_tool(warehouse_id)

    return {
        "warehouse_db_context" : warehouse_db_context
    }



def analyze_route(state):

    """Evaluate the selected route using:
     Extracted shipment metadata
     Retrieved logistics rules
     Selected route details
     Added route delay
     Warehouse utilization
     Warehouse operational status
     Warehouse risk tier
     
     Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, reroute_impact_score and routing_decision
     
    """
    extracted_metadata = state["extracted_metadata"]
    routing_rag_context = state["routing_rag_context"]
    selected_route = state["selected_route"]
    warehouse_db_context = state['warehouse_db_context']

    current_utilization_pct =warehouse_db_context['current_utilization_pct']
    operational_status = warehouse_db_context['operational_status']
    risk_tier = warehouse_db_context['risk_tier']
    maximum_tolerable_delay_hours= extracted_metadata['maximum_tolerable_delay_hours']

    rerouter_impact_score=0
    
    system_prompt = """
    you are a shipping routing expert. 
    Extract the  relevant value from the given variables if in dictionary or list format.
    Use the following rules to perform routing:

    if current_utilization_pct > 85, then choice:"ROUTE_CLARIFICATION"

    if current_utilization_pct > 85, then choice:"ROUTE_CLARIFICATION"

    if current_utilization_pct > 85, then choice:"ROUTE_CLARIFICATION"

    if operational_status is not ACTIVE, then  choice:"
    if risk_tier = ELEVATED, then choice: "ROUTE_CLARIFICATION"

    if added_delay_hours > maximum_tolerable_delay_hours, then  choice:"ROUTE_CLARIFICATION"

    if added_delay > 120 then return choice:Critical_delay

    When none of the above conditions fail, then choice: "OPTIMAL_PATH_FOUND"

    Add to rerouter_impact_score
    +30 if warehouse utilization is above 85 percent
    +25 if warehouse risk tier is ELEVATED
    +30 if warehouse status is not ACTIVE
    +25 if added route delay exceeds the shipment delay limit
    +50 if added route delay exceeds 120 hours

    return {choice:str,
            rerouter_impact_score
            }

    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "extracted_metadata:{extracted_metadata},routing_rag_context : {routing_rag_context},current_utilization_pct:{current_utilization_pct},selected_route:{selected_route}")
    ])

    chain = prompt | llm

    response = chain.invoke({"extracted_metadata":extracted_metadata,"routing_rag_context": routing_rag_context,"current_utilization_pct":current_utilization_pct,"selected_route":selected_route})

    data = dict(response.content)
    routing_decision = data['choice']
    rerouter_impact_score=data['rerouter_impact_score']

  

    return {
        "rerouter_impact_score": rerouter_impact_score,
        "routing_decision": routing_decision
    }
    



def route_clarification(state):
    
    clarification_attempts  = state[clarification_attempts]
    current_route_index = state[current_route_index]
    clarification_attempts+=1
    max_clarification_attempts = 2
    if clarification_attempts>=max_clarification_attempts
        return 




def finalize_route(state):


def escalate_incident(state):


def generate_report(state):



