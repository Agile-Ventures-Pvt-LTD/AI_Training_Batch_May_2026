import json
import os
from loaders import load_docs
from chunking import txt_splitting_to_chunks
from vector_store import create_vector_db, load_vector_db
from retriever import retrieving_chunks
from chains import RAGChain
from logger import log_query

def setup_db():
    """Initializes the database if it doesn't exist."""
    docs = load_docs()
    if not docs:
        print("No Doc founds.")
        return None
    
    chunks = txt_splitting_to_chunks(docs)
    return create_vector_db(chunks)

def run_benchmarks(chain, db):
    """Runs the benchmark questions and saves to outputs/"""
    # Create questions for Amazon 2025 Annual Report
    questions = [
        "What does Amazon say about AWS and AI-related growth?",
        "What risks are mentioned related to supply chain?",
        "Summarise Amazon's key risks factors in 5 bullet points.",
        "What does the document say about Amazon's advertising services revenue?",
        "Compare AWS business growth to the India segment based on the provided documents.",
        "What legal  risks are mentioned for Amazon?",
        "What will Amazon's stock price be next year?",
        "Does the document guarantee future profitability from Amazon's AI investments?"
    ]
    results = []
    for q in questions:
        chunks = retrieving_chunks(db, q)
        context = "\n\n---\n\n".join([f"File: {c.metadata['source_file']} | Page: {c.metadata['page_number']}\nText: {c.page_content}" for c in chunks])
        res = chain.generate(q, context)
        results.append({"question": q, "result": res})
    
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved benchmark answers to outputs folder")

def main():
    chain = RAGChain()
    db = load_vector_db()
    
    if not db:
        db = setup_db()
        if not db:
            return

    while True:
        print("\n AI Knowledge Assistant")
        print("1. Ask a question")
        print("2. Run benchmarks questions")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            query = input("\nQuery: ").strip()
            if not query:
                continue
                
            classification = chain.classify(query)
            chunks = retrieving_chunks(db, query)
            
            context = "\n\n---\n\n".join([f"File: {c.metadata['source_file']} | Page: {c.metadata['page_number']}\nText: {c.page_content}" for c in chunks])
            
            print("\n[Debug] Retrieved Chunks:")
            for idx, c in enumerate(chunks, 1):
                print(f" {idx}. {c.metadata['source_file']} (Page {c.metadata['page_number']}) - {c.metadata['chunk_id']}")
                
            ans = chain.generate(query, context)
            
            print(f"\nAnswer ({ans.get('confidence', 'UNKNOWN')} Confidence):")
            print(ans.get("answer", "No answer generated."))
            
            print("\nSources:")
            for s in ans.get("sources", []):
                print(f"- {s.get('source_file')}, Page {s.get('page_number')} (Chunk {s.get('chunk_id')})")
                
            # Logging the query to JSONL
            log_query({
                "question": query,
                "query_type": classification.get("query_type"),
                "answerability": ans.get("answerability"),
                "retrieved_sources": [c.metadata["chunk_id"] for c in chunks],
                "answer": ans.get("answer"),
                "confidence": ans.get("confidence")
            })
            
        elif choice == "2":
            run_benchmarks(chain, db)
            
if __name__ == "__main__":
    main()