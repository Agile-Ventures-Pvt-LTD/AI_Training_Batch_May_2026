import json


def parse_json_response(response_text):

    try:
        response_text = (response_text.replace("```json","").replace("```","").strip())

        return json.loads(response_text)

    except Exception:
        return {
            "answer":
            "Unable to parse model response.",

            "supporting_evidence": [],

            "sources": [],

            "confidence": "LOW",

            "answerability":
            "NOT_FOUND"
        }