from pydantic_ai import Agent
from pydantic_ai.capabilities import Thinking, WebSearch

agent = Agent(
    'llama-3.3-70b-versatile',
    instructions='Be concise, reply with one sentence.',
    capabilities=[Thinking(), WebSearch(local='duckduckgo')],
)

result = agent.run_sync('What is the weather of Gurgaon right now?')
print(result.output)
"""
The weather of Gurgaon is 40 degree celcius right now.
"""


