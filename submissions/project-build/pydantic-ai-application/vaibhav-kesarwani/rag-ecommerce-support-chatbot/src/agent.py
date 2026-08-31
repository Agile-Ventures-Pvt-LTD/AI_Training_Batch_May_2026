import os
from typing import List
from retreiver import retrival_chunks
from pydantic_ai import Agent, RunContext
from schema import RagAnswer, RagDeps, DocsChunk
from dotenv import load_dotenv
from prompts import agent_prompt

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")


try:
    agent = Agent[RagDeps, RagAnswer](
        model=os.environ["GROQ_MODEL"],
        system_prompt=agent_prompt,
        output_type=RagAnswer,    
        deps_type=RagDeps,
        retries=2
    )
except Exception as e:
    print(e)


@agent.tool()
def search_tool(ctx: RunContext[RagDeps], query: str) -> List[DocsChunk]:
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