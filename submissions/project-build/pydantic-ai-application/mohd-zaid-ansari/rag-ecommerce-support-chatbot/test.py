from src.database import load_pdf, create_chunks, get_metadata, get_embedding_model, create_vector_store, index_chunk_to_vectorstore
from src.config import DATASET_PATH, VECTORE_STORE_PATH, EMBEDDING_MODEL,CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
pdf=load_pdf(DATASET_PATH)
print("length:", len(pdf))

chunking=create_chunks(pdf)
print("Chunk Length:", len(chunking))
print("Chunk is:", chunking[0].metadata)

metadatas=get_metadata(chunking)
print("Chunk is:", metadatas[0].metadata)

embedd_doc=get_embedding_model()
print("Embedding initialized")

vector_db=create_vector_store(embedd_doc)
print("Data:", vector_db)

index=index_chunk_to_vectorstore(chunking, vector_db)
print("Index:", index)