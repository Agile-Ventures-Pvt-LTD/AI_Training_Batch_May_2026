from retriever import retriever
from logger import query_logging
from groq_client import call_groq
from prompts import system_assistant, user_assistant_template
from config import query_classification, source_citations

def call_assistant(query: str):
    content = query_classification(query)
    relevant_chunks = retriever.invoke(query)
    sources = source_citations(relevant_chunks=relevant_chunks)

    context_list = [d.page_content for d in relevant_chunks]
    context_for_query = "\n---\n".join(context_list)

    prompt = [
        {"role" : "system", "content" : system_assistant},
        {"role" : "user", "content" : user_assistant_template.format(
            question=query,
            context=context_for_query
        )}
    ]

    response = call_groq(prompt=prompt)

    query_logging(question=query, query_type=content, retrieved_sources=sources, response=response)

    return response