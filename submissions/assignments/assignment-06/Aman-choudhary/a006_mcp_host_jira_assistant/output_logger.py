import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
QUERY_HISTORY_FILE = OUTPUT_DIR / "query_history.json"
CURRENT_TOOLS_FILE = OUTPUT_DIR / "current_tools.json"
def _read_json(file: Path, default):
    if not file.exists():
        return default
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default
def _write_json(file: Path, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
def record_tool(tool_name: str):
    tools = _read_json(CURRENT_TOOLS_FILE, [])
    tools.append(tool_name)
    _write_json(CURRENT_TOOLS_FILE, tools)


def get_tools_used():
    return _read_json(CURRENT_TOOLS_FILE, [])
def clear_tools():
    _write_json(CURRENT_TOOLS_FILE, [])
def log_query(user_query: str,tools_used: list,final_answer: str,write_action_performed: bool,):
    history = _read_json(QUERY_HISTORY_FILE, [])
    history.append(
        {
            "user_query": user_query,
            "tools_used": tools_used,
            "final_answer": final_answer,
            "write_action_performed": write_action_performed,
        }
    )
    _write_json(QUERY_HISTORY_FILE, history)