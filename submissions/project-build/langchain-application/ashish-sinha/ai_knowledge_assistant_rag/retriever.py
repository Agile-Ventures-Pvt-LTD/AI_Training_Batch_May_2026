from config import TOP_K

class Retriever:

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query: str):

        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=TOP_K
        )

        retrieved_docs = []

        for doc, score in results:

            doc.metadata["similarity_score"] = round(float(score),4)

            retrieved_docs.append(doc)

        return retrieved_docs


def format_context(documents):

    context = []

    for doc in documents:

        source_file = doc.metadata.get("source_file","Unknown")

        page_number = doc.metadata.get("page_number","N/A")

        chunk_id = doc.metadata.get("chunk_id","Unknown")

        similarity_score = doc.metadata.get("similarity_score","N/A")

        context.append(
            f"""
SOURCE_FILE: {source_file}
PAGE_NUMBER: {page_number}
CHUNK_ID: {chunk_id}
SIMILARITY_SCORE: {similarity_score}

CONTENT:
{doc.page_content}
"""
        )

    return "\n\n".join(context)