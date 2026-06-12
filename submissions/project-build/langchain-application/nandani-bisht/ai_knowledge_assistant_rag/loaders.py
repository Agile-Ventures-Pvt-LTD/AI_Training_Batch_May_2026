from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

from langchain_core.documents import Document

from config import settings


SUPPORTED = {
    ".pdf",
    ".txt",
    ".md"
}


def load_documents():

    docs = []

    if not settings.RAW_DATA_DIR.exists():
        raise FileNotFoundError(
            "data/raw folder missing"
        )

    files = list(
        settings.RAW_DATA_DIR.glob("*")
    )

    if not files:
        raise ValueError(
            "No files found inside data/raw"
        )

    for file in files:

        if file.suffix.lower() not in SUPPORTED:
            print(f"Skipped: {file.name}")
            continue

        try:

            if file.suffix == ".pdf":

                loader = PyPDFLoader(
                    str(file)
                )

                pages = loader.load()

                for p in pages:

                    p.metadata.update({
                        "source_file": file.name,
                        "document_type": "pdf"
                    })

                docs.extend(pages)

            else:

                loader = TextLoader(
                    str(file),
                    encoding="utf-8"
                )

                loaded = loader.load()

                for d in loaded:

                    d.metadata.update({
                        "source_file": file.name,
                        "page_number": None,
                        "document_type": file.suffix
                    })

                docs.extend(loaded)

        except Exception as e:

            print(
                f"Load failed: {file.name}"
            )

            print(e)

    return docs