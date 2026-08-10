

import os
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name=os.getenv("EMBEDDING_MODEL"))
