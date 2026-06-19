from __future__ import annotations

from typing import List, Dict

from loaders import load_kb
import config


class SimpleRetriever:
    """A lightweight retriever that ranks KB chunks by query term overlap."""

    def __init__(self, kb_path: str | None = None):
        self.kb_path = kb_path or config.KB_PATH
        self.index = []
        self._build()

    def _build(self):
        self.index = load_kb(self.kb_path)

    def retrieve(self, issue_type: str, query: str, top_k: int | None = None) -> Dict:
        top_k = top_k or config.TOP_K
        q = (query or '').lower()
        
        scored = []
        q_tokens = [t for t in q.split() if t]
        for item in self.index:
            text = (item.get('text') or '').lower()
            score = 0
            for tok in q_tokens:
                score += text.count(tok)
            # boost if filename matches issue_type
            if issue_type and issue_type.lower() in (item.get('source_file') or '').lower():
                score += 1
            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, item in scored[:top_k]:
            results.append({
                "source_file": item.get('source_file'),
                "chunk_id": item.get('chunk_id'),
                "snippet": (item.get('text') or '')[:300].strip(),
            })

        
        if not results and issue_type:
            for item in self.index:
                if issue_type.lower() in (item.get('source_file') or '').lower():
                    results.append({
                        "source_file": item.get('source_file'),
                        "chunk_id": item.get('chunk_id'),
                        "snippet": (item.get('text') or '')[:300].strip(),
                    })
                    if len(results) >= top_k:
                        break

        return {"issue_type": issue_type, "chunks": results}


def build_default_retriever() -> SimpleRetriever:
    return SimpleRetriever()


