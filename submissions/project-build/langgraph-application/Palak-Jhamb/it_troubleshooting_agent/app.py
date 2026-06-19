from prebuilt_agent import invoke

while True:
    query = input("\nUser: ")
    if query.lower() in ["exit", "quit"]:
        break
#try except to handle exceptions
    try:
        response = invoke(query)
        print("\nAssistant:", response)

    except Exception as e:
        print(f"\nError: {e}")

