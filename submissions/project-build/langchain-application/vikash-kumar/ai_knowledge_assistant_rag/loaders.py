from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader,TextLoader

def load_documents(data_path):

    documents = []

    path = Path(data_path)

    if not path.exists():
        raise FileNotFoundError(f"{data_path} does not exist")

    files = list(path.glob("*"))

    print(f"Found {len(files)} files")

    for file in files:

        print(f"Processing: {file.name}")

        try:

            if file.suffix.lower() == ".pdf":

                loader = PyPDFLoader(str(file))

                docs = loader.load()

                for d in docs:
                    d.metadata["source_file"] = file.name
                    d.metadata["document_type"] = "pdf"

                documents.extend(docs)

            elif file.suffix.lower() in [".txt", ".md"]:

                loader = TextLoader(
                    str(file),
                    encoding="utf-8"
                )

                docs = loader.load()

                for d in docs:
                    d.metadata["source_file"] = file.name
                    d.metadata["document_type"] = "text"

                documents.extend(docs)

        except Exception as e:

            print(
                f"Failed loading {file.name}: {e}"
            )

    print(
        f"Total loaded pages/documents: {len(documents)}"
    )

    return documents