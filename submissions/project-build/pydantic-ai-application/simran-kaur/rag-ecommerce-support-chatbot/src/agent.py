from pydantic_ai import Agent
from pydantic_ai import 
# from tools.rag_tools import search_documents


from dataclasses import dataclass
from rag.retriever import Retriever


SYSTEM_PROMPT="""
You are a RAG expert.
You need to answer user questions using the retrieved context.

Instructions:

1. Decide whether the user's question requires searching the document collection.

2. If the answer depends on the uploaded documents,
use the search_documents tool.

3. If the answer is common knowledge,
answer directly without calling any tool.

4. Never invent facts.

5. If the documents do not contain the answer,
say so clearly.

6. Whenever you use retrieved information,
mention the document name(s) as sources.
"""


@dataclass
class AgentDependencies:
    retriever: Retriever


rag_agent = Agent(

    model="groq:openai/gpt-oss-120b",

    deps_type=AgentDependencies,

    system_prompt=SYSTEM_PROMPT,
)


async def semantic_search(collection, query: str, n_results: int = 2):
    """Perform semantic search on the collection"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results