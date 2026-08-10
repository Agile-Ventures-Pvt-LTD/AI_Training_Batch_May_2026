from custom_agent import run_custom_agent

while True:
    query = input("\nUser: ")
    if query.lower() in ["exit", "quit"]:
        break
#try except to handle exceptions
    try:
        response = run_custom_agent(query)
        # final_response = response["messages"][-1].content
        print("\nAssistant:", response)

    except Exception as e:
        print(f"\nError: {e}")