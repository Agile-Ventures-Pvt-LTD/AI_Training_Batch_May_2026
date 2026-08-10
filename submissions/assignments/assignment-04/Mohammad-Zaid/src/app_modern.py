from src.agents.modern_agent import ask_agent

print("=" * 60)
print("Modern E-Commerce SQL Agent")
print("Type 'exit' to quit")
print("=" * 60)

while True:

    question = input("\nQuestion: ")

    if question.lower() in ["exit", "quit"]:
        break

    sql_query, answer = ask_agent(question)

    print("\nSQL Query:")
    print(sql_query)

    print("\nResponse:")
    print(answer)