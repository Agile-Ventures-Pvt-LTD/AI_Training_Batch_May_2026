from src.agents.legacy_agent import agent

print("=" * 60)
print("E-Commerce AI Agent (Legacy LangChain)")
print("Type 'exit' to quit")
print("=" * 60)

while True:

    question = input("\nAsk Question: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    try:
        response = agent.run(question)

        print("\nAnswer:")
        print(response)

    except Exception as e:
        print("\nError:")
        print(str(e))