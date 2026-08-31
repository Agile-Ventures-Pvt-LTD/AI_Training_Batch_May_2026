from schema import DocsChunk
from typing import List
from database import pdf_chunks

def retrival_chunks(query: str, docs: List[DocsChunk] = pdf_chunks(), k: int = 3) -> List[DocsChunk]:
    scores = []
    query_terms = set(query.lower().split())
    
    for d in docs:
        overlap = len(query_terms & set(d.text.lower().split()))
        scores.append((overlap, d))
    
    scores.sort(reverse=True, key=lambda t: t[0])
    
    return [d for score, d in scores[:k] if score > 0]