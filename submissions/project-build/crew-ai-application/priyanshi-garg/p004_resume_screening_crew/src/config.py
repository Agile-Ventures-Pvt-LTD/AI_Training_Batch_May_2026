import os
from crewai import LLM

from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

try:
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.environ["GROQ_API_KEY"],
        tool_choice="auto"
        )
except:
    print("Unable to fetch API key")

