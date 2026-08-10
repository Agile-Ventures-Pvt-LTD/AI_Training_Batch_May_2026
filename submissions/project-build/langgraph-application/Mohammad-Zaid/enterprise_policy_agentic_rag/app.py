# file: app.py
import json
import os

from prebuilt_agent import ask_agent

def extract_source(answer):

    answer = str(answer)

    if ".md" in answer:

        words = answer.split()

        for word in words:
            if word.endswith(".md"):
                return word

    return "Not Available"

def save_result(question, answer):

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/evaluation_results.json"

    data = []

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []

    data.append({
    "question": question,
    "answer": answer,
    "source": extract_source(answer)
    })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
        
def main():

    print("\nEnterprise Policy Assistant")
    print("Type 'exit' to quit\n")

    while True:

        question = input("Question: ")

        if question.lower() == "exit":
            break

        try:
            answer = ask_agent(question)

            print("\nAnswer:")
            print(answer)
            save_result(question, answer)

        except Exception as e:
            print("\nError:", e)


if __name__ == "__main__":
    main()