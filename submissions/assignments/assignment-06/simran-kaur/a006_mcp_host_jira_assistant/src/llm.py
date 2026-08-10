import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


model_llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
    
    )



