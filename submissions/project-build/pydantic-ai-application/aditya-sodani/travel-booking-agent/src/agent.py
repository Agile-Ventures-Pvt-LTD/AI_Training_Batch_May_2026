import requests

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from src.prompts import system_prompt

from src.config import *


# Create Agent
agent = Agent(
    model="groq:llama-3.1-8b-instant",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=str,
    system_prompt=system_prompt
)


if __name__ == "__main__":
    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit", "q"]:
            print("Bye...")
            break

        try:
            result = agent.run_sync(user_prompt=query)
            response = result.output

            print("Response : ", response)


        except Exception as e:
            print(e)

