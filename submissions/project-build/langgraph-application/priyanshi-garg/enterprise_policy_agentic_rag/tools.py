
import os
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
from prompts import QUERY_CLASSIFIER_PROMPT, CLARIFICATION_PROMPT, QUERY_REWRITE_PROMPT, CONTEXT_GRADING_PROMPT, FINAL_RESPONSE_PROMPT, ANSWER_GENERATOR_PROMPT, REFLECTION_PROMPT
 
REWRITE_MAX_ATTEMPTS = 2

llm = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model="openai/gpt-oss-120b",
    temperature=0
)



from typing_extensions import TypedDict

class PolicyAgentState(TypedDict):
    """
    Represents the state of our workflow.
    """

    user_question:str

    query_type:str

    required_policy_domains:list

    retrieved_context:list

    context_grade:str

    answer:str

    retry_count:int

    reflection:dict

    final_response:str

def query_classifier(state: PolicyAgentState) -> PolicyAgentState:
    """Classify the query based on the policies."""
        
    user_question= state['user_question']

    classification_system_message = QUERY_CLASSIFIER_PROMPT

    prompt = ChatPromptTemplate.from_messages([
        ("system", classification_system_message),
        ("human", "user_question: {user_question}")
    ])

    chain = prompt | llm

    response = chain.invoke({"user_question":user_question})

    return {
        "classification": response
    }

def clarification_handler(state: PolicyAgentState) -> PolicyAgentState:
    """Check whether query is ambiguous and ask clarification if needed."""

    classification = state["classification"]
    user_question = state["user_question"]

    clarification_system_message = CLARIFICATION_PROMPT

    prompt = ChatPromptTemplate.from_messages([
        ("system", clarification_system_message),
        ("human", "user_question: {user_question}\nclassification: {classification}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "user_question": user_question,
        "classification": classification
    })

    if response.get("needs_clarification") is True:
        state["pending_clarification"] = True
        state["final_answer"] = response.get("message", 
            "Your question needs clarification."
        )
        return state

    state["pending_clarification"] = False
    return state

def query_rewriter(state: PolicyAgentState) -> PolicyAgentState:
    """Rewrite user query to improve retrieval quality."""

    # Max attempts guard
    if state.get("rewrite_count", 0) >= REWRITE_MAX_ATTEMPTS:
        return state

    query = state["query"]

    # Import prompt from prompts.py
    rewrite_system_message = QUERY_REWRITE_PROMPT

    prompt = ChatPromptTemplate.from_messages([
        ("system", rewrite_system_message),
        ("human", "original_query: {query}")
    ])

    chain = prompt | llm

    response = chain.invoke({"query": query})
    rewritten = response.get("rewritten_query", "").strip()

    # Update state
    state["rewritten_query"] = rewritten
    state["rewrite_count"] = state.get("rewrite_count", 0) + 1

    return state

from config import TOP_K


def normal_retrieval(state: PolicyAgentState) -> PolicyAgentState:
    """Retrieve top-K documents for single-domain policy queries."""

    db = state["vectorstore"]
    query = state["rewritten_query"] or state["query"]

    raw = db.similarity_search_with_score(query, k=TOP_K)

    results = []
    for doc, score in raw:
        results.append({
            "policy_domain": "single",
            "source_file": doc.metadata.get("source_file"),
            "chunk_id": doc.metadata.get("chunk_id"),
            "content": doc.page_content,
            "relevance_score": float(score)
        })

    # Update state
    state["retrieved_docs"] = results
    state["retrieval_mode"] = "normal"

    return state


def parallel_retrieval(state: PolicyAgentState) -> PolicyAgentState:
    """Retrieve top-K documents for multi-domain policy queries."""

    db = state["vectorstore"]
    query = state["rewritten_query"] or state["query"]

    raw = db.similarity_search_with_score(query, k=TOP_K)

    results = []
    for doc, score in raw:
        results.append({
            "policy_domain": "multi",
            "source_file": doc.metadata.get("source_file"),
            "chunk_id": doc.metadata.get("chunk_id"),
            "content": doc.page_content,
            "relevance_score": float(score)
        })

    state["retrieved_docs"] = results
    state["retrieval_mode"] = "parallel"

    return state

def context_grader(state: PolicyAgentState) -> PolicyAgentState:
    """Grade the relevance of retrieved documents before answer generation."""

    user_question = state["query"]
    retrieved_docs = state.get("retrieved_docs", [])

    # Import grading prompt
    grading_system_message = CONTEXT_GRADING_PROMPT

    prompt = ChatPromptTemplate.from_messages([
        ("system", grading_system_message),
        ("human",
         "user_question: {user_question}\n\nretrieved_docs: {retrieved_docs}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "user_question": user_question,
        "retrieved_docs": retrieved_docs
    })

    state["context_grade"] = {
        "overall_relevance": response.get("overall_relevance", ""),
        "relevant_chunks": response.get("relevant_chunks", []),
        "irrelevant_chunks": response.get("irrelevant_chunks", []),
        "missing_information": response.get("missing_information", []),
        "decision": response.get("decision", "ANSWER"),
    }

    return state

def answer_generator_node(state: PolicyAgentState) -> PolicyAgentState:
    """Generate a grounded answer using the relevant retrieved documents."""

    user_question = state["query"]
    graded = state.get("context_grade", {})
    relevant = graded.get("relevant_chunks", [])

    system_msg = ANSWER_GENERATOR_PROMPT

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human",
         "user_question: {user_question}\n\nrelevant_chunks: {relevant_chunks}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "user_question": user_question,
        "relevant_chunks": relevant,
    })

    state["draft_answer"] = response.get("grounded_answer", "")
    state["used_chunks"] = response.get("used_chunks", [])

    return state

def reflection_node(state: PolicyAgentState) -> PolicyAgentState:
    """Reflect on the draft answer and improve quality if needed."""

    draft = state.get("draft_answer", "")
    user_question = state["query"]
    graded = state.get("context_grade", {})
    relevant = graded.get("relevant_chunks", [])

    system_msg = REFLECTION_PROMPT

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human",
         "user_question: {user_question}\n"
         "draft_answer: {draft_answer}\n"
         "relevant_chunks: {relevant_chunks}\n")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "user_question": user_question,
        "draft_answer": draft,
        "relevant_chunks": relevant,
    })

    # Expected JSON:
    # { "improved_answer": "" }

    improved = response.get("improved_answer", draft)

    state["final_candidate"] = improved

    return state


def final_response_node(state: PolicyAgentState) -> PolicyAgentState:
    """Produce the final user-facing answer."""

    candidate = state.get("final_candidate") or state.get("draft_answer") or ""

    system_msg = FINAL_RESPONSE_PROMPT

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", "answer_to_present: {candidate}")
    ])

    chain = prompt | llm

    response = chain.invoke({"candidate": candidate})

    # Expected JSON:
    # { "final_answer": "" }

    state["final_answer"] = response.get("final_answer", candidate)

    return state