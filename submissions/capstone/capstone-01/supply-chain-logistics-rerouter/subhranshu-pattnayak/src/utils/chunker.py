from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(docs):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=150)
        return text_splitter.split_documents(docs)
    except Exception as e:
        print(f"Error: {e}")