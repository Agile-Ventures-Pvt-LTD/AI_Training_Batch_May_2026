import os
from dotenv import load_dotenv
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

load_dotenv()
os.environ["POLICY_DATA_PATH"] = os.getenv("POLICY_DATA_PATH", "data/policies")


documents = DirectoryLoader(
    os.environ["POLICY_DATA_PATH"],
    glob="**/*.md",
    loader_cls=lambda path: TextLoader(path, encoding="utf-8")
).load()

header_split = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

try:
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on = header_split,
        strip_headers = False
    )
except Exception as e:
    print(e)

policies_extracted_chunks = []

for doc in documents:
    splits = markdown_splitter.split_text(doc.page_content)
    
    for split in splits:
        split.metadata.update(doc.metadata)  
    
    policies_extracted_chunks.extend(splits)


recursive_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=700,   
    chunk_overlap=100, 
)

try:
    policies_chunks = recursive_splitter.split_documents(policies_extracted_chunks)
except Exception as e:
    print(e)