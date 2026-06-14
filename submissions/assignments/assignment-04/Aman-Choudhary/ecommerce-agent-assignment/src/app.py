from src.agents.modern_agent import agent

import json
from datetime import datetime
from pathlib import Path

# Create logs folder automatically
Path("logs").mkdir(parents=True, exist_ok=True)

LOG_FILE = "logs/chat_history.json"


def save_chat(
    user_query,
    generated_sql,
    raw_result,
    response_text,
):
    """
    Save chat history in JSON format
    """

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_query": user_query,
            "generated_sql": generated_sql,
            "raw_result": raw_result,
            "response": response_text,
        }
    )

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():

    print("E-commerce Agent Started")
    print("Type 'exit' to quit")

    while True:

        user_query = input("\nAsk Question: ")

        if user_query.lower().strip() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:

            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_query,
                        }
                    ]
                }
            )

            messages = response["messages"]

            generated_sql = None
            raw_result = None

            for msg in messages:

                # Extract SQL query from tool call
                if hasattr(msg, "tool_calls") and msg.tool_calls:

                    try:
                        generated_sql = msg.tool_calls[0]["args"].get(
                            "query"
                        )
                    except Exception:
                        pass

                # Extract tool output
                if msg.__class__.__name__ == "ToolMessage":
                    raw_result = msg.content

            final_answer = messages[-1].content

            print("\nResponse:")
            print(final_answer)

            save_chat(
                user_query=user_query,
                generated_sql=generated_sql,
                raw_result=raw_result,
                response_text=final_answer,
            )

        except Exception as e:
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()