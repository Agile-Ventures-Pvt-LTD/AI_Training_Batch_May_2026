"""
Output parser for extracting and formatting structured responses.
"""

import json
from typing import Dict, Any, Optional


def parse_classification(response: str) -> Dict[str, Any]:
    """
    Parse classification response from model.
    
    Args:
        response: Raw response string from classification API call
        
    Returns:
        Dictionary with parsed classification data
    """
    if isinstance(response, dict):
        return response
    
    try:
        # Try to parse as JSON
        parsed = json.loads(response)
        return parsed
    except json.JSONDecodeError:
        # If not JSON, extract key information
        return {
            "query_type": extract_field(response, "query_type"),
            "requires_retrieval": "true" in response.lower(),
            "requires_comparison": "comparison" in response.lower(),
            "answer_style": extract_field(response, "answer_style"),
            "reasoning_summary": response[:200] + "..." if len(response) > 200 else response
        }


def parse_answer(response: Dict[str, Any] | str) -> Dict[str, Any]:
    """
    Parse answer response from model.
    
    Args:
        response: Response from answer generation API call
        
    Returns:
        Dictionary with parsed answer data
    """
    if isinstance(response, dict):
        return ensure_answer_schema(response)
    
    if isinstance(response, str):
        json_from_response = extract_json_from_response(response)
        if json_from_response is not None:
            return ensure_answer_schema(json_from_response)

        try:
            parsed = json.loads(response)
            return ensure_answer_schema(parsed)
        except (json.JSONDecodeError, TypeError):
            return {
                "question": "",
                "query_type": "",
                "answerability": "NOT_FOUND",
                "confidence": "LOW",
                "answer": response,
                "supporting_evidence": [],
                "sources": []
            }

    return {
        "question": "",
        "query_type": "",
        "answerability": "NOT_FOUND",
        "confidence": "LOW",
        "answer": str(response),
        "supporting_evidence": [],
        "sources": []
    }


def extract_field(text: str, field_name: str) -> Optional[str]:
    """
    Extract field value from unstructured text.
    
    Args:
        text: Text to search
        field_name: Field to extract
        
    Returns:
        Extracted value or None
    """
    import re
    pattern = rf'"{field_name}"\s*:\s*"([^"]*)"'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


def format_response(data: Dict[str, Any], response_type: str = "answer"):
    """
    Format and print response data.
    
    Args:
        data: Parsed response data
        response_type: Type of response ('classification' or 'answer')
    """
    if response_type == "classification":
        print(f"\n Query Type: {data.get('query_type', 'Unknown')}")
        print(f" Requires Retrieval: {data.get('requires_retrieval', False)}")
        print(f" Requires Comparison: {data.get('requires_comparison', False)}")
        print(f" Answer Style: {data.get('answer_style', 'Standard')}")
        print(f" Reasoning: {data.get('reasoning_summary', 'N/A')}")
        
    elif response_type == "answer":
        print(f"\nAnswer:")
        print(f"{data.get('answer', 'No answer generated')}\n")
        
        if data.get('supporting_evidence'):
            print(f"Supporting Evidence:")
            for idx, evidence in enumerate(data['supporting_evidence'], 1):
                print(f"{idx}. {evidence}")
        
        if data.get('sources'):
            print(f"\nSources:")
            for idx, source in enumerate(data['sources'], 1):
                print(f"{idx}. {source}")
        
        print(f"\nConfidence: {data.get('confidence', 'MEDIUM')}")
        print(f"Answerability: {data.get('answerability', 'ANSWERED')}")


def extract_json_from_response(response: str) -> Optional[Dict[str, Any]]:
    """
    Try to extract JSON from response text.
    
    Args:
        response: Raw response text
        
    Returns:
        Parsed JSON or None
    """
    import re

    # Try to find the first balanced JSON object in the text.
    start = response.find("{")
    if start == -1:
        return None

    brace_count = 0
    for idx in range(start, len(response)):
        char = response[idx]
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1
            if brace_count == 0:
                candidate = response[start:idx+1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    break
    return None


def ensure_answer_schema(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure the answer dictionary contains the required schema and defaults.
    """
    if not isinstance(parsed, dict):
        return {
            "question": "",
            "query_type": "",
            "answerability": "NOT_FOUND",
            "confidence": "LOW",
            "answer": "",
            "supporting_evidence": [],
            "sources": []
        }

    return {
        "question": parsed.get("question", ""),
        "query_type": parsed.get("query_type", ""),
        "answerability": parsed.get("answerability", "NOT_FOUND"),
        "confidence": parsed.get("confidence", "LOW"),
        "answer": parsed.get("answer", ""),
        "supporting_evidence": parsed.get("supporting_evidence", []) if isinstance(parsed.get("supporting_evidence", []), list) else [],
        "sources": parsed.get("sources", []) if isinstance(parsed.get("sources", []), list) else []
    }


def validate_answer(answer: Dict[str, Any]) -> bool:
    """
    Validate answer structure.
    
    Args:
        answer: Answer dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['answer', 'confidence', 'answerability']
    return all(field in answer for field in required_fields)


def validate_classification(classification: Dict[str, Any]) -> bool:
    """
    Validate classification structure.
    
    Args:
        classification: Classification dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['query_type', 'reasoning_summary']
    return all(field in classification for field in required_fields)
