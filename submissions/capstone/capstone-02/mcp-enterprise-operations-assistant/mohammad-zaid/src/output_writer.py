import json
from src.config import OUTPUT_DIR


def save_query_result(result_dict: dict):
   
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = OUTPUT_DIR / "mandatory_query_results.json"

    existing_data = []
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = []
        except Exception:
            existing_data = []

    existing_data.append(result_dict)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)


def save_tool_discovery(discovery_dict: dict):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "tool_discovery.json", "w", encoding="utf-8") as f:
        json.dump(discovery_dict, f, indent=2, ensure_ascii=False)