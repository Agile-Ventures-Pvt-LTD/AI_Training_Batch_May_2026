import json
import os

from prebuilt_agent import invoke

questions = [
    "Show me the database schema.",
    "Show customer profile for customer with id 1..",
    "Show card details for customer with id 1..",
    "Show the last 5 transactions for customer with id 1..",
    "Which customers have the highest amount due?",
    "Show statement summary for customer with id 1..",
    "Which merchant type has the highest total spend?",
    "Show reward points for customer with id 1.",
    "Identify potentially suspicious transactions."
]

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

for i, question in enumerate(questions, start=1):
    print(f"Running Test {i}: {question}")
    try:
        response = invoke(question)
        result = {
            "question": question,
            "response": str(response)
        }
    except Exception as e:
        result = {
            "question": question,
            "error": str(e)
        }

    file_path = os.path.join(
        output_dir,
        f"test_{i}.json"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result,f,indent=4, ensure_ascii=False)

print("All outputs saved successfully.")