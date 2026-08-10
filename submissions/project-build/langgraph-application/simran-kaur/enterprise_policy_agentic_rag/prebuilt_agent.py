import os
from langchain_groq import ChatGroq
from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field
from mermaid import Mermaid

from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, StateGraph

# from google.colab import userdata
from IPython.display import Image, display

from config import GROQ_API_KEY,GROQ_MODEL

llm = ChatGroq(
    model=GROQ_MODEL, 
    groq_api_key=GROQ_API_KEY,
)


# class State(TypedDict):
#     """
#     Represents the state of our workflow.
#     """
#     topic: str                      
#     outline: str | None             
#     outline_validation: str | None  
#     document: str | None            
#     error_message: str | None 

 


 

class RouterState(TypedDict):
    """
    Represents the state of our query routing workflow.
    """
    customer_query: str                #by user
    query_category: str | None   #by clssifier node
    context:str|None                 #given by retriver
    context_grade:str|None        #by context_grade node
    response: str | None                
    error_message: str | None    

 #--------------------here : pydantic for classification output syntax-----------------

 


def classify_query(state: RouterState) -> dict:
    """Classifies the customer query into predefined categories."""

    print("---CLASSIFYING QUERY---")
    query = state['customer_query']

    classification_system_message = """
    You are an expert query classifier for enterprise policy documents. Analyze the customer query and classify it into one of the following categories:
        - HR_LEAVE
        - TRAVEL (e.g., domestic travel approval, international travel approval)
        - REIMBURSEMENT (e.g., meal reimbursement, hotel reimbursement)
        - IT_SECURITY (e.g., company laptop usage, personal laptop restrictions)
        - AI_USAGE (e.g., public AI tool restrictions, customer data handling)
        - MULTI_POLICY (if multiple policy-related areas are relevant)
        - UNANSWERABLE (if the query cannot be answered from policy documents)
        - AMBIGUOUS (if the query has multiple possible meanings)
        - OTHER
    Return EXACT JSON only. Use the following fields:
      - query_type
      - required_policy_domains (a list of one or more policy domain IDs: ai_usage_policy, hr_leave_policy, it_security_policy, reimbursement_policy, travel_policy)
      - requires_parallel_retrieval
      - requires_clarification
      - reasoning_summary
    """

    class QueryClassification(BaseModel):
        """
            define structure of query
        """
        query_type: Literal["TRAVEL", "REIMBURSEMENT", "IT_SECURITY", "AI_USAGE","MULTI_POLICY","UNANSWERABLE","AMBIGUOUS","OTHER"] = Field(
            description="The classified category of the customer query."
        ) 
        required_policy_domains: list[Literal["ai_usage_policy", "hr_leave_policy", "it_security_policy", "reimbursement_policy", "travel_policy"]]= Field(
            description="Required policy domains based on the query. Use the exact policy domain ids."
        )
        requires_parallel_retrieval: bool= Field(
            description="it tells whether parallel retrieval is reguired or not. It is true if more than one policy domain is present"
        ) 
        requires_clarification:bool = Field(
            description="It tells whether user input requires clarification or not"
        ) 
        reasoning_summary:str = Field(
            description="It summarises the reason for it classification"
        ) 
    

    prompt = ChatPromptTemplate.from_messages([
        ("system", classification_system_message),
        ("human", "Customer Query: {query}")
    ])

    # Use structured output to get reliable classification
    classifier_chain = prompt | llm.with_structured_output(QueryClassification)

    try:
        classification_result: QueryClassification = classifier_chain.invoke({"query": query})
        print(f"Classification: {classification_result.query_type} (Reason: {classification_result.reasoning_summary})")
        # Update the state with the classification result
        # return {"query_category": classification_result.query_type}
        return {"query_type":classification_result.query_type,"required_policy_domains":classification_result.required_policy_domains,"requires_parallel_retrieval":classification_result.requires_parallel_retrieval, "requires_clarification":classification_result.requires_clarification, "reasoning_summary":classification_result.reasoning_summary}
    
    except Exception as e:
        print(f"Error during classification: {e}")
        # If classification fails, mark as unknown and log error
        return {"query_category": "unknown", "error_message": f"Classification failed: {e}"}
    


#================================GRADING NODE==========================================

