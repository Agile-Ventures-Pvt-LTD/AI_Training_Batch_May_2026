import os
import json
from langchain_core.messages import HumanMessage

from loaders import load_documents
from chunking import chunk_documents, create_vector_store, load_vector_store
from output_parser import parse_final_rag_output, safe_parse
from config import POLICY_DATA_PATH
from prebuilt_agent import agent

OUTPUT_FILE_PATH = "outputs/evauation_results.json"

def build_index():
    print("\nLoading Documents...")
    docs = load_documents(POLICY_DATA_PATH)

    if not docs:
        raise ValueError("No documents found to parse or index.")

    print(f"Loaded {len(docs)} pages.")
    print("\nChunking...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks.")

    print("\nCreating Vector Store...")
    create_vector_store(chunks)
    print("Index Built Successfully.")

def save_output(output_file: str, user_query: str, agent_response: str):
    dir_name = os.path.dirname(output_file)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    default_structure = {
        "answer": agent_response,
        "policy_basis": [],
        "sources": [],
        "answerability": "ERROR_OR_UNPARSED",
        "confidence": "LOW",
        "recommended_next_step": "Review agent execution traces manually."
    }

    parsed_json_payload = safe_parse(parse_final_rag_output, agent_response, default_value=default_structure)

    log_entry = {"user_query": user_query,"parsed_output": parsed_json_payload}

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
    print("\nEnterprise Policy Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Ask a policy question: ").strip()

        if not question:
            print("Please enter a question.\n")
            continue

        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            config = {"recursion_limit": 100}

            response = agent.invoke(
                {"messages": [HumanMessage(content=question)]},
                config=config
            )

            print("\n" + "=" * 80)
            final_response = response["messages"][-1].content
            print(final_response)
            print("=" * 80 + "\n")
            
            save_output(OUTPUT_FILE_PATH, question, final_response)
            print(f"-> Successfully log compiled to: {OUTPUT_FILE_PATH}\n")

        except Exception as e:
            print(f"\nError while processing request: {e}\n")


if __name__ == "__main__":
    print("\nAI Knowledge Assistant CLI Menu Options")
    print("1. Build Index")
    print("2. Ask Questions (Run Assistant)")
    
    choice = input("\nEnter Choice (1 or 2): ").strip()

    if choice == "1":
        build_index()
    elif choice == "2":
        run_interactive_assistant()
    else:
        print("Invalid choice specified. Exiting process pipeline application.")
