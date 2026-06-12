from config import TOP_K


def get_retriever(vector_store):

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K
        }
    )


def retrieve_documents(question,retriever):

    docs = retriever.invoke(question)

    return docs


def build_context(retrieved_docs):

    context_parts = []

    for idx, doc in enumerate(
        retrieved_docs,
        start=1
    ):

        source = doc.metadata.get(
            "source_file",
            "Unknown"
        )

        page = doc.metadata.get(
            "page_number",
            "N/A"
        )

        chunk_id = doc.metadata.get(
            "chunk_id",
            "N/A"
        )

        context_parts.append(
            f"""
Document {idx}

Source: {source}

Page: {page}

Chunk ID: {chunk_id}

Content:
{doc.page_content}
"""
        )

    return "\n".join(context_parts)


def extract_sources(retrieved_docs):

    sources = []

    for doc in retrieved_docs:

        sources.append(
            {
                "source_file":
                doc.metadata.get("source_file"),

                "page_number":
                doc.metadata.get("page_number"),

                "chunk_id":
                doc.metadata.get("chunk_id"),

                "snippet":doc.page_content[:250]
            }
        )

    return sources