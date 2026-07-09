import json

def parse_json(response):
    try:
        return json.loads(response)

    except Exception:

        return {
            "error": "Invalid JSON",
            "raw_output": response
        }