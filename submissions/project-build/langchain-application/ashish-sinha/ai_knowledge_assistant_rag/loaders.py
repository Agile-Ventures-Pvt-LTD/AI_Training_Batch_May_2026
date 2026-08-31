from pathlib import Path
import re
from langchain_community.document_loaders import (PyPDFLoader,TextLoader,UnstructuredMarkdownLoader)

supported_files = [".pdf",".txt",".md"]

def load_documents(folder_path):
    documents = []

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            f"{folder_path} does not exist"
        )

    for file in folder.iterdir():

        if file.suffix.lower() not in supported_files:
            continue

        try:

            if file.suffix == ".pdf":
                loader = PyPDFLoader(str(file))

            elif file.suffix == ".md":
                loader = UnstructuredMarkdownLoader(str(file))

            else:
                loader = TextLoader(str(file))

            docs = loader.load()

            for doc in docs:

                doc.metadata["source_file"] = file.name

            documents.extend(docs)

        except Exception as e:

            print( f"Failed loading {file}: {e}")

    return documents

def clean_text(text):

    text = re.sub(r"\n+","\n",text)

    text = re.sub(r"\s+"," ",text)

    return text.strip()