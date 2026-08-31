from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

GROQ_MODEL = os.getenv('GROQ_MODEL','llama-3.3-70b-versatile')

llm = ChatGroq(model=GROQ_MODEL,groq_api_key = os.environ['GROQ_API_KEY'],temperature=0)

DB_PATH = os.getenv('DB_PATH','data/ccms.db')

