from config import llm
from pydantic import BaseModel, Field
from prompts import issue_classification
from typing import TypedDict, List, Dict, Optional
from langchain_core.output_parsers import StrOutputParser
from tools import (
    retriever_tool,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    generate_resolution_plan
)

class TroubleshootingState(TypedDict):
    user_query: str
    issue_type: str
    user_identifier: Optional[str]
    retrieved_guidance: List[Dict]
    user_profile: Dict
    device_status: Dict
    known_incidents: List[Dict]
    diagnostic_snapshot: Dict
    resolution_plan: Dict
    safety_review: Dict
    final_response: str


def agent(state : TroubleshootingState) -> TroubleshootingState:
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, Simply add the user question in the state
    """
    print("---CALL AGENT---")
    question = state["user_query"]

    prompt = [
        {"role" : "system", "content" : f"Do not change the user Question. Just simply return the same question: {question}"}
    ]

    response = llm.invoke(prompt)

    return {"user_query": response}


def classify_issue_node(state: TroubleshootingState) -> TroubleshootingState:
    """
    Classify the issue before generation

    Supported issue types:
    VPN
    OUTLOOK_EMAIL
    LAPTOP_PERFORMANCE
    PASSWORD_RESET
    NETWORK_CONNECTIVITY
    PRINTER
    UNKNOWN
    """

    class grade(BaseModel):
        """Classify the Query for the relevance"""

        issue_type: str = Field(description="Decide the type of the query between this VPN, OUTLOOK_EMAIL, LAPTOP_PERFORMANCE, PASSWORD_RESET, NETWORK_CONNECTIVITY, PRINTER, UNKNOWN")
        
    
    print("---Issue Classifier---")

    model = llm.with_structured_output(grade)
    
    question = state["user_question"]

    prompt = [
        {"role" : "system", "content" : issue_classification.format(user_question=question)}
    ]

    response = model.invoke(prompt)

    return {"issue_type" : response.query_type}


def retrieve_guidance_node(state: TroubleshootingState) -> TroubleshootingState:
    """
    Given the question, it will decide to retrieve using the retriever tool, or simply end.
    if the agent is answering the question without any context from tool then it should realy mention the same at the begining.
    """

    print("---retrieval_guidance_node---")

    question = state["user_query"]

    prompt = [
        {
            "role" : "system" , 
            "content" : f"""
            Retrieve the Required context using the retriever tool
            
            User Question
            {question}
            """
        }
    ]

    model = llm.bind_tools([retriever_tool])

    response = model.invoke(prompt)

    return {"retrieved_guidance" : response}


def parallel_context_node(state: TroubleshootingState) -> TroubleshootingState:
    """
    Gathers user, device and incident data after retrieving the context
    """

    class grade(BaseModel):
        """Classify the query for the user, device, incident"""
        user : str = Field(description="Only give the user full name")
        device : str = Field(description="Give the information about the device")
        incident : list = Field(description="Give the list of the incident which was happen")

    print("---parallel_context_node---")

    question = state["user_query"]

    prompt = [
        {
            "role" : "system" , 
            "content" : f"""
            Give the output on the basic of the user, device and incidents on the basic of the user query
            
            User Question
            {question}
            """
        }
    ]

    model = llm.bind_tools([get_user_profile, get_device_status, check_known_incidents])

    response = model.invoke(prompt)

    return {
        "user_profile" : response.user,
        "device_status" : response.device,
        "known_incidents" : response.incident
    }


def diagnostic_decision_node(state: TroubleshootingState) -> TroubleshootingState:
    """
    It will Determines likely cause and next step
    """

    print("---diagnostic_decision_node---")

    question = state["user_query"]

    prompt = [
        {
            "role" : "system" , 
            "content" : f"""
            Run the Diagnostic decision by using the tool which have provided
            
            User Question
            {question}
            """
        }
    ] 

    model = llm.bind_tools([run_diagnostic_check])

    response = model.invoke(prompt)

    return {"diagnostic_snapshot" : response}


def resolution_planner_node(state : TroubleshootingState) -> TroubleshootingState:
    """
    Creates recommended troubleshooting plan
    """

    question = state["user_query"]
    context = state["retrieved_guidance"]

    prompt = [
        {
            "role" : "system", 
            "content": f"""
            Make the resolution plan by using the user query and context

            Question : {question}
            Context : {context}
            """
        }
    ]

    model = llm.bind_tools([generate_resolution_plan])

    response = model.invoke(prompt)

    return {
        "resolution_plan" : response
    }


def safety_review_node(state : TroubleshootingState) -> TroubleshootingState:
    """
    Checks for the unsafe recommendation
    """

    question = state["user_query"]
    context = state["retrieved_guidance"]

    prompt = [
        {
            "role" : "system",
            "content" : f"""
            You are the expert safety reviewer you have to properly 
            analyze the question and the context and check wheather 
            is there any unsafe reccomendation.

            Question: {question}
            Context: {context}
            """
        }
    ]

    response = llm.invoke(prompt)

    return {"safety_review" : response}


def final_response_node(state : TroubleshootingState) -> TroubleshootingState:
    """
    Produces the final answer which will display to the user.
    """

    question = state["user_query"]
    context = state["retrieved_guidance"]

    prompt = [
        {
            "role" : "system",
            "content" : f"""
            You are the expert at giving the response to the user friendly manner

            With the help of the Question and Context

            Question : {question}
            Context : {context}
            """
        }
    ]

    chain = llm | StrOutputParser

    response = chain.invoke(prompt)

    return {"final_response" : response}