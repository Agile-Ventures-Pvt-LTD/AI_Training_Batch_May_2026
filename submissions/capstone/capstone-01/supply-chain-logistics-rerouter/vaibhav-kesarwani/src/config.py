import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")

llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model=os.environ["GROQ_MODEL"],
    temperature=0
)

def call_llm(prompt: list, model: str=os.environ["GROQ_MODEL"], temperature: int=0, type: dict={"type" : "json_object"}):
    client = Groq()

    try: 
        response = client.chat.completions.create(
            messages=prompt,
            model=model,
            response_format=type,
            temperature=temperature
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating the response : {e}")
        return None
