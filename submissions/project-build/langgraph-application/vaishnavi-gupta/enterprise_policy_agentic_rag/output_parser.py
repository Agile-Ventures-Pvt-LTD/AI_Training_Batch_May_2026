import json
from datetime import datetime
from pathlib import Path

LOG_FILE = "outputs/execution_logs.json"

Path("logs").mkdir(exist_ok=True)


def log_execution(
        answer,
        policy_basis,
        sources,
        answerability,
        confidence,
        recommended_next_step
           
):
    record = {
        "answer": "",
        "policy_basis": [],
        "sources": [],
        "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
        "confidence": "HIGH | MEDIUM | LOW",
        "recommended_next_step":
    }

    print("Writing log...")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print("Log saved.")