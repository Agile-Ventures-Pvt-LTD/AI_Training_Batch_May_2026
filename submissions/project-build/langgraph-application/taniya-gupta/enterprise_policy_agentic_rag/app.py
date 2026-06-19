import json
from graph import run_agent
from config import config
from tools import get_vector_store

get_vector_store()
print("Vectors are loaded")
print("The enterprise policy agent, to exit the loop type 'exit'")
while True:
    try:
        query=input("Ask your question:").strip()
        if query in ['exit']:
            break
        response=run_agent(query)
        print("\nResponse:")
        print(json.dumps(response, indent=2))
    except KeyboardInterrupt:
            print("\nExiting. Goodbye!")
            break