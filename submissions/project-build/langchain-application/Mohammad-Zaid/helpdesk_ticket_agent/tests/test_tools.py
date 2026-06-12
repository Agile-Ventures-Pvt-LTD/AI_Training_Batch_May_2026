# tests/test_tools.py

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import json

from app import chat


test_prompts = [

    "Show me all open high-priority tickets.",

    "Which tickets are overdue?",

    "Which tickets should I work on first today?",

    "Summarize ticket TCK-00077.",

    "Add a comment to TCK-00001 saying billing team is reviewing the duplicate invoice.",

    "Update TCK-00001 status to In Progress.",

    "Remember that I want to prioritize enterprise customer issues first.",

    "Based on my preference, which tickets should I handle first?",

    "What did we discuss earlier about billing tickets?",

    "Summarize this conversation and store it in memory."
]


results = []

for prompt in test_prompts:

    print(f"\nRunning: {prompt}")

    response = chat(prompt)

    results.append(
        {
            "prompt": prompt,
            "response": response
        }
    )


with open(
    "outputs/evaluation_outputs.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )


print("\nEvaluation completed.")
print("Results saved to outputs/evaluation_outputs.json")