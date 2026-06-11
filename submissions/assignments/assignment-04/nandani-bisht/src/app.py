import langchain
def main():

    version = langchain.__version__

    print(f"\nLangChain Version: {version}")

    if version.startswith("0."):

        from src.agents.legacy_agent import (
            create_legacy_ecommerce_agent
        )

        agent = create_legacy_ecommerce_agent()

        while True:

            user_query = input(
                "\nAsk a question: "
            )

            if user_query.lower() == "exit":
                break

            response = agent.run(user_query)

            print("\nAnswer:")
            print(response)

    else:

        from src.agents.modern_agent import (
            create_ecommerce_agent
        )

        agent = create_ecommerce_agent()

        while True:

            user_query = input(
                "\nAsk a question "
            )

            if user_query.lower() == "exit":
                break

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
            print(response["messages"][-1].content)


if __name__ == "__main__":
    main()