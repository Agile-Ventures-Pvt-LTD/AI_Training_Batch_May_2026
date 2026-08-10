from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import tools_condition, ToolNode
from core_rag.embedding import init_embedding
from langchain_groq import Chroma

embedding_model = init_embedding()

def choose_retriever(policy_name):
    vectorstore_persisted = Chroma(
        collection_name=policy_name,
        persist_directory='./enterprise_db',
        embedding_function=embedding_model
    )
    
    retriever = vectorstore_persisted.as_retriever(search_kwargs={'k': 5})
    
    return create_retriever_tool(
        retriever,
        "retrieve_",
        "Search and return information about Tesla 10k reports for the period 2021 - 2023."
    )

def retrieve_hr_leave_policy():
    return choose_retriever('hr_leave_policy')

def retrieve_travel_policy():
    return choose_retriever('travel_policy')

def retrieve_reimbursement_policy():
    return choose_retriever('reimbursement_policy')

def retrieve_it_security_policy():
    return choose_retriever('it_security_policy')

def retrieve_ai_usage_policy():
    return choose_retriever('ai_usage_policy')

tools = [retrieve_ai_usage_policy(), retrieve_it_security_policy(), retrieve_reimbursement_policy(), retrieve_travel_policy(), retrieve_hr_leave_policy()]