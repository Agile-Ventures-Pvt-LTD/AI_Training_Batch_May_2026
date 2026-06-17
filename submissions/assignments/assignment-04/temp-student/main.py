from src.agents.modern_agent import agent

print("=" * 60)
print("E-Commerce AI Agent")
print("=" * 60)

while True:

    user_query = input("\nAsk Question: ")

    if user_query.lower() == "exit":
        break

    try:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_query
                    }
                ]
            }
        )

        print("\nAnswer:")

        print(
            response["messages"][-1].content
        )

    except Exception as e:
        print("Error:", e)