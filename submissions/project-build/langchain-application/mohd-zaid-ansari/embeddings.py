from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def get_embedding_model():

    embedding_model = embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    return embedding_model

