import os
import json
from typing import Optional, Any

def to_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def to_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
    

def read_json(filename):
    file_path = filename

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            data.pop("success", None)

        return data

    except Exception as e:
        raise RuntimeError(f"Error reading '{file_path}': {e}")