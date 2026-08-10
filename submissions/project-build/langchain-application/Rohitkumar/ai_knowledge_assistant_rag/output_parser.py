import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import OUTPUTS_DIR


def parse_json_response(raw_response: str) -> Optional[Dict[str, Any]]:
    """Attempt to parse a JSON response from the LLM. Falls back gracefully."""
    if not raw_response or not raw_response.strip():
        return None

    text = raw_response.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
        try:
            return json.loads(text[brace_start : brace_end + 1])
        except json.JSONDecodeError:
            pass

    return None


def build_answer_output(
    question: str,
    query_type: str,
    parsed: Optional[Dict[str, Any]],
    raw_response: str,
    retrieved_chunks: List[Dict[str, Any]],
    top_k: int,
) -> Dict[str, Any]:
    """Build the standardised output dictionary from parsed LLM response."""
    if parsed:
        raw_sources = parsed.get("sources", [])
        formatted_sources = []
        for src in raw_sources:
            if isinstance(src, str):
                formatted_sources.append({"source_file": src, "page_number": "", "chunk_id": "", "snippet": ""})
            elif isinstance(src, dict):
                formatted_sources.append({
                    "source_file": src.get("source_file", ""),
                    "page_number": src.get("page_number", ""),
                    "chunk_id": src.get("chunk_id", ""),
                    "snippet": src.get("snippet", ""),
                })
            else:
                formatted_sources.append(src)

        answer_data = {
            "answer": parsed.get(
                "answer", "I could not find this information in the provided documents."
            ),
            "supporting_evidence": parsed.get("supporting_evidence", []),
            "sources": formatted_sources,
            "confidence": parsed.get("confidence", "LOW"),
            "answerability": parsed.get("answerability", "NOT_FOUND"),
        }
    else:
        answer_data = {
            "answer": raw_response.strip()
            if raw_response.strip()
            else "I could not find this information in the provided documents.",
            "supporting_evidence": [],
            "sources": [],
            "confidence": "LOW",
            "answerability": "PARTIALLY_ANSWERED",
        }

    answer_data.setdefault("answer", "I could not find this information in the provided documents.")
    answer_data.setdefault("supporting_evidence", [])
    answer_data.setdefault("sources", [])
    answer_data.setdefault("confidence", "LOW")
    answer_data.setdefault("answerability", "NOT_FOUND")

    retrieval_debug = {
        "top_k": top_k,
        "retrieved_chunks": [
            {
                "rank": i + 1,
                "chunk_id": c.get("chunk_id", ""),
                "source_file": c.get("source_file", ""),
                "page_number": c.get("page_number", ""),
                "similarity_score": c.get("similarity_score", None),
                "preview": c.get("text", "")[:200],
            }
            for i, c in enumerate(retrieved_chunks)
        ],
    }

    return {
        "question": question,
        "query_type": query_type,
        "answer": answer_data["answer"],
        "supporting_evidence": answer_data["supporting_evidence"],
        "sources": answer_data["sources"],
        "confidence": answer_data["confidence"],
        "answerability": answer_data["answerability"],
        "retrieval_debug": retrieval_debug,
    }


def build_not_found_output(question: str, query_type: str, top_k: int) -> Dict[str, Any]:
    """Build output when no relevant chunks are retrieved."""
    return {
        "question": question,
        "query_type": query_type,
        "answer": "I could not find this information in the provided documents. "
        "The retrieved context does not contain enough evidence to answer this question reliably.",
        "supporting_evidence": [],
        "sources": [],
        "confidence": "LOW",
        "answerability": "NOT_FOUND",
        "retrieval_debug": {
            "top_k": top_k,
            "retrieved_chunks": [],
        },
    }


def save_output_to_json(output: Dict[str, Any], filename: str = "results.json") -> Path:
    """Save the pipeline output dictionary to a JSON file in the outputs directory."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUTS_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    return output_path


def save_output_with_timestamp(output: Dict[str, Any]) -> Path:
    """Save output with a timestamp-based filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.json"
    return save_output_to_json(output, filename=filename)