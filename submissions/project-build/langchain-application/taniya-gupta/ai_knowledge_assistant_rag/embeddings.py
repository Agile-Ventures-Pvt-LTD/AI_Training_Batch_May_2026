from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingManager:
    @staticmethod
    def get_embeddings(model_name:"sentence-transformers/all-MiniLM-L6-v2"):
        return HuggingFaceEmbeddings(model_name=model_name)