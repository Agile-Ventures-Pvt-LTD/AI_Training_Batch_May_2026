import os
import json
import uuid
from prebuilt_agent import prebuilt_agent


def save_output(question: str, result, out_dir: str = "outputs") -> str:
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.json"
    path = os.path.join(out_dir, filename)
    payload = {
        "question": question,
        "result": result
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Saved output to: {path}")
    return path


def main():
    print("Credit Card Management AI Agent - simple runner")
    question = input("Enter your question: ")
    result = prebuilt_agent(question)
    print("\nResponse:\n", result)
    save_output(question, result)


if __name__ == "__main__":
    main()
