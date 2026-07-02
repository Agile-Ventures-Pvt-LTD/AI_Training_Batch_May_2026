import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
os.environ['GROQ_MODEL']=os.getenv("GROQ_MODEL")



def get_llm():
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        api_key=os.getenv("GROQ_API_KEY")
    )