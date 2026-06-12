from config import TOP_K

def get_retriever(vector_db):
    return vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": TOP_K
    }
)


def retrieve_context(retriever,query):
     docs = retriever.invoke(query)

     return docs

