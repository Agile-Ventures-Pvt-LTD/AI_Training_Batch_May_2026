import os
import json
from langchain_core.messages import HumanMessage
from loaders import load_documents, chunk_documents, create_vector_store
from output_parser import clean_and_parse_json
from config import KB_PATH
from prebuilt_agent import agent_executor

OUTPUT_FILE_PATH = "outputs/evaluation_results.json"

def build_index():
    docs = load_documents(KB_PATH)
    if not docs:
        raise ValueError(f"No documents found to parse or index inside: {KB_PATH}")
    chunks = chunk_documents(docs)
    create_vector_store(chunks)
    print("Index Built Successfully.")

def save_output(output_file: str, user_query: str, agent_response: str):
    dir_name = os.path.dirname(output_file)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    parsed_json = clean_and_parse_json(agent_response)
    
    if not parsed_json:
        parsed_json = {
            "raw_text_answer": agent_response,
            "status": "Unstructured_Reply"
        }

    log_entry = {
        "user_query": user_query,
        "parsed_output": parsed_json
    }

    history_records = []
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    history_records = json.loads(content)
                    if not isinstance(history_records, list):
                        history_records = [history_records]
        except Exception:
            history_records = []

    history_records.append(log_entry)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(history_records, f, indent=4, ensure_ascii=False)

def run_interactive_assistant():
    agent = agent_executor
    print("Enterprise IT Troubleshooting Assistant")
    print("Type 'exit' to quit.")

    while True:
        question = input(" Ask question: ").strip()

        if not question:
            print("Please enter a valid query string.\n")
            continue

        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            response = agent.invoke({"input": question})
            final_response = response.get("output", str(response))
            print(final_response)
            save_output(OUTPUT_FILE_PATH, question, final_response)
            print(f"Successfully logged compiled : {OUTPUT_FILE_PATH}\n")

        except Exception as e:
            print(f"\n Error while processing request : {e}\n")


if __name__ == "__main__":
    print("\nAI Knowledge Assistant CLI Menu Options")
    print("1. Build Index")
    print("2. Ask Questions ")
    
    choice = input("\nEnter Choice 1/2: ").strip()

    if choice == "1":
        build_index()
    elif choice == "2":
        run_interactive_assistant()
    else:
        print("Invalid choice specified. Choose the exist one.")
