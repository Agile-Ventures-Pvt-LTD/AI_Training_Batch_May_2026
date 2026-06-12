def format_output(answer, docs):

    sources = []

    for doc in docs:

        sources.append({
            "source": doc.metadata.get(
                "source_file",
                "unknown"
            ),
            "page": doc.metadata.get(
                "page",
                "N/A"
            ),
            "chunk": doc.metadata.get(
                "chunk_id",
                "N/A"
            )
        })

    return {
        "answer": answer,
        "sources": sources
    }