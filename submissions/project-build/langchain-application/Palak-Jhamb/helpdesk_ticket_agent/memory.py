
from agents import llm
from prompts import summary_system, summary_user
from groq_client import GroqClient
client=GroqClient()
   
def summary(data):
    raw_response_summary = client.generate(
    system_prompt=summary_system,
    user_prompt=summary_user.format(input=data)
    )
