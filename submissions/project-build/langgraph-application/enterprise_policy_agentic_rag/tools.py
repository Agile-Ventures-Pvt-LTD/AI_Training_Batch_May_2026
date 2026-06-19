def format_chunks(chunks):
    return [
        {
            "text": c.page_content,
            "metadata": c.metadata
        }
        for c in chunks
    ]


def format_sources(docs):
    return [
        {
            "source_file": d.metadata.get("source_file", ""),
            "policy_domain": d.metadata.get("policy_domain", ""),
            "chunk_id": d.metadata.get("chunk_id", ""),
            "snippet": d.page_content[:300]
        }
        for d in docs
    ]