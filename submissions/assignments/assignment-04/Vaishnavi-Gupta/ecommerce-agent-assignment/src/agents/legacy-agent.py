from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent


def build_agent():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    db = SQLDatabase.from_uri(
        "sqlite:///data/ecommerce.db"
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True
    )

    return agent


if __name__ == "__main__":

    agent = build_agent()

    response = agent.run(
        "What is the total revenue from completed orders?"
    )

    print(response)