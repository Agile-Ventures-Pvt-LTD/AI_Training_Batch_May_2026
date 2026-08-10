try:
    from pathlib import Path
    from agents.agent import ask_agent, get_tools_used
except ModuleNotFoundError as e:
    print(f"Error: {e}")


def main():

    print("IT Support Agent")
    print("Type 'exit' to quit.\n")

    while True:

        query = input("User: ")

        if query.lower() == "exit":
            break

        try:

            response = ask_agent(query)

            answer = response["messages"][-1].content

            print("\nAssistant:")
            print(answer)

        except Exception as e:

            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()