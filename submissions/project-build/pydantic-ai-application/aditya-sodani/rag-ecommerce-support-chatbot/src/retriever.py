from src.schema import DocumentChunk
from typing import List
from src.database import get_text_chunks,load_pdf_documents

def retrival_chunks(query: str, docs: List[DocumentChunk] = get_text_chunks(load_pdf_documents()), k: int = 3) -> List[DocumentChunk]:
    scores = []
    query_terms = set(query.lower().split())
    
    for d in docs:
        overlap = len(query_terms & set(d.text.lower().split()))
        scores.append((overlap, d))
    
    scores.sort(reverse=True, key=lambda t: t[0])
    
    return [d for score, d in scores[:k] if score > 0]