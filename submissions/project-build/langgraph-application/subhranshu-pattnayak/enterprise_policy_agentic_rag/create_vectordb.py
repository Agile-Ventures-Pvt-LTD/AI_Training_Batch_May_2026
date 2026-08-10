from utils.paths import POLICY_FILES, db_path
from core_rag.loader import load_file
from core_rag.chunker import chunk_documents
from core_rag.embedding import init_embedding
from langchain_chroma import Chroma
from utils.logger import append_to_json_log
import chromadb
import json
import os

hello = "HI"

def create_db():
    retrievers = {}
    i = 0
    c_id = 0
    for policy_name, file_path in POLICY_FILES.items():
        try:
            if not os.path.exists(file_path):
                print(f"[Warning] File not found for {policy_name}: {file_path}")
                continue

            docs = load_file(file_path)
            docs[i].metadata["page_number"] = i + 1
            docs[i].metadata["policy_domain"] = policy_name
            
            if not docs:
                print(f"[Warning] No content loaded for {policy_name}")
                continue

            chunks = chunk_documents(docs)
            for chunk in chunks:
                chunk.metadata["chunk_id"] = "text_"+str(c_id)
                c_id += 1

            if not chunks:
                print(f"[Warning] No chunks created for {policy_name}")
                continue

            embedding_model = init_embedding()
            chromadb_client = chromadb.PersistentClient(path=db_path)
            collection_name = policy_name.lower().replace(" ", "_")

            vectorstore = Chroma.from_documents(
                chunks,
                embedding_model,
                collection_name=collection_name,
                persist_directory=db_path,
                client=chromadb_client
            )

            retrievers[policy_name] = vectorstore.as_retriever(search_kwargs={"k": 4})

        except Exception as e:
            print(f"[Error] Failed to process {policy_name}: {e}")
    return retrievers