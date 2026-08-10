from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        return text_splitter.split_documents(docs)
    except Exception as e:
        print(f"Error: {e}")