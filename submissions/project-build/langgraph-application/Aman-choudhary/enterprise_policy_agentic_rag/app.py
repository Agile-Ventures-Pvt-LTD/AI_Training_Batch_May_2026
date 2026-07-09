import json
import os

from graph import workflow
from loaders import load_documents
from chunking import chunk_documents
from retrievers import vector_store
from config import POLICY_DATA_PATH


# Load and index documents
docs = load_documents(POLICY_DATA_PATH)
chunks = chunk_documents(docs)
vector_store.create_vector_store(chunks)

print("Policy Path:", os.path.exists("data/policies"))
print("Vector Store Path:", os.path.exists("vector_store"))

if os.path.exists("vector_store"):
    print("Vector Store Files:", os.listdir("vector_store"))


def ask_question(question: str):
    state = {
        "user_question": question,
        "query_type": "",
        "required_policy_domains": [],
        "requires_clarification": False,
        "rewritten_query": None,
        "retrieved_context": [],
        "context_grade": {},
        "answer": {},
        "reflection": {},
        "retry_count": 0,
        "final_response": {}
    }

    result = workflow.invoke(state)
    return result.get("final_response")


def save_output(question, response):
    """
    Save all questions and responses to outputs/evaluation_results.json
    """

    os.makedirs("outputs", exist_ok=True)

    output_file = "outputs/evaluation_results.json"

    # Load existing data if file exists
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = []
    else:
        data = []

    # Append new result
    data.append({
        "question": question,
        "response": response
    })

    # Save updated results
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"\nOutput saved to {output_file}")


def main():
    print("\nEnterprise Policy Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            response = ask_question(question)

            print("\nResponse:\n")
            print(response)

            # Save question and response
            save_output(question, response)

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()