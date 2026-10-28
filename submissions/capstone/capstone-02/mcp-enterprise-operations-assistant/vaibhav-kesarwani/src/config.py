import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")

try:
    llm = ChatGroq(
        model=os.environ["GROQ_MODEL"],
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0
    )

except Exception as e:
    print(f"Error loading the groq model : {e}")