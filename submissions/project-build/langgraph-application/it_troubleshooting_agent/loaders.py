from __future__ import annotations

import os
from typing import List, Dict

import config


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP
    if chunk_size <= 0:
        return [text]
    chunks: List[str] = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        start = end - overlap if end - overlap > start else end
    return chunks


def load_kb(kb_path: str | None = None) -> List[Dict]:
    """Load markdown/text files from KB path and chunk them.

    Returns list of chunk dicts with metadata.
    """
    kb_path = kb_path or config.KB_PATH
    chunks = []
    if not os.path.isdir(kb_path):
        return chunks

    for fname in sorted(os.listdir(kb_path)):
        if not (fname.endswith('.md') or fname.endswith('.txt')):
            continue
        full = os.path.join(kb_path, fname)
        try:
            with open(full, 'r', encoding='utf-8') as fh:
                text = fh.read()
        except Exception:
            continue

        text_chunks = chunk_text(text)
        for i, c in enumerate(text_chunks, start=1):
            chunks.append({
                "source_file": fname,
                "issue_domain": fname.replace('_troubleshooting_guide.md', '').upper(),
                "chunk_id": f"{fname}::chunk_{i}",
                "text": c,
            })

    return chunks



