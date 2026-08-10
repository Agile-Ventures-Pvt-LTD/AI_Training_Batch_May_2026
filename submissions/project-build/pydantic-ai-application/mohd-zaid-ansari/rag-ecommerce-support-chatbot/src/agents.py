import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List
from pydantic_ai import Agent, RunContext
from src.database import create_vector_store, get_embedding_model, retrive_data
from src.prompts import system_prompt

@dataclass
class Vector:
    vector_db=Any
    embedding_model=Any

rag_agent=Agent(
    model='groq:llama-3.1-8b-instant',
    deps_type=Vector,
    instructions=system_prompt
)

@rag_agent.tool
async def vector_search(
    ctx: RunContext[Vector],
    query: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for relevant information using semantic similarity.
    This tool performs vector similarity search across document chunks
    to find semantically related content. Returns the most relevant results
    regardless of similarity score."""
    input_data = retrive_data(
        query=query,
        limit=limit
    )
    
    results = await retrive_data(input_data)
    return [
        {
            "content": r.content,
            "score": r.score,
            "document_title": r.document_title,
            "document_source": r.document_source,
            "chunk_id": r.chunk_id
        }
        for r in results
    ]
