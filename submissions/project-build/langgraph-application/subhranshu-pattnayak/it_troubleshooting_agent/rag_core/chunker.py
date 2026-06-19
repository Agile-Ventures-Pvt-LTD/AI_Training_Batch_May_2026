from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)
        cid = 0
        for chunk in chunks:
            chunk.metadata["chunk_id"] = "text_"+str(cid)
            cid += 1
        return chunks
    except Exception as e:
        print(f"Error: {e}")