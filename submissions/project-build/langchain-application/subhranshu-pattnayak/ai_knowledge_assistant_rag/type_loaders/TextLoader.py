from langchain.document_loaders import TextLoader

def load_text(path: str):
    """Load plain text documents with error handling."""
    try:
        loader = TextLoader(path)
        docs = loader.load()
        if not docs:
            raise ValueError("No content extracted from text file.")
        return docs
    except Exception as e:
        raise RuntimeError(f"Text loading failed for {path}: {e}")
