from src.agents.modern_agent import agent


def ask(question: str):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    return result["messages"][-1].content


if __name__ == "__main__":

    print("=" * 60)
    print("Modern E-Commerce Agent (LangGraph)")
    print("=" * 60)

    while True:

        query = input("\nQuestion: ")

        if query.lower() in ["exit", "quit"]:
            break

        try:

            answer = ask(query)

            print("\nAnswer:")
            print(answer)

        except Exception as e:

            print(f"\nError: {e}")