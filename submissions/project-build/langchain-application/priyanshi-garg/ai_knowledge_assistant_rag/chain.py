from langchain_groq import ChatGroq
from retriever import retrieve
from config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile"
)


def answer_question(question):

    docs = retrieve(question)

    context = "\n\n".join(
        d.page_content for d in docs
    )

    prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

If answer is not in context say:
"I could not find this in the provided documents."

-------------------
CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": [
            {
                "file": d.metadata.get("source_file"),
                "page": d.metadata.get("page"),
                "chunk": d.metadata.get("chunk_id")
            }
            for d in docs
        ],
        "confidence": "HIGH" if docs else "LOW",
        "answerability": "ANSWERED" if docs else "NOT_FOUND",
        "retrieved_chunks": docs
    }