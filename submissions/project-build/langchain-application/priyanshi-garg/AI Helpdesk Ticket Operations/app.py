import json
import os

from agent import run_agent

# ensure output folder exists
os.makedirs("outputs", exist_ok=True)

output_file = os.path.join("outputs", "outputs.json")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    result = run_agent(user_input)

    print("\nAgent:")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # append result safely as JSONL style (better than broken JSON file)
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False))
        f.write("\n")