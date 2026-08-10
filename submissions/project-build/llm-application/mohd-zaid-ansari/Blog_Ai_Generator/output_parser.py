import json

def parse_json(response):

    try:
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        return json.loads(response)

    except Exception as e:
        return {
            "error": "Invalid JSON returned",
            "raw_response": response
        }