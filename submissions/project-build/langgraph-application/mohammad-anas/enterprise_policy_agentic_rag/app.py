import os
from config import POLICY_DATA_PATH
from loaders import load_policies
from chunking import chunking
from prebuilt_agent import app_graph

# Import required LangChain components for vector indexing
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_groq import ChatGroq

def initialize_system():
    """Validates data environment, loads documents, and initializes search tools."""
    print("=== Initializing Enterprise Policy Assistant ===")
    
    # 1. Create source data directory if missing
    if not os.path.exists(POLICY_DATA_PATH):
        print(f"Creating directory at: {POLICY_DATA_PATH}")
        os.makedirs(POLICY_DATA_PATH)
        print("Please drop your policy files (.txt, .md, .pdf) into that folder and restart.")
        return None

    # 2. Extract raw data using custom loaders
    raw_docs = load_policies()
    if not raw_docs:
        print("No documents found in your policy data path. Agent will run without context.")
        return None

    # 3. Create document fragments via text splitters
    chunks = chunking(raw_docs)
    print(f"Processed {len(chunks)} text chunks.")

    # 4. Initialize embedding models and index documents
    # (Note: Replace this with your EMBEDDING_MODEL from config if using HuggingFace/OpenAI)
    from langchain_core.embeddings import FakeEmbeddings
    embeddings = FakeEmbeddings(size=1536) 
    
    print("Building vector index storage layer...")
    vector_store = InMemoryVectorStore.from_documents(chunks, embeddings)
    print("Indexing complete! Vector store is ready.")
    
    return vector_store

def run_chat_loop():
    """Runs a terminal-based interactive loop with your LangGraph prebuilt agent."""
    # Build or retrieve vector index lookup configuration
    vector_store = initialize_system()
    
    # Expose retriever reference globally or inject it if your tools.py reads it dynamically
    # For this example implementation, the agent runs directly via graph state streaming
    print("\n System Online!")
    
    while True:
        try:
            user_input = input("input ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("exit!")
                break
                
            print("\nAssistant : ", end="", flush=True)
            
            # Streaming events directly out of the compiled LangGraph reactive agent loop
            inputs = {"messages": [("user", user_input)]}
            config = {"configurable": {"thread_id": "policy_session_1"}}
            
            for chunk in app_graph.stream(inputs, config, stream_mode="values"):
                # Always grab the last message state appended by either the agent or tools
                if "messages" in chunk and chunk["messages"]:
                    last_msg = chunk["messages"][-1]
            
            # Print final compiled text reply from the ChatGroq model block
            if last_msg and hasattr(last_msg, "content"):
                print(f"{last_msg.content}\n")
                
        except KeyboardInterrupt:
            print("\nSession expire.")
            break
        except Exception as e:
            print(f"\nAn error occurred processing request: {e}\n")

if __name__ == "__main__":
    run_chat_loop()
