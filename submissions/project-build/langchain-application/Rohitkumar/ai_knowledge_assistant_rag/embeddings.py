from typing import List

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class EmbeddingModel:
    def __init__(self, model_name: str):
        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers is required for embeddings. Install sentence-transformers or update dependencies."
            )
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        embedding = self.model.encode([query], show_progress_bar=False, convert_to_numpy=True)
        return embedding[0].tolist()
