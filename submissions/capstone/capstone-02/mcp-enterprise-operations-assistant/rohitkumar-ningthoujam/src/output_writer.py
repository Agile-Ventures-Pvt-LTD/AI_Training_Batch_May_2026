import json
from pathlib import Path

OUTPUTS_DIR = Path(__file__).resolve().parents[1] / "outputs"

def save_tool_discovery(discovered):
    path = OUTPUTS_DIR / "tool_discovery.json"
    with open(path, "w") as f:
        json.dump(discovered, f, indent=2)
    return path

def save_query_results(results):
    path = OUTPUTS_DIR / "mandatory_query_results.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    return path