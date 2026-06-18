from langchain_core.messages import HumanMessage

print("Choose Agent")
print("1. Prebuilt ReAct Agent")
print("2. Custom ReAct Agent")

choice = input("Enter choice (1 or 2): ")

if choice == "1":
    from prebuilt_agent import agent

elif choice == "2":
    from custom_react_agent import custom_agent

else:
    print("Invalid Choice")
    exit()


while True:

    user_input = input("\nAsk Question (type exit to quit): ")

    if user_input.lower() == "exit":
        break

    try:

        if choice == "1":

            response = agent.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                }
            )

        else:

            response = custom_agent.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                }
            )

        print("\nAnswer:")
        print(response["messages"][-1].content)

    except Exception as e:
        print(f"Error : {e}")