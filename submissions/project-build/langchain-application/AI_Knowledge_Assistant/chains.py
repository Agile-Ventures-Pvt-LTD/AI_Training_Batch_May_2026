import os 
from pathlib import Path
from groq_client import run_case, build_prompt
from output_parser import parse_json_response
from prompts import (
    system_message,
    user_message_template,
    classification_system_message,
    classification_user_template,
)


def classify_query(question: str) -> dict:
    messages = build_prompt(classification_system_message, question)
    raw = run_case(messages)
    return parse_json_response(raw)


def respond(question: str, retriever) -> dict:
    
    classification = classify_query(question)
    print(f"Query type: {classification.get('query_type')}")

    docs = retriever.invoke(question)
    context = "\n---\n".join([d.page_content for d in docs])

    messages = build_prompt(system_message, question, context=context)
    raw = run_case(messages)

    
    try:
        result = parse_json_response(raw)
    except ValueError:
        result = {"answer": raw, "answerability": "UNKNOWN"}

    result["query_type"] = classification.get("query_type")
    result["retrieval_debug"] = [
        {
            "chunk_id": d.metadata.get("chunk_id"),
            "source_file": d.metadata.get("source_file"),
            "page": d.metadata.get("page"),
            "preview": d.page_content[:200],
        }
        for d in docs
    ]

    return result


def print_result(result: dict):
    print(f"\nAnswer: {result.get('answer')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Answerability: {result.get('answerability')}")
    print(f"Query Type: {result.get('query_type')}")
    print("\n Retrieved Chunks:")
    for chunk in result.get("retrieval_debug", []):
        print(f"  {chunk['chunk_id']} | {chunk['source_file']} | page {chunk['page']}")
        print(f"  Preview: {chunk['preview']}\n")

def main(retriever):
    while True:
        question = input("User (type q to quit): ")
        if question == "q":
            break
        result = respond(question, retriever)
        print_result(result)