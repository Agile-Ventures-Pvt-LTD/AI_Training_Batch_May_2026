import json
from datetime import datetime
from pathlib import Path

LOG_FILE = "outputs/sample_run_outputs.json"

Path("logs").mkdir(exist_ok=True)


def log_execution(
    user_query,
    tasks,
    task_results,
    final_report
):
    record = {
        "user_query": user_query,
        "tasks": tasks,
        "task_results": task_results,
        "final_report": final_report
    }

    print("Writing log...")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print("Log saved.")