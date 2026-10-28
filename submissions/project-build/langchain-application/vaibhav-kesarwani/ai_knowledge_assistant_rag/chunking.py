import os
import json
from dotenv import load_dotenv
from loaders import pdf_loader 
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
os.environ["CHUNK_SIZE"] = os.getenv("CHUNK_SIZE")
os.environ["CHUNK_OVERLAP"] = os.getenv("CHUNK_OVERLAP")

output_file = "data/processed/chunks.json"
os.makedirs(os.path.dirname(output_file), exist_ok=True)


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=int(os.environ["CHUNK_SIZE"]),
    chunk_overlap=int(os.environ["CHUNK_OVERLAP"])
)

amazon_chunks = pdf_loader.load_and_split(text_splitter)

json_chunks = []
for i, doc in enumerate(amazon_chunks):
    chunk = {
        "chunk_id": f"chunk_{i}",
        "source_file": doc.metadata.get("source", ""),
        "page_number": doc.metadata.get("page", None),
        "section_title": doc.metadata.get("title", ""),
        "text": doc.page_content
    }
    json_chunks.append(chunk)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_chunks, f, indent=2, ensure_ascii=False)

print(f"Chunks saved to {output_file}")
