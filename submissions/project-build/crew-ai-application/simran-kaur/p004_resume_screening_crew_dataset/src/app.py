
from crew import run_crew

try:
    query = input("\nQuestion: ")

    if query.lower() == "exit":
        break

    response = run_crew.kickoff(query)

    print(response)


except Exception as e:
    print("ERROR:", e)
