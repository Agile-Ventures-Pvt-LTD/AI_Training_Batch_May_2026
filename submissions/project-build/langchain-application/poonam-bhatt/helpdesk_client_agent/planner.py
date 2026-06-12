def create_plan(user_query):

    return {
        "user_goal": user_query,
        "required_tools": [],
        "reasoning":
        "Determine required data before answering."
    }