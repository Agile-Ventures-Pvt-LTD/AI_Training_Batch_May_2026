import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")

try:
    llm = ChatGroq(
        api_key=os.environ["GROQ_API_KEY"], 
        model=os.environ["GROQ_MODEL"],
        temperature=0
    )

except Exception as e:
    print(e)