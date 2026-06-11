from langchain.agents import initialize_agent
from langchain.agents import AgentType

from src.agents.legacy_agent import llm
from src.tools.ecommerce_sql_tool import query_ecommerce_database


tools = [query_ecommerce_database]


agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)


def ask(question: str):

    result = agent_executor.invoke(
        {
            "input": question
        }
    )

    return result["output"]


if __name__ == "__main__":

    print("=" * 60)
    print("E-Commerce Database Agent")
    print("Type 'exit' to quit")
    print("=" * 60)

    while True:

        query = input("\nQuestion: ")

        if query.lower() in ["exit", "quit"]:
            break

        try:
            answer = ask(query)

            print("\nAnswer:")
            print(answer)

        except Exception as e:
            print(f"\nError: {e}")