def build_sources(docs):
     sources = []

     for d in docs:
       sources.append(
        {
            "source_file":d.metadata.get("source_file"),

            "page_number":d.metadata.get("page"),

            "chunk_id":d.metadata.get("chunk_id"),

            "snippet":d.page_content[:250]
        }
    )
    
     return sources
