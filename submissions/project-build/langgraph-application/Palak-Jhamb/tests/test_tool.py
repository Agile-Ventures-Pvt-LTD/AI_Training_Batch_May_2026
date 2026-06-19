import os

from custom_agent import run_custom_agent

questions = [
    'How many annual leave days can an employee carry forward?', 
    'Can I claim meals for same-day domestic business travel?', 
    'What documents are needed for hotel reimbursement?', 
    'Can I use my personal laptop for office work?', 
    'What approvals are needed for international travel?',
    'Can customer data be uploaded to a public AI tool?', 
    'Will my reimbursement definitely be approved?',
    'What should I do if the policy does not mention my scenario?'
]

os.makedirs("outputs", exist_ok=True)
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