import json
import re
from typing import Dict, Any, List

def extract_json(text: str) -> Dict[str, Any]:
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json|JSON)?\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                pass
        try:
            return json.loads(text[text.index("{"):text.rindex("}") + 1])
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Unable to parse valid JSON structure from response: {str(e)}")

def parse_query_classification(llm_response: str) -> Dict[str, Any]:
    res = extract_json(llm_response)
    return {
        "query_type": res.get("query_type", "OTHER"),
        "required_policy_domains": res.get("required_policy_domains", []),
        "requires_parallel_retrieval": res.get("requires_parallel_retrieval", False),
        "requires_clarification": res.get("requires_clarification", False),
        "reasoning_summary": res.get("reasoning_summary", "")
    }

def parse_context_grade(llm_response: str) -> Dict[str, Any]:
    res = extract_json(llm_response)
    return {
        "overall_relevance": res.get("overall_relevance", "WEAK"),
        "relevant_chunks": res.get("relevant_chunks", []),
        "irrelevant_chunks": res.get("irrelevant_chunks", []),
        "missing_information": res.get("missing_information", []),
        "decision": res.get("decision", "NOT_FOUND")
    }

def parse_reflection(llm_response: str) -> Dict[str, Any]:
    res = extract_json(llm_response)
    return {
        "is_grounded": res.get("is_grounded", False),
        "has_citations": res.get("has_citations", False),
        "unsupported_claims": res.get("unsupported_claims", []),
        "needs_revision": res.get("needs_revision", False),
        "reflection_summary": res.get("reflection_summary", "")
    }

def parse_final_rag_output(llm_response: str) -> Dict[str, Any]:
    res = extract_json(llm_response)
    sources = res.get("sources", [])
    
    validated_sources = [
        {
            "source_file": str(src.get("source_file", "unknown")),
            "policy_domain": str(src.get("policy_domain", "UNKNOWN")),
            "chunk_id": str(src.get("chunk_id", "unknown")),
            "snippet": str(src.get("snippet", ""))
        }
        for src in sources if isinstance(src, dict)
    ] if isinstance(sources, list) else []

    return {
        "answer": res.get("answer", ""),
        "policy_basis": res.get("policy_basis", []),
        "sources": validated_sources,
        "answerability": res.get("answerability", "UNANSWERED"),
        "confidence": res.get("confidence", "LOW"),
        "recommended_next_step": res.get("recommended_next_step", "")
    }

def safe_parse(parser_function, response: str, default_value: Dict[str, Any]) -> Dict[str, Any]:
    try:
        return parser_function(response)
    except Exception:
        return default_value
