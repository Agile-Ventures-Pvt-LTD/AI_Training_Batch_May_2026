import os
from type_loaders.type_loaders import load_documents

def load_directory(directory_path: str):
    """Load all supported documents from a directory into LangChain format."""
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    file_paths = [
        os.path.join(directory_path, f)
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
    ]

    if not file_paths:
        raise ValueError(f"No files found in directory: {directory_path}")

    documents = load_documents(file_paths)

    if not documents:
        raise RuntimeError(f"No documents loaded from directory: {directory_path}")

    return documents
