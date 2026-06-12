"""
Tests for the AI Knowledge Assistant RAG pipeline.

"""

import sys
import os
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import RAW_DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from loaders import list_document_paths, load_documents
from chunking import split_text, create_chunks, make_chunk_id
from embeddings import EmbeddingModel


def test_raw_data_directory_exists():
    """Test that the raw data directory exists."""
    assert RAW_DATA_DIR.exists(), f"Raw data directory not found: {RAW_DATA_DIR}"


def test_documents_are_loadable():
    """Test that documents can be found and loaded."""
    paths = list_document_paths()
    assert len(paths) > 0, "No documents found in raw data directory"
    documents = load_documents()
    assert len(documents) > 0, "No documents were loaded"


def test_document_metadata():
    """Test that loaded documents have required metadata fields."""
    documents = load_documents()
    for doc in documents:
        assert "source_file" in doc, "Document missing source_file"
        assert "page_number" in doc, "Document missing page_number"
        assert "text" in doc, "Document missing text"
        assert "document_type" in doc, "Document missing document_type"
        assert isinstance(doc["text"], str), "Document text should be a string"
        assert len(doc["text"]) > 0, "Document text should not be empty"


def test_chunking_basic():
    """Test basic chunking functionality."""
    text = "A " * 2000  
    chunks = split_text(text, chunk_size=500, chunk_overlap=50)
    assert len(chunks) > 0, "Chunking should produce at least one chunk"
    assert all(len(c) <= 500 for c in chunks), "No chunk should exceed chunk_size"
    assert all(len(c) > 0 for c in chunks), "No chunk should be empty"


def test_chunking_overlap():
    """Test that chunking with overlap produces fewer chunks than without."""
    text = "B " * 2000

    chunks_no_overlap = split_text(text, chunk_size=500, chunk_overlap=0)
    chunks_with_overlap = split_text(text, chunk_size=500, chunk_overlap=100)
    
    assert len(chunks_with_overlap) >= len(chunks_no_overlap), (
        "With overlap, we should have at least as many chunks"
    )


def test_chunk_id_generation():
    """Test that chunk IDs are unique and deterministic."""
    id1 = make_chunk_id("test.pdf", 1, 1, "Hello world")
    id2 = make_chunk_id("test.pdf", 1, 2, "Hello world different")
    id3 = make_chunk_id("test.pdf", 1, 1, "Hello world")
    assert id1 != id2, "Different chunks should have different IDs"
    assert id1 == id3, "Same chunk should have the same ID"


def test_chunks_have_metadata():
    """Test that all chunks have required metadata fields."""
    documents = load_documents()
    chunks = create_chunks(documents)
    for chunk in chunks:
        assert "chunk_id" in chunk, "Chunk missing chunk_id"
        assert "source_file" in chunk, "Chunk missing source_file"
        assert "page_number" in chunk, "Chunk missing page_number"
        assert "text" in chunk, "Chunk missing text"
        assert isinstance(chunk["text"], str), "Chunk text should be a string"
        assert len(chunk["text"]) > 0, "Chunk text should not be empty"


def test_embedding_model_loads():
    """Test that the embedding model can be loaded."""
    model = EmbeddingModel("sentence-transformers/all-MiniLM-L6-v2")
    assert model is not None, "Embedding model should load successfully"


def test_embedding_generation():
    """Test that embeddings can be generated."""
    model = EmbeddingModel("sentence-transformers/all-MiniLM-L6-v2")
    documents = load_documents()
    chunks = create_chunks(documents)
    texts = [chunk["text"] for chunk in chunks[:5]]  # Use first 5 chunks
    embeddings = model.embed_documents(texts)
    assert len(embeddings) == len(texts), "Should get one embedding per text"
    assert len(embeddings[0]) > 0, "Embedding should be non-empty"
    assert all(len(e) == len(embeddings[0]) for e in embeddings), "All embeddings should have same dimension"


def test_query_embedding():
    """Test that query embedding works."""
    model = EmbeddingModel("sentence-transformers/all-MiniLM-L6-v2")
    embedding = model.embed_query("What are the major risks?")
    assert len(embedding) > 0, "Query embedding should be non-empty"
    # Embedding dimension should match document embeddings
    doc_embeddings = model.embed_documents(["test document"])
    assert len(embedding) == len(doc_embeddings[0]), "Query embedding should have same dimension as document embeddings"


if __name__ == "__main__":
    test_raw_data_directory_exists()
    print("✓ test_raw_data_directory_exists")
    test_documents_are_loadable()
    print("✓ test_documents_are_loadable")
    test_document_metadata()
    print("✓ test_document_metadata")
    test_chunking_basic()
    print("✓ test_chunking_basic")
    test_chunking_overlap()
    print("✓ test_chunking_overlap")
    test_chunk_id_generation()
    print("✓ test_chunk_id_generation")
    test_chunks_have_metadata()
    print("✓ test_chunks_have_metadata")
    test_embedding_model_loads()
    print("✓ test_embedding_model_loads")
    test_embedding_generation()
    print("✓ test_embedding_generation")
    test_query_embedding()
    print("✓ test_query_embedding")
    print("\nAll tests passed!")