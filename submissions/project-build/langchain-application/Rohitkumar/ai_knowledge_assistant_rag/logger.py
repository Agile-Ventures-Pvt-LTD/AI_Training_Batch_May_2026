import json
from datetime import datetime
from typing import Dict, Any

from config import QUERY_LOG_FILE


def log_query(payload: Dict[str, Any]) -> None:
    query_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "question": payload.get("question", ""),
        "query_type": payload.get("query_type", ""),
        "retrieved_sources": [
            {
                "source_file": chunk.get("source_file", ""),
                "page_number": chunk.get("page_number", ""),
                "chunk_id": chunk.get("chunk_id", ""),
            }
            for chunk in payload.get("retrieval_debug", {}).get("retrieved_chunks", [])
        ],
        "answer": payload.get("answer", ""),
        "answerability": payload.get("answerability", ""),
        "confidence": payload.get("confidence", ""),
    }
    QUERY_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUERY_LOG_FILE, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(query_record, ensure_ascii=False) + "\n")
