from graph import run_custom_agent
from src.rag import create_faiss_db
create_faiss_db()
while True:
    print("enter 1 for INC-001, 2 for INC-002, 3 for INC-003 ")
    query = int(input("\n select 1 / 2 /3: "))
    if query.lower() in ["exit", "quit"]:
        break

    try:    
        response = run_custom_agent(query)
        print("\nAssistant:", response)

    except Exception as e:
        print(f"\nError: {e}")