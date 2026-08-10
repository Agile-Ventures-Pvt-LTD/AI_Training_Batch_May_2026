
from crewai import LLM
import os

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
    tool_choice="auto"
    )
