import os
from pydantic_ai import Agent
from dotenv import load_dotenv
from src.database import retrieve_documents, initialize_database
from src.guardrails_config import validate_input, validate_output

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


rag_agent = Agent(
    "groq:llama-3.3-70b-versatile",
    system_prompt=(
        "You are a helpful assistant for eBay sellers.\n"
        "- Your knowledge is limited to the eBay Advanced Business Seller Guide.\n"
        "- Use the `retrieve_docs` tool whenever user questions may require external info.\n"
        "- When you call it, read the returned documents and answer using ONLY that info plus the question.\n"
        "- If the tool returns nothing relevant, say you couldn't find anything relevant in the guide.\n"
        "- Do not make up information or answer questions outside the scope of the guide.\n"
        "- Be concise and provide specific information from the guide when possible."
    ),
)

# Define a retriever tool for RAG
@rag_agent.tool
def retrieve_docs(query: str) -> str:
    """
    Retrieve relevant documents for a query from the eBay seller guide.
    """
    docs = retrieve_documents(query)
    if not docs:
        return "No relevant information found in the eBay Advanced Business Seller Guide."
    
    # Combine the retrieved documents
    combined_docs = "\n\n".join(docs)
    return combined_docs

async def ask_question(question: str, initialize_db=False) -> str:
    """
    Ask a question to the RAG agent with guardrails
    """
    # Initialize database if needed
    if initialize_db:
        await initialize_database()
    
    # Validate input
    is_valid, result = validate_input(question)
    if not is_valid:
        return result
    
    # Get response from agent
    agent_result = await rag_agent.run(question)
    response = agent_result.output
    
    # Validate output
    is_valid, safe_response = validate_output(response)
    if not is_valid:
        return safe_response
    
    return safe_response

async def initialize_rag_system(force_reset=False):
    """
    Initialize the RAG system by setting up the database
    """
    await initialize_database(force_reset=force_reset)
    print("RAG system initialized successfully!")