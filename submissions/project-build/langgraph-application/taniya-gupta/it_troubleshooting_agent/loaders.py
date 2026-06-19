import os
import config
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_domain(filename):
    name = os.path.basename(filename)
    for key, domain in [
        ("vpn", "VPN"),
        ("email", "OUTLOOK_EMAIL"),
        ("laptop", "LAPTOP_PERFORMANCE"),
        ("network", "NETWORK_CONNECTIVITY"),
        ("password", "PASSWORD_RESET"),
        ("printer", "PRINTER")]:
        if key in name:
            return domain
    return "DONT KNOW"

def load_kb(kb_path):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP)
    
    documents = []
    for path in Path(kb_path).iterdir():
        if path.is_file() and path.suffix in (".md", ".txt"):
            domain = get_domain(path.name)
            content = path.read_text(encoding="utf-8")        
            documents.extend([
                {
                    "content": chunk,
                    "metadata": {
                        "source_file": path.name,
                        "issue_domain": domain,
                        "chunk_id": f"{domain.lower()}_chunk_{idx + 1:03d}"}}
                for idx, chunk in enumerate(text_splitter.split_text(content))])
    return documents