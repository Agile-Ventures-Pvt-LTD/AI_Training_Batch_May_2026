from src.agents.legacy_agent import (
    create_legacy_agent
)

agent = create_legacy_agent()

print("Legacy Ecommerce Agent Ready")
print("Type exit to quit")

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    try:

        response = agent.run(question)

        print("\nAnswer:")
        print(response)

    except Exception as e:

        print("\nError:")
        print(e)