import json
from groq_client import call_groq
from prompts import query_classification_system

def query_classification(query : str):
    """
    This function will describe the user query into these categories:
    
    - FACTUAL_LOOKUP
    - SUMMARY
    - COMPARISON
    - RISK_ANALYSIS
    - UNANSWERABLE_OR_SPECULATIVE
    - FOLLOW_UP
    - OTHER
    """

    prompt = [
        {"role" : "system", "content" : query_classification_system.format(query=query)},
        {"role" : "user", "content" : query}
    ]

    response = call_groq(prompt)

    try:
        classification = json.loads(response)
    except Exception as e:
        print(e)

    return classification


def source_citations(relevant_chunks, snippet_length: int = 50):
    """
    Function for the Source Citations
    """

    citations = []
    for doc in relevant_chunks:
        source_file = doc.metadata.get("source", "")
        page_number = doc.metadata.get("page", "")
        chunk_id = doc.id
        text = doc.page_content.strip()

        snippet = text[:snippet_length] + ("..." if len(text) > snippet_length else "")

        citations.append({
            "source_file": source_file,
            "page_number": page_number,
            "chunk_id": chunk_id,
            "snippet": snippet
        })

    return citations
