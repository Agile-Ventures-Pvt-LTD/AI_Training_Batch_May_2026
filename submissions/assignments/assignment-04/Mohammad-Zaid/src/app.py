from src.agents.legacy_agent import (
    agent_executor
)


def extract_sql_query(intermediate_steps):
    """
    Extract SQL query from agent intermediate steps.
    """

    for action, observation in intermediate_steps:

        if hasattr(action, "tool_input"):

            tool_input = action.tool_input

            if isinstance(tool_input, dict):

                sql_query = tool_input.get(
                    "sql_query"
                )

                if sql_query:
                    return sql_query

    return "SQL query not available."


def ask_question(question: str):
    """
    Execute agent and display:
    - Generated SQL
    - Final Answer
    """

    response = agent_executor.invoke(
        {
            "input": question
        }
    )

    generated_sql = extract_sql_query(
        response.get(
            "intermediate_steps",
            []
        )
    )

    return {
        "sql_query": generated_sql,
        "answer": response["output"]
    }


def main():

    print("=" * 60)
    print("E-Commerce SQL Agent")
    print("Type 'exit' to quit")
    print("=" * 60)

    while True:

        question = input("\nQuestion: ")

        if question.lower() == 'exit':
            break

        result = ask_question(question)

        print("\nGenerated SQL:")
        print(result["sql_query"])

        print("\nAnswer:")
        print(result["answer"])


if __name__ == "__main__":
    main()