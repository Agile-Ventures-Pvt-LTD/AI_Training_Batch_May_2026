import json
import datetime
from pathlib import Path

# Path to log file
LOG_FILE = Path("./logs/query_log.jsonl")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_interaction(query: str, response: str):
    """Record a query and response in structured format."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "query": query,
        "response": response
    }

    # Append to JSONL file
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Also print to console for visibility
    print("\n=== Interaction Logged ===")
    print(json.dumps(entry, indent=2, ensure_ascii=False))
