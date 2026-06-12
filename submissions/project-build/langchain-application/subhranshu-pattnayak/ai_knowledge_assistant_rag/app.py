from embeddings import init_embedding
from vector_store import load_chunks
from retriever import init_retriever, query_retriever
import chromadb
from config import load_env
from logger import log_interaction
from prompts import QA_PROMPT
from langchain_groq import ChatGroq

def main():
    load_env()
    
    collection_name = "amazon_annual_reports"
    path = "./amazon.db"
    query = input("Enter your query: ")
    
    embedding_model = init_embedding()
    chromadb_client = chromadb.PersistentClient(path=path)

    retriever = init_retriever(
        collection=collection_name,
        embedding=embedding_model,
        chromadb_client=chromadb_client,
        directory=path,
        search_kwargs={"k": 5}
    )

    # Retrieve context
    results = query_retriever(retriever, query=query)
    context = "\n\n".join([r.page_content for r in results])

    # Initialize Groq LLM
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0, max_tokens=1024)

    # Format QA prompt with context + question
    prompt = QA_PROMPT.format(context=context, question=query)

    # Run query through Groq
    answer = llm.invoke(prompt)

    print("\n=== Answer ===")
    print(answer)

    # Log interaction
    log_interaction(query, answer.content)

main()