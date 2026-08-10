import json
import re
from pathlib import Path
from datetime import datetime


# Extract JSON object or array from LLM response.
def extract_json(response_text):
    """
    Handles:
    - raw JSON
    - markdown JSON blocks
    - extra explanatory text
    """

    if not response_text:
        return None

    response_text = response_text.strip()

    # Direct parse
    try:
        return json.loads(response_text)
    except:
        pass

    # Pattern matching
    patterns = [
        r'```json\s*(.*?)\s*```',
        r'```(.*?)```',
        r'(\{.*\})',
        r'(\[.*\])'
    ]

    for pattern in patterns:

        match = re.search(pattern, response_text, re.DOTALL)

        if match:

            candidate = match.group(1).strip()

            try:
                return json.loads(candidate)

            except:
                continue

    return None


# Basic validation.
def validate_output(parsed_output):

    if parsed_output is None:
        return False

    if isinstance(parsed_output, (dict, list)):
        return True

    return False


# Save output JSON.
def save_output(filename, data):

    Path(filename).parent.mkdir( parents=True, exist_ok=True)

    existing_data = []

    # Load existing data if file exists
    if Path(filename).exists():

        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except:
            existing_data = []

    # Ensure list structure
    if not isinstance(existing_data, list):
        existing_data = [existing_data]

    # Remove duplicate case if rerunning
    existing_data = [
        item for item in existing_data
        if item.get("case_name") != data.get("case_name")
    ]

    # Append new result
    existing_data.append(data)

    # Save updated list
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)