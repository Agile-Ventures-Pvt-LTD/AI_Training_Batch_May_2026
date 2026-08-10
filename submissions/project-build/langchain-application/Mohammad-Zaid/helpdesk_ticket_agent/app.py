# app.py

import json

from agent import agent_executor
from memory import save_conversation
from output_formatter import format_response


def chat(query):

    response = agent_executor.invoke(
        {
            "input": query
        }
    )

    answer = response["output"]

    save_conversation.invoke(
        {
            "user_message": query,
            "agent_response": answer
        }
    )

    formatted_response = format_response(
        user_request=query,
        final_answer=answer
    )

    with open(
        "outputs/sample_agent_run.txt", "a", encoding="utf-8") as f:

        f.write(
            json.dumps(formatted_response, indent=2))

        f.write("\n\n")

    return formatted_response


if __name__ == "__main__":

    while True:
        query = input("\nUser: ")
        if query.lower() == "exit":
            break

        print("\nAgent:")

        response = chat(query)

        print(json.dumps(response, indent=2))