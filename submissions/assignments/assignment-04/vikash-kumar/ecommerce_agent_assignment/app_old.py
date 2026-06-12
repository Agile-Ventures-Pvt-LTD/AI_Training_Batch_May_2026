from langchain.agents import initialize_agent
from langchain.agents import AgentType

from src.agents.legacy_agent import llm
from src.tools.ecommerce_sql_tool import ecommerce_sql_tool

tools = [ecommerce_sql_tool]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)


def ask(question):

    result = agent_executor.invoke(
        {"input": question}
    )

    return result["output"]


if __name__ == "__main__":

    print("\nOlist Ecommerce Agent Ready\n")

    while True:

        question = input("\nAsk Question: ")

        if question.lower() == "exit":
            break

        try:

            answer = ask(question)

            print("\nAnswer:")
            print(answer)

        except Exception as e:

            print(e)