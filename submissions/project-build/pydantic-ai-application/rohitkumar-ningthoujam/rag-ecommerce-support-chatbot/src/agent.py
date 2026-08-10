import os
from pydantic_ai import Agent
from typing import List
from database import retriever
from guaedrails_config import validattion_user_input, validate_output
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
from groq import Groq
client = Groq()
rag_prompt = """
You are an enterprise knowledge assistant. Answer the user question using only the provided context.
Rules:
- Do not use outside knowledge.
- If the answer is not available in the context, say: 'I could not find this in the provided documents.'
- Cite the source file, page number, or chunk ID for each key claim.
- Do not invent numbers, dates, risks, or business conclusions.
- Keep the answer clear and business-friendly.

Question: {question}

Retrieved Context: {context}
"""

def retrieve_docs(query: str) -> List[str]:
    """
    Retrieve relevant documents for a query.
    In real life, call your vector DB / search index here.
    """
    
    fake_corpus = retriever
    
    return [text for key, text in fake_corpus.items() if key in query.lower()]


rag_agent = Agent(
    "groq:openai/gpt-oss-120b",
    system_prompt=(
        rag_prompt
    ),
    tools=[retrieve_docs],
)

async def main():

    print("Agent support is active")
    print("Type 'exit' to quit")
    print()

    while True:
        try:
            user_query = input("Enter your query: ")
            if user_query.lower() in ("exit", "quit"):
                break
            if validattion_user_input:
                result = await rag_agent.run(user_query)
                print(validate_output(result.output))
            else:
                return "validation fail " 
            print()
            print(json.dumps(result, indent=2))
            print()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())