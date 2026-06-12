import argparse
import json
import sys
from pathlib import Path

from config import GROQ_API_KEY, GROQ_MODEL, TOP_K, RAW_DATA_DIR
from loaders import load_documents
from chunking import create_chunks
from embeddings import EmbeddingModel
from vector_store import create_vector_store
from retriever import retrieve, format_retrieved_chunks
from chains import classify_query, build_rag_answer
from output_parser import build_not_found_output
from logger import log_query


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enterprise AI Knowledge Assistant using RAG, Groq, and LangChain."
    )
    parser.add_argument("question", type=str, help="Question to ask the knowledge assistant.")
    parser.add_argument("--top_k", type=int, default=TOP_K, help="Number of chunks to retrieve.")
    parser.add_argument("--debug", action="store_true", help="Show retrieved context debug view.")
    args = parser.parse_args()

    
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY is not set. Create a .env file with your Groq API key.")
        sys.exit(1)

    if not RAW_DATA_DIR.exists() or not any(RAW_DATA_DIR.iterdir()):
        print(f"ERROR: No documents found in {RAW_DATA_DIR}. Place PDFs, TXT, or MD files in the raw folder.")
        sys.exit(1)

    question = args.question.strip()
    if not question:
        print("ERROR: Question cannot be empty.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}\n")

    print("[1/7] Classifying query type...")
    query_data = classify_query(question)
    print(f"  Query Type: {query_data['query_type']}")
    print(f"  Answer Style: {query_data['answer_style']}")

    
    print("\n[2/7] Loading documents...")
    documents = load_documents()
    print(f"  Loaded {len(documents)} document page(s).")


    print("\n[3/7] Chunking documents...")
    chunks = create_chunks(documents)
    print(f"  Created {len(chunks)} chunks.")
    print(f"  Chunk Size: {chunks[0].get('text', '')[:100]}..." if chunks else "  No chunks created.")

    
    print("\n[4/7] Generating embeddings...")
    embedding_model = EmbeddingModel("sentence-transformers/all-MiniLM-L6-v2")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.embed_documents(texts)
    print(f"  Generated {len(embeddings)} embeddings (dimension: {len(embeddings[0])})" if embeddings else "  No embeddings generated.")

    
    print("\n[5/7] Creating vector store...")
    vector_store = create_vector_store(chunks, embeddings)
    print(f"  Vector store ready.")

    
    print(f"\n[6/7] Retrieving top-{args.top_k} chunks...")
    retrieved_chunks = retrieve(question, vector_store, embedding_model, top_k=args.top_k)
    print(f"  Retrieved {len(retrieved_chunks)} chunk(s).")

    
    print("\n[7/7] Generating answer...\n")
    if not retrieved_chunks:
        output = build_not_found_output(question, query_data["query_type"], args.top_k)
        output["query_type"] = query_data["query_type"]
    else:
        output = build_rag_answer(question, retrieved_chunks, GROQ_API_KEY, GROQ_MODEL)
        output["query_type"] = query_data["query_type"]

    
    log_query(output)


    print(f"{'='*60}")
    print(f"ANSWER:")
    print(f"{'='*60}")
    print(f"  {output['answer']}")
    print()
    print(f"Answerability: {output['answerability']}")
    print(f"Confidence: {output['confidence']}")
    
    if output.get("sources"):
        print(f"{'='*60}")
        print(f"SOURCES:")
        print(f"{'='*60}")
        for src in output["sources"]:
            print(f"  - File: {src.get('source_file', 'N/A')}, Page: {src.get('page_number', 'N/A')}")
            snippet = src.get("snippet", "")
            if snippet:
                print(f"    Snippet: {snippet[:150]}...")
        print()

   
    if output.get("supporting_evidence"):
        print(f"{'='*60}")
        print(f"SUPPORTING EVIDENCE:")
        print(f"{'='*60}")
        for ev in output["supporting_evidence"]:
            print(f"  - Claim: {ev.get('claim', 'N/A')}")
            print(f"    Source: {ev.get('source_file', 'N/A')}, Page: {ev.get('page_number', 'N/A')}")
        

    # Debug 
    if args.debug and output.get("retrieval_debug", {}).get("retrieved_chunks"):
        print(f"{'='*60}")
        print(f"RETRIEVED CONTEXT (DEBUG VIEW):")
        print(f"{'='*60}")
        for chunk in output["retrieval_debug"]["retrieved_chunks"]:
            print(f"  Rank {chunk['rank']}: Score={chunk.get('similarity_score', 'N/A')}")
            print(f"    File: {chunk.get('source_file', 'N/A')}, Page: {chunk.get('page_number', 'N/A')}")
            print(f"    Chunk: {chunk.get('chunk_id', 'N/A')}")
            print(f"    Preview: {chunk.get('preview', '')[:200]}...")
            print()

    # JSON output
    print(f"{'='*60}")
    print(f"FULL OUTPUT (JSON):")
    print(f"{'='*60}")
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()