
from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any

import chromadb
import fitz  # PyMuPDF

from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    """
    Handles:
    - PDF parsing
    - Chunk creation
    - Embeddings
    - Chroma persistence
    - Retrieval
    """

    COLLECTION_NAME = "seller_guide"

    def __init__(
        self,
        persist_directory: str = "chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.persist_directory = persist_directory

        self.embedding_model = SentenceTransformer(
            embedding_model
        )

        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False
            ),
        )

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={
                "description": "eBay Advanced Business Seller Guide"
            },
        )

        logger.info(
            "Chroma collection initialized: %s",
            self.COLLECTION_NAME,
        )


    @staticmethod
    def parse_pdf(pdf_path: str) -> str:
        """
        Extract text from a PDF using PyMuPDF.
        """

        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        logger.info("Reading PDF: %s", pdf_path)

        document = fitz.open(pdf_path)

        text_pages: List[str] = []

        try:
            for page in document:
                text_pages.append(page.get_text())
        finally:
            document.close()

        full_text = "\n".join(text_pages)

        logger.info(
            "Extracted %s characters",
            len(full_text),
        )

        return full_text

    @staticmethod
    def create_chunks(text: str) -> List"""
        Creates semantic-friendly chunks.

        Chunk size and overlap were selected
        to preserve operational workflow context.
        """

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,