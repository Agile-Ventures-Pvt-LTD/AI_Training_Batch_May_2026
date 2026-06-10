from src.agents.modern_agent import invoke


while True:

    question = input("\nUser: ")

    if question.lower() in ["exit", "quit"]:
        break

    answer = invoke(question)

    print("\nAssistant:")
    print(answer)
