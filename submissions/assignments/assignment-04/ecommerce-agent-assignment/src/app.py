from src.agents.modern_agent import run_agent


def main():

    print("E-Commerce Database Agent")

    while True:

        user_input = input("\nAsk a question: ")

        if user_input.lower() in [
            "exit",
            "quit"
        ]:
            break

        response = run_agent(
            user_input
        )

        print("\nResponse:")
        print(response)


if __name__ == "__main__":
    main()