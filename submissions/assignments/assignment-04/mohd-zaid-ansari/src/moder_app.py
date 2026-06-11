from agents.modern_agent import answer_business_question

question = input("Ask a question: ")

response = answer_business_question(question)

print("Generated SQL:")
print(response["sql"])

print("Database Result:")
print(response["result"])

print("Final Answer:")
print(response["answer"])