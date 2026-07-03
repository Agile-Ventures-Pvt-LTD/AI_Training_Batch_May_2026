import os
from typing import List
from src.retriever import retrival_chunks
from pydantic_ai import Agent, RunContext
from src.schema import RagAnswer, RagDeps, DocumentChunk
from dotenv import load_dotenv
from src.prompts import agent_prompt
from src.config import Config



try:
    agent = Agent[RagDeps, RagAnswer](
        model=Config.GROQ_MODEL_NAME,
        system_prompt=agent_prompt,
        output_type=RagAnswer,    
        deps_type=RagDeps,
        retries=2
    )
except Exception as e:
    print(e)


@agent.tool()
def search_tool(ctx: RunContext[RagDeps], query: str) -> List[DocumentChunk]:
    """
    Used to get the required chunks from the documents 
    according to the user query.

    Args:
        ctx: Documents chunks created from the pdf
        query: User Query    
    
    Return:
        return: The List of related chunks from the documents
    """

    return retrival_chunks(query=query, docs=ctx.deps.documents)