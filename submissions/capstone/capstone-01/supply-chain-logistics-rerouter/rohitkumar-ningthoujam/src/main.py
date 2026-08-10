import sys
from src.graph import graph_agent
def run_agent():
    """Run agent interactively and output structured responses."""
   
    print("\n LangGraph  Agent")
    print("Type 'exit' to quit.\n")
    while True:
        question = input("User: ").strip()
        if question.lower() == "exit":
            break
        result = graph_agent.invoke({"messages": [("user", question)]})
        return result
    

def main():
    print("Supply  chain agent runing")
    return run_agent()



