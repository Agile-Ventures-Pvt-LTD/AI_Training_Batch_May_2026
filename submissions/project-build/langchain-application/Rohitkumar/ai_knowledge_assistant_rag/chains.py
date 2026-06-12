import json
from typing import Any, Dict, List

from config import GROQ_API_KEY, GROQ_MODEL, TOP_K
from embeddings import EmbeddingModel
from vector_store import create_vector_store, load_vector_store
from chunking import create_chunks
from loaders import load_documents
from prompts import prompt, rag_prompt
from output_parser import parse_json_response, build_answer_output, build_not_found_output
from retriever import retrieve, format_retrieved_chunks
from logger import log_query

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None


def classify_query(question: str) -> Dict[str, Any]:
    """Classify the user query type using keyword-based logic."""
    lower = question.lower()
    if any(term in lower for term in ["compare", "comparison", "vs", "versus", "difference between"]):
        return {
            "query_type": "COMPARISON",
            "requires_retrieval": True,
            "requires_comparison": True,
            "answer_style": "structured",
            "reasoning_summary": "Comparison questions require multiple document sections.",
        }
    if any(term in lower for term in ["summarize", "summary", "summarise", "key points", "bullet"]):
        return {
            "query_type": "SUMMARY",
            "requires_retrieval": True,
            "requires_comparison": False,
            "answer_style": "summary",
            "reasoning_summary": "Summarization requests should condense retrieved context.",
        }
    if any(term in lower for term in ["risk", "risks", "regulatory", "legal", "compliance"]):
        return {
            "query_type": "RISK_ANALYSIS",
            "requires_retrieval": True,
            "requires_comparison": False,
            "answer_style": "analysis",
            "reasoning_summary": "Risk-related questions should retrieve risk and compliance context.",
        }
    if any(term in lower for term in ["will", "forecast", "predict", "future", "next year", "stock price", "guarantee"]):
        return {
            "query_type": "UNANSWERABLE_OR_SPECULATIVE",
            "requires_retrieval": True,
            "requires_comparison": False,
            "answer_style": "refusal",
            "reasoning_summary": "Speculative questions should be refused unless supported by documentation.",
        }
    if any(term in lower for term in ["who", "what", "when", "where", "how", "why", "which"]):
        return {
            "query_type": "FACTUAL_LOOKUP",
            "requires_retrieval": True,
            "requires_comparison": False,
            "answer_style": "direct",
            "reasoning_summary": "Factual lookup questions should use retrieved document evidence.",
        }
    return {
        "query_type": "OTHER",
        "requires_retrieval": True,
        "requires_comparison": False,
        "answer_style": "direct",
        "reasoning_summary": "General question that requires retrieval.",
    }


def build_rag_answer(
    question: str,
    retrieved_chunks: List[Dict[str, Any]],
    groq_api_key: str,
    model_name: str,
) -> Dict[str, Any]:
    """Generate a grounded answer using Groq LLM with retrieved context."""
    if ChatGroq is None:
        raise ImportError(
            "langchain-groq is required for answer generation. "
            "Install it with: pip install langchain-groq"
        )

    context_blocks = []
    for chunk in retrieved_chunks:
        context_blocks.append(
            f"Source: {chunk['source_file']} | Page: {chunk['page_number']} | Chunk: {chunk['chunk_id']}\n{chunk['text']}"
        )
    context_text = "\n\n---\n\n".join(context_blocks)
    prompt_text = rag_prompt.format(question=question, context=context_text)

    llm = ChatGroq(model=model_name, api_key=groq_api_key, temperature=0.1)
    response = llm.invoke(prompt_text)
    raw_response = response.content if hasattr(response, "content") else str(response)

    parsed = parse_json_response(raw_response)
    return build_answer_output(question, "GENERATED", parsed, raw_response, retrieved_chunks, TOP_K)


def run_question(question: str) -> Dict[str, Any]:
    """Run the full RAG pipeline for a single question."""
    
    query_data = classify_query(question)
    query_type = query_data["query_type"]

    
    documents = load_documents()
    if not documents:
        raise FileNotFoundError("No documents were loaded from the raw data folder.")

    # Chunk documents
    chunks = create_chunks(documents)

    # Generate embeddings
    embedding_model = EmbeddingModel("sentence-transformers/all-MiniLM-L6-v2")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.embed_documents(texts)

    #  Create vector store and retrieve
    vector_store = create_vector_store(chunks, embeddings)
    retrieved_chunks = retrieve(question, vector_store, embedding_model, top_k=TOP_K)

    #  Generate answer or return NOT_FOUND
    if not retrieved_chunks:
        output = build_not_found_output(question, query_type, TOP_K)
    else:
        
        if query_type == "UNANSWERABLE_OR_SPECULATIVE":
            
            output = build_not_found_output(question, query_type, TOP_K)
            output["answer"] = (
                "I could not find this information in the provided documents. "
                "The question appears to be speculative or ask about future events, "
                "which cannot be answered from the available document collection."
            )
        else:
            output = build_rag_answer(question, retrieved_chunks, GROQ_API_KEY, GROQ_MODEL)
            output["query_type"] = query_type

    #  Log the query
    log_query(output)
    return output