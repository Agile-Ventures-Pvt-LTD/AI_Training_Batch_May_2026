import os
from prebuilt_agent import invoke
from custom_agent import run_custom_agent

questions = [
    "Show me the database schema.",
    "Show customer profile for customer with id 1.",
    "Show card details for customer with id 1.",
    "Show the last 5 transactions for customer with id 1.",
    "Which customers have the highest amount due?",
    "Show statement summary for customer with id 1.",
    "Which merchant type has the highest total spend?",
    "Show reward points for customer with id 1.",
    "Identify potentially suspicious transactions."
]

os.makedirs("outputs", exist_ok=True)
output_file = "outputs/sample_prebuilt_agent_run.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for i, question in enumerate(questions, start=1):
        print(f"Running Test {i}: {question}")
        f.write(f"Test {i}\n")
        f.write(f"Question: {question}\n")

        try:
            response = invoke(question)
            f.write("Response:\n")
            f.write(str(response))
            f.write("\n\n")

        except Exception as e:
            f.write("Error:\n")
            f.write(str(e))
            f.write("\n")

print(f"All outputs saved to {output_file}")

output_file = "outputs/sample_custom_agent_run.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for i, question in enumerate(questions, start=1):
        print(f"Running Test {i}: {question}")
        f.write(f"Test {i}\n")
        f.write(f"Question: {question}\n")

        try:
            response = run_custom_agent(question)

            f.write("Response:\n")
            f.write(f"Answer:\n{response['answer']}\n\n")
            f.write(f"Tools Used:\n{response['tools_used']}\n\n")
            f.write(f"Reflection:\n{response['reflection']}\n\n")

        except Exception as e:
            f.write("Error:\n")
            f.write(str(e))
            f.write("\n")

print(f"All outputs saved to {output_file}")