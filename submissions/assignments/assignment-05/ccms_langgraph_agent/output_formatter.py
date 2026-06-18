import json
import os
from datetime import datetime


def save_agent_response(
    user_question,
    implementation_choice,
    tools_used,
    records_found,
    answer,
    limitations=None,
    filename="outputs/final_agent_responses.json"
):

    response = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_question": user_question,
        "implementation_choice": implementation_choice,
        "tools_used": tools_used,
        "records_found": records_found,
        "answer": answer,
        "sensitive_data_masked": True,
        "limitations": limitations or []
    }

    os.makedirs("outputs", exist_ok=True)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            existing = json.load(f)
    except:
        existing = []

    existing.append(response)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            existing,
            f,
            indent=4
        )

    return response