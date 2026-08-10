
from pathlib import Path
from langchain_community.document_loaders import TextLoader
import chromadb
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


#======================================load documents==========================================

def load_documents():

    documents = []

    md_files = [
        "data/knowledge_base/email_outlook_troubleshooting_guide.md",
        "data/knowledge_base/laptop_performance_guide.md",
        "data/knowledge_base/network_connectivity_guide.md",
        "data/knowledge_base/password_reset_guide.md",
        "data/knowledge_base/printer_troubleshooting_guide.md",
        "data/knowledge_base/vpn_troubleshooting_guide.md"
    ]

    for file_path in md_files:

        loader = TextLoader(
            file_path=file_path,
            encoding="utf-8"
        )

        docs = loader.load()

        guide_domain = Path(file_path).stem

        for doc in docs:
            doc.metadata = {
                "source_file": Path(file_path).name,
                "guide_domain": guide_domain,
                "page_number": ""
            }

        documents.extend(docs)

    return documents

#========================================chunking==========================================

documents=load_documents()
def split_documents():

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120
    )

    chunks = splitter.split_documents(documents)

# for idx, chunk in enumerate(chunks):

#     chunk.metadata["chunk_id"] = f"chunk_{idx}"

    for idx, chunk in enumerate(chunks):

            guide = chunk.metadata["guide_domain"]

            chunk.metadata = {
                "chunk_id": f"{guide.lower().replace(' ', '_')}_{idx}",
                "source_file": chunk.metadata["source_file"],
                "issue_domain": guide,
                "text": chunk.page_content
            }

    return chunks


#==========================================vectordb========================================



chunks=split_documents()


def create_vector_db():

    client = chromadb.PersistentClient(
        path="./vector_store"
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        client=client
    )

    return vectordb

create_vector_db()