from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import VECTOR_STORE_PATH, TOP_K


vectordb_global = None

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vectorstore(chunks):
    texts = [c["text"] for c in chunks]
    metadatas = [
        {
            "chunk_id": c["chunk_id"],
            "source_file": c["source_file"],
            "policy_domain": c["policy_domain"]
        }
        for c in chunks
    ]

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas,
        persist_directory=VECTOR_STORE_PATH
    )

    vectordb.persist()
    return vectordb


def get_retriever(vectordb):
    return vectordb.as_retriever(search_kwargs={"k": TOP_K})