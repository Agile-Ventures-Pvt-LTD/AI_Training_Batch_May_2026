from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=800,
    chunk_overlap=100
)
    chunks = text_splitter.split_documents(documents)

    return chunks