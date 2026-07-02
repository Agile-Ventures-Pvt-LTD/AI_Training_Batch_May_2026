"""Utility functions."""

from __future__ import annotations
import json
import os
from typing import Any
try:
    from src_config import OUTPUT_DIR
except ImportError:
    from .src_config import OUTPUT_DIR


DEFAULT_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "output.json")
TEST_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "test_output.json")


def write_output(
    data: dict[str, Any],
    test: bool = False
) -> str:
    output_path = DEFAULT_OUTPUT_PATH if not test else TEST_OUTPUT_PATH
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "a", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return output_path