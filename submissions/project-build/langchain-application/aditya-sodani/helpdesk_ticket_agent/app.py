from agent import agent

print("\nHelpdesk Agent Started\n")

while True:

    query = input("User: ")

    if query.lower() in [
        "exit",
        "quit"
    ]:
        break

    try:

        response = agent.invoke(
            {
                "input": query
            }
        )

        print("\nAgent:")
        print(response["output"])

    except Exception as e:

        print("\nERROR:")
        print(str(e))