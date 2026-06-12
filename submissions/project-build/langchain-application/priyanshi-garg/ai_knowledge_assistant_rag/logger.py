import json
import os
from datetime import datetime

LOG_FILE = "logs/query_logs.jsonl"

os.makedirs("logs", exist_ok=True)


def log_query(data):

    data["timestamp"] = datetime.now().isoformat()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")