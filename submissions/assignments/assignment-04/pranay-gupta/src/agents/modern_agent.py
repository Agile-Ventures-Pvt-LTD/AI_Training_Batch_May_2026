from dotenv import load_dotenv

from langchain.agents import create_agent

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)

from src.prompts.system_prompt import (
    SYSTEM_PROMPT
)

load_dotenv()


agent = create_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[query_ecommerce_database],
    system_prompt=SYSTEM_PROMPT
)


def run_agent(user_query: str) -> str:
    """
    Execute user query using LangChain >= 1.0 agent.
    """

    try:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_query
                    }
                ]
            }
        )

        messages = response.get("messages", [])

        if messages:
            return messages[-1].content

        return "No response generated."

    except Exception as error:

        return (
            f"Agent Error: {str(error)}"
        )