import json

from agent import run_agent_with_response
from output_formatter import save_runtime_output


def main():
    print("Helpdesk agent is ready. Type exit to quit.")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            break

        if not question:
            continue

        try:
            answer, agent_response = run_agent_with_response(question)
            saved_output = save_runtime_output(question, answer, agent_response)
            print("Agent:", json.dumps(saved_output, indent=2))
        except Exception as error:
            saved_output = save_runtime_output(question, "", error=error)
            print("Error:", json.dumps(saved_output, indent=2))


if __name__ == "__main__":
    main()


# Run in PowerShell:
# .\.venv\Scripts\python.exe app.py
