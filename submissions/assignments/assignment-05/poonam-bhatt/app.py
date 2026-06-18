from prebuilt_agent import agent
from custom_react_agent import compiled_graph
from prompts import SYSTEM_PROMPT

from groq import RateLimitError

while True:
    query = input("\nAsk Question: ")

    if query.lower().strip() in [
        "exit",
        "quit",
        "bye",
        "stop"
    ]:
        print("\nExiting CCMS Agent...")
        break

    # for prebuilt_agent(prebuilt_agent.py)

    # response = agent.invoke(
    #     {
    #         "messages": [
    #             ("user", query)
    #             ]
    #     },
    #             config={
    #                 "recursion_limit": 5
    #                 }
    # )

    # for custom react agent(Custom_react_agent.py)

    response = compiled_graph.invoke(
        {
            "messages": [
                ("user", query)
            ]
        }
    )

    print(
        "\nAnswer:\n",
        response["messages"][-1].content
    )

    