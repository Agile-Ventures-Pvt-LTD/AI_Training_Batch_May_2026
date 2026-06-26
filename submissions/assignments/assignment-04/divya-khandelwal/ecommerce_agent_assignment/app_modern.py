from src.agents.modern_agent import (
    ModernEcommerceAgent
)


def main():

    agent = ModernEcommerceAgent()

    print(
        "\nModern LangChain Agent"
    )

    print(
        "Type 'exit' to quit"
    )

    while True:

        question = input(
            "\nQuestion: "
        )

        if question.lower() == "exit":

            break

        try:

            result = agent.run(
                question
            )

            print("\nAnswer:\n")

            print(
                result["messages"][-1].content
            )

        except Exception as e:

            print(
                f"\nError: {e}"
            )


if __name__ == "__main__":
    main()