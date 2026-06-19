from config import POLICY_DATA_PATH
from loaders import load_documents
from chunking import create_chunks
from retrievers import build_vector_store
from graph import graph

from dotenv import load_dotenv
load_dotenv()
import os
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

def setup_vector_store():
    """Setup for vector store"""
    documents = load_documents(POLICY_DATA_PATH)
    chunks = create_chunks(documents)
    build_vector_store(chunks)
    print("Vector store created")

def run():
    """This will give answer"""
    question = input("Ask a policy question:")
    result = graph.invoke({"user_question":question,"query_type": "","required_policy_domains":[],"requires_clarification":False,"rewritten_query":"","retrieved_context":[],"context_grade":{},"answer":{},"reflection":{},"retry_count":0,"final_response":"",})
    print(result["final_response"])

if __name__ == "__main__":
    setup_vector_store()
    while True:
        run()

        