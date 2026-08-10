import json
import os
from datetime import datetime
from config import Config

def log_query(data: dict):
    """save query history to jsonl files"""
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
    data["timestamp"] = datetime.now().isoformat()
    with open(Config.LOG_FILE, "a",) as f: #encoding="utf-8"
        f.write(json.dumps(data) + "\n")