import os
from dotenv import load_dotenv
from vector_store import vectorstore

load_dotenv()
os.environ["TOP_K"] = os.getenv("TOP_K")

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        'k': int(os.environ["TOP_K"])
    }
)