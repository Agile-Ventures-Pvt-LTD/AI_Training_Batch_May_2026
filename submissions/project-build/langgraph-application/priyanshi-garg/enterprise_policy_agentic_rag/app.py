from graph import build_policy_assistant_graph
from tools import PolicyAgentState
from store import db 

def run_policy_assistant(user_query: str):
    graph = build_policy_assistant_graph()

    initial_state = PolicyAgentState(
        query=user_query,
        vectorstore=db
    )

    result = graph.invoke(initial_state)
    return result.final_answer

if __name__ == "__main__":
    q = input("Ask your policy question: ")
    print(run_policy_assistant(q))