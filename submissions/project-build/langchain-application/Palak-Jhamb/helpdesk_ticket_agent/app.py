from agent import invoke

while True:
    query = input("\nUser: ")

    if query.lower() in ["exit", "quit"]:
        break

    response = invoke(query)

    print("\nAssistant:", response)



