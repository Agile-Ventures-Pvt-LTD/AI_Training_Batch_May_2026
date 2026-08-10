import json
import os
from datetime import datetime

OUTPUT_FILE = "outputs/evaluation_results.json"


def save_output(user_query, response_text):
    os.makedirs("outputs", exist_ok=True)

    try:
        parsed_response = json.loads(response_text)
    except:
        parsed_response = {
            "raw_output": response_text
        }

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": user_query,
        "response": parsed_response
    }

    data = []

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]
            except:
                data = []

    data.append(entry)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("Output saved")