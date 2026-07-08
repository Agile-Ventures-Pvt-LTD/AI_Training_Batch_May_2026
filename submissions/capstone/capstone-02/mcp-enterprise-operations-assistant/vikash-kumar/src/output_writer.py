import os
import json
from typing import Any

def save_json(folder: str, filename: str, data: Any):
    os.makedirs(folder, exist_ok=True)
    target_path = os.path.join(folder, filename)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_markdown_summary(folder: str, filename: str, logs: list):
    os.makedirs(folder, exist_ok=True)
    target_path = os.path.join(folder, filename)
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("# Sample Run Outputs\n\n")
        for i, entry in enumerate(logs, 1):
            f.write(f"## Q{i} – Automated Operational Check\n")
            f.write(f"**User Query:** {entry['query']}\n")
            f.write(f"**Tools Used:** {entry['tool_used']}\n")
            f.write(f"**Final Answer:**\n```text\n{entry['result']}\n```\n\n")
            if i < len(logs):
                f.write("---\n\n")
