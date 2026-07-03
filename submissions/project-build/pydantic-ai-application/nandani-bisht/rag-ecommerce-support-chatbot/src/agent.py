import os
from dataclasses import dataclass
from typing import Any
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
load_dotenv()

from guardrails_config import scan_text
from database import initialize_database, COLLECTION_NAME

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key and openai_key.startswith("gsk_"):
        api_key = openai_key

if not api_key:
    raise ValueError("Error: Groq API Key not found. Please set GROQ_API_KEY or OPENAI_API_KEY in your environment.")

model = OpenAIModel(
    model_name="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

@dataclass
class RAGDeps:
    collection: Any  

agent = Agent(
    model=model,
    deps_type=RAGDeps,
    system_prompt=(
        "You are an enterprise-grade seller support agent for ShopSphere Marketplace.\n"
        "Your task is to help independent business sellers with advanced operations, calculating Average Selling Price (ASP), managing Detailed Seller Ratings (DSRs), and handling fulfillment.\n\n"
        "Guidelines:\n"
        "1. Answer queries using ONLY the retrieved context retrieved via the retrieve_seller_guide_context tool.\n"
        "2. Do not mention anything about 'the provided context' or 'the document' in your final response. Answer naturally.\n"
        "3. If the query falls completely outside the scope of the document, or if the retrieved context is insufficient to answer the question, you MUST return the following exact standardized polite fallback message:\n"
        "'I am sorry, but I cannot find information in the seller guide regarding this topic. Please contact ShopSphere support for further assistance.'\n"
        "Do not fabricate or make up any details."
    )
)

@agent.tool
def retrieve_seller_guide_context(ctx: RunContext[RAGDeps], query: str) -> str:
    """
    Retrieves the most relevant document chunks from the eBay Advanced Business Seller Guide.
    
    Args:
        ctx: RunContext containing agent dependencies.
        query: The semantic search query string.
        
    Returns:
        A string containing relevant document pages and content.
    """
    results = ctx.deps.collection.query(
        query_texts=[query],
        n_results=5
    )
    
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    
    if not docs:
        return "No relevant context found."
        
    context_list = []
    for doc, meta in zip(docs, metadatas):
        page = meta.get("page", "unknown")
        context_list.append(f"[Page {page}]\n{doc}")
        
    return "\n---\n".join(context_list)

def respond(user_query: str, collection: Any) -> str:
    """
    Processes the user query end-to-end:
    1. Input scan via Guardrails (Profanity + Toxicity)
    2. Context retrieval and LLM processing via Pydantic AI
    3. Output scan via Guardrails (Profanity + Toxicity)
    
    Args:
        user_query: The natural language question from the seller.
        collection: The initialized Chroma DB collection.
        
    Returns:
        The validated chatbot answer or a safety warning.
    """
    
    is_safe_input, input_msg = scan_text(user_query, is_input=True)
    if not is_safe_input:
        return input_msg
        
    deps = RAGDeps(collection=collection)
    try:
        result = agent.run_sync(user_query, deps=deps)
        answer = result.data.strip()
    except Exception as e:
        return f"Error:Failed to process query. Details: {e}"
        
    is_safe_output, output_msg = scan_text(answer, is_input=False)
    if not is_safe_output:
        return output_msg
        
    return answer

def main():
    """Interactive chatbot for the seller """
    print("Initializing persistent Chroma DB...")
    collection = initialize_database()
    print("Chroma DB initialized and loaded.")
    print("-" * 60)
    print("ShopSphere RAG Marketplace Chatbot Initialized.")
    print("Ask about fulfillment, ASP calculation, and DSR metrics.")
    print("Type 'q' to exit the conversation.")
    print("-" * 60)
    
    while True:
        try:
            user_query = input("\nSeller: ")
            if user_query.strip().lower() == 'q':
                print("Exit")
                break
                
            if not user_query.strip():
                continue
                
            answer = respond(user_query, collection)
            print(f"Agent: {answer}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Thank you!")
            break

if __name__ == "__main__":
    main()
