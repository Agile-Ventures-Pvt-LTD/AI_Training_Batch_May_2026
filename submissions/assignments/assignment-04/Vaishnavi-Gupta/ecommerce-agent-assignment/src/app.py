from agents.modern_agent import build_agent
agent = build_agent()

print("Ecommerce Agent Started")

while True:
    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )

    print("\nAnswer:")
    print(response["messages"][-1].content)