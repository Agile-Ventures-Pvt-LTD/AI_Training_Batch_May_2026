import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")

try:
    llm = LLM(
        model=os.environ["GROQ_MODEL"], 
        api_key=os.environ["GROQ_API_KEY"],
        tool_choice="auto"
    )

except Exception as e:
    print(e)