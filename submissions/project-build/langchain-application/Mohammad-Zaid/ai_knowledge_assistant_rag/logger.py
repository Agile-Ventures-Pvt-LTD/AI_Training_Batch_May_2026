

import json
from datetime import datetime
from pathlib import Path


def save_query_log(question, answer, sources, confidence, answerability):
    """Save query to logs/query_logs.jsonl"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "answerability": answerability
    }
    
    with open(log_dir / "query_logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
