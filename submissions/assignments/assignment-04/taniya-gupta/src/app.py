import sys

MODE = sys.argv[1].lower() if len(sys.argv) > 1 else "modern"

if MODE == "legacy":
    from src.agents.legacy_agent import agent
else:
    from src.agents.modern_agent import agent

print(f"Running in {MODE} mode")
print("Type 'exit' to quit")

while True:
    question = input("\nAsk a question: ")

    if question.strip().lower() in ["exit", "quit"]:
        break

    
    if MODE == "legacy":

            response = agent.invoke(
                {"input": question}
            )

            print("\nAnswer:")
            print(response["output"])

    else:

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
            print(response["messages"][-1].content)
