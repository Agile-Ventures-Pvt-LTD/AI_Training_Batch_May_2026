from langchain_text_splitters import CharacterTextSplitter

def chunk_documents(documents, chunk_size=800, chunk_overlap=100):
    """Split documents into token-aware chunks for embedding and retrieval. Returns a list of chunked Document objects."""
    if not documents:
        raise ValueError("No documents provided for chunking.")

    try:
        splitter = CharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        chunks = splitter.split_documents(documents)

        if not chunks:
            raise ValueError("Chunking produced no output. Check input documents.")

        return chunks

    except Exception as e:
        raise RuntimeError(f"Chunking failed: {e}")
