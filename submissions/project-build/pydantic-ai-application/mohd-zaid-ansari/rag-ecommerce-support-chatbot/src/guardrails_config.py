from guardrails import Guard
from pydantic import BaseModel
from typing import List
from groq import Groq
client=Groq()
model='openai/gpt-oss-120b'

from guardrails.hub import profanityFree
from guardrails.hub import ToxicLanguage

user_input="What is the total sales of the company"

def llm_wrapper(messages=None, model=None, **kwargs):
    return client.chat.completions.create(model=model, messages=messages, **kwargs).choices[0].message.content

guard=Guard.use(profanityFree(on_fail="fix"))

response=client.chat.completions.create(
    model='openai/gpt-oss-120b',
    messages=[{
        'role':'user', 'content':user_input
    }]
)

generate_output=response.choices[0].message.content

response=guard(
    llm_wrapper,
    messages=[{"role":"user", "content":generate_output}],
    model=model
)

print("Validated output:", response.validated_output)
print("Validation passed:", response.validation_passed)


#================================================================================================================================

def llm_wrapper(messages=None, model=None, **kwargs):
    return client.chat.completions.create(model=model, messages=messages, **kwargs).choices[0].message.content

guard=Guard.use(ToxicLanguage(threshold=0.5, validation_method="sentence",on_fail="exception"))
try:
    guard.validate(user_input)
except Exception as e:
    print(e)

output=response.validated_output

response=guard(
    llm_wrapper,
    messages=[{"role":"user", "content":output}],
    model=model
)

response=response.validation_passed

#=================================================================================================================================




















import asyncio
from dataclasses import dataclass
from typing import Any
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

# 1. Define Dependencies to hold your vector db client and embeddings API
@dataclass
class VectorDeps:
    vector_db_client: Any       # e.g., Supabase client, pgvector pool, Pinecone, or Qdrant client
    embeddings_model: Any       # e.g., OpenAI, HuggingFace, or Ollama embeddings instance

# 2. Initialize the model and agent
model = OpenAIModel('gpt-4o')
rag_agent = Agent(
    model,
    deps_type=VectorDeps,
    instructions="You are a helpful assistant. Use the retrieve_context tool to answer questions about internal knowledge."
)

# 3. Create the retriever as a tool
@rag_agent.tool
async def retrieve_context(ctx: RunContext[VectorDeps], search_query: str) -> str:
    """
    Retrieve external knowledge sections based on the user's query.
    
    Args:
        ctx: The call context containing dependencies.
        search_query: The natural language search query for the vector database.
    """
    # Generate the embedding for the query
    # (Replace with your specific embedding generation logic)
    query_vector = await ctx.deps.embeddings_model.create(
        input=search_query,
        model="text-embedding-3-small"
    )
    
    # Execute the vector similarity search
    # Example: PostgreSQL/pgvector approach with cosine similarity
    # results = await ctx.deps.vector_db_client.fetch(
    #     'SELECT content FROM document_chunks ORDER BY embedding <-> $1 LIMIT 5',
    #     query_vector
    # )
    
    # Mock retrieved context
    retrieved_records = ["Mocked result 1 based on query", "Mocked result 2 based on query"]
    
    # Format and return the matched context back to the LLM
    formatted_context = "\n\n".join(retrieved_records)
    return f"Retrieved Context:\n{formatted_context}"

# 4. Run the agent
async def main():
    # Provide your actual database and embedding configurations here
    deps = VectorDeps(
        vector_db_client="YOUR_DB_CLIENT",
        embeddings_model="YOUR_EMBEDDINGS_CLIENT"
    )
    
    response = await rag_agent.run(
        "Can you explain the internal policies on data retention?",
        deps=deps
    )
    print(response.output)

if __name__ == "__main__":
    asyncio.run(main())
