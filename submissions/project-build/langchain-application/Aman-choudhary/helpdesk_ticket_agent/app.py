from agent import agent
print("Helpdesk Agent Started")
while True:
    query = input("You: ")
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