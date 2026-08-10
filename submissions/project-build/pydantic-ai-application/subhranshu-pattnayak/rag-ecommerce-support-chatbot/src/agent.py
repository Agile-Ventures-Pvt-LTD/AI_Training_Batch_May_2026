"""AGENT FILE for Rag Chatbot"""

import asyncio
import warnings
from pydantic_ai import Agent
from prompts import SYSTEM_PROMPT
from langchain_cohere import CohereRerank
from langchain_chroma import Chroma
from rag.embedding import init_embedding
from config import COLLECTION_NAME, DB_PATH
from langchain.retrievers import ContextualCompressionRetriever

warnings.filterwarnings("ignore")

agent = Agent(
    'groq:openai/gpt-oss-20b',
    system_prompt=SYSTEM_PROMPT,
    instructions="Be accurate and avoid hallucinations."
)

@agent.tool_plain
def retrieve(query: str):
    vectorstore_persisted = Chroma(
        collection_name=COLLECTION_NAME,
        collection_metadata={"hnsw:space": "cosine"},
        embedding_function=init_embedding(),
        persist_directory=DB_PATH
    )
    
    retriever = vectorstore_persisted.as_retriever(
        search_type="similarity",
        search_kwargs={
            'k': 5
        }
    )
    
    reranker = CohereRerank(model="rerank-v3.5", top_n=3)
    
    reranker_retriever = ContextualCompressionRetriever(
        base_compressor=reranker, base_retriever=retriever
    )
    
    return reranker_retriever.invoke(query)

async def main():
    res = await agent.run(query)
    return res.output

if __name__ =="__main__":
    while True:
        query = input("INPUT  (write 'exit' to leave)> ")
        
        if query == 'exit':
            break
        
        result = asyncio.run(main())
        
        print(result)