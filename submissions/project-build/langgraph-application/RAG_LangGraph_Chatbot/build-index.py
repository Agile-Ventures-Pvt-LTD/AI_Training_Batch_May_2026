from loaders import load_policy_documents
from chunker import chunk_documents
from vectorstore import get_vector_store

docs = load_policy_documents()
chunks = chunk_documents(docs)
get_vector_store(chunks)  