import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()
os.environ["EMBEDDING_MODEL"] = os.getenv("EMBEDDING_MODEL")

embedding = HuggingFaceEmbeddings(model_name=os.environ["EMBEDDING_MODEL"])
