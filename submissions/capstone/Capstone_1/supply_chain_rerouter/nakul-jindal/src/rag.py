from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

KB_PATH = Path("data/logistics_knowledge_base.txt")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 4

_vectorstore = None


def load_and_chunk_kb() -> list[Document]:
    text = KB_PATH.read_text(encoding="utf-8")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    docs = splitter.create_documents([text])

    for i, chunk in enumerate(docs):
        chunk.metadata = {
            "chunk_id": f"chunk_{i:04d}",
            "source_file": KB_PATH.name,
        }

    print(f"Created {len(docs)} chunks from {KB_PATH.name}")
    return docs


def get_vector_store():
    global _vectorstore
    if _vectorstore is None:
        docs = load_and_chunk_kb()
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        _vectorstore = FAISS.from_documents(docs, embeddings)
    return _vectorstore


def retrieve_rules(query: str, top_k: int = TOP_K) -> list[dict]:
    db = get_vector_store()
    results = db.similarity_search_with_score(query, k=top_k)
    return _format_results(results)


def _format_results(results) -> list[dict]:
    formatted = []
    for doc, score in results:
        formatted.append({
            "chunk_id": doc.metadata.get("chunk_id", ""),
            "source_file": doc.metadata.get("source_file", ""),
            "content": doc.page_content,
            "relevance_score": round(max(0.0, 1.0 - score), 4),
        })
    return formatted


def get_relevant_rules_text(query: str, top_k: int = TOP_K) -> str:
    chunks = retrieve_rules(query, top_k)
    return "\n\n".join(c["content"] for c in chunks)


if __name__ == "__main__":
    question = "What is WAREHOUSE_FIT_CHECK?"
    for r in retrieve_rules(question):
        print(r)
