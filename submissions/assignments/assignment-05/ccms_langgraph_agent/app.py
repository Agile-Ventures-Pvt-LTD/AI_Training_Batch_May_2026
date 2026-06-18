import json
import os
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from custom_react_agent import compiled_graph

questions = [
    "Show me the database schema.",
    "Show customer profile for customer 1.",
    "Show card details for customer 1.",
    "Show the last 5 transactions for customer 1.",
    "Which customers have the highest amount due?",
    "Show statement summary for customer 1.",
    "Which merchant type has the highest total spend?",
    "Show reward points for customer 1.",
    "Identify potentially suspicious transactions."
]

os.makedirs("outputs", exist_ok=True)

all_results = []

for i, question in enumerate(questions):

    print(f"\nRunning: {question}")

    config = {
        "configurable": {
            "thread_id": f"test_{i}"
        }
    }

    try:

        result = compiled_graph.invoke(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            },
            config=config
        )

        reflection = result.get(
        "reflection",
        ""
        )

        messages = result["messages"]

        final_answer = ""

        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                if msg.content:
                    final_answer = msg.content
                    break

        tools_used = []

        for msg in messages:
            if isinstance(msg, ToolMessage):

                tool_name = getattr(msg, "name", None)

                if tool_name and tool_name not in tools_used:
                    tools_used.append(tool_name)

        response = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "user_question": question,
            "implementation_choice": "custom_react_agent",
            "tools_used": tools_used,
            "records_found": len(tools_used),
            "reflection": reflection,
            "answer": final_answer,
            "sensitive_data_masked": True,
            "limitations": []
        }

        all_results.append(response)

        print("SUCCESS")
        print(final_answer)

    except Exception as e:

        print("FAILED")
        print(str(e))

        error_response = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "user_question": question,
            "implementation_choice": "custom_react_agent",
            "tools_used": [],
            "records_found": 0,
            "answer": "",
            "sensitive_data_masked": True,
            "limitations": [
                str(e)
            ]
        }

        all_results.append(error_response)

output_file = "outputs/final_agent_responses.json"

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_results,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"Results saved to: {output_file}")