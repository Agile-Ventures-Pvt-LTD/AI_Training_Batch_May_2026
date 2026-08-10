from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field
from utils.gClient import get_client

class RouterState(TypedDict):
    """
    Represents the state of our query routing workflow.
    """
    customer_query: str
    query_category: str | None
    response: str | None
    error_message: str | None

class QueryClassification(BaseModel):
    """Schema for the query classification result."""
    category: Literal["HR_LEAVE", "TRAVEL", "REIMBURSEMENT", "IT_SECURITY", "AI_USAGE", "AMBIGUOUS"] = Field(
        description="The classified category of the customer query."
    )

def classify_query(state: RouterState) -> dict:
    """Classifies the customer query into predefined categories."""

    print("---CLASSIFYING QUERY---")
    query = state['customer_query']

    classification_system_message = """
    You are an expert query classifier. Analyze the customer query and classify it into one of the following categories:
    - HR_LEAVE 
    - TRAVEL 
    - REIMBURSEMENT 
    - IT_SECURITY 
    - AI_USAGE 
    - AMBIGUOUS 
    Respond ONLY with the word.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", classification_system_message),
        ("human", "Customer Query: {query}")
    ])
    llm = get_client()
    # Use structured output to get reliable classification
    classifier_chain = prompt | llm.with_structured_output(QueryClassification)

    try:
        classification_result: QueryClassification = classifier_chain.invoke({"query": query})
        print(f"Classification: {classification_result.category} (Reason: {classification_result.reasoning})")
        # Update the state with the classification result
        return {"query_category": classification_result.category}

    except Exception as e:
        print(f"Error during classification: {e}")
        return {"query_category": "unknown", "error_message": f"Classification failed: {e}"}