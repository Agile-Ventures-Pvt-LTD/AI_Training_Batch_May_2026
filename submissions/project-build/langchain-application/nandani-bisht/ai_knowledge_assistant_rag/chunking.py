import re

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from config import settings


def clean_text(text):

    text = re.sub(
        r"\n+",
        "\n",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def chunk_documents(documents):

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " "
            ]
        )
    )

    split_docs = (
        splitter.split_documents(
            documents
        )
    )

    chunks = []

    for idx, chunk in enumerate(
        split_docs
    ):

        chunk.page_content = clean_text(
            chunk.page_content
        )

        chunk.metadata[
            "chunk_id"
        ] = (
            f"chunk_{idx:05}"
        )

        chunk.metadata[
            "section_title"
        ] = "unknown"

        chunks.append(
            chunk
        )

    return chunks