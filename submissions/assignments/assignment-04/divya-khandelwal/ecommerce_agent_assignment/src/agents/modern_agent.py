import os

from dotenv import load_dotenv

from langchain.agents import create_agent

from langchain_groq import ChatGroq

from src.prompts.system_prompts import (
    SYSTEM_PROMPT
)

from src.tools.ecommerce_sql_tool_modern import (
    query_ecommerce_database
)

load_dotenv()


class ModernEcommerceAgent:

    def __init__(self):

        self.model = ChatGroq(
            api_key=os.environ["GROQ_API_KEY"],
            model="openai/gpt-oss-120b",
            temperature=0
        )

        self.agent = create_agent(
            model=self.model,
            tools=[
                query_ecommerce_database
            ],
            system_prompt=SYSTEM_PROMPT
        )

    def run(self, question):

        response = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )

        return response