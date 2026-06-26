from src.agents.legacy_agent import EcommerceAgent


def main():

    agent = EcommerceAgent()

    print("\nEcommerce AI Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        user_query = input("Question: ")

        if user_query.lower() == "exit":
            break

        try:

            response = agent.run(
                user_query
            )

            print("\nAnswer:\n")
            print(
                response["final_answer"]
            )

        except Exception as e:

            print(
                f"\nError: {str(e)}"
            )


if __name__ == "__main__":
    main()