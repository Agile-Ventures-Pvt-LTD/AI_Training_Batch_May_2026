from graph import graph


def run_agent(user_query: str) -> str:
    state = {
        "user_query": user_query,
        "issue_type": "",
        "user_identifier": None,
        "retrieved_guidance": [],
        "user_profile": {},
        "device_status": {},
        "known_incidents": [],
        "diagnostic_snapshot": {},
        "resolution_plan": {},
        "safety_review": {},
        "final_response": "",
    }

    result = graph.invoke(state)
    return result.get("final_response", "")


if __name__ == "__main__":
    print("Enter your IT troubleshooting request:")
    query = input().strip()

    if query:
        print("\n--- Response ---\n")
        print(run_agent(query))
    else:
        print("No query provided.")
