import os
import sys
import json
from datetime import datetime
from config import Config
from loaders import load_pdf_documents
from chunking import get_text_chunks
from vector_store import create_vector_store
from retriever import get_retriever
from chains import get_classification_chain, get_grounded_rag_chain


def run_ingestion():
    """Runs the ingestion pipeline to build the vector store."""
    print("Step 1: Loading PDF documents...")
    docs = load_pdf_documents()
    if not docs:
        print("Error: No PDF documents found in data/raw/.")
        sys.exit(1)

    print(f"Step 2: Splitting {len(docs)} pages into chunks...")
    chunks = get_text_chunks(docs)
    
    print("Step 3: Generating embeddings and updating Vector Store...")
    create_vector_store(chunks)
    print("--- Ingestion Complete ---\n")



def log_query(log_data):
    """Saves query history to a JSONL file."""
    try:
        # Ensure the logs directory exists
        Config.LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(Config.LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data) + "\n")
    except Exception as e:
        print(f"[Warning] Failed to save log: {e}")



def save_benchmark(benchmark_data):
    """Saves the structured answer to a JSON file for benchmarking."""
    try:
        Config.BENCHMARK_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        results = []
        if Config.BENCHMARK_FILE_PATH.exists():
            with open(Config.BENCHMARK_FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    results = json.load(f)
                    if not isinstance(results, list): results = []
                except json.JSONDecodeError:
                    results = []
        
        results.append(benchmark_data)
        with open(Config.BENCHMARK_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
    except Exception as e:
        print(f"[Warning] Failed to save benchmark: {e}")



def main():
    print("--- AI Knowledge Assistant (CLI) ---")

    # Check if vector store exists, if not, ingest
    if not Config.VECTOR_STORE_DIR.exists() or not any(Config.VECTOR_STORE_DIR.iterdir()):
        print("Vector store not found. Starting initial ingestion...")
        run_ingestion()
    else:
        print(f"Existing Vector Store found at {Config.VECTOR_STORE_DIR}. Skipping ingestion.")

    # Initialize Retriever and Chain
    print("Initializing RAG Engine...")
    retriever = get_retriever()
    classifier = get_classification_chain()
    rag_chain = get_grounded_rag_chain()
    
    print("\nReady! Ask me anything about your documents (type 'exit' to quit).")
    
    while True:
        query = input("\nUser: ")
        
        if query.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        if not query.strip():
            continue

        print("Assistant is thinking...")
        
        # Step 1: Classification
        classification = classifier.invoke({"input": query})
        print(f"[Log] Classification: Retrieval Required={classification.get('requires_retrieval')}")
        
        # Initialize log structure
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": query,
            "query_type": classification.get("query_type"),
            "retrieved_sources": [],
            "answer": "",
            "answerability": "",
            "confidence": ""
        }

        if classification.get("requires_retrieval"):
            # Step 2: Retrieval
            docs = retriever.invoke(query)
            context = "\n\n".join([d.page_content for d in docs])
            
            # Step 3: Grounded Answer
            response = rag_chain.invoke({
                "input": query,
                "context": context
            })
            
            print(f"\nAssistant: {response.get('answer')}")

            print("\nSource References:")
            for doc in docs:
                source = doc.metadata.get("source_file", "Unknown")
                page = doc.metadata.get("page_number", "Unknown")
                chunk_id = doc.metadata.get("chunk_id", "Unknown")
                # Clean up text for the snippet: remove newlines and truncate
                snippet = doc.page_content.replace("\n", " ").strip()
                snippet = (snippet[:140] + "...") if len(snippet) > 140 else snippet
                
                print(f"Source: {source}, page {page}, {chunk_id}")
                print(f"Snippet: \"{snippet}\"\n")

                # Update log with sources
                log_entry["retrieved_sources"].append({
                    "source_file": source,
                    "page_number": page,
                    "chunk_id": chunk_id
                })

            print(f"Confidence: {response.get('confidence')}")
            print(f"Status: {response.get('answerability')}")
            
            # Update log with answer details
            log_entry.update({
                "answer": response.get("answer"),
                "answerability": response.get("answerability"),
                "confidence": response.get("confidence")
            })

            # Save benchmark result
            benchmark_data = {
                "question": query,
                "answer": response.get("answer"),
                "supporting_evidence": response.get("supporting_evidence", []),
                "sources": response.get("sources", []),
                "confidence": response.get("confidence"),
                "answerability": response.get("answerability")
            }
            save_benchmark(benchmark_data)
        else:
            answer = f"{classification.get('reasoning_summary')} (I'm a RAG bot, please ask questions about your data.)"
            print(f"\nAssistant: {answer}")
            log_entry["answer"] = answer

        # Save the history
        log_query(log_entry)

if __name__ == "__main__":
    main()