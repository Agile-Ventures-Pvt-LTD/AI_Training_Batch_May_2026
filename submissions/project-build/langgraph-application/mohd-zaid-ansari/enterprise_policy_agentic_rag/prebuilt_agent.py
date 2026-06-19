from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from config import MODEL_NAME, GROQ_API_KEY
from prompts import system_prompt
from embedding import get_embedding_model
from vector_store import create_vectorstore
from retrievers import get_retriever
from tools import (
    classify_query,
    retrieve_hr_policy as _retrieve_hr_policy,
    retrieve_travel_policy as _retrieve_travel_policy,
    retrieve_reimbursement_policy as _retrieve_reimbursement_policy,
    retrieve_it_security_policy as _retrieve_it_security_policy,
    retrieve_ai_usage_policy as _retrieve_ai_usage_policy,
    generate_grounded_answer as _generate_grounded_answer,
)

system_message = system_prompt

llm = ChatGroq(model=MODEL_NAME, groq_api_key=GROQ_API_KEY)

embedding_model = get_embedding_model()
vectorstore = create_vectorstore(embedding_model)
retriever = get_retriever(vectorstore)


def retrieve_hr_policy(query: str):
    """Retrieve HR policy information relevant to the user query."""
    return _retrieve_hr_policy(query, retriever)


def retrieve_travel_policy(query: str):
    """Retrieve travel policy information relevant to the user query."""
    return _retrieve_travel_policy(query, retriever)


def retrieve_reimbursement_policy(query: str):
    """Retrieve reimbursement policy information relevant to the user query."""
    return _retrieve_reimbursement_policy(query, retriever)


def retrieve_it_security_policy(query: str):
    """Retrieve IT security policy information relevant to the user query."""
    return _retrieve_it_security_policy(query, retriever)


def retrieve_ai_usage_policy(query: str):
    """Retrieve AI usage policy information relevant to the user query."""
    return _retrieve_ai_usage_policy(query, retriever)


def generate_grounded_answer(query: str):
    """Generate a grounded answer using retrieved policy documents."""
    docs = []
    try:
        if hasattr(retriever, "get_relevant_documents"):
            docs = retriever.get_relevant_documents(query)
        elif hasattr(retriever, "retrieve"):
            docs = retriever.retrieve(query)
        else:
            docs = retriever.invoke(query)
    except Exception:
        docs = []

    normalized = []
    for d in docs:
        try:
            content = getattr(d, "page_content", d.get("page_content", ""))
            metadata = getattr(d, "metadata", d.get("metadata", {}))
        except Exception:
            content = ""
            metadata = {}
        normalized.append({
            "content": content,
            "source": metadata.get("source", metadata.get("file", "Unknown")),
            "page": metadata.get("page", "N/A"),
        })

    return _generate_grounded_answer(query, normalized)


tools = [
    classify_query,
    retrieve_hr_policy,
    retrieve_travel_policy,
    retrieve_reimbursement_policy,
    retrieve_it_security_policy,
    retrieve_ai_usage_policy,
    generate_grounded_answer,
]

agent = create_react_agent(
    llm,
    tools=tools,
    prompt=system_message,
)


def prebuilt_agent(user_input):
    try:
        message_input = [HumanMessage(content=user_input)]
        response = agent.invoke({"messages": message_input})
        return response["messages"][-1].content
    except Exception as e:
        return f"Error: {str(e)}"

