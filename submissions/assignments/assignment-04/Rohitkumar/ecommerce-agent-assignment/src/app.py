import os
from dotenv import load_dotenv

load_dotenv()

mode = input("Choose mode (legacy/modern): ").strip().lower()

if mode == "legacy":
    from src.agents.legacy_agent import create_legacy_agent
    agent = create_legacy_agent()
    use_run = True
else:
    from src.agents.modern_agent import create_agent
    agent = create_agent()
    use_run = False

while True:
    user_input = input("Ask: ")

    if user_input.lower() == "exit":
        break

    if use_run:
        response = agent.run(user_input)
        print("Answer:", response)
    else:
        response = agent.invoke({"input": user_input})
        print("Answer:", response["output"])