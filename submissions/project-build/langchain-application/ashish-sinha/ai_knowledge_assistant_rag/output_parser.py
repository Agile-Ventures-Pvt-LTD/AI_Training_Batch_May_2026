import json

def parse_output(response):

    try:
        return json.loads(response)

    except Exception:

        return {
            "answer": response,
            "supporting_evidence": [],
            "sources": [],
            "confidence": "LOW",
            "answerability": "NOT_FOUND"
        }