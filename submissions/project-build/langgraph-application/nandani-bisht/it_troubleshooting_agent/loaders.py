import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import KB_PATH, CHUNK_SIZE, CHUNK_OVERLAP


ISSUE_DOMAIN_MAP = {
    "vpn_troubleshooting_guide": "VPN",
    "email_outlook_troubleshooting_guide": "OUTLOOK_EMAIL",
    "laptop_performance_guide": "LAPTOP_PERFORMANCE",
    "password_reset_guide": "PASSWORD_RESET",
    "network_connectivity_guide": "NETWORK_CONNECTIVITY",
    "printer_troubleshooting_guide": "PRINTER",
}


def get_issue_domain(filename):
    base = os.path.splitext(os.path.basename(filename))[0].lower()
    for key, domain in ISSUE_DOMAIN_MAP.items():
        if key in base:
            return domain 
    return "GENERAL"


def load_knowledge_base(kb_path=None):
    if kb_path is None:
        kb_path = KB_PATH

    kb_path = os.path.abspath(kb_path)
    if not os.path.exists(kb_path):
        raise FileNotFoundError(f"Knowledge base path not found: {kb_path}")

    loader = DirectoryLoader(
        kb_path,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=False,
        use_multithreading=False,
    )

    documents = loader.load()

    txt_loader = DirectoryLoader(
        kb_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=False,
        use_multithreading=False,
    )

    try:
        txt_docs = txt_loader.load()
        documents.extend(txt_docs)
    except Exception:
        pass

    for doc in documents:
        source = doc.metadata.get("source", "")
        filename = os.path.basename(source)
        issue_domain = get_issue_domain(filename)
        doc.metadata["source_file"] = filename
        doc.metadata["issue_domain"] = issue_domain

    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        source_file = chunk.metadata.get("source_file", "unknown")
        base_name = os.path.splitext(source_file)[0]
        chunk.metadata["chunk_id"] = f"{base_name}_chunk_{i:03d}"

    return chunks


def load_and_chunk_knowledge_base(kb_path=None):
    documents = load_knowledge_base(kb_path)
    chunks = chunk_documents(documents)
    print(f"Loaded {len(documents)} documents and created {len(chunks)} chunks from knowledge base.")
    return chunks

