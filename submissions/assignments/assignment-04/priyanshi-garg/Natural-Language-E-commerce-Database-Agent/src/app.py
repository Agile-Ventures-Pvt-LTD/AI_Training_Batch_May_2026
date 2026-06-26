
from src.logger import write_log
from src.agents.modern_agent import (
    create_modern_agent
)

agent = create_modern_agent()

print("Ecommerce Agent Ready")
print("Type exit to quit")



while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break
        

    try:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )

        print("\nAnswer:")

        print(
            response["messages"][-1].content
        )

    except Exception as e:

        print(f"\nError: {e}")