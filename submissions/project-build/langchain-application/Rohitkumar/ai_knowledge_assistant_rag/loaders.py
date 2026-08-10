import re
from pathlib import Path
from typing import List, Dict, Any

from config import RAW_DATA_DIR, SUPPORTED_EXTENSIONS

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


def _clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines: List[str] = []
    seen_headers = set()

    for line in lines:
        if not line:
            continue
        if line.isdigit() and len(line) < 4:
            continue
        if line in seen_headers and len(line) < 80:
            continue
        cleaned_lines.append(line)
        seen_headers.add(line)

    normalized = "\n".join(cleaned_lines)
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{2,}", "\n\n", normalized)
    return normalized.strip()


def _load_pdf(file_path: Path) -> List[Dict[str, Any]]:
    if PdfReader is None:
        raise ImportError("pypdf is required to load PDF documents. Install pypdf or update dependencies.")

    reader = PdfReader(str(file_path))
    pages: List[Dict[str, Any]] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = _clean_text(text)
        if not text:
            continue
        pages.append(
            {
                "source_file": file_path.name,
                "page_number": page_number,
                "document_type": "pdf",
                "text": text,
            }
        )
    return pages


def _load_text_file(file_path: Path, document_type: str) -> List[Dict[str, Any]]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    text = _clean_text(text)
    if not text:
        return []
    return [
        {
            "source_file": file_path.name,
            "page_number": 1,
            "document_type": document_type,
            "text": text,
        }
    ]


def list_document_paths() -> List[Path]:
    if not RAW_DATA_DIR.exists() or not RAW_DATA_DIR.is_dir():
        raise FileNotFoundError(f"Raw document folder not found: {RAW_DATA_DIR}")

    documents = [path for path in RAW_DATA_DIR.iterdir() if path.suffix.lower() in SUPPORTED_EXTENSIONS]
    return sorted(documents)


def load_documents() -> List[Dict[str, Any]]:
    documents: List[Dict[str, Any]] = []
    for path in list_document_paths():
        extension = path.suffix.lower()
        if extension == ".pdf":
            documents.extend(_load_pdf(path))
        elif extension in {".txt", ".md"}:
            documents.extend(_load_text_file(path, extension.strip(".")))
    return documents