class ContextGrading(BaseModel):
    """Schema for context grade result."""
    overall_relevance: Literal["HIGHLY_RELEVANT","PARTIALLY_RELEVANT","WEAK","NOT_RELEVANT"] = Field(
        description="It tells how relevant is the retrieved context to the user query."
    ) 
    relevant_chunks:list[str]= Field(
        description="It has the list of relevant chunks from the context"
    ) 
    irrelevant_chunks:list[str]= Field(
        description="it send list of irrelevant chunks from the context"
    ) 
    missing_information:list[str] = Field(
        description="It send the list of the missing information which was required to answer user query"
    ) 
    decision:Literal["ANSWER","REWRITE_QUERY","ASK_CLARIFICATION","NOT_FOUND"] = Field(
        description="It describe further actions to take"
    ) 



def grade_context(state: RouterState) -> RouterState:
    """Checks whether the context is relevant to the user query."""

    print("---VALIDATING OUTLINE---")

    customer_query=state['customer_query']
    context = state['context']
    context_grade=context_grade['context_grade']

    if not context:
         return {
             "outline_validation": "INVALID: No outline provided.", "error_message": "Outline generation failed."
         }



    validation_system_prompt = """
    You are an outline validator. The assistant must grade retrieved context before generating the final answer. Supported grades: HIGHLY_RELEVANT,PARTIALLY_RELEVANT ,WEAK ,NOT_RELEVANT. Comapare the retrieved context with the customer query to prove grades
    Respond ONLY with the required JSON format.
    """

    validation_prompt = ChatPromptTemplate.from_messages([
        ("system", validation_system_prompt),
        ("human", f"context:\n\n{context}")
    ])

    # Use tool/function calling for structured output
    validation_llm = llm.with_structured_output(ContextGrading)
    validation_chain = validation_prompt | validation_llm

    try:
        validation_result: grade_context = validation_chain.invoke({"customer_query":customer_query,"context":context})
        print(f"Validation result: {validation_result}")

        if validation_result.overall_relevance=="HIGHLY_RELEVANT" or validation_result.overall_relevance=="PARTIALLY_RELEVANT":
            return {"context_grade": "RELEVANT"}
        
        else:
            error_msg = f"INVALID: {validation_result.reason}"
            return {"outline_validation": error_msg, "error_message": error_msg}
    except Exception as e:
        print(f"Error during validation: {e}")
        error_msg = f"INVALID: Validation check failed due to error: {e}"
        return {"outline_validation": error_msg, "error_message": error_msg}



#======================generate answer======================

def generate_answer(state: RouterState) -> RouterState:

    """Generates the full document based on the validated relevant context."""

    print("---GENERATING DOCUMENT---")

    context= state['context']

    customer_query = state['customer_query']

    writer_system_prompt = """
    You are a skilled writer. Write a comprehensive document based on the provided outline.
    Expand on each point with clear explanations and examples.
    Use appropriate section numbers and subsection numbers in the following format:
    - Main sections to be numbered (e.g., 2)
    - Subsections to use decimal numbering (e.g., 2.1)
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", writer_system_prompt),
        ("human", f"Topic: {customer_query}\n\nOutline:\n{context}\n\nPlease write the full document:")
    ])

    chain = prompt | llm

    response = chain.invoke({"customer_query": customer_query, "context": context})

    print("---Answer GENERATED---")

    return {
        "document": response.content
    }
#===============conditional gate====================
def should_generate_answer(state: RouterState) -> Literal["generate_answer",END]:

    """Determines the next step based on outline validation."""
    print("---CHECKING OUTLINE VALIDITY---")

    validation_result = state.get('outline_validation', '') # Use .get for safety

    if validation_result == "HIGHLY_RELEVANT" or validation_result=="PARTIALLY_RELEVANT":
        print("Context: Context is relevant. Proceeding to answer generation.")
        return "generate_answer"
    elif validation_result=="WEAK":
        print(f": Context is of weak relevance.")
        # Store the reason for stopping if not already set by validation node
        if not state.get('error_message'):
            state['error_message'] = f"Outline validation failed: {validation_result}"
        return "end" # LangGraph convention for ending the graph execution
    



#================gRAPH================================

workflow = StateGraph(RouterState)

# Add the nodes
workflow.add_node("generate_outline", classify_query)
workflow.add_node("validate_outline", grade_context)
workflow.add_node("generate_document", generate_answer)

# Add edges for the sequential flow
workflow.add_edge(START, 'generate_outline')
workflow.add_edge()
workflow.add_edge("generate_outline", "validate_outline")

# Add the conditional edge (the gate)
workflow.add_conditional_edges(
    "validate_outline",         # Source node
    should_generate_answer   # Function to decide the next step
)

# Add the final edge
workflow.add_edge("generate_document", END)


compiled_workflow = workflow.compile()
