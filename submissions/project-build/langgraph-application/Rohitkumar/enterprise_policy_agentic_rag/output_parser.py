import json
import re

def parse_json(text):
    text = text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = re.sub(r'^```\s*', '', text)
    try:
        return json.loads(text)
    except:
        pass
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

def parse_classifier(text):
    default = {"query_type": "OTHER", "required_policy_domains": [], "requires_parallel_retrieval": False, "requires_clarification": False, "reasoning_summary": ""}
    data = parse_json(text)
    return data if data else default

def parse_grader(text):
    default = {"overall_relevance": "WEAK", "relevant_chunks": [], "irrelevant_chunks": [], "missing_information": [], "decision": "REWRITE_QUERY"}
    data = parse_json(text)
    return data if data else default

def parse_answer(text):
    default = {"answer": "Unable to generate answer from context.", "policy_basis": [], "sources": [], "answerability": "NOT_FOUND", "confidence": "LOW", "recommended_next_step": "Please contact HR or Finance for clarification."}
    data = parse_json(text)
    return data if data else default

def parse_reflection(text):
    default = {"is_grounded": False, "has_citations": False, "unsupported_claims": [], "needs_revision": True, "reflection_summary": "Reflection check failed."}
    data = parse_json(text)
    return data if data else default

def parse_clarification(text):
    default = {"clarification_question": "Could you please provide more details about which policy area your question relates to?", "missing_details": []}
    data = parse_json(text)
    return data if data else default