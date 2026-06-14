from src.agents.legacy_agent import agent

import json
from datetime import datetime
from pathlib import Path

Path("logs").mkdir(parents=True, exist_ok=True)

LOG_FILE = "logs/chat_history_legacy.json"


def save_chat(
    user_query,
    response_text,
):
    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

    except (
        FileNotFoundError,
        json.JSONDecodeError,
    ):
        data = []

    data.append(
        {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "user_query": user_query,
            "response": response_text,
        }
    )

    with open(
        LOG_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )


def main():

    print("=" * 60)
    print("E-Commerce Agent (LangChain 0.3.27)")
    print("Type 'exit' to quit")
    print("=" * 60)

    while True:

        user_query = input("\nAsk Question: ")

        if user_query.lower().strip() in [
            "exit",
            "quit",
        ]:
            print("Goodbye!")
            break

        try:

            response = agent.invoke(
                {
                    "input": user_query,
                }
            )

            print("\n")
            print("=" * 60)
            print("FULL RESPONSE OBJECT")
            print("=" * 60)

            print(response)

            print("\n")
            print("=" * 60)
            print("RESPONSE TYPE")
            print("=" * 60)

            print(type(response))

            if isinstance(response, dict):

                print("\n")
                print("=" * 60)
                print("RESPONSE KEYS")
                print("=" * 60)

                print(response.keys())

            # Try all common output keys
            final_answer = None

            if isinstance(response, dict):

                if "output" in response:
                    final_answer = response["output"]

                elif "answer" in response:
                    final_answer = response["answer"]

                elif "result" in response:
                    final_answer = response["result"]

                else:
                    final_answer = str(response)

            else:
                final_answer = str(response)

            print("\n")
            print("=" * 60)
            print("FINAL ANSWER")
            print("=" * 60)

            print(final_answer)

            save_chat(
                user_query=user_query,
                response_text=final_answer,
            )

        except Exception as e:

            print("\n")
            print("=" * 60)
            print("ERROR")
            print("=" * 60)

            print(str(e))


if __name__ == "__main__":
    main()