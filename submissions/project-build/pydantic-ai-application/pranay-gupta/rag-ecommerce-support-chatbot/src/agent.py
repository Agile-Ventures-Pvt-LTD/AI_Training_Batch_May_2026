from narwhals import List
from pydantic_ai import Agent
from database import retrieve_documents
from guardrails import Guard
from guardrails_config import response2,response1,response3,Guard_rails


# Define a retriever tool for RAG
def retrieve_docs(query: str) -> List[str]:
    """
    Retrieve relevant documents for a query.
    In real life, call your vector DB / search index here.
    """
    doc = retrieve_documents(query)
    relevant_document_chunks = doc
    context_list = [d.page_content for d in relevant_document_chunks]
    context_for_query = "\n---\n".join(context_list)
    return context_for_query

async def main():
    rag_agent = Agent(
        "groq:llama-3.3-70b-versatile",
        system_prompt=(
            "You are a RAG assistant.\n"
            "- Use the `retrieve_docs` tool whenever user questions may require external info.\n"
            "- When you call it, read the returned documents and answer using ONLY that info plus the question.\n"
            "- If the tool returns nothing, say you couldn't find anything relevant."
        ),
        tools=[retrieve_docs],
    )
    user_query = input("Enter your question: ")
    check = Guard_rails(user_query)
    if response2.validated_passed and response1.validation_passed is False:
        print("Query invalid")

    result = await rag_agent.run(user_query)
    return result.output



