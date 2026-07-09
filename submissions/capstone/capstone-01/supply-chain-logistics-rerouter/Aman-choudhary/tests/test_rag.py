import os
import unittest
from pathlib import Path
from src.rag import (load_knowledge_base,split_documents,build_vector_store,get_relevant_rules,)
DATA_DIR = Path("data")
KB_FILE = DATA_DIR / "logistics_knowledge_base.txt"
class TestRAGPipeline(unittest.TestCase):

    def test_knowledge_base_exists(self):
        """Ensure the knowledge base text file exists."""
        self.assertTrue(KB_FILE.exists(), f"Missing KB file: {KB_FILE}")

    def test_load_knowledge_base(self):
        """Ensure KB loads and is not empty."""
        kb_text = load_knowledge_base()
        self.assertIsInstance(kb_text, str)
        self.assertGreater(len(kb_text.strip()), 10)

    def test_split_documents(self):
        """Ensure documents are chunked properly."""
        kb_text = load_knowledge_base()
        docs = split_documents(kb_text)

        self.assertIsInstance(docs, list)
        self.assertGreater(len(docs), 0, "No chunks produced")
        self.assertTrue(hasattr(docs[0], "page_content"))

    def test_vector_store_build(self):
        """Ensure FAISS index builds without errors."""
        vector_store = build_vector_store()
        self.assertTrue(hasattr(vector_store, "index"))

    def test_relevant_rules(self):
        """RAG should retrieve relevant chunks for a query."""
        query = "What is a warehouse fit check?"
        result = get_relevant_rules(query)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result.strip()), 10)
        self.assertIn("warehouse", result.lower())


if __name__ == "__main__":
    unittest.main()