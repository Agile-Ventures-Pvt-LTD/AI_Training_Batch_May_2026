# file: output_parser.py

import json

def parse_output(text):
    try:
        return json.loads(text)
    except:
        return {
            "answer": text,
            "policy_basis": [],
            "sources": [],
            "confidence": "LOW"
        }