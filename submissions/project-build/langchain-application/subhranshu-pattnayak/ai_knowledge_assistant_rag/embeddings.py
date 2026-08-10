from langchain_huggingface import HuggingFaceEmbeddings

def init_embedding(model_name: str = "sentence-transformers/all-mpnet-base-v2"):
    """Initialize HuggingFace embedding model."""
    try:
        embedding_model = HuggingFaceEmbeddings(model_name=model_name)
        return embedding_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedding model {model_name}: {e}")