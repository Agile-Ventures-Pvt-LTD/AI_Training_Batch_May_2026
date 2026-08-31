from retrievers import retrieve
from config import GROQ_API_KEY, GROQ_MODEL, TOP_K
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)


def retrieve_hr_policy(query):
    """Retrieve HR/Leave policy chunks"""
    results = retrieve(query, k=TOP_K)
    filtered = [r for r in results if r["policy_domain"] == "HR_LEAVE"]
    return filtered if filtered else results


def retrieve_travel_policy(query):
    """Retrieve travel policy chunks"""
    results = retrieve(query, k=TOP_K)
    filtered = [r for r in results if r["policy_domain"] == "TRAVEL"]
    return filtered if filtered else results


def retrieve_reimbursement_policy(query):
    """Retrieve reimbursement policy chunks"""
    results = retrieve(query, k=TOP_K)
    filtered = [r for r in results if r["policy_domain"] == "REIMBURSEMENT"]
    return filtered if filtered else results


def retrieve_it_security_policy(query):
    """Retrieve IT security policy chunks"""
    results = retrieve(query, k=TOP_K)
    filtered = [r for r in results if r["policy_domain"] == "IT_SECURITY"]
    return filtered if filtered else results


def retrieve_ai_usage_policy(query):
    """Retrieve AI usage policy chunks"""
    results = retrieve(query, k=TOP_K)
    filtered = [r for r in results if r["policy_domain"] == "AI_USAGE"]
    return filtered if filtered else results


class GradeContext(BaseModel):
    """Grade relevance of retrieved chunks"""
    binary_score: str = Field(description="Relevance score 'yes' or 'no'")
    overall_relevance: str = Field(description="HIGHLY_RELEVANT, PARTIALLY_RELEVANT, WEAK, or NOT_RELEVANT")
    decision: str = Field(description="ANSWER, REWRITE_QUERY, or ASK_CLARIFICATION")


class RewriteQuery(BaseModel):
    """Rewritten query"""
    rewritten_query: str = Field(description="Improved query for better retrieval")


class Answer(BaseModel):
    """Grounded answer with citations"""
    answer: str = Field(description="Answer to the question based on policy chunks")
    citations: list = Field(description="List of chunk_ids used as references")


def grade_context(question, chunks):
    """Grade if retrieved chunks answer the question"""
    if not chunks:
        return {
            "binary_score": "no",
            "overall_relevance": "NOT_RELEVANT",
            "decision": "REWRITE_QUERY"
        }
    chunk_texts = "\n".join([c["content"] for c in chunks])
    template = """You are a grader. Check if these policy chunks are relevant to answer the question.
    Question: {question}
    Policy Chunks:
    {chunk_texts}
    Return:
    1. binary_score: 'yes' if relevant, 'no' if not
    2. overall_relevance: HIGHLY_RELEVANT, PARTIALLY_RELEVANT, WEAK, or NOT_RELEVANT
    3. decision: ANSWER (if good), REWRITE_QUERY (if weak), or ASK_CLARIFICATION (if unclear)"""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm.with_structured_output(GradeContext)
    
    result = chain.invoke({"question": question,"chunk_texts": chunk_texts})
    return {"binary_score": result.binary_score,
        "overall_relevance": result.overall_relevance,
        "decision": result.decision,
        "relevant_chunks": chunks
    }


def rewrite_query(original_query, feedback=None):
    """Rewrite query to make it better"""
    feedback_text = f"Feedback: {feedback}" if feedback else ""
    
    template = """Rewrite this query to be more specific and clear for policy document search.
    Original Query: {original_query}
    {feedback}
    Return the improved query.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm.with_structured_output(RewriteQuery)
    
    result = chain.invoke({"original_query": original_query,"feedback": feedback_text})
    
    return {"original_query": original_query, "rewritten_query": result.rewritten_query}


def generate_grounded_answer(question, chunks):
    """Generate answer based on policy chunks with citations"""
    if not chunks:
        return {
            "answer": "I couldn't find relevant policy information to answer this question.",
            "citations": []
        }
    
    chunk_refs = "\n".join([
        f"[{c['chunk_id']}] {c['content'][:200]}..."
        for c in chunks
    ])
    
    template = """Answer this question based ONLY on the policy chunks provided.
    Question: {question}
    Policy Chunks:
    {chunk_refs}
    Provide a clear answer with citations in format [chunk_id]. If you cannot answer from the chunks, say so."""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm.with_structured_output(Answer)
    
    result = chain.invoke({"question": question,"chunk_refs": chunk_refs})

    return {"question": question,
        "answer": result.answer,
        "citations": result.citations
    }
