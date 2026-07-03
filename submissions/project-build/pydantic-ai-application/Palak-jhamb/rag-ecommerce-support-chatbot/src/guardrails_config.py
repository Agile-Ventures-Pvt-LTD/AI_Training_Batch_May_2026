from guardrails import Guard
from guardrails.hub import ProfanityFree
from src.agent_pydantic import agent_tool

def input_guard(query:str):
   guard = Guard().use(ProfanityFree(on_fail="exception"))
   res = guard.validate(query)
   return res.validated_output


def output_guard(query:str):
   guard = Guard().use(ProfanityFree(on_fail="exception"))
   response = guard(
    agent_tool,
    messages=[{"role": "user", "content": query}],
    )
   return response.validated_output


