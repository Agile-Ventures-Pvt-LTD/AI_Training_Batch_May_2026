
from database import collection
from pydantic_ai import Agent
from typing import List

# Define a retriever tool for RAG

def retrieve_docs(query: str) -> List[str]:
    """
    Retrieve relevant documents for a query.
    In real life, call your vector DB / search index here.
    """
    results = collection.query(
        query_texts=query,
        n_results=2,
    )
    return results


# Create the agent and attach the tool
rag_agent = Agent(
    "groq:openai/gpt-oss-120b",
    system_prompt=(
        "You are a RAG assistant.\n"
        "- Use the `retrieve_docs` tool whenever user questions may require external info.\n"
        "- When you call it, read the returned documents and answer using ONLY that info plus the question.\n"
        "- If the tool returns nothing, say you couldn't find anything relevant."
    ),
    tools=[retrieve_docs],
)
question = input("Enetr Query: ")
result = await rag_agent.run(question)
result.all_messages()

async def ask(question: str):
    result = await rag_agent.run(question)
    print(result.output)
await ask(question)
