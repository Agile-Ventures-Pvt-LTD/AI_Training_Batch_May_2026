from langchain_community.document_loaders import DirectoryLoader, TextLoader
from utils.paths import issue_domains
import os

def load_files(path):
    """
    Loads all Markdown (.md) files from the given directory using LangChain's DirectoryLoader.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory not found: {path}")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Path is not a directory: {path}")

    try:
        loader = DirectoryLoader(
            path,
            glob=["**/*.md", "**/*txt"],
            loader_cls=lambda path: TextLoader(path, encoding="utf-8"),
            show_progress=True
        )

        documents = loader.load()

        for doc in documents:
            doc.metadata["issue_domain"] = issue_domains[doc.metadata["source"][20:]]
        return documents

    except Exception as e:
        print(f"Error: {e}")
        return []