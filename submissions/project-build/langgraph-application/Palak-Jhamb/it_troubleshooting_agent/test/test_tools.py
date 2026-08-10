import os
from prebuilt_agent import invoke


questions = [
    "Amit says VPN times out after MFA approval. What should we check and what is the next action?",
    "Priya's laptop is very slow after startup. Diagnose the likely issue.",
    " David cannot login and password reset email is not received. What should be done?",
    "Sara's VPN disconnects frequently. What is the likely reason?",
    "Outlook is not syncing for Emily but webmail works. What is the next step?",
    "Which active known incidents may affect VPN users?",
    "Create a ticket summary for Rahul's laptop performance issue.",
    "My email is slow. Fix it."
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

