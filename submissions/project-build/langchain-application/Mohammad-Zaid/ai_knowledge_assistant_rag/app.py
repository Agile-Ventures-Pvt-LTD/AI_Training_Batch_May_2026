
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from loaders import load_pdf
from chunking import set_document_metadata, chunk_documents
from vector_store import vector_db
from retriever import retrieve_documents, build_context_from_documents, build_citations_from_documents
from prompts import SYSTEM_PROMPT
from groq import Groq
from logger import save_query_log


def index_documents(file_path):
    """Load and index PDF documents"""
    print(f"Loading PDF: {file_path}")
    docs = load_pdf(file_path)
    
    if not docs:
        print("No documents loaded")
        return
    
    print(f"Loaded {len(docs)} pages")
    
    # Preprocess
    cleaned_docs = [set_document_metadata(doc, file_path) for doc in docs]
    print(f"Preprocessed {len(cleaned_docs)} pages")
    
    # Chunk
    chunks = chunk_documents(cleaned_docs)
    print(f"Created {len(chunks)} chunks")
    
    # Add to vector store
    existing_count = vector_db._collection.count()
    if existing_count == 0:
        vector_db.add_documents(
            documents=chunks,
            ids=[chunk.metadata["chunk_id"] for chunk in chunks],
        )
        print(f"Added {len(chunks)} chunks to vector store")
    else:
        print(f"Vector store already contains {existing_count} chunks")


def query_rag(question):
    """Query the RAG system"""
    print(f"\nQuestion: {question}\n")
    
    # Retrieve
    print("Retrieving documents...")
    retrieved_chunks = retrieve_documents(vector_db, question)
    print(f"Retrieved {len(retrieved_chunks)} chunks\n")
    
    # Build context
    context = build_context_from_documents(retrieved_chunks)
    context_citations = build_citations_from_documents(retrieved_chunks)
    
    # Build prompt
    prompt = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.format(
                question=question,
                context=context,
                citations="\n".join(context_citations)
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]
    
    # Generate answer
    print("Generating answer...\n")
    groq_client = Groq()
    response = groq_client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=prompt,
        temperature=0.2
    )
    
    answer = response.choices[0].message.content
    
    # Display
    print("="*80)
    print("ANSWER:")
    print("="*80)
    print(answer)
    print("="*80)
    print(f"Sources: {context_citations}\n")
    
    # Log
    save_query_log(
        question=question,
        answer=answer,
        sources=context_citations,
        confidence="MEDIUM",
        answerability="ANSWERED"
    )
    
    print("Query logged to logs/query_logs.jsonl")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python app.py index <pdf_file>")
        print("  python app.py query \"<question>\"")
        return
    
    command = sys.argv[1]
    
    if command == "index" and len(sys.argv) > 2:
        file_path = sys.argv[2]
        index_documents(file_path)
    elif command == "query" and len(sys.argv) > 2:
        question = sys.argv[2]
        query_rag(question)
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
