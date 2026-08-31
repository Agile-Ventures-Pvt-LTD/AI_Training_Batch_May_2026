import sys
import json
from pathlib import Path
from loaders import load_kb_documents
from chunking import chunk_documents, add_chunk_metadata
from vector_store import get_or_create_vector_store
from prebuilt_agent import build_agent, invoke_agent
from output_parser import parse_agent_output, format_json_response, validate_output
from config import OUTPUT_DIR


def initialize_system():
    print("Initializing IT Troubleshooting Agent...")
    try:
        print("Loading knowledge base documents...")
        documents = load_kb_documents()
        print(f"    Loaded {len(documents)} documents")
        
        print("Chunking documents...")
        chunks = chunk_documents(documents)
        chunks = add_chunk_metadata(chunks)
        print(f"    Created {len(chunks)} chunks")
        
        print("Building vector store...")
        vector_store = get_or_create_vector_store(chunks)
        print(f"    Vector store ready")
        
        print("Building agent...")
        agent = build_agent()
        print(f"    Agent initialized")
        return agent
    except Exception as e:
        print(f"ERROR during initialization: {e}")
        sys.exit(1)


def query_agent(agent, user_query):
    try:
        print(f"\nProcessing query: '{user_query}'")
        print("Agent is thinking...\n")
        
        response = invoke_agent(agent, user_query)
        parsed = parse_agent_output(response)
        if not validate_output(parsed):
            print("Output missing")
        return parsed
    
    except Exception as e:
        print(f"ERROR during agent invocation: {e}")


def save_output(parsed_output, query):
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = output_dir / "evaluation_results.json"
    
    output_entry = {
        "query": query,
        "response": parsed_output
    }
    
    try:
        existing = []
        if filename.exists() and filename.stat().st_size > 0:
            with open(filename, "r") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
        
        existing.append(output_entry)
        
        with open(filename, "w") as f:
            json.dump(existing, f, indent=2)
        
        print(f"Output saved to {filename}")
    
    except Exception as e:
        print(f"Warning: Could not save output: {e}")


def main():
    agent = initialize_system()
    
    print("\nAgent ready! Enter your support query.")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("Support Query: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting agent. Goodbye!")
                break
            if not user_input:
                print("Please enter a query.\n")
                continue
            parsed_output = query_agent(agent, user_input)
            print(format_json_response(parsed_output))
            save_output(parsed_output, user_input)
            print()
    
        except KeyboardInterrupt:
            print("\n\nExiting agent. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
