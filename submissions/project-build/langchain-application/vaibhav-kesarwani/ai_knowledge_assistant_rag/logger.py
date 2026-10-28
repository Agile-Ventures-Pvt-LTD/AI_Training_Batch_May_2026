import os
import json
from groq_client import call_groq
from prompts import system_query_logging, user_query_logging

def query_logging(question: str, query_type: dict, retrieved_sources: list, response : dict):
    """This function will logg the query in the json file"""
    
    LOG_FILE = "logs/query_logs.json"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    prompt = [
        {"role" : "system", "content" : system_query_logging},
        {"role" : "user", "content" : user_query_logging.format(
            question=question,
            query_type=query_type,
            sources=retrieved_sources, 
            response=response,
        )}
    ]

    response = call_groq(prompt=prompt)

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(json.loads(response))

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
        print("Query logged Successfully")