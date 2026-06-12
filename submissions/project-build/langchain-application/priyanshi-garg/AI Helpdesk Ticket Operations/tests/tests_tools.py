from agent import run_agent

test_cases = [
    "Show me all open high-priority tickets.",
    "Which tickets are overdue?",
    "Which tickets should I work on first today?",
    "Summarize ticket TCK-1003.",
    "Remember that I want to prioritize enterprise customer issues first.",
    "Based on my preference, which tickets should I handle first?"
]

for test in test_cases:

    print("\n" + "="*50)
    print("TEST:", test)

    response = run_agent(test)

    print("RESPONSE:")
    print(response)