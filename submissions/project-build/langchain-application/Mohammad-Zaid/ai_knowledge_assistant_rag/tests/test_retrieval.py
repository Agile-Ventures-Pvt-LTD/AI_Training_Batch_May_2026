
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from loaders import load_pdf
from chunking import chunk_documents, set_document_metadata
from vector_store import vector_db
from retriever import retrieve_documents


def test_load_pdf():
    """Test PDF loading"""
    pdf_path = "./data/raw/Amazon-2025-Annual-Report.pdf"
    docs = load_pdf(pdf_path)
    assert docs is not None
    print(f"✓ Loaded {len(docs)} pages")


def test_chunk():
    """Test chunking"""
    pdf_path = "./data/raw/Amazon-2025-Annual-Report.pdf"
    docs = load_pdf(pdf_path)
    if docs:
        cleaned = [set_document_metadata(doc, pdf_path) for doc in docs]
        chunks = chunk_documents(cleaned)
        assert len(chunks) > 0
        print(f"✓ Created {len(chunks)} chunks")


def test_retrieval():
    """Test retrieval"""
    query = "What are the financial highlights?"
    docs = retrieve_documents(vector_db, query)
    assert docs is not None
    print(f"✓ Retrieved {len(docs)} documents")


if __name__ == "__main__":
    print("\nRunning tests...\n")
    try:
        test_load_pdf()
        test_chunk()
        test_retrieval()
        print("\n✓ All tests passed")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
