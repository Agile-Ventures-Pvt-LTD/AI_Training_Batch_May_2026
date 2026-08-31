from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL, VECTOR_DB_PATH, TOP_K


def init_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings


def create_vector_db(documents):
    embeddings = init_embeddings()
    
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    return vector_db


def load_vector_db():
    embeddings = init_embeddings()
    vector_db = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )
    return vector_db


def search_documents(vector_db, query, k=TOP_K):
    results = vector_db.similarity_search_with_score(query, k=k)
    return results


if __name__ == "__main__":
    from loaders import load_md_documents
    from chunking import chunk_documents
    import os
    
    print("Loading documents...")
    docs = load_md_documents("data/policies")
    print(f"Loaded {len(docs)} documents")
    
    print("Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")
    
    print("Creating vector database...")
    db = create_vector_db(chunks)
    print(f"Vector database created at: {VECTOR_DB_PATH}")
    print(f"Contents: {os.listdir(VECTOR_DB_PATH)}")
    
    print("\nTesting search...")
    results = search_documents(db, "travel policy")
    print(f"Found {len(results)} results")
    for doc, score in results[:2]:
        print(f"  Score: {score:.2f} | Source: {doc.metadata.get('source_file')}")
