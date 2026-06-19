import json
import os
from datetime import datetime

OUTPUT_FILE = "outputs/evaluation_results.json"


def save_output(record: dict):
    os.makedirs("outputs", exist_ok=True)

    data = []

   
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except Exception:
            data = []  # fallback if corrupted

   
    record["timestamp"] = str(datetime.now())

    data.append(record)

   
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)