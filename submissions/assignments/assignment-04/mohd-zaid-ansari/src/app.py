from agents.legacy_agent import answer_business_question
while True:
    question = input("\nAsk a business question (or type exit): ")
    if question.lower() == "exit":
        break
    answer = answer_business_question(question)
    print("\nAnswer:")
    print(answer)