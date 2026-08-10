from rag import load_documents, chunk_documents, create_vector_store, get_retriever
from graph import builder
from langchain_core.prompts import ChatPromptTemplate
import asyncio
import json

# Answer Generation Prompt

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are Supply Chain Logistics Rerouter.

Rules:

1. Answer ONLY from retrieved context.

2. Never use outside knowledge.

3. If context is missing,
say

"I couldn't find relevant information."

4. Always mention citations.

5. Never hallucinate.

Retrieved Context

{context}
"""
        ),
        ("human", "{question}")
    ]
)


# Reflection Prompt

REFLECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Review the generated answer.

Check

- Grounded?
- Citations?
- Hallucination?
- Confidence?

Return JSON.
"""
        ),
        (
            "human",
            """
Question

{question}

Answer

{answer}

Context

{context}
"""
        )
    ]
)

async def main():

    main = builder()

    await main.connect()

    print("=" * 70)
    print("Supply Chain Logistics Rerouter")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        query = input("\nYou: ").strip()

        if query.lower() in ["exit", "quit"]:

            break

        response = await main.chat(query)
        
        output_dir = "outputs"
        output_dir.mkdir(exist_ok=True)

        file_path = output_dir / "INC-001_reroute_advisory_report.json"
        


        if file_path.exists():

            existing_data = json.loads(file_path.read_text(encoding="utf-8"))
        else:
             existing_data = []

        existing_data.append(response)

        file_path.write_text(
        json.dumps(existing_data, indent=4, default=str),
        encoding="utf-8"
)

        print("\nAssistant\n")

        print(json.dumps(response, indent=4))

    await main.close()


if __name__ == "__main__":
    asyncio.run(main())
