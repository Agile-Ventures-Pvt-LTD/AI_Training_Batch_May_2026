
import json


def parse_json_response(response_text):

    response_text = response_text.strip()

    # Remove markdown json fences if present
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json","",1)
    elif response_text.startswith("```"):
        response_text = response_text.replace("```", "", 1)
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except Exception:
        raise ValueError(
            "Invalid JSON returned by model."
        )