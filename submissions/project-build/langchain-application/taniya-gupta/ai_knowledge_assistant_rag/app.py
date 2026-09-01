import os
from dotenv import load_dotenv
import json
import argparse
from config import Config
import loaders
import chunking
import vector_store
from retriever import RetrieverManager
from chains import ChainManager
from logger import QueryLogger

load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")

def main():
    parser = argparse.ArgumentParser(description="AI Knowledge Assistant")
    parser.add_argument("--index", action="store_true", help="Index documents from the raw data folder")
    parser.add_argument("--query", type=str, help="Ask a question")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark questions")
    
    args = parser.parse_args()

    vsm = vector_store.VectorStoreManager(Config.VECTOR_DB_DIR, Config.EMBEDDING_MODEL)
    rm = RetrieverManager(vsm, Config.TOP_K)
    cm = ChainManager(os.environ['GROQ_API_KEY'], Config.GROQ_MODEL)
    ql = QueryLogger(Config.LOG_FILE)

    if args.index:
        index_documents(vsm)
    
    if args.query:
        process_query(args.query, cm, rm, ql)
    elif args.benchmark:
        run_benchmarks(cm, rm, ql)
    elif not args.index:
        interactive_mode(vsm, rm, cm, ql)

def index_documents(vsm):
    print("Loading documents")
    docs = loaders.load_documents(Config.RAW_DATA_DIR)
    chunks = chunking.split_documents(docs, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
    vsm.create_or_load_vector_store(chunks)
    print(f"Indexed {len(chunks)} chunks.")

def interactive_mode(vsm, rm, cm, ql):
    print("Project case 3: AI knowledge assistant")
    
    choice = input("1. Index documents\n2. Ask a question\n3. Run benchmark questions\nChoice: ")

    if choice == "1":
        index_documents(vsm)
    elif choice == "2":
        query = input("Question: ")
        process_query(query, cm, rm, ql)
    elif choice == "3":
        run_benchmarks(cm, rm, ql)

def process_query(query, cm, rm, ql):
    # Retrieve
    docs = rm.retrieve(query)
    
    # Classify & Answer
    classification = cm.get_classification_chain().invoke({"query": query})
    answer = cm.get_rag_chain().invoke({"context": docs, "question": query})
    
    print(f"\nType: {classification['query_type']}")
    print(f"Answer: {answer['answer']}")
    print(f"Confidence: {answer['confidence']}")
    
    ql.log_query(query, classification, answer, [d.metadata for d in docs])
    return answer

def run_benchmarks(cm, rm, ql):
    questions = ["What is PrimeAir", 
                 "What is definition and Limitations of Internal Control Over Financial Reporting",
                 "Summarize the key factors in 5 bullet points.",
                 "Summarize the key points of cybersecurity",
                 "Compare the cumulative total return on the common stock with the cumulative total return of the NYSE Technology Index",
                 "What legal or regulatory risks are mentioned?", 
                 "What will the stock price be?",
                 "Did the document say that it guarantees future profitability from AI products?"]
    results = []
    for q in questions:
        print(f"\nQuery: {q}")
        res = process_query(q, cm, rm, ql)
        results.append({"question": q, "answer": res["answer"]})
    
    if not os.path.exists(os.path.dirname(Config.BENCHMARK_OUTPUT)):
        os.makedirs(os.path.dirname(Config.BENCHMARK_OUTPUT))
        
    with open(Config.BENCHMARK_OUTPUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {Config.BENCHMARK_OUTPUT}")

if __name__ == "__main__":
    main()
