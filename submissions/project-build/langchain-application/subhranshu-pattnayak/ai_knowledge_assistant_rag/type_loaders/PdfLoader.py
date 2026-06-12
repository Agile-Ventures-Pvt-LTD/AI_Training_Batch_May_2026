from langchain.document_loaders import PyPDFLoader

def load_pdf(path: str):
    """Load PDF documents with error handling."""
    try:
        loader = PyPDFLoader(path)
        docs = loader.load()
        if not docs:
            raise ValueError("No content extracted from PDF.")
        return docs
    except Exception as e:
        raise RuntimeError(f"PDF loading failed for {path}: {e}")