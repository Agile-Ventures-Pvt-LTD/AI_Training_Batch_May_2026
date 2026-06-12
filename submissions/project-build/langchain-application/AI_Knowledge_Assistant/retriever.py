from vector_store import get_vector_store
from config import TOP_K

def get_retriever(db=None):
    if db is None:
        db = get_vector_store()
    
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )
    return retriever