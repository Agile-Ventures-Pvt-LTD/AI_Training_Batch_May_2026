from langchain_core.prompts import ChatPromptTemplate
from utils.gClient import get_client


def classify_query(query) -> dict:
    """Classifies the customer query into predefined categories."""

    print("---CLASSIFYING QUERY---")

    classification_system_message = """
    You are an expert query classifier. Analyze the customer query and classify it into one of the following categories:
    - VPN
    - OUTLOOK_EMAIL
    - LAPTOP_PERFORMANCE
    - PASSWORD_RESET
    - NETWORK_CONNECTIVITY
    - PRINTER
    - UNKNOWN
    Respond ONLY with the classification type, reasoning summary and confidence.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", classification_system_message),
        ("human", "Customer Query: {query}")
    ])
    
    llm = get_client()
    
    classifier_chain = prompt | llm

    try:
        classification_result: str = classifier_chain.invoke({"query": query})
        print(f"Classification: {classification_result.content}")
        
        return classification_result

    except Exception as e:
        print(f"Error during classification: {e}")
        return {"query_category": "unknown", "error_message": f"Classification failed: {e}"}