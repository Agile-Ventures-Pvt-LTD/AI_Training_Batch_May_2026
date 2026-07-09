from pathlib import Path
from functools import lru_cache

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
DATA_DIR = Path("data")
KNOWLEDGE_BASE_FILE = DATA_DIR / "logistics_knowledge_base.txt"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
@lru_cache(maxsize=1)
def get_embeddings():
    """Load the embedding model once."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
def load_knowledge_base() -> str:
    """Load logistics knowledge base text file."""
    if not KNOWLEDGE_BASE_FILE.exists():
        raise FileNotFoundError(f"File not found: {KNOWLEDGE_BASE_FILE}")

    with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as file:
        return file.read()
def split_documents(document_text: str) -> list[Document]:
    """Split KB into chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.create_documents([document_text])
@lru_cache(maxsize=1)
def build_vector_store():
    """Build FAISS vector store. Cached after first build."""
    kb_text = load_knowledge_base()
    documents = split_documents(kb_text)
    embeddings = get_embeddings()

    return FAISS.from_documents(documents, embeddings)
@lru_cache(maxsize=1)
def get_retriever():
    """Create retriever."""
    vector_store = build_vector_store()
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
def get_relevant_rules(query: str) -> str:
    """Retrieve logistics rules. Returns formatted text."""
    retriever = get_retriever()
    docs = retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in docs)
def get_relevant_rule_documents(query: str) -> list[Document]:
    """Return retrieved chunks as list. Useful for reports."""
    retriever = get_retriever()
    return retriever.invoke(query)

if __name__ == "__main__":
    question = "What is WAREHOUSE_FIT_CHECK?"
    print("\n=== Retrieved Knowledge ===\n")
    print(get_relevant_rules(question))