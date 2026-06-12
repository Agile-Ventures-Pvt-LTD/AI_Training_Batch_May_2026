def reflect(tool_output):

    return {
        "tool_result_available":
        bool(tool_output),

        "answer_complete":
        bool(tool_output),

        "missing_information":
        [],

        "risk":
        "No obvious risk detected."
    }